const MH={};
MH.J=async u=>(await fetch(u)).json();
MH.css=n=>getComputedStyle(document.documentElement).getPropertyValue(n).trim();
MH.nav=function(cur){const p=[["index.html","Overview"],["methods.html","Methods"],["satcom.html","Satcom"],["flight.html","Flight models"],["map.html","Combined map"],["reference.html","Reference map"],["canonical.html","Canonical map"],["drift.html","Drift"],["drift2.html","Drift diagnostics"],["closing.html","Closing report"]];
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
