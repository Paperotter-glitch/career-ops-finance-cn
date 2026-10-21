# 招聘链接审计（2026-10-21）

Checked on 2026-10-21 from this environment: DNS via 1.1.1.1, then an HTTPS GET. A URL was replaced only when the response identified the same institution (page title, or a page the institution itself publishes). Entries with no verified official URL stay in the file with `enabled: false`. No domain was invented to fill a gap.

2026-10-21 在本环境核过：先用 1.1.1.1 查 DNS，再做 HTTPS GET。只有响应能对上同一家机构（页面标题，或机构自己公布的地址）才改链接。没核到官方地址的条目留在库里，`enabled: false`。没有为了补洞去编域名。

上游 career-ops 只扫描 `enabled` 不为 false 的条目。停用不是删除。

## 已更换

| 机构 | 新链接 | 依据 |
|---|---|---|
| 平安信托 | https://talent.pingan.com/ | 2026-10-21：原 www.jobs.pingan.com 无 A 记录。改为平安公开招聘站 talent.pingan.com（平安自己的说明页所载）。 |
| 招商证券 | https://cms.hotjob.cn/ | 2026-10-21：原 career.cmschina.com 无此主机名。公司在高校宣讲材料中写明的投递站为 cms.hotjob.cn，打开后跳到 hotjob 招聘页。 |
| 中信证券(华南 / 深圳分公司) | https://careers.citics.com/ | 2026-10-21：原 /newsite/hrzp/ 返回 HTTP 404。careers.citics.com 页面标题为「中信证券招聘」。 |
| 中金深圳子公司 | https://cicc.zhiye.com/ | 2026-10-21：原 career.cicc.com 无此主机名。公司招聘说明写明 cicc.zhiye.com，页面标题为「中金公司」。与中金香港共用该站。 |
| 南方基金 | https://www.nffund.com/ | 2026-10-21：原 /main/aboutNF/recruit/ 返回 HTTP 404。官网首页标题为「南方基金管理股份有限公司_南方基金官网」。另有高校就业网引用的 hotjob 地址，静态页未能确认机构名，未采用。 |
| 平安集团 | https://talent.pingan.com/ | 2026-10-21：原 pingan.zhiye.com 打开后落到 /404。改为平安公开招聘站 talent.pingan.com。 |
| 平安人寿 | https://talent.pingan.com/ | 2026-10-21：原 pingan.zhiye.com 打开后落到 /404。改为平安公开招聘站 talent.pingan.com，与集团条目共用。 |
| 招商局集团 | https://cmhk.zhiye.com/ | 2026-10-21：原 /main/c_zp/ 返回 HTTP 404。cmhk.zhiye.com 页面标题为「招商局集团招聘官网」。 |
| 大疆 - 法律 AI 产品 | https://careers.dji.com/zh-CN/ | 2026-10-21：原 we.dji.com/zh-CN/job 会跳到 careers.dji.com/zh-CN/。 |
| HSBC 汇丰(香港 / 深圳) | https://www.hsbc.com/careers | 2026-10-21：原 where-we-hire/china 返回 HTTP 404。汇丰招聘站首页 www.hsbc.com/careers 可打开。 |
| Standard Chartered 渣打(香港 / 深圳) | https://www.sc.com/en/global-careers/ | 2026-10-21：原 /en/careers/ 会跳到 global-careers，改为这个招聘入口。 |
| 中银香港 BOCHK | https://www.bochk.com/en/career.html | 2026-10-21：原 /sc/aboutus/careers.html 返回 HTTP 404。现招聘页为 /en/career.html，页面标题为 Career。 |
| 中银国际 | https://www.bocigroup.com/web/Inner/Inner/48 | 2026-10-21：原 /careers/ 会跳回网站首页。/web/Inner/Inner/48 页面标题为「中银国际」，栏目标题为人才招聘。 |
| 工银亚洲 | https://www.icbcasia.com/ | 2026-10-21：原带中文路径的 Career 地址返回 HTTP 404。官网首页可打开（标题含中国工商银行（亚洲）），未再核到单独招聘路径。 |
| 招商永隆银行 | https://www.cmbwinglungbank.com/wlb_corporate/en/about-us/careers/index.html | 2026-10-21：原 /wlbweb/jsp/career/ 返回 HTTP 404。现招聘页标题为 Careers - CMB Wing Lung Bank。 |
| AIA Hong Kong 友邦香港 | https://www.aia.com.hk/en/about-aia/careers | 2026-10-21：原 /zh-hk/careers.html 返回 HTTP 404。现页为 AIA Hong Kong Careers。 |
| 宏利保险 Manulife(香港) | https://careers.manulife.com/global/en | 2026-10-21：原 www.manulife.com/careers 会跳到 careers.manulife.com。 |
| 保诚保险 Prudential(香港) | https://www.prudential.com.hk/en/about-us/work-with-us/corporate-careers/ | 2026-10-21：原 /zh-hant/careers/ 返回 HTTP 404。现页标题为 Corporate Careers / Prudential HK。 |
| 中信证券国际(香港) | https://www.clsa.com/careers/ | 2026-10-21：原 citicsifg.com 整域不存在。公开招聘页标题为 Careers – CITIC CLSA，与库内中信里昂证券 CLSA 条目相同。 |
| 中金香港 | https://cicc.zhiye.com/ | 2026-10-21：原 career.cicc.com 无此主机名。与中金深圳共用 cicc.zhiye.com（页面标题「中金公司」）。 |
| 海通国际(香港) | https://www.htisec.com/zh-cn/careers | 2026-10-21：原 /zh-CN/career 返回 HTTP 404。/zh-cn/careers 页面标题为「海通国际证券集团有限公司 / 人才招聘」。 |
| 红杉中国香港 Sequoia China HK | https://www.hongshan.com/jobs/ | 2026-10-21：原 sequoiacap.cn/careers/ 无此主机名。hongshan.com/jobs 标题为「工作机会 - 红杉」。页内飞书招聘链接当时返回 404，未采用。机构名未改。 |
| 招商致远资本(招商证券旗下 PE) | https://cmscapital.cmschina.com/ | 2026-10-21：原 cmsc-pe.com 整域不存在。该公司网站声明官网为 cmscapital.cmschina.com，页面标题为「招商致远资本投资有限公司」。未见单独招聘页。 |
| 金石投资(中信证券股权投资) | https://www.goldstone-investment.com/ | 2026-10-21：原 citics-jinshi.com 整域不存在。goldstone-investment.com 页面标题为「中信金石投资有限公司」，文中写明为中信证券全资私募子公司。未见单独招聘页。 |
| 国信弘盛(国信证券旗下) | https://hs.guosen.com.cn/ | 2026-10-21：原 guosenhongsheng.com 整域不存在。国信证券子公司页面列出的官网为 hs.guosen.com.cn，标题为「国信弘盛」。该站使用旧式 TLS 重协商，部分客户端握手会失败。 |
| 国君创投(国泰君安创投) | https://gimcs.com/ | 2026-10-21：原 gtjavc.com 整域不存在。gimcs.com 页面标题为「国泰君安投资管理股份有限公司」，但证书已过期。是否与旧称国君创投为同一主体需再核对工商登记；这里只换已打开的公开网址，不改机构名。 |
| 招银国际 CMB International(招商银行海外旗舰) | https://www.cmbi.com.hk/zh-CN/society | 2026-10-21：原 /career/ 返回 HTTP 404。/zh-CN/society 页面标题为「社会招聘 - 招银国际金融有限公司」。 |
| 浦银国际控股(浦发银行海外) | https://www.spdbi.com/career.html | 2026-10-21：原 www.spdbintl.com 无此主机名。spdbi.com 首页含「浦银」，/career.html 返回 200。 |
| 中信资本 CITIC Capital(顶级中资 PE) | https://www.citiccapital.com/ | 2026-10-21：原 /careers/ 返回 HTTP 404。公司站首页可打开（标题含 Citic Capital），未见单独招聘页，暂用首页。 |
| 易方达基金(深圳总部) | https://job.efunds.com.cn/ | 2026-10-21：原 /recruit/ 返回 HTTP 404。公司应聘说明写明投递站为 job.efunds.com.cn，打开后跳到 hotjob。 |
| 博时基金(深圳总部) | https://www.bosera.com/ | 2026-10-21：原 /job/index.htm 会跳到官网首页。未见另一份已核验的内地招聘页，暂用首页。博时国际的香港招聘页是另一家主体，未拿来替换。 |
| 易方达资产管理 HK | https://www.efunds.com.hk/ | 2026-10-21：原 efundhk.com 整域不存在。efunds.com.hk 页面标题为 E Fund Management (Hong Kong) Co., Limited。 |
| 国调基金(中国国有企业结构调整基金) | https://www.cctfund.cn/cctfund/gywm55/gdjj/index.html | 2026-10-21：原 guodiao.com 无 A 记录。cctfund.cn 该页标题为「国调基金」，正文为中国国有企业结构调整基金。原备注把它写成国家集成电路产业投资基金管理人，与该页不符，已删，并去掉「半导体 + 战新」标签。此页严格 TLS 校验在本环境失败过一次，页面本身能打开。 |
| 五矿资本(中国五矿) | https://www.minmetals-finance.com/ | 2026-10-21：原 www.minmetalscapital.com 无此主机名。minmetals-finance.com 页面标题为「五矿资本股份有限公司」。未见单独招聘页。 |
| 深圳市引导基金 / 鲲鹏资本 | https://www.kpcapital.cn/ | 2026-10-21：原 kunpengcapital.cn 无此主机名。kpcapital.cn 页面标题为「深圳市鲲鹏股权投资管理有限公司」。未另核到独立的「深圳市引导基金」招聘页。 |
| 深圳市投控(深圳市投资控股) | https://www.sihc.com.cn/ | 2026-10-21：原 szic.com 整域不存在。sihc.com.cn 公司简介页自述网址为 www.sihc.com.cn，主体为深圳市投资控股有限公司。同旧域名下的「重大产业基金」和「VC/PE 引导基金」没有核到独立页面，已另停用。 |
| IDG Capital | https://career.idgcapital.com/index.html | 2026-10-21：原 /careers/ 返回 HTTP 404。career.idgcapital.com 页面标题为 IDG Capital。 |
| 基石资本(深圳) | https://stonevc.com/RecruitASage/index.aspx | 2026-10-21：原 cornerstonecapital.com.cn 整域不存在。stonevc.com 招聘页标题为「基石资产管理股份有限公司」。 |
| 同创伟业(深圳) | http://www.cowincapital.com.cn/index.php?a=recruit&c=index&m=goods | 2026-10-21：原 tcvinvest.com 整域不存在。cowincapital.com.cn 招聘页标题为「诚聘英才 - 同创伟业」。页面是 http，岗位信息看起来较旧，投递前请再核对。 |
| 中信信托深圳分部 | https://www.citictrust.com.cn/ | 2026-10-21：原 citictrust.com 无 A 记录。citictrust.com.cn 页面标题为「中信信托」（备案主体为中信信托有限责任公司）。 |
| 腾讯投资 Tencent Investment(独立于腾讯法务) | https://careers.tencent.com/ | 2026-10-21：原 tencent.com/zh-cn/careers.html 返回 HTTP 404。腾讯招聘站为 careers.tencent.com，与库内腾讯法务条目相同；未见投资部单独招聘站。 |
| 华为哈勃投资(半导体产业基金) | https://career.huawei.com/cn | 2026-10-21：原 career.huawei.com/ 会跳到 /cn。这是华为集团招聘站，不是哈勃单独的招聘页。 |
| 比亚迪战投 | https://job.byd.com/portal/pc/ | 2026-10-21：原 /cn/JoinByd.html 返回 HTTP 404。job.byd.com 页面标题为「比亚迪招聘」。这是集团招聘站，不是战投部单独页面。 |
| 顺丰投资 | https://hr.sf-express.com/index.jsp | 2026-10-21：原 /cn/sc/careers/ 返回 HTTP 404。hr.sf-express.com 页面标题为「顺丰人才招聘系统首页」。这是集团招聘站。 |
| 中兴投资 | https://job.zte.com.cn/cn/index.html | 2026-10-21：原 /china/about/recruitment.html 打开后是 404 页。job.zte.com.cn 页面标题为「中兴通讯招聘」。这是集团招聘站。 |
| TCL 创投 / 半导体基金 | https://zhaopin.tcl.com/index.html | 2026-10-21：原 /cn/zh/careers 返回 HTTP 404。zhaopin.tcl.com 页面标题为「TCL招聘」。这是集团招聘站，不是创投单独页面。 |
| 农银投资深圳分公司(农银金融资产投资) | https://www.abchina.com/cn/ | 2026-10-21：原 /cn/HumanResources/ 返回 HTTP 404。农业银行官网首页标题为「中国农业银行」。career.abchina.com 只返回标题 Loading 的空壳，未采用。 |
| 平安资产管理(深圳总部) | https://talent.pingan.com/ | 2026-10-21：原 www.pingan.com/careers/ 返回 HTTP 404。改为平安公开招聘站 talent.pingan.com。 |
| 人保资产深圳分公司 | https://www.picc.com.cn/recruit/ | 2026-10-21：原 picc.com/recruit/ 会跳到 picc.com.cn/recruit/，本环境收到 HTTP 403（更像拦截，不是 404），链接保留为跳转后的地址，未停用。 |
| 太保资产深圳分公司 | https://www.cpic.com.cn/ | 2026-10-21：原 /careers/ 返回 HTTP 404。官网首页标题含「中国太平洋保险」。未见已核验的单独招聘路径。 |
| 泰康资产深圳分公司 | https://www.taikang.com/ | 2026-10-21：原 /talent/ 返回 HTTP 404，job.taikang.com 无此主机名。官网首页标题为「泰康保险集团」。未见已核验的单独招聘路径。 |
| 平安海外控股(深圳 + HK) | https://talent.pingan.com/ | 2026-10-21：原链接是集团首页而不是招聘页。改为平安公开招聘站 talent.pingan.com。 |
| HSBC Private Banking HK | https://www.hsbc.com/careers | 2026-10-21：原 where-we-hire/asia-pacific/hong-kong-sar 返回 HTTP 404。改用汇丰招聘站首页，不是私人银行单独页面。 |
| 万科 BU / 万科基金 | https://www.vanke.com/ | 2026-10-21：原 hr.vanke.com 无此主机名，job.vanke.com 与 join.vanke.com 同样不存在。www.vanke.com 可打开，但是集团站首页，静态页几乎是脚本，未见单独的基金招聘页。 |
| 平安不动产 | https://talent.pingan.com/ | 2026-10-21：原链接是集团首页而不是招聘页。改为平安公开招聘站 talent.pingan.com。 |
| 香港特区政府投资基金 HKIC(Hong Kong Investment Corporation) | https://www.hkic.org.hk/ | 2026-10-21：原 hkic.hk 证书为自签名。hkic.org.hk 页面标题为 Hong Kong Investment Corporation Limited / HKIC。 |

## 已停用

| 机构 | 原因 |
|---|---|
| 工银国际 ICBC International | 2026-10-21：www.icbci.icbc.com.cn 无 A 记录。未核到可替换的官方招聘页，先停用。 |
| 国新基金深圳分部 | 2026-10-21：guoxinguotong.com 整域不存在。中国国新控股招聘栏目常见于 crhc.cn，但本环境因 TLS 密码套件和 403 没能打开该页，未采用，先停用。 |
| 国新国际(国新海外平台) | 2026-10-21：guoxinguotong.com 整域不存在。未核到可替换的官方页（crhc.cn 在本环境打不开），先停用。 |
| 国家集成电路产业基金深圳办(大基金) | 2026-10-21：gjjcdlcyjj.com 整域不存在。检索里出现的华芯资本 huaxcap.com 是另一家机构，不能拿来替换大基金，先停用。 |
| 远致投资(深圳市国资委直属) | 2026-10-21：shum-yip.com 整域不存在。未核到远致投资的官方站，先停用。 |
| 前海管理局相关基金 | 2026-10-21：szqh.gov.cn 整域不存在。qh.sz.gov.cn 有解析但 TLS 失败，未采用，先停用。 |
| 深圳市重大产业基金 | 2026-10-21：szic.com 整域不存在。深投控已另核到 sihc.com.cn，但没有核到「重大产业基金」自己的页面，不把投控首页算作本条，先停用。 |
| 深圳市 VC/PE 引导基金 | 2026-10-21：szic.com 整域不存在。没有核到该引导基金自己的页面，先停用。 |
| 重庆信托深圳分部 | 2026-10-21：chongqingtrust.com 整域不存在。cqiti.com 连接超时，未采用，先停用。 |
| 国寿安保资管深圳分公司 | 2026-10-21：cgbac.cn 整域不存在。未核到国寿安保资管的官方站（不把名称相近的其他国寿机构拿来替换），先停用。 |
| 深圳市天使母基金 | 2026-10-21：szangelfof.com 整域不存在。未核到官方站，先停用。 |
| 国家中小企业发展基金深圳办 | 2026-10-21：smefoundation.cn 整域不存在。未核到官方站，先停用。 |

## 未确认，保持启用

这些地址这次没能完成一次干净的访问，但也没有 404 或 NXDOMAIN。保持原链接和 `enabled: true`。

| 机构 | 链接 | 当时看到的情况 |
|---|---|---|
| 东方富海 | https://www.oceanpine.com.cn/ | TLS 握手超时，不能据此判死。 |
| 海通创新资本(海通证券旗下) | https://www.htsec.com/ | 站点拒绝现代 TLS 重协商，主机仍在。 |
| 建银国际 CCBI | https://www.ccbintl.com.hk/English/join.html | 证书校验失败，主机仍在。 |
| 交银国际 BoCom International | https://www.bocomgroup.com/ | 站点拒绝现代 TLS 重协商，主机仍在。 |
| 博裕资本 Boyu Capital | https://www.boyucapital.com/ | 证书校验失败，主机仍在。 |
| 松禾资本(深圳) | https://www.songhecapital.com/ | TLS 连接被对端提前断开，不能据此判死。 |
| Carlyle 凯雷(香港) | https://www.carlyle.com/careers | HTTP 403，更像拦截。 |
| Blackstone 黑石(香港) | https://www.blackstone.com/careers/ | HTTP 403，更像拦截。 |
| TPG(香港) | https://www.tpg.com/careers | HTTP 403，更像拦截。 |
| Warburg Pincus 华平(香港 / 深圳) | https://warburgpincus.com/careers/ | HTTP 403，更像拦截。 |
| 中海信托深圳分部 | https://www.shctrust.com/ | 读取超时，不能据此判死。 |
| 建信投资深圳分公司(建信金融资产投资) | https://www.ccb.com/cn/v3/include/aboutus/recruitment_/ | 站点拒绝现代 TLS 重协商。建行私人银行条目共用此链接。 |
| 交银投资深圳分公司(交银金融资产投资) | https://www.bankcomm.com/BankCommSite/shtml/jyzh/cn/7773/list.shtml | 站点拒绝现代 TLS 重协商。 |
| 建行私人银行深圳分行 | https://www.ccb.com/cn/v3/include/aboutus/recruitment_/ | 与建信投资条目相同，TLS 重协商失败。 |
| BNP Paribas Wealth Management HK | https://group.bnpparibas/en/careers | HTTP 403，更像拦截。 |
| 中海地产资管深圳分部 | https://www.coli.com.hk/ | 证书校验失败，主机仍在。 |
| 越秀房产信托(HK 上市) | https://www.yuexiureit.com/ | TLS 握手失败，不能据此判死。 |
| 中投公司海外(China Investment Corporation) | https://www.china-inv.cn/ | GET 返回 HTTP 405，主机仍在。 |
| 三峡资本(三峡集团旗下 PE) | https://www.ctgcapital.cn/ | 公共 DNS 返回 SERVFAIL，不是 NXDOMAIN，先保留。 |
| 诚通基金(中国诚通) | https://www.chengtong.cn/ | TLS 握手超时，不能据此判死。 |
| 中信集团(深港产业投资) | https://www.citic.com/ | HTTP 521（源站暂时不可用），不是 404。 |
| Pictet 瑞士百达(香港) | https://www.group.pictet/careers | 从本环境会跳到美国站 careers 页面，像是按访问地跳转，不能改成美国 URL。 |
