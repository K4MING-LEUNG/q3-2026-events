"""International finance RSS sources for the Q3 2026 site daily news module.

Verified live as of 2026-06-12. Sources organized by tier:
1) 一线财经媒体  2) 深度/区域  3) 官方/监管  4) 央行
WSJ / Reuters / Axios / IMF / OECD / OPEC / IEA / US Treasury / BLS RSS feeds
have been confirmed dead or deprecated and are intentionally omitted.
"""

US_FEEDS = [
    # 一线财经媒体（速度 / 全市场覆盖）
    ("Bloomberg", "https://feeds.bloomberg.com/markets/news.rss"),
    ("CNBC", "https://www.cnbc.com/id/100003114/device/rss/rss.html"),
    ("MarketWatch", "https://feeds.content.dowjones.io/public/rss/mw_topstories"),
    ("FT", "https://www.ft.com/markets?format=rss"),
    ("NYT Business", "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml"),
    ("Barron's", "https://feeds.content.dowjones.io/public/rss/RSSMarketsMain"),
    ("Seeking Alpha", "https://seekingalpha.com/market_currents.xml"),

    # 深度评论 / 区域视角
    ("Economist Finance", "https://www.economist.com/finance-and-economics/rss.xml"),
    ("Economist Business", "https://www.economist.com/business/rss.xml"),
    ("Nikkei Asia", "https://asia.nikkei.com/rss/feed/nar"),

    # 官方 / 监管
    ("Federal Reserve", "https://www.federalreserve.gov/feeds/press_all.xml"),
    ("SEC Press", "https://www.sec.gov/news/pressreleases.rss"),

    # 主要央行（影响汇率/利率/全球流动性）
    ("Bank of England", "https://www.bankofengland.co.uk/rss/news"),
    ("Bank of Japan", "https://www.boj.or.jp/en/rss/whatsnew.xml"),
]

ITEMS_PER_FEED = 5
FRESHNESS_HOURS = 30
TARGET_ITEMS = 9
