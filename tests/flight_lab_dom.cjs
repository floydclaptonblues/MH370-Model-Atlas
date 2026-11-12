// DOM/controller regression checks, not browser rendering or scientific model validation.
const {JSDOM}=require('jsdom'),fs=require('fs'),assert=require('node:assert/strict');
const dom=new JSDOM(fs.readFileSync('flight-lab.html','utf8'),{url:'https://example.test/flight-lab.html',runScripts:'outside-only'}),w=dom.window;
const timers=new Map();let next=0,scene;w.setInterval=fn=>{timers.set(++next,fn);return next;};w.clearInterval=id=>timers.delete(id);
w.Scene3D=class {constructor(){scene=this;}setScene(s){this.scene=s;}setView(){} };w.HTMLElement.prototype.scrollIntoView=()=>{};
w.eval(fs.readFileSync('flight-lab/assets/data.js','utf8'));w.eval(fs.readFileSync('flight-lab/assets/app.js','utf8'));
const $=s=>w.document.querySelector(s),tests=[],check=(name,v)=>{assert(v,name);tests.push(name);},click=s=>$(s).click(),input=(s,v,event='input')=>{const el=$(s);el.value=v;el.dispatchEvent(new w.Event(event,{bubbles:true}));},tick=()=>[...timers.values()].forEach(fn=>fn()),state=()=>w.FLIGHT_LAB.getState();
click('#guided-example');check('Seven checkpoint worked example',+$('#time-slider').max===6);
for(let i=0;i<7;i++){
 input('#time-slider',i);const st=w.MH370_DATA.witness.states[i],text=$('#inspector').textContent;
 check('Source-state synchronization at checkpoint '+i,state().checkpoint===i&&$('[data-checkpoint-utc]').dataset.checkpointUtc===st.epoch&&+$('[data-fuel-cursor]').dataset.fuelCursor===i&&scene.scene.points.find(p=>p.size===6).id==='checkpoint:'+i&&[st.massKg/1000,st.fuelKg,Math.abs(st.lat),Math.abs(st.lon)].every((v,k)=>text.includes(v.toLocaleString('en-US',{minimumFractionDigits:[2,1,4,4][k],maximumFractionDigits:[2,1,4,4][k]}))));
}
const slider=$('#time-slider');input('#time-slider',2);check('Slider node preserved during drag',slider===$('#time-slider'));
click('#step-play');tick();check('Slideshow advances one saved checkpoint',state().checkpoint===3);
input('#time-slider',1);tick();check('Slider interrupts timer',state().checkpoint===1&&!state().playing&&timers.size===0);
click('#step-play');click('#step-next');tick();check('Next button interrupts timer',state().checkpoint===2&&!state().playing);
click('#step-play');click('#jump-terminal');tick();check('Jump interrupts timer',state().checkpoint===6&&!state().playing);
click('#step-play');tick();check('Restart from final checkpoint starts at first then advances',state().checkpoint===1&&state().playing);
click('[data-view="forces"]');tick();check('View switch stops playback',!state().playing&&state().view==='forces');
click('#guided-example');click('#cloud-mode');const p=w.MH370_DATA.points.find(p=>p.flightId===w.MH370_DATA.witness.flightId&&p.id!==w.MH370_DATA.witness.responseId&&p.compatible);input('#point-select',p.id,'change');click('#point-flight');
check('Different response on witness parent gets no witness terminal state',!$('#time-slider')&&state().routeResponseId===p.id&&$('#inspector').textContent.includes('00:11:00'));
check('Missing ground speed remains missing',$('#inspector').textContent.includes('Ground speed—'));
check('Derived summary mass is labelled',$('#inspector').textContent.includes('Mass · derived'));
click('#cloud-mode');const orphan=w.MH370_DATA.points.find(p=>!w.MH370_DATA.flights.some(f=>f.id===p.flightId)&&p.compatible);input('#point-select',orphan.id,'change');click('#route-mode');check('Response without parent cannot show stale previous flight',$('#inspector').textContent.includes('No saved flight available'));
click('[data-view="grid"]');const empty=w.MH370_DATA.configurations.find(c=>!w.MH370_DATA.flights.some(f=>f.configId===c.id));input('#cell-select',empty.id,'change');click('[data-view="flight"]');check('Uncomputed cell clears selected flight',$('#inspector').textContent.includes('No saved flight available'));
click('#guided-example');input('#time-slider',6);click('#inspect-forces');check('Force view follows selected UTC',state().terminalIndex===6&&$('#scene-count').textContent.startsWith('00:19:37'));
const st=w.MH370_DATA.witness.states[6];check('Force diagram lift length matches source magnitude',Math.abs(Math.hypot(...scene.scene.lines.find(l=>l.color==='#83c5f2'&&l.width===3).b)-st.liftN/350000)<1e-10);
check('Force diagram drag length matches source magnitude',Math.abs(Math.hypot(...scene.scene.lines.find(l=>l.color==='#ecc17b'&&l.width===3).b)-st.dragN/350000)<1e-10);
click('#force-back');check('Force return preserves exact witness response',state().checkpoint===6&&state().routeResponseId===w.MH370_DATA.witness.responseId);
check('Actual elapsed interval explicitly displayed',$('#checkpoint-interval').textContent.includes('8.000 seconds'));
console.log(JSON.stringify({scope:'DOM/controller checks with stubbed canvas renderer and controlled timers; not pixel/browser QA',passed:tests.length,tests},null,2));
