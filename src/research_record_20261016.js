/* Source-based addendum for EXISTING Atlas pages. No model computation or route.
 * Loaded by common.js; gen.py already retains that shared script reference.
 * Content and provenance live in ../data/research_record_20261016.json.
 * Do not merge these historically distinct evaluators into one qualified flight.
 */
(function () {
  'use strict';
  const scriptURL = document.currentScript && document.currentScript.src;
  if (!scriptURL) return;
  const page = location.pathname.split('/').pop() || 'index.html';
  const pages = new Set(['index.html','satcom.html','flight.html','closing.html','northsouth.html']);
  if (!pages.has(page)) return;
  const full = page === 'flight.html' || page === 'closing.html';
  const dataURL = new URL('../data/research_record_20261016.json', scriptURL);
  function element(tag, text, className) {
    const node = document.createElement(tag);
    if (text !== undefined && text !== null) node.textContent = text;
    if (className) node.className = className;
    return node;
  }
  function reference(id) {
    const a = element('a', '[source]');
    a.href = '#record-source-' + id;
    a.className = 'rr-source-link';
    return a;
  }
  function paragraph(parent, text, source) {
    const p = element('p', text);
    if (source) { p.append(' ', reference(source)); }
    parent.append(p);
    return p;
  }
  function section(parent, title, id) {
    const s = element('section');
    if (id) s.id = id;
    s.append(element('h3', title));
    parent.append(s);
    return s;
  }
  function table(parent, headings, rows, caption) {
    const region = element('div', null, 'rr-table-scroll');
    region.tabIndex = 0;
    region.setAttribute('role','region');
    region.setAttribute('aria-label', caption);
    const t = element('table');
    t.append(element('caption',caption));
    const head = element('thead'), tr = element('tr');
    headings.forEach(h => { const th = element('th',h); th.scope='col'; tr.append(th); });
    head.append(tr); t.append(head);
    const body=element('tbody');
    rows.forEach(values => {
      const row=element('tr');
      values.forEach((value,i) => {
        const cell=element(i === 0 ? 'th' : 'td');
        if (i === 0) cell.scope='row';
        if (value instanceof Node) cell.append(value); else cell.textContent=value;
        row.append(cell);
      });
      body.append(row);
    });
    t.append(body);region.append(t);parent.append(region);
  }
  function revealHash() {
    if (!location.hash) return;
    let id;
    try { id=decodeURIComponent(location.hash.slice(1)); } catch (_) { return; }
    if (!id.startsWith('record-') && !id.startsWith('run-history-') && id!=='research-record-20261016') return;
    const target=document.getElementById(id);
    if (!target) return;
    let node=target;
    while (node) { if (node.tagName==='DETAILS') node.open=true; node=node.parentElement; }
    requestAnimationFrame(() => target.scrollIntoView({block:'start'}));
  }
  function render(data) {
    const wrap=document.querySelector('.wrap');
    const h1=wrap && wrap.querySelector('h1');
    if (!h1 || document.getElementById('research-record-20261016')) return;
    const style=element('style');
    style.textContent=`
      #research-record-20261016{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--c1);border-radius:8px;padding:18px;min-width:0}
      #research-record-20261016 h2{font-size:19px;line-height:1.35;margin:4px 0 12px}
      #research-record-20261016 h3{font-size:15px;margin:18px 0 8px}
      #research-record-20261016 p{margin:0 0 10px;max-width:95ch}
      #research-record-20261016 a{color:var(--accent);text-underline-offset:2px}
      #research-record-20261016 a:focus-visible,#research-record-20261016 summary:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
      #research-record-20261016 .rr-kicker{color:var(--muted);font-size:12px}
      #research-record-20261016 .rr-status{font-weight:700}
      #research-record-20261016 .rr-source-link{font-size:12px;white-space:nowrap}
      #research-record-20261016 .rr-table-scroll{overflow:auto;max-width:100%;border:1px solid var(--line);border-radius:6px;margin:10px 0}
      #research-record-20261016 table{min-width:680px;table-layout:auto}
      #research-record-20261016 caption{text-align:left;padding:10px;color:var(--muted);font-size:12px}
      #research-record-20261016 th,#research-record-20261016 td{padding:10px;position:static}
      #research-record-20261016 tbody th{width:105px;white-space:normal;color:var(--fg)}
      #research-record-20261016 details{border-top:1px solid var(--line);padding-top:12px;margin-top:16px}
      #research-record-20261016 summary{font-weight:700;cursor:pointer;margin-bottom:10px}
      #research-record-20261016 blockquote{border-left:3px solid var(--line);margin:12px 0;padding:4px 12px}
      #research-record-20261016 .rr-source{padding:12px 0;border-bottom:1px solid var(--line);scroll-margin-top:12px}
      #research-record-20261016 .rr-source h4{font-size:14px;margin:0 0 6px}
      #research-record-20261016 .rr-policy{border-top:1px solid var(--line);padding-top:12px;margin-top:14px}
      .rr-archive-label{border-left:3px solid var(--line);padding:8px 12px;margin:0;color:var(--muted);font-size:13px}
      @media(max-width:600px){#research-record-20261016{padding:14px}#research-record-20261016 h2{font-size:17px}}
    `;
    document.head.append(style);
    const record=element('section');
    record.id='research-record-20261016';
    record.setAttribute('aria-labelledby','record-title');
    record.dataset.version=data.version;
    record.append(element('p','Project record • '+data.updated,'rr-kicker'));
    const title=element('h2',data.title);title.id='record-title';record.append(title);
    paragraph(record,data.headline).className='rr-status';
    paragraph(record,data.status_note);
    const freeze=section(record,'What the resolution-limit decision actually says','record-freeze');
    data.freeze_points.forEach(text=>paragraph(freeze,text,'freeze'));
    const quote=element('blockquote',data.sources.find(s=>s.id==='freeze').quote);
    freeze.append(quote);
    paragraph(freeze,'Recorded reopening conditions: new independent measurements, or an early-offset check identifying a systematic error large enough to move the arcs. The later task ledger records subsequent experiments separately; it does not silently replace this freeze decision.','freeze');
    const lanes=section(record,'Keep three kinds of result separate','record-distinctions');
    data.lanes.forEach(([label,text,source])=>{
      const p=element('p');p.append(element('strong',label+'. '),document.createTextNode(text),' ',reference(source));lanes.append(p);
    });
    if (full) {
      const history=element('details');history.open=page==='flight.html';history.id='run-history-20261016';
      history.append(element('summary','Run ledger — original connected work and TASK_042–053'));
      paragraph(history,'Execution status and scientific outcome are separate columns. “Delivered” is not a claim that the original scientific aim was fully resolved. Task numbers are identifiers, not a claim that every tranche ran in numerical order.');
      table(history,['Run / source','Execution status','Established result','Still conditional or unresolved'],data.runs.map(r=>{
        const label=element('span');label.append(element('strong',r.task),element('br'),reference(r.source));
        return [label,r.execution,r.finding,r.limit];
      }),'Source-based record: one row per task, not one row per uploaded file.');
      paragraph(history,data.inventory_note);
      record.append(history);
      const latest=section(record,'Latest revised-model endpoint candidates — TASK_053','record-latest-candidates');
      table(latest,['Parent','19:41 latitude','BTO residual','Fuel at 19:41','Pilot outcome'],data.candidates,'Production-resolution candidates; not finely qualified SATCOM connections.');
      paragraph(latest,data.candidate_note,'t053');
      const timeline=element('details');timeline.id='record-chronology';timeline.append(element('summary','Freeze, reopening and reassessment chronology'));
      data.chronology.forEach(([date,label,text,source])=>{const p=element('p');p.append(element('strong',date+' — '+label+'. '),document.createTextNode(text),' ',reference(source));timeline.append(p);});
      record.append(timeline);
    } else {
      paragraph(record,'The full task-by-task ledger and the two latest production candidates are integrated into the existing Flight models and Closing report pages.');
      const links=element('p');
      const a=element('a','Flight models: completed work and unresolved results');a.href='flight.html#run-history-20261016';
      const b=element('a','Closing report: freeze and subsequent experiments');b.href='closing.html#research-record-20261016';
      links.append(a,document.createTextNode(' · '),b);record.append(links);
    }
    paragraph(record,data.boundary_note).className='rr-policy';
    paragraph(record,data.stop_note,'decisions');
    const provenance=element('details');provenance.id='record-sources';
    provenance.append(element('summary','Source notes and preserved qualifications'));
    paragraph(provenance,data.provenance);
    const sourceIDs=full?null:new Set(['freeze','chronology','run020','t042','t043','t053','decisions']);
    data.sources.filter(s=>!sourceIDs || sourceIDs.has(s.id)).forEach(source=>{
      const box=element('section',null,'rr-source');box.id='record-source-'+source.id;box.tabIndex=-1;
      box.append(element('h4',source.title));paragraph(box,source.kind).className='rr-kicker';
      paragraph(box,source.evidence);if(source.quote)box.append(element('blockquote',source.quote));paragraph(box,source.caveat);
      provenance.append(box);
    });
    const raw=element('a','Structured publication record (JSON)');raw.href=dataURL.href;
    provenance.append(raw);record.append(provenance);
    const subtitle=h1.nextElementSibling && h1.nextElementSibling.matches('p.sub')?h1.nextElementSibling:null;
    const originalSubtitle=subtitle && subtitle.textContent;
    if(subtitle){
      subtitle.dataset.originalIntroduction=originalSubtitle;
      subtitle.textContent=page==='satcom.html'?'The raw burst-log plots remain observational. The dated project-status record below is separately labeled model analysis.':
        'Updated 16 October 2026: completed native results and the SATCOM freeze are preserved; later revised-model work has its own outcomes and limits.';
    }
    (subtitle||h1).insertAdjacentElement('afterend',record);
    if(page!=='satcom.html'){
      const archive=element('aside',null,'rr-archive-label');
      archive.append(element('strong','Earlier published page material follows. '),document.createTextNode('It is retained as historical context, not silently promoted to the latest status of every model. Use the dated record above to distinguish the freeze, later experiments and unresolved connections.'));
      if(originalSubtitle){const d=element('details');d.append(element('summary','Original page introduction'),element('p',originalSubtitle));archive.append(d);}
      record.insertAdjacentElement('afterend',archive);
    }
    document.addEventListener('click',event=>{
      const a=event.target.closest && event.target.closest('a.rr-source-link');
      if(!a)return;
      const target=document.getElementById(a.hash.slice(1));
      if(target){let node=target;while(node){if(node.tagName==='DETAILS')node.open=true;node=node.parentElement;}}
    });
    window.addEventListener('hashchange',revealHash);revealHash();
  }
  const ready=document.readyState==='loading'?new Promise(resolve=>document.addEventListener('DOMContentLoaded',resolve,{once:true})):Promise.resolve();
  Promise.all([fetch(dataURL.href).then(response=>{if(!response.ok)throw new Error('Publication record HTTP '+response.status);return response.json();}),ready])
    .then(([data])=>render(data))
    .catch(error=>{console.error('Atlas publication record unavailable:',error);const h=document.querySelector('.wrap h1');if(h&&!document.getElementById('record-load-warning')){const p=element('p','The 16 October project-record addendum could not load. The older page content remains visible.','note');p.id='record-load-warning';h.insertAdjacentElement('afterend',p);}});
})();
