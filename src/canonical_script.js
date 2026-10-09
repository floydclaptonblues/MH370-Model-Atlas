MH.nav("canonical.html");
const VIEWS={"Whole basin":[15,130,-60,50],"Full published arc":[55,115,-50,50],"Northern arm":[60,110,-5,48],"Southern arm and search":[55,115,-50,-10],"Debris coasts":[25,70,-40,-5],"Takeoff to IGARI":[95,112,-2,12]};
(async()=>{
const [mask,arc,sat,ev,rad,fnd,rng]=await Promise.all(["mask","arc7","satstate","events_canon","radar","finds","rings"].map(n=>MH.J("data/"+n+".json")));

// --- radar rows arrive as {"null":[...]} arrays: header then data
const rr=rad.map(r=>r.null||r).filter(Array.isArray);
const rhead=rr[0], rdata=rr.slice(1).map(r=>Object.fromEntries(r.map((v,i)=>[rhead[i],v])));
const rpts=rdata.filter(r=>r.lat_deg&&String(r.lat_deg).trim()!=="").map(r=>({lat:+r.lat_deg,lon:+r.lon_deg,t:r.timestamp_utc,st:r.status}));

// --- layers unique to this page
const satTrack=(S)=>({on:true,draw(x,m){
 x.strokeStyle=MH.css("--c2");x.lineWidth=2;x.beginPath();
 S.forEach((r,i)=>{const p=m.pt(r.lon,r.lat);i?x.lineTo(p[0],p[1]):x.moveTo(p[0],p[1])});x.stroke();
 S.forEach(r=>{const p=m.pt(r.lon,r.lat);x.fillStyle=MH.css("--c2");x.beginPath();x.arc(p[0],p[1],2.6,0,6.3);x.fill()});
 const a=S[0],b=S[S.length-1];
 x.fillStyle=MH.css("--fg");x.font="11px "+MH.css("--font-mono");
 let p=m.pt(a.lon,a.lat);x.fillText(a.t.slice(11)+" UTC",p[0]+7,p[1]);
 p=m.pt(b.lon,b.lat);x.fillText(b.t.slice(11)+" UTC",p[0]+7,p[1]+10);
 x.lineWidth=1}});

const findCircles=(F)=>({on:true,draw(x,m){
 for(const s of F.sites){
  const c=m.pt(s.lon,s.lat);
  // 100 km nominal radius, scaled on the longitude axis at this latitude
  const e=m.pt(s.lon+100/(111.19*Math.cos(s.lat*Math.PI/180)),s.lat);
  const r=Math.max(2.5,Math.abs(e[0]-c[0]));
  x.strokeStyle=MH.css("--ok");x.globalAlpha=.5;x.setLineDash([3,3]);
  x.beginPath();x.arc(c[0],c[1],r,0,6.3);x.stroke();x.setLineDash([]);
  x.globalAlpha=.85;x.fillStyle=MH.css("--ok");
  x.beginPath();x.arc(c[0],c[1],3+Math.min(3.5,s.items.length*.7),0,6.3);x.fill();x.globalAlpha=1}
 }});

const btoRings=(G)=>({on:true,draw(x,m){
 const r=Math.PI/180;
 G.rings.forEach((g,i)=>{
  const last=i===G.rings.length-1;
  x.strokeStyle=MH.css(last?"--c3":"--c1");x.globalAlpha=last?1:.55;
  x.lineWidth=last?2:1.2;x.setLineDash(last?[]:[3,3]);x.beginPath();
  let st=false,pv=null;
  for(let b=0;b<=360;b+=0.5){
   const d=g.theta*r,p0=g.clat*r,br=b*r;
   const p1=Math.asin(Math.sin(p0)*Math.cos(d)+Math.cos(p0)*Math.sin(d)*Math.cos(br));
   const l1=g.clon*r+Math.atan2(Math.sin(br)*Math.sin(d)*Math.cos(p0),Math.cos(d)-Math.sin(p0)*Math.sin(p1));
   const P=m.pt(l1/r,p1/r);
   if(pv&&Math.abs(P[0]-pv[0])>m.W/2){st=false}
   if(!st){x.moveTo(P[0],P[1]);st=true}else x.lineTo(P[0],P[1]);pv=P}
  x.stroke();
  const d=g.theta*r,p0=g.clat*r,br=(i%2?168:192)*r;
  const p1=Math.asin(Math.sin(p0)*Math.cos(d)+Math.cos(p0)*Math.sin(d)*Math.cos(br));
  const l1=g.clon*r+Math.atan2(Math.sin(br)*Math.sin(d)*Math.cos(p0),Math.cos(d)-Math.sin(p0)*Math.sin(p1));
  const P=m.pt(l1/r,p1/r);
  x.globalAlpha=1;x.fillStyle=MH.css(last?"--c3":"--c1");x.font="11px "+MH.css("--font-mono");
  x.fillText(g.hm,P[0]+4,P[1]-3)});
 x.setLineDash([]);x.globalAlpha=1;x.lineWidth=1}});

const map=new MH.Map(document.getElementById("mp"),mask,VIEWS["Full published arc"]);
map.layers.rings=btoRings(rng);
map.layers.search=MH.L.search(MH.SEARCH);
map.layers.arc=MH.L.arc(arc);
map.layers.sat=satTrack(sat);
map.layers.finds=findCircles(fnd);
map.layers.radar=MH.L.radar(rpts);
map.draw();

const names={rings:"All 10 BTO rings (derived)",arc:"7th arc (published, both arms)",sat:"Satellite states 16:30–00:20",finds:"Debris find sites (assumed geocode, 100 km)",radar:"IGARI last SSR 17:21 UTC",search:"Seabed search areas (approximate)"};
const tg=document.getElementById("tg");
tg.innerHTML=Object.keys(names).map(k=>`<label><input type="checkbox" data-k="${k}" checked> ${names[k]}</label>`).join("");
tg.querySelectorAll("input").forEach(i=>i.onchange=()=>{map.layers[i.dataset.k].on=i.checked;map.draw()});

document.getElementById("lg").innerHTML=MH.legend([
 [MH.css("--c3"),"7th arc, as published"],
 [MH.css("--c1"),"the other nine BTO rings, derived"],
 [MH.css("--c2"),"subsatellite track"],
 [MH.css("--ok"),"debris finds, 100 km nominal"],
 [MH.css("--c4"),"search areas, approximate (dashed outlines, one colour each)"]]);

const vw=document.getElementById("vw");
vw.innerHTML=Object.keys(VIEWS).map(k=>`<button data-v="${k}">${k}</button>`).join(" ");
vw.querySelectorAll("button").forEach(b=>b.onclick=()=>map.setView(VIEWS[b.dataset.v]));

map.onhover=h=>{const r=document.getElementById("ro");
 if(!h){r.textContent="Hover for position.";return}
 let t=`${Math.abs(h.lat).toFixed(2)}°${h.lat<0?"S":"N"}  ${h.lon.toFixed(2)}°E`;
 const f=MH.findNear(fnd,map,h);
 if(f)t=MH.findText(f);
 else{const d=MH.arcDist(MH.arcPts(arc),h.lat,h.lon);t+=`   ${MH.fmt(d,0)} km from the published arc`}
 r.textContent=t};
matchMedia("(prefers-color-scheme: dark)").addEventListener("change",()=>setTimeout(()=>map.draw(),50));

// --- canonical observation table
const yn=v=>String(v)==="True"?"yes":"—";
document.getElementById("ev").innerHTML="<tr><th>Time UTC</th><th class=n>BTO µs</th><th class=n>BFO Hz</th><th class=n>BTO used</th><th class=n>BFO used</th><th>Message</th></tr>"+
 ev.slice().sort((a,b)=>a.timestamp_utc.localeCompare(b.timestamp_utc)).map(r=>
 `<tr><td><code>${r.timestamp_utc.slice(8,10)==="08"?"8 Mar ":"7 Mar "}${r.timestamp_utc.slice(11,19)}</code></td>`+
 `<td class=n>${r.canonical_bto_us?MH.fmt(+r.canonical_bto_us):"–"}</td>`+
 `<td class=n>${r.observed_bfo_hz!==""?r.observed_bfo_hz:"–"}</td>`+
 `<td class=n>${yn(r.included_for_bto)}</td><td class=n>${yn(r.included_for_bfo)}</td>`+
 `<td>${r.message_type}</td></tr>`).join("");

// --- debris table, by find date
const items=[];
fnd.sites.forEach(s=>s.items.forEach(i=>items.push({...i,place:s.place,lat:s.lat,lon:s.lon})));
items.sort((a,b)=>String(a.found).localeCompare(String(b.found)));
document.getElementById("fi").innerHTML="<tr><th class=n>#</th><th>Item</th><th class=n>Found</th><th>Region</th><th>Site as geocoded</th></tr>"+
 items.map(i=>`<tr><td class=n>${i.id}</td><td>${i.desc}</td><td class=n><code>${i.found||"–"}</code></td><td>${i.region||"–"}</td><td class="muted">${i.place}</td></tr>`).join("");
})();
