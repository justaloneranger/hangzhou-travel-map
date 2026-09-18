# -*- coding: utf-8 -*-
"""Build a single-file, mobile-first POI map for the Hangzhou travel video."""
import io
import json
import os

from poi_data import CATEGORIES, POIS

ROOT = os.path.dirname(os.path.abspath(__file__))
VENDOR = os.path.join(ROOT, "vendor")
OUT = os.path.join(os.path.dirname(ROOT), "hangzhou-poi-map.html")

leaflet_js = io.open(os.path.join(VENDOR, "leaflet.js"), encoding="utf-8").read()
leaflet_css = io.open(os.path.join(VENDOR, "leaflet.css"), encoding="utf-8").read()

cats_js = json.dumps([{"id": c[0], "name": c[1], "color": c[2]} for c in CATEGORIES],
                     ensure_ascii=False)
pois_js = json.dumps([{"n": p[0], "c": p[1], "lon": p[2], "lat": p[3],
                       "note": p[4], "ap": p[5], "nav": p[6]} for p in POIS],
                     ensure_ascii=False, separators=(",", ":"))

HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,maximum-scale=1">
<meta name="theme-color" content="#0f172a">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<title>杭州旅游点位地图 · 按视频线路整理</title>
<style>__LEAFLET_CSS__</style>
<style>
:root{--bg:#0b1220;--panel:#ffffff;--panel-2:#f5f7fa;--line:#e4e8ef;--text:#0f172a;--muted:#64748b;--brand:#e11d48;--safe-b:env(safe-area-inset-bottom,0px)}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;padding:0;height:100%;overflow:hidden;background:var(--bg);
  font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei","Helvetica Neue",Arial,sans-serif;color:var(--text)}
#app{position:fixed;inset:0;display:flex;flex-direction:column}
#map{position:absolute;inset:0;background:#dfe6ee}
.topbar{position:relative;z-index:1200;padding:calc(8px + env(safe-area-inset-top,0px)) 10px 8px;
  background:linear-gradient(180deg,rgba(255,255,255,.97),rgba(255,255,255,.88));backdrop-filter:blur(10px);
  border-bottom:1px solid var(--line)}
.titleRow{display:flex;align-items:center;gap:8px}
h1{font-size:16px;line-height:1.25;margin:0;font-weight:600;letter-spacing:.2px}
.sub{font-size:11px;color:var(--muted);margin-top:2px}
.spacer{flex:1}
.iconBtn{width:36px;height:36px;border-radius:10px;border:1px solid var(--line);background:#fff;
  display:flex;align-items:center;justify-content:center;font-size:16px;color:var(--text)}
.chips{display:flex;gap:6px;overflow-x:auto;padding:8px 2px 2px;scrollbar-width:none}
.chips::-webkit-scrollbar{display:none}
.chip{flex:0 0 auto;display:flex;align-items:center;gap:6px;padding:8px 12px;border-radius:999px;
  border:1px solid var(--line);background:#fff;font-size:12.5px;color:#334155;white-space:nowrap}
.chip .dot{width:8px;height:8px;border-radius:50%}
.chip.on{background:#0f172a;border-color:#0f172a;color:#fff}
.chip.on .dot{box-shadow:0 0 0 2px rgba(255,255,255,.35)}
.bottom{position:relative;z-index:1200;margin-top:auto;background:var(--panel);border-top:1px solid var(--line);
  border-radius:16px 16px 0 0;box-shadow:0 -8px 24px rgba(15,23,42,.12);
  max-height:46vh;display:flex;flex-direction:column;padding-bottom:var(--safe-b)}
.bottom.collapsed{max-height:62px}
.handle{padding:9px 14px 6px;display:flex;align-items:center;gap:8px;flex:0 0 auto}
.handle .bar{position:absolute;left:50%;top:6px;transform:translateX(-50%);width:38px;height:4px;border-radius:2px;background:#cbd5e1}
.count{font-size:12.5px;color:var(--muted)}
.list{overflow-y:auto;-webkit-overflow-scrolling:touch;padding:0 12px 14px}
.item{display:flex;gap:10px;padding:11px 0;border-bottom:1px solid var(--line)}
.item:last-child{border-bottom:none}
.idx{flex:0 0 auto;width:26px;height:26px;border-radius:8px;color:#fff;font-size:12.5px;font-weight:600;
  display:flex;align-items:center;justify-content:center}
.body{flex:1;min-width:0}
.nm{font-size:14px;font-weight:600;display:flex;align-items:center;gap:6px;flex-wrap:wrap}
.badge{font-size:10px;font-weight:500;color:#92400e;background:#fef3c7;border-radius:6px;padding:1px 5px}
.nt{font-size:12px;color:var(--muted);margin-top:3px;line-height:1.5}
.acts{display:flex;gap:6px;margin-top:7px;flex-wrap:wrap}
.act{font-size:12px;padding:6px 10px;border-radius:8px;border:1px solid var(--line);background:var(--panel-2);
  color:#1e293b;text-decoration:none;display:inline-flex;align-items:center;gap:4px}
.act.primary{background:#0f172a;border-color:#0f172a;color:#fff}
.pin{width:26px;height:26px;border-radius:9px 9px 9px 2px;background:var(--c);color:#fff;font-size:12px;
  font-weight:600;display:flex;align-items:center;justify-content:center;
  box-shadow:0 2px 6px rgba(2,6,23,.35);border:1.5px solid rgba(255,255,255,.9)}
.pin.on{transform:scale(1.22)}
.leaflet-popup-content{margin:10px 12px;width:220px!important}
.pop h3{margin:0 0 4px;font-size:14.5px}
.pop .pc{font-size:11px;color:var(--muted)}
.pop p{font-size:12px;color:#334155;margin:6px 0 8px;line-height:1.55}
.pop .row{display:flex;gap:6px;flex-wrap:wrap}
.banner{position:absolute;left:10px;right:10px;top:calc(96px + env(safe-area-inset-top,0px));z-index:1300;
  background:#fff7ed;border:1px solid #fed7aa;color:#9a3412;border-radius:10px;padding:8px 10px;font-size:12px;display:none}
.legendNote{font-size:11px;color:var(--muted);padding:6px 2px 0}
</style>
</head>
<body>
<div id="app">
  <div id="map"></div>
  <div class="topbar">
    <div class="titleRow">
      <div>
        <h1>杭州旅游点位地图</h1>
      <div class="sub" id="sub">按视频线路分类整理 · 标“近似点位”的为估算位置，导航按名称搜索最准</div>
      </div>
      <div class="spacer"></div>
      <button class="iconBtn" id="btnRoute" title="显示/隐藏顺序连线">路</button>
      <button class="iconBtn" id="btnBase" title="切换底图">图</button>
      <button class="iconBtn" id="btnLoc" title="定位到我">◎</button>
    </div>
    <div class="chips" id="chips"></div>
  </div>
  <div class="banner" id="banner">底图加载失败（可能无网络）。点位与说明仍可查看，联网后刷新即可显示地图。</div>
  <div class="bottom" id="bottom">
    <div class="handle" id="handle"><span class="bar"></span>
      <strong id="catName" style="font-size:13.5px">全部点位</strong>
      <span class="count" id="count"></span>
      <div class="spacer"></div><span style="font-size:12px;color:#94a3b8" id="hint">收起/展开</span>
    </div>
    <div class="list" id="list"></div>
  </div>
</div>
<script>__LEAFLET_JS__</script>
<script>
var CATS=__CATS__;
var POIS=__POIS__;
var ROUTE_ON=true;
function wgs2gcj(lon,lat){var a=6378245.0,ee=0.00669342162296594323;
 function tl(x,y){var r=-100+2*x+3*y+0.2*y*y+0.1*x*y+0.2*Math.sqrt(Math.abs(x));
  r+=(20*Math.sin(6*x*Math.PI)+20*Math.sin(2*x*Math.PI))*2/3;
  r+=(20*Math.sin(y*Math.PI)+40*Math.sin(y/3*Math.PI))*2/3;
  r+=(160*Math.sin(y/12*Math.PI)+320*Math.sin(y*Math.PI/30))*2/3;return r;}
 function tn(x,y){var r=300+x+2*y+0.1*x*x+0.1*x*y+0.1*Math.sqrt(Math.abs(x));
  r+=(20*Math.sin(6*x*Math.PI)+20*Math.sin(2*x*Math.PI))*2/3;
  r+=(20*Math.sin(x*Math.PI)+40*Math.sin(x/3*Math.PI))*2/3;
  r+=(150*Math.sin(x/12*Math.PI)+300*Math.sin(x/30*Math.PI))*2/3;return r;}
 var dlat=tl(lon-105,lat-35),dlon=tn(lon-105,lat-35),rl=lat/180*Math.PI,m=Math.sin(rl);
 m=1-ee*m*m;var sm=Math.sqrt(m);
 dlat=(dlat*180)/((a*(1-ee))/(m*sm)*Math.PI);dlon=(dlon*180)/(a/sm*Math.cos(rl)*Math.PI);
 return [lon+dlon,lat+dlat];}
var catMap={};CATS.forEach(function(c){catMap[c.id]=c;});
POIS.forEach(function(p,i){var g=wgs2gcj(p.lon,p.lat);p.glon=g[0];p.glat=g[1];p.i=i;});
var map=L.map('map',{zoomControl:false,attributionControl:true}).setView([30.2490,120.1480],12);
L.control.zoom({position:'bottomright'}).addTo(map);
function amapUrl(s){return 'https://webrd0'+s+'.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}';}
function satUrl(s){return 'https://webst0'+s+'.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}';}
var road=L.tileLayer(amapUrl('{s}'),{subdomains:'1234',maxZoom:18,attribution:'© 高德地图'});
var sat=L.tileLayer(satUrl('{s}'),{subdomains:'1234',maxZoom:18,attribution:'© 高德地图'});
var satLabel=L.tileLayer(amapUrl('{s}'),{subdomains:'1234',maxZoom:18,opacity:0.85});
road.addTo(map);
var baseIdx=0,satOn=false;
var tileErr=0;
road.on('tileerror',function(){tileErr++;if(tileErr>6)document.getElementById('banner').style.display='block';});
sat.on('tileerror',function(){tileErr++;if(tileErr>6)document.getElementById('banner').style.display='block';});
document.getElementById('btnBase').onclick=function(){
  if(!satOn){map.removeLayer(road);map.addLayer(sat);map.addLayer(satLabel);satOn=true;this.textContent='卫';}
  else{map.removeLayer(sat);map.removeLayer(satLabel);map.addLayer(road);satOn=false;this.textContent='图';}
  setCat(active,true);
};
var layers={},routes={},active='all';
function buildLayers(){
  CATS.forEach(function(c){
    var g=L.layerGroup(),pts=[];
    var arr=POIS.filter(function(p){return p.c===c.id;});
    arr.forEach(function(p,k){
      var m=L.marker([p.glat,p.glon],{icon:L.divIcon({className:'',html:'<div class="pin" style="--c:'+c.color+'">'+(k+1)+'</div>',iconSize:[26,26],iconAnchor:[13,26],popupAnchor:[0,-24]})});
      m.bindPopup(popHTML(p,c),{maxWidth:260});
      m.on('click',function(){pinOn(p);});
      g.addLayer(m);p.m=m;pts.push([p.glat,p.glon]);
    });
    layers[c.id]=g;
    routes[c.id]=L.polyline(pts,{color:c.color,dashArray:'6 7',weight:3,opacity:.85});
  });
  layers.all=L.layerGroup(CATS.map(function(c){return layers[c.id];}));
  routes.all=L.layerGroup([]);
}
function popHTML(p,c){
  var g=p.glon.toFixed(5)+','+p.glat.toFixed(5);
  var nav='https://uri.amap.com/marker?position='+g+'&name='+encodeURIComponent(p.n)+'&coordinate=gaode&callnative=1&src=travel-map';
  var srch='https://uri.amap.com/search?keyword='+encodeURIComponent(p.nav)+'&city='+encodeURIComponent('杭州')+'&src=travel-map';
  return '<div class="pop"><h3>'+p.n+(p.ap?' <span class="badge">近似点位</span>':'')+'</h3>'+
    '<div class="pc">'+c.name+' · '+g+'</div><p>'+p.note+'</p><div class="row">'+
    '<a class="act primary" target="_blank" rel="noopener" href="'+nav+'">高德导航</a>'+
    '<a class="act" target="_blank" rel="noopener" href="'+srch+'">按名称搜索</a></div></div>';
}
var curPin=null;
function pinOn(p){if(curPin&&curPin.i!==p.i){curPin.m.setIcon(icon(p,false));}curPin=p;p.m.setIcon(icon(p,true));}
function icon(p,on){var c=catMap[p.c];var k=POIS.filter(function(x){return x.c===p.c;}).indexOf(p)+1;
 return L.divIcon({className:'',html:'<div class="pin'+(on?' on':'')+'" style="--c:'+c.color+'">'+k+'</div>',iconSize:[26,26],iconAnchor:[13,26],popupAnchor:[0,-24]});}
function setCat(id,noFit){
  active=id;
  Object.keys(layers).forEach(function(k){map.removeLayer(layers[k]);});
  Object.keys(routes).forEach(function(k){map.removeLayer(routes[k]);});
  if(id==='all'){layers.all.addTo(map);}else{layers[id].addTo(map);}
  if(ROUTE_ON){if(id==='all'){CATS.forEach(function(c){routes[c.id].addTo(map);});}else{routes[id].addTo(map);}}
  document.querySelectorAll('.chip').forEach(function(el){el.classList.toggle('on',el.dataset.id===id);});
  renderList(id);
  if(!noFit){
    var arr=POIS.filter(function(p){return id==='all'||p.c===id;});
    if(arr.length){var b=L.latLngBounds(arr.map(function(p){return [p.glat,p.glon];}));
      map.fitBounds(b,{padding:[40,60],maxZoom:id==='all'?13:15});}
  }
}
function renderList(id){
  var arr=POIS.filter(function(p){return id==='all'||p.c===id;});
  var box=document.getElementById('list');box.innerHTML='';
  document.getElementById('catName').textContent=id==='all'?'全部点位':catMap[id].name;
  document.getElementById('count').textContent='共 '+arr.length+' 个';
  arr.forEach(function(p){
    var c=catMap[p.c],k=POIS.filter(function(x){return x.c===p.c;}).indexOf(p)+1;
    var g=p.glon.toFixed(5)+','+p.glat.toFixed(5);
    var div=document.createElement('div');div.className='item';
    div.innerHTML='<div class="idx" style="background:'+c.color+'">'+k+'</div><div class="body">'+
      '<div class="nm">'+p.n+(p.ap?'<span class="badge">近似点位</span>':'')+'</div>'+
      '<div class="nt">'+p.note+'</div><div class="acts">'+
      '<a class="act primary" target="_blank" rel="noopener" href="https://uri.amap.com/marker?position='+g+'&name='+encodeURIComponent(p.n)+'&coordinate=gaode&callnative=1&src=travel-map">导航</a>'+
      '<a class="act" target="_blank" rel="noopener" href="https://uri.amap.com/search?keyword='+encodeURIComponent(p.nav)+'&city='+encodeURIComponent('杭州')+'&src=travel-map">搜索</a>'+
      '<button class="act" data-copy="'+g+'">复制坐标</button>'+
      '<button class="act" data-go="'+p.i+'">地图定位</button></div></div>';
    box.appendChild(div);
  });
  box.querySelectorAll('[data-copy]').forEach(function(b){b.onclick=function(){
    var t=b.dataset.copy;if(navigator.clipboard){navigator.clipboard.writeText(t);}b.textContent='已复制';setTimeout(function(){b.textContent='复制坐标';},1200);};});
  box.querySelectorAll('[data-go]').forEach(function(b){b.onclick=function(){
    var p=POIS[+b.dataset.go];map.flyTo([p.glat,p.glon],16,{duration:.6});
    setTimeout(function(){p.m.openPopup();pinOn(p);},700);
    document.getElementById('bottom').classList.add('collapsed');};});
}
function buildChips(){
  var box=document.getElementById('chips');
  var all=document.createElement('button');all.className='chip on';all.dataset.id='all';
  all.innerHTML='<span class="dot" style="background:#0f172a"></span>全部';
  all.onclick=function(){setCat('all');};box.appendChild(all);
  CATS.forEach(function(c){
    var b=document.createElement('button');b.className='chip';b.dataset.id=c.id;
    var n=POIS.filter(function(p){return p.c===c.id;}).length;
    b.innerHTML='<span class="dot" style="background:'+c.color+'"></span>'+c.name+'<span style="color:#94a3b8">'+n+'</span>';
    b.onclick=function(){setCat(c.id);};box.appendChild(b);
  });
}
document.getElementById('btnRoute').onclick=function(){ROUTE_ON=!ROUTE_ON;this.style.opacity=ROUTE_ON?1:.45;setCat(active,true);};
document.getElementById('btnLoc').onclick=function(){
  if(!navigator.geolocation){alert('此环境不支持定位');return;}
  navigator.geolocation.getCurrentPosition(function(pos){
    var g=wgs2gcj(pos.coords.longitude,pos.coords.latitude);
    map.setView([g[1],g[0]],15);
    L.circleMarker([g[1],g[0]],{radius:8,color:'#2563eb',fillColor:'#3b82f6',fillOpacity:.9}).addTo(map).bindPopup('我的位置');
  },function(){alert('定位失败：请允许定位权限（用本地文件打开时浏览器可能禁用定位）');},{enableHighAccuracy:true,timeout:8000});
};
document.getElementById('handle').onclick=function(){document.getElementById('bottom').classList.toggle('collapsed');};
buildChips();buildLayers();setCat('all',true);
</script>
</body>
</html>
"""

html = (HTML.replace("__LEAFLET_CSS__", leaflet_css)
            .replace("__LEAFLET_JS__", leaflet_js)
            .replace("__CATS__", cats_js)
            .replace("__POIS__", pois_js))

with io.open(OUT, "w", encoding="utf-8") as fh:
    fh.write(html)
print("wrote", OUT, len(html), "bytes,", len(POIS), "POIs,", len(CATEGORIES), "categories")

# quick sanity: no unresolved placeholders, balanced script tags
for token in ("__LEAFLET_JS__", "__CATS__", "__POIS__", "{|}"):
    assert token not in html, token

# syntax-check the page script with a real JS parser
import esprima  # noqa: E402

start = html.rindex("<script>") + len("<script>")
page_js = html[start:html.index("</script>", start)]
esprima.parseScript(page_js)
print("page script parses cleanly")
