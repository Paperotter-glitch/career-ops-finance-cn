## 做了什么 / What changed

<!-- 一次 PR 最好只动一家机构，或只做一件维护事项。 -->

## 雇主数据 / Employer data

- [ ] 没有改 `portals.finance-cn.yml`
- [ ] 改了，而且 `careers_url` 是我打开过的官方页面（请贴最终 URL）
- [ ] 链接死了但没找到替代，已设 `enabled: false` 并在 `notes` 里写了原因
- [ ] 跑过 `python scripts/check_portals.py`，需要的话也跑了 `--write-tracker`

替代链接：

核验方式（打开了哪个页面、标题是什么）：

## 检查 / Checks

- [ ] `ruff check scripts tests`
- [ ] `python -m unittest discover -s tests`
- [ ] 没有提交 `config/profile.yml`、`cv.md` 或其他个人材料
