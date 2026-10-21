# 金融版用法说明

本仓是 [Career-Ops](https://github.com/career-ops-hq/career-ops) 的**金融配置包**，不是独立程序。`santifer/career-ops` 会跳到该仓库。

## 1. 先装 career-ops
按上游 README 装好框架（Node，以及它自带的 Go dashboard），跑通它的示例。

上游仓库现在在 [career-ops-hq/career-ops](https://github.com/career-ops-hq/career-ops)。`santifer/career-ops` 会 301 到那里。

## 2. 套上金融配置
```bash
cp portals.finance-cn.yml                 <career-ops>/portals.yml
cp config/profile.finance-cn.example.yml  <career-ops>/config/profile.yml   # 再填你自己的信息
```

## 3. 各 mode 在金融场景怎么用
| career-ops mode | 金融场景 |
|---|---|
| `scan` | 按 134 家金融机构 + 金融岗位词典扫岗位 |
| `apply` | 生成投递材料（简历 / 求职信），吃你的金融 profile |
| `pipeline` | 全流程：扫 → 匹配打分 → 投递 → 跟进 |
| `interview-prep` | 面试准备，结合你的 story-bank |
| `followup` | 投递后跟进 |

## 4. A → B 怎么扩
- **A（法律 / 合规，默认）**：profile 的 archetypes 用 投资法务 / 合规 / 风控；`title_filter` 已内置这些词。
- **B（泛金融）**：在 profile 加 投资 / 研究 / 投行 archetype；在 `portals.finance-cn.yml` 的 `title_filter.positive` 里加对应岗位词（如 "投资经理" / "行业研究" / "量化" / "投行"）。雇主库本身已覆盖全金融，无需改。

## 5. ⚠️ 隐私铁律
`config/profile.yml`、`cv.md`、`data/` 已被 `.gitignore` 排除——**永远不要提交你的真实个人数据**。只提交 `*.example` / `*.template`。

## 6. 和上游的兼容（2026-10-21 核对）

本仓仍是配置包。复制路径没变：`portals.finance-cn.yml` → 上游 `portals.yml`，profile 示例 → `config/profile.yml`。

对照过当天 `main` 上的 `validate-portals.mjs`、`templates/portals.example.yml`、`config/profile.example.yml` 和 `modes/zh/README.md`：

- 启用中的公司要有非空 `name` 和绝对 `careers_url`。`enabled` 必须是布尔值；只有 `false` 会让上游跳过该公司。本仓用它标记没核到招聘链接的 12 家，条目还在。
- `office_cities`、`tags`、`notes` 是本仓自己的字段。上游校验器不认识它们，也不会因为这些字段报错。
- `title_filter.positive` / `negative` / `seniority_boost` 和上游示例是同一种列表。
- 个人配置的语言键以 `config/profile.example.yml` 为准：`language.output: zh-CN`（中文输出，并启用中文 PDF 排版），`language.modes_dir: modes/zh`（内地市场模式）。`modes/zh/README.md` 里仍写着 `language.primary`，和 profile 示例不是同一个键。
- 中国简历用 A4。上游不写 `page_format` 时默认 letter，所以 profile 示例里写了 `page_format: a4`。
- 上游模式比本页表格里的 scan / apply / pipeline / interview-prep / followup 多。这五类会直接吃到雇主库和 profile；其余模式以上游文档为准，本仓没有各写一份。

雇主库改完可以用上游的 `node validate-portals.mjs --file portals.yml` 再对一次。本仓的 `python scripts/check_portals.py` 只检查这份金融配置自己的字段。
