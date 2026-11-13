"""Present selected case studies as authored visual work, then supporting evidence."""
import json
from pathlib import Path
from html import escape
from html_utils import Document, Node

PRESENTATION = json.loads((Path(__file__).resolve().parents[1] / 'content/case-presentation.json').read_text(encoding='utf-8'))


def fragment(markup):
    return Document(markup).root.children[0]


def visual_first(body, slug):
    config = PRESENTATION.get(slug)
    if not config:
        return body
    root = Document(body).root
    if slug == 'lending':
        examples = root.find(lambda n: n.has('case-ui-examples'))[0]
        intro = next(n for n in examples.children if isinstance(n, Node) and n.has('project-copy'))
        desktop = next(n for n in examples.children if isinstance(n, Node) and n.attrs.get('id') == 'loanai-desktop')
        examples.children.remove(intro)
        examples.children.insert(examples.children.index(desktop) + 1, intro)
    if slug == 'healthesystems':
        gallery = next(n for n in root.children if isinstance(n, Node) and n.has('gallery'))
        root.children.remove(gallery)
        root.children.insert(0, gallery)
    galleries = root.find(lambda n: n.has('gallery'))
    assert len(galleries) == len(config['galleries']), slug
    for gallery, spec in zip(galleries, config['galleries']):
        figures = [n for n in gallery.children if isinstance(n, Node) and n.tag == 'figure']
        if spec.get('first'):
            first = next(f for f in figures if any(spec['first'] in im.attrs.get('src', '') for im in f.find(lambda n: n.tag == 'img')))
            gallery.children.remove(first)
            gallery.children.insert(0, first)
        for figure in figures:
            img = figure.find(lambda n: n.tag == 'img')[0]
            key = img.attrs.get('src', '').split('/')[-1]
            entry = spec['captions'].get(key)
            assert entry, (slug, key)
            caption = fragment(f'<figcaption><span class="case-caption-context">{escape(spec["status"])}</span><strong>{escape(entry[0])}</strong><p>{escape(entry[1])}</p></figcaption>')
            figure.children = [n for n in figure.children if not isinstance(n, Node) or n.tag != 'figcaption'] + [caption]
            caption.parent = figure
        parent = gallery.parent
        # Keep a short heading before the pictures; move explanatory prose below.
        before = parent.children[:parent.children.index(gallery)]
        copies = [n for n in before if isinstance(n, Node) and n.has('project-copy') and not n.has('case-visual-context')]
        for copy in copies:
            prose = [n for n in copy.children if isinstance(n, Node) and n.tag not in ('h2', 'h3') and not n.has('eyebrow')]
            if prose:
                copy.children = [n for n in copy.children if n not in prose]
                details = Node('div', [('class', 'project-copy case-visual-context')], parent)
                details.children = prose
                for n in prose:
                    n.parent = details
                parent.children.insert(parent.children.index(gallery) + 1, details)
        if parent.has('combined-project-section'):
            prose = [n for n in before if isinstance(n, Node) and n.tag == 'p' and not n.has('eyebrow')]
            if prose:
                parent.children = [n for n in parent.children if n not in prose]
                offset = parent.children.index(gallery) + 1
                parent.children[offset:offset] = prose
        label = fragment(f'<div class="case-ownership"><span><span class="tiny-cross" aria-hidden="true">+</span>{escape(spec["status"])}</span><p>{escape(spec["ownership"])}</p></div>')
        label.parent = parent
        parent.children.insert(parent.children.index(gallery), label)
    return root.html()
