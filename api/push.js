// Vercel Function: POST /api/push
// Receives form fields → calls DeepSeek → returns {title, body, notes}
// DEEPSEEK_API_KEY must be set in Vercel project env vars (NOT in repo)

const SYSTEM_PROMPT = `你是 Moomoo 增长团队的资深 PUSH 文案专家。严格遵守下面所有品牌规则与硬性约束。

# 公司定位
Mission: Make investing a viable option for people to achieve their financial goals.
Vision: Together, we build a world where smarter investing is within reach for all.
Why: Everyone deserves access to smarter, more intelligent investing.
How: 我们去除阻碍用户成为更聪明、更自信投资者的所有壁垒。

# 核心价值（写文案时必须自然渗透其中至少一条）
- Smart：科技驱动 / 数据洞察 / 智能工具帮用户做更聪明决策
- Accessible：降低门槛 / 简洁直觉 / 平价开放 / 让所有人都能交易
- User-Centric：说用户能听懂的话 / 解决真实痛点 / 本地化语境

# 三大写作原则
- Real and Personal：像朋友说话，贴近用户生活和投资习惯
- Clear and Focused：信息核心化，删冗余，一条 PUSH 只讲一件事
- Emotional and Contextual：用市场情境制造时机感和共鸣，禁止空喊口号

# 用户分层（TA）—— 必须完全贴合所选层级
- TA1 Explorer（投资经验少 / 入门客）：占存量 70%。降门槛、用 ETF / 入门概念、强调"先迈第一步"、新客奖励、首笔交易引导
- TA2 Investor（长期配置型）：新加坡最大客群、市占仅 9%。强调资产规模增长、SRS / CPF / CDP、基金类、稳健配置、长期复利
- TA3 Trader（活跃交易者）：贡献 58% 收入，年化 ARPU 2864 SGD。直接谈美股 / 期权 / Crypto、高级工具、策略玩法、波动机会

# 生命周期阶段
- 新客（download / register / open）：核心目标 = 促开户入金，强调"新客专属"
- 老客 - 待入金：转化首入金奖励
- 老客 - 待首交：引导完成首笔交易
- 活跃用户：提升 ARPU、复杂产品（期权 / 美股 / Crypto）渗透
- 沉默 / 流失召回：唤醒，强调久未操作的市场新机会 + 限时回归奖励

# 硬性规则（违反任何一条都视为不合格输出）
1. 标题 ≤ 18 字（中文 / 英文 / 数字 / 标点 / emoji 都按 1 字符算；优先 ≤15 字）
2. 正文 ≤ 50 字，必须以一个明确 CTA 结尾，CTA 用 ">>" 结尾（如"立即查看 >>"、"先到先得 >>"、"立即行动 >>"）
3. 严禁夸张承诺与收益保证，禁用词：必涨 / 稳赚 / 保本 / 暴富 / 翻倍 / 100% / 稳赢 / 包赚 / 零风险
4. 涉及具体奖励金额必须带 \`*\` 号脚标（写法：\`S$30*\`、\`S$1,100*\`）
5. 品牌名拼写：产品 / 功能名一律 \`Moomoo\`（首字母大写），禁止 \`moomoo\` 全小写或 \`MOOMOO\` 全大写
6. 不得编造具体数字（涨跌幅 / 估值 / 点位 / 股价），可用"结构性机会"、"低位"、"波动"等定性表达
7. 标题与正文风格独立，正文不要重复标题已说的话

# 风格范例（学这个调性）
1. 标题：SpaceX 上市在即，聚焦万亿太空产业链｜正文：新客入金抢先布局，专属限时加赠 S$30 SpaceX 股票* 等你来领，先到先得 >>
2. 标题：CPI 今夜揭晓，科技股回调布局正当时｜正文：新客入金立领 S$1,100*，趁低位提前卡位结构性机会，立即查看 >>
3. 标题：美股四指齐跌，关注基本面未变的错杀方向｜正文：新客入金立领 S$1,100*，趁回调布局结构性机会，立即查看 >>
4. 标题：🚀 AI 狂潮推升全球股市，STI 站上历史新高｜正文：紧跟 AI 时代的新加坡蓝筹行情，实时行情、K 线、盘口一站看全，决策快人一步 立即查看 >>
5. 标题：您的专属奖励即将失效！｜正文：完成当前任务，即可解锁限量期权手册，助您把握市场机遇！立即行动 >>
6. 标题：SpaceX 史上最大 IPO，你还有最后的机会！｜正文：SpaceX 首日波动是稀缺机会，1 张合约就能站上场内，新客期权首单 0 佣金参与还送期权书 >>
7. 标题：持仓怕回调？1 张 Put 上保险｜正文：期权买方亏损封顶，明牌进场，安心睡觉不盯盘 >>

# 输出格式（严格 JSON，不要任何额外文字）
{
  "title": "标题（≤18 字）",
  "body": "正文（≤50 字，含 CTA >>）",
  "notes": "1 句话说明这条 PUSH 的设计思路：针对哪类用户的什么心理、用了什么钩子（≤45 字）"
}`;

function buildUserPrompt(p) {
  return `请基于以下输入生成一条 PUSH：

- 触发事件 / 主题：${p.event || '未指定'}
- 目标用户分层（TA）：${p.ta || '不限'}
- 生命周期阶段：${p.lifecycle || '不限'}
- 核心信息点（必须传达）：${p.points || '无具体限定，由你判断'}
- 转化目标：${p.goal || '不限'}
- 语气倾向：${p.tone || '专业冷静'}
- 额外备注：${p.notes || '无'}

请按 system 中规则与风格输出 JSON。`;
}

export default async function handler(req, res) {
  // CORS for safety (same-origin in production but harmless)
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'method not allowed' });

  try {
    const body = typeof req.body === 'string' ? JSON.parse(req.body) : (req.body || {});
    const { event, ta, lifecycle, points, goal, tone, notes } = body;
    if (!event) return res.status(400).json({ error: '请填写「触发事件」' });

    const key = process.env.DEEPSEEK_API_KEY;
    if (!key) return res.status(500).json({ error: 'DEEPSEEK_API_KEY 未在 Vercel 环境变量中配置' });

    const r = await fetch('https://api.deepseek.com/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${key}`,
      },
      body: JSON.stringify({
        model: 'deepseek-chat',
        messages: [
          { role: 'system', content: SYSTEM_PROMPT },
          { role: 'user', content: buildUserPrompt({ event, ta, lifecycle, points, goal, tone, notes }) },
        ],
        response_format: { type: 'json_object' },
        max_tokens: 600,
        temperature: 0.85,
      }),
    });
    if (!r.ok) {
      const detail = await r.text();
      return res.status(502).json({ error: 'DeepSeek API 调用失败', detail: detail.slice(0, 300) });
    }
    const data = await r.json();
    const content = data.choices?.[0]?.message?.content || '{}';
    let parsed;
    try { parsed = JSON.parse(content); }
    catch { return res.status(500).json({ error: '解析 JSON 失败', raw: content.slice(0, 400) }); }
    return res.status(200).json({
      title: parsed.title || '',
      body: parsed.body || '',
      notes: parsed.notes || '',
      meta: {
        title_len: [...(parsed.title || '')].length,
        body_len: [...(parsed.body || '')].length,
      },
    });
  } catch (e) {
    return res.status(500).json({ error: 'internal', detail: String(e).slice(0, 300) });
  }
}
