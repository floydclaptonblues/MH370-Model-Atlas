
(function(){
  'use strict';
  // Supplied demonstration polyline, ordered north to south. Schematic only;
  // this is not a fresh BTO calculation or the canonical full-resolution arc.
  var arc = [
    [-26.01,101.35],[-32.16,96.26],[-34.46,93.67],
    [-36.97,90.17],[-37.36,89.55],[-39.16,86.25]
  ];
  // Coordinates are retained from the supplied HTML, not from the current
  // terminal catalogue. Original labels are identified as such in the notes.
  var pts = [
    {n:'Northern reference point', la:-32.34, lo:96.29, c:'var(--hot)',
     note:'Labelled “northern cluster centroid” in the supplied demonstration; not a current-catalogue endpoint.'},
    {n:'Southern reference point', la:-37.17, lo:89.86, c:'var(--hot)',
     note:'Labelled “southern cluster centroid” in the supplied demonstration. No search-coverage claim is inferred here.'},
    {n:'C120 reference point', la:-36.92, lo:90.28, c:'var(--cold)',
     note:'The supplied reproduction-control marker, retained to explain how a reference case is shown.'},
    {n:'Illustrative span, southern end', la:-38.82, lo:86.34, c:'var(--undet)',
     note:'One end of the span drawn in the supplied example; the line is not a flight path or confidence boundary.'},
    {n:'Illustrative span, northern end', la:-26.09, lo:101.02, c:'var(--undet)',
     note:'The other end of the same illustrative span. Neither endpoint is ranked as a candidate.'}
  ];

  var W=520,H=440,M={t:26,r:30,b:42,l:52};
  var lo0=84.5, lo1=103.5, la0=-40.2, la1=-24.8;
  var k=Math.cos(-32.5*Math.PI/180);
  function X(lo){return M.l+(lo-lo0)/(lo1-lo0)*(W-M.l-M.r);}
  function Y(la){return M.t+(la1-la)/(la1-la0)*(H-M.t-M.b);}
  var s=[];
  s.push('<rect x="0" y="0" width="'+W+'" height="'+H+'" fill="none"/>');
  for(var lo=86;lo<=102;lo+=4){
    s.push('<line x1="'+X(lo).toFixed(1)+'" y1="'+M.t+'" x2="'+X(lo).toFixed(1)+'" y2="'+(H-M.b)+'" stroke="var(--rule)" stroke-width="1"/>');
    s.push('<text x="'+X(lo).toFixed(1)+'" y="'+(H-M.b+18)+'" fill="var(--ink-3)" font-family="IBM Plex Mono, monospace" font-size="10" text-anchor="middle">'+lo+'°E</text>');
  }
  for(var la=-40;la<=-26;la+=4){
    s.push('<line x1="'+M.l+'" y1="'+Y(la).toFixed(1)+'" x2="'+(W-M.r)+'" y2="'+Y(la).toFixed(1)+'" stroke="var(--rule)" stroke-width="1"/>');
    s.push('<text x="'+(M.l-8)+'" y="'+(Y(la)+3.5).toFixed(1)+'" fill="var(--ink-3)" font-family="IBM Plex Mono, monospace" font-size="10" text-anchor="end">'+Math.abs(la)+'°S</text>');
  }
  var d=arc.map(function(p,i){return (i?'L':'M')+X(p[1]).toFixed(1)+' '+Y(p[0]).toFixed(1);}).join(' ');
  s.push('<path d="'+d+'" fill="none" stroke="var(--arc)" stroke-width="2.5" stroke-linecap="round"/>');
  s.push('<text x="'+(X(100.6)).toFixed(1)+'" y="'+(Y(-27.6)).toFixed(1)+'" fill="var(--arc)" font-family="IBM Plex Mono, monospace" font-size="10.5" text-anchor="end">schematic seventh arc</text>');
  var u0=pts[3], u1=pts[4];
  s.push('<path d="M'+X(u0.lo).toFixed(1)+' '+Y(u0.la).toFixed(1)+' L'+X(u1.lo).toFixed(1)+' '+Y(u1.la).toFixed(1)+'" fill="none" stroke="var(--undet)" stroke-width="7" stroke-dasharray="2 7" stroke-linecap="round" opacity=".55"/>');
  s.push('<text x="'+(X(93.6)).toFixed(1)+'" y="'+(Y(-31.1)).toFixed(1)+'" fill="var(--undet)" font-family="IBM Plex Mono, monospace" font-size="10.5" text-anchor="middle">illustrative span from the supplied example</text>');
  s.push('<text x="'+(X(93.6)).toFixed(1)+'" y="'+(Y(-31.1)+13).toFixed(1)+'" fill="var(--ink-3)" font-family="IBM Plex Mono, monospace" font-size="9.5" text-anchor="middle">markers 4 and 5 are its two ends</text>');
  pts.forEach(function(p,i){
    var x=X(p.lo), y=Y(p.la);
    s.push('<circle cx="'+x.toFixed(1)+'" cy="'+y.toFixed(1)+'" r="7.5" fill="'+p.c+'" stroke="var(--plate)" stroke-width="2"/>');
    var labelX=x+(i===1?-12:12),labelY=y+(i===1?14:4);
    s.push('<text x="'+labelX.toFixed(1)+'" y="'+labelY.toFixed(1)+'" text-anchor="'+(i===1?'end':'start')+'" fill="var(--ink-2)" font-family="IBM Plex Mono, monospace" font-size="10.5">'+(i+1)+'</text>');
  });
  s.push('<text x="'+M.l+'" y="'+(H-10)+'" fill="var(--ink-3)" font-family="IBM Plex Mono, monospace" font-size="9.5">southern Indian Ocean · demonstration figure</text>');
  document.getElementById('map').innerHTML=s.join('');

  document.getElementById('keylist').innerHTML=pts.map(function(p,i){
    return '<div class="key"><span class="dot" aria-hidden="true" style="background:'+p.c+'">'+(i+1)+'</span><div>'
      +'<h3>'+(i+1)+'. '+p.n+'</h3>'
      +'<p class="co">'+Math.abs(p.la).toFixed(2)+'°S, '+p.lo.toFixed(2)+'°E</p>'
      +'<p class="note">'+p.note+'</p></div></div>';
  }).join('');

  var rows=[
    {n:'1,565',t:'admissible histories reaching the late-flight segment',w:17},
    {n:'1,523',t:'of those admit all six flight schedules',w:17},
    {n:'9,138',t:'full minute-by-minute simulations',w:99.5},
    {n:'42',t:'histories recorded as outside the declared speed bounds, kept rather than discarded',w:1},
    {n:'9,180',t:'records in the declared population',w:100}
  ];
  document.getElementById('funnel').innerHTML=rows.map(function(r){
    return '<div class="frow"><div class="flabel"><span class="n">'+r.n+'</span><span class="t">'+r.t+'</span></div>'
      +'<div class="bar"><i style="width:'+r.w+'%"></i></div></div>';
  }).join('');

  var done=2775,total=9180,pc=done/total*100;
  document.getElementById('pct').textContent=pc.toFixed(1)+'%';
  document.getElementById('ptext').textContent=done.toLocaleString()+' of '+total.toLocaleString()+' records verified durable · '+(total-done).toLocaleString()+' remaining';
  document.getElementById('pbar').style.width=pc.toFixed(2)+'%';

  var N=[[200,52,'Mass'],[320,160,'Lift'],[200,268,'Drag'],[80,160,'Fuel flow']];
  var g=[];
  g.push('<circle cx="200" cy="160" r="86" fill="none" stroke="var(--rule)" stroke-width="1" stroke-dasharray="3 5"/>');
  [[200,74,320,146],[320,174,210,258],[190,258,86,174],[80,146,190,74]].forEach(function(a){
    g.push('<path d="M'+a[0]+' '+a[1]+' Q 200 160 '+a[2]+' '+a[3]+'" fill="none" stroke="var(--arc)" stroke-width="1.6" opacity="0"/>');
  });
  var ar=[[200,160,86,-80,-10],[200,160,86,10,80],[200,160,86,100,170],[200,160,86,190,260]];
  ar.forEach(function(a){
    var r=a[2],s0=a[3]*Math.PI/180,s1=a[4]*Math.PI/180;
    var x0=200+r*Math.cos(s0),y0=160+r*Math.sin(s0),x1=200+r*Math.cos(s1),y1=160+r*Math.sin(s1);
    g.push('<path d="M'+x0.toFixed(1)+' '+y0.toFixed(1)+' A '+r+' '+r+' 0 0 1 '+x1.toFixed(1)+' '+y1.toFixed(1)+'" fill="none" stroke="var(--arc)" stroke-width="1.8"/>');
    var th=a[4]*Math.PI/180, tx=200+r*Math.cos(th), ty=160+r*Math.sin(th);
    var nx=-Math.sin(th), ny=Math.cos(th);
    g.push('<path d="M'+(tx+nx*6-Math.cos(th)*5).toFixed(1)+' '+(ty+ny*6-Math.sin(th)*5).toFixed(1)
      +' L'+(tx+Math.cos(th)*3).toFixed(1)+' '+(ty+Math.sin(th)*3).toFixed(1)
      +' L'+(tx-nx*6-Math.cos(th)*5).toFixed(1)+' '+(ty-ny*6-Math.sin(th)*5).toFixed(1)+'" fill="none" stroke="var(--arc)" stroke-width="1.8"/>');
  });
  N.forEach(function(n){
    g.push('<rect x="'+(n[0]-52)+'" y="'+(n[1]-17)+'" width="104" height="34" rx="2" fill="var(--plate)" stroke="var(--ink)" stroke-width="1.4"/>');
    g.push('<text x="'+n[0]+'" y="'+(n[1]+5)+'" fill="var(--ink)" font-family="Archivo, sans-serif" font-weight="700" font-size="13" text-anchor="middle">'+n[2]+'</text>');
  });
  g.push('<text x="200" y="312" fill="var(--ink-3)" font-family="IBM Plex Mono, monospace" font-size="10" text-anchor="middle">solved every minute, not assumed once</text>');
  document.getElementById('loop').innerHTML=g.join('');

  /* ---- satellite geometry diagram (schematic, not to scale) ---- */
  (function(){
    var o=[],CX=250,SY=38,EY=236,R=560;
    o.push('<path d="M'+(CX-215)+' '+EY+' Q '+CX+' '+(EY-40)+' '+(CX+215)+' '+EY+'" fill="none" stroke="var(--arc)" stroke-width="2"/>');
    o.push('<text x="'+(CX-215)+'" y="'+(EY+19)+'" fill="var(--ink-3)" font-family="IBM Plex Mono, monospace" font-size="10">ocean surface</text>');
    o.push('<circle cx="'+CX+'" cy="'+SY+'" r="9" fill="var(--ink)"/>');
    o.push('<path d="M'+(CX-22)+' '+(SY-2)+' L'+(CX-10)+' '+(SY-2)+' M'+(CX+10)+' '+(SY-2)+' L'+(CX+22)+' '+(SY-2)+'" stroke="var(--ink)" stroke-width="3"/>');
    o.push('<text x="'+CX+'" y="'+(SY-20)+'" fill="var(--ink)" font-family="Archivo, sans-serif" font-weight="700" font-size="12" text-anchor="middle">satellite</text>');
    var ax=CX+118, ay=EY-56;
    o.push('<line x1="'+CX+'" y1="'+(SY+10)+'" x2="'+ax+'" y2="'+ay+'" stroke="var(--hot)" stroke-width="2"/>');
    o.push('<text x="'+(CX+72)+'" y="'+(SY+96)+'" fill="var(--hot)" font-family="IBM Plex Mono, monospace" font-size="10.5">slant range from BTO</text>');
    var bx=CX-118;
    o.push('<line x1="'+CX+'" y1="'+(SY+10)+'" x2="'+bx+'" y2="'+ay+'" stroke="var(--hot)" stroke-width="1.2" stroke-dasharray="4 4"/>');
    o.push('<ellipse cx="'+CX+'" cy="'+ay+'" rx="118" ry="17" fill="none" stroke="var(--hot)" stroke-width="1.6" stroke-dasharray="5 4"/>');
    o.push('<text x="'+CX+'" y="'+(ay+34)+'" fill="var(--hot)" font-family="IBM Plex Mono, monospace" font-size="10.5" text-anchor="middle">every point on this ring fits the same BTO</text>');
    o.push('<path d="M'+(ax-11)+' '+ay+' l11 -6 l11 6 l-11 3 z" fill="var(--ink)"/>');
    o.push('<text x="'+(ax+20)+'" y="'+(ay-6)+'" fill="var(--ink)" font-family="Archivo, sans-serif" font-weight="700" font-size="11.5">aircraft</text>');
    var HX=600,HY=140;
    o.push('<line x1="470" y1="30" x2="470" y2="265" stroke="var(--rule)" stroke-width="1"/>');
    o.push('<text x="520" y="44" fill="var(--ink-3)" font-family="IBM Plex Mono, monospace" font-size="10">BFO: same place, different heading</text>');
    o.push('<circle cx="'+HX+'" cy="'+HY+'" r="4.5" fill="var(--ink)"/>');
    [[-38,'var(--cold)','toward: shift up'],[8,'var(--undet)','across: little shift'],[52,'var(--arc)','away: shift down']].forEach(function(a,i){
      var th=a[0]*Math.PI/180, L=86;
      var ex=HX+L*Math.cos(th), ey2=HY+L*Math.sin(th);
      o.push('<line x1="'+HX+'" y1="'+HY+'" x2="'+ex.toFixed(1)+'" y2="'+ey2.toFixed(1)+'" stroke="'+a[1]+'" stroke-width="2"/>');
      var nx=-Math.sin(th),ny=Math.cos(th);
      o.push('<path d="M'+(ex+nx*5-Math.cos(th)*9).toFixed(1)+' '+(ey2+ny*5-Math.sin(th)*9).toFixed(1)
        +' L'+ex.toFixed(1)+' '+ey2.toFixed(1)
        +' L'+(ex-nx*5-Math.cos(th)*9).toFixed(1)+' '+(ey2-ny*5-Math.sin(th)*9).toFixed(1)+'" fill="none" stroke="'+a[1]+'" stroke-width="2"/>');
      o.push('<text x="'+HX+'" y="'+(226+i*17)+'" fill="'+a[1]+'" font-family="IBM Plex Mono, monospace" font-size="9.5" text-anchor="middle">'+a[2]+'</text>');
    });
    o.push('<text x="8" y="292" fill="var(--ink-3)" font-family="IBM Plex Mono, monospace" font-size="9.5">schematic · not to scale</text>');
    document.getElementById('geo').innerHTML=o.join('');
  })();

  /* ---- worked example: demonstration integrator ----
     Inventory and reference constants retained from the supplied HTML.
     Fixed cruise conditions and a simple drag polar; not the project kernel.
     Full steps are 60 s. The last step consumes only the remaining fuel. */
  var NONFUEL=174369.0, FUEL0=27856.86569474842;
  var S=427.8, G=9.80665, RHO=0.3639, SND=296.6, CD0=0.019, KI=0.045,
      TSFC=1.55e-5, CLMAX=0.70, MACH=0.84, DT=60;
  var EPOCH=Date.UTC(2014,2,7,19,41,3);
  var SCALES=[1.0,1.024738];

  function stepOnce(fuel,kflow){
    var m=NONFUEL+fuel;
    var V=MACH*SND;
    var q=0.5*RHO*V*V;
    var cl=m*G/(q*S);
    var cd=CD0+KI*cl*cl;
    var D=cd*q*S;
    var ff=TSFC*D*kflow;
    return {m:m,V:V,q:q,cl:cl,cd:cd,D:D,ff:ff,bm:0.77-cl/CLMAX,burn:ff*DT};
  }
  function runOut(kflow){
    var fuel=FUEL0,t=0;
    while(fuel>0&&t<40000){
      var s=stepOnce(fuel,kflow), dt=Math.min(DT,fuel/s.ff);
      fuel=Math.max(0,fuel-s.ff*dt); t+=dt;
      if(dt<DT) fuel=0;
    }
    return t;
  }
  var EXH=[runOut(SCALES[0]),runOut(SCALES[1])];
  function hhmmss(x){x=Math.round(x);var h=Math.floor(x/3600),m2=Math.floor(x%3600/60),s2=x%60;
    return h+'h '+String(m2).padStart(2,'0')+'m '+String(s2).padStart(2,'0')+'s';}
  document.getElementById('k1out').textContent=hhmmss(EXH[0]);
  document.getElementById('k2out').textContent=hhmmss(EXH[1]);
  document.getElementById('kdiff').textContent=(EXH[0]-EXH[1]).toFixed(0)+' s earlier';

  var fuel,t,hist,timer=null,flashTimers=[];
  var el={m:'v_m',f:'v_f',M:'v_M',h:'v_h',V:'v_V',cl:'v_cl',D:'v_D',ff:'v_ff',bm:'v_bm'};
  function fmt(n,d){return n.toLocaleString(undefined,{minimumFractionDigits:d,maximumFractionDigits:d});}

  function paint(){
    var s=stepOnce(Math.max(fuel,0),SCALES[0]);
    var empty=fuel<=0;
    document.getElementById(el.m).textContent=fmt(NONFUEL+Math.max(fuel,0),0)+' kg';
    document.getElementById(el.f).textContent=fmt(Math.max(fuel,0),0)+' kg';
    document.getElementById(el.M).textContent=MACH.toFixed(2);
    document.getElementById(el.h).textContent='230 hPa ≈ 11.0 km';
    document.getElementById(el.V).textContent=fmt(s.V,1)+' m/s';
    document.getElementById(el.cl).textContent=s.cl.toFixed(4);
    document.getElementById(el.D).textContent=fmt(s.D/1000,2)+' kN';
    document.getElementById(el.ff).textContent=fmt(empty?0:s.ff*3600,0)+' kg/h';
    document.getElementById(el.bm).textContent=(s.bm>=0?'+':'')+s.bm.toFixed(3);
    document.getElementById('o1').textContent=fmt(s.q,0)+' Pa';
    document.getElementById('o2').textContent=s.cl.toFixed(4);
    document.getElementById('o3').textContent=fmt(s.D/1000,2)+' kN';
    document.getElementById('o4').textContent=empty?'0 kg — fuel exhausted':'−'+fmt(Math.min(fuel,s.burn),1)+' kg next step';
    var d=new Date(EPOCH+Math.round(t)*1000);
    document.getElementById('clock').textContent=
      String(d.getUTCHours()).padStart(2,'0')+':'+String(d.getUTCMinutes()).padStart(2,'0')+':'+
      String(d.getUTCSeconds()).padStart(2,'0')+' UTC';
    document.getElementById('elapsed').textContent=empty
      ? 'fuel exhausted at '+hhmmss(t)+' after the reference epoch'
      : hhmmss(t)+' elapsed';
    document.getElementById('run-state').textContent=empty?'EXHAUSTED — calculation stopped':timer?'RUNNING — 1 simulated minute per frame':t>0?'PAUSED — ready to step':'READY — fixed-cruise demonstration';
    document.getElementById('step').disabled=empty;
    document.getElementById('finish').disabled=empty;
    document.getElementById('play').textContent=timer?'Pause':empty?'Replay':'Play';
    document.getElementById('play').setAttribute('aria-pressed',String(!!timer));
    drawTrace();
  }

  function drawTrace(){
    var W2=760,H2=260,P={t:16,r:58,b:50,l:62};
    var tmax=Math.max(EXH[0]*1.04,3600);
    function tx(v){return P.l+v/tmax*(W2-P.l-P.r);}
    function fy(v){return P.t+(1-v/FUEL0)*(H2-P.t-P.b);}
    var ffmax=2.3;
    function gy(v){return P.t+(1-v/ffmax)*(H2-P.t-P.b);}
    var o=[];
    [0,.25,.5,.75,1].forEach(function(fr){
      var y=P.t+fr*(H2-P.t-P.b);
      o.push('<line x1="'+P.l+'" y1="'+y.toFixed(1)+'" x2="'+(W2-P.r)+'" y2="'+y.toFixed(1)+'" stroke="var(--rule)" stroke-width="1"/>');
      o.push('<text x="'+(P.l-8)+'" y="'+(y+3.5).toFixed(1)+'" fill="var(--ink-3)" font-family="IBM Plex Mono, monospace" font-size="9.5" text-anchor="end">'+Math.round((1-fr)*FUEL0/1000)+'t</text>');
      o.push('<text x="'+(W2-P.r+8)+'" y="'+(y+3.5).toFixed(1)+'" fill="var(--ink-3)" font-family="IBM Plex Mono, monospace" font-size="9.5">'+((1-fr)*ffmax).toFixed(1)+'</text>');
    });
    for(var hh=0;hh<=Math.ceil(tmax/3600);hh++){
      var x=tx(hh*3600); if(x>W2-P.r+1) break;
      o.push('<line x1="'+x.toFixed(1)+'" y1="'+P.t+'" x2="'+x.toFixed(1)+'" y2="'+(H2-P.b)+'" stroke="var(--rule)" stroke-width="1"/>');
      o.push('<text x="'+x.toFixed(1)+'" y="'+(H2-P.b+16)+'" fill="var(--ink-3)" font-family="IBM Plex Mono, monospace" font-size="9.5" text-anchor="middle">+'+hh+'h</text>');
    }
    SCALES.forEach(function(kf,i){
      var f=FUEL0,tt=0,pth=[];
      while(f>0&&tt<=tmax){
        pth.push((pth.length?'L':'M')+tx(tt).toFixed(1)+' '+fy(f).toFixed(1));
        var st=stepOnce(f,kf), dt=Math.min(DT,f/st.ff);
        f=Math.max(0,f-st.ff*dt); tt+=dt; if(dt<DT) f=0;
      }
      pth.push('L'+tx(tt).toFixed(1)+' '+fy(0).toFixed(1));
      o.push('<path d="'+pth.join(' ')+'" fill="none" stroke="var(--arc)" stroke-width="'+(i?1.4:2.4)+'"'+(i?' stroke-dasharray="5 4"':'')+'/>');
      o.push('<circle cx="'+tx(EXH[i]).toFixed(1)+'" cy="'+fy(0).toFixed(1)+'" r="4" fill="var(--hot)"/>');
    });
    var f2=FUEL0,t2=0,gp=[];
    while(f2>0&&t2<=tmax){
      var s2=stepOnce(f2,SCALES[0]),dt2=Math.min(DT,f2/s2.ff);
      gp.push((gp.length?'L':'M')+tx(t2).toFixed(1)+' '+gy(s2.ff).toFixed(1));
      f2=Math.max(0,f2-s2.ff*dt2); t2+=dt2;
      if(dt2<DT){f2=0;gp.push('L'+tx(t2).toFixed(1)+' '+gy(s2.ff).toFixed(1));}
    }
    o.push('<path d="'+gp.join(' ')+'" fill="none" stroke="var(--hot)" stroke-width="2" stroke-dasharray="2 3"/>');
    if(hist&&hist.length){
      var last=hist[hist.length-1];
      o.push('<line x1="'+tx(last.t).toFixed(1)+'" y1="'+P.t+'" x2="'+tx(last.t).toFixed(1)+'" y2="'+(H2-P.b)+'" stroke="var(--hot)" stroke-width="1.5"/>');
      o.push('<circle cx="'+tx(last.t).toFixed(1)+'" cy="'+fy(Math.max(last.f,0)).toFixed(1)+'" r="5" fill="var(--hot)" stroke="var(--plate)" stroke-width="2"/>');
    }
    o.push('<text x="'+P.l+'" y="'+(H2-18)+'" fill="var(--arc)" font-family="IBM Plex Mono, monospace" font-size="10">fuel, tonnes (left) · solid k=1.000000; dashed k=1.024738</text>');
    o.push('<text x="'+P.l+'" y="'+(H2-3)+'" fill="var(--hot)" font-family="IBM Plex Mono, monospace" font-size="10">dotted: powered fuel flow, kg/s (right) · vertical cursor: current step</text>');
    document.getElementById('trace').innerHTML=o.join('');
  }

  function clearFlash(){
    flashTimers.forEach(clearTimeout); flashTimers=[];
    ['eq1','eq2','eq3','eq4'].forEach(function(id){document.getElementById(id).classList.remove('lit');});
  }
  function reset(){ stop(); clearFlash(); fuel=FUEL0; t=0; hist=[{t:0,f:FUEL0}]; paint(); }
  function integrateStep(){
    var s=stepOnce(fuel,SCALES[0]),dt=Math.min(DT,fuel/s.ff);
    fuel=Math.max(0,fuel-s.ff*dt); if(dt<DT) fuel=0;
    t+=dt; hist.push({t:t,f:fuel});
  }
  function advance(){
    if(fuel<=0){ stop(); paint(); return; }
    integrateStep();
    clearFlash();
    var ids=['eq1','eq2','eq3','eq4'];
    ids.forEach(function(id,i){ var e=document.getElementById(id);
      flashTimers.push(setTimeout(function(){ e.classList.add('lit'); flashTimers.push(setTimeout(function(){ e.classList.remove('lit'); },170)); }, i*55)); });
    if(fuel<=0) stop();
    paint();
  }
  function stop(){ if(timer){ clearInterval(timer); timer=null; } }
  document.getElementById('play').addEventListener('click',function(){
    if(timer){ stop(); paint(); return; }
    if(fuel<=0) reset();
    timer=setInterval(advance,260);
    paint();
  });
  document.getElementById('step').addEventListener('click',function(){ stop(); advance(); });
  document.getElementById('finish').addEventListener('click',function(){
    stop(); clearFlash(); while(fuel>0&&t<40000) integrateStep(); paint();
  });
  document.getElementById('reset').addEventListener('click',reset);
  document.querySelectorAll('.demo-toolbar a').forEach(function(a){
    a.addEventListener('click',function(){
      var target=document.getElementById(a.hash.slice(1));
      if(target&&target.tagName==='DETAILS') target.open=true;
    });
  });
  document.querySelectorAll('.arc7-tool .scroll,.arc7-tool .chartwrap,.arc7-tool .geowrap,.arc7-tool .mapgrid > div:first-child').forEach(function(panel){
    panel.tabIndex=0;
    panel.setAttribute('role','region');
    var graphic=panel.querySelector('svg');
    panel.setAttribute('aria-label',graphic?graphic.getAttribute('aria-label'):'Scrollable demonstration equation or table');
  });
  reset();
})();
