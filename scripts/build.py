"""Build the six-world portfolio from portable content and approved assets."""
from pathlib import Path
from html import escape as esc
import json, re, hashlib
from html_utils import Document
from case_order import ui_before_architecture
from case_presentation import visual_first, PRESENTATION

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'content/portfolio.json').read_text(encoding='utf-8'))
ASSET_VERSION={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()[:12] for name in ('style.css','app.js','contact.js')}
HOVER_FX_PREVIEW=(ROOT/'content/hover-fx-preview.enabled').exists()
PAGES=[
 dict(key='home',file='index.html',name='Home',world='earth',number='01',eyebrow='UI/UX design / Architecture / Development',title='I make complex<br>software feel simple.',copy='I lead UX architecture, design product interfaces, and build the UI that brings them to life. Applied AI helps me solve the hard problems.',action='Explore my work'),
 dict(key='history',file='work-history.html',name='Work History',world='mars',number='02',eyebrow='Experience / Leadership / Engineering',title='Experience,<br>applied.',copy='Two decades of turning complexity into working products. Leading teams, shaping experiences, and building what comes next.',action='Explore my experience'),
 dict(key='ui',file='portfolio.html',name='UI/UX Portfolio',world='ocean',number='03',eyebrow='Product design / Systems / Brand',title='Clarity at<br>every scale.',copy='UX architecture and interface design for products generating over $500 million in annual revenue.',action='Explore the portfolio'),
 dict(key='ai',file='creative-ai.html',name='Creative AI Portfolio',world='purple',number='04',eyebrow='Custom models / Visual worlds / Motion',title='Human vision.<br>Machine possibility.',copy='Custom models and new visual worlds. Hands-on practice with GPT, Grok, Claude, Midjourney, Stable Diffusion, Kling, and Seedance.',action='Enter the gallery'),
 dict(key='other',file='other-work.html',name='Other Work',world='yellow',number='05',eyebrow='Fiction / Film / Frequencies',title='Stories. Sound.<br>Something more.',copy='Published science-fiction author. Video, audio, and music producer. Different mediums. The same restless imagination.',action='Explore other work'),
 dict(key='contact',file='contact.html',name='Contact',world='city',number='06',eyebrow='Contact / Lawrence Railey',title="Let's connect.",copy='Contact Lawrence Railey about product design, AI engineering, video, audio, and voiceover services.',action='Contact details'),
]
LI='https://www.linkedin.com/in/lawrence-r-8537a535/'

def header(active):
    logo=(ROOT/'assets/brand/lr-monogram.svg').read_text(encoding='utf-8').strip()
    logo=logo.replace('role="img" aria-label="LR"', 'class="brand-mark" aria-hidden="true" focusable="false"')
    logo=logo.replace('<path ', '<path class="brand-rim" ', 1)
    links=''.join(f'<a href="{p["file"]}" data-nav-world="{"contact" if p["key"]=="contact" else p["world"]}"'+(' aria-current="page"' if p['key']==active else '')+f'>{p["name"]}</a>' for p in PAGES)
    return f'''<a class="skip" href="#main">Skip to content</a><header class="site-header"><a class="brand" href="index.html" aria-label="Lawrence Railey — home">{logo}<span>LAWRENCE RAILEY<small>UI/UX + AI Tech + Creative</small></span></a><button class="menu-toggle" aria-expanded="false" aria-controls="main-navigation"><span>Menu</span><i aria-hidden="true"></i></button><nav id="main-navigation" aria-label="Main navigation">{links}</nav></header>'''

def hero(p):
    world=p['world']
    hero_title=''.join(f'<span>{line}</span>' for line in p['title'].split('<br>'))
    hero_action='<a class="button hero-action" href="portfolio.html#portfolio-items">View UI/UX portfolio <span aria-hidden="true">&#8599;</span></a>' if p['key']=='home' else ''
    if p['key']=='ui':
        hero_action='<a class="button hero-action" href="#content">Explore <span aria-hidden="true">&#8595;</span></a>'
    if p['key']=='history':
        hero_action='<a class="button hero-action" href="assets/resume/Lawrence-Railey-Resume.pdf" download>Download résumé <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9Z"/><path d="M14 3v6h6M8 13h8M8 17h6"/></svg></a>'
    alt={'earth':'An ivory sanctuary across a quiet teal bay, framed by an ancient tree.','mars':'An astronaut overlooking a rust-red canyon and distant Greco Deco sanctuary.','ocean':'A sanctuary on an island, small ships on blue water, and a traveler on the shore.','purple':'A violet canyon and ivory sanctuary beneath a ringed planet.','yellow':'A golden landscape with wind turbines, a distant sanctuary, and a traveler.','city':'An ivory sanctuary and futuristic white city across a silver-blue waterfront, with a traveler in the foreground.'}[world]
    contact_hero = p['key']=='contact'
    hero_class = 'world-hero contact-hero' if contact_hero else 'world-hero'
    copy_class = 'hero-copy contact-hero-copy' if contact_hero else 'hero-copy'
    hero_body = contact_form() if contact_hero else f'<p class="hero-description">{p["copy"]}</p>{hero_action}'
    motion = f'<video class="hero-video" id="hero-motion" data-src="assets/worlds-video/{world}-4k.mp4" width="3840" height="2160" muted loop playsinline preload="none" disablepictureinpicture aria-hidden="true" tabindex="-1"></video>'
    return f'''<section class="{hero_class}" aria-labelledby="page-title"><picture class="hero-art" data-fallback="assets/worlds-4k/{world}-4k.png"><source type="image/webp" srcset="assets/worlds-web/{world}-1280.webp 1280w, assets/worlds-web/{world}-1920.webp 1920w, assets/worlds-web/{world}-3840.webp 3840w" sizes="(max-aspect-ratio: 16/9) 178vh, 100vw"><img src="assets/worlds-web/{world}-1920.webp" alt="{alt}" width="3840" height="2160" fetchpriority="high"></picture>{motion}<div class="hero-shade"></div><div class="{copy_class}"><p class="eyebrow"><span class="tiny-cross" aria-hidden="true">+</span>{p['eyebrow']}</p><h1 id="page-title">{hero_title}</h1>{hero_body}</div><div class="hero-bottom"><a class="scroll-link" href="#content"><span class="scroll-line" aria-hidden="true"></span>{p['action']}<span aria-hidden="true">↓</span></a><div class="hero-meta"><div class="world-index"><span>{p['number']} <span class="index-divider">/ {len(PAGES):02}</span></span><i aria-hidden="true"></i><span>{p['name']}</span></div></div></div></section>'''

def footer(active='home'):
    invitation = '<div class="footer-invitation"><p class="eyebrow">The next possibility</p><a href="contact.html">Let\'s make something<br>worth exploring. <span aria-hidden="true">↗</span></a></div>' if active != 'contact' else ''
    return f'''<footer class="site-footer">{invitation}<div class="footer-bottom"><a class="footer-logo" href="index.html" aria-label="Home"><img src="assets/brand/lr-monogram.svg" width="44" height="44" alt="LR"></a><span>© 2026 LAWRENCE RAILEY</span><div><a href="assets/resume/Lawrence-Railey-Resume.pdf" download>Résumé ↓</a><a href="{LI}" target="_blank" rel="noopener noreferrer">LinkedIn ↗</a><a href="#main">Back to top ↑</a></div></div></footer>'''

def lightbox():
    return '''<dialog class="lightbox" aria-label="Image gallery" aria-describedby="lightbox-caption"><div class="lightbox-toolbar"><span>LAWRENCE RAILEY / VISUAL ARCHIVE</span><button class="lightbox-close" aria-label="Close image viewer">Close ×</button></div><div class="lightbox-stage"><button class="lightbox-prev" aria-label="Previous image">←</button><img class="lightbox-image" alt=""><button class="lightbox-next" aria-label="Next image">→</button></div><div class="lightbox-bottom"><p id="lightbox-caption"></p><span class="lightbox-count" aria-live="polite"></span><a class="lightbox-original" target="_blank" rel="noopener noreferrer">Open original ↗</a></div></dialog>'''

def page(file,title,description,body,active='home',world='earth',compact=False):
    html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} | Lawrence Railey</title><meta name="description" content="{esc(description,quote=True)}"><meta name="theme-color" content="#080e13"><meta property="og:title" content="{esc(title,quote=True)} — Lawrence Railey"><meta property="og:description" content="{esc(description,quote=True)}"><link rel="icon" href="assets/brand/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="style.css?v={ASSET_VERSION['style.css']}"><link rel="stylesheet" href="diagrams.css"><script src="app.js?v={ASSET_VERSION['app.js']}" defer></script></head><body data-world="{world}" class="{'compact-page' if compact else ''}">{header(active)}<main id="main">{body}</main>{footer(active)}{lightbox()}</body></html>'''
    if HOVER_FX_PREVIEW:
        fx_version=hashlib.sha256((ROOT/'hover-fx.css').read_bytes()+(ROOT/'hover-fx.js').read_bytes()).hexdigest()[:12]
        html=html.replace('</head>', f'<link rel="stylesheet" href="hover-fx.css?v={fx_version}"><script src="hover-fx.js?v={fx_version}" defer></script></head>')
    if active == 'contact':
        html = html.replace('</head>', f'<script src="contact.js?v={ASSET_VERSION["contact.js"]}" defer></script></head>')
    (ROOT/file).write_text(html,encoding='utf-8')

def section_heading(kicker,title,aside=''):
    return f'<div class="section-heading"><div><p class="eyebrow">{kicker}</p><h2>{title}</h2></div>{aside}</div>'

def project_card(p, branded=False):
    if branded and p.get('stack'):
        layers=''.join(f'<img class="archive-layer archive-layer--{i}" src="{src}" loading="lazy" alt="{alt}">' for i,src,alt in [(3,p['stack'][2],'Reeves Import Motorcars website'),(2,p['stack'][1],'Kennards Hire interface'),(1,p['stack'][0],'The Melting Pot website')])
        return f'''<article class="project-card project-card--archive" data-category="archive"><a href="project-{p['slug']}.html"><div class="project-brand-image"><span class="brand-card-label">Selected archive</span><div class="archive-card-stack">{layers}</div><div class="brand-card-footer"><span>More brands. More experiences.</span><span aria-hidden="true">&#8599;</span></div></div><div class="project-caption"><h3>{p['title']}</h3><span class="project-arrow" aria-hidden="true">&#8599;</span></div><p class="project-summary">{p['summary']}</p></a></article>'''
    if branded and p.get('logo'):
        return f'''<article class="project-card project-card--brand" data-brand="{p['slug']}"><a href="project-{p['slug']}.html"><div class="project-brand-image"><span class="brand-card-label">{p['label']}</span><img class="project-brand-logo" src="{p['logo']}" loading="lazy" alt="{esc(p['title'],quote=True)}"><div class="brand-card-footer"><span>{p.get('role','Product design')}</span><span aria-hidden="true">&#8599;</span></div></div><div class="project-caption"><h3>{p['title']}</h3><span class="project-arrow" aria-hidden="true">&#8599;</span></div><p class="project-summary">{p['summary']}</p></a></article>'''
    return f'''<article class="project-card" data-category="{p['category']}"><a href="project-{p['slug']}.html"><div class="project-image"><img src="{p['image']}" loading="lazy" alt="{esc(p.get('image_alt',p['title']+' interface'),quote=True)}"><span class="image-corner" aria-hidden="true">↗</span></div><div class="project-caption"><div><p class="eyebrow">{p['label']}</p><h3>{p['title']}</h3></div><span class="project-arrow" aria-hidden="true">↗</span></div><p class="project-summary">{p['summary']}</p></a></article>'''

def filters(group,items,anchor=''):
    anchor_attr=f' id="{esc(anchor,quote=True)}"' if anchor else ''
    return '<div class="filter-bar"'+anchor_attr+' role="group" aria-label="Filter '+group+'">'+''.join(f'<button type="button" data-filter="{key}" aria-pressed="{str(i==0).lower()}">{name}</button>' for i,(key,name) in enumerate(items))+'</div>'

def home_content():
    nav=''.join(f'''<a class="world-link" href="{p['file']}"><img src="assets/worlds-web/{p['world']}-1280.webp" loading="lazy" alt=""><span class="world-link-number">{p['number']}</span><div><h3>{p['name']}</h3><span aria-hidden="true">↗</span></div></a>''' for p in PAGES[1:5])
    featured=''.join(project_card(p, branded=True) for p in DATA['projects'][:3])
    return f'''<div id="content" class="content-shell"><section class="section">{section_heading('01 / Selected work','Built for the real world.','<a class="text-link" href="portfolio.html">All UI/UX work ↗</a>')}<div class="project-grid">{featured}</div></section><section class="intro-section"><p class="eyebrow">02 / UX Leadership. Built to work.</p><div><h2>From complex workflows<br>to clear experiences.</h2><p>I turn complex product requirements into software people can use with confidence. Research, UX architecture, interface design, front-end development, and applied AI connect the strategy to the working product.</p></div></section><section class="section">{section_heading('03 / Explore the practice','A different world.<br>The same curiosity.')}<div class="world-links">{nav}</div></section></div>'''

def history_content():
    return f'''<div id="content" class="content-shell"><section class="section">{section_heading('The professional story','Leadership with<br>hands-on depth.')}<div class="career-history">{DATA['history']}</div></section></div>'''

def portfolio_content():
    by_slug={p['slug']:p for p in DATA['projects']}
    cards=''.join(project_card(by_slug[slug],branded=True) for slug in DATA['portfolio_order'])
    diagrams=''.join(f'<a href="project-{slug}.html#{anchor}"><span>{number}</span><div><h3>{title}</h3><p>{copy}</p></div><b aria-hidden="true">↗</b></a>' for number,slug,anchor,title,copy in [
      ('01','cox','cox-experience','Cox Automotive','Research, product architecture, and AI in dealership workflows.'),
      ('02','bagsid','bags-platform-title','BagsID','Connected applications, identity, and a shared design system.'),
      ('03','lending','loan-ai-title','LoanAI','Purpose-built AI and the architecture of loan origination.'),
      ('04','fullpath','fp-data-title','Fullpath × Cox','Integrating customer intelligence into an established CRM.')])
    return f'''<div id="content" class="content-shell"><section class="section">{section_heading('Selected engagements','The experience.<br>And everything behind it.')}<p class="section-lead">Product interfaces, design systems, architecture, workflow diagrams, websites, and marketing — brought together in the original case studies.</p><div class="project-grid portfolio-brand-grid" id="portfolio-items">{cards}</div></section><section class="section architecture-index" id="architecture">{section_heading('Beneath the interface','Systems made visible.')}<div class="architecture-links">{diagrams}</div></section></div>'''

def creative_content():
    figures=[]
    for i,a in enumerate(DATA['art'],1):
        tags=' '.join(a['categories'])
        figures.append(f'''<figure class="artwork" data-category="{tags}"><a href="{a['image']}" data-lightbox data-title="{esc(a['title'],quote=True)}" aria-label="Enlarge {esc(a['title'],quote=True)}"><img src="{a['thumb']}" alt="{esc(a['alt'],quote=True)}" width="{a['width']}" height="{a['height']}" loading="lazy" decoding="async"><span class="image-corner" aria-hidden="true">+</span></a><figcaption><span>{a['title']}</span><span>{i:02}</span></figcaption></figure>''')
    categories=[('all','All images'),('worlds','Worlds & architecture'),('characters','Characters'),('byzantium','Cyber Byzantium'),('transport','Transport'),('music','Music & posters'),('covers','Cover art')]
    return f'''<div id="content" class="content-shell"><section class="section">{section_heading('Creative AI / The visual archive','A little further<br>than the familiar.')}<div class="ai-intro"><p>Original visual direction, custom Stable Diffusion checkpoints and extensions, and a production workflow spanning language, image, and video models. Higgsfield brings Kling and Seedance into my video workflow.</p><div class="creative-tools"><p class="eyebrow">Models &amp; creative tools</p><div class="platforms" aria-label="Models and creative tools"><span>GPT</span><span>Grok</span><span>Claude</span><span>Midjourney</span><span>Stable Diffusion</span><span>Kling</span><span>Seedance</span></div></div></div>{filters('artwork',categories,'gallery')}<div class="art-grid filter-grid">{''.join(figures)}</div><p class="filter-status" role="status" aria-live="polite">{len(figures)} images</p></section><section class="creative-note"><p class="eyebrow">Beyond the still image</p><h2>One idea. Many mediums.</h2><p>The same visual practice extends into book covers, video, animation, and the identity around my music.</p><a class="text-link" href="other-work.html">Explore the other work &rarr;</a></section></div>'''


def florida_feature():
    root=Document(DATA['florida']).root
    figures=root.find(lambda n:n.tag=='figure')
    wanted=['assets/creative/cure-after-party-thumb.webp','assets/creative/halloween-2023-thumb.webp','assets/creative/florida-regime-flyer.webp','assets/creative/surviving-the-storm-thumb.webp','assets/portfolio/logobooth.webp']
    selected=[next(f for f in figures if any(im.attrs.get('src')==path for im in f.find(lambda n:n.tag=='img'))) for path in wanted]
    for i,figure in enumerate(selected):
        figure.attrs['id']=f'florida-feature-{i+1}'
    return f'''<div class="florida-brand-feature" id="florida-brand"><div class="florida-feature-intro"><div class="florida-logo-frame"><img src="assets/FR3.webp" alt="Florida Regime logo against a blue starry sky and palm silhouettes" width="1024" height="1024" loading="lazy" decoding="async"></div><div><p class="eyebrow">Florida Regime / The visual identity</p><h3>A sound with its own signature.</h3><p>I built the brand around the music: a recognizable identity across the logo, business cards, booth, flyers, and website. Tropical color and atmospheric artwork connect the live performance with its digital presence.</p></div></div><div class="gallery florida-showcase" aria-label="Florida Regime branding and promotional artwork">{''.join(f.html() for f in selected)}</div></div>'''


def bagsid_film():
    body=next(p['body'] for p in DATA['projects'] if p['slug']=='bagsid')
    film=re.search(r'<video\b.*?</video>', body, re.S)
    if not film:
        raise ValueError('The BagsID marketing film is missing from the case study')
    return film.group()


def other_content():
    production = section_heading('Video production / Voiceover', 'Picture. Voice. Impact.')
    return f'''<div id="content" class="content-shell"><nav class="section-nav" aria-label="Other work sections"><a href="#writing">Fiction &amp; worldbuilding ↓</a><a href="#music">Music &amp; audio ↓</a><a href="#production">Video &amp; voiceover ↓</a></nav><section class="section writing-section" id="writing">{DATA['writing']}</section><section class="section music-section" id="music">{DATA['music']}{florida_feature()}<div class="audio-player" id="listen"><p class="eyebrow">Listen / Florida Regime — Trance: 001</p><iframe title="Florida Regime Trance 001 on Mixcloud" loading="lazy" width="100%" height="180" src="https://www.mixcloud.com/widget/iframe/?hide_cover=1&amp;feed=%2FFloridaRegime%2Ftrance-001%2F"></iframe></div></section><section class="section production-section" id="production">{production}<div class="two-col production-copy"><div><h3>Video that makes the story clear.</h3><p>I produce marketing films and product demonstrations, bringing visuals, editing, sound, and narration together. My BagsID work includes video for the website and presentations at national and international conferences.</p></div><div><h3>A voice for the work.</h3><p>I also offer voiceover services for marketing videos, product explainers, and audiobooks, alongside audio editing and mastering. I narrated the BagsID film below.</p><a class="text-link" href="contact.html">Discuss video or voiceover work →</a></div></div><figure class="project-media production-film">{bagsid_film()}<figcaption><span>BagsID / Marketing film</span><span>Video production &amp; narration by Lawrence Railey</span></figcaption></figure><a class="text-link" href="project-bagsid.html">Explore the BagsID project ↗</a></section></div>'''


def contact_form():
    return (ROOT/'content/contact-form.html').read_text(encoding='utf-8').replace('__LINKEDIN__', LI)


def contact_content():
    return '''<div id="content" class="content-shell"><section class="contact-details" aria-label="Direct contact information"><div><p class="eyebrow">Email</p><a href="mailto:lawrence@lawrencerailey.com">lawrence@lawrencerailey.com</a></div><div><p class="eyebrow">Phone</p><a href="tel:+18134338197">813-433-8197</a></div><div><p class="eyebrow">Address</p><address>2918 Timberlee Road<br>Wimauma, Florida 33598</address></div></section></div>'''


for p,content in zip(PAGES,[home_content,history_content,portfolio_content,creative_content,other_content,contact_content]):
    page(p['file'],p['name'],re.sub('<[^>]+>',' ',p['copy']),hero(p)+content(),p['key'],p['world'])

for p in DATA['projects']:
    body=visual_first(ui_before_architecture(p['body'], p['slug']), p['slug'])
    if p['slug']=='earlier':
        by_slug={item['slug']:item for item in DATA['projects']}
        archive_cards=''.join(project_card(by_slug[slug]) for slug in DATA['archive_projects'])
        body=f'<section class="archive-engagements"><p class="eyebrow">More selected engagements</p><h2>Products, brands, and digital experiences.</h2><div class="project-grid">{archive_cards}</div></section><section class="archive-screens"><h2>Earlier websites &amp; interfaces.</h2>{body}</section>'
    site_action=f'<div class="case-actions"><a class="button button-secondary" href="{p["site_url"]}" target="_blank" rel="noopener noreferrer">{p["site_label"]} <span aria-hidden="true">&#8599;</span></a></div>' if p.get('site_url') else ''
    # Keep the source architecture intact, and give the index stable anchor targets.
    aliases={'cox':'cox-research','bagsid':'bags-platform','lending':'loan-architecture','fullpath':'fp-integration'}
    anchor=f'<span id="{aliases[p["slug"]]}" class="anchor-target"></span>' if p['slug'] in aliases and f'id="{aliases[p["slug"]]}"' not in body else ''
    intro_copy=PRESENTATION.get(p['slug'], {}).get('ownership', p['detail'])
    case_class=' case-page--visual' if p['slug'] in PRESENTATION else ''
    content=f'''<div class="content-shell case-page{case_class}"><a class="back-link" href="portfolio.html">← UI/UX Portfolio</a><header class="case-intro"><p class="eyebrow">{p['label']}</p><h1>{p['title']}</h1><p>{intro_copy}</p>{site_action}</header><div class="case-content">{anchor}{body}</div><a class="end-link text-link" href="portfolio.html">← Back to all UI/UX work</a></div>'''
    page(f'project-{p["slug"]}.html',p['title'],p['detail'],content,'ui','ocean',True)

# Florida Regime now lives entirely in Other Work. Remove stale generated output.
(ROOT/'project-florida.html').unlink(missing_ok=True)

for file,target in [('ai-gallery.html','creative-ai.html'),('project-creative-ai.html','creative-ai.html'),('extras.html','other-work.html'),('project-clinical.html','project-healthesystems.html#clinical'),('project-jurne.html','project-healthesystems.html#jurne'),('project-vertice.html','project-healthesystems.html#vertice')]:
    (ROOT/file).write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url={target}"><title>Continue to portfolio</title></head><body><a href="{target}">Continue to portfolio</a></body></html>',encoding='utf-8')
page('404.html','Page not found','Return to Lawrence Railey’s portfolio.','<div class="content-shell contact-page"><p class="eyebrow">404 / Off the map</p><h1>A different route.</h1><a class="button" href="index.html">Return home →</a></div>',compact=True)
print(f'Built {len(list(ROOT.glob("*.html")))} pages.')
