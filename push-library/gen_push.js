const fs = require('fs');

// 37 事件 PUSH。CTA 多样化：
// - 经典 "1 张 XX 期权，新客 0 佣金"：约 10 条（最重磅事件）
// - 提问钩子：让用户自己想答案 → 进富途看资金怎么投票
// - 工具钩子：富途期权链 OI 热力图 / IV 分位 / 财报日历
// - 学习钩子：跨式 / IV Crush 不懂？富途期权学院
// - 简单指令：一张 Put 备着、加入自选盯异动
const PUSHES = [
  {id:'0610cpi', name:'5月 CPI', date:'6/10', tickers:'SPY,QQQ,TLT', t:'QQQ',
   angle:'CPI 三看：整体/核心/服务，叠加关税滞后图',
   title:'今晚 CPI 决定 Fed 降息节奏，超预期就翻车',
   body:'CPI 是 Fed 是否降息最关键变量，超预期或不及预期市场都会瞬间反向，QQQ 单日波动常翻倍。1 张 QQQ 跨式组合双向押宝，新客期权首单 0 佣金。'},
  {id:'0611ppi', name:'5月 PPI + 初请', date:'6/11', tickers:'SPY,XLI', t:'XLI',
   angle:'CPI vs PPI 剪刀差，解读企业利润空间',
   title:'PPI 上游成本，CPI 之后的"二次锤"',
   body:'CPI 已出，PPI 是企业利润空间最后一块拼图，工业股最容易被剪刀差打到。你觉得这次会延续 CPI 方向，还是反向定价？打开富途期权链看 XLI 资金正在押哪边。'},
  {id:'0612spx', name:'SpaceX IPO 传闻窗口', date:'6/12', tickers:'RKLB,ASTS', t:'RKLB',
   angle:'商业航天估值对照表 + IPO 打新教学',
   title:'SpaceX 万亿 IPO 传闻发酵，商业航天集体躁动',
   body:'史上最大 IPO 传闻一来，RKLB/ASTS 容易冲高回落，IV 已经开始抬升。直接追高容易被套，提前 1 张 RKLB 看跌期权封顶亏损，比割肉理性得多。'},
  {id:'0613umich', name:'密歇根消费者信心', date:'6/13', tickers:'XLY,XRT', t:'XRT',
   angle:'消费信心 vs 标普消费板块相关性',
   title:'消费者信心数据，零售板块的"体温计"',
   body:'信心走弱时 XRT/XLY 当日就开始跟跌。打开富途期权链先看一眼 XRT 当前 IV 分位 + OI 集中区，再决定 Put 行权价怎么选最划算。'},
  {id:'0617fomc', name:'6月 FOMC + 点阵图 + Powell', date:'6/17', tickers:'SPY,QQQ,TLT,GLD,UUP', t:'SPY',
   angle:'点阵图 4 看：中位数/分歧度/2027 终点/长期利率',
   title:'今夜 FOMC + 点阵图，全年权重最高之夜',
   body:'带 SEP 的 FOMC 一年只有 4 次，点阵图直接定调未来 18 个月利率路径，标普历史平均波动 1.5%。1 张 SPY 跨式组合双向布局，新客期权首单 0 佣金。'},
  {id:'0618boj', name:'BOJ 利率决议', date:'6/18', tickers:'QQQ,FXY', t:'QQQ',
   angle:'日元套利交易解除会冲击美股',
   title:'BOJ 决议夜，全球流动性的隐形开关',
   body:'BOJ 一旦超预期，日元套利解除会引发美股闪崩（去年 8 月已演示）。这种夜盘风险，你买没买保险？1 张 QQQ Put 当作保险单，几十美元封顶最大亏损。'},
  {id:'0619quad', name:'六月四巫日(季度交割)', date:'6/19', tickers:'SPY,QQQ,IWM', t:'SPY',
   angle:'四巫日交易日历 + Pin Risk 集中区',
   title:'六月四巫日，全年最大期权到期日',
   body:'季度四类衍生品同日到期，OI 集中点最容易触发 Pin Risk，尾盘 30 分钟波动放大数倍。富途期权链一键看 OI 热力图，机构在哪里"钉桩"一目了然。'},
  {id:'0620pce', name:'5月 核心 PCE', date:'6/20', tickers:'SPY,TLT', t:'SPY',
   angle:'CPI vs PCE 权重差异图解',
   title:'核心 PCE，Fed 真正盯的通胀指标',
   body:'Fed 决策时优先看 PCE 而不是 CPI，权重不同口径不同，市场反应可能与 CPI 完全相反。CPI 已 priced in 的方向，PCE 会不会反水？打开富途看资金提前怎么布。'},
  {id:'0625gdp', name:'Q1 GDP 终值', date:'6/25', tickers:'SPY,TLT', t:'TLT',
   angle:'GDP 三次估算流程 + 终值修正含义',
   title:'Q1 GDP 终值，经济叙事最终定锤',
   body:'三次估算到此为止，终值若较二次估算大幅修正，债市常剧烈反应。把 TLT 加入富途自选 + 设置数据提醒，开盘前 30 分钟 IV 异动你会第一个收到。'},
  {id:'0630end', name:'Q2 季末 + 上半年收官', date:'6/30', tickers:'SPY,QQQ', t:'SPY',
   angle:'上半年涨跌幅榜 + 下半年三大主线展望',
   title:'Q2 季末，机构强制调仓最后一天',
   body:'季末机构必须再平衡，被动资金被动买卖，权重股容易在尾盘出现非常规冲量。富途模拟盘先试一手 SPY 期权感受波动，看看符不符合自己节奏，0 风险练手。'},
  {id:'0702nfp', name:'6月 非农', date:'7/2', tickers:'SPY,TLT', t:'SPY',
   angle:'非农 5 看：就业/失业率/时薪/参与率/前值修正',
   title:'独立日前夜非农，长假 Gap 风险叠加',
   body:'非农当日恰逢长假前，数据偏离会被节后放大，假期持仓风险翻倍。1 张 SPY Put 锁定下行保护，新客期权首单 0 佣金。'},
  {id:'0703hol', name:'美股提前休市/独立日', date:'7/3', tickers:'SPY', t:'SPY',
   angle:'美股节假日交易日历 + Gap 风险管理',
   title:'美股 13:00 提前收盘，三天长假 Gap 风险来了',
   body:'流动性骤降叠加非农刚出，假期风险被压缩到 4 小时内集中释放，节后跳空概率显著提升。一张到期日跨过假期的 SPY Put，就是最简单的防 Gap 保险。'},
  {id:'0708fed', name:'FOMC 6月会议纪要', date:'7/8', tickers:'SPY,TLT', t:'TLT',
   angle:'纪要 vs 发布会差异解读',
   title:'FOMC 纪要，Powell 当时没说出口的话',
   body:'纪要常披露发布会未提的内部分歧，鹰鸽倾向常与发布会相反。你猜这次纪要更鹰还是更鸽？打开富途看 TLT 期权链，资金已经开始用真金白银投票了。'},
  {id:'0710cpi', name:'6月 CPI', date:'7/10', tickers:'SPY,QQQ', t:'QQQ',
   angle:'核心商品/核心服务/住房三分项追踪表',
   title:'6月 CPI，7月 FOMC 决策的最后一块拼图',
   body:'距离 FOMC 仅 3 周，这份 CPI 直接决定是否降息，超预期暴跌或暴涨概率都不低。1 张 QQQ 跨式期权两个方向都不错过，新客期权首单 0 佣金。'},
  {id:'0714jpm', name:'JPM 财报 (Q2 财报季开启)', date:'7/14', tickers:'JPM,XLF,KRE', t:'JPM',
   angle:'美国六大行 Q2 看点对照表',
   title:'JPM 财报，Q2 财报季正式开打',
   body:'大行率先出炉，信用卡核销率 / 净息差是判断衰退预期最敏感的领先指标。财报日 JPM 隐含波动率最贵，富途期权链看 IV Crush 区间提前定方向，比盲买便宜不少。'},
  {id:'0715bac', name:'BAC/GS/MS 财报', date:'7/15', tickers:'BAC,KRE', t:'BAC',
   angle:'投行 vs 商行 vs 财富管理三模式对比',
   title:'BAC + GS + MS 同日，银行业三大模式 PK',
   body:'商业银行 vs 投行 vs 财富管理三模式同日出炉，板块内分化剧烈。你看好哪个模式赢？富途期权链对照三家 IV，差异越大，超预期反应空间越大。'},
  {id:'0716tsm', name:'TSM 财报 + 资本开支', date:'7/16', tickers:'TSM,SMH,NVDA', t:'TSM',
   angle:'TSM 资本开支 vs SOX 指数走势叠加 + SOXX',
   title:'TSM 财报，NVDA 之前 AI 算力的预演',
   body:'TSM 资本开支是 AI 算力链最权威的领先指标，直接决定 SOXX/NVDA 下一季节奏。等到 NVDA 财报当日 IV 翻倍才动手，性价比早已不在；TSM 期权链先看一眼吧。'},
  {id:'0722goog', name:'Alphabet / Tesla 财报', date:'7/22', tickers:'GOOGL,TSLA,QQQ', t:'GOOGL',
   angle:'GOOGL 三块业务拆解 + Mag7 财报日历',
   title:'GOOGL + TSLA，Mag7 财报首场登场',
   body:'搜索 / 云 / 自动驾驶三块业务一起验证，Mag7 财报首场常奠定整轮节奏。把后续 Mag7 财报日全部加入富途自选 + 财报日历提醒，下一场是 Meta，一场不漏才是关键。'},
  {id:'0723meta', name:'Meta 财报', date:'7/23', tickers:'META,QQQ', t:'META',
   angle:'广告 ARPU vs 时长占比双轴图',
   title:'Meta 财报，AI 广告变现真章',
   body:'广告 ARPU + Reels 时长是判断 AI 能否真正变现的核心，Meta 财报后单日波动常超 8%。你押 META 涨还是跌？看一眼期权链 Put/Call Ratio，资金的答案已经在那里。'},
  {id:'0724msft', name:'Microsoft 财报', date:'7/24', tickers:'MSFT,QQQ', t:'MSFT',
   angle:'Azure 增速 vs AWS/GCP 三巨头对比',
   title:'MSFT 财报，AI 最大 To-B 故事的真相',
   body:'Azure 增速是判断 AI 商业化是否真实落地的最硬指标，超预期时 QQQ 容易被一同拉起。富途看 Azure vs AWS vs GCP 同期增速对照表，财报数字一出谁高谁低秒判断。'},
  {id:'0729fomc', name:'7月 FOMC (无 SEP)', date:'7/29', tickers:'SPY,QQQ,TLT', t:'QQQ',
   angle:'有/无 SEP 会议反应模式差异',
   title:'7月 FOMC，全靠 Powell 一张嘴定 9月',
   body:'无 SEP 没点阵图，市场只能从 Powell 措辞里猜降息节奏，发布会每个字都被反复解读。1 张 QQQ 期权抓发布会窗口波动，新客期权首单 0 佣金。'},
  {id:'0731pce', name:'6月 核心 PCE + ECI', date:'7/31', tickers:'SPY,TLT', t:'SPY',
   angle:'ECI vs 时薪 指标差异 + 劳动力成本传导',
   title:'PCE + ECI 双发，9月降息条件最后试金石',
   body:'PCE 通胀 + ECI 劳动力成本同日出炉，二者同步降温才是 Fed 启动降息的真正信号。富途宏观日历把这两个数据并列追踪，开盘前 1 分钟读完不迟。'},
  {id:'0807nfp', name:'7月 非农', date:'8/7', tickers:'SPY,TLT', t:'SPY',
   angle:'夏季季调对非农影响科普',
   title:'7月非农，夏季季调最容易"翻车"的一期',
   body:'七月数据夏季季调影响最大，"假爆冷"或"假爆热"频出，回调修正才是真正机会。这次你赌哪种翻车方向？打开富途期权链看 SPY Put/Call OI，资金倾向一目了然。'},
  {id:'0812cpi', name:'7月 CPI', date:'8/12', tickers:'SPY,QQQ', t:'QQQ',
   angle:'核心商品 vs 服务通胀 剪刀差',
   title:'7月 CPI，9月降息 25bp 还是 50bp 之争开打',
   body:'9月 FOMC 前最重磅通胀，决定市场押 25 还是 50bp，债市股市同步剧烈反应。1 张 QQQ 期权押降息节奏，新客期权首单 0 佣金。'},
  {id:'0813ppi', name:'7月 PPI', date:'8/13', tickers:'SPY,XLI', t:'XLI',
   angle:'PPI→PCE 传导路径',
   title:'7月 PPI，PCE 子项的提前剧透',
   body:'PPI 中医疗 / 金融服务子项直接进入 PCE 计算，CPI 之后 PPI 常引发利率预期二次定价。把 PPI + 月底 PCE 一并加入富途数据日历，连贯看才不会错过节奏。'},
  {id:'0820jh', name:'Jackson Hole 全球央行年会(开幕)', date:'8/20', tickers:'SPY,TLT', t:'SPY',
   angle:'JH 历届主题与 SPX 反应回顾',
   title:'Jackson Hole 周开启，全球央行年度集结',
   body:'JH 周一开启 IV 就开始抬升，期权溢价随预期升温。这种"还没出事就已经开始贵"的特性，恰好是提前布局者的窗口期 — 周一买比周五便宜得多。'},
  {id:'0822jh', name:'Powell Jackson Hole 演讲', date:'8/22', tickers:'SPY,TLT,GLD', t:'SPY',
   angle:'JH 演讲前后 SPX 历史 5 日表现 + 债券 ETF',
   title:'今夜 Powell JH 演讲，重要性仅次 FOMC',
   body:'Powell 历史上常在 JH 透露重大政策转向（2022 年那次至今难忘），SPX 5 日波动均值 2%+。1 张 SPY 期权押方向，新客期权首单 0 佣金。'},
  {id:'0826nvda', name:'NVIDIA 财报 (Q2 FY27)', date:'8/26', tickers:'NVDA,SMH,SPY', t:'NVDA',
   angle:'NVDA 数据中心/游戏/汽车收入拆解 + AI 算力 ETF SMH/SOXX',
   title:'今夜 NVDA 财报，AI 算力主线最重磅之夜',
   body:'NVDA 单家公司决定 AI 主线情绪，数据中心增速 + 下季指引定调全市场风险偏好，SMH/SOXX 当日同步联动。1 张 NVDA 期权押 AI 主线，新客期权首单 0 佣金。'},
  {id:'0829pce', name:'7月 核心 PCE', date:'8/29', tickers:'SPY,TLT', t:'SPY',
   angle:'超级核心 PCE 跟踪表',
   title:'7月核心 PCE，9月 FOMC 前最后一份通胀',
   body:'这份 PCE 之后，市场对 9月降息的押注就再无变量了。25 还是 50bp 的天平今天就要倾斜。富途期权链看 SPY 当周到期合约 IV 分位，资金的判断比新闻早 24 小时。'},
  {id:'0901hol', name:'劳工节(美股休市)', date:'9/1', tickers:'SPY', t:'SPY',
   angle:'9月 季节性最弱 + 节假日日历',
   title:'劳工节休市，9月历史最差行情前夜',
   body:'9月美股历史季节性最弱，过去 30 年平均下跌，长假前持仓风险偏大。一张到期日跨过劳工节的 SPY Put 备着，比假期里盯着新闻焦虑省心。'},
  {id:'0902nfp', name:'8月 非农', date:'9/4', tickers:'SPY,TLT,GLD', t:'SPY',
   angle:'非农 5 看 + Sahm Rule + 债券 ETF 选择',
   title:'8月非农，9月 FOMC 前最关键就业数据',
   body:'这份非农直接决定 9月降息幅度，失业率若触发 Sahm Rule，市场对衰退定价会瞬间切换。1 张 SPY 期权押降息节奏，新客期权首单 0 佣金。'},
  {id:'0909appl', name:'Apple 秋季新品发布会', date:'9/9', tickers:'AAPL,SWKS,QRVO', t:'AAPL',
   angle:'Apple 供应链 ETF + 消费电子季节性策略',
   title:'今夜 Apple 发布会，秋季旗舰登场',
   body:'苹果发布会规律是"提前涨预期 + 当日卖事实"，AAPL 单日方向最难判断，最适合双向押宝的跨式组合。还没用过跨式？富途期权学院 30 分钟搞懂，今晚就能用上。'},
  {id:'0911cpi', name:'8月 CPI', date:'9/11', tickers:'SPY,QQQ,TLT', t:'QQQ',
   angle:'CPI vs 非农 组合对降息路径影响',
   title:'8月 CPI，9月 FOMC 前最后通胀牌',
   body:'CPI + 非农组合直接决定降息 25 还是 50bp，市场押宝心态浓，单日波动易翻倍。25 还是 50，你押哪边？富途期权链 OI 分布告诉你大资金已经选好了哪边。'},
  {id:'0915fomc', name:'9月 FOMC + SEP + 点阵图', date:'9/16', tickers:'SPY,QQQ,TLT,GLD', t:'SPY',
   angle:'点阵图四看升级版 + 降息周期下 债券+黄金 ETF 组合',
   title:'今夜 9月 FOMC + 点阵图，Q3 最重磅之夜',
   body:'带 SEP 的 FOMC + 降息周期可能正式开启，标普历史平均波动 2%、债市黄金同步异动。1 张 SPY 跨式组合双向布局，新客期权首单 0 佣金。'},
  {id:'0918quad', name:'九月四巫日', date:'9/18', tickers:'SPY,QQQ,IWM', t:'SPY',
   angle:'四巫日 + FOMC 双叠加效应',
   title:'九月四巫日 + FOMC 余波，二次定价良机',
   body:'FOMC 隔两日就是季度交割，定价分歧 + Pin Risk 双重叠加，全年罕见的双因子日，尾盘波动放大数倍。富途期权链 OI 热力图打开，"钉桩"位置一目了然。'},
  {id:'0926pce', name:'8月 核心 PCE', date:'9/26', tickers:'SPY,TLT', t:'TLT',
   angle:'FOMC 后 PCE 反应模式',
   title:'8月核心 PCE，FOMC 决策合理性的"考卷"',
   body:'FOMC 刚决议完，这份 PCE 是市场对 Fed 判断的验证；偏差大时债市反应比股市更剧烈。把 TLT 加入富途自选盯隔夜异动，比看新闻更直观。'},
  {id:'0930end', name:'Q3 季末 + 联邦财年末', date:'9/30', tickers:'SPY,QQQ,IWM', t:'SPY',
   angle:'Q3 复盘 + Q4 三大主线 + 政府关门历史规律',
   title:'Q3 季末 + 联邦财年末，政府关门倒计时',
   body:'联邦财年末若拨款法案未过即关门，历史上 SPX 短期承压、防御板块反而跑出超额。一张到期日跨过 10 月初的 SPY Put 备着，是这种政策尾部风险最便宜的对冲方式。'},
];

console.log('events:', PUSHES.length);

const copyEntries = PUSHES.map(p => {
  const j = (s) => JSON.stringify(s);
  return `'${p.id}':{title:${j(p.title)},body:${j(p.body)},angle:${j(p.angle)}}`;
}).join(',\n');
fs.writeFileSync('push_copy.js', `const PUSH_COPY={\n${copyEntries}\n};`);

const csvRows = [['序号','事件','时间','核心标的','Growth Angle','PUSH 标题','PUSH 正文','状态','上线日期','CTR','CVR','备注']];
PUSHES.forEach((p, i) => {
  csvRows.push([i+1, p.name, p.date, p.tickers, p.angle, p.title, p.body, '草稿', '', '', '', '']);
});
function esc(v){
  v = String(v);
  if(v.includes(',')||v.includes('"')||v.includes('\n')) return '"'+v.replace(/"/g,'""')+'"';
  return v;
}
fs.writeFileSync('q3_2026_options_push_library.csv', csvRows.map(r=>r.map(esc).join(',')).join('\n')+'\n');

const jsRows = PUSHES.map((p, i) => [i+1, p.name, p.date, p.tickers, p.angle, p.title, p.body]);
fs.writeFileSync('lib_data.js', 'const PUSH_LIBRARY=' + JSON.stringify(jsRows) + ';');

const classics = PUSHES.filter(p => p.body.includes('新客期权首单 0 佣金')).length;
console.log('classic CTA:', classics, '/', PUSHES.length);
console.log('CSV / lib_data / push_copy generated');
