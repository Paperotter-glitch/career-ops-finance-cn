"""Schema, tracker, audit, and link-classification tests. No live HTTP."""

from __future__ import annotations

import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_portals  # noqa: E402

AUDIT = ROOT / "docs" / "link-audit-2026-10-21.md"
README = ROOT / "README.md"
README_EN = ROOT / "README.en.md"


def _section(text: str, heading: str) -> str:
    start = text.index(heading)
    rest = text[start + len(heading) :]
    nxt = rest.find("\n## ")
    return rest if nxt < 0 else rest[:nxt]


def _table(section: str) -> list[list[str]]:
    rows = []
    for line in section.splitlines():
        if not line.startswith("|") or line.startswith("|---") or line.startswith("| 机构"):
            continue
        rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
    return rows


class PortalFileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = check_portals.load_portals()
        cls.firms = check_portals.firms_of(cls.data)

    def test_real_file_schema(self):
        self.assertEqual(check_portals.check_schema(self.data), [])
        self.assertEqual(len(self.firms), 134)

    def test_keyword_counts_match_readmes(self):
        title_filter = self.data["title_filter"]
        self.assertEqual(len(title_filter["positive"]), 54)
        self.assertEqual(len(title_filter["negative"]), 13)
        self.assertEqual(len(title_filter["seniority_boost"]), 9)
        readme = README.read_text(encoding="utf-8")
        english = README_EN.read_text(encoding="utf-8")
        self.assertIn("正向 54", readme)
        self.assertIn("排除 13", readme)
        self.assertIn("资历加权 9", readme)
        self.assertIn("54 positive", english)
        self.assertIn("13 negative", english)
        self.assertIn("9 seniority", english)

    def test_category_table_matches_tags(self):
        counts = check_portals.category_counts(self.firms)
        self.assertEqual(sum(counts.values()), 134)
        for path in (README, README_EN):
            text = path.read_text(encoding="utf-8")
            for name, count in counts.items():
                self.assertIn(f"| {name} | {count} |", text, path.name)

    def test_tracker_is_generated_from_yaml(self):
        expected = check_portals.render_tracker(self.firms)
        self.assertEqual(check_portals.TRACKER.read_text(encoding="utf-8"), expected)
        self.assertIn("| 停用 |", expected)
        self.assertEqual(expected.count("| 停用 |"), 12)

    def test_audit_matches_database(self):
        text = AUDIT.read_text(encoding="utf-8")
        updated = _table(_section(text, "## 已更换"))
        disabled = _table(_section(text, "## 已停用"))
        unverified = _table(_section(text, "## 未确认，保持启用"))
        by_name = {firm["name"]: firm for firm in self.firms}

        self.assertEqual(len(updated), 56)
        self.assertEqual(len(disabled), 12)
        for name, url, _note in updated:
            self.assertIn(name, by_name)
            self.assertEqual(by_name[name]["careers_url"], url)
            self.assertTrue(by_name[name]["enabled"])
        disabled_names = {row[0] for row in disabled}
        self.assertEqual(
            disabled_names,
            {firm["name"] for firm in self.firms if firm["enabled"] is False},
        )
        for name, url, _note in unverified:
            self.assertIn(name, by_name)
            self.assertEqual(by_name[name]["careers_url"], url)
            self.assertTrue(by_name[name]["enabled"])

    def test_readmes_do_not_repeat_retired_claims(self):
        for path in (README, README_EN):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("57k", text)
            self.assertNotIn("76+", text)
            self.assertNotIn("English（WIP）", text)
            self.assertNotIn("每条数据都带", text)


class SchemaTests(unittest.TestCase):
    def _base(self) -> dict:
        return {
            "title_filter": {
                "positive": ["合规"],
                "negative": ["实习"],
                "seniority_boost": ["Senior"],
            },
            "tracked_companies": [
                {
                    "name": "示例资本",
                    "careers_url": "https://example.com/jobs",
                    "office_cities": ["深圳"],
                    "enabled": True,
                    "tags": ["PE"],
                }
            ],
        }

    def test_rejects_bad_url_and_disabled_without_notes(self):
        data = self._base()
        data["tracked_companies"][0]["careers_url"] = "not a url"
        data["tracked_companies"].append(
            {
                "name": "停用但没写原因",
                "careers_url": "https://example.com/other",
                "office_cities": ["香港"],
                "enabled": False,
                "tags": ["PE"],
            }
        )
        errors = check_portals.check_schema(data)
        self.assertTrue(any("careers_url" in error for error in errors))
        self.assertTrue(any("notes" in error for error in errors))

    def test_rejects_string_false_and_duplicate_names(self):
        data = self._base()
        data["tracked_companies"][0]["enabled"] = "false"
        data["tracked_companies"].append(dict(data["tracked_companies"][0]))
        errors = check_portals.check_schema(data)
        self.assertTrue(any("布尔" in error for error in errors))
        self.assertTrue(any("重复" in error for error in errors))


class LinkClassificationTests(unittest.TestCase):
    def _classify(self, urlopen):
        with (
            mock.patch.object(check_portals, "_dns_failure", return_value=None),
            mock.patch("urllib.request.urlopen", urlopen),
        ):
            return check_portals.classify_link("https://example.com/jobs", timeout=1)

    def test_http_404_is_dead(self):
        def urlopen(*_args, **_kwargs):
            raise urllib.error.HTTPError("https://example.com/jobs", 404, "missing", {}, None)

        result = self._classify(urlopen)
        self.assertEqual(result["status"], "dead")
        self.assertEqual(result["http_status"], 404)

    def test_http_403_is_blocked_not_dead(self):
        def urlopen(*_args, **_kwargs):
            raise urllib.error.HTTPError("https://example.com/jobs", 403, "blocked", {}, None)

        self.assertEqual(self._classify(urlopen)["status"], "blocked")

    def test_timeout_is_unverified(self):
        def urlopen(*_args, **_kwargs):
            raise TimeoutError("timed out")

        self.assertEqual(self._classify(urlopen)["status"], "unverified")

    def test_dns_nxdomain_is_dead(self):
        with mock.patch.object(check_portals, "_dns_failure", return_value="dns:-2"):
            result = check_portals.classify_link("https://missing.example/jobs", timeout=1)
        self.assertEqual(result["status"], "dead")

    def test_soft_404_final_url_is_dead(self):
        class Response:
            status = 200

            def geturl(self):
                return "https://example.com/404"

            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

        self.assertEqual(self._classify(lambda *_a, **_k: Response())["status"], "dead")

    def test_normalize_quotes_unicode_path(self):
        url = check_portals.normalize_url(
            "https://www.example.com/ICBC/海外分行/Career/"
        )
        self.assertTrue(url.startswith("https://www.example.com/"))
        self.assertNotIn("海外", url)
        self.assertIn("%E6%B5%B7%E5%A4%96", url)

    def test_cli_schema_only_on_temp_file(self):
        data = (
            "title_filter:\n"
            "  positive: ['合规']\n"
            "  negative: ['实习']\n"
            "  seniority_boost: ['Senior']\n"
            "tracked_companies:\n"
            "  - name: 示例\n"
            "    careers_url: https://example.com/jobs\n"
            "    office_cities: ['深圳']\n"
            "    enabled: true\n"
            "    tags: ['PE']\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "portals.yml"
            path.write_text(data, encoding="utf-8")
            self.assertEqual(check_portals.main(["--file", str(path)]), 0)


if __name__ == "__main__":
    unittest.main()
