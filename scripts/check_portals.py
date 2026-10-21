#!/usr/bin/env python3
"""Validate portals.finance-cn.yml and optionally probe careers URLs.

Schema checks are the pull-request gate. Live link checks classify each URL
and, with --fail-on-dead, fail only when an enabled entry is a confirmed
HTTP 404/410 or an unusable URL. DNS failures, TLS errors, timeouts, and
bot-blocks (401/403/429) are reported as unverified so a runner that cannot
reach a Chinese site does not fail the build.

Usage:
  python scripts/check_portals.py
  python scripts/check_portals.py --links --fail-on-dead
  python scripts/check_portals.py --write-tracker
"""

from __future__ import annotations

import argparse
import json
import socket
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

try:
    import yaml
except ImportError:
    print("需要 pyyaml：pip install pyyaml", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
PORTALS = ROOT / "portals.finance-cn.yml"
TRACKER = ROOT / "docs" / "投递追踪表.md"

REQUIRED_FIRM_FIELDS = ("name", "careers_url", "office_cities", "enabled", "tags")
TITLE_LISTS = ("positive", "negative", "seniority_boost")
DEAD_HTTP = {404, 410}
BLOCKED_HTTP = {401, 403, 429, 999}
ODD_HTTP = {405, 501}
USER_AGENT = (
    "Mozilla/5.0 (compatible; career-ops-finance-cn-linkcheck/1.0; "
    "+https://github.com/Paperotter-glitch/career-ops-finance-cn)"
)


def load_portals(path: Path = PORTALS) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("portals file must be a mapping")
    return data


def firms_of(data: dict) -> list[dict]:
    firms = data.get("tracked_companies")
    if not isinstance(firms, list):
        return []
    return [firm for firm in firms if isinstance(firm, dict)]


def _keyword_errors(values, path: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(values, list) or not values:
        errors.append(f"{path} 必须是非空字符串列表")
        return errors
    seen: set[str] = set()
    for index, value in enumerate(values):
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{path}[{index}] 必须是非空字符串")
            continue
        if value in seen:
            errors.append(f"{path} 有重复关键词 {value!r}")
        seen.add(value)
    return errors


def check_schema(data: dict) -> list[str]:
    """Return schema errors. Empty means the file is safe to copy into career-ops."""
    errors: list[str] = []
    title_filter = data.get("title_filter")
    if not isinstance(title_filter, dict):
        errors.append("缺少 title_filter 对象")
    else:
        unknown = sorted(set(title_filter) - set(TITLE_LISTS))
        if unknown:
            errors.append(f"title_filter 有未使用的字段：{', '.join(unknown)}")
        for key in TITLE_LISTS:
            errors.extend(_keyword_errors(title_filter.get(key), f"title_filter.{key}"))

    raw_firms = data.get("tracked_companies")
    if not isinstance(raw_firms, list) or not raw_firms:
        errors.append("tracked_companies 必须是非空列表")
        return errors

    seen_names: set[str] = set()
    for index, firm in enumerate(raw_firms):
        label = f"tracked_companies[{index}]"
        if not isinstance(firm, dict):
            errors.append(f"{label} 必须是对象")
            continue
        name = firm.get("name")
        if isinstance(name, str) and name.strip():
            label = name.strip()
            if label in seen_names:
                errors.append(f"{label}：机构名重复")
            seen_names.add(label)
        for key in REQUIRED_FIRM_FIELDS:
            if key not in firm:
                errors.append(f"{label}：缺字段 `{key}`")
        if "name" in firm and (not isinstance(firm.get("name"), str) or not firm["name"].strip()):
            errors.append(f"{label}：name 必须是非空字符串")
        url = firm.get("careers_url")
        if isinstance(url, str):
            try:
                normalize_url(url)
            except ValueError as exc:
                errors.append(f"{label}：careers_url 不可用（{exc}）")
        elif "careers_url" in firm:
            errors.append(f"{label}：careers_url 必须是字符串")
        cities = firm.get("office_cities")
        if "office_cities" in firm and (
            not isinstance(cities, list)
            or not cities
            or not all(isinstance(city, str) and city.strip() for city in cities)
        ):
            errors.append(f"{label}：office_cities 必须是非空字符串列表")
        tags = firm.get("tags")
        if "tags" in firm and (
            not isinstance(tags, list)
            or not tags
            or not all(isinstance(tag, str) and tag.strip() for tag in tags)
        ):
            errors.append(f"{label}：tags 必须是非空字符串列表")
        if "enabled" in firm and not isinstance(firm.get("enabled"), bool):
            errors.append(f"{label}：enabled 必须是布尔值 true/false")
        if firm.get("enabled") is False:
            notes = firm.get("notes")
            if not isinstance(notes, str) or not notes.strip():
                errors.append(f"{label}：enabled 为 false 时必须写 notes，说明为什么停用")
        notes = firm.get("notes")
        if "notes" in firm and notes is not None and not isinstance(notes, str):
            errors.append(f"{label}：notes 必须是字符串")
    return errors


def category_of(firm: dict) -> str:
    """Group a firm from tags already in the file. Residual firms stay in 其他."""
    tags = firm.get("tags") or []
    name = firm.get("name") or ""
    if any("猎头" in tag for tag in tags):
        return "猎头（非终端雇主）"
    if any("AIC" in tag for tag in tags):
        return "AIC 金融资产投资"
    if any("REIT" in tag or "地产" in tag for tag in tags):
        return "REITs / 地产基金"
    if any("引导" in tag or "母基金" in tag or "政府投资" in tag for tag in tags):
        return "政府引导 / 母基金"
    if any(tag == "私行" or "家办" in tag for tag in tags) or "私人银行" in name:
        return "家办 / 私行"
    if any("保险资管" in tag for tag in tags):
        return "保险资管"
    if any(tag == "保险" or tag.startswith("保险") for tag in tags):
        return "保险"
    if any("信托" in tag for tag in tags):
        return "信托"
    if any("CVC" in tag for tag in tags):
        return "产业投资 / CVC"
    if any("外资" in tag for tag in tags):
        return "外资机构"
    if any("公募" in tag for tag in tags):
        return "公募 / 公募系"
    if any("券商" in tag for tag in tags):
        return "券商 / 券商系"
    if any("银行" in tag for tag in tags) or "银行" in name:
        return "银行 / 银行系"
    if any(any(key in tag for key in ("央企", "国资", "国家级", "主权", "政府")) for tag in tags):
        return "国资 / 央企 / 政府平台"
    if any("PE" in tag or "VC" in tag for tag in tags):
        return "市场化 PE / VC"
    return "其他"


def category_counts(firms: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for firm in firms:
        name = category_of(firm)
        counts[name] = counts.get(name, 0) + 1
    return counts


def normalize_url(url: str) -> str:
    parts = urllib.parse.urlsplit(url.strip())
    if parts.scheme not in {"http", "https"} or not parts.hostname:
        raise ValueError("必须是绝对 http(s) URL")
    host = parts.hostname.encode("idna").decode("ascii")
    if parts.port:
        host = f"{host}:{parts.port}"
    if parts.username or parts.password:
        raise ValueError("不应包含用户名或密码")
    path = urllib.parse.quote(parts.path, safe="/%:@")
    query = urllib.parse.quote(parts.query, safe="=&%:/?+,%@")
    return urllib.parse.urlunsplit((parts.scheme, host, path, query, ""))


def _dns_failure(hostname: str) -> str | None:
    try:
        socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        # -2 NXDOMAIN, -5 no address. -3 is a temporary resolver failure.
        if exc.errno in {-2, -5}:
            return f"dns:{exc.errno}"
        return None
    return None


def classify_link(url: str, timeout: float = 15.0) -> dict:
    """Classify one careers URL. Network errors are unverified, not dead."""
    try:
        normalized = normalize_url(url)
    except ValueError as exc:
        return {"status": "dead", "http_status": None, "final_url": None, "detail": str(exc)}

    hostname = urllib.parse.urlsplit(normalized).hostname or ""
    dns_problem = _dns_failure(hostname)
    if dns_problem:
        return {
            "status": "dead",
            "http_status": None,
            "final_url": None,
            "detail": dns_problem,
        }

    context = ssl.create_default_context()
    headers = {"User-Agent": USER_AGENT, "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"}
    request = urllib.request.Request(normalized, method="GET", headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
            final_url = response.geturl()
            status = getattr(response, "status", 200)
            detail = "ok"
            kind = "redirected" if _url_key(final_url) != _url_key(normalized) else "ok"
            if _looks_like_soft_404(final_url) and not _looks_like_soft_404(normalized):
                kind = "dead"
                detail = f"soft-404:{final_url}"
            return {
                "status": kind,
                "http_status": status,
                "final_url": final_url,
                "detail": detail,
            }
    except urllib.error.HTTPError as exc:
        detail = f"http:{exc.code}"
        if exc.code in DEAD_HTTP:
            kind = "dead"
        elif exc.code in BLOCKED_HTTP:
            kind = "blocked"
        elif exc.code in ODD_HTTP or 500 <= exc.code <= 599:
            kind = "unverified"
        else:
            kind = "unverified"
        return {
            "status": kind,
            "http_status": exc.code,
            "final_url": exc.geturl(),
            "detail": detail,
        }
    except (TimeoutError, urllib.error.URLError, OSError, ssl.SSLError) as exc:
        return {
            "status": "unverified",
            "http_status": None,
            "final_url": None,
            "detail": f"{type(exc).__name__}:{exc}",
        }


def _url_key(url: str) -> str:
    parts = urllib.parse.urlsplit(url)
    path = parts.path.rstrip("/") or "/"
    return urllib.parse.urlunsplit(
        (parts.scheme.lower(), parts.netloc.lower(), path, parts.query, "")
    )


def _looks_like_soft_404(url: str) -> bool:
    path = urllib.parse.urlsplit(url).path.lower()
    return path.rstrip("/").endswith("/404") or path.lower() in {"/404.html", "/404"}


def check_links(firms: list[dict], timeout: float, workers: int = 12) -> list[dict]:
    results: list[dict | None] = [None] * len(firms)

    def probe(index: int, firm: dict) -> tuple[int, dict]:
        outcome = classify_link(firm.get("careers_url", ""), timeout=timeout)
        outcome["name"] = firm.get("name")
        outcome["url"] = firm.get("careers_url")
        outcome["enabled"] = firm.get("enabled")
        return index, outcome

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(probe, index, firm) for index, firm in enumerate(firms)]
        for future in as_completed(futures):
            index, outcome = future.result()
            results[index] = outcome
    return [item for item in results if item is not None]


def render_tracker(firms: list[dict]) -> str:
    lines = [
        "# 134 家中国 / 香港金融机构 · 投递追踪表",
        "",
        (
            "> 由 `python scripts/check_portals.py --write-tracker` "
            "从 `portals.finance-cn.yml` 生成。改雇主库，不要手改这张表。"
        ),
        (
            "> 「启用」为停用的条目仍留在库里，但 `enabled: false`，"
            "上游 career-ops 扫描会跳过。"
            "原因见 [2026-10-21 链接审计](link-audit-2026-10-21.md)。"
        ),
        "",
        "| # | 机构 | 城市 | 招聘页 | 启用 | 投递 |",
        "|--:|---|---|---|:--:|:--:|",
    ]
    for index, firm in enumerate(firms, start=1):
        cities = "/".join(firm.get("office_cities") or [])
        url = firm.get("careers_url") or ""
        state = "启用" if firm.get("enabled") else "停用"
        name = (firm.get("name") or "").replace("|", "/")
        lines.append(f"| {index} | {name} | {cities} | <{url}> | {state} | ☐ |")
    lines.append("")
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="校验 portals.finance-cn.yml")
    parser.add_argument("--file", type=Path, default=PORTALS, help="雇主库路径")
    parser.add_argument("--links", action="store_true", help="检查 careers_url 是否可访问")
    parser.add_argument("--timeout", type=float, default=12.0, help="单次 HTTP 超时（秒）")
    parser.add_argument(
        "--fail-on-dead",
        action="store_true",
        help="启用中的条目若确认是死链（HTTP 404/410、无 DNS、非法 URL）则失败",
    )
    parser.add_argument("--report", type=Path, help="把链接结果写成 JSON")
    parser.add_argument("--write-tracker", action="store_true", help="重写 docs/投递追踪表.md")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    data = load_portals(args.file)
    firms = firms_of(data)
    title_filter = data.get("title_filter") or {}
    positives = title_filter.get("positive") or []
    negatives = title_filter.get("negative") or []
    boosts = title_filter.get("seniority_boost") or []
    print(
        f"共 {len(firms)} 家机构；岗位词 {len(positives)} 正向 / "
        f"{len(negatives)} 排除 / {len(boosts)} 资历加权"
    )
    counts = category_counts(firms)
    for name, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        print(f"  {count:3}  {name}")

    errors = check_schema(data)
    if errors:
        print("Schema 校验失败：")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Schema 校验通过")

    if args.write_tracker:
        TRACKER.write_text(render_tracker(firms), encoding="utf-8")
        print(f"已重写 {TRACKER.relative_to(ROOT)}")

    if not args.links:
        return 0

    results = check_links(firms, timeout=args.timeout)
    if args.report:
        args.report.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"已写入 {args.report}")

    buckets: dict[str, list[dict]] = {}
    for result in results:
        buckets.setdefault(result["status"], []).append(result)
    for status in ("ok", "redirected", "blocked", "unverified", "dead"):
        rows = buckets.get(status, [])
        print(f"{status}: {len(rows)}")
        if status in {"dead", "unverified", "blocked"}:
            for row in rows:
                flag = "enabled" if row.get("enabled") else "disabled"
                print(f"  - [{flag}] {row['name']}  {row['detail']}  {row['url']}")

    if args.fail_on_dead:
        dead_enabled = [row for row in buckets.get("dead", []) if row.get("enabled") is not False]
        if dead_enabled:
            print(f"启用中的死链 {len(dead_enabled)} 条")
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
