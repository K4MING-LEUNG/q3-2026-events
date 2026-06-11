"""US finance RSS sources for the Q3 2026 site daily news module.

Verified live as of 2026-06-08 (memory/reference_us_finance_rss.md).
WSJ feeds intentionally omitted — confirmed dead.
"""

US_FEEDS = [
    ("Bloomberg", "https://feeds.bloomberg.com/markets/news.rss"),
    ("CNBC", "https://www.cnbc.com/id/100003114/device/rss/rss.html"),
    ("MarketWatch", "https://feeds.content.dowjones.io/public/rss/mw_topstories"),
    ("FT", "https://www.ft.com/markets?format=rss"),
    ("NYT Business", "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml"),
    ("Federal Reserve", "https://www.federalreserve.gov/feeds/press_all.xml"),
]

ITEMS_PER_FEED = 6
FRESHNESS_HOURS = 30
TARGET_ITEMS = 9
