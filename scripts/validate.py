"""Check generated local routes, assets, anchors and essential page structure."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from collections import Counter
import json,re
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__(); self.refs=[]; self.ids=[]; self.h1=0; self.mains=0; self.images=[]; self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag=='h1': self.h1+=1
        if tag=='main': self.mains+=1
        if tag=='img': self.images.append(a)
        for attr in ('src','href','poster','data-thumb','data-src','data-fallback'):
            if a.get(attr): self.refs.append(a[attr])
        for candidate in a.get('srcset','').split(','):
            if candidate.strip(): self.refs.append(candidate.strip().split()[0])
pages={p.name:Page(p.read_text(encoding='utf-8')) for p in ROOT.glob('*.html')}
errors=[]; refs=0
for filename,doc in pages.items():
    for ident,count in Counter(doc.ids).items():
        if count>1: errors.append(f'{filename}: duplicate id {ident}')
    for ref in doc.refs:
        parts=urlsplit(ref)
        if parts.scheme or ref.startswith('//'): continue
        name=unquote(parts.path)
        if name and not (ROOT/name).is_file(): errors.append(f'{filename}: missing {name}'); continue
        target=pages.get(name or filename)
        if parts.fragment and target and unquote(parts.fragment) not in target.ids:
            errors.append(f'{filename}: missing anchor {ref}')
        refs+=1
    if doc.mains and doc.h1!=1: errors.append(f'{filename}: {doc.h1} h1 headings')
    for im in doc.images:
        if 'alt' not in im: errors.append(f'{filename}: missing image alt')
    text=(ROOT/filename).read_text(encoding='utf-8')
    if re.search(r'[\x00-\x08\x0b-\x1f\ufffd]',text): errors.append(f'{filename}: malformed text encoding')
for world in ('earth','mars','ocean','purple','yellow','city'):
    for width in (1280,1920,3840):
        if not (ROOT/f'assets/worlds-web/{world}-{width}.webp').is_file(): errors.append(f'missing {world}/{width}')
print(json.dumps({'pages':len(pages),'local_references_checked':refs,'errors':errors},indent=2))
raise SystemExit(bool(errors))
