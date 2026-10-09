MH.nav("reference.html");
const VIEWS={"Indian Ocean \u2014 full current field":[15,130,-60,15],"Agulhas to Madagascar":[15,68,-50,-5],
 "Debris coasts":[25,70,-40,-5],"Southern arc and search":[55,115,-50,-10],"Arc, both arms":[55,115,-50,50],
 "Whole basin with northern arm":[15,130,-60,50],"Takeoff to last radar":[95,112,-2,14]};
const NX=345,NY=225,LA0=-59.875,LO0=15.125,D=1/3;
const dec=b=>{const s=atob(b),u=new Uint8Array(s.length);for(let i=0;i<s.length;i++)u[i]=s.charCodeAt(i);return new Int16Array(u.buffer)};
const toF=a=>{const f=new Float32Array(a.length);for(let i=0;i<a.length;i++)f[i]=a[i]===-32768?NaN:a[i]/1000;return f};

(async()=>{
const [mask,arc,sat,rng,ev,rad,fnd,idx,wj]=await Promise.all(
 ["data/mask.json","data/arc7.json","data/satstate.json","data/rings.json","data/events_canon.json",
  "data/radar.json","data/finds.json","fields/index.json","fields/winds.json"].map(MH.J));

const rr=rad.map(r=>r.null||r).filter(Array.isArray);
const rh=rr[0], rpts=rr.slice(1).map(r=>Object.fromEntries(r.map((v,i)=>[rh[i],v])))
  .filter(r=>r.lat_deg&&String(r.lat_deg).trim()!=="").map(r=>({lat:+r.lat_deg,lon:+r.lon_deg}));

// ---- wind regrid onto the current grid, nearest neighbour
const WLAT=wj.lat,WLON=wj.lon;
function regrid(src){const o=new Float32Array(NX*NY);
 for(let y=0;y<NY;y++){const la=LA0+y*D;let yi=0,bd=1e9;
  for(let i=0;i<WLAT.length;i++){const d=Math.abs(WLAT[i]-la);if(d<bd){bd=d;yi=i}}
  for(let x=0;x<NX;x++){const lo=LO0+x*D;let xi=0,bx=1e9;
   for(let i=0;i<WLON.length;i++){const d=Math.abs(WLON[i]-lo);if(d<bx){bx=d;xi=i}}
   o[y*NX+x]=src[yi][xi]/100}}
 return o}

const cache=new Map(); let cur=null, mi=0, mode="mean";
async function month(i){
 if(cache.has(i))return cache.get(i);
 document.getElementById("st").textContent="loading "+idx[i].full+"…";
 const txt=await (await fetch("fields/"+idx[i].file)).text();
 const a=dec(txt.trim()),n=NX*NY,w=wj.months[i];
 const o={mean:{u:toF(a.subarray(0,n)),v:toF(a.subarray(n,2*n)),wu:regrid(w.um),wv:regrid(w.vm)},
          snap:{u:toF(a.subarray(2*n,3*n)),v:toF(a.subarray(3*n,4*n)),wu:regrid(w.us||w.um),wv:regrid(w.vs||w.vm)}};
 cache.set(i,o);document.getElementById("st").textContent="";
 return o}

const samp=(f,la,lo)=>{const x=Math.round((lo-LO0)/D),y=Math.round((la-LA0)/D);
 if(x<0||x>=NX||y<0||y>=NY)return null;return f[y*NX+x]};

function vecLayer(pick,colVar,gain){return {on:true,draw(x,m){
 if(!cur)return;const f=cur[mode];const step=+document.getElementById("dn").value;
 const[b0,b1,b2,b3]=m.view;const cellPx=m.W/(b1-b0)*D;
 const st=Math.max(1,Math.round(step/cellPx));
 const col=MH.css(colVar);x.strokeStyle=col;x.fillStyle=col;const spacing=st*cellPx;
 for(let y=0;y<NY;y+=st){const la=LA0+y*D;if(la<b2||la>b3)continue;
  for(let i=0;i<NX;i+=st){const lo=LO0+i*D;if(lo<b0||lo>b1)continue;
   const u=pick.u(f)[y*NX+i],v=pick.v(f)[y*NX+i];
   if(!isFinite(u)||!isFinite(v))continue;
   const sp=Math.hypot(u,v);if(sp<0.01)continue;
   const w=Math.min(1,sp/0.6);
   x.globalAlpha=0.3+0.7*w;x.lineWidth=0.8+0.9*w;
   const p=m.pt(lo,la);const L=Math.min(spacing*0.9,sp*gain*spacing/26);
   const ex=p[0]+u/sp*L, ey=p[1]-v/sp*L;
   x.beginPath();x.moveTo(p[0],p[1]);x.lineTo(ex,ey);x.stroke();
   const a=Math.atan2(-(ey-p[1]),ex-p[0]);
   x.beginPath();x.moveTo(ex,ey);
   x.lineTo(ex-3.5*Math.cos(a-0.4),ey+3.5*Math.sin(a-0.4));
   x.lineTo(ex-3.5*Math.cos(a+0.4),ey+3.5*Math.sin(a+0.4));
   x.closePath();x.fill()}}
 x.globalAlpha=1;x.lineWidth=1}}}

const ringLayer=(G)=>({on:true,draw(x,m){const r=Math.PI/180;
 G.rings.forEach((g,i)=>{const last=i===G.rings.length-1;
  x.strokeStyle=MH.css(last?"--c3":"--c1");x.globalAlpha=last?1:.5;
  x.lineWidth=last?2:1.1;x.setLineDash(last?[]:[3,3]);x.beginPath();
  let st=false,pv=null;
  for(let b=0;b<=360;b+=0.5){const d=g.theta*r,p0=g.clat*r,br=b*r;
   const p1=Math.asin(Math.sin(p0)*Math.cos(d)+Math.cos(p0)*Math.sin(d)*Math.cos(br));
   const l1=g.clon*r+Math.atan2(Math.sin(br)*Math.sin(d)*Math.cos(p0),Math.cos(d)-Math.sin(p0)*Math.sin(p1));
   const P=m.pt(l1/r,p1/r);
   if(pv&&Math.abs(P[0]-pv[0])>m.W/2)st=false;
   if(!st){x.moveTo(P[0],P[1]);st=true}else x.lineTo(P[0],P[1]);pv=P}
  x.stroke();
  const d=g.theta*r,p0=g.clat*r,br=(i%2?168:192)*r;
  const p1=Math.asin(Math.sin(p0)*Math.cos(d)+Math.cos(p0)*Math.sin(d)*Math.cos(br));
  const l1=g.clon*r+Math.atan2(Math.sin(br)*Math.sin(d)*Math.cos(p0),Math.cos(d)-Math.sin(p0)*Math.sin(p1));
  const P=m.pt(l1/r,p1/r);
  x.globalAlpha=1;x.fillStyle=MH.css(last?"--c3":"--c1");x.font="11px "+MH.css("--font-mono");
  x.fillText(g.hm,P[0]+4,P[1]-3)});
 x.setLineDash([]);x.globalAlpha=1;x.lineWidth=1}});

const satLayer=(S)=>({on:true,draw(x,m){
 x.strokeStyle=MH.css("--c2");x.lineWidth=2;x.beginPath();
 S.forEach((r,i)=>{const p=m.pt(r.lon,r.lat);i?x.lineTo(p[0],p[1]):x.moveTo(p[0],p[1])});x.stroke();
 S.forEach(r=>{const p=m.pt(r.lon,r.lat);x.fillStyle=MH.css("--c2");x.beginPath();x.arc(p[0],p[1],2.4,0,6.3);x.fill()});
 const p=m.pt(S[0].lon,S[0].lat);x.fillStyle=MH.css("--fg");x.font="11px "+MH.css("--font-mono");
 x.fillText("satellite 16:30–00:20",p[0]+7,p[1]-4);x.lineWidth=1}});

const findLayer=(F)=>({on:true,draw(x,m){for(const s of F.sites){
 const c=m.pt(s.lon,s.lat);
 const e=m.pt(s.lon+100/(111.19*Math.cos(s.lat*Math.PI/180)),s.lat);
 const r=Math.max(2.5,Math.abs(e[0]-c[0]));
 x.strokeStyle=MH.css("--ok");x.globalAlpha=.5;x.setLineDash([3,3]);
 x.beginPath();x.arc(c[0],c[1],r,0,6.3);x.stroke();x.setLineDash([]);
 x.globalAlpha=.9;x.fillStyle=MH.css("--ok");
 x.beginPath();x.arc(c[0],c[1],3+Math.min(3.5,s.items.length*.7),0,6.3);x.fill();x.globalAlpha=1}}});

const map=new MH.Map(document.getElementById("mp"),mask,VIEWS["Indian Ocean \u2014 full current field"]);
map.layers.cur=vecLayer({u:f=>f.u,v:f=>f.v},"--accent",46);
map.layers.wind=vecLayer({u:f=>f.wu,v:f=>f.wv},"--c4",1.6);
map.layers.wind.on=false;
map.layers.search=MH.L.search(MH.SEARCH);
map.layers.rings=ringLayer(rng);
map.layers.arc=MH.L.arc(arc);
map.layers.sat=satLayer(sat);
map.layers.finds=findLayer(fnd);
map.layers.radar=MH.L.radar(rpts);

const names={cur:"Ocean currents",wind:"Surface winds",rings:"Rings 1–7 (derived)",arc:"7th arc (published)",
 sat:"Satellite track",finds:"Debris finds",radar:"Last radar fix",search:"Search areas"};
const tg=document.getElementById("tg");
tg.innerHTML=Object.keys(names).map(k=>`<label><input type="checkbox" data-k="${k}"${map.layers[k].on?" checked":""}> ${names[k]}</label>`).join("");
tg.querySelectorAll("input").forEach(i=>i.onchange=()=>{map.layers[i.dataset.k].on=i.checked;map.draw()});

const mo=document.getElementById("mo");
mo.innerHTML=idx.map((m,i)=>`<option value="${i}">${m.full}</option>`).join("");
async function setMonth(i){mi=i;cur=await month(i);map.draw()}
mo.onchange=()=>setMonth(+mo.value);
document.getElementById("fm").onchange=e=>{mode=e.target.value;map.draw()};
document.getElementById("dn").onchange=()=>map.draw();

document.getElementById("lg").innerHTML=MH.legend([
 [MH.css("--accent"),"ocean current"],[MH.css("--c4"),"wind"],[MH.css("--c3"),"7th arc, published"],
 [MH.css("--c1"),"rings 1–6, derived"],[MH.css("--c2"),"satellite track"],[MH.css("--ok"),"debris finds, 100 km nominal"]]);

const vw=document.getElementById("vw");
vw.innerHTML=Object.keys(VIEWS).map(k=>`<button data-v="${k}">${k}</button>`).join(" ");
vw.querySelectorAll("button").forEach(b=>b.onclick=()=>map.setView(VIEWS[b.dataset.v]));

const AP=MH.arcPts(arc);
map.onhover=h=>{const r=document.getElementById("ro");
 if(!h){r.textContent="Hover anywhere for position, current, wind and distance to the 7th arc.";return}
 const f=MH.findNear(fnd,map,h);
 if(f){r.textContent=MH.findText(f);return}
 let t=`${Math.abs(h.lat).toFixed(2)}°${h.lat<0?"S":"N"}  ${h.lon.toFixed(2)}°E`;
 if(cur){const F=cur[mode];
  const u=samp(F.u,h.lat,h.lon),v=samp(F.v,h.lat,h.lon);
  const wu=samp(F.wu,h.lat,h.lon),wv=samp(F.wv,h.lat,h.lon);
  if(isFinite(u)&&isFinite(v)){const sp=Math.hypot(u,v);
   t+=`   current ${sp.toFixed(3)} m/s toward ${((Math.atan2(u,v)*180/Math.PI+360)%360).toFixed(0)}°`}
  else t+="   current — (land or missing)";
  if(isFinite(wu)&&isFinite(wv)){const ws=Math.hypot(wu,wv);
   t+=`   wind ${ws.toFixed(1)} m/s`}}
 t+=`   ${MH.fmt(MH.arcDist(AP,h.lat,h.lon),0)} km from the 7th arc`;
 r.textContent=t};
matchMedia("(prefers-color-scheme: dark)").addEventListener("change",()=>setTimeout(()=>map.draw(),50));
await setMonth(0);
})();
