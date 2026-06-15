"""Phase 3: Rewrite all events' angle + push to embed [KPI=...·TA=...] tag and
named moomoo SG campaign landing actions.

Rules:
- angle starts with [KPI=X·TA=Y]
- push.body names a campaign: NUP / Referral 裂变中心 / CDP 直连转仓 /
  期权投教 / 赚效活动页 / MooFest / Moo庄园
- 货币 S$, 奖励金额一律占位 [奖励金额*]
- TA: TA1 Explorer (小白) / TA2 Investor (中老年长配) / TA3 Trader (活跃)
- KPI: 促首次入金 / 促首笔交易 / 促有效PC / 促期权首交 / 促CDP转仓 /
       促Referral裂变 / 提AUM / 拉新NUP / 唤醒沉默

Run: python fetcher/rewrite_content.py
"""
import json
from pathlib import Path

FETCHER = Path(__file__).parent

# id -> {angle, push: {title, body}}
R = {
    # ============ JUNE ============
    "0601ism": {
        "angle": "[KPI=促期权首交·TA=TA3] 做\"PMI 4 分项 + XLI 当日波动\"图,落期权投教——SG 期权渗透率仅 8%,工业股 IV 在 PMI 日易抬升,适合首单练手",
        "push": {
            "title": "今晚 ISM PMI,XLI 期权 IV 易抬升",
            "body": "PMI 跌破 50 时 XLI 当日跟跌概率超六成。打开 moomoo 富途\"期权投教\"15 分钟通关 + 1 张 XLI Put 保护组合,新客期权首单 0 佣金,首次入金最高 S$[奖励金额*]。"
        }
    },
    "0602jolts": {
        "angle": "[KPI=促期权首交·TA=TA3] 做\"JOLTS 三看 vs 非农领先关系\"图,引导用户开期权账户布局 TLT——辞职率拐点是债券长期看多信号",
        "push": {
            "title": "JOLTS,Fed 真正盯的劳动力数据",
            "body": "辞职率破 2% 几乎锁定降息——这种隐藏信号比非农早 2 周。把 TLT 加入富途自选 + 数据提醒,期权投教课同步跟,新客期权首单 0 佣金。"
        }
    },
    "0604ecb": {
        "angle": "[KPI=促期权首交+促CDP转仓·TA=TA2+TA3] 做\"欧美利差 vs EURUSD\"图,TA2 中老年关注 HSBC 通过 CDP 转仓,TA3 用 FXE 期权押欧元方向",
        "push": {
            "title": "ECB 决议夜,欧美利差再校准",
            "body": "ECB 鸽于 Fed → 欧元跌、HSBC 港美 ADR 套利窗口。CDP 直连转仓最快 T+1,首次转入最高 S$[奖励金额*],新客期权首单 0 佣金。"
        }
    },
    "0605nfp": {
        "angle": "[KPI=促期权首交+促有效PC·TA=TA3] 做\"非农 5 看 + Sahm Rule\"科普长图,落 SPY 跨式期权策略——非农日 SPY ATM straddle 隐含 1.5%,新客转化期权户的最佳事件",
        "push": {
            "title": "今夜非农,FOMC 前最重要数据",
            "body": "超预期或不及,SPY 单日波动常超 1.5%。1 张 SPY 跨式组合双向押宝,期权投教 15 分钟学会,新客期权首单 0 佣金,首次入金最高 S$[奖励金额*]。"
        }
    },
    "0610cpi": {
        "angle": "[KPI=促期权首交·TA=TA3] 做\"CPI 三看(整体/核心/超级核心)叠加关税滞后\"图,QQQ 跨式期权布局——CPI 日 QQQ 单日 IV 翻倍是教育用户期权杠杆的最佳示例",
        "push": {
            "title": "今晚 CPI 决定 9 月降息节奏",
            "body": "CPI 是 Fed 是否降息最关键变量,QQQ 单日波动常翻倍。1 张 QQQ 跨式组合双向押宝,期权投教 15 分钟通关,新客期权首单 0 佣金,首次入金最高 S$[奖励金额*]。"
        }
    },
    "0611wcup": {
        "angle": "[KPI=拉新NUP+促首次入金·TA=TA1] 世界杯是 2026 最大赚效活动页抓手,做\"赛程日历 + 受益清单(V/MA/DIS/NKE)\"页,落 NUP 新客拉新——每场比赛触发推送、每个受益股看一眼",
        "push": {
            "title": "世界杯开赛!Visa/MA 跨境支付旺季",
            "body": "赛事 38 天,Visa 跨境支付历史 +30%。打开 moomoo 富途\"世界杯赚效活动页\"看实时受益清单,首次入金最高 S$[奖励金额*],新客期权首单 0 佣金。"
        }
    },
    "0616retail": {
        "angle": "[KPI=促期权首交·TA=TA3] 做\"零售控制组 vs XRT/XLY\"映射,XRT Put 锁定下行——零售弱 → 消费板块跟跌,期权对冲是 TA3 高频教育点",
        "push": {
            "title": "5 月零售,消费动能体温计",
            "body": "控制组连续两月走弱,XRT 容易跟跌。1 张 XRT Put 锁定下行,期权投教 15 分钟学会,新客期权首单 0 佣金,首次入金最高 S$[奖励金额*]。"
        }
    },
    "0617fomc": {
        "angle": "[KPI=促期权首交+促有效PC·TA=TA3] 做\"点阵图 4 看升级版 + Powell 关键词清单\"图,SPY 跨式 + IV Crush 双教学——年内权重最高节点之一,转化期权户最佳窗口",
        "push": {
            "title": "今夜 FOMC + 点阵图,全年最高之夜",
            "body": "带 SEP 的 FOMC 一年仅 4 次,点阵图重写未来 18 个月利率。1 张 SPY 跨式双向布局,期权投教课同步开,新客期权首单 0 佣金,首次入金最高 S$[奖励金额*]。"
        }
    },
    "0619boj": {
        "angle": "[KPI=促期权首交·TA=TA3] 做\"日元套利交易复盘 + 2024-08 黑色星期一\"图,QQQ 防御 Put——美股休市叠加 BOJ 信号,周一开盘 Gap 风险翻倍",
        "push": {
            "title": "BOJ 决议夜 + 美股 Juneteenth 休市",
            "body": "美股休市 + BOJ 信号 = 周一开盘集中定价。1 张 QQQ Put 跨过周末作保险,几十美元封顶最大亏损,期权投教课 15 分钟跟,新客期权首单 0 佣金。"
        }
    },
    "0619hol": {
        "angle": "[KPI=唤醒沉默·TA=TA1] 节假日盘点页:11 个美股法定假日 + 跨假日持仓清单,推送给 30 天未登录沉默用户——节日是低意图用户重新打开 App 的最佳钩子",
        "push": {
            "title": "Juneteenth 休市,跨周末持仓盘点",
            "body": "BOJ 决议夜 + 美股休市 = 周一开盘 Gap 风险翻倍。打开 moomoo 富途模拟盘试一手 SPY 期权感受夜盘波动,0 风险练手,新户首次入金最高 S$[奖励金额*]。"
        }
    },
    "0626pce": {
        "angle": "[KPI=促期权首交+提AUM·TA=TA2+TA3] 做\"CPI vs PCE 权重差异\"图 + Russell 再平衡 IWM Pin Risk 教学——TA2 长配看 IWM 季节性,TA3 看 PCE 期权链 OI 热力图",
        "push": {
            "title": "PCE + Russell 再平衡,IWM 流动性日",
            "body": "IWM 成交量翻 3 倍,期权 IV 抬升 + Pin Risk 集中。富途期权链一键看 OI 热力图,期权投教课同步跟,新客期权首单 0 佣金,首次入金最高 S$[奖励金额*]。"
        }
    },
    "0630end": {
        "angle": "[KPI=提AUM+促CDP转仓·TA=TA2] 做\"H1 涨跌幅榜 + H2 三大主线\"复盘,TA2 长配视角——季末是中老年盘点资产、考虑 CDP 转仓的最佳窗口",
        "push": {
            "title": "Q2 季末,机构强制调仓最后一天",
            "body": "被动资金机械买卖,权重股尾盘易冲量。CDP 直连转仓最快 T+1 把竞品持仓搬过来 H2 一站统配,首次转入最高 S$[奖励金额*]。"
        }
    },

    # ============ JULY ============
    "0701ism": {
        "angle": "[KPI=促期权首交·TA=TA3] 做\"PMI 拐点信号 + XLI 期权链\"图,落期权投教——制造业 PMI 是衰退最早预警,XLI Put 是教育用户对冲的高频示例",
        "push": {
            "title": "7 月开门第一份 ISM PMI",
            "body": "PMI 跌破 50 时 XLI 当日跟跌概率超六成。1 张 XLI Put 锁定下行,期权投教 15 分钟通关,新客期权首单 0 佣金,首次入金最高 S$[奖励金额*]。"
        }
    },
    "0702nfp": {
        "angle": "[KPI=促期权首交+促有效PC·TA=TA3] 做\"独立日提前一天的非农\"特别图——节前流动性低 + 高 IV,SPY 跨式杠杆效率最高,转化期权户黄金日",
        "push": {
            "title": "独立日前夜非农,流动性最低之夜",
            "body": "节前流动性低 + 非农冲击 = SPY 单日波动放大。1 张 SPY 跨式跨节,期权投教课同步跟,新客期权首单 0 佣金,首次入金最高 S$[奖励金额*]。"
        }
    },
    "0703hol": {
        "angle": "[KPI=唤醒沉默·TA=TA1] 节假日提醒 + 长周末持仓盘点页,推送 30 天未登录沉默用户——独立日是 SG 用户夜间习惯打断的天然契机,Moo 庄园打卡触发签到",
        "push": {
            "title": "独立日休市,长周末持仓盘点",
            "body": "美股周五全天休市,Crypto 24/7 不停。打开 moomoo 富途 Moo 庄园签到 + Crypto 行情看一眼,新户首次入金最高 S$[奖励金额*]。"
        }
    },
    "0708minutes": {
        "angle": "[KPI=促期权首交·TA=TA3] 做\"6 月 FOMC 内部分歧拆解 + 措辞变化\"图——纪要常出鸽派或鹰派意外,SPY/TLT 单日波动易超 1%",
        "push": {
            "title": "6 月 FOMC 纪要,内部分歧曝光",
            "body": "纪要常曝出会议未明说的分歧,SPY/TLT 易超 1%。1 张 TLT 期权押降息节奏,期权投教 15 分钟学会,新客期权首单 0 佣金。"
        }
    },
    "0710cpi": {
        "angle": "[KPI=促期权首交·TA=TA3] 做\"CPI 关税传导 + 服务通胀粘性\"图,QQQ 跨式期权——CPI 日 IV 翻倍最适合教 TA3 期权杠杆",
        "push": {
            "title": "今晚 CPI 决定下半年降息节奏",
            "body": "CPI 是 Fed 最关键变量,QQQ 单日 IV 翻倍。1 张 QQQ 跨式双向押宝,期权投教 15 分钟通关,新客期权首单 0 佣金,首次入金最高 S$[奖励金额*]。"
        }
    },
    "0714jpm": {
        "angle": "[KPI=促期权首交·TA=TA3] 做\"大行净息差 + 投行收入分项\"图,XLF 期权布局——财报季首发周,JPM 信号决定整个金融板块基调",
        "push": {
            "title": "财报季开锣!JPM/Citi/WFC 三连发",
            "body": "大行净息差 + 投行收入双线索,XLF 板块同步定调。1 张 XLF 价差期权押方向,期权投教课同步跟,新客期权首单 0 佣金。"
        }
    },
    "0716tsm": {
        "angle": "[KPI=促期权首交+拉新NUP·TA=TA3] 做\"TSMC 资本开支 vs NVDA/AMD 营收\"图——TSMC 是全球 AI 芯片晶圆代工垄断者,赚效活动页+期权投教双触发",
        "push": {
            "title": "TSMC 财报,AI 芯片产业链晴雨表",
            "body": "TSMC 资本开支直接定价 NVDA/AMD 出货节奏,赚效活动页同步上线。打开富途\"AI 半导体赚效页\"看清单,新客期权首单 0 佣金,首次入金最高 S$[奖励金额*]。"
        }
    },
    "0719wcupfinal": {
        "angle": "[KPI=拉新NUP+促Referral裂变·TA=TA1] 世界杯决赛是赚效活动页收官 + 裂变邀请高峰,做\"全球收视 vs 受益股榜\"图,Referral 裂变中心同步推奖",
        "push": {
            "title": "世界杯决赛夜!赚效页最后一波",
            "body": "决赛收视破纪录,V/MA/DIS 单周波动放大。打开 moomoo 富途\"世界杯赚效页\"决赛特别版,Referral 裂变中心邀好友同步得 S$[奖励金额*]。"
        }
    },
    "0722goog": {
        "angle": "[KPI=促期权首交·TA=TA3] 做\"GOOG 云 + AI 资本开支拆解 + TSLA 交付指引\"图——双 Mag7 财报夜,QQQ 期权 IV 翻倍",
        "push": {
            "title": "GOOG/TSLA 财报双引爆",
            "body": "Mag7 双财报夜,QQQ 单日 IV 翻倍。1 张 QQQ 跨式 + 单股价差期权组合,期权投教 15 分钟学会,新客期权首单 0 佣金,首次入金最高 S$[奖励金额*]。"
        }
    },
    "0723meta": {
        "angle": "[KPI=促期权首交·TA=TA3] 做\"META AI 资本开支 + MSFT Azure/Copilot 收入\"图——AI 主线两大权重股财报,期权 IV Crush 教育最佳示例",
        "push": {
            "title": "META/MSFT 财报夜,AI 主线压舱石",
            "body": "Mag7 双财报夜,IV Crush 教育最佳示例。1 张 META 价差 + MSFT Put 组合,期权投教课同步跟,新客期权首单 0 佣金,首次入金最高 S$[奖励金额*]。"
        }
    },
    "0729fomc": {
        "angle": "[KPI=促期权首交+促有效PC·TA=TA3] 做\"无 SEP 的 FOMC vs 带 SEP\"对比图——这次仅声明 + Powell,SPY 波动相对小,适合教 TA3 调整仓位",
        "push": {
            "title": "无 SEP 的 FOMC,声明措辞为王",
            "body": "无点阵图但 Powell 关键词足以重写预期,SPY 波动 0.7-1.2%。1 张 SPY 价差期权布局,期权投教 15 分钟通关,新客期权首单 0 佣金。"
        }
    },
    "0730aapl": {
        "angle": "[KPI=促期权首交+拉新NUP·TA=TA3] 做\"AAPL iPhone 周期 + AMZN AWS 增速\"图——双 Mag7 财报,SG 用户对苹果热度最高,期权投教 + 赚效页双触发",
        "push": {
            "title": "AAPL/AMZN 财报双夜,Mag7 收官",
            "body": "Mag7 财报季收官夜,期权 IV 翻倍。1 张 AAPL 价差 + AMZN 跨式,期权投教课同步跟,新客期权首单 0 佣金,首次入金最高 S$[奖励金额*]。"
        }
    },
    "0731pce": {
        "angle": "[KPI=促期权首交·TA=TA3] 做\"6 月 PCE vs CPI 差异 + Fed 9 月降息概率重估\"图——FOMC 后第一份 PCE,验证 Powell 措辞",
        "push": {
            "title": "FOMC 后第一份 PCE,降息概率重估",
            "body": "PCE 是 Fed SEP 跟踪指标,直接重写 9 月降息定价。1 张 TLT 价差期权押降息节奏,期权投教 15 分钟通关,新客期权首单 0 佣金。"
        }
    },

    # ============ AUGUST ============
    "0803ism": {
        "angle": "[KPI=促期权首交·TA=TA3] 做\"PMI 拐点 + XLI 历史回测\"图,落期权投教——8 月 PMI 是夏季淡季后第一个高频读数",
        "push": {
            "title": "8 月开门 ISM PMI,工业股拐点",
            "body": "PMI 跌破 50 时 XLI 当日跟跌概率超六成。1 张 XLI Put,期权投教 15 分钟通关,新客期权首单 0 佣金,首次入金最高 S$[奖励金额*]。"
        }
    },
    "0804jolts": {
        "angle": "[KPI=促期权首交·TA=TA3] 做\"JOLTS 辞职率 vs 时薪同比\"图——劳动力松紧度领先非农 2 周,TLT 期权布局教育示例",
        "push": {
            "title": "JOLTS 辞职率破 2% 即降息信号",
            "body": "辞职率比非农早 2 周露马脚。把 TLT 加入富途自选 + 数据提醒,期权投教课同步跟,新客期权首单 0 佣金。"
        }
    },
    "0807nfp": {
        "angle": "[KPI=促期权首交+促有效PC·TA=TA3] 做\"非农 5 看 + Sahm Rule 衰退预警\"图——FOMC 后第一份非农,验证 Powell 措辞",
        "push": {
            "title": "FOMC 后第一份非农,验证 Powell",
            "body": "Powell 7 月措辞 vs 8 月数据,SPY 单日波动常超 1.5%。1 张 SPY 跨式双向押宝,期权投教课同步跟,新客期权首单 0 佣金,首次入金最高 S$[奖励金额*]。"
        }
    },
    "0813cpi": {
        "angle": "[KPI=促期权首交·TA=TA3] 做\"CPI 服务通胀粘性 + 关税传导\"图——9 月 FOMC 前第二份 CPI,QQQ 跨式期权高频教学",
        "push": {
            "title": "今晚 CPI,9 月 FOMC 前第二份",
            "body": "QQQ 单日 IV 翻倍,跨式期权杠杆效率最高。1 张 QQQ 跨式双向押宝,期权投教 15 分钟通关,新客期权首单 0 佣金,首次入金最高 S$[奖励金额*]。"
        }
    },
    "0814retail": {
        "angle": "[KPI=促期权首交·TA=TA3] 做\"零售控制组 + Michigan 消费者预期\"双图——双数据日,XRT/XLY 期权链解读最佳教学示例",
        "push": {
            "title": "零售 + Michigan 双数据日",
            "body": "双数据日 XRT/XLY 当日波动放大,期权链 OI 热力图直接看主力位。富途期权链一键查,期权投教 15 分钟通关,新客期权首单 0 佣金。"
        }
    },
    "0817wmt": {
        "angle": "[KPI=促期权首交·TA=TA3] 做\"WMT 同店销售 + 低收入消费分层\"图——零售龙头财报,XRT 板块基调由此定",
        "push": {
            "title": "Walmart 财报,零售龙头定调",
            "body": "WMT 同店销售 + 低收入分层是消费温度计,XRT 跟动。1 张 WMT 价差期权押方向,期权投教课同步跟,新客期权首单 0 佣金。"
        }
    },
    "0819target": {
        "angle": "[KPI=促期权首交·TA=TA3] 做\"TGT/LOW 财报 vs WMT 对比\"图——二线零售财报,中低端消费分层信号",
        "push": {
            "title": "TGT/LOW 财报,二线零售信号",
            "body": "TGT 同店是中产消费温度计,与 WMT 对比信息量最大。期权投教课同步跟,新客期权首单 0 佣金,首次入金最高 S$[奖励金额*]。"
        }
    },
    "0821jh": {
        "angle": "DELETE",
        "push": {"title": "", "body": ""}
    },
    "0827nvda": {
        "angle": "[KPI=促期权首交+拉新NUP·TA=TA3] 做\"NVDA 数据中心收入 + AI Capex 指引\"图——AI 主线最大权重股,赚效活动页+期权投教双触发,IV 70%+",
        "push": {
            "title": "NVDA 财报夜,AI 主线压舱石",
            "body": "NVDA IV 70%+,单日波动常 6-10%。打开富途\"AI 半导体赚效页\" + 1 张 NVDA 价差期权,期权投教课同步跟,新客期权首单 0 佣金,首次入金最高 S$[奖励金额*]。"
        }
    },
    "0828pce": {
        "angle": "[KPI=促期权首交·TA=TA3] 做\"7 月 PCE 验证 Powell JH 演讲\"图——JH 后第一份 PCE,定调 9 月 FOMC 降息节奏",
        "push": {
            "title": "JH 后第一份 PCE,降息节奏定锚",
            "body": "Powell JH 演讲 vs PCE 数据双重验证,TLT 期权直接重写。1 张 TLT 价差期权,期权投教课同步跟,新客期权首单 0 佣金。"
        }
    },

    # ============ SEPTEMBER ============
    "0901ism": {
        "angle": "[KPI=促期权首交·TA=TA3] 做\"PMI 拐点 + 9 月季节性\"图——9 月历史是 SPX 表现最差月,PMI 偏弱 + 季节性叠加,XLI Put 教育示例",
        "push": {
            "title": "9 月开门 PMI,历史最差月开局",
            "body": "9 月历史 SPX 表现最差 + PMI 偏弱叠加,XLI 易跟跌。1 张 XLI Put 防御,期权投教 15 分钟通关,新客期权首单 0 佣金,首次入金最高 S$[奖励金额*]。"
        }
    },
    "0903jolts": {
        "angle": "[KPI=促期权首交·TA=TA3] 做\"JOLTS 辞职率拐点 + 9 月降息概率\"图——FOMC 前第一份 JOLTS,TLT 期权前置布局",
        "push": {
            "title": "9 月 FOMC 前第一份 JOLTS",
            "body": "辞职率破 2% 几乎锁定降息。把 TLT 加入富途自选 + 数据提醒,期权投教课同步跟,新客期权首单 0 佣金。"
        }
    },
    "0904nfp": {
        "angle": "[KPI=促期权首交+促有效PC·TA=TA3] 做\"FOMC 前最重磅非农\"特别图——9 月降息概率最关键变量,SPY/TLT 单日 ATM straddle 隐含 1.5%+",
        "push": {
            "title": "9 月 FOMC 前最重磅非农",
            "body": "决定 9 月降息节奏的最后一份非农,SPY 单日波动 1.5%+。1 张 SPY 跨式双向押宝,期权投教课同步跟,新客期权首单 0 佣金,首次入金最高 S$[奖励金额*]。"
        }
    },
    "0907labor": {
        "angle": "[KPI=唤醒沉默·TA=TA1] 节假日页 + 长周末持仓盘点,推送 30 天未登录用户——劳动节是 SG 用户秋季节奏开始的天然唤醒点",
        "push": {
            "title": "Labor Day 休市,秋季交易节奏启动",
            "body": "9 月历史 SPX 最差月,长周末后 Gap 风险翻倍。打开 moomoo 富途模拟盘试一手 SPY 期权,0 风险练手,新户首次入金最高 S$[奖励金额*]。"
        }
    },
    "0910ecb": {
        "angle": "[KPI=促CDP转仓+促期权首交·TA=TA2+TA3] 做\"ECB vs Fed 9 月分化\"图——TA2 中老年关注 HSBC 通过 CDP 直连转仓,TA3 用 FXE 期权",
        "push": {
            "title": "ECB 9 月决议,欧美利差再分化",
            "body": "ECB 鸽 → 欧元跌 → HSBC 港美 ADR 套利窗口。CDP 直连转仓最快 T+1 把竞品持仓搬过来,首次转入最高 S$[奖励金额*]。"
        }
    },
    "0911cpi": {
        "angle": "[KPI=促期权首交·TA=TA3] 做\"FOMC 前最后 CPI + 关税传导成熟期\"图——9/16 FOMC 前最后高权重通胀,QQQ 跨式期权",
        "push": {
            "title": "FOMC 前最后 CPI,降息节奏定锚",
            "body": "FOMC 前最后高权重通胀,QQQ 单日 IV 翻倍。1 张 QQQ 跨式双向押宝,期权投教课同步跟,新客期权首单 0 佣金,首次入金最高 S$[奖励金额*]。"
        }
    },
    "0915retail": {
        "angle": "[KPI=促期权首交·TA=TA3] 做\"FOMC 前零售控制组\"图——消费温度计,XRT/XLY 期权链是 TA3 高频教学示例",
        "push": {
            "title": "FOMC 前零售,消费温度计",
            "body": "控制组直接进 GDP 消费分项,XRT 当日跟动。1 张 XRT 价差期权,期权投教 15 分钟通关,新客期权首单 0 佣金。"
        }
    },
    "0916fomc": {
        "angle": "[KPI=促期权首交+促有效PC+拉新NUP·TA=TA3] 做\"9 月点阵图 4 看 + 降息路径全图\"——年内最大 FOMC 之夜,赚效活动页 + 期权投教 + NUP 三触发",
        "push": {
            "title": "9 月 FOMC + 点阵图,年内最大之夜",
            "body": "带 SEP 的 FOMC + 全年关键降息节点,SPX 历史平均波动 1.5%+。打开富途\"FOMC 赚效页\" + 1 张 SPY 跨式,期权投教课同步跟,新客期权首单 0 佣金,首次入金最高 S$[奖励金额*]。"
        }
    },
    "0917boj": {
        "angle": "[KPI=促期权首交·TA=TA3] 做\"BOJ 后 FOMC 24 小时双央行\"图——日元套利交易解除风险,QQQ 防御 Put 教学示例",
        "push": {
            "title": "FOMC 隔夜 BOJ,双央行 24 小时",
            "body": "FOMC + BOJ 24 小时双重定价,日元若大涨,QQQ 易跟跌。1 张 QQQ Put 跨过夜盘,几十美元封顶最大亏损,期权投教课同步跟。"
        }
    },
    "0918quad": {
        "angle": "[KPI=促期权首交·TA=TA3] 做\"四巫日 + S&P 季度调整\"双线图——成交量翻 3 倍 + 期权交割集中,Pin Risk 教学最佳示例",
        "push": {
            "title": "9 月四巫日 + S&P 调仓",
            "body": "四巫日 + 季末调仓 = 成交量翻 3 倍,Pin Risk 集中。富途期权链一键看 OI 热力图,期权投教课同步跟,新客期权首单 0 佣金。"
        }
    },
    "0925pce": {
        "angle": "[KPI=促期权首交·TA=TA3] 做\"FOMC 后第一份 PCE 验证降息节奏\"图——9 月 FOMC 决议后核心通胀验证,TLT 期权直接重写",
        "push": {
            "title": "FOMC 后第一份 PCE,降息节奏验证",
            "body": "Powell 措辞 vs PCE 数据双重验证,TLT 期权直接重写。1 张 TLT 价差期权,期权投教课同步跟,新客期权首单 0 佣金,首次入金最高 S$[奖励金额*]。"
        }
    },
    "0930end": {
        "angle": "[KPI=提AUM+促CDP转仓·TA=TA2] 做\"Q3 涨跌幅榜 + Q4 三大主线\"复盘——TA2 中老年长配视角,季末是 CDP 转仓 + AUM 加码最佳窗口",
        "push": {
            "title": "Q3 季末,机构强制调仓收官",
            "body": "被动资金机械买卖,权重股尾盘冲量。CDP 直连转仓最快 T+1 一站统配 Q4,首次转入最高 S$[奖励金额*],新户期权首单 0 佣金。"
        }
    },
}

# ---------------------------------------------------------------------------
# Apply rewrites
# ---------------------------------------------------------------------------
applied = 0
deleted = 0
missing_ids = []
for m in ("jun", "jul", "aug", "sep"):
    p = FETCHER / f"events_{m}.json"
    evs = json.loads(p.read_text(encoding="utf-8"))
    out = []
    for e in evs:
        if e["id"] in R:
            r = R[e["id"]]
            if r.get("angle") == "DELETE":
                deleted += 1
                continue
            e["angle"] = r["angle"]
            e["push"] = r["push"]
            applied += 1
        out.append(e)
    p.write_text(json.dumps(out, ensure_ascii=False, indent=0), encoding="utf-8")

# Sanity: which expected ids were missing
existing_ids = set()
for m in ("jun", "jul", "aug", "sep"):
    for e in json.loads((FETCHER / f"events_{m}.json").read_text(encoding="utf-8")):
        existing_ids.add(e["id"])
for k in R:
    if k not in existing_ids and R[k].get("angle") != "DELETE":
        missing_ids.append(k)

print(f"applied: {applied}")
print(f"deleted: {deleted}")
if missing_ids:
    print(f"WARN missing ids in JSON: {missing_ids}")
print("done.")
