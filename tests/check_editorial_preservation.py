"""Compare rendered table numbers and protected artifacts with the recovered baseline."""
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess

BASELINE = 'e79b34ea61f207ab8eb86101bdc314a5788579c9'
class TableNumbers(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = False
        self.buffer = ''
        self.numbers = []
    def handle_starttag(self, tag, attrs):
        if tag in ('td', 'th'):
            self.active = True
            self.buffer = ''
    def handle_data(self, data):
        if self.active:
            self.buffer += data
    def handle_endtag(self, tag):
        if tag in ('td', 'th') and self.active:
            self.numbers.extend(re.findall(r'[-−+]?\d+(?:[.,:]\d+)*', self.buffer))
            self.active = False

def baseline(path):
    return subprocess.check_output(['git', 'show', f'{BASELINE}:{path}'])

def check():
    count = 0
    for path in sorted(Path('.').glob('*.html')):
        old, new = TableNumbers(), TableNumbers()
        old.feed(baseline(path).decode())
        new.feed(path.read_text())
        assert old.numbers == new.numbers, f'Numeric table changes: {path}'
        count += len(old.numbers)
    for path in ('src/assessment_body.html', 'assessment.html', 'flight-lab/assets/data.js'):
        assert baseline(path) == Path(path).read_bytes(), f'Protected artifact changed: {path}'
    shell = Path('common.js').read_text()
    assert '<span>FUEL EXHAUSTED</span><output>00:17:29' not in shell
    assert 'case-dependent' in shell
    assert 'negated or unavailable' not in shell
    canonical = Path('src/canonical_body.html').read_text()
    assert '>observations only<' not in canonical
    assert 'ten derived BTO rings' in canonical
    assert 'they are not a full-year timestep convergence test' in Path('src/drift3_body.html').read_text()
    assert 'These offsets are not distances along the arc' in Path('src/drift4_body.html').read_text()
    print(f'PASS: {count} numeric table tokens and protected artifacts preserved; editorial scope assertions pass.')
if __name__ == '__main__':
    check()
