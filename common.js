const MH={};
MH.J=async u=>(await fetch(u)).json();
MH.css=n=>getComputedStyle(document.documentElement).getPropertyValue(n).trim();
MH.nav=function(cur){const p=[["index.html","Overview"],["satcom.html","Satcom"],["flight.html","Flight models"],["map.html","Combined map"],["drift.html","Drift"],["drift2.html","Drift diagnostics"],["closing.html","Closing report"]];
 document.getElementById("nav").innerHTML=p.map(([h,l])=>`<a href="${h}"${h===cur?' aria-current="page"':''}>${l}</a>`).join("")};
MH.fit=function(c,h){const r=c.getBoundingClientRect(),d=Math.min(2,window.devicePixelRatio||1);c.width=Math.round(r.width*d);c.height=Math.round(h*d);c.style.height=h+"px";const x=c.getContext("2d");x.setTransform(d,0,0,d,0,0);return {x,w:r.width,h}};
MH.fmt=(v,d=0)=>v==null?"–":Number(v).toLocaleString("en",{maximumFractionDigits:d,minimumFractionDigits:d});
MH.hm=m=>{const h=Math.floor(m/60)%24,mi=Math.floor(m%60);return String(h).padStart(2,"0")+":"+String(mi).padStart(2,"0")};
MH.day=m=>m<1440?"7 Mar":"8 Mar";
// distance km
MH.km=(a,b,c,d)=>{const R=6371,r=Math.PI/180,dl=(d-b)*r,p1=a*r,p2=c*r;const h=Math.sin((p2-p1)/2)**2+Math.cos(p1)*Math.cos(p2)*Math.sin(dl/2)**2;return 2*R*Math.asin(Math.sqrt(h))};
// map
MH.Map=class{
 constructor(canvas,mask,view){this.c=canvas;this.mask=mask;this.view=view||[15,130,-60,15];this.layers={};this.h=480;this.hover=null;
  canvas.addEventListener("mousemove",e=>{const r=canvas.getBoundingClientRect();this.hover=this.inv(e.clientX-r.left,e.clientY-r.top);this.onhover&&this.onhover(this.hover)});
  canvas.addEventListener("mouseleave",()=>{this.hover=null;this.onhover&&this.onhover(null)});
  new ResizeObserver(()=>this.draw()).observe(canvas.parentElement)}
 setView(v){this.view=v;this.draw()}
 pt(lon,lat){const[b0,b1,b2,b3]=this.view;return[(lon-b0)/(b1-b0)*this.W,(b3-lat)/(b3-b2)*this.H]}
 inv(x,y){const[b0,b1,b2,b3]=this.view;return{lon:b0+x/this.W*(b1-b0),lat:b3-y/this.H*(b3-b2)}}
 draw(){const[b0,b1,b2,b3]=this.view;const r=this.c.getBoundingClientRect();const asp=(b3-b2)/((b1-b0)*Math.cos(((b2+b3)/2)*Math.PI/180));
  const W=Math.max(300,r.width),H=Math.max(260,Math.min(640,W*asp));const f=MH.fit(this.c,H);const x=f.x;this.W=W;this.H=H;
  x.fillStyle=MH.css("--panel");x.fillRect(0,0,W,H);
  // land
  const m=this.mask,D=m.D;x.fillStyle=MH.css("--land");
  for(let y=0;y<m.NY;y++){const lat=m.LA0+y*D;if(lat<b2-D||lat>b3+D)continue;const row=m.rows[y];let s=-1;
   for(let i=0;i<=m.NX;i++){const L=i<m.NX&&row[i]==="1";if(L&&s<0)s=i;if(!L&&s>=0){const lo0=m.LO0+s*D-D/2,lo1=m.LO0+i*D-D/2;if(lo1>b0&&lo0<b1){const p=this.pt(lo0,lat+D/2),q=this.pt(lo1,lat-D/2);x.fillRect(p[0],p[1],q[0]-p[0]+.6,q[1]-p[1]+.6)}s=-1}}}
  // grid
  x.strokeStyle=MH.css("--grid");x.fillStyle=MH.css("--muted");x.font="11px "+MH.css("--font-mono");x.lineWidth=1;
  const st=(b1-b0)>60?10:5;for(let lo=Math.ceil(b0/st)*st;lo<=b1;lo+=st){const p=this.pt(lo,b3);x.beginPath();x.moveTo(p[0],0);x.lineTo(p[0],H);x.stroke();x.fillText(lo+"°E",p[0]+3,H-4)}
  for(let la=Math.ceil(b2/st)*st;la<=b3;la+=st){const p=this.pt(b0,la);x.beginPath();x.moveTo(0,p[1]);x.lineTo(W,p[1]);x.stroke();x.fillText(Math.abs(la)+"°"+(la<0?"S":"N"),3,p[1]-3)}
  for(const k of Object.keys(this.layers)){const L=this.layers[k];if(L.on)L.draw(x,this)}
  x.strokeStyle=MH.css("--line");x.strokeRect(.5,.5,W-1,H-1)}
};
MH.L={
 arc:(A)=>({on:true,draw(x,m){x.strokeStyle=MH.css("--c3");x.lineWidth=2;x.beginPath();let st=false;for(const[lo,la]of A.lonlat){const p=m.pt(lo,la);if(!st){x.moveTo(p[0],p[1]);st=true}else x.lineTo(p[0],p[1])}x.stroke();x.lineWidth=1}}),
 density:(D,hpd)=>({on:true,hpd:!!hpd,draw(x,m){const h=D.cell_deg/2,mx=Math.max(...D.cells.map(c=>c[2]));const col=MH.css("--accent");x.fillStyle=col;
  for(const[la,lo,ms,hp]of D.cells){const p=m.pt(lo-h,la+h),q=m.pt(lo+h,la-h);x.globalAlpha=Math.min(.95,.12+.85*Math.sqrt(ms/mx));x.fillRect(p[0],p[1],q[0]-p[0]+.5,q[1]-p[1]+.5)}x.globalAlpha=1;
  if(this.hpd){x.strokeStyle=MH.css("--fg");x.lineWidth=.8;for(const[la,lo,ms,hp]of D.cells){if(hp>=1){const p=m.pt(lo-h,la+h),q=m.pt(lo+h,la-h);x.strokeRect(p[0],p[1],q[0]-p[0],q[1]-p[1])}}}
  const pk=D.cells.reduce((a,b)=>b[2]>a[2]?b:a);const p=m.pt(pk[1],pk[0]);x.strokeStyle=MH.css("--fg");x.lineWidth=2;x.beginPath();x.arc(p[0],p[1],7,0,6.3);x.stroke();x.fillStyle=MH.css("--fg");x.font="12px "+MH.css("--font-body");x.fillText("density peak "+Math.abs(pk[0])+"°S "+pk[1]+"°E",p[0]+10,p[1]+4);x.lineWidth=1}}),
 cand:(C)=>({on:true,draw(x,m){for(const c of C){const p=m.pt(c.lon,c.lat);x.beginPath();if(c.prior){x.strokeStyle=MH.css("--bad");x.lineWidth=2;x.moveTo(p[0]-6,p[1]-6);x.lineTo(p[0]+6,p[1]+6);x.moveTo(p[0]+6,p[1]-6);x.lineTo(p[0]-6,p[1]+6);x.stroke();x.lineWidth=1;continue}
   x.fillStyle=c.term==="True"?MH.css("--c1"):MH.css("--muted");x.globalAlpha=.85;x.arc(p[0],p[1],c.stable==="True"?4.5:3,0,6.3);x.fill();x.globalAlpha=1}}}),
 search:(S)=>({on:true,draw(x,m){x.setLineDash([5,3]);x.lineWidth=1.5;S.forEach((b,i)=>{x.strokeStyle=[MH.css("--c4"),MH.css("--c2"),MH.css("--c1")][i%3];const p=m.pt(b.lo0,b.la1),q=m.pt(b.lo1,b.la0);x.strokeRect(p[0],p[1],q[0]-p[0],q[1]-p[1])});x.setLineDash([]);x.lineWidth=1}}),
 radar:(P)=>({on:true,draw(x,m){for(const r of P){const p=m.pt(r.lon,r.lat);x.fillStyle=MH.css("--fg");x.beginPath();x.moveTo(p[0],p[1]-6);x.lineTo(p[0]+6,p[1]+5);x.lineTo(p[0]-6,p[1]+5);x.closePath();x.fill();x.font="12px "+MH.css("--font-body");x.fillText("IGARI last SSR 17:21 UTC",p[0]-60,p[1]-10)}}}),
 pts:(P,col,lab)=>({on:true,draw(x,m){for(const r of P){const p=m.pt(r.lon,r.lat);x.fillStyle=MH.css(col);x.beginPath();x.arc(p[0],p[1],5,0,6.3);x.fill();x.fillStyle=MH.css("--fg");x.font="12px "+MH.css("--font-body");x.fillText(r.l||lab,p[0]+8,p[1]+4)}}})
};
MH.SEARCH=[{n:"ATSB/Fugro 2014–2017",lo0:93,lo1:100,la0:-32,la1:-27},{n:"Ocean Infinity 2018",lo0:95,lo1:100,la0:-31,la1:-28},{n:"Ocean Infinity 2025–26",lo0:95,lo1:97,la0:-33,la1:-31}];
MH.legend=(items)=>items.map(([c,l])=>`<span style="display:inline-flex;align-items:center;gap:5px;margin-right:12px"><i style="width:10px;height:10px;border-radius:50%;background:${c};display:inline-block"></i>${l}</span>`).join("");

MH.arcPts=A=>{const p=[];for(let i=0;i<A.lonlat.length-1;i++){const[x1,y1]=A.lonlat[i],[x2,y2]=A.lonlat[i+1];for(let k=0;k<20;k++){const t=k/20;p.push([y1+(y2-y1)*t,x1+(x2-x1)*t])}}return p};
MH.arcDist=(P,la,lo)=>{let b=1e9;for(const q of P){const d=MH.km(la,lo,q[0],q[1]);if(d<b)b=d}return b};

MH.RING={la0:0.5327,lo0:64.3347,R:44.4701};
MH.L.ring=()=>({on:true,draw(x,m){const r=Math.PI/180,{la0,lo0,R}=MH.RING;x.strokeStyle=MH.css("--c3");x.setLineDash([2,4]);x.lineWidth=1.5;x.beginPath();let st=false;
 for(let b=0;b<=360;b+=0.5){const d=R*r,p0=la0*r,br=b*r;const p1=Math.asin(Math.sin(p0)*Math.cos(d)+Math.cos(p0)*Math.sin(d)*Math.cos(br));const l1=lo0*r+Math.atan2(Math.sin(br)*Math.sin(d)*Math.cos(p0),Math.cos(d)-Math.sin(p0)*Math.sin(p1));const P=m.pt(l1/r,p1/r);if(!st){x.moveTo(P[0],P[1]);st=true}else x.lineTo(P[0],P[1])}
 x.stroke();x.setLineDash([]);x.lineWidth=1}});
MH.L.box=(B,lab)=>({on:true,draw(x,m){const p=m.pt(B.lo0,B.la1),q=m.pt(B.lo1,B.la0);x.strokeStyle=MH.css("--bad");x.lineWidth=2;x.strokeRect(p[0],p[1],q[0]-p[0],q[1]-p[1]);x.fillStyle=MH.css("--fg");x.font="12px "+MH.css("--font-body");x.fillText(lab,p[0]+q[0]-p[0]+6,p[1]+14);x.lineWidth=1}});
MH.BTOBOX={lo0:53.449,lo1:55.793,la0:-44.158,la1:-43.284};

MH.L.finds=(F)=>({on:true,draw(x,m){for(const s of F.sites){const p=m.pt(s.lon,s.lat);x.beginPath();x.fillStyle=MH.css("--ok");x.strokeStyle=MH.css("--panel");x.lineWidth=1.5;const r=4.5+Math.min(4,s.items.length*.8);x.arc(p[0],p[1],r,0,6.3);x.fill();x.stroke();x.lineWidth=1}}});
MH.findNear=(F,m,h)=>{if(!h)return null;let best=null,bd=1e9;for(const s of F.sites){const p=m.pt(s.lon,s.lat),q=m.pt(h.lon,h.lat),d=Math.hypot(p[0]-q[0],p[1]-q[1]);if(d<bd){bd=d;best=s}}return bd<14?best:null};
MH.findText=s=>s?`${s.place} (${s.items.length}): `+s.items.map(i=>`#${i.id} ${i.desc} ${i.found}`).join("; "):"";

MH.L.flights=(A)=>({on:true,draw(x,m){const cols=["--c2","--c1","--c4"];A.forEach((f,i)=>{x.strokeStyle=MH.css(cols[i]);x.lineWidth=1.6;x.beginPath();f.track.forEach((q,j)=>{const p=m.pt(q[2],q[1]);j?x.lineTo(p[0],p[1]):x.moveTo(p[0],p[1])});x.stroke();
 const k=f.track.find(q=>q[0]>=f.cut_s);if(k){const p=m.pt(k[2],k[1]);x.fillStyle=MH.css(cols[i]);x.strokeStyle=MH.css("--fg");x.lineWidth=1;x.beginPath();for(let a=0;a<10;a++){const R=a%2?4:8,t=a*Math.PI/5-Math.PI/2;x.lineTo(p[0]+R*Math.cos(t),p[1]+R*Math.sin(t))}x.closePath();x.fill();x.stroke()}
 const l=f.track[f.track.length-1],p=m.pt(l[2],l[1]);x.strokeStyle=MH.css(cols[i]);x.beginPath();x.moveTo(p[0]-4,p[1]-4);x.lineTo(p[0]+4,p[1]+4);x.moveTo(p[0]+4,p[1]-4);x.lineTo(p[0]-4,p[1]+4);x.stroke();x.lineWidth=1})}});
MH.L.fwd=(F)=>({on:true,draw(x,m){x.lineWidth=1;F.forEach(r=>{const a=m.pt(r.arc_lon,r.arc_lat),b=m.pt(r.end_lon,r.end_lat);x.strokeStyle=MH.css("--muted");x.beginPath();x.moveTo(a[0],a[1]);x.lineTo(b[0],b[1]);x.stroke();x.fillStyle=MH.css("--ok");x.beginPath();x.arc(b[0],b[1],3.5,0,6.3);x.fill();x.fillStyle=MH.css("--fg");x.font="11px "+MH.css("--font-mono");x.fillText(Math.abs(r.arc_lat)+"S",a[0]+4,a[1]-3)})}});

MH.L.peaks=(R)=>({on:true,draw(x,m){const cols={shuffled_regions:"--c1",random_coast:"--c3",observed:"--c2"};for(const k of Object.keys(R)){x.fillStyle=MH.css(cols[k]);x.globalAlpha=.45;for(const q of R[k]){const p=m.pt(q.lon,q.lat);x.beginPath();x.arc(p[0],p[1],5.5,0,6.3);x.fill()}}x.globalAlpha=1;const p=m.pt(55.75,-35.25);x.strokeStyle=MH.css("--fg");x.lineWidth=2;x.beginPath();x.moveTo(p[0]-9,p[1]);x.lineTo(p[0]+9,p[1]);x.moveTo(p[0],p[1]-9);x.lineTo(p[0],p[1]+9);x.stroke();x.lineWidth=1;x.fillStyle=MH.css("--fg");x.font="12px "+MH.css("--font-body");x.fillText("original peak 35.25°S 55.75°E",p[0]+12,p[1]+16)}});

/* Atlas 98: progressive, presentation-only shell. No data or model mutation. */
(() => {
  'use strict';
  if (!document.querySelector('meta[name="viewport"]')) {
    const viewport = document.createElement('meta');
    viewport.name = 'viewport';
    viewport.content = 'width=device-width, initial-scale=1';
    document.head.append(viewport);
  }
  if (!document.documentElement.lang) document.documentElement.lang = 'en';

  // Small original SVG icons, not third-party Windows assets or font downloads.
  const drawings = {
    folder:'<path fill="#806000" d="M2 8h12l3 3h13v19H2z"/><path fill="#ffff80" d="M3 7h10l3 4h13v16H3z"/><path fill="#c0a040" d="M2 14h30l-4 16H2z"/><path fill="#ffe680" d="M3 15h28l-4 13H3z"/><path stroke="#fff" d="M4 16h25"/>',
    monitor:'<path fill="#404040" d="M1 3h30v22H1zM11 25h10v4h6v3H5v-3h6z"/><path fill="#dfdfdf" d="M2 2h28v22H2zM12 24h8v5h6v2H6v-2h6z"/><path fill="#000080" d="M4 5h24v16H4z"/><path fill="#008080" d="M5 6h22v14H5z"/><path stroke="#8fffff" fill="none" d="M6 14h5l3-6 4 10 3-5h5"/><path fill="#008000" d="M25 22h3v1h-3z"/>',
    globe:'<path fill="#000" d="M10 1h12v2h5v5h3v15h-3v5h-5v3H10v-3H5v-5H2V8h3V3h5z"/><path fill="#00a6b6" d="M10 2h12v2h4v5h3v13h-3v5h-5v3H11v-3H6v-5H3V9h3V4h4z"/><path fill="#80d060" d="M9 4h7v3h-3v4H8v3H4v-4h3V6h2zM18 10h7v4h3v7h-4v6h-4v-5h-4v-8h2zM9 18h4v4h3v4h-5v-4H8z"/><path stroke="#b1eeee" fill="none" d="M3 16h26M16 3v27M8 5l-2 10 3 11M23 5l3 10-3 11"/>',
    plane:'<path stroke="#303030" stroke-width="2" fill="#dfdfdf" d="M16 2l3 3v7l11 7v4l-11-3v7l4 2v2l-7-2-7 2v-2l4-2v-7L2 23v-4l11-7V5z"/><path fill="#fff" d="M15 5h2v23h-2z"/><path fill="#008080" d="M14 8h4v4h-4z"/>',
    dish:'<path stroke="#303030" stroke-width="2" fill="#dfdfdf" d="M6 6l18 18C11 29 2 19 6 6zM14 24l-4 6h17l-8-8"/><path stroke="#303030" stroke-width="2" d="M16 16L26 6"/><path fill="#ffd64d" d="M23 3h6v6h-6z"/><path stroke="#000080" stroke-width="2" fill="none" d="M15 3q10 0 14 12M19 2q9 0 12 8"/>',
    waves:'<path fill="#eee" stroke="#555" d="M3 2h20l6 6v23H3z"/><path fill="#c0c0c0" d="M23 2v7h6"/><path stroke="#008080" stroke-width="3" fill="none" d="M5 14q3-5 6 0t6 0t6 0t5 0M5 21q3-5 6 0t6 0t6 0t5 0M5 27q3-5 6 0t6 0t6 0t5 0"/>',
    chart:'<path fill="#eee" stroke="#555" d="M3 2h20l6 6v23H3z"/><path fill="#c0c0c0" d="M23 2v7h6"/><path stroke="#555" fill="none" d="M7 10v17h19"/><path fill="#000080" d="M10 20h3v6h-3z"/><path fill="#008080" d="M15 15h3v11h-3z"/><path fill="#b4570f" d="M20 10h3v16h-3z"/>',
    report:'<path fill="#eee" stroke="#555" d="M3 2h20l6 6v23H3z"/><path fill="#c0c0c0" d="M23 2v7h6"/><path stroke="#000080" stroke-width="2" d="M7 10h13M7 14h17M7 18h17M7 22h17M7 26h10"/>',
    help:'<path fill="#000080" d="M7 2h18v3h4v22h-4v4H7v-4H3V5h4z"/><path stroke="#fff" stroke-width="3" fill="none" d="M10 10V8h3V6h7v3h2v4l-6 4v4"/><path fill="#fff" d="M14 25h4v3h-4z"/>'
  };
  const icon = (name, cls='') => `<svg class="${cls}" viewBox="0 0 32 34" aria-hidden="true" focusable="false" shape-rendering="crispEdges">${drawings[name] || drawings.folder}</svg>`;
  const el = (tag, cls, text) => {
    const node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text !== undefined) node.textContent = text;
    return node;
  };
  function init() {
    const app = document.querySelector('body > .wrap');
    const nav = document.getElementById('nav');
    if (!app || !nav || document.querySelector('.w98-taskbar')) return;
    const pages = [
      ['index.html','Overview','monitor'],['satcom.html','Satcom','dish'],
      ['flight.html','Flight models','plane'],['map.html','Combined map','globe'],
      ['drift.html','Drift','waves'],['drift2.html','Drift diagnostics','chart'],
      ['closing.html','Closing report','report']
    ];
    const selectedLink = nav.querySelector('[aria-current="page"]');
    const name = selectedLink ? selectedLink.getAttribute('href') : (location.pathname.split('/').pop() || 'index.html');
    const current = pages.find(p => p[0] === name) || [name,document.title || 'Atlas','folder'];
    const home = name === 'index.html';
    const heading = app.querySelector('h1');
    if (heading && !heading.id) heading.id = 'atlas-content';
    if (heading) heading.tabIndex = -1;
    nav.setAttribute('aria-label','Atlas sections');
    const skip = el('a','w98-skip','Skip to page content');
    skip.href = '#'+(heading ? heading.id : 'nav');
    document.body.prepend(skip);

    const titlebar = el('header','w98-titlebar');
    titlebar.innerHTML = icon('monitor')+'<span class="w98-titlebar-label">MH370 Model Atlas — '+current[1]+'</span>';
    const controls = el('div','w98-window-buttons');
    const minimize = el('button','','_');
    minimize.type='button';minimize.title='Minimize atlas';minimize.setAttribute('aria-label','Minimize atlas');
    const maximize = el('button','','□');
    maximize.type='button';maximize.title='Maximize atlas';maximize.setAttribute('aria-label','Maximize atlas');maximize.setAttribute('aria-pressed','false');
    const help = el('button','','?');help.type='button';help.title='About this interface';help.setAttribute('aria-label','About this interface');
    controls.append(minimize,maximize,help);titlebar.append(controls);app.prepend(titlebar);

    const about = el('dialog','w98-about');about.setAttribute('aria-labelledby','w98-about-heading');
    about.innerHTML='<div class="w98-titlebar"><span id="w98-about-heading">About MH370 Model Atlas</span></div><div class="w98-about-body"><strong>Atlas 98</strong><p>A Windows 98-inspired interface for the existing MH370 research atlas. The retro interface does not change the model data, results, or qualifications.</p><p>Open a section using the tabs, desktop shortcuts, or Start menu. Minimize and restore with the taskbar. The clock shows the current time in UTC, not flight time.</p><p>This interface is not affiliated with Microsoft.</p><button type="button">OK</button></div>';
    document.body.append(about);
    about.querySelector('button').addEventListener('click',()=>about.close());
    const showAbout=()=>{ if (!about.open) about.showModal(); };
    help.addEventListener('click',showAbout);

    const toolbar=el('div','w98-tools');
    [['index.html','Overview','monitor'],['map.html','Map','globe'],['https://github.com/floydclaptonblues/MH370-Model-Atlas','Source files','folder']].forEach(([href,label,image])=>{
      const a=el('a');a.href=href;a.innerHTML=icon(image)+'<span>'+label+'</span>';toolbar.append(a);
    });
    const aboutButton=el('button');aboutButton.type='button';aboutButton.innerHTML=icon('help')+'<span>About</span>';aboutButton.addEventListener('click',showAbout);toolbar.append(aboutButton);
    const printButton=el('button','w98-print','Print');printButton.type='button';printButton.addEventListener('click',()=>window.print());toolbar.append(printButton);titlebar.after(toolbar);
    const address=el('div','w98-address');address.innerHTML='<span>Address</span><div class="w98-address-path">'+icon('folder')+'<span>Atlas / '+current[1]+'</span><span class="w98-address-end">Research directory</span></div>';toolbar.after(address);

    const desktop=el('aside','w98-desktop');desktop.setAttribute('aria-label','Desktop shortcuts');
    [pages[0],pages[3],pages[1],pages[2],pages[4],pages[6]].forEach(([href,label,image])=>{
      const a=el('a');a.href=href;a.innerHTML=icon(image)+'<span>'+label+'</span>';desktop.append(a);
    });document.body.append(desktop);

    if(home && heading){
      const description=heading.nextElementSibling;
      const hero=el('section','w98-hero');hero.setAttribute('aria-labelledby',heading.id);
      const text=el('div');text.append(el('div','w98-eyebrow','MH370 MODEL ATLAS / RESEARCH DIRECTORY'));
      heading.before(hero);text.append(heading);
      if(description && description.matches('p.sub')) text.append(description);
      hero.append(text);hero.insertAdjacentHTML('beforeend',icon('monitor','w98-hero-art'));
      const grid=app.querySelector(':scope > .grid');
      if(grid){
        grid.classList.add('w98-launch-grid');
        const label=el('div','w98-section-label');label.innerHTML='<b>Explore the atlas</b><span>6 sections · single-click to open</span>';grid.before(label);
        grid.querySelectorAll(':scope > a.card').forEach(a=>{
          const p=pages.find(p=>p[0]===a.getAttribute('href'));
          if(p) a.insertAdjacentHTML('afterbegin',icon(p[2],'w98-launch-icon'));
        });
      }
    }
    // Contain wide tables without hiding text or changing IDs/event handlers.
    app.querySelectorAll('.card > table').forEach(table=>{
      const box=el('div','w98-table-wrap');box.tabIndex=0;box.setAttribute('role','region');
      const h=table.parentElement.querySelector('h2,h3');box.setAttribute('aria-label',(h?h.textContent:'Data table')+' — horizontally scrollable');
      table.before(box);box.append(table);
    });
    const status=el('div','w98-status');status.innerHTML='<span>Document: '+current[1]+'</span><span>Windows 98-inspired presentation</span>';app.append(status);

    const taskbar=el('div','w98-taskbar');taskbar.setAttribute('role','navigation');taskbar.setAttribute('aria-label','Desktop taskbar');
    const start=el('button','w98-start');start.type='button';start.innerHTML=icon('monitor')+'<span>Start</span>';start.setAttribute('aria-expanded','false');start.setAttribute('aria-controls','w98-start-menu');
    const task=el('button','w98-task');task.type='button';task.innerHTML=icon(current[2])+'<span>'+current[1]+'</span>';task.setAttribute('aria-label','Minimize or restore '+current[1]);
    const tray=el('div','w98-tray');tray.innerHTML='<span class="w98-tray-indicator" aria-hidden="true"></span>';const clock=el('time');clock.title='Current time in UTC — not model time';tray.append(clock);
    taskbar.append(start,el('span','w98-task-divider'),task,el('span','w98-theme-note','MH370 Model Atlas'),tray);document.body.append(taskbar);
    const menu=el('div','w98-start-menu');menu.id='w98-start-menu';menu.hidden=true;menu.innerHTML='<div class="w98-start-brand" aria-hidden="true">MH370 Atlas 98</div>';
    const menuLinks=el('div','w98-start-links');menuLinks.setAttribute('aria-label','Start navigation');
    pages.forEach(([href,label,image])=>{const a=el('a');a.href=href;a.innerHTML=icon(image)+'<span>'+label+'</span>';if(href===name)a.setAttribute('aria-current','page');menuLinks.append(a);});
    menuLinks.append(el('hr'));const menuAbout=el('button');menuAbout.type='button';menuAbout.innerHTML=icon('help')+'<span>About this atlas</span>';menuLinks.append(menuAbout);menu.append(menuLinks);document.body.append(menu);
    function setMenu(open,focus=false){menu.hidden=!open;start.setAttribute('aria-expanded',String(open));if(open&&focus)menuLinks.querySelector('a').focus();}
    start.addEventListener('click',()=>setMenu(menu.hidden));
    start.addEventListener('keydown',e=>{if(e.key==='ArrowUp'||e.key==='ArrowDown'){e.preventDefault();setMenu(true,true);}});
    menuAbout.addEventListener('click',()=>{setMenu(false);showAbout();});
    document.addEventListener('pointerdown',e=>{if(!menu.hidden&&!menu.contains(e.target)&&!start.contains(e.target))setMenu(false);});
    document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!menu.hidden){setMenu(false);start.focus();}});
    menu.addEventListener('keydown',e=>{
      const links=[...menuLinks.querySelectorAll('a,button')];const index=links.indexOf(document.activeElement);
      if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();links[(index+(e.key==='ArrowDown'?1:-1)+links.length)%links.length].focus();}
    });
    menu.addEventListener('focusout',()=>setTimeout(()=>{if(!menu.contains(document.activeElement)&&document.activeElement!==start)setMenu(false);},0));
    function toggleMinimized(){const hidden=document.body.classList.toggle('w98-minimized');task.setAttribute('aria-pressed',String(!hidden));if(hidden)task.focus();else{window.dispatchEvent(new Event('resize'));if(heading)heading.focus({preventScroll:true});}}
    minimize.addEventListener('click',toggleMinimized);task.addEventListener('click',toggleMinimized);task.setAttribute('aria-pressed','true');
    maximize.addEventListener('click',()=>{const max=document.body.classList.toggle('w98-maximized');maximize.setAttribute('aria-pressed',String(max));maximize.setAttribute('aria-label',max?'Restore window size':'Maximize atlas');window.dispatchEvent(new Event('resize'));});
    const updateClock=()=>{const now=new Date();clock.dateTime=now.toISOString();clock.textContent=now.toISOString().slice(11,16)+' UTC';};updateClock();setInterval(updateClock,30000);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
