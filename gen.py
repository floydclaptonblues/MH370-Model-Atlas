HEAD='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s</title><link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="common.css"><script src="common.js"></script></head><body><div class="wrap"><nav id="nav"></nav>'''
TAIL='</div></body></html>'
pages={}
pages["satcom.html"]=HEAD%"MH370 Satcom"+'''
<h1>Satcom: the Inmarsat burst log <span class="tag frozen">satellite model frozen</span></h1>
<p class="sub">Every point below is a row of <code>satcom_observations.csv</code> (WS-004 canon). Nothing is simulated. Time is UTC, 7–8 March 2014.</p>
<div class="card">
 <div class="ctl" id="rng"></div>
 <div class="read" id="ro1">Hover a plot for values.</div>
 <canvas id="c1"></canvas><canvas id="c2" style="margin-top:8px"></canvas>
 <p class="sub" style="margin-top:8px">Dashed lines mark the 10 usable BTO events from the validated sequence (table below). Raw BTO is shown, not corrected for bias. Within the same minute the log carries more than one BTO level (for example about 9,9xx and 14,9xx µs near 16:41–16:42). I show them as recorded and do not assign a cause.</p>
</div>
<div class="grid">
 <div class="card"><h2>What the log contains</h2><div id="stats"></div></div>
 <div class="card"><h2>Frozen-model facts (from your June restart manifests)</h2>
  <p>BTO status <span class="tag ok">VALIDATED</span> absolute-calibrated, default bias −495,679 µs. Calibration max benchmark residual 59 µs against a 60 µs tolerance. 10 usable BTO events, 12 Table 6 rows, 2 BFO-only rows, 2 excluded log-on rows.</p>
  <p class="muted">Those manifests describe the <b>June 2026 restart</b>, where BFO residuals were blocked. Your later frozen BTO/BFO scorer output (engine v06) is not in the folders I could read, so no scorer residuals or scorer-derived position appear here.</p></div>
</div>
<div class="card"><h2>Canonical event table v1.0 <span class="tag frozen">Average Day package</span></h2><p class="sub">From <code>mh370_satcom_canonical_events_v1_0.csv</code>. 12 canonical observations, 6 restart transients excluded, 1 terminal BFO-only row. Corrections of −4,600 µs are applied to the two log-on requests.</p><div class="scroll" style="max-height:420px"><table id="ce"></table></div></div>
<div class="card"><h2>Published satellite state (Inmarsat Table 4)</h2><p class="sub">11 validated states, 16:30 to 00:20 UTC. Latitude and longitude of the sub-satellite point are computed here from the ECEF position. Perth ground station (ECEF km): −2368.8, 4881.1, −3342.0.</p><div class="scroll"><table id="ss"></table></div>
<p class="sub" style="margin-top:6px">The 00:20 sub-satellite point (0.53°N, 64.46°E) matches the centre of the circle I fitted to your reference arc (0.53°N, 64.33°E), which supports treating the arc as a circle about the satellite.</p></div>
<div class="card"><h2>June diagnostic table</h2><p class="sub">From <code>satcom_events.csv</code> (WS-002 chat export). Residual is observed minus predicted BTO for the diagnostic path family used in June, not a located aircraft. Blank means the file has no value.</p>
 <div class="scroll"><table id="ev"></table></div></div>
<div class="card"><h2>Excluded or unavailable</h2><ul id="gaps"></ul></div>
<script>
MH.nav("satcom.html");
(async()=>{
const [B,E,CE,SS]=await Promise.all([MH.J("data/burst.json"),MH.J("data/events.json"),MH.J("data/events_canon.json"),MH.J("data/satstate.json")]);
const T=B.t;const t0=Date.parse(B.t0);
const evs=E.filter(e=>e.row_kind==="usable_bto_event").map(e=>({id:e.event_id,m:(Date.parse(e.event_utc)-t0)/60000,bto:+e.bto_us,bfo:+e.bfo_hz,res:+e.bto_residual_us}));
const ranges={"Full log":[0,1450],"Last 8 h":[960,1450],"Final hour":[1380,1445],"Takeoff to 16:00":[0,960]};let R=ranges["Full log"];
const rd=document.getElementById("ro1");
const rngEl=document.getElementById("rng");
function mkRng(){rngEl.innerHTML=Object.keys(ranges).map(k=>`<button data-k="${k}" class="${ranges[k]===R?"on":""}">${k}</button>`).join("");rngEl.querySelectorAll("button").forEach(b=>b.onclick=()=>{R=ranges[b.dataset.k];mkRng();draw()})}
function plot(cv,key,label,col,h){const f=MH.fit(cv,h),x=f.x,W=f.w,H=f.h,L=62,Rr=10,Tp=10,Bt=26;
 const idx=[];for(let i=0;i<T.length;i++)if(T[i]>=R[0]&&T[i]<=R[1]&&B[key][i]!=null)idx.push(i);
 if(!idx.length){return}const sv=idx.map(i=>B[key][i]).sort((a,b)=>a-b);let lo=sv[Math.floor(sv.length*.005)],hi=sv[Math.min(sv.length-1,Math.ceil(sv.length*.995))];let clipped=0;if(key==='bto'){clipped=idx.filter(i=>B[key][i]<lo||B[key][i]>hi).length}else{lo=sv[0];hi=sv[sv.length-1]}
 const pad=(hi-lo)*.06||1;lo-=pad;hi+=pad;
 x.fillStyle=MH.css("--panel");x.fillRect(0,0,W,H);
 const X=t=>L+(t-R[0])/(R[1]-R[0])*(W-L-Rr),Y=v=>Tp+(hi-v)/(hi-lo)*(H-Tp-Bt);
 x.font="11px "+MH.css("--font-mono");x.fillStyle=MH.css("--muted");x.strokeStyle=MH.css("--grid");
 for(let k=0;k<=4;k++){const v=lo+(hi-lo)*k/4,y=Y(v);x.beginPath();x.moveTo(L,y);x.lineTo(W-Rr,y);x.stroke();x.textAlign="right";x.fillText(MH.fmt(v),L-6,y+4)}
 const span=R[1]-R[0],step=span>600?120:span>200?60:span>80?15:10;x.textAlign="center";
 for(let t=Math.ceil(R[0]/step)*step;t<=R[1];t+=step){const px=X(t);x.beginPath();x.moveTo(px,Tp);x.lineTo(px,H-Bt);x.stroke();x.fillText(MH.hm(t),px,H-Bt+14)}
 x.textAlign="left";x.fillText(label+(clipped?`  (${clipped} outlier rows beyond the 0.5–99.5% range not drawn)`:""),L+4,Tp+11);
 x.fillStyle=col;idx.forEach(i=>{if(B[key][i]<lo||B[key][i]>hi)return;x.fillRect(X(T[i])-1,Y(B[key][i])-1,2.4,2.4)});
 x.strokeStyle=MH.css("--accent");x.setLineDash([4,3]);evs.forEach(e=>{if(e.m>=R[0]&&e.m<=R[1]){const px=X(e.m);x.beginPath();x.moveTo(px,Tp);x.lineTo(px,H-Bt);x.stroke()}});x.setLineDash([]);
 cv._m={X,Y,idx,key,L,Rr,W,R:[...R]};cv.onmousemove=ev=>{const r=cv.getBoundingClientRect(),px=ev.clientX-r.left;const t=R[0]+(px-L)/(W-L-Rr)*(R[1]-R[0]);let best=-1,bd=1e9;for(const i of idx){const d=Math.abs(T[i]-t);if(d<bd){bd=d;best=i}}
  if(best>=0&&bd<(R[1]-R[0])/40){const tt=T[best];rd.textContent=`${MH.day(tt)} ${MH.hm(tt)}:${String(Math.round((tt%1)*60)).padStart(2,"0")} UTC   BTO ${MH.fmt(B.bto[best])} µs   BFO ${MH.fmt(B.bfo[best])} Hz   (σ ${B.sig_bto} µs, ${B.sig_bfo} Hz as listed)`}}}
function draw(){plot(document.getElementById("c1"),"bto","BTO (µs)",MH.css("--c1"),230);plot(document.getElementById("c2"),"bfo","BFO (Hz)",MH.css("--c2"),230)}
mkRng();draw();new ResizeObserver(draw).observe(document.querySelector(".card"));matchMedia("(prefers-color-scheme: dark)").addEventListener("change",()=>setTimeout(draw,50));
// stats
const nb=B.bto.filter(v=>v==null).length;const lastg=T[T.length-1];
document.getElementById("stats").innerHTML=`<table><tr><td>Rows</td><td class="n">${MH.fmt(T.length)}</td></tr><tr><td>First / last row</td><td class="n">7 Mar ${MH.hm(T[0])} / 8 Mar ${MH.hm(lastg)}</td></tr><tr><td>Rows with no BTO value</td><td class="n">${nb}</td></tr><tr><td>Listed σ BTO / BFO</td><td class="n">${B.sig_bto} µs / ${B.sig_bfo} Hz</td></tr></table><p class="sub" style="margin-top:6px">The log includes the ground and takeoff period (from 00:51 UTC on 7 March) as well as the flight.</p>`;
// event table
document.getElementById("ce").innerHTML="<tr><th>Event</th><th>UTC</th><th>Message type</th><th>Channel</th><th class=n>BFO Hz</th><th class=n>Raw BTO µs</th><th class=n>Corr.</th><th class=n>Canon. BTO µs</th><th>BTO</th><th>BFO</th><th>Class / note</th></tr>"+CE.map(e=>`<tr><td>${e.event_id}</td><td>${e.timestamp_utc.slice(5,19).replace("T"," ")}</td><td>${e.message_type}</td><td>${e.channel}</td><td class=n>${e.observed_bfo_hz}</td><td class=n>${e.raw_bto_us||"–"}</td><td class=n>${e.bto_correction_us||"–"}</td><td class=n>${e.canonical_bto_us||"–"}</td><td>${e.included_for_bto==="True"?"used":"no"}</td><td>${e.included_for_bfo==="True"?"used":"no"}</td><td>${e.classification.replace(/_/g," ")}${e.note?": "+e.note:""}</td></tr>`).join("");
document.getElementById("ss").innerHTML="<tr><th>UTC</th><th class=n>x km</th><th class=n>y km</th><th class=n>z km</th><th class=n>vz km/s</th><th class=n>Sub-sat lat</th><th class=n>Sub-sat lon</th></tr>"+SS.map(s=>`<tr><td>${s.t}</td><td class=n>${s.x}</td><td class=n>${s.y}</td><td class=n>${s.z}</td><td class=n>${s.vz}</td><td class=n>${s.lat.toFixed(2)}</td><td class=n>${s.lon.toFixed(2)}</td></tr>`).join("");
const rows=E;let h="<tr><th>Event</th><th>Time (UTC)</th><th>Kind</th><th class=n>BTO µs</th><th class=n>BFO Hz</th><th class=n>BTO residual µs</th><th>Gate</th></tr>";
rows.forEach(e=>{h+=`<tr><td>${e.event_id||"–"}</td><td>${(e.event_utc||"").slice(5,19).replace("T"," ")||e.event_time_utc_unqualified||"–"}</td><td>${e.row_kind.replace(/_/g," ")}</td><td class=n>${e.bto_us||"–"}</td><td class=n>${e.bfo_hz||"–"}</td><td class=n>${e.bto_residual_us?MH.fmt(+e.bto_residual_us,1):"–"}</td><td>${e.bto_gate_passed==="true"?"pass ≤600":e.bto_gate_passed||"–"}</td></tr>`});
document.getElementById("ev").innerHTML=h;
document.getElementById("gaps").innerHTML=E.filter(e=>e.exclusion_reason).map(e=>`<li><b>${e.event_id||e.event_time_utc_unqualified||"row"}</b> (${e.row_kind.replace(/_/g," ")}): ${e.exclusion_reason}</li>`).join("")+"<li>Full UTC dates for the two excluded log-on rows are not stored in the manifest, only time of day.</li><li>The satellite ephemeris file in the WS-004 canon has zero satellite velocity and a fixed position for all rows, so I did not use it. The validated Table 4 states above come from the Average Day package.</li>";
})();
</script>'''+TAIL

VIEWS='''const VIEWS={"Average Day tracks":[84,100,-40,2],"Terminal area":[86,93,-39,-35],"Whole basin":[15,130,-60,15],"Search area":[80,112,-42,-20],"Western drift focus":[35,80,-52,-20],"Southern Africa to Réunion":[25,70,-40,-5]};'''
pages["flight.html"]=HEAD%"MH370 Flight Models"+'''
<h1>Flight models <span class="tag frozen">Average Day frozen</span> <span class="tag prov">Phase 5A provisional</span></h1>
<p class="sub">What exists in your archive for the path and endpoint side, with its status. I did not run or rank anything here.</p>
<div class="note bad"><b>Not a located aircraft.</b> No source below produces a final coordinate. The candidate points are not all on the reference 7th arc: measured here, they sit 65 to 1,306 km from it (median about 610 km). I have not investigated why. The reference arc is drawn at 40,000 ft.</div>

<div class="card"><h2>Average Day model <span class="tag frozen">frozen, packaged 3 Oct 2026</span></h2>
 <p>Flies one commanded flight from the 19:41:03 arc-1 start through ERA5 weather with a Boeing 777-200 performance model, scores it against 4 BTO and 5 BFO residuals to 00:11 UTC, and tracks fuel. I ran its <code>verify.py</code> here: all three stored reference flights reproduce (chi² within 1e-11, 00:11 positions and fuel exact). Tracks below are those flights re-flown at dt 7.5 s.</p>
 <div class="ctl" id="adv"></div><div class="read" id="adro">Stars mark the 00:11 position, × the end of the modelled track at 00:17.</div>
 <canvas id="mp2"></canvas>
 <div class="scroll" style="margin-top:8px"><table id="adt"></table></div>
 <div class="note" style="margin-top:8px">All outputs are diagnostic and conditional on the commanded-flight model. The score stops at 00:11, so the 00:19 data are not scored. Chi² contours are not confidence regions. Nothing here is an endpoint, crash coordinate or search area.</div></div>
<div class="grid">
 <figure class="card" style="margin:0"><h2>Reach vs fuel-matched speed</h2><img src="img/fuel_reach.png" alt="Left: speed needed to reach the 7th arc against arc latitude, with the speed that flames out at 00:17 and the normal cruise band. Right: altitude that burns fuel out at 00:17 against true airspeed." style="width:100%;height:auto;border-radius:6px"><p class="sub" style="margin-top:6px">Your figure. The black line is the speed needed to reach the arc on a direct path. Red points are the speeds at which fuel runs out at 00:17 with altitude solved.</p></figure>
 <figure class="card" style="margin:0"><h2>Terminal points vs surveyed seabed</h2><img src="img/terminal_vs_coverage.png" alt="Diagnostic terminal points for five scenarios plotted with Fugro deep tow, Fugro AUV and Dong Hai Jiu 101 coverage and the sea-level 7th arc." style="width:100%;height:auto;border-radius:6px"><p class="sub" style="margin-top:6px">Your figure. Coverage is where sonar data exist, not a detection measure. Contact points are conditional kinematic scenarios, not crash coordinates.</p></figure>
</div>
<div class="card"><h2>Known limits (package README)</h2><ul><li>Score stops at 00:11 UTC; nothing after is modelled beyond fuel.</li><li>SDU pre-compensation keeps zero vertical speed (K-mode open).</li><li>ERA5 is clamped east of 102.4°E; temperatures above 300 hPa are held at their 300 hPa values.</li><li>One-engine fuel burn may be too generous at altitude (about FL370 at M0.60 against FL290 in the ATSB figure).</li><li>Fuel is one tank feeding both engines.</li></ul></div>
<div class="grid">
 <div class="card"><h2>High-Fidelity Average Day Solver: nominal startup and route-box diagnostics <span class="tag prov">TASK_021, conditional</span></h2>
<p class="sub">Replays of the saved flights with the force model, nine-term score (4 BTO, 5 BFO), fuel profile and k bounds fixed. Both solves start from the P038_C commands. The score stops at 00:11.</p>
<div class="scroll"><table><tr><th>Case</th><th class="n">&chi;&sup2;</th><th class="n">&Delta;&chi;&sup2; vs U</th><th class="n">k</th><th class="n">Loss time</th><th class="n">Gap to log-on</th><th>Position at 00:11</th><th class="n">Fuel at 00:11</th><th>Status</th></tr>
<tr><td>P038_U (reference)</td><td class="n">7.4948</td><td class="n">&ndash;</td><td class="n">1.02689</td><td class="n">00:14:08</td><td class="n">320.7 s</td><td>&minus;36.526, 89.353</td><td class="n">301.9 kg</td><td>reference</td></tr>
<tr><td>P038_C</td><td class="n">7.9141</td><td class="n">+0.419</td><td class="n">&ndash;</td><td class="n">00:16:29</td><td class="n">179.9 s</td><td>&minus;35.901, 90.327</td><td class="n">516.6 kg</td><td>guard False</td></tr>
<tr><td><b>C120</b></td><td class="n">8.1171</td><td class="n">+0.622</td><td class="n">1.024738</td><td class="n">00:17:14</td><td class="n">134.9 s</td><td>&minus;35.848, 90.393</td><td class="n">585.0 kg</td><td>passed guard, stationarity, verification</td></tr>
<tr><td>C-box</td><td class="n">7.7633</td><td class="n">+0.269</td><td class="n">1.024738</td><td class="n">&ndash;</td><td class="n">179.9 s</td><td>&minus;36.161, 89.917</td><td class="n">517.6 kg</td><td>solve failed (stalled); flight verified</td></tr></table></div>
<ul>
<li><b>C120</b> costs +0.62 in &chi;&sup2; against the unconstrained solve, so within this diagnostic it does not depend on a slow startup. It is 8.3 km from P038_C and 119.9 km from P038_U.</li>
<li><b>It is constrained, not a free optimum.</b> Nine constraints are active, including k at its lower bound, start latitude at its 0.5&deg; limit and a fuel allowance margin of about 0.1 kg.</li>
<li><b>C-box</b> did not converge (15 accepted iterations). It moved 46.9 km from P038_C, which triggers the box-shaping rule. It cannot separate the bound widening from extra optimisation of a reference that was not stationary.</li></ul>
<h3>C120 cruise profile</h3>
<div class="scroll"><table><tr><th>Time UTC</th><th>Lat, lon</th><th class="n">Ground speed</th><th class="n">Track</th><th class="n">Height</th></tr>
<tr><td>19:41:03</td><td>0.500, 93.754</td><td class="n">251.3 m/s (489 kt)</td><td class="n">184.6&deg;</td><td class="n">11,957 m (39,227 ft)</td></tr>
<tr><td>20:41:05</td><td>&minus;7.719, 93.092</td><td class="n">253.5 m/s</td><td class="n">184.7&deg;</td><td class="n">11,949 m</td></tr>
<tr><td>21:41:27</td><td>&minus;15.967, 92.401</td><td class="n">254.2 m/s</td><td class="n">184.8&deg;</td><td class="n">11,969 m</td></tr>
<tr><td>22:41:22</td><td>&minus;24.097, 91.660</td><td class="n">250.7 m/s</td><td class="n">185.1&deg;</td><td class="n">11,959 m</td></tr>
<tr><td>00:11:00</td><td>&minus;35.848, 90.393</td><td class="n">237.7 m/s (462 kt)</td><td class="n">185.7&deg;</td><td class="n">11,736 m (38,502 ft)</td></tr></table></div>
<p class="sub" style="margin-top:6px">Mach 0.8406 at the start falling to 0.8306 at 00:11; pressure constant at 214.2 hPa; temperature 223.5 K to 219.2 K; no turn above 1&deg;/min; path length 4,179 km (2,190 nm) from 19:41 to 00:11. C-box is similar (Mach 0.8420 to 0.8320, track 185.2&deg; to 186.5&deg;, path 4,183 km).</p>
<img src="img/c120_profile.png" alt="Mach, ground speed and height against time for C120 and C-box, with 00:11, engine loss and log-on marked" style="width:100%;height:auto;border-radius:6px">
<div class="note" style="margin-top:8px"><b>Limits.</b> These are finite conditional diagnostics, not global minima. Incoming-route and systems closure are unproved. The BFO uses a zero-vertical-speed convention (K-mode open). k is not adopted anywhere else. The 00:11 positions are conditional model states, not endpoints. The geometry file runs to 00:19:37, but after engine loss it only continues the same state (Mach 0.8306, track about 185.8&deg;, height falling 6 m). That is not a descent, glide or terminal path. The terminal phase is TASK_022 and has not been run.</div></div>
<div class="card"><h2>TASK_022: terminal continuations of C120 <span class="tag prov">bounded experiment, conditional</span></h2>
<p class="sub">582 searched histories from C120&rsquo;s own engine-loss state, six matched strata (E+ and E&minus; at &Delta;CD 0, 0.005, 0.015), eight shared seeds. C120 itself was frozen: no parent, fuel, k or engine-loss change. Fitting stops at 00:19:37; the continuation to the surface is then held fixed, not fitted to any location.</p>
<h3>The central result</h3>
<p>Twelve histories reproduce the final frequency pair. <b>Every one of them reaches the water supersonic, far outside the airframe envelope, inside the aerodynamic proxy the model flags as unsupported.</b> The two controls that stay inside the supported aerodynamic domain and arrive at survivable speed miss the 00:19:37 BFO by more than 100 Hz.</p>
<div class="scroll"><table>
<tr><th>Group</th><th>Final BFO pair</th><th class="n">Mach at surface</th><th class="n">EAS at surface</th><th class="n">Descent rate</th><th>Aerodynamic domain</th></tr>
<tr><td>12 fitted, held law</td><td>compatible</td><td class="n">1.06 &ndash; 1.33</td><td class="n">704 &ndash; 885 kt</td><td class="n">36,700 &ndash; 78,000 ft/min</td><td>parabolic proxy (unsupported)</td></tr>
<tr><td>R0, G0 controls</td><td>fail by 28&ndash;48&sigma;</td><td class="n">0.31 &ndash; 0.38</td><td class="n">198 &ndash; 252 kt</td><td class="n">1,100 &ndash; 1,500 ft/min</td><td>clean surrogate (supported)</td></tr>
<tr><td>2 bank-release comparisons</td><td>compatible to release</td><td class="n">0.34, 0.55</td><td class="n">225, 364 kt</td><td class="n">1,700, 4,900 ft/min</td><td>parabolic proxy</td></tr></table></div>
<p class="sub" style="margin-top:6px">A 777&rsquo;s Vmo is 330 kt and Mmo 0.87. The fitted contacts arrive at 2.1 to 2.7 times Vmo, banked 76&deg; to 89&deg;. Impact states read from each saved contact trajectory.</p>
<img src="img/t22_descent.png" alt="Left: height against time for all 16 tested continuations, showing 12 near-vertical dives, two long control glides and two bank-release cases. Right: equivalent airspeed against height, with the fitted histories crossing far beyond Vmo." style="width:100%;height:auto;border-radius:6px">
<div class="note bad" style="margin-top:8px"><b>These contact points are not candidate locations.</b> They are the endpoints of intact-body trajectories at speeds where an intact body is not physical. An aircraft in that descent would break up well above the water, and debris would not reach those coordinates. The clustering of the twelve within about 13 km is a property of holding one control law, not evidence of a located point.</div>
<h3>What the signals actually say</h3>
<ul>
<li><b>The BTO is not a miss.</b> The reported residuals of &minus;24.98 to &minus;26.69 &micro;s are 0.86 to 0.92&sigma; against this project&rsquo;s own listed &sigma;<sub>BTO</sub> of 29.0 &micro;s. All twelve sit inside one standard deviation. The 1 &micro;s target in the brief was about 0.03&sigma;, roughly thirty times tighter than the measurement, and was declared as a numerical search target rather than an acceptance rule.</li>
<li><b>The BTO is inherited, not fitted.</b> Across six strata, both bank signs, three drag values and 582 histories, the residual spans 1.71 &micro;s, about 256 m of range. It is set by the frozen C120 state at 00:11 and the terminal law cannot move it, so the 00:19:29 timing gives no discrimination among terminal laws here. Nothing was drawn toward the arc: the model sits a consistent 3.7 km of range away from it.</li>
<li><b>One case is clean.</b> S03 (E&minus;, &Delta;CD 0) needs no warm-up offset at all: BFO29 0.85&sigma;, BFO37 &minus;1.72&sigma;, BTO29 &minus;0.90&sigma;, all within 2&sigma;. The other nine warm-up cases rely on a shared offset anywhere in 17 to 136 Hz, permissive enough to absorb raw residuals of 10 to 67 Hz. S07 and S11 also need no offset but sit at 2.35&sigma; and 5.75&sigma; on BFO29.</li>
</ul>
<h3>G0 control: contact resolved</h3>
<p class="sub">G0 was horizon-limited at 00:45 in the original run. A follow-up addendum continued the same state with unchanged physics and no refitting. It reaches the surface at <b>00:47:16 UTC, 38.7059&deg;S 90.4148&deg;E</b>, 1,802 s after engine loss, after 230.3 km of ground path from 11.72 km &mdash; a glide ratio near 19.6:1, realistic for a clean 777. It arrives at 198 kt EAS and 1,091 ft/min. The two finest meshes agree to 0.02 m and 7 &micro;s against targets of 100 m and 1 s. Its frequency mismatch is unchanged: it remains a control, not a candidate.</p>
<h3>Spread across tested assumptions</h3>
<div class="scroll"><table><tr><th>Outcome</th><th class="n">Signed distance to the arc ring (my fit)</th></tr>
<tr><td>12 fitted contacts, held law</td><td class="n">+1.4 to &minus;6.6 km</td></tr>
<tr><td>Bank-release comparisons</td><td class="n">&minus;41 and &minus;46 km</td></tr>
<tr><td>R0 control</td><td class="n">&minus;141 km</td></tr>
<tr><td>G0 control</td><td class="n">&minus;167 km</td></tr></table></div>
<p class="sub" style="margin-top:6px">Positive is inside the ring. G0&rsquo;s contact lies about 199 km from the fitted cluster, so the spread across tested assumptions is of order 200 km, not the 13 km seen within the held-law group. Distances use my circle fit to the reference arc, which is a 40,000 ft reference compared here against sea-level contacts; they indicate position, not a BTO residual.</p>
<div class="note" style="margin-top:8px"><b>What this does and does not establish.</b> The narrow result is that these twelve selected imposed-force histories matched the adopted frequency envelopes, and that these two specific controls did not. That is not a theorem about descents and glides in general, and the earlier wording on this page overstated it. The E&plusmn; laws are imposed diagnostic force histories, not reconstructed attitudes, pilot action or a natural upset. Systems support stays conditional: continuous feed is assumed, and antenna orientation and hydraulic authority are unresolved. No endpoint, crash coordinate, debris origin or search area follows from any of this.</div></div>

<div class="card"><h2>TASK_026: how much rests on the BFO convention <span class="tag ok">complete, 6 Oct</span></h2>
<p class="sub">The compensation convention was swept with a diagnostic coordinate &kappa;, the fraction of the aircraft&rsquo;s vertical Doppler removed by the SDU pre-compensation. &kappa;&nbsp;=&nbsp;0 is the convention in use; &kappa;&nbsp;=&nbsp;1 makes the BFO insensitive to vertical speed. The sixteen frozen message states were re-scored across the range; no trajectory was re-integrated and no &kappa; was fitted or preferred.</p>
<h3>The premise was wrong: the convention is published</h3>
<p>Holland (arXiv 1702.02432v2), sections IV-A and IV-B, describes the SDU calculation as using ground speed and track, <b>zero vertical speed</b>, nominal satellite position and sea-level aircraft position, with the physical Doppler term separately carrying actual vertical motion. That is the convention the model uses. It is documentary support rather than inspected SDU firmware, but it is not an undocumented choice.</p>
<p class="sub">The &ldquo;K-mode OPEN&rdquo; label that prompted this check turns out to concern historical callers that forced the physical up velocity to zero, and an unavailable cross-lineage specification. The current call path passes physical local up and has no such switch. Earlier wording on this page treated that label as evidence the compensation convention was unvalidated. It was not.</p>
<h3>The sweep does not invert the result &mdash; it empties it</h3>
<img src="img/kappa_sweep.png" alt="BFO37 residual against the diagnostic coordinate kappa for all sixteen frozen histories, with compatibility bands marked. All fitted histories leave the band as kappa rises; the two controls begin far below it and never enter." style="width:100%;height:auto;border-radius:6px">
<ul>
<li>All twelve fitted histories keep at least one compatible hypothesis up to <b>&kappa; = 0.042</b>. The last warm-up-compatible one ends at <b>&kappa; = 0.269</b>, and the last compatible history of any kind at <b>&kappa; = 0.317</b>. Above that, nothing in the retained set is compatible.</li>
<li><b>R0 and G0 never become compatible anywhere in [0, 1]</b>, under any of the four geometry switch combinations. There is no value of &kappa; at which a glide control works.</li>
<li>So the sensitivity runs from &ldquo;dives match&rdquo; to &ldquo;nothing matches&rdquo;, never to &ldquo;glides match&rdquo;. The positive half of the TASK_022 reading is fragile beyond about &kappa; = 0.32. The negative half &mdash; that these particular controls fail &mdash; holds across the whole domain.</li>
<li>The original operator reproduces to 4.5&times;10<sup>&minus;13</sup> Hz, and the BTO is untouched by &kappa;, so TASK_022&rsquo;s timing residuals are unchanged.</li></ul>
<h3>The cruise score is not flat, but it cannot choose</h3>
<p class="sub">I expected the nine cruise terms to be blind to &kappa; and predicted a circularity argument from that. The curve is measurably non-flat: &chi;&sup2; moves from 8.117071 to 8.119623 across the full range, a span of 0.00255, with a largest BFO change of 0.116 Hz against a listed &sigma;<sub>BFO</sub> of 4.3 Hz. Codex declined to draw the identifiability conclusion I had anticipated, which was the right call: the claim that the cruise data carry no information is not established. In practice a 0.0026 spread in &chi;&sup2; cannot discriminate between conventions, but that is a statement about resolving power, not about information being absent.</p>
<h3>The 18:25 log-on, as observed</h3>
<div class="scroll"><table><tr><th class="n">Seconds after log-on</th><th class="n">0</th><th class="n">7</th><th class="n">97</th><th class="n">97</th><th class="n">101</th><th class="n">159</th><th class="n">168</th></tr>
<tr><td>BFO (Hz)</td><td class="n">142</td><td class="n">273</td><td class="n">176</td><td class="n">175</td><td class="n">172</td><td class="n">144</td><td class="n">143</td></tr></table></div>
<p class="sub" style="margin-top:6px">Holland identifies the first burst as unreliable on signal quality. Excluding it, the sequence decays by 130 Hz over 161 s &mdash; a real excess-then-decay shape of about the magnitude the warm-up envelope allows (17 to 136 Hz). It is <b>not</b> an independent calibration: the raw differences also contain motion, geometry and channel effects, and this event already contributed to the published envelope, so reusing it would reuse evidence. The envelope was not narrowed. Six other log-ons exist in the literature but their burst samples are not in the archived copy.</p>
<div class="note" style="margin-top:8px"><b>Still unresolved.</b> The BFO bias calibration epoch is MISSING, with a CONFLICT on its locator: the cited reference resolves to a nine-page project packet rather than the article page named. The nominal satellite altitude of 36,210,120 m is an inherited detail with no inspected engineering support. SDU hardware verification and direct oscillator measurements were not obtained.</div></div>

<div class="card"><h2>TASK_029: why every flight lands near 36&deg;S <span class="tag prov">coarse pilot, 1% of grid</span></h2>
<p class="sub">Seven solutions in this family arrive at 00:11 between 35.85&deg;S and 36.85&deg;S. A forward sweep tested whether anything further north is reachable: commanded inputs swept, 00:11 latitude recorded as an output, no optimiser, no target latitude.</p>
<p><b>Fuel was never the obstacle. The handshake sequence is.</b> Four sampled commands reach 23.9&deg;S to 26.4&deg;S still powered at 00:11, holding 2.3 to 3.0 tonnes. Their nine-term &chi;&sup2; is 2,507 against C120&rsquo;s 8.117.</p>
<div class="scroll"><table><tr><th>Handshake</th><th class="n">z&sup2;</th><th class="n">Residual</th><th class="n">Range error</th></tr>
<tr><td>21:41 BTO</td><td class="n">855.4</td><td class="n">29.2&sigma;</td><td class="n">~127 km</td></tr>
<tr><td>00:11 BTO</td><td class="n">829.8</td><td class="n">28.8&sigma;</td><td class="n">~125 km</td></tr>
<tr><td>20:41 BTO</td><td class="n">614.5</td><td class="n">24.8&sigma;</td><td class="n">~108 km</td></tr></table></div>
<p class="sub" style="margin-top:6px">Range errors are mine, converted from the squared residuals at the listed &sigma;<sub>BTO</sub> of 29 &micro;s.</p>
<ul>
<li><b>The mechanism.</b> The ring radii grow through the night at a rate set by ground speed. A flight slow enough to finish north cannot match how fast they expanded earlier. The 00:11 arc alone permits a northern crossing; the sequence of four does not.</li>
<li><b>They fail the chronology too, from the other side.</b> Those four are still powered at 00:25, so they never flame out near 00:17 and cannot produce the 00:19 log-on. Four faster commands exhaust before 00:11. Northern reach and a 00:17 flameout are mutually exclusive in this family.</li>
<li><b>The 19:41 BFO improves sharply:</b> 0.031 against C120&rsquo;s 2.901, with 44 initial states beating C120 on the model&rsquo;s largest single misfit. Every one of them fails later, so this is an observation about one term, not a fit.</li>
<li><b>Incoming leg clears everything:</b> 631 to 843 km from the 18:22 derived radar position, 259 to 346 kt implied, turns of 5&deg; to 67&deg; left. Recorded for every grid point, never used to filter or rank.</li>
<li><b>One hypothesis retired.</b> The package README warns that one-engine fuel burn may be too generous, which would add range and push the endpoint south. The evaluator has no single-engine phase at all &mdash; fuel is one tank feeding both engines &mdash; so that warning does not apply here and the sensitivity is unassessable.</li></ul>
<div class="note" style="margin-top:8px"><b>Coverage.</b> 36 grid points of the 3,276 specified, about 1%. Pressure was sampled only at 175 and 450 hPa with nothing between, so the 200&ndash;300 hPa band where cruise actually lives was never tested, and 24 of 36 rows died on weather coverage or envelope limits at those corners. Nothing is established about commands between the nodes. The conclusion rests on these points plus the structural ring-expansion argument, which together are enough to answer the question and not enough to call it proved.</div></div>
<div class="card"><h2>TASK_030: the full arc-1 sweep, and what it exposed <span class="tag ok">complete, 7 Oct</span></h2>
<p class="sub">1,008 commanded flights across 21 arc-1 start points spanning 6&deg;S to 14&deg;N, four bearings, four Mach values, three pressure levels, screened at dt 15 s with every reported profile rerun at 7.5 s. All 21 starts retained; initial-locus BTO residual 1.16&times;10<sup>&minus;10</sup> &micro;s.</p>
<div class="note bad"><b>The northern endpoint has never been testable, and this is why.</b> The ERA5 subset ends at 10&deg;N and 100&deg;E. The 7th arc crosses 100&deg;E at <b>27.5&deg;S</b>. North of that there is no forcing for an aircraft to fly through, so the model cannot place one on the arc there at all. 765 of 1,008 rows failed on <code>WEATHER_HORIZONTAL_OR_TIME_DOMAIN</code>; starts north of 10&deg;N produced no finite history; and the per-start minima piled up at 29.2&ndash;31.6&deg;S, which is the edge of the data rather than an optimum. Earlier wording on this page read the northern result as a physical exclusion. It is a coverage limit.</div>
<h3>The arc segment nobody could model and nobody has searched</h3>
<img src="img/t30_blindspot.png" alt="The 7th arc against the ERA5 east edge at 100 degrees east and the three approximate seabed search boxes. North of 27 degrees south the arc lies outside both." style="width:100%;height:auto;border-radius:6px">
<p class="sub" style="margin-top:4px">The northern limit of every search box in your manifest is <b>27&deg;S</b>. The arc leaves the weather data at <b>27.5&deg;S</b>. Those two boundaries fall within half a degree of each other, leaving roughly <b>1,460 km of arc</b>, from 27&deg;S to 15&deg;S, that is outside the model's forcing and outside all recorded seabed coverage.</p>
<p class="sub"><b>That coincidence is not mysterious.</b> The ERA5 subset was evidently clipped to the region the search already assumed. The consequence is that the model has never been able to challenge the assumption that defined its own inputs.</p>
<h3>What the sweep found where it could look</h3>
<div class="scroll"><table><tr><th>Result</th><th>Value</th></tr>
<tr><td>Rows with all nine score terms</td><td class="n">267 of 1,008</td></tr>
<tr><td>Powered and force-supported through 00:11</td><td class="n">48</td></tr>
<tr><td>Meeting the declared joint score and fuel bands</td><td class="n">0</td></tr>
<tr><td>Best powered record (start 3&deg;N)</td><td class="n">&chi;&sup2; 221.7 at 30.53&deg;S, 96.30&deg;E, 2,643 kg remaining</td></tr>
<tr><td>Lowest geometric score (start 6&deg;N)</td><td class="n">&chi;&sup2; 112.3 at 31.37&deg;S &mdash; fails buffet at the start, not a feasible flight</td></tr>
<tr><td>Rows improving C120's 19:41 BFO term (2.901)</td><td class="n">460, of which 48 have supported powered histories</td></tr>
<tr><td>Range of verified powered 00:11 latitudes</td><td class="n">24.58&deg;S to 35.48&deg;S</td></tr></table></div>
<h3>The sweep points north, and the absolute scores are not the signal</h3>
<img src="img/t30_chi2_by_start.png" alt="Nine-term chi-squared against arc-1 start latitude on a log scale. The coarse grid scores about 1,170 at C120's own start, where C120 itself achieves 8.12, and reaches 112 at 6 degrees north." style="width:100%;height:auto;border-radius:6px">
<p class="sub" style="margin-top:4px">The grid used bearings {140, 158, 176, 195}&deg;, Mach {0.55, 0.65, 0.75, 0.86} and pressures {200, 260, 320} hPa. C120 flies bearing 184.6&deg; at Mach 0.8406 falling to 0.8306 &mdash; a schedule, not a constant &mdash; at 214.2 hPa, and so misses the grid on all three axes.</p>
<div class="note bad"><b>The decisive number: at C120&rsquo;s own start the grid manages &chi;&sup2; &asymp; 1,174, while that same start demonstrably supports 8.117. The coarse grid is 145&times; off at a point where the right answer is known.</b> So the absolute scores measure the grid&rsquo;s coarseness, not each start&rsquo;s quality &mdash; every start is handicapped alike. What carries information is the <i>relative</i> pattern, and it points north: the grid reaches <b>112.3 at 6&deg;N and 119.5 at 4&deg;N</b>, about <b>ten times better than it manages from C120&rsquo;s start</b>.</div>
<ul>
<li><b>Every per-start minimum chose bearing 176&deg;</b>, the grid value nearest C120&rsquo;s 184.6&deg;. Bearing resolution is 18&deg;, so the optimum bearing is unresolved at every start.</li>
<li><b>The best Mach climbs monotonically with start latitude</b> &mdash; 0.55, 0.65, 0.75 &mdash; and is <b>pinned at the grid ceiling of 0.86 for every start from 6&deg;N north</b>. The grid wanted to go faster than it was allowed to. Mmo is 0.87.</li>
<li><b>460 rows improve C120&rsquo;s 19:41 BFO term</b> of 2.901, the model&rsquo;s single largest misfit, 48 of them with supported powered histories.</li>
<li><b>The trend was still interesting where the data stopped.</b> Starts north of 9&deg;N produced no finite history at all, because ERA5 ends at 10&deg;N.</li></ul>
<p><b>Read together, this is a positive indication of plausible northern arc-1 starts, not an absence of them.</b> A start at which a 145&times;-handicapped grid still reaches 112 is a start that may well support a fit in C120&rsquo;s territory once bearing, Mach and pressure are resolved properly. That is a hypothesis the data suggests and the model cannot currently test.</p>
<div class="note" style="margin-top:8px"><b>What would have to be true for this to be wrong.</b> The 145&times; refinement available at 0.5&deg;N is not guaranteed at 6&deg;N; the refinement factor could be far smaller there. The northern optima may also lie beyond Mach 0.86, which is close enough to Mmo that the real optimum could be outside the airframe envelope rather than merely outside the grid. Neither can be settled at this resolution. <b>&ldquo;Nothing beat C120&rdquo; remains true and remains nearly meaningless</b>, because the grid cannot represent C120 in the first place.</div>
<h3>The start was never observed</h3>
<p class="sub">Part A confirmed that C120's 0.5&deg;N initial latitude is a <b>fitted latitude-box boundary</b>, not an observed latitude; its longitude is then constructed from the 19:41 BTO given that latitude, pressure and datum. The 19:41 BTO is not among the four scored BTOs. Every flight in the family inherits that start, C120 included.</p>
<h3>Three coverage limits, all in the same direction</h3>
<div class="scroll"><table><tr><th>Limit</th><th>Consequence</th></tr>
<tr><td>Grid cannot represent C120&rsquo;s commands</td><td>Absolute &chi;&sup2; is uninformative; no start can be fairly compared with C120</td></tr>
<tr><td>ERA5 ends at 10&deg;N</td><td>Starts north of 9&deg;N have no history, and the trend was still improving</td></tr>
<tr><td>ERA5 ends at 100&deg;E; arc crosses it at 27.5&deg;S</td><td>The endpoints northern starts would reach cannot be scored at all</td></tr></table></div>
<p class="sub" style="margin-top:6px">Every one of these truncates the same hypothesis, and none of them is a physical result.</p>
<p><b>Next:</b> extending ERA5 east to 120&deg;E and north to 20&deg;N is a data acquisition task, not a modelling one, and is the only thing that makes the northern question askable. Until then, no amount of computation can answer it. Directive 19 specifies that acquisition, with an overlap gate so a 2026 download is not silently spliced onto a 2014-vintage subset.</p></div>
<div class="card"><h2>Phase 5A candidates <span class="tag prov">Aug 2026 snapshot</span></h2><p>97 candidates (96 labelled final handshake position, 1 prior diagnostic coordinate). Search status for all 97 is <code>unknown</code>; the file notes that unknown is not converted to unsearched.</p></div>
 <div class="card"><h2>BTO-only survivors <span class="tag prov">Jun 2026</span></h2><p>12 terminal-dynamics diagnostic rows from 3 families in one region. <code>selected_as_best</code> and <code>final_coordinate_produced</code> are false for all 12.</p></div>
 <div class="card"><h2>Radar and search <span class="tag ok">sourced</span></h2><p>One measured radar point (IGARI last SSR, 17:21:13 UTC). The 18:22:12 primary radar report has no coordinates. Search boxes are approximate bounding boxes from your manifest.</p></div>
</div>
<div class="card"><h2>Candidates and the 7th arc</h2>
 <div class="ctl" id="views"></div><div class="read" id="ro">Hover the map for coordinates.</div>
 <canvas id="mp"></canvas>
 <p class="sub" id="lg" style="margin-top:6px"></p></div>
<div class="card"><h2>Phase 5A candidate table</h2><p class="sub">Scores are the snapshot's own columns. The satcom score here is that engine's value, not the frozen v06 scorer's. Distance to the reference arc is computed in this page from the arc file's vertices (nearest point, so slightly overstated between vertices). Click a column to sort.</p><div class="scroll" style="max-height:420px"><table id="ct"></table></div></div>
<div class="card"><h2>BTO-only terminal survivors (June)</h2><p class="sub">Initial parameters are at the start of the path family; terminal values are at 00:19:29 UTC.</p><div class="scroll"><table id="sv"></table></div>
 <div class="note" style="margin-top:8px">The candidate-state file gives the terminal bounding box for this region at 00:19:29 as 44.16–43.28°S, 53.45–55.79°E. Your arc file stops at 64.46°E, but its 200 vertices fit a circle (centre 0.53°N, 64.33°E, radius 44.47°, RMS 0.009°). That circle continues west and passes within 1 to 140 km of the box (dotted line on the map). So this endpoint is on the 7th-arc ring, not off it. Switch to "Western drift focus" to see it. The ring extension is my fit, not a file.</div></div>
<div class="card"><h2>Known caveats in the sources</h2><ul>
 <li>The point 34.86°S, 93.107°E at 36,603 ft appears in candidate-derived geometry. Its BTO bias is observed minus geometry at that point, so a zero residual there is circular and it is not a calibration benchmark (June candidate-state file).</li>
 <li>Prior diagnostic coordinate in Phase 5A: 31.397°S, 90.403°E.</li>
 <li>Height datum: geopotential height treated as ellipsoidal height may matter, per your notes. I have not tested it here.</li></ul></div>
<script>
MH.nav("flight.html");'''+VIEWS+'''
(async()=>{
const [mask,arc,cand,radar,sv,fnd,adf]=await Promise.all(["mask","arc7","phase5a","radar","survivors","finds","avgday"].map(n=>MH.J("data/"+n+".json")));
const map=new MH.Map(document.getElementById("mp"),mask,VIEWS["Search area"]);
map.layers.ring=MH.L.ring();map.layers.arc=MH.L.arc(arc);map.layers.bto=MH.L.box(MH.BTOBOX,'June BTO-only endpoint box');map.layers.search=MH.L.search(MH.SEARCH);map.layers.finds=MH.L.finds(fnd);map.layers.cand=MH.L.cand(cand);
const rp=radar.filter(r=>r.lat_deg).map(r=>({lat:+r.lat_deg,lon:+r.lon_deg}));map.layers.radar=MH.L.radar(rp);
map.layers.flights=MH.L.flights(adf);map.draw();
const m2=new MH.Map(document.getElementById("mp2"),mask,[84,100,-40,2]);m2.layers.ring=MH.L.ring();m2.layers.arc=MH.L.arc(arc);m2.layers.flights=MH.L.flights(adf);m2.draw();
const cs=["--c2","--c1","--c4"];document.getElementById("adv").innerHTML=adf.map((f,i)=>`<span><i style="width:18px;height:3px;background:var(${cs[i]});display:inline-block;vertical-align:middle"></i> ${f.name}</span>`).join(" &nbsp; ");
document.getElementById("adt").innerHTML="<tr><th>Flight</th><th class=n>Mach</th><th class=n>p hPa</th><th class=n>k</th><th class=n>PHYSICAL χ²</th><th class=n>LEGACY χ²</th><th class=n>00:11 lat, lon</th><th class=n>Fuel 00:11 kg</th><th class=n>Fuel 00:17 kg</th><th>Exhausted</th></tr>"+adf.map(f=>`<tr><td>${f.name}</td><td class=n>${f.mach.toFixed(4)}</td><td class=n>${f.p_hpa.toFixed(1)}</td><td class=n>${f.k}</td><td class=n>${f.physical_chi2.toFixed(3)}</td><td class=n>${f.legacy_chi2.toFixed(3)}</td><td class=n>${f.lat_0011.toFixed(3)}, ${f.lon_0011.toFixed(3)}</td><td class=n>${f.fuel_0011_kg.toFixed(0)}</td><td class=n>${f.fuel_0017_kg.toFixed(0)}</td><td>${f.exhaust_utc==="None"?"not by 00:17":f.exhaust_utc.slice(11,19)+" UTC"}</td></tr>`).join("");
matchMedia("(prefers-color-scheme: dark)").addEventListener("change",()=>setTimeout(()=>m2.draw(),50));
const vb=document.getElementById("views");let cur="Search area";
function vb2(){vb.innerHTML=Object.keys(VIEWS).map(k=>`<button class="${k===cur?"on":""}" data-k="${k}">${k}</button>`).join("");vb.querySelectorAll("button").forEach(b=>b.onclick=()=>{cur=b.dataset.k;map.setView(VIEWS[cur]);vb2()})}vb2();
document.getElementById("lg").innerHTML=MH.legend([[MH.css("--c3"),"7th arc (reference file, 40,000 ft; dotted = my circle fit continuing west)"],[MH.css("--bad"),"June BTO-only endpoint box"],[MH.css("--c1"),"candidate, terminal-compatible (larger = stable)"],[MH.css("--muted"),"candidate, not terminal-compatible"],[MH.css("--bad"),"× prior diagnostic coordinate"],[MH.css("--ok"),"debris find site (assumed geocode)"]])+" Average Day tracks are coloured, with stars at 00:11. Dashed boxes: approximate search areas (manifest bounding boxes, not swaths).";
map.onhover=h=>{const f=MH.findNear(fnd,map,h);document.getElementById("ro").textContent=f?MH.findText(f):h?`${Math.abs(h.lat).toFixed(2)}°${h.lat<0?"S":"N"}  ${h.lon.toFixed(2)}°E`:"Hover the map for coordinates."};
matchMedia("(prefers-color-scheme: dark)").addEventListener("change",()=>setTimeout(()=>map.draw(),50));
// tables
const AP=MH.arcPts(arc);let rows=cand.map(c=>({...c,rank:c.r==null?9999:c.r,dist:MH.arcDist(AP,c.lat,c.lon)}));let sk="rank",asc=true;
const cols=[["rank","Rank",0],["id","Candidate",0],["lat","Lat",1],["lon","Lon",1],["dist","km to ref arc",1],["sat","Satcom score",1],["term","Terminal compatible",0],["stable","Stable",0],["srch","Search status",0]];
function ct(){rows.sort((a,b)=>(a[sk]>b[sk]?1:a[sk]<b[sk]?-1:0)*(asc?1:-1));
 document.getElementById("ct").innerHTML="<tr>"+cols.map(([k,l,n])=>`<th class="${n?"n":""}" data-k="${k}" style="cursor:pointer">${l}</th>`).join("")+"</tr>"+rows.map(r=>"<tr>"+cols.map(([k,l,n])=>`<td class="${n?"n":""}">${k==="rank"?(r.r==null?"prior":r.r):k==="dist"?Math.round(r.dist).toLocaleString("en"):k==="sat"?(r.sat==null?"–":r.sat.toFixed(5)):k==="lat"||k==="lon"?r[k].toFixed(3):(r[k]||"–")}</td>`).join("")+"</tr>").join("");
 document.querySelectorAll("#ct th").forEach(t=>t.onclick=()=>{const k=t.dataset.k;if(sk===k)asc=!asc;else{sk=k;asc=true}ct()})}ct();
document.getElementById("sv").innerHTML="<tr><th>#</th><th>Family</th><th>Variant</th><th>Initial lat/lon</th><th class=n>Max |res| µs</th><th class=n>RMS µs</th><th>Transition</th><th class=n>Speed kt</th><th class=n>Track °</th><th class=n>Alt ft</th></tr>"+sv.map(s=>`<tr><td>${s.diagnostic_order}</td><td>${s.family_id.replace("adaptive_","")}</td><td>${s.variant_id_1707.replace("transition_","")}</td><td>${(+s.representative_lat_deg).toFixed(2)}, ${(+s.representative_lon_deg).toFixed(2)}</td><td class=n>${(+s.max_residual_us).toFixed(0)}</td><td class=n>${(+s.rms_residual_us).toFixed(0)}</td><td>${s.limiting_transition}</td><td class=n>${s.terminal_endpoint_speed_kt}</td><td class=n>${s.terminal_endpoint_track_deg}</td><td class=n>${s.terminal_endpoint_altitude_ft}</td></tr>`).join("");
})();
</script>'''+TAIL

pages["map.html"]=HEAD%"MH370 Combined Map"+'''
<h1>Combined map</h1>
<p class="sub">Every layer is real data from your files, drawn on one map. Switch layers on and off. Nothing here is fitted to the arc.</p>
<div class="card"><div class="ctl" id="tg"></div><div class="ctl" id="views" style="margin-top:6px"></div><div class="read" id="ro">Hover the map for coordinates.</div>
 <canvas id="mp"></canvas><p class="sub" id="lg" style="margin-top:6px"></p></div>
<div class="grid">
 <div class="card"><h2>Reading this map</h2><p>The <b>7th arc</b> is the locus of positions at the final handshake (00:19 UTC) from your reference file. <b>Candidates</b> are Phase 5A points near it (65 to 1,306 km away). The <b>density</b> is the combined <i>reverse-drift</i> distribution from the baseline run with assigned classes. It is a different kind of quantity from the arc and candidates, and it depends on assumed find coordinates, the class table and no explicit Stokes.</p></div>
 <div class="card"><h2>What the overlay does and does not show</h2><p>The density peak (35.25°S, 55.75°E) sits about 870 km inside the 7th-arc ring and 918 km from the June BTO-only endpoint box (43.5°S, 55.5°E), which is on the ring. The two share a longitude and differ by about 8° of latitude. That is as far as the data goes. The drift side does not locate the aircraft. Task 9 (complete) found the same broad western focus in the shuffled-region and random-coast nulls, so the peak is not specific to the finds; its cause is the open question, and Task 10 is set up to isolate it.</p><div id="rd"></div></div>
</div>
<script>
MH.nav("map.html");'''+VIEWS+'''
(async()=>{
const [mask,arc,cand,radar,den,fnd,adf]=await Promise.all(["mask","arc7","phase5a","radar","density","finds","avgday"].map(n=>MH.J("data/"+n+".json")));
const map=new MH.Map(document.getElementById("mp"),mask,VIEWS["Whole basin"]);
map.layers.density=MH.L.density(den,false);map.layers.ring=MH.L.ring();map.layers.arc=MH.L.arc(arc);map.layers.bto=MH.L.box(MH.BTOBOX,'June BTO-only endpoint box');map.layers.search=MH.L.search(MH.SEARCH);map.layers.finds=MH.L.finds(fnd);map.layers.cand=MH.L.cand(cand);map.layers.flights=MH.L.flights(adf);
map.layers.radar=MH.L.radar(radar.filter(r=>r.lat_deg).map(r=>({lat:+r.lat_deg,lon:+r.lon_deg})));
const names={density:"Reverse-drift density",hpd:"Density 90% HPD cells",arc:"7th arc",ring:"Ring extension (my fit)",bto:"June BTO-only endpoint box",cand:"Phase 5A candidates",finds:"Debris find sites",flights:"Average Day flights (star = 00:11)",search:"Search areas (approx)",radar:"IGARI radar point"};
const tg=document.getElementById("tg");
tg.innerHTML=Object.entries(names).map(([k,l])=>`<label><input type="checkbox" data-k="${k}" ${k==="hpd"?"":"checked"}>${l}</label>`).join("");
tg.querySelectorAll("input").forEach(i=>i.onchange=()=>{const k=i.dataset.k;if(k==="hpd")map.layers.density.hpd=i.checked;else map.layers[k].on=i.checked;map.draw()});
let cur="Whole basin";const vb=document.getElementById("views");
function vb2(){vb.innerHTML="<span class=muted>View:</span> "+Object.keys(VIEWS).map(k=>`<button class="${k===cur?"on":""}" data-k="${k}">${k}</button>`).join("");vb.querySelectorAll("button").forEach(b=>b.onclick=()=>{cur=b.dataset.k;map.setView(VIEWS[cur]);vb2()})}vb2();
document.getElementById("lg").innerHTML=MH.legend([[MH.css("--accent"),"reverse-drift probability mass (0.5° cells, √ scale)"],[MH.css("--c3"),"7th arc"],[MH.css("--c1"),"Phase 5A candidate"],[MH.css("--ok"),"debris find site (assumed geocode)"]])+" Average Day tracks are coloured, with stars at 00:11. Dashed boxes: approximate search areas. Map shows 15–130°E, 60°S–15°N in the whole-basin view; the arc continues north beyond the frame.";
map.onhover=h=>{const r=document.getElementById("ro");if(!h){r.textContent="Hover the map for coordinates.";return}let t=`${Math.abs(h.lat).toFixed(2)}°${h.lat<0?"S":"N"}  ${h.lon.toFixed(2)}°E`;
 const ff=MH.findNear(fnd,map,h);if(ff)t=MH.findText(ff);const c=ff?null:den.cells.find(c=>Math.abs(c[0]-h.lat)<.25&&Math.abs(c[1]-h.lon)<.25);if(c)t+=`   density mass ${c[2].toExponential(2)}${c[3]?" (HPD"+(c[3]===2?" 50/90":" 90")+")":""}`;r.textContent=t};
const pk=den.cells.reduce((a,b)=>b[2]>a[2]?b:a);const tot=den.cells.reduce((a,c)=>a+c[2],0);const h90=den.cells.filter(c=>c[3]>=1);
document.getElementById("rd").innerHTML=`<table><tr><td>Peak cell</td><td class=n>${Math.abs(pk[0])}°S ${pk[1]}°E</td></tr><tr><td>Peak cell mass</td><td class=n>${(pk[2]*100).toFixed(2)}%</td></tr><tr><td>Cells in 90% HPD</td><td class=n>${h90.length}</td></tr><tr><td>Mass in HPD-90 cells</td><td class=n>${(h90.reduce((a,c)=>a+c[2],0)*100).toFixed(1)}%</td></tr></table>`;
matchMedia("(prefers-color-scheme: dark)").addEventListener("change",()=>setTimeout(()=>map.draw(),50));
map.draw();
})();
</script>'''+TAIL

pages["drift.html"]=HEAD%"MH370 Drift"+'''
<h1>Drift and currents <span class="tag prov">assumption-dependent</span></h1>
<p class="sub">Ocean currents (GLORYS12V1 via Copernicus Marine), the debris reverse-drift density, and the three follow-up diagnostics.</p>
<div class="note ok"><b>Newer results:</b> Task 10 (origin of the western focus), the Task 11 drifter hindcast, the forward release from 24.5–41°S, 80–100°E and the gyre/mean-flow check are on <a href="drift2.html" style="color:var(--accent)">Drift diagnostics</a>.</div>
<div class="card"><h2>Surface currents, March 2014 – July 2015</h2>
 <p class="sub">Monthly mean and mid-month snapshot, 17 months, with a floating-object drift mode. Daily 0.494 m currents averaged to 1/3°. March 2014 starts 8 March. Winds are NCEP/NCAR Reanalysis 1 (about 1.9°).</p>
 <iframe src="currents.html" style="height:1500px" title="Indian Ocean surface currents" loading="lazy"></iframe>
 <p class="sub" style="margin-top:6px"><a href="currents.html" style="color:var(--accent)">Open the currents map full page</a></p></div>
<div class="card"><h2>Combined reverse-drift density (baseline, assigned classes)</h2>
 <div class="ctl"><label><input type="checkbox" id="hp"> 90% HPD cells</label><label><input type="checkbox" id="ar" checked> 7th arc</label><span class="muted"><i style="width:10px;height:10px;border-radius:50%;background:var(--ok);display:inline-block"></i> debris find sites (assumed geocodes, 32 items at 21 sites)</span></div><div class="read" id="ro">Hover for density.</div>
 <canvas id="mp"></canvas>
 <div class="note" style="margin-top:8px">Depends on: assumed find coordinates (<code>ASSUMED_GEOCODE</code>), the assigned leeway class table, daily winds, no explicit Stokes, absorbing coasts and the offshore launch rule. No parameter was chosen by agreement with the 7th arc.</div>
 <div class="note bad" style="margin-top:8px"><b>Corrected 8 October.</b> <b>Only 21 of the 32 items contribute to this field, across 18 of the 23 distinct date windows.</b> The legend above counts the find-site markers, not the density&rsquo;s inputs, and the card previously gave no contributing count at all. TASK_021 Part A also confirmed <b>upstream smoothing</b> of the field before it is written, so the peak marked at 35.25&deg;S, 55.75&deg;E is the maximum of a smoothed field, not of the raw one &mdash; the atlas asserted the opposite for a day. All 11 exclusions are <b>identification-based</b> &mdash; not trajectory conditioning, which retires one circularity concern. But <b>10 of the 11 are Madagascar items</b>, so the mechanism is not geographic while the effect is: one region is almost wholly absent from the field, and the markers plotted here include items that do not inform it. TASK_021 is testing what this peak represents, and measuring how far it moves if the excluded items are put back.</div></div>
<div class="grid">
 <div class="card"><h2>Currents-only forward drift test, 8–23 Mar 2014</h2>
 <p class="sub">From <code>reverse_drift_forward_summary.csv</code>: 15 days of currents-only forward drift (no wind or Stokes) from arc points 26–41°S. Lines join each arc point to its endpoint.</p>
 <canvas id="mp3"></canvas>
 <div class="grid" style="margin-top:8px"><div><img src="img/currents_only.png" alt="Currents-only drift test: seeds, reverse drift and forward endpoints from the 7th arc" style="width:100%;height:auto;border-radius:6px"><p class="sub" style="margin-top:4px">Your figure, with the French-area seeds and the reverse drift.</p></div>
 <div class="scroll"><table id="fw"></table></div></div>
 <div class="note" style="margin-top:8px">Currents-only test. Endpoints move 32–204 nm from the arc point in 15 days; the minimum gap to the seed field is 40–970 nm (the table). No wind slip is included, which the leeway audit says is the main missing term.</div></div>
<div class="card"><h2>Task 7: recovery-delay ceiling</h2><p class="sub">Share of arrivals already later than the find window at zero delay. A delay can only push arrivals later, so this is a hard ceiling. Range spans the saved leeway grid.</p>
  <div class="ctl">Window tolerance <select id="tol"></select></div><div class="scroll" style="margin-top:6px"><table id="t7"></table></div></div>
 <div class="card"><h2>Task 8: leeway class support</h2><p class="sub">Literature audit only. Classes unchanged.</p><div class="scroll"><table id="t8"></table></div></div>
</div>
<div class="card"><h2>Task 9: independent-seed null tests <span class="tag ok">complete, 90 of 90</span></h2>
 <p>30 runs each of shuffled regions, random coast and observed, 32 items × 500 particles, all physics and seeds as registered. Closure passed 256/256 and the saved N2 baseline reproduced exactly (Codex qualification).</p>
 <div class="scroll"><table id="t9h"></table></div>
 <div class="ctl" style="margin-top:10px"><span class="muted">Peak of the combined density, every run:</span></div>
 <canvas id="mp4"></canvas>
 <p class="sub" id="lg4" style="margin-top:6px"></p>
 <div class="grid" style="margin-top:8px">
  <div><h3>Peak spread (all runs, grid 0.5°)</h3><div class="scroll"><table id="t9s"></table></div></div>
  <div><h3>Fixed original run among each null</h3><div class="scroll"><table id="t9p"></table></div><p class="sub" style="margin-top:6px">Empirical midranks of the single original N2 run, not averages over the new observed seeds.</p></div>
 </div>
 <div class="note ok" style="margin-top:8px"><b>Reading.</b> Scrambling find locations leaves the peak where it was: every null peak is within 500 km of the original, and 96.7% of shuffled-region peaks are within 250 km. The observed replicates are more spread than the shuffled nulls and drift east (mean 58.05°E). The western focus comes from the frozen dynamics, launch and density method and survivor conditioning, not from the find locations. The exact 55.75°E is not stable.</div>
 <div class="note" style="margin-top:8px"><b>Arc distance.</b> Codex's peak-to-arc distance (1,003–1,433 km) uses the arc file, which stops at 64.46°E. Measured to the full ring (my circle fit), peaks are 726–1,059 km inside it, mean about 920 km, with a handful under 1,000 km. Either way no peak is near the ring.</div>
 <div class="note" style="margin-top:8px"><b>Not isolated.</b> The test does not say which component causes the focus, and it does not show the finds are uninformative in general. Results depend on assumed coordinates, assigned classes and divergence, daily NCEP winds, N2 launches, absorbing coasts, diffusion and region-balanced smoothing. Explicit Stokes stays null.</div></div>
<div class="card"><h2>Open caveats</h2><ul><li>Find coordinates and date intervals are assumed.</li><li>Class slip and divergence are my assumptions. The audit finds C3 unsupported as a measured class and C2 untestable.</li><li>Daily NCEP winds and no Stokes (WAVERYS not acquired). ERA5 not yet used.</li><li>Beach residence, refloat and detection delay are not modeled; Task 7 delays are post-hoc shifts only.</li></ul></div>
<script>
MH.nav("drift.html");'''+VIEWS+'''
(async()=>{
const [mask,arc,den,t7,t8,t9,fnd,fwd,T9]=await Promise.all(["mask","arc7","density","task7","task8","task9","finds","fwd","task9_final"].map(n=>MH.J("data/"+n+".json")));
const map=new MH.Map(document.getElementById("mp"),mask,[20,100,-55,0]);
map.layers.density=MH.L.density(den,false);map.layers.ring=MH.L.ring();map.layers.arc=MH.L.arc(arc);map.layers.bto=MH.L.box(MH.BTOBOX,'BTO-only endpoint');map.layers.finds=MH.L.finds(fnd);map.draw();
document.getElementById("hp").onchange=e=>{map.layers.density.hpd=e.target.checked;map.draw()};document.getElementById("ar").onchange=e=>{map.layers.arc.on=e.target.checked;map.draw()};
map.onhover=h=>{const r=document.getElementById("ro");if(!h){r.textContent="Hover for density.";return}let t=`${Math.abs(h.lat).toFixed(2)}°${h.lat<0?"S":"N"}  ${h.lon.toFixed(2)}°E`;const ff=MH.findNear(fnd,map,h);const c=den.cells.find(c=>Math.abs(c[0]-h.lat)<.25&&Math.abs(c[1]-h.lon)<.25);if(c)t+=`   mass ${(c[2]*100).toFixed(3)}%`;r.textContent=ff?MH.findText(ff):t};
matchMedia("(prefers-color-scheme: dark)").addEventListener("change",()=>setTimeout(()=>map.draw(),50));
const m3=new MH.Map(document.getElementById("mp3"),mask,[78,106,-52,-22]);m3.layers.ring=MH.L.ring();m3.layers.arc=MH.L.arc(arc);m3.layers.fwd=MH.L.fwd(fwd);m3.draw();
document.getElementById("fw").innerHTML="<tr><th class=n>Arc lat</th><th class=n>Arc lon</th><th class=n>End lat</th><th class=n>End lon</th><th class=n>Disp nm</th><th class=n>Brg °</th><th class=n>Min gap nm</th><th class=n>Median gap nm</th></tr>"+fwd.map(r=>`<tr><td class=n>${r.arc_lat}</td><td class=n>${r.arc_lon.toFixed(2)}</td><td class=n>${r.end_lat.toFixed(2)}</td><td class=n>${r.end_lon.toFixed(2)}</td><td class=n>${r.cur_disp_nm.toFixed(0)}</td><td class=n>${r.cur_brg.toFixed(0)}</td><td class=n>${r.min_gap_nm.toFixed(0)}</td><td class=n>${r.median_gap_nm.toFixed(0)}</td></tr>`).join("");
matchMedia("(prefers-color-scheme: dark)").addEventListener("change",()=>setTimeout(()=>m3.draw(),50));
const tols=[...new Set(t7.map(r=>r.tolerance_days))];const sel=document.getElementById("tol");sel.innerHTML=tols.map(t=>`<option value="${t}">±${t} d</option>`).join("");
const p=v=>(100*v).toFixed(1)+"%";
function r7(){const rows=t7.filter(r=>r.tolerance_days===sel.value);document.getElementById("t7").innerHTML="<tr><th>Region</th><th class=n>Late at zero delay</th><th class=n>Ceiling</th></tr>"+rows.map(r=>`<tr><td>${r.region}</td><td class=n>${p(+r.zero_delay_late_min)} – ${p(+r.zero_delay_late_max)}</td><td class=n>${p(+r.potential_success_ceiling_min)} – ${p(+r.potential_success_ceiling_max)}</td></tr>`).join("")}
sel.onchange=r7;r7();
document.getElementById("t8").innerHTML="<tr><th>Class</th><th class=n>Slip %</th><th class=n>Angle ≤°</th><th>Assessment</th></tr>"+t8.map(r=>`<tr><td>${r.class_id}</td><td class=n>${(+r.raw_min_percent).toFixed(1)}–${(+r.raw_max_percent).toFixed(1)}</td><td class=n>${r.angle_abs_max_deg}</td><td>${r.assessment.replace(/_/g," ").toLowerCase()}</td></tr>`).join("");
const nm={shuffled_regions:"Shuffled regions",random_coast:"Random coast",observed:"Observed"};const f1=(v,d=1)=>(+v).toFixed(d);
document.getElementById("t9h").innerHTML="<tr><th>Experiment</th><th class=n>Runs</th><th class=n>Survival %</th><th class=n>Mean peak</th><th class=n>≤250 km</th><th class=n>≤500 km</th><th class=n>≤1000 km</th><th class=n>31–34°S survivors %</th><th class=n>Mean peak shift km</th></tr>"+T9.headlines.map(h=>`<tr><td>${nm[h.experiment]}</td><td class=n>${h.n}</td><td class=n>${f1(h.mean_survival_percent,2)}</td><td class=n>${Math.abs(h.mean_peak_lat).toFixed(2)}°S ${f1(h.mean_peak_lon,2)}°E</td><td class=n>${f1(h.within250_percent)}%</td><td class=n>${f1(h.within500_percent)}%</td><td class=n>${f1(h.within1000_percent)}%</td><td class=n>${f1(h.mean_survivors_31_34_percent)}</td><td class=n>${f1(h.mean_peak_shift_km,0)}</td></tr>`).join("");
document.getElementById("t9s").innerHTML="<tr><th>Experiment</th><th>Metric</th><th class=n>Mean</th><th class=n>SD</th><th class=n>5–95%</th><th class=n>Range</th></tr>"+T9.summary.filter(s=>/peak_(lat|lon)$/.test(s.metric)).map(s=>`<tr><td>${nm[s.experiment]}</td><td>${s.metric.replace("peak_","")}</td><td class=n>${f1(s.mean,2)}</td><td class=n>${f1(s.sd,2)}</td><td class=n>${f1(s.p05,2)} – ${f1(s.p95,2)}</td><td class=n>${f1(s.minimum,2)} – ${f1(s.maximum,2)}</td></tr>`).join("");
const mn={peak_density_per_km2:"Peak density",mass_within500km_peak:"Mass ≤500 km of peak",mass_within1000km_peak:"Mass ≤1000 km of peak"};
document.getElementById("t9p").innerHTML="<tr><th>Null</th><th>Metric</th><th class=n>Original run</th><th class=n>Percentile</th></tr>"+T9.percentiles.map(p=>`<tr><td>${nm[p.null]}</td><td>${mn[p.metric]||p.metric}</td><td class=n>${p.metric==="peak_density_per_km2"?(+p.observed_fixed).toExponential(2):f1(p.observed_fixed,3)}</td><td class=n>${f1(p.midrank_percentile)}</td></tr>`).join("");
const m4=new MH.Map(document.getElementById("mp4"),mask,[40,75,-45,-25]);m4.layers.ring=MH.L.ring();m4.layers.peaks=MH.L.peaks(T9.runs);m4.layers.finds=MH.L.finds(fnd);m4.draw();
document.getElementById("lg4").innerHTML=MH.legend([[MH.css("--c1"),"shuffled regions (30)"],[MH.css("--c3"),"random coast (30)"],[MH.css("--c2"),"observed seeds (30)"],[MH.css("--ok"),"find sites"]])+" Peaks sit on a 0.5° grid, so many overlap; darker means more runs.";
matchMedia("(prefers-color-scheme: dark)").addEventListener("change",()=>setTimeout(()=>m4.draw(),50));
})();
</script>'''+TAIL
pages["drift2.html"]=HEAD%"MH370 Drift Diagnostics"+open("src/drift2_body.html").read()+'<script>MH.nav("drift2.html");</script>'+TAIL
pages["closing.html"]=HEAD%"MH370 Closing Report"+open("src/closing_body.html").read()+'<script>MH.nav("closing.html");</script>'+TAIL
pages["index.html"]='''<title>MH370 Models Atlas</title><link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="common.css"><script src="common.js"></script>
<div class="wrap"><nav id="nav"></nav>
<h1>MH370 models in one place</h1>
<p class="sub">Satcom, flight models and drift, drawn from your own files. Where a source is missing or provisional, the page says so. The satellite and flight chapter closed on 6 October 2026 and was partly reopened on 7 October: the arc north of 27.5&deg;S turns out to lie outside the model’s weather data, so northern endpoints were never testable. The drift branch is still open.</p>
<div class="grid">
 <a class="card" href="satcom.html" style="text-decoration:none;color:inherit"><h2>Satcom <span class="tag frozen">frozen</span></h2><p>5,029 BTO/BFO rows from the Inmarsat log, the canonical 19-row event table and the published satellite states.</p></a>
 <a class="card" href="flight.html" style="text-decoration:none;color:inherit"><h2>Flight models <span class="tag prov">provisional</span></h2><p>Average Day flights re-flown from your package, the High-Fidelity Average Day Solver (TASK_021), the TASK_022 terminal experiment, 97 Phase 5A candidates, BTO-only survivors.</p></a>
 <a class="card" href="map.html" style="text-decoration:none;color:inherit"><h2>Combined map</h2><p>Arc, candidates, search areas and the reverse-drift density on one switchable map.</p></a>
 <a class="card" href="drift.html" style="text-decoration:none;color:inherit"><h2>Drift <span class="tag prov">assumption-dependent</span></h2><p>17-month currents map, reverse-drift density, currents-only forward test, Tasks 7 to 9 (Task 9 complete).</p></a>
 <a class="card" href="closing.html" style="text-decoration:none;color:inherit"><h2>Closing report <span class="tag frozen">satellite chapter</span></h2><p>What the satcom and flight branch established, what it rests on, and an appendix of readings that were wrong.</p></a>
 <a class="card" href="drift2.html" style="text-decoration:none;color:inherit"><h2>Drift diagnostics <span class="tag prov">conditional</span></h2><p>Task 10 results, drifter hindcast, forward release grid, permutation null, the B1 stop, the provenance audit, and why no source region can be determined.</p></a>
</div>
<div class="card"><h2>Status of each model</h2><table>
<tr><th>Model</th><th>Status</th><th>What this atlas shows</th><th>What is missing here</th></tr>
<tr><td>Satellite BTO/BFO</td><td><span class="tag frozen">frozen</span></td><td>Raw burst log; June manifest facts (bias, calibration residual)</td><td>Frozen v06 scorer outputs are not in the folders I could read</td></tr>
<tr><td>Average Day flight model</td><td><span class="tag frozen">frozen</span></td><td>3 reference flights re-flown from your 3 Oct package (verify.py passes), TASK_021 solver, TASK_022 terminal experiment, TASK_026 convention sweep, TASK_029 reachability</td><td>Score stops at 00:11; no endpoint by design. Chapter closed 6 Oct &mdash; see the closing report</td></tr>
<tr><td>Other endpoint work</td><td><span class="tag prov">provisional</span></td><td>TASK_021, TASK_022, the TASK_026 convention sweep and the TASK_030 arc-1 sweep, on the Flight models page</td><td>No final coordinate exists in any source. <b>Northern arc-1 starts score ten times better than C120's own start under a grid 145&times; too coarse to represent C120 &mdash; a positive indication that cannot be tested.</b> The arc north of 27.5&deg;S is outside the ERA5 domain and outside every search box in the manifest</td></tr>
<tr><td>Ocean currents</td><td><span class="tag ok">data</span></td><td>GLORYS12V1 daily surface currents, 17 months</td><td>Not a drift result by itself</td></tr>
<tr><td>Debris drift</td><td><span class="tag prov">assumption-dependent</span></td><td>Baseline density; Tasks 7 and 8 results</td><td>Tasks 9&ndash;16: no source region is determinable. The method recovers known synthetic sources, but on the real finds the answer moves 1,000&ndash;1,900 km when an unmeasured assumption changes. B1 found no supported bias correction; the 1.2% slip floor was fitted to forcing products B0 does not use</td></tr></table></div>
<div class="card"><h2>Sources used</h2><table>
<tr><th>Data</th><th>File</th><th>Snapshot</th></tr>
<tr><td>Canonical events, satellite state, Average Day flights</td><td><code>MH370_AverageDay_algorithm_2026-10-03.zip</code> (data/, examples/, re-flown here)</td><td>3 Oct 2026</td></tr>
<tr><td>Forward currents-only test</td><td><code>reverse_drift_forward_summary.csv</code></td><td>Mar 2014 test</td></tr>
<tr><td>Burst log</td><td><code>satcom_observations.csv</code> (WS-004 canon)</td><td>13 Jul 2026 recovery</td></tr>
<tr><td>Event table, survivors</td><td><code>satcom_events.csv</code>, <code>candidate_survivors_top.csv</code> (WS-002)</td><td>11 Jun 2026 restart</td></tr>
<tr><td>Candidates</td><td><code>MH370_PHASE5A_CANDIDATE_STATUS.csv</code> (WS-008)</td><td>2 Aug 2026</td></tr>
<tr><td>7th arc</td><td><code>reference_arc.json</code> (Codex 2026-10-03), 40,000 ft reference</td><td>3 Oct 2026</td></tr>
<tr><td>Radar, search areas</td><td><code>radar_track_points.csv</code>, <code>search_history_manifest.csv</code> (WS-004)</td><td>13 Jul 2026</td></tr>
<tr><td>Drift density, Tasks 7 to 9 (Task 9 complete)</td><td>Codex outputs, <code>diagnostics_v2</code></td><td>3–5 Oct 2026</td></tr>
<tr><td>Currents</td><td>GLORYS12V1 via Copernicus Marine; NCEP/NCAR winds</td><td>Mar 2014 – Jul 2015</td></tr></table></div>
<div class="card"><h2>Appendix: sources set aside</h2><ul>
<li>Satellite ephemeris in WS-004: one fixed position with zero velocity for all 5,029 rows. Not used.</li>
<li>The reference arc file stops at 64.46°E. Its western continuation is my circle fit and is drawn dotted.</li>
<li>Point 34.86°S, 93.107°E: circular as a calibration benchmark, per the June candidate-state file.</li>
<li>The archive domain folders (satcom, flight dynamics, terminal event, search) are empty placeholders. The material is in <code>archive/source_snapshots</code>.</li></ul></div>
</div>
<script>MH.nav("index.html")</script>'''
for k,v in pages.items(): open(k,"w").write(v)
