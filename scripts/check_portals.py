#!/usr/bin/env python3
"""校验 portals.finance-cn.yml：字段完整性（硬性）+ careers_url 死链检测（软性）。

用法：
  python scripts/check_portals.py           # 只校验 schema（PR 门禁）
  python scripts/check_portals.py --links   # 额外抽查链接可达性
"""
from __future__ import annotations

import ssl
import sys
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:
    print("需要 pyyaml：pip install pyyaml", file=sys.stderr)
    sys.exit(2)

PORTALS = Path(__file__).resolve().parent.parent / "portals.finance-cn.yml"
REQUIRED = ("name", "careers_url")


def collect_firms(data) -> list[dict]:
    """从嵌套结构里收集所有"机构条目"（同时含 name 和 careers_url 的 dict）。"""
    firms: list[dict] = []

    def walk(node):
        if isinstance(node, dict):
            if "name" in node and "careers_url" in node:
                firms.append(node)
            else:
                for v in node.values():
                    walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(data)
    return firms


def check_schema(firms: list[dict]) -> list[str]:
    errors: list[str] = []
    for f in firms:
        for key in REQUIRED:
            if not f.get(key):
                errors.append(f"{f.get('name', '?')}：缺必填字段 `{key}`")
    return errors


def link_ok(url: str) -> bool:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    headers = {"User-Agent": "Mozilla/5.0 (finance-career-ops link check)"}
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers=headers)
            with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
                return resp.status < 400
        except Exception:
            continue
    return False


def main() -> int:
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

    if "--links" in sys.argv:
        dead = [f["name"] for f in firms if not link_ok(f["careers_url"])]
        if dead:
            print(f"⚠️ {len(dead)}/{len(firms)} 个招聘链接抽查不可达（可能是反爬，不作硬失败）：")
            for name in dead:
                print("  -", name)
        else:
            print("✅ 招聘链接抽查全部可达")

    return 0


if __name__ == "__main__":
    sys.exit(main())
