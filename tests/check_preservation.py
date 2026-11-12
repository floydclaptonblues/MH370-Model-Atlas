#!/usr/bin/env python3
"""Check editorial/UI scope against the published pre-recovery Atlas baseline."""
from pathlib import Path
from html.parser import HTMLParser
import subprocess, hashlib, re, json
BASE='e79b34ea61f207ab8eb86101bdc314a5788579c9'
ROOT=Path(__file__).resolve().parents[1]
def original(path):
    return subprocess.check_output(['git','show',f'{BASE}:{path}'],cwd=ROOT)
class Cells(HTMLParser):
    def __init__(self):
        super().__init__(); self.depth=0; self.buf=[]; self.cells=[]
    def handle_starttag(self,tag,attrs):
        if tag=='td': self.depth+=1; self.buf=[]
    def handle_endtag(self,tag):
        if tag=='td' and self.depth:
            self.cells.append(' '.join(''.join(self.buf).split())); self.depth-=1
    def handle_data(self,data):
        if self.depth: self.buf.append(data)
def numeric_cells(text):
    p=Cells();p.feed(text)
    return [re.findall(r'[-+−]?\d+(?:[.,]\d+)*',s) for s in p.cells if re.search(r'\d',s)]
checks=[]
for file in ['flight-lab/assets/data.js','assessment.html','src/assessment_body.html','src/arc7_demo_body.html','src/arc7_demo.js','arc7-demo.css']:
    same=original(file)==(ROOT/file).read_bytes()
    checks.append({'file':file,'check':'byte_identity','passed':same})
count=0
for p in sorted(ROOT.glob('*.html')):
    old=numeric_cells(original(p.name).decode());new=numeric_cells(p.read_text())
    count+=len(old)
    checks.append({'file':p.name,'check':'numeric_table_cells','passed':old==new,'original_count':len(old),'current_count':len(new)})
report={'baseline':BASE,'numeric_table_cells_checked':count,'checks':checks,'passed':all(x['passed'] for x in checks)}
print(json.dumps(report,indent=2))
raise SystemExit(0 if report['passed'] else 1)
