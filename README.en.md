<div align="center">

# Career-Ops Finance-CN

### A China / Hong Kong finance job-search pack

Chinese is the primary README. This page is the English version of the same repository.

[简体中文](README.md) · **English**

[![career-ops](https://img.shields.io/github/stars/career-ops-hq/career-ops?style=flat&label=career-ops&logo=github)](https://github.com/career-ops-hq/career-ops)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

</div>

This repository is a finance configuration pack for [career-ops](https://github.com/career-ops-hq/career-ops). It is not a separate application. The old URL `santifer/career-ops` redirects to that repository.

What it adds:

- **134 employer records** for China / Hong Kong finance: a careers URL, office cities, and tags. After the 2026-10-21 link check, **12 disabled** records remain in the file with `enabled: false`.
- **Role dictionary: 54 positive, 13 negative, and 9 seniority-boost keywords**, in Chinese and English, aimed at investment legal, compliance, and risk, plus a few adjacent titles.
- A finance profile example and notes for using career-ops on mainland and Hong Kong roles.

There are no usage statistics, testimonials, or star counts stored in this repo. The career-ops badge above is GitHub's live star shield.

## What is in the employer file

Counts come from the `tags` already on each record, via `category_of` in `scripts/check_portals.py`. CI checks this table. The groups sum to 134.

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

「其他」is the residual: 平安集团, DJI (legal AI), Tencent (legal / compliance), BOCHK, BOC International, ICBC Asia, and Harvest Global Investments. Their tags do not match the labels above.

Cities are mostly Shenzhen and Hong Kong, plus Beijing and Shanghai. The link audit is [docs/link-audit-2026-10-21.md](docs/link-audit-2026-10-21.md). Records do not each carry their own source URL.

## Use

```bash
# 1. Install career-ops (see its README).
# 2. Copy this pack in.
cp portals.finance-cn.yml                 <career-ops>/portals.yml
cp config/profile.finance-cn.example.yml  <career-ops>/config/profile.yml
# 3. In your AI CLI: scan, apply, followup, interview-prep.
```

Details and the upstream compatibility notes are in [docs/USAGE.finance.md](docs/USAGE.finance.md). `enabled: false` entries stay in the database and are skipped by the career-ops scanner.

## Privacy

The tool is meant to run locally. Do not commit `config/profile.yml`, `cv.md`, or `data/`. Those paths are in `.gitignore`. Application materials are drafts; this pack does not submit applications for you.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). One firm per pull request. Do not invent a careers URL. If you cannot verify an official page, leave the record disabled and say why in `notes`.

Pull requests run lint, unit tests, schema validation, and a live link check. An enabled URL fails that check when it is a confirmed dead link (HTTP 404/410, a soft 404, or no DNS address). HTTP 403, timeouts, and TLS errors are reported and do not fail the build.

## License

MIT. This pack is a derivative of career-ops. See [LICENSE](LICENSE), [NOTICE.md](NOTICE.md), and [CHANGELOG.md](CHANGELOG.md).

Employer records are for job search only. Hiring information belongs to each institution's own channels. The data here is from public pages and contains no non-public information.
