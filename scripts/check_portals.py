#!/usr/bin/env python3
"""校验 portals.finance-cn.yml：字段完整性（硬性）+ careers_url 死链检测（软性）。

用法：
  python scripts/check_portals.py           # 只校验 schema（PR 门禁）
  python scripts/check_portals.py --links   # 额外抽查链接可达性
"""
from __future__ import annotations

import argparse
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:
    print("需要 pyyaml：pip install pyyaml", file=sys.stderr)
    sys.exit(2)

PORTALS = Path(__file__).resolve().parent.parent / "portals.finance-cn.yml"
REQUIRED = ("name", "careers_url")
LINK_TIMEOUT = 15.0
SOFT_REACHABLE_STATUS = {401, 403, 429, 999}
HEAD_UNSUPPORTED_STATUS = {405, 501}


def collect_firms(data) -> list[dict]:
    """从嵌套结构里收集所有疑似"机构条目"。"""
    firms: list[dict] = []

    def walk(node, in_list: bool = False):
        if isinstance(node, dict):
            looks_like_firm = (
                any(key in node for key in REQUIRED)
                or (in_list and bool({"office_cities", "enabled", "tags"} & node.keys()))
            )
            if looks_like_firm:
                firms.append(node)
            else:
                for v in node.values():
                    walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v, in_list=True)

    walk(data)
    return firms


def check_schema(firms: list[dict]) -> list[str]:
    errors: list[str] = []
    if not firms:
        errors.append("未找到任何机构条目（至少需要包含 `name` 或 `careers_url`）")
        return errors

    for f in firms:
        label = f.get("name") or f.get("careers_url") or "?"
        for key in REQUIRED:
            value = f.get(key)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{label}：缺必填字段 `{key}`")
    return errors


def normalize_url(url: str) -> str:
    parts = urllib.parse.urlsplit(url)
    if parts.scheme not in {"http", "https"} or not parts.netloc:
        raise ValueError("careers_url must be an absolute http(s) URL")
    netloc = parts.netloc.encode("idna").decode("ascii")
    path = urllib.parse.quote(parts.path, safe="/%:@")
    query = urllib.parse.quote(parts.query, safe="=&%:/?+,%@")
    return urllib.parse.urlunsplit((parts.scheme, netloc, path, query, parts.fragment))


def link_ok(url: str, timeout: float = LINK_TIMEOUT) -> bool:
    try:
        url = normalize_url(url)
    except ValueError:
        return False

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    headers = {"User-Agent": "Mozilla/5.0 (finance-career-ops link check)"}
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
                return resp.status < 400
        except urllib.error.HTTPError as exc:
            if method == "HEAD" and exc.code in HEAD_UNSUPPORTED_STATUS:
                continue
            if exc.code in SOFT_REACHABLE_STATUS:
                return True
        except (TimeoutError, urllib.error.URLError, OSError, ValueError):
            continue
    return False


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="校验 portals.finance-cn.yml")
    parser.add_argument("--links", action="store_true", help="额外抽查 careers_url 可达性")
    parser.add_argument(
        "--timeout",
        type=float,
        default=LINK_TIMEOUT,
        help="单次 HTTP 请求超时时间（秒）",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    data = yaml.safe_load(PORTALS.read_text(encoding="utf-8"))
    firms = collect_firms(data)
    print(f"共 {len(firms)} 家机构")

    errors = check_schema(firms)
    if errors:
        print("❌ Schema 校验失败：")
        for e in errors:
            print("  -", e)
        return 1
    print("✅ Schema 校验通过")

    if args.links:
        dead = [
            f["name"]
            for f in firms
            if not link_ok(f["careers_url"], timeout=args.timeout)
        ]
        if dead:
            print(f"⚠️ {len(dead)}/{len(firms)} 个招聘链接抽查不可达（可能是反爬，不作硬失败）：")
            for name in dead:
                print("  -", name)
        else:
            print("✅ 招聘链接抽查全部可达")

    return 0


if __name__ == "__main__":
    sys.exit(main())
