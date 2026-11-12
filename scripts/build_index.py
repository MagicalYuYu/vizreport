# Build the unified visualization-report index v2 (07_EXPORTS/showcase-index.html)
# v2: three view modes (cards / compact list / detailed list) x four sorts,
#     pin/hide per report + manage panel, persisted prefs, search, iframe preview.
import json
import os
import re
import sys
import datetime

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = 'D:/AOS/07_EXPORTS'
OUT = os.path.join(ROOT, 'showcase-index.html')

PAGE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="color-scheme" content="light dark">
<title>AOS · 可视化报告索引</title>
<style>
:root{--bg:#F3F4F6;--surface:#FFF;--border:#D8DDE4;--border-hi:#A9B4C2;--text:#1B2430;--muted:#4B5563;--faint:#68737F;
--accent:#16A34A;--accent-hi:#15803D;--accent-soft:rgba(22,163,74,.10);--cyan-hi:#0369A1;--cyan-soft:rgba(2,132,199,.09);
--rail-bg:rgba(255,255,255,.92);
--mono:"Fira Code","Cascadia Code",Consolas,monospace;--sans:"Segoe UI",system-ui,"PingFang SC","Microsoft YaHei",sans-serif}
[data-theme="dark"]{--bg:#020617;--surface:#0B1120;--border:#26304A;--border-hi:#3D4A6B;--text:#F8FAFC;--muted:#94A3B8;--faint:#64748B;
--accent:#22C55E;--accent-hi:#4ADE80;--accent-soft:rgba(34,197,94,.13);--cyan-hi:#7DD3FC;--cyan-soft:rgba(56,189,248,.10);
--rail-bg:rgba(11,17,32,.92)}
*{box-sizing:border-box;margin:0;padding:0}html{font-size:17px}
body{font-family:var(--sans);background:var(--bg);color:var(--text);line-height:1.6;min-height:100vh}
.wrap{max-width:1180px;margin:0 auto;padding:0 22px}
header{border-bottom:1px solid var(--border);padding:38px 0 40px;background:var(--surface)}
.brand{font-family:var(--mono);font-size:.88rem;color:var(--faint);margin-bottom:14px}
h1{font-family:var(--mono);font-size:clamp(1.25rem,2.6vw,1.55rem)}
.sub{color:var(--muted);margin-top:8px;max-width:76ch}
.bar{display:flex;gap:10px;align-items:center;margin-top:22px;flex-wrap:wrap}
.search{flex:1;min-width:200px;display:flex;align-items:center;gap:8px;background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:0 12px;min-height:42px}
.search input{flex:1;border:0;outline:0;background:none;color:var(--text);font-family:var(--mono);font-size:.9rem}
.count{font-family:var(--mono);font-size:.85rem;color:var(--faint);white-space:nowrap}
.sel{background:var(--surface);border:1px solid var(--border);color:var(--muted);border-radius:8px;height:42px;padding:0 10px;font-family:var(--mono);font-size:.85rem;cursor:pointer}
.vbtn{border:1px solid var(--border);background:var(--surface);color:var(--muted);border-radius:8px;height:42px;padding:0 13px;cursor:pointer;font-family:var(--mono);font-size:.85rem}
.vbtn:hover{color:var(--text);border-color:var(--border-hi)}
.vbtn.on{color:var(--accent-hi);border-color:var(--accent);background:var(--accent-soft)}
main{padding:44px 0 56px}
/* 卡片视图 */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:18px}
.card{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:18px 20px;transition:border-color .15s,transform .15s;display:flex;flex-direction:column;gap:10px}
.card:hover{border-color:var(--accent);transform:translateY(-2px)}
.card.pinned{border-color:var(--accent)}
h3.t{font-size:1rem;font-weight:600}
.meta{font-family:var(--mono);font-size:.8rem;color:var(--faint);display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.desc{font-size:.88rem;color:var(--muted)}
.path{font-family:var(--mono);font-size:.72rem;color:var(--faint);overflow-wrap:anywhere}
.badge{font-family:var(--mono);font-size:.75rem;padding:2px 9px;border-radius:999px;border:1px solid var(--border);color:var(--muted)}
.badge.r{color:var(--cyan-hi);border-color:var(--cyan-hi);background:var(--cyan-soft)}
.badge.c{color:var(--accent-hi);border-color:var(--accent);background:var(--accent-soft)}
.acts{display:flex;gap:8px;margin-top:auto;padding-top:6px;flex-wrap:wrap}
.acts a,.acts button{font-family:var(--mono);font-size:.8rem;text-decoration:none;border:1px solid var(--border);border-radius:7px;padding:5px 11px;color:var(--muted);background:none;cursor:pointer}
.acts a:hover,.acts button:hover{color:var(--text);border-color:var(--accent)}
.acts button.on{color:var(--accent-hi);border-color:var(--accent)}
/* 横条视图 */
.list{display:flex;flex-direction:column;gap:10px}
.row{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:14px 18px;display:flex;gap:14px;align-items:center;flex-wrap:wrap;transition:border-color .15s}
.row:hover{border-color:var(--accent)}
.row.pinned{border-color:var(--accent)}
.row .t{font-weight:600;font-size:.95rem;flex:1;min-width:200px}
.row .meta{font-size:.78rem}
.row .desc{flex-basis:100%;font-size:.85rem;color:var(--muted);display:none}
.list.detail .row .desc{display:block}
.list.detail .row .path{display:block;flex-basis:100%}
.row .path{display:none}
.empty{grid-column:1/-1;text-align:center;padding:50px;color:var(--faint);font-family:var(--mono);border:1px dashed var(--border);border-radius:10px}
/* 管理面板 */
.mgr{display:none;margin-top:20px;border:1px solid var(--border);border-radius:10px;background:var(--surface);padding:18px 20px}
.mgr.open{display:block}
.mgr .mt{font-family:var(--mono);font-size:.8rem;color:var(--faint);margin-bottom:10px}
.mgr .hidden-item{display:flex;align-items:center;gap:10px;padding:9px 0;border-bottom:1px dashed var(--border);font-size:.88rem}
.mgr .hidden-item:last-child{border-bottom:0}
.mgr .hidden-item span{flex:1;overflow-wrap:anywhere}
.mgr button{font-family:var(--mono);font-size:.78rem;border:1px solid var(--border);border-radius:7px;padding:4px 10px;background:none;color:var(--muted);cursor:pointer}
.mgr button:hover{color:var(--text);border-color:var(--accent)}
/* 预览 */
.viewer{position:fixed;inset:0;z-index:90;background:rgba(10,15,26,.72);display:none}
.viewer.open{display:flex;flex-direction:column}
.viewer .top{display:flex;align-items:center;gap:12px;background:var(--surface);border-bottom:1px solid var(--border);padding:10px 16px}
.viewer .top .t{font-family:var(--mono);font-size:.9rem;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.viewer .top button,.viewer .top a{font-family:var(--mono);font-size:.82rem;border:1px solid var(--border);border-radius:7px;padding:6px 12px;background:none;color:var(--muted);cursor:pointer;text-decoration:none}
.viewer iframe{flex:1;width:100%;border:0;background:#fff}
footer{border-top:1px solid var(--border);color:var(--faint);font-size:.85rem;padding:26px 0 48px;margin-top:10px}
footer .fnote{font-family:var(--mono);font-size:.8rem}
/* 设置面板 */
.settings-pop{position:fixed;right:64px;bottom:16px;z-index:70;width:290px;max-width:calc(100vw - 80px);background:var(--rail-bg);border:1px solid var(--border);border-radius:12px;box-shadow:0 4px 14px rgba(15,23,42,.16);backdrop-filter:blur(10px);padding:14px 16px;display:none}
.settings-pop.open{display:block}
.settings-pop .st{font-family:var(--mono);font-size:.75rem;letter-spacing:.03em;color:var(--faint);text-transform:uppercase;margin-bottom:6px}
.settings-pop label{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:8px 0;font-size:.9rem;color:var(--text);border-bottom:1px dashed var(--border)}
.settings-pop label:last-of-type{border-bottom:0}
.settings-pop select{background:var(--surface);border:1px solid var(--border);color:var(--text);border-radius:6px;height:30px;font-size:.85rem;padding:0 6px}
.settings-pop input[type=checkbox]{width:17px;height:17px;accent-color:var(--accent)}
.settings-pop .foot{margin-top:10px}
.settings-pop .foot button{width:100%;font-family:var(--mono);font-size:.8rem;padding:6px;border-radius:6px;border:1px solid var(--border);background:var(--surface);color:var(--muted);cursor:pointer}
@media print{.bar,.acts,.mgr,.viewer{display:none!important}}
</style>
</head>
<body>
<header><div class="wrap">
<div class="brand">▚▞ AOS // SHOWCASE INDEX v2</div>
<h1>可视化报告索引</h1>
<p class="sub">所有项目 report / showcase 单文件的统一入口。数据源=扫描 07_EXPORTS（交付后由 build_index.py 刷新）；置顶/隐藏为视图层状态（本机持久，不动文件）。</p>
<div class="bar">
<label class="search"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg><input id="q" type="search" placeholder="搜索标题 / 路径 / 类型…" aria-label="搜索报告"></label>
<select id="sort" class="sel" aria-label="排序">
<option value="updated">排序：最近更新</option>
<option value="title">排序：标题</option>
<option value="size">排序：文件大小</option>
<option value="type">排序：类型</option>
</select>
<button id="vCard" class="vbtn on" type="button" title="卡片视图">▦ 卡片</button>
<button id="vList" class="vbtn" type="button" title="紧凑横条">☰ 横条</button>
<button id="vDetail" class="vbtn" type="button" title="详细横条">☰☰ 详细</button>
<button id="mgrBtn" class="vbtn" type="button">⚙ 管理</button>
<button id="setBtn" class="vbtn" type="button" aria-expanded="false" title="索引设置">☰ 设置</button>
<button id="themeBtn" class="vbtn" type="button" aria-pressed="false">☾ 主题</button>
<span class="count" id="count"></span>
</div>
<div class="mgr" id="mgr">
<div class="mt">已隐藏的报告（视图层，可随时恢复；文件本体不受影响）</div>
<div id="mgrList"></div>
</div>
<div class="settings-pop" id="setPop" role="dialog" aria-label="索引设置">
<div class="st">索引设置（本机持久）</div>
<label>默认视图
<select id="sView"><option value="card">卡片</option><option value="list">横条</option><option value="detail">详细</option></select>
</label>
<label>默认排序
<select id="sSort"><option value="updated">最近更新</option><option value="title">标题</option><option value="size">大小</option><option value="type">类型</option></select>
</label>
<label>卡片显示描述<input type="checkbox" id="sDesc" checked></label>
<label>卡片显示路径<input type="checkbox" id="sPath" checked></label>
<div class="foot"><button type="button" id="sReset">重置本页全部偏好</button></div>
</div>
</div></header>
<main class="wrap"><div id="host"></div></main>
<footer><div class="wrap"><div class="fnote" id="foot"></div></div></footer>
<div class="viewer" id="viewer"><div class="top"><span class="t" id="vTitle"></span><a id="vOpen" href="#" target="_blank" rel="noopener noreferrer">↗ 新标签页</a><button id="vClose" type="button">✕ 关闭预览</button></div><iframe id="vFrame" title="报告预览"></iframe></div>
<script id="idx-data" type="application/json">__DATA__</script>
<script>
(function(){
var esc=function(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});};
var DATA=JSON.parse(document.getElementById('idx-data').textContent);
var host=document.getElementById('host'),q=document.getElementById('q'),count=document.getElementById('count');
var K={view:'aos-idx-view',sort:'aos-idx-sort',pin:'aos-idx-pin',hide:'aos-idx-hide',desc:'aos-idx-desc',path:'aos-idx-path'};
function ls(k,d){try{var v=localStorage.getItem(k);return v===null?d:JSON.parse(v);}catch(e){return d;}}
function lsSet(k,v){try{localStorage.setItem(k,JSON.stringify(v));}catch(e){}}
var view=ls(K.view,'card'),sort=ls(K.sort,'updated');
var pins=ls(K.pin,[]),hides=ls(K.hide,[]);
var showDesc=ls(K.desc,true),showPath=ls(K.path,true);
function saveState(){lsSet(K.pin,pins);lsSet(K.hide,hides);}
function render(){
var kw=q.value.trim().toLowerCase();
var list=DATA.reports.filter(function(r){return hides.indexOf(r.path)<0;})
 .filter(function(r){return !kw||(r.title+' '+r.path+' '+r.layout).toLowerCase().indexOf(kw)>=0;});
list.sort(function(a,b){
var pa=pins.indexOf(a.path)>=0?1:0,pb=pins.indexOf(b.path)>=0?1:0;
if(pa!==pb)return pb-pa;
if(sort==='title')return a.title.localeCompare(b.title,'zh-Hans-CN');
if(sort==='size')return parseInt(b.sizeKB,10)-parseInt(a.sizeKB,10);
if(sort==='type')return (a.layout+b.title).localeCompare(b.layout+b.title);
return (b.updated||'').localeCompare(a.updated||'')||a.path.localeCompare(b.path);
});
count.textContent=(list.length+hides.length)+' 份 · 显示 '+list.length+(hides.length?' · 隐藏 '+hides.length:'');
if(!list.length){host.innerHTML='<div class="empty">$ grep "'+esc(kw)+'" → 0 reports</div>';renderMgr();return;}
if(view==='card'){
var h='<div class="grid">'+list.map(function(r){
var pin=pins.indexOf(r.path)>=0;
return '<article class="card'+(pin?' pinned':'')+'">'+
'<h3 class="t">'+esc(r.title)+'</h3>'+
'<div class="meta"><span class="badge '+(r.layout==='report'?'r':'c')+'">'+esc(r.layout)+'</span><span>'+esc(r.updated)+'</span><span>'+esc(r.sizeKB)+' KB</span></div>'+
(showDesc&&r.desc?'<div class="desc">'+esc(r.desc)+'</div>':'')+
(showPath?'<div class="path">'+esc(r.path)+'</div>':'')+
'<div class="acts"><a href="'+esc(r.path)+'" target="_blank" rel="noopener noreferrer">↗ 打开</a><button type="button" data-pv="'+esc(r.path)+'">▤ 预览</button><button type="button" data-pin="'+esc(r.path)+'" class="'+(pin?'on':'')+'">'+(pin?'★ 已置顶':'☆ 置顶')+'</button><button type="button" data-hide="'+esc(r.path)+'">— 隐藏</button></div>'+
'</article>';}).join('')+'</div>';
host.innerHTML=h;
}else{
var h2='<div class="list'+(view==='detail'?' detail':'')+'">'+list.map(function(r){
var pin=pins.indexOf(r.path)>=0;
return '<div class="row'+(pin?' pinned':'')+'">'+
'<span class="t">'+esc(r.title)+'</span>'+
'<div class="meta"><span class="badge '+(r.layout==='report'?'r':'c')+'">'+esc(r.layout)+'</span><span>'+esc(r.updated)+'</span><span>'+esc(r.sizeKB)+' KB</span></div>'+
'<div class="acts"><a href="'+esc(r.path)+'" target="_blank" rel="noopener noreferrer">↗ 打开</a><button type="button" data-pv="'+esc(r.path)+'">▤ 预览</button><button type="button" data-pin="'+esc(r.path)+'" class="'+(pin?'on':'')+'">'+(pin?'★':'☆')+'</button><button type="button" data-hide="'+esc(r.path)+'">—</button></div>'+
(r.desc?'<div class="desc">'+esc(r.desc)+'</div>':'')+
'<div class="path">'+esc(r.path)+'</div>'+
'</div>';}).join('')+'</div>';
host.innerHTML=h2;
}
host.querySelectorAll('[data-pv]').forEach(function(b){b.addEventListener('click',function(){
var p=b.getAttribute('data-pv');
var r=DATA.reports.filter(function(x){return x.path===p;})[0]||{title:p,path:p};
document.getElementById('vTitle').textContent=r.title;
document.getElementById('vOpen').href=r.path;
document.getElementById('vFrame').src=r.path;
document.getElementById('viewer').classList.add('open');});});
host.querySelectorAll('[data-pin]').forEach(function(b){b.addEventListener('click',function(){
var p=b.getAttribute('data-pin'),i=pins.indexOf(p);
if(i>=0)pins.splice(i,1);else pins.push(p);
saveState();render();});});
host.querySelectorAll('[data-hide]').forEach(function(b){b.addEventListener('click',function(){
hides.push(b.getAttribute('data-hide'));saveState();render();});});
renderMgr();
}
function renderMgr(){
var el=document.getElementById('mgrList');
if(!hides.length){el.innerHTML='<div style="color:var(--faint);font-size:.88rem">（无隐藏项）</div>';return;}
el.innerHTML=hides.map(function(p){
var r=DATA.reports.filter(function(x){return x.path===p;})[0];
var t=r?r.title:p;
return '<div class="hidden-item"><span>'+esc(t)+'</span><button type="button" data-un="'+esc(p)+'">↺ 恢复</button></div>';
}).join('')+'<div style="margin-top:8px"><button type="button" id="unAll">全部恢复</button></div>';
el.querySelectorAll('[data-un]').forEach(function(b){b.addEventListener('click',function(){
var i=hides.indexOf(b.getAttribute('data-un'));
if(i>=0){hides.splice(i,1);saveState();render();}});});
var ua=el.querySelector('#unAll');
if(ua)ua.addEventListener('click',function(){hides=[];saveState();render();});
}
q.addEventListener('input',render);
document.getElementById('sort').value=sort;
document.getElementById('sort').addEventListener('change',function(){sort=this.value;lsSet(K.sort,sort);render();});
var vb={card:document.getElementById('vCard'),list:document.getElementById('vList'),detail:document.getElementById('vDetail')};
function setView(v){view=v;lsSet(K.view,v);Object.keys(vb).forEach(function(k){vb[k].classList.toggle('on',k===v);});render();}
vb.card.addEventListener('click',function(){setView('card');});
vb.list.addEventListener('click',function(){setView('list');});
vb.detail.addEventListener('click',function(){setView('detail');});
setView(view);
document.getElementById('mgrBtn').addEventListener('click',function(){document.getElementById('mgr').classList.toggle('open');renderMgr();});
// 设置面板（v1.6.2 F25）
var setPop=document.getElementById('setPop'),setBtn=document.getElementById('setBtn');
var sView=document.getElementById('sView'),sSort=document.getElementById('sSort'),sDesc=document.getElementById('sDesc'),sPath=document.getElementById('sPath');
setBtn.addEventListener('click',function(e){e.stopPropagation();var o=setPop.classList.toggle('open');setBtn.setAttribute('aria-expanded',o?'true':'false');});
setPop.addEventListener('click',function(e){e.stopPropagation();});
document.addEventListener('click',function(e){if(setPop.classList.contains('open')&&!e.target.closest('#setPop')&&!e.target.closest('#setBtn')){setPop.classList.remove('open');setBtn.setAttribute('aria-expanded','false');}});
sView.value=view;sSort.value=sort;sDesc.checked=showDesc;sPath.checked=showPath;
sView.addEventListener('change',function(){view=this.value;lsSet(K.view,view);Object.keys(vb).forEach(function(k){vb[k].classList.toggle('on',k===view);});render();});
sSort.addEventListener('change',function(){sort=this.value;lsSet(K.sort,sort);document.getElementById('sort').value=sort;render();});
sDesc.addEventListener('change',function(){showDesc=this.checked;lsSet(K.desc,showDesc);render();});
sPath.addEventListener('change',function(){showPath=this.checked;lsSet(K.path,showPath);render();});
document.getElementById('sReset').addEventListener('click',function(){Object.keys(K).forEach(function(k){try{localStorage.removeItem(K[k]);}catch(e){}});location.reload();});
document.getElementById('vClose').addEventListener('click',function(){
document.getElementById('viewer').classList.remove('open');
document.getElementById('vFrame').src='about:blank';});
document.addEventListener('keydown',function(e){if(e.key==='Escape')document.getElementById('vClose').click();});
document.getElementById('viewer').addEventListener('click',function(e){if(e.target===this)document.getElementById('vClose').click();});
var tb=document.getElementById('themeBtn');
var dk=localStorage.getItem('aos-showcase-theme')==='dark';
function ap(d){document.documentElement.setAttribute('data-theme',d?'dark':'light');tb.setAttribute('aria-pressed',d?'true':'false');}
ap(dk);
tb.addEventListener('click',function(){dk=!dk;ap(dk);localStorage.setItem('aos-showcase-theme',dk?'dark':'light');});
document.getElementById('foot').textContent='索引生成于 '+DATA.generated+' · '+DATA.reports.length+' 份报告（含已隐藏）· build_index.py 扫描生成 · 预览=同窗 iframe，正式阅读请「↗ 打开」';
render();
})();
</script>
</body>
</html>'''


def extract_meta(path):
    rel = os.path.relpath(path, ROOT).replace('\\', '/')
    m = {'title': os.path.basename(path), 'updated': '', 'layout': '?', 'desc': '', 'path': rel}
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read(200000)
        mm = re.search(r'<script type="application/json" id="aos-data">(.*?)</script>', content, re.S)
        if mm:
            d = json.loads(mm.group(1))
            meta = d.get('meta', {}) or {}
            m['title'] = meta.get('title') or m['title']
            m['updated'] = meta.get('updated') or ''
            m['layout'] = meta.get('layout') or ('cardwall' if 'showcase' in rel else 'report')
            m['desc'] = (meta.get('subtitle') or '')[:140]
    except Exception as e:
        m['desc'] = '（meta 解析失败：%s）' % str(e)[:60]
    m['sizeKB'] = str(max(1, round(os.path.getsize(path) / 1024)))
    return m


reports = []
for dirpath, _dirnames, filenames in os.walk(ROOT):
    for fn in filenames:
        if fn == os.path.basename(OUT):
            continue
        if (fn.endswith('_report.html') or fn.endswith('_showcase.html')) and not fn.startswith('.'):
            reports.append(extract_meta(os.path.join(dirpath, fn)))
reports.sort(key=lambda r: (r['updated'], r['path']), reverse=True)
if not reports:
    print('WARN: no reports found under', ROOT)

payload = {
    'generated': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
    'reports': reports,
}
html_out = PAGE.replace('__DATA__', json.dumps(payload, ensure_ascii=False).replace('</script', '<\\/script'))
with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
    f.write(html_out)
print('OK: %s (%d reports)' % (OUT, len(reports)))
for r in reports:
    print('  [%s] %s | %s | %s KB' % (r['layout'], r['updated'], r['title'], r['sizeKB']))
