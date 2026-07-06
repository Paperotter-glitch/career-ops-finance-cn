# 金融版用法说明

本仓是 [Career-Ops](https://github.com/santifer/career-ops) 的**金融配置包**，不是独立程序。

## 1. 先装 career-ops
按上游 README 装好框架（Node / Go），跑通它的示例。

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
