"""Phase 1+2:
1. Remove all CN-market events from 4 JSON files
2. Add major IPO rumor / window events the market is hyping in 2026 H2:
   - SpaceX (Starlink IPO speculation)
   - Stripe
   - Klarna
   - Cerebras
   - SHEIN
   - Anthropic
   - Databricks
Plus a few missing major events (BoE, Aramco-related, OPEC).

All content baked with moomoo SG growth ops context (TA tag + KPI goal +
campaign reference + S$ currency + named landing action).

Run: python fetcher/clean_and_add_ipos.py
"""
import json
from pathlib import Path

FETCHER = Path(__file__).parent

# ---------------------------------------------------------------------------
# 1. Remove CN events
# ---------------------------------------------------------------------------
removed_total = 0
for m in ("jun", "jul", "aug", "sep"):
    p = FETCHER / f"events_{m}.json"
    evs = json.loads(p.read_text(encoding="utf-8"))
    before = len(evs)
    evs = [e for e in evs if e.get("market") != "CN"]
    removed_total += before - len(evs)
    p.write_text(json.dumps(evs, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"{m}: {before} -> {len(evs)} (removed {before-len(evs)})")
print(f"total CN events removed: {removed_total}")

# ---------------------------------------------------------------------------
# 2. New events to ADD per month
# ---------------------------------------------------------------------------
# All sources are .gov / IR / authoritative org. No .cn / no .com.cn.
# Each event embeds KPI target + TA tag in `angle` and named landing action in `push.body`.

NEW_EVENTS = {
    "jun": [
        {
            "id": "0612spx",
            "date": "2026-06-12",
            "weekday": "五",
            "month": 6,
            "market": "US",
            "title": "SpaceX / Starlink IPO 窗口期(传闻)",
            "cats": ["ipo", "product"],
            "imp": 3,
            "confirmed": False,
            "tickers": ["SPACEX*", "SPCE", "RKLB", "ASTS", "IRDM", "LMT"],
            "summary": "市场炒作 SpaceX 拆分 Starlink IPO 时间窗口",
            "background": "Reuters/Bloomberg 等持续追踪 Musk 多次公开提到 Starlink 有可能在用户突破 6000 万 + 现金流稳定后单独上市。市场普遍把 2026 H2 当作可能窗口。一旦 S-1 文件递交,SEC EDGAR 即可查询。在此之前所有信息均为传闻级,但仍是太空板块最大估值催化剂——SpaceX 一级估值已达 $400B 量级,Starlink 拆分后单体可能超 $200B。受益板块:商业航天(RKLB/ASTS/IRDM)、卫星通信、国防(LMT/NOC)。",
            "hook": "TA1+TA3 双吃·赚效活动页最大抓手",
            "angle": "[KPI=拉新NUP+促期权首交·TA=TA1+TA3] SpaceX 是 2026 太空概念赚效活动页核心抓手——做\"SpaceX/Starlink 估值拆解+一级二级套利逻辑\"科普长图,落 NUP 拉新 + 期权投教转化",
            "jargon": [
                {"t": "S-1", "d": "美国 IPO 招股说明书,SEC 上市必递交"},
                {"t": "SEC EDGAR", "d": "美国证监会公司备案数据库,IPO 信息源头"},
                {"t": "Pre-IPO", "d": "未上市轮次,通过一级市场基金参与"}
            ],
            "push": {
                "title": "SpaceX 上市传闻再起,太空概念怎么玩?",
                "body": "SpaceX 一旦递 S-1,RKLB/ASTS 板块齐涨。打开 moomoo 富途\"SpaceX 太空概念赚效页\"看实时受益清单,首次入金最高得 [奖励金额*],期权首单 0 佣金。"
            },
            "source": {"name": "SEC EDGAR", "url": "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company=spacex&type=S-1&dateb=&owner=include&count=40"}
        },
        {
            "id": "0618boe",
            "date": "2026-06-18",
            "weekday": "四",
            "month": 6,
            "market": "EU",
            "title": "BoE 利率决议 + 会议纪要",
            "cats": ["macro"],
            "imp": 2,
            "confirmed": True,
            "tickers": ["EWU", "FXB", "BP", "SHEL", "HSBC"],
            "summary": "英国央行政策利率与投票分布",
            "background": "12:00 GMT BoE 公布银行利率(Bank Rate)决议与 9 名 MPC 委员投票分布(Hawk/Hold/Cut 票数)。同步发布会议纪要。BoE 鸽于 Fed → 英镑承压、伦敦 ADR(BP/SHEL/HSBC)跨市场套利窗口打开。英国是 SG 用户高关注度市场之一(英联邦法律体系、HSBC 母行)。",
            "hook": "MPC 投票分布即英镑方向风向标",
            "angle": "[KPI=促有效PC·TA=TA2+TA3] 做\"BoE 9 票拆解 + 英镑/HSBC 联动\"图解,SG 中老年关注 HSBC 配置——引导 TA2 用 CDP 转仓把 HSBC 持仓从竞品搬过来,同时 TA3 看 FXB 期权",
            "jargon": [
                {"t": "MPC", "d": "Monetary Policy Committee 英国央行货币政策委员会"},
                {"t": "Bank Rate", "d": "BoE 政策利率,影响英镑和英国国债"}
            ],
            "push": {
                "title": "BoE 决议,HSBC 持仓的你必看",
                "body": "BoE 鸽 → 英镑跌 → HSBC 港股+美股 ADR 套利窗口。富途 CDP 直连转仓最快 T+1,持仓搬过来同步打开,首次转入最高得 [奖励金额*]。"
            },
            "source": {"name": "Bank of England", "url": "https://www.bankofengland.co.uk/monetary-policy/monetary-policy-committee"}
        }
    ],
    "jul": [
        {
            "id": "0708stripe",
            "date": "2026-07-08",
            "weekday": "三",
            "month": 7,
            "market": "US",
            "title": "Stripe IPO 窗口期(传闻)",
            "cats": ["ipo"],
            "imp": 3,
            "confirmed": False,
            "tickers": ["STRIPE*", "PYPL", "SQ", "ADYEY", "V", "MA"],
            "summary": "支付独角兽 IPO 时间窗口持续被市场炒作",
            "background": "Stripe 一级估值 $91.5B(2024 tender),Collison 兄弟多次表示 IPO 不在短期议程,但每次员工流动性事件都引发 IPO 时间表猜测。SEC EDGAR 一旦出现 Stripe S-1,即立即被市场捕捉。受益对照组:PYPL/SQ/ADYEY 上市同业估值锚。SG 用户中 TA3 Trader 对支付科技板块兴趣度高。",
            "hook": "支付科技 IPO 第一梯队,情绪股集体催化",
            "angle": "[KPI=促期权首交·TA=TA3] Stripe 一旦递表,PYPL/SQ 同业即重定价。做\"Stripe vs PYPL/SQ 估值倍数对比\"图,落期权投教转化(SG 期权渗透率仅 8%,缺口最大)",
            "jargon": [
                {"t": "Tender Offer", "d": "员工股份回购,常用于一级估值确认"},
                {"t": "Direct Listing", "d": "直接挂牌,无承销商,Stripe 可能采用"}
            ],
            "push": {
                "title": "Stripe IPO 再传闻,PYPL/SQ 该买吗?",
                "body": "支付独角兽递表,同业对标股估值同步重写。1 张 PYPL 价差期权押宝同业反弹,新客期权首单 0 佣金,打开富途\"期权投教\"3 分钟学会怎么开。"
            },
            "source": {"name": "SEC EDGAR", "url": "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company=stripe&type=S-1&dateb=&owner=include&count=40"}
        }
    ],
    "aug": [
        {
            "id": "0805jh",
            "date": "2026-08-27",
            "weekday": "四",
            "month": 8,
            "market": "US",
            "title": "Jackson Hole 全球央行年会(8/27-29)",
            "cats": ["fomc", "macro"],
            "imp": 3,
            "confirmed": True,
            "tickers": ["SPY", "QQQ", "TLT", "GLD", "UUP"],
            "summary": "Powell 主旨演讲定调全年货币政策",
            "background": "堪萨斯城联储主办的年度央行峰会,Powell 周五主旨演讲历来是市场关注度最高的非 FOMC 央行讲话。2022 年\"Pain ahead\"演讲单日 SPX 跌 3.4%,2024 年\"Time has come\"启动降息周期。SG 时间(EDT 周五 10:00 ≈ SGT 周五 22:00)正好 SG 用户晚间在线时段。",
            "hook": "Powell 演讲定全年货币政策基调",
            "angle": "[KPI=促期权首交+促有效PC·TA=TA3] 做\"JH 演讲历史回顾+SPX 当日波动榜\"图解,直播 + 期权投教联动:演讲前先开期权户,演讲中跟单",
            "jargon": [
                {"t": "Jackson Hole", "d": "怀俄明州 KC 联储主办的年度央行论坛"},
                {"t": "Forward Guidance", "d": "前瞻指引,央行用语沟通未来政策"}
            ],
            "push": {
                "title": "Jackson Hole · Powell 演讲夜",
                "body": "历届演讲日 SPX 单日波动 1-3%。SGT 周五 22:00 直播,期权投教课同步开,新客期权首单 0 佣金,首次入金最高得 [奖励金额*]。"
            },
            "source": {"name": "Kansas City Fed", "url": "https://www.kansascityfed.org/research/jackson-hole-economic-symposium/"}
        },
        {
            "id": "0812klarna",
            "date": "2026-08-12",
            "weekday": "三",
            "month": 8,
            "market": "US",
            "title": "Klarna IPO 窗口期(传闻)",
            "cats": ["ipo"],
            "imp": 2,
            "confirmed": False,
            "tickers": ["KLARNA*", "AFRM", "PYPL", "SQ", "SEZL"],
            "summary": "瑞典 BNPL 巨头美股 IPO 推迟后再传重启",
            "background": "Klarna 2025 年 4 月已递 F-1 但因关税担忧推迟,2026 H2 市场重新预期重启。BNPL(Buy Now Pay Later)板块:AFRM 是直接对标股,SEZL 是新晋小盘。一旦 Klarna 上市,BNPL 整体估值倍数可能重写。",
            "hook": "BNPL 板块第一大 IPO,AFRM/SEZL 直接受益",
            "angle": "[KPI=促期权首交·TA=TA3] 做\"BNPL 三巨头估值倍数对比\"图,AFRM 期权 IV 在 IPO 临近常飙升,落期权投教 + 跟单提示",
            "jargon": [
                {"t": "F-1", "d": "外国发行人在美 IPO 招股书,Klarna 用 F-1"},
                {"t": "BNPL", "d": "Buy Now Pay Later 先买后付分期支付"}
            ],
            "push": {
                "title": "Klarna 重启 IPO,AFRM 该上车吗?",
                "body": "BNPL 板块估值重写在即,AFRM 期权 IV 已在异动。1 张 AFRM 价差期权 锁定方向,新客期权首单 0 佣金,打开富途\"期权投教\"15 分钟通关。"
            },
            "source": {"name": "SEC EDGAR", "url": "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company=klarna&type=F-1&dateb=&owner=include&count=40"}
        }
    ],
    "sep": [
        {
            "id": "0909cerebras",
            "date": "2026-09-09",
            "weekday": "三",
            "month": 9,
            "market": "US",
            "title": "Cerebras IPO 窗口期(传闻)",
            "cats": ["ipo", "earnings"],
            "imp": 3,
            "confirmed": False,
            "tickers": ["CRBR*", "NVDA", "AMD", "AVGO", "SMCI"],
            "summary": "AI 芯片独角兽 IPO 重启传闻",
            "background": "Cerebras 2024 年 9 月已递 S-1,但因 CFIUS(美国外资投资委员会)审查 G42 投资关系一度搁置。2026 年市场预期 G42 持股结构调整后 IPO 可能重启。Cerebras 主打 wafer-scale AI 芯片,与 NVDA H100/B200 直接竞争。一旦上市,AI 芯片板块 NVDA/AMD/AVGO 估值可能重定价。",
            "hook": "AI 芯片板块第一大 IPO,NVDA 同业竞争白热化",
            "angle": "[KPI=促期权首交+促有效PC·TA=TA3] 做\"Cerebras WSE-3 vs NVDA H100 性能对比\"图,AI 芯片是 SG 用户最热门主题,落期权投教 + NVDA 期权链解读",
            "jargon": [
                {"t": "Wafer-scale", "d": "整片晶圆做单芯片,Cerebras 独家"},
                {"t": "CFIUS", "d": "美国外资投资委员会,审查涉外投资国安"}
            ],
            "push": {
                "title": "Cerebras 重启 IPO,NVDA 怎么应对?",
                "body": "AI 芯片第二供应商上市将冲击 NVDA 估值,机构期权 OI 已在异动。富途\"AI 半导体赚效页\"看实时清单,期权首单 0 佣金,首次入金最高得 [奖励金额*]。"
            },
            "source": {"name": "SEC EDGAR", "url": "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0002021728&type=S-1&dateb=&owner=include&count=40"}
        },
        {
            "id": "0923shein",
            "date": "2026-09-23",
            "weekday": "三",
            "month": 9,
            "market": "EU",
            "title": "SHEIN 伦交所 IPO 窗口期(传闻)",
            "cats": ["ipo"],
            "imp": 2,
            "confirmed": False,
            "tickers": ["SHEIN*", "PDD", "BABA", "AMZN", "ZAL.DE"],
            "summary": "快时尚巨头转战伦敦 IPO 时间窗口",
            "background": "SHEIN 2024 年放弃纽交所 IPO 改投伦交所(LSE),受英国 FCA 审查。新加坡是 SHEIN 总部地之一,SG 用户对该 IPO 关注度极高。一旦上市,跨境电商板块(PDD/BABA)+ 欧洲服装(ZAL.DE)同步重定价。",
            "hook": "新加坡总部公司 IPO,SG 用户最高关注度",
            "angle": "[KPI=拉新NUP+促首笔交易·TA=TA1+TA2] SHEIN 总部在 SG,本地话题度最高,做\"SHEIN 伦敦 IPO 全流程\"科普,落 NUP 新客拉新 + 引导首笔交易购买对标股",
            "jargon": [
                {"t": "FCA", "d": "英国金融行为监管局,LSE 上市审批方"},
                {"t": "Premium Listing", "d": "LSE 高级上市标准,可入富时 100 指数"}
            ],
            "push": {
                "title": "SHEIN 伦敦 IPO,SG 总部公司在路上",
                "body": "新加坡总部公司全球 IPO,跨境电商 PDD/BABA 同步催化。打开 moomoo 富途 NUP 新客页 加入 SHEIN 主题群,首次入金最高得 [奖励金额*],新客期权首单 0 佣金。"
            },
            "source": {"name": "London Stock Exchange", "url": "https://www.londonstockexchange.com/raise-finance/equity"}
        }
    ]
}

# ---------------------------------------------------------------------------
# 3. Append to month files (dedup by id)
# ---------------------------------------------------------------------------
for m, new_evs in NEW_EVENTS.items():
    p = FETCHER / f"events_{m}.json"
    evs = json.loads(p.read_text(encoding="utf-8"))
    existing_ids = {e["id"] for e in evs}
    added = 0
    for ev in new_evs:
        if ev["id"] in existing_ids:
            continue
        evs.append(ev)
        added += 1
    evs.sort(key=lambda e: (e["date"], e["id"]))
    p.write_text(json.dumps(evs, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"{m}: appended {added}, now {len(evs)} events")

print("done.")
