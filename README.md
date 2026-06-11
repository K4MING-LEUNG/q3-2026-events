# Q3 2026 · 美股事件 & 增长内容

Futu / Moomoo 增长团队用的 Q3 2026 美股事件 + 期权 PUSH 文案站点。
Apple-style 单页 SPA，每日 8:00 自动抓取财经头条 + DeepSeek 实时分析，可溯源到原文。

## 功能

- **Today's Spotlight** — 当日最重要事件
- **Today, in markets** — Bento Grid 布局，9 条美股要闻 + 中文增长角度
- **Strategy Lab** — DeepSeek 基于当日真实新闻识别 3-4 个有潜力的美股细分行业，带原文 Evidence
- **Calendar** — 6/7/8/9 月日历，可切换月份
- **Super Nodes** — 15 个 Super 节点，默认显示 6 个可展开
- **All Events** — 37 个事件全列表，多维度筛选
- **PUSH Library** — 37 条 PUSH 文案库，支持搜索

## 项目结构

```
.
├── index.html              # 主站（Vanilla JS SPA）
├── news.json               # 当日新闻 + sectors（每日 8:00 由 fetcher 生成）
├── vercel.json             # Vercel 静态站点配置
├── fetcher/                # Python 抓取 + DeepSeek 分析
│   ├── fetch_news.py       # 主流程：RSS → 美股相关性筛选 → DeepSeek 摘要 + 行业分析
│   ├── feeds.py            # RSS 源列表
│   ├── requirements.txt
│   ├── run.bat             # Windows 启动器
│   └── setup_task.ps1      # 注册 Task Scheduler 每日 8:00
└── push-library/           # PUSH 文案生成器
    ├── gen_push.js         # 37 条 PUSH 元数据
    ├── push_copy.js        # 输出：标题/正文映射
    ├── lib_data.js         # 输出：嵌入到 HTML 的库数据
    └── q3_2026_options_push_library.csv  # CSV 导出
```

## 本地运行

```bash
# 启动静态站
python -m http.server 8765

# 抓取最新新闻 + DeepSeek 分析
cd fetcher
pip install -r requirements.txt
# 在 fetcher/.env 填入 DEEPSEEK_API_KEY=sk-xxxxx
python fetch_news.py
```

## 部署

Vercel 自动检测 `index.html` 即可部署，无需构建命令。`vercel.json` 设置了 `news.json` 5 分钟边缘缓存。

## 新闻数据流

```
RSS (Bloomberg/CNBC/MarketWatch/FT/NYT) 
  → 美股关键词打分筛选（Fed/Powell/Mag7/CPI/PPI 等）
  → DeepSeek-Chat（中文摘要 + 8 类分类 + 增长角度）
  → DeepSeek-Chat（基于本日要闻识别细分行业 + Evidence 溯源）
  → news.json
```

## 配置

`fetcher/.env`（不入仓）:

```
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

## 不构成投资建议

所有分析仅作研究方法论展示。
