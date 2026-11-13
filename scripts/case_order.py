"""Put tangible UI examples ahead of the four architecture narratives."""
from html_utils import Document, Node


def ui_before_architecture(body, slug):
    story_classes = {'cox': 'cox-story', 'bagsid': 'bags-story', 'lending': 'loan-story', 'fullpath': 'fp-story'}
    if slug not in story_classes:
        return body
    root = Document(body).root
    story = next(n for n in root.children if isinstance(n, Node) and n.has(story_classes[slug]))
    examples = [n for n in root.children if isinstance(n, Node) and n is not story]
    if slug == 'bagsid':
        # Website and brand first, then all product UI, then video and architecture.
        website = next(i for i, n in enumerate(examples) if n.has('project-copy') and 'THE CURRENT WEBSITE' in n.text())
        website_pair = examples[website:website + 2]
        examples = website_pair + [n for n in examples if n not in website_pair]
        videos = [n for n in examples if n.find(lambda child: child.tag == 'video')]
        examples = [n for n in examples if n not in videos] + videos
    gallery_section = Node('section', [('class', 'case-ui-examples'), ('id', f'{slug}-ui'), ('aria-label', 'UI and visual examples')], story)
    gallery_section.children = examples
    for node in examples:
        node.parent = gallery_section
    # The existing overview and scale metrics stay first; diagrams follow examples.
    first_chapter = next(n for n in story.children if isinstance(n, Node) and n.tag == 'section')
    intro = next((n for n in story.children if isinstance(n, Node) and n.has('bags-evidence-intro')), None)
    if intro:
        story.children.remove(intro)
        gallery_section.children.insert(0, intro)
        intro.parent = gallery_section
    nav = next((n for n in story.children if isinstance(n, Node) and n.tag == 'nav'), None)
    ui_link = Document(f'<a href="#{slug}-ui">UI examples ↓</a>').root.children[0]
    if nav:
        nav.children.insert(0, ui_link)
        ui_link.parent = nav
    else:
        target = first_chapter.attrs.get('id') or first_chapter.attrs['aria-labelledby']
        nav = Document(f'<nav class="case-section-nav" aria-label="Case study sections"><a href="#{slug}-ui">UI examples ↓</a><a href="#{target}">Architecture &amp; workflow ↓</a></nav>').root.children[0]
        story.children.insert(story.children.index(first_chapter), nav)
        nav.parent = story
    # Screens establish the work before the overview, scale, and process narrative.
    story.children.insert(0, gallery_section)
    # Keep legacy architecture links attached to the architecture, not page start.
    aliases = {'bagsid': ('bags-platform', 'bags-platform-title'), 'lending': ('loan-architecture', 'loan-ai-title'), 'fullpath': ('fp-integration', 'fp-journey-title')}
    if slug in aliases:
        alias, labelledby = aliases[slug]
        if not story.find(lambda n: n.attrs.get('id') == alias):
            target = next(n for n in story.children if isinstance(n, Node) and n.attrs.get('aria-labelledby') == labelledby)
            target.attrs['id'] = alias
    return story.html()
