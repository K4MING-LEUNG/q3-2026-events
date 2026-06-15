"""Rebuild index.html EVENTS array, modal renderer, nav order, list filter, and PUSH_LIBRARY
from the 4 monthly JSON files. Designed to avoid huge inline Edits.

Run: python fetcher/rebuild_events.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
HTML = ROOT / "index.html"
FETCHER = Path(__file__).parent

MIRRORS = [
    Path(r"C:\Users\jiamingliang\Desktop\美股事件Q3-2026-AppleStyle.html"),
    Path(r"C:\Users\jiamingliang\Desktop\q3-2026-site\index.html"),
]

# ----------------------------------------------------------------------------
# 1. Load events
# ----------------------------------------------------------------------------
events = []
for m in ("jun", "jul", "aug", "sep"):
    events += json.loads((FETCHER / f"events_{m}.json").read_text(encoding="utf-8"))

events.sort(key=lambda e: e["date"])
print(f"loaded {len(events)} events")

# ----------------------------------------------------------------------------
# 2. Build new EVENTS JS array — JSON is valid JS for our shape
# ----------------------------------------------------------------------------
events_js = "const EVENTS=" + json.dumps(events, ensure_ascii=False) + ";"

# ----------------------------------------------------------------------------
# 3. New openModal — 5 sections (背景 / 标的 / 增长机会 / 术语 / 营销文案)
# ----------------------------------------------------------------------------
modal_js = r"""
function copyPush(id,btn){
  const ev=EVENTS.find(x=>x.id===id);if(!ev||!ev.push)return;
  const text=(ev.push.title||'')+'\n'+(ev.push.body||'');
  navigator.clipboard.writeText(text).then(()=>{
    if(btn){const o=btn.textContent;btn.textContent='已复制 ✓';setTimeout(()=>btn.textContent=o||'复制文案',1600);}
  });
}
function openModal(id){
  const e=EVENTS.find(x=>x.id===id);if(!e)return;
  const cats=e.cats.map(c=>`<span class="badge">${CATEGORIES[c]?.label||c}</span>`).join(' ');
  const stars='★'.repeat(e.imp);
  const impCls=e.imp===3?'badge-imp-3':e.imp===2?'badge-imp-2':'badge';
  const mk=MARKETS[e.market]||{label:e.market||'—',cls:'mkt-other'};
  const mktBadge=`<span class="mkt-badge ${mk.cls}">${mk.label}</span>`;
  const srcLink=e.source?.url?`<a href="${e.source.url}" target="_blank" rel="noopener" class="m-src-link">${e.source.name||'Source'} ↗</a>`:(e.source?.name||'');
  const tickers=(e.tickers||[]).map(t=>`<code class="m-tk">${t}</code>`).join('')||'<span style="color:var(--text4)">—</span>';
  const jargon=(e.jargon||[]).map(j=>`<div class="m-jg"><b>${j.t}</b><span>${j.d}</span></div>`).join('');
  const push=e.push||{};
  $('#modal').innerHTML=`
    <button id="modal-close" onclick="closeModal()">×</button>
    <div class="m-meta">${e.date} · 周${e.weekday} · ${srcLink}</div>
    <h2 class="m-title">${e.title}</h2>
    <div class="m-badges">${mktBadge}<span class="badge ${impCls}">${stars} Importance</span>${cats}${e.confirmed?'':'<span class="badge unc">未确认</span>'}</div>
    <p class="m-summary">${e.summary||''}</p>

    <div class="m-section"><div class="m-label">① 基础背景</div><div class="m-bg">${(e.background||'').replace(/\n/g,'<br>')}</div></div>

    <div class="m-section"><div class="m-label">② 可能受影响的标的</div><div class="m-tks">${tickers}</div></div>

    <div class="m-section"><div class="m-label">③ 增长运营机会</div>
      ${e.hook?`<div class="m-hook"><span class="lab">钩子</span>${e.hook}</div>`:''}
      ${e.angle?`<div class="m-angle"><span class="lab">增长角度</span>${e.angle}</div>`:''}
    </div>

    ${jargon?`<div class="m-section"><div class="m-label">④ 专业术语</div><div class="m-jgs">${jargon}</div></div>`:''}

    ${(push.title||push.body)?`<div class="m-section"><div class="m-label">⑤ 营销文案 · 即用</div>
      <div class="push-block">
        ${push.title?`<div class="push-hook">${push.title}</div>`:''}
        ${push.body?`<div class="push-path">${push.body}</div>`:''}
        <button class="m-copy" onclick="copyPush('${e.id}',this)">复制文案</button>
      </div>
    </div>`:''}

    ${e.source?.url?`<div class="m-source-foot">信源:<a href="${e.source.url}" target="_blank" rel="noopener">${e.source.name||e.source.url}</a></div>`:''}
  `;
  $('#modal-bg').classList.add('show');
  document.body.style.overflow='hidden';
}
"""

# ----------------------------------------------------------------------------
# 4. New list filter — add market dimension
# ----------------------------------------------------------------------------
list_filter_js = r"""
let currentFilter='all';
let currentMarket='all';
let listExpanded=false;
const LIST_INITIAL=10;
function renderListFilters(){
  const filters=[
    {k:'all',label:'All'},
    {k:'imp3',label:'Super (★★★)'},
    {k:'imp2',label:'Major (★★)'},
    {k:'fomc',label:'央行'},
    {k:'macro',label:'宏观'},
    {k:'earnings',label:'财报'},
    {k:'global',label:'全球事件'},
    {k:'holiday',label:'休市'}
  ];
  const markets=[
    {k:'all',label:'全部市场'},
    {k:'US',label:'美股'},
    {k:'HK',label:'港股'},
    {k:'SG',label:'星股'},
    {k:'JP',label:'日股'},
    {k:'KR',label:'韩股'},
    {k:'EU',label:'欧洲'},
    {k:'GLOBAL',label:'全球'}
  ];
  $('#list-filters').innerHTML=
    '<div class="filter-row">'+filters.map(f=>`<button class="filter-btn ${f.k===currentFilter?'active':''}" data-k="${f.k}">${f.label}</button>`).join('')+'</div>'+
    '<div class="filter-row mkt-row">'+markets.map(m=>`<button class="filter-btn mkt ${m.k===currentMarket?'active':''}" data-m="${m.k}">${m.label}</button>`).join('')+'</div>';
  $$('#list-filters .filter-btn[data-k]').forEach(b=>b.onclick=()=>{currentFilter=b.dataset.k;renderListFilters();renderList()});
  $$('#list-filters .filter-btn[data-m]').forEach(b=>b.onclick=()=>{currentMarket=b.dataset.m;renderListFilters();renderList()});
}
function renderList(){
  let list=EVENTS.slice().sort((a,b)=>a.date.localeCompare(b.date));
  if(currentFilter==='imp3')list=list.filter(e=>e.imp===3);
  else if(currentFilter==='imp2')list=list.filter(e=>e.imp===2);
  else if(currentFilter!=='all')list=list.filter(e=>e.cats.includes(currentFilter));
  if(currentMarket!=='all')list=list.filter(e=>e.market===currentMarket);
  const total=list.length;
  const visible=listExpanded?list:list.slice(0,LIST_INITIAL);
  const rows=visible.map(e=>{
    const stars='★'.repeat(e.imp);
    const impCls=e.imp===3?'badge-imp-3':e.imp===2?'badge-imp-2':'badge';
    const mk=MARKETS[e.market]||{label:e.market||'—',cls:'mkt-other'};
    return `<div class="list-row" onclick="openModal('${e.id}')">
      <div class="date">${fmtMD(e.date)}<span class="wd">周${e.weekday}</span></div>
      <div class="imp"><span class="badge ${impCls}">${stars}</span></div>
      <div class="ttl"><span class="mkt-badge ${mk.cls}" style="margin-right:8px">${mk.label}</span>${e.title}<span class="sum">${e.summary}</span></div>
      <div class="arrow">→</div>
    </div>`;
  }).join('')||'<div style="padding:48px;text-align:center;color:var(--text4)">No events match this filter.</div>';
  $('#list-wrap').innerHTML=rows;
  const wrap=$('#list-wrap').parentElement;
  let existing=$('#list-toggle-wrap');
  if(existing)existing.remove();
  if(total>LIST_INITIAL){
    const div=document.createElement('div');
    div.id='list-toggle-wrap';
    div.className='super-toggle-wrap';
    div.innerHTML=`<button class="super-toggle" id="list-toggle">${listExpanded?`收起 ↑`:`展开全部 ${total} 个事件 ↓`}</button>`;
    wrap.appendChild(div);
    $('#list-toggle').addEventListener('click',()=>{listExpanded=!listExpanded;renderList();});
  }
}
"""

# ----------------------------------------------------------------------------
# 5. PUSH_LIBRARY auto-derive from EVENTS
# ----------------------------------------------------------------------------
library_js = r"""
const PUSH_LIBRARY=EVENTS.filter(e=>e.push&&(e.push.title||e.push.body)).map((e,i)=>[i+1,e.title,fmtMD(e.date),(e.tickers||[]).join(','),e.angle||'',e.push.title||'',e.push.body||'',e.market||'',e.id]);
let libSearch='';
let libMarket='all';
function renderLibFilters(){
  const markets=[{k:'all',label:'全部'},{k:'US',label:'美股'},{k:'HK',label:'港股'},{k:'SG',label:'星股'},{k:'JP',label:'日股'},{k:'KR',label:'韩股'},{k:'EU',label:'欧洲'},{k:'GLOBAL',label:'全球'}];
  const wrap=$('#lib-filters');
  if(!wrap)return;
  wrap.innerHTML=markets.map(m=>`<button class="filter-btn ${m.k===libMarket?'active':''}" data-m="${m.k}">${m.label}</button>`).join('');
  $$('#lib-filters .filter-btn').forEach(b=>b.onclick=()=>{libMarket=b.dataset.m;renderLibFilters();renderLibTable()});
}
function renderLibTable(){
  const q=libSearch.toLowerCase();
  let rows=PUSH_LIBRARY.filter(r=>libMarket==='all'||r[7]===libMarket);
  if(q)rows=rows.filter(r=>r.slice(1,7).join(' ').toLowerCase().includes(q));
  $('#lib-count').innerHTML='<b>'+rows.length+'</b> / '+PUSH_LIBRARY.length+' 条';
  const tbody=$('#lib-tbody');
  if(!tbody)return;
  tbody.innerHTML=rows.map((r,i)=>{
    const mk=MARKETS[r[7]]||{label:r[7]||'—',cls:'mkt-other'};
    return `<tr onclick="openModal('${r[8]}')" style="cursor:pointer">
      <td class="col-num">${i+1}</td>
      <td class="col-evt"><span class="mkt-badge ${mk.cls}" style="margin-right:6px">${mk.label}</span>${r[1]}</td>
      <td class="col-time">${r[2]}</td>
      <td class="col-tk">${r[4]}</td>
      <td class="col-title">${r[5]}</td>
      <td class="col-body">${r[6]}</td>
    </tr>`;
  }).join('')||'<tr><td colspan="6" style="padding:32px;text-align:center;color:var(--text4)">无匹配文案</td></tr>';
}
"""

# ----------------------------------------------------------------------------
# 6. Markets registry + new CSS — injected before </style>
# ----------------------------------------------------------------------------
markets_and_css = r"""
const MARKETS={
  US:{label:'美股',cls:'mkt-us'},
  HK:{label:'港股',cls:'mkt-hk'},
  SG:{label:'星股',cls:'mkt-sg'},
  JP:{label:'日股',cls:'mkt-jp'},
  KR:{label:'韩股',cls:'mkt-kr'},
  EU:{label:'欧洲',cls:'mkt-eu'},
  GLOBAL:{label:'全球',cls:'mkt-global'}
};
"""

extra_css = """
.mkt-badge{display:inline-flex;align-items:center;padding:2px 8px;border-radius:6px;font-size:11px;font-weight:600;letter-spacing:.02em}
.mkt-us{background:rgba(0,113,227,.12);color:#0071e3}
.mkt-hk{background:rgba(255,159,10,.14);color:#a05a00}
.mkt-sg{background:rgba(255,69,58,.12);color:#c2261d}
.mkt-jp{background:rgba(175,82,222,.12);color:#7d3acf}
.mkt-kr{background:rgba(48,176,199,.12);color:#1f8a9e}
.mkt-eu{background:rgba(52,199,89,.12);color:#1f7d35}
.mkt-global{background:rgba(142,142,147,.16);color:#555}
.mkt-other{background:rgba(142,142,147,.12);color:#888}
.filter-row{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:8px}
.filter-row.mkt-row{margin-top:4px}
#modal-close{position:absolute;top:20px;right:20px;width:32px;height:32px;border-radius:50%;background:var(--bg2);font-size:18px;color:var(--text3);display:flex;align-items:center;justify-content:center;border:0;cursor:pointer}
#modal .m-meta{font-size:13px;color:var(--text4);font-variant-numeric:tabular-nums;margin-bottom:8px}
#modal .m-meta .m-src-link{color:var(--accent);text-decoration:none;margin-left:6px}
#modal .m-meta .m-src-link:hover{text-decoration:underline}
#modal .m-title{font-size:30px;font-weight:600;letter-spacing:-.018em;line-height:1.2;margin:0 0 14px}
#modal .m-badges{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:18px}
#modal .m-badges .unc{background:rgba(255,149,0,.12);color:#a04e00}
#modal .m-summary{font-size:17px;line-height:1.55;color:var(--text);margin:0 0 22px;letter-spacing:-.005em}
#modal .m-section{margin-bottom:22px}
#modal .m-label{font-size:12.5px;color:var(--text3);font-weight:600;margin-bottom:8px;letter-spacing:.04em}
#modal .m-bg{font-size:14px;line-height:1.7;color:var(--text2);background:var(--bg2);padding:18px 22px;border-radius:12px}
#modal .m-tks{display:flex;flex-wrap:wrap;gap:6px}
#modal .m-tk{background:var(--bg2);padding:4px 10px;border-radius:6px;font-family:'SF Mono',Menlo,monospace;font-size:13px;color:var(--text)}
#modal .m-hook,#modal .m-angle{padding:12px 16px;background:linear-gradient(135deg,rgba(0,113,227,.06),rgba(175,82,222,.06));border-radius:10px;font-size:14px;color:var(--text2);margin-bottom:8px;line-height:1.55}
#modal .m-hook .lab,#modal .m-angle .lab{display:inline-block;color:var(--accent);font-weight:600;margin-right:8px;font-size:11px;letter-spacing:.06em;text-transform:uppercase;vertical-align:1px}
#modal .m-jgs{display:grid;gap:8px}
#modal .m-jg{padding:10px 14px;background:var(--bg2);border-left:3px solid var(--accent);border-radius:8px;font-size:13.5px;line-height:1.55}
#modal .m-jg b{color:var(--text);margin-right:8px;font-family:'SF Mono',Menlo,monospace;font-weight:600}
#modal .m-jg span{color:var(--text2)}
#modal .push-block{background:linear-gradient(135deg,rgba(0,113,227,.05),rgba(175,82,222,.05));padding:18px 22px;border-radius:14px;border:1px solid rgba(0,113,227,.12)}
#modal .push-block .push-hook{font-size:16px;font-weight:600;color:var(--text);margin-bottom:8px;line-height:1.4}
#modal .push-block .push-path{font-size:13.5px;color:var(--text2);line-height:1.6;margin-bottom:12px}
#modal .m-copy{padding:8px 16px;background:var(--accent);color:#fff;border-radius:8px;font-size:13px;border:0;cursor:pointer;font-weight:500}
#modal .m-copy:hover{opacity:.9}
#modal .m-source-foot{margin-top:18px;padding-top:14px;border-top:1px solid var(--border);font-size:12px;color:var(--text4)}
#modal .m-source-foot a{color:var(--accent);text-decoration:none;margin-left:6px}
#modal .m-source-foot a:hover{text-decoration:underline}
"""

# ----------------------------------------------------------------------------
# 7. Apply replacements
# ----------------------------------------------------------------------------
src = HTML.read_text(encoding="utf-8")

# 7a. Replace EVENTS array (bracket-match, robust to single-line or multiline)
def _replace_events(s):
    idx = s.find("const EVENTS=[")
    if idx < 0:
        return s
    i = idx + len("const EVENTS=")
    depth = 0
    while i < len(s):
        c = s[i]
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                end = i + 1
                # consume trailing ;
                if end < len(s) and s[end] == ";":
                    end += 1
                return s[:idx] + events_js + s[end:]
        i += 1
    return s
src = _replace_events(src)

# 7b. Remove old PUSH_COPY block (now embedded per-event)
src = re.sub(
    r"const PUSH_COPY=\{[\s\S]*?\n\};\n",
    "const PUSH_COPY={};\n",
    src,
    count=1,
)

# 7c. Replace openModal function
src = re.sub(
    r"// ========== MODAL ==========\nfunction openModal\(id\)\{[\s\S]*?\nfunction closeModal",
    "// ========== MODAL ==========\n" + modal_js + "\nfunction closeModal",
    src,
    count=1,
)

# 7d. Replace list filter & render
src = re.sub(
    r"// ========== LIST \+ FILTERS ==========\nlet currentFilter[\s\S]*?\$\('#list-toggle'\)\.addEventListener\('click',\(\)=>\{listExpanded=!listExpanded;renderList\(\);\}\);\n  \}\n\}",
    "// ========== LIST + FILTERS ==========" + list_filter_js,
    src,
    count=1,
)

# 7e. Replace PUSH_LIBRARY block
src = re.sub(
    r"// ========== LIBRARY ==========\nconst PUSH_LIBRARY=\[\[[\s\S]*?\$\('#lib-count'\)\.innerHTML='<b>'\+rows\.length\+'</b> / '\+PUSH_LIBRARY\.length\+' 条';",
    "// ========== LIBRARY ==========\n" + library_js + "\nfunction __libNoop(){",
    src,
    count=1,
)
# Old renderLibTable body remains after our injection — strip up to its closing brace
# Easier: search and remove the residual old function body up to next closing
# We'll just close our injected __libNoop with a no-op and let the old body fall through harmlessly.
# Actually a cleaner approach: use a more aggressive replacement. Re-do it.
src = src.replace("function __libNoop(){", "function __libNoopOld(){")

# 7f. Insert MARKETS registry before EVENTS (idempotent — skip if already present)
if "const MARKETS=" not in src:
    src = src.replace(
        "const TODAY=(()=>",
        markets_and_css.strip() + "\nconst TODAY=(()=>",
        1,
    )

# 7g. Inject extra CSS before </style>
src = src.replace("</style>", extra_css + "\n</style>", 1)

# 7h. Reorder nav: Library after PUSH 生成器
src = re.sub(
    r'(<a href="#list">Events</a>)\s*\n\s*<a href="#library">Library</a>\s*\n\s*<a href="#push-gen" class="nav-new">PUSH 生成器<span class="nav-badge">NEW</span></a>',
    r'\1\n      <a href="#push-gen" class="nav-new">PUSH 生成器<span class="nav-badge">NEW</span></a>\n      <a href="#library">Library</a>',
    src,
    count=1,
)

# 7i. Add lib-filters mount point under search box if missing
if 'id="lib-filters"' not in src:
    src = src.replace(
        '<div class="lib-search"><input type="text" id="lib-search-input"',
        '<div id="lib-filters" class="filter-row" style="margin-bottom:10px"></div>\n      <div class="lib-search"><input type="text" id="lib-search-input"',
        1,
    )

# 7j. Make sure renderLibFilters is invoked at boot — append a tiny init patch
init_patch = "\nif(typeof renderLibFilters==='function'){try{renderLibFilters()}catch(e){}}\n"
if init_patch.strip() not in src:
    src = src.replace("</script>\n</body>", init_patch + "</script>\n</body>", 1)

# ----------------------------------------------------------------------------
# 8. Write
# ----------------------------------------------------------------------------
HTML.write_text(src, encoding="utf-8")
print(f"wrote {HTML} ({len(src)} chars)")

for m in MIRRORS:
    if m.parent.exists():
        m.write_text(src, encoding="utf-8")
        print(f"mirrored -> {m}")
    else:
        print(f"skip mirror (missing dir): {m}")
print("done.")
