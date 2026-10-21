# 贡献指南

目标：把这份雇主库做成中文金融圈**最全、最新**的一份。欢迎两类贡献——**补数据**和**分享经历**，非技术背景也能提。

## 一、补充 / 修正一家机构（最有价值）

**最简单**：开一个 [「补充机构」Issue](../../issues/new/choose)，填表单即可，我们来落库。

**会 Git 的**：直接改 `portals.finance-cn.yml`，**一次 PR 只加 / 改一家**（评审快、少冲突）。字段规范：

```yaml
- name: "机构全称"                    # 必填。用法定/通用名，别加个人批注
  careers_url: "https://..."          # 必填。官网招聘页优先
  office_cities: ["深圳", "香港"]      # 必填。该机构实际办公城市
  enabled: true                       # 默认 true
  tags: ["券商系私募", "中信系"]        # 中性行业标签；别放个人优先级
  source_url: "https://..."           # 建议。让别人能核验（官网/监管公示/牌照页）
  last_verified: "2026-07"            # 建议。你核验链接有效的年月
```

### 收录标准（重要 —— 这是可信度的命脉）
- ✅ 收：**中国内地 / 香港**的私募 · 资管 · 券商 · 信托 · 银行 · 保险资管 · PE/VC · 引导基金等**持牌 / 正规金融机构**，且有公开招聘渠道。
- ❌ 不收：无法核验的机构、明显停业、纯个人工作室、与金融招聘无关的公司。
- ⚠️ 猎头 / FA 可收，但须标 `tags: ["猎头公司"]` 注明"非终端雇主"。

## 二、分享你的经历 🎉

用它找到工作、或攒了金融面经？开一个 [「上岸 / 面经」Issue](../../issues/new/choose)，**可完全匿名**，不用透露真实身份或点名机构。你的一条经验，就是下一个人的社会证明。

## 三、隐私铁律（所有贡献者必读）
- **绝不提交任何个人真实数据**：`config/profile.yml`、`cv.md`、`data/` 已被 `.gitignore` 排除，请勿绕过。
- 只提交 `*.example` / `*.template` 和公开的机构信息。
- 机构条目里**不要**写任何个人化批注（"我投过""前东家""内推路径"等）。

## 四、行为准则

友善、就事论事。数据类分歧以「能否公开核验」为准。完整文本见 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。安全问题走 [SECURITY.md](SECURITY.md)，不要把简历或 token 发到公开 Issue。

## 五、改完怎么自测

```bash
python -m pip install -r requirements-dev.txt
ruff check scripts tests
python -m unittest discover -s tests -v
python scripts/check_portals.py
python scripts/check_portals.py --write-tracker   # 改了雇主库才需要
```

`enabled: false` 的机构必须有 `notes`。不要编造招聘链接：打不开、又找不到机构自己的页面，就停用并写原因。

PR 上的 GitHub Actions 会跑 lint、单元测试、schema，以及活链接检查。启用中的确认死链（HTTP 404/410 或 DNS 无记录）会让检查失败；403、超时和证书错误只会记在日志里。

## English

Contributions are data fixes and short docs. One firm per pull request. A careers URL has to be a page you opened. If you cannot find an official page, set `enabled: false` and explain that in `notes`. Do not commit a real profile or CV. Run the commands in section 五 before opening a PR. The code of conduct is [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
