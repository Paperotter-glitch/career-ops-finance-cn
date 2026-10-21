# Changelog

本文件记录对本仓库有影响的改动。版本号只用于这里和 `pyproject.toml`，没有单独发布到包索引。

## 0.2.0 — 2026-10-21

维护更新。没有新增雇主，没有改 MIT 许可证。

- 核了全部 134 条 `careers_url`。能对上同一家机构官方页面的，改成新地址；对不上的 12 家设为 `enabled: false` 并写明原因。名单在 [docs/link-audit-2026-10-21.md](docs/link-audit-2026-10-21.md)。
- 改正一条错误备注：国调基金是中国国有企业结构调整基金，不是国家集成电路产业投资基金的管理人。
- `scripts/check_portals.py` 现在检查字段、岗位词、停用必须有 notes，并能按 404/410、DNS 无记录、403、超时给链接分类。`docs/投递追踪表.md` 由该脚本生成。
- 加上单元测试。GitHub Actions 在 PR 上跑 ruff、测试、schema，以及会让启用中的确认死链失败的链接检查。
- 补上英文 README。中文 README 仍是主文档，并去掉已经对不上的星数、类目家数和「76+ 正向词」。
- 补上 `CHANGELOG.md`、`SECURITY.md`、`CODE_OF_CONDUCT.md`、PR 模板和失效链接 Issue 模板。
- 用法说明按 2026-10-21 的上游 `career-ops-hq/career-ops` 改过：仓库已从 `santifer/career-ops` 跳转过去，profile 使用 `language.output` 和 `modes/zh`。

## 0.1.0 — 2026-07-06

首次公开：134 家雇主库、金融岗位词、profile 示例，以及字段校验脚本。
