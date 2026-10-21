<div align="center">

# 💼 Career-Ops Finance-CN

### 中国私募 · 金融行业 AI 求职系统

**别再给上百家机构海投简历。<br>让 AI 从 <kbd>134 家</kbd> 中国 / 香港私募 · 投资机构里，替你挑出真正值得投的那几家。**

*"金融/私募版的 [career-ops](https://github.com/santifer/career-ops)" —— 券商用 AI 筛简历；这个工具把 AI 交给金融人，反过来去 **挑** 机构。*

<img src="docs/demo.svg" width="680" alt="扫 134 家金融机构 → A-F 打分 → 筛出对口岗位 → 生成投递草稿">

[![career-ops](https://img.shields.io/github/stars/career-ops-hq/career-ops?style=flat&label=career-ops&logo=github)](https://github.com/career-ops-hq/career-ops)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![雇主库](https://img.shields.io/badge/%E9%9B%87%E4%B8%BB%E5%BA%93-134%E5%AE%B6-e8b04b)
![岗位词典](https://img.shields.io/badge/%E5%B2%97%E4%BD%8D%E8%AF%8D-54%20%2F%2013%20%2F%209-5cc2a8)
![数据](https://img.shields.io/badge/%E6%95%B0%E6%8D%AE-%E5%8F%AF%E5%AF%BC%E5%87%BA%20%C2%B7%20%E6%B0%B8%E4%B8%8D%E4%B8%8A%E4%BA%91-8957e5)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

**简体中文** · [English](README.en.md)

</div>

---

> **⭐ 先点个 Star** —— 134 家雇主库每逢更新（新机构 / 新招聘季 / 新面经）你会第一时间看到，也方便日后找回来。

## 目录
[这是什么](#这是什么) · [缘起](#缘起) · [覆盖版图](#️-覆盖版图--别处没有的东西) · [怎么用](#-怎么用) · [真实场景](#-它能帮你做什么) · [隐私](#-你的数据永远是你的) · [路线](#-定位与路线-a--b) · [一起做全](#-一起把它做全) · [致谢](#-致谢--license)

## 这是什么

[Career-Ops](https://github.com/career-ops-hq/career-ops) 是开源的 AI 求职系统（旧地址 [santifer/career-ops](https://github.com/santifer/career-ops) 会跳到这里）。它本身不带中国金融圈的雇主和岗位词：不知道某家信托的招聘页在哪，也不知道「投资法务」该怎么筛。

**Career-Ops Finance-CN 把它武装成懂中国私募 / 金融行业的样子：**

- 📇 **134 家机构雇主库** —— 每家带 careers 链接、办公城市、行业标签。2026-10-21 核链接之后，**停用 12 家**（`enabled: false`，仍留在库里）
- 🎯 **中英双语岗位筛选词典：正向 54、排除 13、资历加权 9** —— 投资法务 / 合规 / 风控，外加少量相邻词。三列加总是 76，不是 76 个正向词
- 🀄 **中文金融求职 & 面试模式** + 金融方向 Profile 模板

> 一句话：**career-ops 是引擎，这里是给中国金融人的燃料。**

## 缘起

> 这个项目源于一次真实的中国金融求职。
> 与其给上百家机构海投、石沉大海，不如让 AI 从对口的机构里精挑几家、逐一打透。
> 作者把求职时打磨出来的这套配置，**脱敏后开源**——
> 因为在找工作那会儿，市面上没有一个真正懂中国金融圈的这种工具。

## 🗺️ 覆盖版图 —— 别处没有的东西

下面的家数由 `scripts/check_portals.py` 按现有 `tags` 归类，CI 会核对，不是另做的一套分类。加总为 134。

| 类别 | 家数 |
|---|---:|
| 国资 / 央企 / 政府平台 | 18 |
| 券商 / 券商系 | 15 |
| 外资机构 | 12 |
| 市场化 PE / VC | 12 |
| 公募 / 公募系 | 10 |
| 家办 / 私行 | 9 |
| 银行 / 银行系 | 9 |
| 产业投资 / CVC | 8 |
| REITs / 地产基金 | 7 |
| 其他 | 7 |
| AIC 金融资产投资 | 6 |
| 信托 | 6 |
| 保险资管 | 5 |
| 政府引导 / 母基金 | 5 |
| 保险 | 4 |
| 猎头（非终端雇主） | 1 |

「其他」是标签对不上上面类目的 7 家：平安集团、大疆（法律 AI）、腾讯（法务 / 合规）、中银香港、中银国际、工银亚洲、嘉实国际。

**覆盖城市：深圳 · 香港**（主战场）+ 北京 · 上海。2026-10-21 的链接核验见 [docs/link-audit-2026-10-21.md](docs/link-audit-2026-10-21.md)。不是每条都有独立来源链接。

## ⚡ 怎么用

三步上手（配置包，套在 career-ops 上）：

```bash
# 1) 先装 career-ops（见它的 README）
# 2) 套上金融配置
cp portals.finance-cn.yml                 <career-ops>/portals.yml
cp config/profile.finance-cn.example.yml  <career-ops>/config/profile.yml   # 填你自己的信息
# 3) 在你的 AI CLI（Claude Code / Codex / Gemini …）里跑：
#    scan（扫岗）→ apply（生成投递）→ followup（跟进）→ interview-prep（面试准备）
```

完整用法见 [docs/USAGE.finance.md](docs/USAGE.finance.md)。

## 🎯 它能帮你做什么

- **应届 / 在读**：一次扫清 134 家的在招岗，AI 按你的背景打分排序，把有限的精力压到最对口的头部私募 / 券商资管上，而不是海投石沉大海。
- **卖方转买方**：用配置包对齐十几家资管 / PE 的 JD 关键词，简历按"deal 经验"重构，面试前用 interview-prep 过一遍买方常问。
- **法律 / 合规背景**：内置投资法务 / 合规 / 风控的岗位词典，直接命中信托 / 基金 / PE 的法务合规岗——这套通用求职工具永远不会有。

## 🔒 你的数据永远是你的

金融求职最敏感的就是隐私。本工具**全程本地运行**：

- 你的简历、deal 记录、求职意向 —— **只留在你本地 / 你的账户**
- 投递材料一律 **draft-only**，绝不自动提交、绝不替你点"申请"
- 雇主库、配置包**可随时导出**，不锁定
- **永不上云**

> 你的 deal 数据和求职意向，不该是别人训练数据的一部分。

## 🧭 定位与路线（A → B）

- **现在（A）**：金融 **法律 / 合规 / 投资法务** 方向 —— 先做深、做可信。
- **成长为 B**：投资 / 研究 / 投行 / 风控 全覆盖 —— 雇主库已就位，扩岗位词即可。

## 🤝 一起把它做全

中国金融圈的雇主信息变化快。目标是做成中文金融圈**最全、最新**的求职雇主库——靠大家一起维护：

- 🏢 **补一家机构** / 🔗 **报个失效链接** / 🏷️ **补岗位词** → 提 [Issue](https://github.com/Paperotter-glitch/career-ops-finance-cn/issues/new/choose) 或 PR（一次一家，评审快）
- 🎉 **用它拿到金融 offer 了？** 开个 Issue 分享你的故事（可匿名），帮下一个人
- 📋 招聘链接以 [2026-10-21 审计](docs/link-audit-2026-10-21.md) 为准。PR 会跑字段校验、单元测试和 lint；活链接检查会把启用中的确认死链（HTTP 404/410 或 DNS 无记录）标成失败。403、超时和证书错误只报告，不当成死链

## 💬 社区 & 免费资料

**仓库里就有的开放资料**（欢迎 PR 一起补）：
- 📚 [金融面经题库](resources/金融面经题库.md) —— 投行 / PE·VC / 研究 / **投资法务·合规** / 风控 / 香港岗
- 📐 [估值建模模板](resources/估值建模模板.md) —— DCF / 可比公司 / LBO + 金融机构特殊估值
- 📋 [134 家投递追踪表](docs/投递追踪表.md) —— 从雇主库一键导出

关注公众号 **［待建号后填］** 领 **打包 PDF 版 + 更新推送**（回复 `面经` / `估值` / `清单`）。
> 📱 二维码待建号后放 `docs/qrcode.png` ｜ 小红书 / 知乎 ［待填］ 同步金融求职干货。

## 🙏 致谢 & License

构建于 **[Career-Ops](https://github.com/career-ops-hq/career-ops)** by [@santifer](https://x.com/santifer)（MIT）。旧地址 `santifer/career-ops` 会跳到这个仓库。若本项目对你有用，也去给上游点个 star。本仓同样以 **MIT** 发布，详见 [NOTICE.md](NOTICE.md)。变更记录见 [CHANGELOG.md](CHANGELOG.md)。

> ⚠️ 雇主库仅供求职参考；招聘信息以各机构官方渠道为准。数据均来自公开渠道，不含任何非公开信息。
