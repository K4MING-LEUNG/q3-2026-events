"""Daily 08:00 news fetcher for the Q3 2026 events site.

Pipeline: RSS → freshness filter → DeepSeek (summary + growth angle) → news.json.
Writes news.json next to the master HTML and to the Cloudflare deploy mirror.
"""
import json
import os
import re
import sys
import traceback
from datetime import datetime, timedelta, timezone
from pathlib import Path

import feedparser
from dotenv import load_dotenv
from openai import OpenAI

from feeds import US_FEEDS, ITEMS_PER_FEED, FRESHNESS_HOURS, TARGET_ITEMS

ROOT = Path(__file__).parent
LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

REPO_ROOT = ROOT.parent
OUT_PATHS = [REPO_ROOT / "news.json"]
# 兼容历史本地路径（如果存在则同步更新）
DESKTOP = Path(r"C:\Users\jiamingliang\Desktop")
if DESKTOP.exists():
    OUT_PATHS += [DESKTOP / "news.json", DESKTOP / "q3-2026-site" / "news.json"]

load_dotenv(ROOT / ".env")
DEEPSEEK_KEY = os.getenv("DEEPSEEK_API_KEY")


def log(msg: str) -> None:
    line = f"[{datetime.now().isoformat(timespec='seconds')}] {msg}"
    print(line, flush=True)
    today = datetime.now().strftime("%Y-%m-%d")
    with open(LOG_DIR / f"{today}.log", "a", encoding="utf-8") as f:
        f.write(line + "\n")


def strip_html(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s or "")
    return " ".join(s.split())


IMPACT_KEYWORDS = [
    # US core
    "us ", "u.s.", "u.s ", "america", "american", "wall street", "fed", "fomc", "powell",
    "treasury", "treasuries", "yellen", "trump", "biden", "white house", "congress", "senate",
    "s&p", "spx", "nasdaq", "dow", "spy", "qqq", "nvidia", "apple", "microsoft", "tesla",
    "google", "alphabet", "meta", "amazon", "boeing", "jpmorgan", "goldman", "morgan stanley",
    "cpi", "ppi", "pce", "nonfarm", "non-farm", "payroll", "jobless", "ism", "gdp",
    "boj", "ecb", "opec", "yen", "dollar", "iran", "ukraine", "tariff", "china tariff",
    "earnings", "q1", "q2", "q3", "q4", "stocks", "bond", "yield", "rate cut", "rate hike",
    # Commodities & supply chain
    "oil", "crude", "brent", "wti", "gold", "copper", "lithium", "uranium", "nickel",
    "semiconductor", "chip", "tsmc", "asml", "supply chain", "port", "suez", "panama canal",
    # Crypto / digital assets
    "bitcoin", "ethereum", "btc", "eth", "crypto", "stablecoin", "spot etf",
    # Macro / global event drivers
    "inflation", "recession", "layoffs", "retail sales", "housing", "mortgage", "credit",
    "debt ceiling", "default", "election", "brexit", "eurozone", "germany", "france",
    "uk economy", "japan economy", "china economy", "korea",
    # Mega events that move consumer / advertising / travel / insurance markets
    "world cup", "olympic", "olympics", "super bowl", "world expo",
    "hurricane", "wildfire", "drought", "earthquake", "typhoon", "climate",
    "pandemic", "outbreak", "vaccine",
    # Big consumer / travel / payments
    "visa", "mastercard", "delta", "united airlines", "marriott", "airbnb", "disney",
]
# Strong negatives = pure regional stories with no global / US linkage
NEGATIVE_KEYWORDS = ["india equity", "indian stock", "pakistan", "vietnam", "philippines", "thailand"]

def impact_score(item: dict) -> int:
    text = (item["title"] + " " + item["raw_summary"]).lower()
    score = sum(1 for kw in IMPACT_KEYWORDS if kw in text)
    score -= sum(2 for kw in NEGATIVE_KEYWORDS if kw in text)
    return score


def fetch_items() -> list[dict]:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=FRESHNESS_HOURS)
    pool: list[dict] = []
    for source, url in US_FEEDS:
        try:
            parsed = feedparser.parse(url, request_headers={"User-Agent": "Mozilla/5.0"})
            entries = parsed.entries[:ITEMS_PER_FEED]
            kept = 0
            for e in entries:
                pub_dt = None
                for key in ("published_parsed", "updated_parsed"):
                    if getattr(e, key, None):
                        pub_dt = datetime(*getattr(e, key)[:6], tzinfo=timezone.utc)
                        break
                if pub_dt and pub_dt < cutoff:
                    continue
                title = (e.get("title") or "").strip()
                if not title:
                    continue
                pool.append({
                    "source": source,
                    "title": title,
                    "url": (e.get("link") or "").strip(),
                    "published_at": pub_dt.isoformat() if pub_dt else "",
                    "raw_summary": strip_html(e.get("summary") or "")[:400],
                })
                kept += 1
            log(f"  [ok]   {source}: {kept} items")
        except Exception as ex:
            log(f"  [err]  {source}: {ex}")
    for item in pool:
        item["_score"] = impact_score(item)
    pool = [x for x in pool if x["_score"] >= 0]
    pool.sort(key=lambda x: (x["_score"], x["published_at"]), reverse=True)
    return pool[:TARGET_ITEMS]


SYSTEM_PROMPT = """你是富途/Moomoo 增长团队的内容编辑助理。任务：把英文财经新闻改写成中文摘要 + 分类 + 给出可落地的"内容增长角度"。

输出 JSON 对象 {"items":[...]}，items 顺序保持输入顺序，每条包含：
- summary: 1-2 句中文，客观陈述事实，不预测、不夸张、不报具体涨跌幅
- category: 必须严格从这 9 类里选一个（不能新造、不能多选）：大盘走势 | 地缘政治 | 金融 | 经济数据 | 财报 | 政策 | 能源 | 科技 | 全球事件
- angle: 1 句中文，给富途增长团队的内容创作建议（如"做 XX 对照表"/"科普 XX 机制"/"梳理 XX 板块标的"），目标是引导用户进行期权交易、ETF 配置或学习金融知识

分类指引：
- 大盘走势：标普/纳指/SPY/QQQ 等指数本身的涨跌、市场宽度、ETF 资金流
- 地缘政治：战争、制裁、关税、贸易争端、外交冲突
- 金融：银行业、并购、IPO、监管、对冲基金、私募
- 经济数据：CPI/PPI/非农/GDP/PCE/消费者信心 等数据发布
- 财报：单家公司业绩、指引、分析师评级
- 政策：Fed/BOJ/ECB 利率决议、货币/财政政策、政府关门
- 能源：油价、OPEC、天然气、石油公司
- 科技：AI、半导体、Mag7 战略、产品发布
- 全球事件：体育大赛（世界杯/奥运/超级碗）、气候灾害（飓风/野火/干旱）、全球大选、供应链中断、疫情等具有跨市场影响的事件——重点说明对消费/旅游/广告/支付/保险/基建等板块的潜在传导

要求：
- 不要在 summary/angle 里编造数字
- 即使新闻本身不直接谈股市，只要有间接传导（如世界杯影响 Visa/Disney/Airbnb），也要在 angle 中点出受益板块或标的方向
- angle 必须以动作开头（做/梳理/科普/对照/拆解 等）
- 每条 angle 都不一样，不要重复模板
"""


def call_deepseek(items: list[dict]) -> list[dict]:
    if not items:
        return []
    client = OpenAI(api_key=DEEPSEEK_KEY, base_url="https://api.deepseek.com")
    user_payload = {
        "items": [
            {"i": idx, "source": x["source"], "title": x["title"], "raw_summary": x["raw_summary"]}
            for idx, x in enumerate(items)
        ]
    }
    user_msg = "原始新闻 JSON：\n" + json.dumps(user_payload, ensure_ascii=False)
    log("calling deepseek-chat...")
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        response_format={"type": "json_object"},
        max_tokens=3500,
        temperature=0.5,
    )
    raw = resp.choices[0].message.content
    log(f"  response chars: {len(raw)}")
    data = json.loads(raw)
    out_items = data.get("items", [])
    enriched: list[dict] = []
    for idx, src in enumerate(items):
        match = next((o for o in out_items if o.get("i") == idx), None)
        if not match and idx < len(out_items):
            match = out_items[idx]
        enriched.append({
            "source": src["source"],
            "title": src["title"],
            "url": src["url"],
            "published_at": src["published_at"],
            "summary": (match or {}).get("summary", src["raw_summary"][:160]),
            "category": (match or {}).get("category", "大盘走势"),
            "angle": (match or {}).get("angle", ""),
        })
    return enriched


SECTOR_PROMPT = """你是富途/Moomoo 行业研究助理。任务：基于今日真实要闻，识别 3-4 个**近期有潜力的美股细分行业/主题**，并给出可溯源的依据。

输出 JSON {"sectors":[{...}]}，每个 sector：
- name: 细分行业/主题中文名（如 "AI 算力·数据中心"、"网络安全"、"国防军工"、"核能·铀矿"、"减肥药 GLP-1"、"电力基础设施"、"网络安全"）
- tickers: 该主题代表标的或 ETF，2-4 个，字符串逗号分隔（用真实美股代码：NVDA, AVGO, SMH, PANW, CRWD, URA, CCJ, LMT, ITA, GE, VST, LLY, NVO 等）
- thesis: 1 句话核心逻辑，≤ 36 字
- drivers: 2-3 条具体驱动因素，每条 ≤ 42 字，必须基于真实已发生事实（财报数字 / 政策 / 资本开支指引 / 地缘冲突），禁止编造
- evidence: 数组，每条 {"i": 引用的新闻 index（必须是输入 items 中实际存在的 index 整数）, "point": 这条新闻支撑了什么观点（≤ 28 字）}
  - 如果今日新闻确实没有支撑某主题的内容，evidence 可以为空数组 []，但要在 drivers 里只用公开已知的近期事实（如"OPEC+ 已宣布减产"、"NVDA 上季 data center 收入 YoY+150%"等可被公开验证的内容），不要瞎编
- risk: 1 句风险提示，≤ 36 字

硬性要求：
- 禁止编造数字、估值、点数预测、具体涨跌幅
- evidence 中的 i 必须真实存在于 items
- 主题选择要"有潜力"≠"今天涨"，重点是结构性逻辑（订单/政策/资本开支/技术拐点）
- 宁可少出主题，不可硬凑；最少 3 个，最多 4 个
- thesis/drivers 用专业冷静的研究语气，不喊口号、不用感叹号
"""


def call_sectors(items: list[dict]) -> dict:
    if not items:
        return {"sectors": []}
    client = OpenAI(api_key=DEEPSEEK_KEY, base_url="https://api.deepseek.com")
    news_brief = "\n".join(
        f"[{idx}] {x['source']} | {x.get('category','')} | {x['title']}"
        + (f"\n     {x.get('summary','') or x['raw_summary'][:140]}" if (x.get('summary') or x['raw_summary']) else "")
        for idx, x in enumerate(items)
    )
    user_msg = (
        f"今日真实要闻（index | 来源 | 分类 | 标题 + 摘要）：\n{news_brief}\n\n"
        f"请基于以上真实新闻 + 你对近期美股已发生事实的常识，识别 3-4 个有潜力的细分行业，"
        f"并在 evidence 中用 i 字段精确引用 items 的 index。"
    )
    log("calling deepseek-chat (sectors)...")
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": SECTOR_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        response_format={"type": "json_object"},
        max_tokens=2500,
        temperature=0.4,
    )
    raw = resp.choices[0].message.content
    log(f"  sector response: {len(raw)} chars")
    data = json.loads(raw)
    sectors = data.get("sectors", [])
    # Hydrate evidence with real news pointer
    for s in sectors:
        ev = s.get("evidence") or []
        hydrated = []
        for e in ev:
            try:
                i = int(e.get("i"))
            except (TypeError, ValueError):
                continue
            if 0 <= i < len(items):
                hydrated.append({
                    "i": i,
                    "point": e.get("point", ""),
                    "source": items[i]["source"],
                    "title": items[i]["title"],
                    "url": items[i]["url"],
                })
        s["evidence"] = hydrated
    return {"sectors": sectors}


def write_outputs(payload: dict) -> None:
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    for p in OUT_PATHS:
        try:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")
            log(f"  wrote {p} ({len(text)} chars)")
        except Exception as ex:
            log(f"  [err] writing {p}: {ex}")


def main() -> int:
    log("=" * 60)
    log("fetch_news start")
    if not DEEPSEEK_KEY:
        log("FATAL: DEEPSEEK_API_KEY missing (.env)")
        return 2
    log("fetching RSS...")
    items = fetch_items()
    log(f"  pool size after freshness filter: {len(items)}")
    if not items:
        log("FATAL: no fresh items")
        return 3
    try:
        enriched = call_deepseek(items)
    except Exception as ex:
        log(f"deepseek failed: {ex} — falling back to raw summaries")
        enriched = [{
            "source": x["source"], "title": x["title"], "url": x["url"],
            "published_at": x["published_at"],
            "summary": x["raw_summary"][:200], "category": "大盘走势", "angle": "",
        } for x in items]
    try:
        sectors_data = call_sectors(enriched)
    except Exception as ex:
        log(f"sectors failed: {ex}")
        sectors_data = {"sectors": []}
    payload = {
        "updated_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "items": enriched,
        "sectors": sectors_data.get("sectors", []),
    }
    write_outputs(payload)
    log("done")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        log("UNCAUGHT EXCEPTION:\n" + traceback.format_exc())
        sys.exit(1)
