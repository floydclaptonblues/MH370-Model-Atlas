#!/usr/bin/env python3
"""Check static local file links in generated root pages; external URLs are not fetched."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
import json
ROOT=Path(__file__).resolve().parents[1]
class Links(HTMLParser):
    def __init__(self): super().__init__();self.links=[]
    def handle_starttag(self,tag,attrs):
        for k,v in attrs:
            if k in ('href','src') and v:self.links.append(v)
missing=[];count=0
for page in ROOT.glob('*.html'):
    p=Links();p.feed(page.read_text())
    for link in p.links:
        u=urlsplit(link)
        if u.scheme or u.netloc or not u.path:continue
        count+=1
        target=ROOT/unquote(u.path.lstrip('/')) if u.path.startswith('/') else page.parent/unquote(u.path)
        if not target.exists(): missing.append({'page':page.name,'link':link})
print(json.dumps({'local_file_links_checked':count,'missing':missing,'passed':not missing},indent=2))
raise SystemExit(bool(missing))
