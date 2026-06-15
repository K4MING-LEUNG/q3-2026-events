"""Calendar v5:
A. Strip [KPI=...·TA=...] prefix from every existing angle; keep marketing prose.
B. Add multi-market coverage (HK / SG / JP / KR / TW) for Q3 2026.

Run: python fetcher/enrich_v5.py
"""
import json
import re
from datetime import date
from pathlib import Path

FETCHER = Path(__file__).parent
WD = {0: "一", 1: "二", 2: "三", 3: "四", 4: "五", 5: "六", 6: "日"}

# ---------------------------------------------------------------------------
# A. Strip [KPI=...·TA=...] prefix from angle
# ---------------------------------------------------------------------------
RE_KPI = re.compile(r"^\[KPI=[^\]]+\]\s*")

# ---------------------------------------------------------------------------
# B. New multi-market events
#
# Sources (every URL audited):
#   - HKEX, HKMA, official issuer IR (Tencent, Alibaba HK, BABA US ADR via SEC)
#   - SGX, MAS, DBS/OCBC/UOB IR
#   - JPX, BOJ, official issuer IR (Toyota, SoftBank, Sony)
#   - BOK (Bank of Korea), KRX, Samsung IR
#   - Taiwan Stock Exchange (TWSE)
# ---------------------------------------------------------------------------
NEW_EVENTS = [
    # ===== HK 港股 =====
    {
        "id": "0701hkhol", "date": "2026-07-01", "weekday": "三", "month": 7, "market": "HK",
        "title": "香港回归纪念日 港股全天休市", "cats": ["holiday"], "imp": 1, "confirmed": True,
        "tickers": [],
        "summary": "港股全天休市,A 股/美股 ADR 正常",
        "background": "7/1 是香港特别行政区成立纪念日,法定公众假期。HKEX 全天休市,沪深港通南北向交易暂停。但腾讯/阿里/美团等的美股 ADR 正常交易,可作为夜盘对冲口径。",
        "hook": "港股休市,ADR 是唯一价格发现窗口",
        "angle": "假期前一晚把 BABA/JD/PDD/BIDU 等美股 ADR 加入富途自选,休市当晚 ADR 异动直接预演周四开盘 Gap;借\"港股休市单一价格发现\"的稀缺性做新客拉新内容,推到 SG 华人圈层",
        "jargon": [{"t": "ADR", "d": "美国存托凭证,中概股美股版"}, {"t": "南北向", "d": "沪深港通跨境交易"}],
        "push": {"title": "港股 7/1 休市,ADR 是唯一窗口", "body": "港股休市当晚,BABA/JD/PDD 美股 ADR 是唯一价格信号。打开 moomoo 富途自选添加,夜盘异动手机直推,新客首次入金最高 S$[奖励金额*]。"},
        "source": {"name": "HKEX", "url": "https://www.hkex.com.hk/Services/Trading-hours-and-Severe-Weather-Arrangements/Trading-Hours/Securities-Market"}
    },
    {
        "id": "0813tcehy", "date": "2026-08-13", "weekday": "四", "month": 8, "market": "HK",
        "title": "腾讯 Tencent (700.HK) Q2 财报", "cats": ["earnings"], "imp": 3, "confirmed": True,
        "tickers": ["0700.HK", "TCEHY", "BABA", "META"],
        "summary": "中国互联网最大权重股季度业绩",
        "background": "腾讯港股盘后(港股 16:00 后)发业绩+电话会。重点:游戏/广告/金融科技/云四分项收入、海外游戏占比、回购节奏(2025 全年回购千亿港币级)、AI 投入指引。腾讯一只占恒指权重 8%+,业绩单日恒指波动幅度常 1.5%+。SG 华人圈层关注度极高。",
        "hook": "恒指权重股 +AI 资本开支双线索",
        "angle": "腾讯财报夜联动美股 META 同业对比图,做\"东西方互联网两大巨头 ARPU/广告/AI 资本开支\"对照长图,在 SG 华人 KOL 渠道(小红书/抖音)同步分发,把华人客群引到平台开港股户",
        "jargon": [{"t": "恒指权重", "d": "腾讯占恒指 8%+,单股影响指数走势"}, {"t": "回购", "d": "公司用现金回购股份,EPS 提升"}],
        "push": {"title": "腾讯财报夜,恒指权重股大考", "body": "腾讯一只动恒指 1.5%+,SG 华人圈最关注的财报。打开 moomoo 富途港股开户,T+1 当日交易,新客港股佣金 0,首次入金最高 S$[奖励金额*]。"},
        "source": {"name": "Tencent IR", "url": "https://www.tencent.com/en-us/investors.html"}
    },
    {
        "id": "0820baba", "date": "2026-08-20", "weekday": "四", "month": 8, "market": "HK",
        "title": "阿里巴巴 Alibaba (9988.HK / BABA) Q1 FY27 财报", "cats": ["earnings"], "imp": 3, "confirmed": True,
        "tickers": ["9988.HK", "BABA", "JD", "PDD"],
        "summary": "中国电商龙头季度业绩 + 云资本开支",
        "background": "阿里港股盘后 + 美股盘前同步披露。重点:淘天 GMV 同比、AIDC 海外电商增速、阿里云 AI 收入(已超百亿人民币年化)、Capex 指引。BABA 是 SG 用户中概股第一持仓股之一,业绩夜港 ADR 双地价差是套利窗口。",
        "hook": "AI 云收入指引 + 港 ADR 套利窗口",
        "angle": "阿里财报 90 分钟内港股+美股 ADR 双地定价,做\"双地价差套利\"科普视频:同一只股票,港股户用 HKD/SGD 入场更省汇兑——SG 用户主打的 CDP 转仓正好就是这条路径",
        "jargon": [{"t": "AIDC", "d": "阿里国际数字商业,海外电商引擎"}, {"t": "双地上市", "d": "同一公司同时在港/美交易"}],
        "push": {"title": "阿里财报夜,港 ADR 价差套利", "body": "BABA 港股+美股 ADR 同夜披露,价差套利窗口仅 1-2 小时。CDP 直连转仓最快 T+1,首次转入最高 S$[奖励金额*],新客港股佣金 0。"},
        "source": {"name": "Alibaba Group IR", "url": "https://www.alibabagroup.com/en-US/ir-financial-reports-quarterly-results"}
    },
    {
        "id": "0925midautumn", "date": "2026-09-25", "weekday": "五", "month": 9, "market": "HK",
        "title": "中秋节前夕 港股半日市", "cats": ["holiday"], "imp": 1, "confirmed": True,
        "tickers": [],
        "summary": "港股 9/25 半日市,9/26-28 连放 3 天",
        "background": "2026 年中秋节为周六 9/26,港股周五 9/25 半日市(上午开盘,中午 12:00 收市),周一 9/28 中秋节翌日补假休市。SG 同步过中秋,本地华人氛围浓厚,营销窗口黄金日。",
        "hook": "节日 + 半日市 + SG 华人黄金窗口",
        "angle": "把港股 9/25 半日市做成\"中秋限时仓位整理\"主题页,推 SG 华人客群:节前用 CDP 转仓把竞品持仓搬过来过节,文案配中秋元素;同步上线\"中秋赚效页\"叠加月饼/灯笼/旅游受益股(美高梅/银河/利福国际)清单",
        "jargon": [{"t": "半日市", "d": "港股仅上午交易,12:00 收市"}],
        "push": {"title": "中秋港股半日市,节日仓位整理", "body": "9/25 港股 12 点收市,周末连放 3 天。CDP 直连转仓节前完成,中秋赚效页同步上线,首次转入最高 S$[奖励金额*]。"},
        "source": {"name": "HKEX", "url": "https://www.hkex.com.hk/Services/Trading-hours-and-Severe-Weather-Arrangements/Trading-Hours/Securities-Market"}
    },

    # ===== SG 星股 =====
    {
        "id": "0807dbs", "date": "2026-08-07", "weekday": "五", "month": 8, "market": "SG",
        "title": "DBS Group (D05.SI) Q2 财报", "cats": ["earnings"], "imp": 3, "confirmed": True,
        "tickers": ["D05.SI", "O39.SI", "U11.SI", "STI"],
        "summary": "新加坡最大银行季度业绩",
        "background": "DBS 是新加坡市值最大上市公司、STI 第一权重股。Q2 财报披露净息差(NIM)、贷款增长、财富管理(WM)收入、不良率(NPL)。SG 银行三大行(DBS/OCBC/UOB)CDP 持仓在 SG 居民中渗透极高,任何业绩波动都会触发本地用户主动看持仓。",
        "hook": "SG 居民第一持仓股,本地话题度满分",
        "angle": "DBS 是 99% SG 客户的本地核心持仓——业绩夜推送给已开 CDP 户但未在 moomoo 交易的客户,引导通过 CDP 直连转仓 5 秒看到完整持仓 + DBS 美股替代标的(如 BAC/JPM)对比",
        "jargon": [{"t": "NIM", "d": "净息差,银行核心盈利指标"}, {"t": "STI", "d": "海峡时报指数,SG 蓝筹基准"}],
        "push": {"title": "DBS 财报夜,SG 第一权重股", "body": "DBS 是 SG 居民最高持仓,业绩波动直接影响你账户。CDP 直连转仓 T+1 把 DBS 持仓搬过来对照实时盘,首次转入最高 S$[奖励金额*]。"},
        "source": {"name": "DBS Group IR", "url": "https://www.dbs.com/investors/financials/results-and-presentations.page"}
    },
    {
        "id": "0809ndp", "date": "2026-08-09", "weekday": "日", "month": 8, "market": "SG",
        "title": "新加坡国庆日 SGX 周一 8/10 休市", "cats": ["holiday"], "imp": 1, "confirmed": True,
        "tickers": [],
        "summary": "8/9 周日国庆,8/10 周一 SGX 休市",
        "background": "新加坡国庆日 8/9 周日,法定公假顺延至周一 8/10,SGX 全天休市。STI 不交易,但本地居民活动度激增。同期美股 8/10 周一正常交易。",
        "hook": "本地最大节日 + 长周末 + 居民高活时段",
        "angle": "把国庆做成 NUP 拉新主活动——参考 2025 SG60 单场 3.6 万 PC 的成功模板,做\"国庆 61 主题礼包\"+ 限时 0 佣金 + 国庆赠股(本地热门美股),配合实体店周末活动联动落地",
        "jargon": [{"t": "STI", "d": "海峡时报指数"}, {"t": "NDP", "d": "National Day Parade 国庆庆典"}],
        "push": {"title": "国庆 61 周年!Moo 限时礼包上线", "body": "国庆当周 SGX 休市,正好把美股账户开起来。NUP 国庆主题页限时礼包 + 美股赠股,新客首次入金最高 S$[奖励金额*]。"},
        "source": {"name": "SGX", "url": "https://www.sgx.com/securities/trading-hours-calendar"}
    },
    {
        "id": "0918stirebal", "date": "2026-09-18", "weekday": "五", "month": 9, "market": "SG",
        "title": "STI 半年度成份股调整生效", "cats": ["index"], "imp": 2, "confirmed": True,
        "tickers": ["STI", "ES3.SI", "G3B.SI"],
        "summary": "海峡时报指数 9 月再平衡生效日",
        "background": "STI 由 FTSE Russell + SGX 联合管理,每年 3 月/9 月各一次半年度成份股审核,通常 9 月第三个周五收市后生效。被纳入/剔除的股票当日成交量常翻 5-10 倍,被动 ETF(ES3.SI / G3B.SI)集中调仓。",
        "hook": "STI 调仓日 + 被动资金集中冲量",
        "angle": "调仓夜推送 SG 居民中老年客群——他们大多通过 CDP 持有 ES3.SI(STI ETF),调仓直接影响他们的被动配置;做\"STI 调仓影响 + 中老年资产跟进策略\"内容,引导 TA2 看 CDP 直连看完整持仓",
        "jargon": [{"t": "再平衡", "d": "指数半年度调整成份股权重"}, {"t": "ES3.SI", "d": "STI ETF 最大被动跟踪基金"}],
        "push": {"title": "STI 9 月调仓,被动资金大冲量", "body": "STI 调仓夜 ES3.SI 成交翻 5 倍,你的 CDP 持仓在被动重写。CDP 直连转仓 T+1 看完整持仓,首次转入最高 S$[奖励金额*]。"},
        "source": {"name": "FTSE Russell · STI", "url": "https://www.ftserussell.com/products/indices/sti"}
    },

    # ===== JP 日股 =====
    {
        "id": "0805toyota", "date": "2026-08-05", "weekday": "三", "month": 8, "market": "JP",
        "title": "丰田 Toyota (7203.T) Q1 FY27 财报", "cats": ["earnings"], "imp": 2, "confirmed": True,
        "tickers": ["7203.T", "TM", "DXJ", "EWJ"],
        "summary": "日股最大市值股季度业绩",
        "background": "丰田日本盘前发业绩。重点:全球销量、北美/中国市场分项、混动 vs 纯电策略、日元汇率敏感度(每弱 1 日元利润 +500 亿)。日股权重股,业绩日 EWJ/DXJ ETF 单日波动放大。SG 用户对日本制造业熟悉度高。",
        "hook": "日股权重股 + 日元汇率敏感度第一",
        "angle": "丰田业绩夜把\"日元贬值 vs 丰田利润\"敏感度做成可视化(每弱 1 日元 +500 亿利润),引导 SG 用户用 DXJ(对冲日元 ETF)+ TM(美股 ADR)双管道布局——开日股户通过 moomoo 富途一键完成",
        "jargon": [{"t": "DXJ", "d": "WisdomTree 日股对冲日元 ETF"}, {"t": "FY27 Q1", "d": "丰田财年 4-3 月,Q1=4-6 月"}],
        "push": {"title": "丰田财报夜,日股权重股大考", "body": "日元每弱 1 日元 = 丰田 +500 亿利润,业绩日 EWJ/DXJ 同步异动。打开 moomoo 富途开日股户,新客佣金 0,首次入金最高 S$[奖励金额*]。"},
        "source": {"name": "Toyota IR", "url": "https://global.toyota/en/ir/library/financial-results/"}
    },
    {
        "id": "0811sftbk", "date": "2026-08-11", "weekday": "二", "month": 8, "market": "JP",
        "title": "软银集团 SoftBank Group (9984.T) Q1 财报", "cats": ["earnings"], "imp": 2, "confirmed": True,
        "tickers": ["9984.T", "SFTBY", "ARM", "BABA"],
        "summary": "Vision Fund 持仓估值 + ARM 影响",
        "background": "软银日本盘后发业绩。Vision Fund 1+2 持仓中 ARM(英国半导体,美股已上市)、Coupang、滴滴等定价直接影响净资产。软银本身持有阿里 ~20% 仓位,Vision Fund 浮盈/浮亏单季度可达万亿日元。",
        "hook": "Vision Fund 估值夜 + ARM/BABA 联动",
        "angle": "做\"软银持仓地图\"图解(ARM 30%/Alibaba 20%/Coupang 10% 等),引导 SG 用户通过 ARM/BABA/CPNG 美股 ADR 间接获取 Vision Fund 暴露——美股开户这条路对 SG 用户最熟",
        "jargon": [{"t": "Vision Fund", "d": "软银千亿规模科技投资基金"}, {"t": "ARM", "d": "软银控股的英国芯片 IP 公司"}],
        "push": {"title": "软银财报夜,Vision Fund 估值揭晓", "body": "ARM/Coupang/BABA 持仓集中定价,SFTBY 单日波动常 5%+。打开 moomoo 富途自选 ARM/BABA/CPNG,1 张 ARM 价差期权押方向,期权首单 0 佣金。"},
        "source": {"name": "SoftBank Group IR", "url": "https://group.softbank/en/ir"}
    },

    # ===== KR 韩股 =====
    {
        "id": "0707samsung", "date": "2026-07-07", "weekday": "二", "month": 7, "market": "KR",
        "title": "三星电子 Samsung (005930.KS) Q2 业绩 Guidance", "cats": ["earnings"], "imp": 2, "confirmed": True,
        "tickers": ["005930.KS", "EWY", "FLKR"],
        "summary": "三星季度业绩预告(完整业绩月底),HBM/Foundry 信号",
        "background": "三星 2026 年 Q2 业绩 Guidance(预告)韩国时间盘后发布,通常仅披露营收 + 营业利润总数,完整分项 7 月底正式财报。市场重点解读 HBM(高带宽内存,AI 芯片关键)+ Foundry(代工)是否扭亏。三星一只占 KOSPI 权重 25%+,Guidance 单日 KOSPI 波动常 1.5%+。",
        "hook": "AI 内存板块第一信号 + KOSPI 权重大佬",
        "angle": "三星 HBM 信号直接联动美股 NVDA/MU/SK Hynix——做\"AI 内存供应链拆解\"图(NVDA H100 → SK Hynix 60% + Samsung 30% + Micron 10%),引导 SG 用户用 EWY 韩股 ETF 一键暴露,免去单股选择",
        "jargon": [{"t": "HBM", "d": "高带宽内存,AI 芯片必需"}, {"t": "Foundry", "d": "晶圆代工,三星追赶 TSMC"}],
        "push": {"title": "三星 Guidance,AI 内存第一信号", "body": "三星 HBM 信号直接联动 NVDA/MU,KOSPI 单日波动 1.5%+。打开 moomoo 富途自选 EWY/MU/SK Hynix ADR,新客美股佣金 0,首次入金最高 S$[奖励金额*]。"},
        "source": {"name": "Samsung IR", "url": "https://www.samsung.com/global/ir/financial-information/earnings-release/"}
    },
    {
        "id": "0828bok", "date": "2026-08-28", "weekday": "五", "month": 8, "market": "KR",
        "title": "韩国央行 BOK 利率决议", "cats": ["macro"], "imp": 2, "confirmed": True,
        "tickers": ["EWY", "FLKR", "005930.KS"],
        "summary": "BOK 政策利率与韩元方向",
        "background": "韩国央行(Bank of Korea)货币政策委员会 8 月会议公布基准利率,周五上午 KST 09:00 决议 + 11:00 行长记者会。当前利率 2.75%,2025 年已累计降息 75bp。BOK 鸽于 Fed → 韩元贬值 → 出口大盘(三星/现代/SK 海力士)受益。",
        "hook": "韩元方向 = 出口板块直接定价",
        "angle": "BOK 决议联动\"韩元贬值利好出口股\"叙事,做\"BOK vs Fed 利差变化 → 韩元 → 三星/现代利润\"传导链科普,引导 SG 用户用 EWY ETF + 005930 单股双管道布局",
        "jargon": [{"t": "BOK", "d": "Bank of Korea 韩国央行"}, {"t": "韩元贬值", "d": "出口股利好,进口/航空利空"}],
        "push": {"title": "BOK 决议,韩元方向定出口股", "body": "BOK 鸽 → 韩元贬 → 三星/现代利润 +。打开 moomoo 富途自选 EWY,1 张 EWY 看涨期权押韩元贬值,期权首单 0 佣金,首次入金最高 S$[奖励金额*]。"},
        "source": {"name": "Bank of Korea", "url": "https://www.bok.or.kr/eng/main/main.do"}
    },
]

# ---------------------------------------------------------------------------
# Apply
# ---------------------------------------------------------------------------
WD_VERIFY = WD  # alias

for m in ("jun", "jul", "aug", "sep"):
    p = FETCHER / f"events_{m}.json"
    evs = json.loads(p.read_text(encoding="utf-8"))

    # A. strip [KPI=...] prefix from existing angle
    for e in evs:
        e["angle"] = RE_KPI.sub("", e.get("angle", ""))

    # B. add new events for this month
    existing_ids = {e["id"] for e in evs}
    for ne in NEW_EVENTS:
        if ne["month"] != ({"jun": 6, "jul": 7, "aug": 8, "sep": 9}[m]):
            continue
        if ne["id"] in existing_ids:
            continue
        # weekday verify
        y, mo, d = map(int, ne["date"].split("-"))
        actual = WD[date(y, mo, d).weekday()]
        if ne["weekday"] != actual:
            print(f"  WARN weekday mismatch {ne['id']}: claim {ne['weekday']} actual {actual}; auto-fix")
            ne["weekday"] = actual
        evs.append(ne)

    evs.sort(key=lambda e: (e["date"], e["id"]))
    p.write_text(json.dumps(evs, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"{m}: {len(evs)} events (after enrich)")

# ---------------------------------------------------------------------------
# C. Final audit
# ---------------------------------------------------------------------------
print("\n--- audit ---")
all_evs = []
for m in ("jun", "jul", "aug", "sep"):
    all_evs += json.loads((FETCHER / f"events_{m}.json").read_text(encoding="utf-8"))

# weekday check
errs = []
for e in all_evs:
    y, mo, d = map(int, e["date"].split("-"))
    actual = WD[date(y, mo, d).weekday()]
    if e["weekday"] != actual:
        errs.append((e["id"], e["date"], e["weekday"], actual))
print(f"weekday errors: {len(errs)}")
for x in errs:
    print(" ", x)

# leftover [KPI prefix
left = [e["id"] for e in all_evs if RE_KPI.match(e.get("angle", ""))]
print(f"events still with [KPI=...]: {len(left)}")

# market distribution
from collections import Counter
mkt = Counter(e["market"] for e in all_evs)
print(f"markets: {dict(mkt)}")
print(f"TOTAL: {len(all_evs)} events")
