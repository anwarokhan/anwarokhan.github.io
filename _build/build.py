"""Builds the static pages for anwarokhan.github.io.
Edit the content below, then run:  python3 _build/build.py
(The folder starts with an underscore, so GitHub Pages does not publish it.)"""
import json, html, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, '_build', 'data.json')))
WP = 'https://spfmakerclub.wordpress.com/'
UP = WP + 'wp-content/uploads/'
e = html.escape
import time
VER = str(int(time.time()))

NAV = [('index.html', 'Home'), ('work.html', 'Work'), ('photographs.html', 'Photography'),
       ('notebook.html', 'Notebook'), ('videos.html', 'Videos'), ('about.html', 'About'), (WP, 'Maker Club')]

def page(fname, title, body, desc='Projects, photography and notes by Anwar Khan.'):
    nav = ''.join(f'<a href="{h}"{" aria-current=\"page\"" if h == fname else ""}{" class=\"ext\"" if h.startswith("http") else ""}>{t}</a>' for h, t in NAV)
    doc = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css?v={VER}"></head>
<body><a class="skip" href="#main">Skip to content</a>
<header class="site-head"><div class="wrap"><a class="mark" href="index.html">Anwar <span>Khan</span></a>
<button class="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button>
<nav class="nav" id="nav" aria-label="Main">{nav}</nav></div></header>
<main id="main">{body}</main>
<footer class="site-foot"><div class="wrap"><div>Anwar Khan · Atholton High School, Class of 2027<br>
<a href="mailto:spfmakerclub@gmail.com">spfmakerclub@gmail.com</a></div>
<div><a href="assets/anwar-khan-photography-portfolio.pdf">Photography portfolio (PDF)</a> &nbsp; <a href="{WP}">SPF Maker Club</a> &nbsp; <a href="https://www.thingiverse.com/AcidicCane/designs">Thingiverse</a> &nbsp; <a href="https://grabcad.com/anwar.o.khan-1">GrabCAD</a> &nbsp; <a href="https://atholton-electronics-club.vercel.app/">Electronics Club</a></div></div></footer>
<div class="lightbox" role="dialog" aria-modal="true" aria-label="Photo viewer"><button type="button">Close</button><figure><img alt=""><figcaption></figcaption></figure></div>
<script src="site.js?v={VER}"></script></body></html>'''
    open(os.path.join(ROOT, fname), 'w').write(doc)

def zoom(src, alt, cap='', cls=''):
    return f'<figure class="{cls}" data-full="{e(src)}" data-caption="{e(cap or alt)}"><img src="{e(src)}" alt="{e(alt)}" loading="lazy">{f"<figcaption>{cap}</figcaption>" if cap else ""}</figure>'

# ---------------- projects ----------------
P = json.load(open(os.path.join(ROOT, '_build', 'projects.json')))

def project_block(p):
    return f'''<article class="project" id="{p['id']}">
<div class="project-media"><img src="{p['img']}" alt="{e(p['alt'])}" loading="lazy"></div>
<div><p class="kind">{e(p['kind'])}</p><h2>{e(p['title'])}</h2>
{''.join(f'<p>{x}</p>' for x in p['text'])}
{('<div class="project-gallery">' + ''.join(zoom(g, c, '', '') for g, c in p['gallery']) + '</div>') if p.get('gallery') else ''}
<div class="link-row"><a class="btn big" href="{p['url']}">Read the full build journal</a>{''.join(f'<a class="btn ghost" href="{u}">{e(t)}</a>' for u,t in p.get('models',[]))}</div></div></article>'''

page('work.html', 'Work · Anwar Khan', f'''<div class="wrap">
<section class="page-head"><h1>Work</h1><p class="lede">Everything I've built since I took over SPF Maker Club in 2023: my own projects, a team project with the Electronics Club, and software from my internship. Each one has a full build journal on the Maker Club site with the photos, calculations, failures and fixes.</p></section>
{''.join(project_block(p) for p in P)}
<section class="club"><div><h2>Want the whole story?</h2><p>Every project above has a full build journal on SPF Maker Club, plus the club's older projects from before I took over.</p></div><a class="btn big yellow" href="{WP}blog/">Browse all build journals</a></section></div>''')

# ---------------- photography ----------------
from PIL import Image
def dims(s):
    try:
        w,h=Image.open(os.path.join(ROOT,s)).size; return f'width="{w}" height="{h}"'
    except Exception: return ''
PH = D['photos_ranked']
filters = [('all', 'All'), ('cars', 'Motorsport'), ('city', 'City'), ('outdoors', 'Outdoors'), ('sports', 'Sports'), ('film', 'Film'), ('digital', 'Digital'), ('edits', 'Composites')]
wall = ''.join(
    f'<figure data-full="{e(s)}" data-caption="{e(c)}" data-tags="{e(t)}"><img src="{e(s)}" {dims(s)} alt="{e(c.split(":")[0])}" loading="lazy"><figcaption><b>{e(c.split(":")[0])}</b>{(" · " + e(m)) if m else ""}</figcaption></figure>'
    for s, c, t, m in PH)
page('photographs.html', 'Photography · Anwar Khan', f'''<div class="wrap">
<section class="page-head ph-head"><div><h1>Photography</h1><p class="lede">Cars at the track, city streets, the water, soccer, and Loki. I shoot film and digital. The strongest frames are first.</p>
<p>My portfolio collects ten of my favorite photographs from 2023 to 2025, each with a short note on how and why I took it.</p>
<div class="link-row"><a class="btn" href="assets/anwar-khan-photography-portfolio.pdf">View my portfolio (PDF)</a><a class="btn ghost" href="assets/anwar-khan-photography-portfolio.pdf" download>Download PDF</a></div></div>
<a class="ph-cover" href="assets/anwar-khan-photography-portfolio.pdf" aria-label="Open my photography portfolio (PDF)"><img src="assets/portfolio-cover.jpg" alt="Cover of my photography portfolio"><span>Photography portfolio · PDF</span></a></section>

<div class="filters" role="group" aria-label="Filter photos">{''.join(f'<button type="button" data-filter="{k}" aria-pressed="{"true" if k=="all" else "false"}">{v}</button>' for k,v in filters)}</div>
<div class="wall">{wall}</div></div>''', 'Film and digital photography by Anwar Khan.')

# ---------------- notebook ----------------
N = json.load(open(os.path.join(ROOT, '_build', 'notebook.json')))
def entry(n):
    strip = ''.join(zoom(s, c, c) for s, c in n.get('photos', []))
    return f'''<article class="entry" id="{n['id']}"><div class="when">{n['when']}<small>{n.get('where','')}</small></div>
<div><h2>{e(n['title'])}</h2>{''.join(f'<p>{x}</p>' for x in n['text'])}{f'<div class="strip">{strip}</div>' if strip else ''}</div></article>'''
page('notebook.html', 'Notebook · Anwar Khan', f'''<div class="wrap">
<section class="page-head"><h1>Notebook</h1><p class="lede">The things that happened outside the lab: trips, races, injuries, classes, and the people I did them with. Newest first.</p></section>
{''.join(entry(n) for n in N)}
<section class="club"><div><h2>The build side</h2><p>For the projects themselves, every build has a full journal on SPF Maker Club.</p></div><a class="btn big yellow" href="{WP}blog/">Read the build journals</a></section></div>''')

# ---------------- videos ----------------
V = json.load(open(os.path.join(ROOT, '_build', 'videos.json')))
def vid(v):
    if v.get('youtube'):
        m = f'<iframe src="https://www.youtube-nocookie.com/embed/{v["youtube"]}" title="{e(v["title"])}" allowfullscreen loading="lazy"></iframe>'
    elif v.get('vimeo'):
        m = f'<iframe src="https://player.vimeo.com/video/{v["vimeo"]}" title="{e(v["title"])}" allowfullscreen loading="lazy"></iframe>'
    else:
        m = f'<video controls playsinline preload="none" poster="{v["poster"]}"{" muted" if v.get("muted") else ""}><source src="{v["src"]}" type="video/mp4"></video>'
    return f'<div class="vid">{m}<h3>{e(v["title"])}</h3><p>{e(v["meta"])}</p></div>'
secs = ''
for group in V:
    secs += f'<section class="section"><div class="section-head"><h2>{e(group["group"])}</h2></div><div class="vid-grid">{"".join(vid(v) for v in group["items"])}</div></section>'
page('videos.html', 'Videos · Anwar Khan', f'''<div class="wrap"><section class="page-head"><h1>Videos</h1><p class="lede">Project films, tests, and clips from the track.</p></section>{secs}</div>''')

# ---------------- about ----------------
A = json.load(open(os.path.join(ROOT, '_build', 'about.json')))
albums = ''
for al in A['albums']:
    albums += f'<section class="section" id="{al["id"]}"><div class="section-head"><h2>{e(al["title"])}</h2></div>{"".join(f"<p>{x}</p>" for x in al.get("text", []))}<div class="strip">{"".join(zoom(s, c, c) for s, c in al["photos"])}</div></section>'
facts = ''.join(f'<li><b>{e(k)}</b><span>{v}</span></li>' for k, v in A['facts'])
page('about.html', 'About · Anwar Khan', f'''<div class="wrap">
<section class="page-head about-grid"><div><h1>About me</h1>{''.join(f'<p>{x}</p>' for x in A['intro'])}
<ul class="facts">{facts}</ul></div>
<figure class="portrait"><img src="{A['portrait']}" alt="Me with my cat Loki curled up against my shoulder"><figcaption>Me and Loki on the couch, October 2026.</figcaption></figure></section>
{albums}
<section class="club"><div><h2>See what I'm building</h2><p>My build journals, from the motion simulator to the go-kart, are on the SPF Maker Club site.</p></div><a class="btn big yellow" href="{WP}">Visit SPF Maker Club</a></section></div>''')

# ---------------- home ----------------
H = A['home']
mini = ''.join(f'''<div class="mini"><a href="work.html#{p['id']}"><div class="thumb"><img src="{p['img']}" alt="{e(p['alt'])}" loading="lazy"></div><h3>{e(p['title'])}</h3><p>{e(p['short'])}</p></a></div>''' for p in P[:6])
notes = ''.join(f'''<div class="mini"><a href="notebook.html#{n['id']}"><div class="thumb"><img src="{n['photos'][0][0] if n.get('photos') else n.get('cover','')}" alt="" loading="lazy"></div><h3>{e(n['title'])}</h3><p>{re.sub('<[^>]+>','',n['when'])}</p></a></div>''' for n in [x for x in N if x.get('photos')][:3])
photos = ''.join(f'<figure data-full="{e(s)}" data-caption="{e(c)}"><img src="{e(s)}" alt="{e(c.split(":")[0])}" loading="lazy"></figure>' for s, c, t, m in PH[:6])
page('index.html', 'Anwar Khan', f'''<div class="wrap">
<section class="hero"><h1>Anwar Khan</h1><div class="stripes" aria-hidden="true"><i></i><i></i></div>
<div class="hero-grid"><div>{''.join(f'<p class="lede">{x}</p>' for x in H['intro'])}
<div class="link-row"><a class="btn big" href="work.html">See my projects</a><a class="btn ghost" href="about.html">More about me</a></div></div>
<figure class="hero-photo"><img src="{H['photo']}" alt="{e(H['photo_alt'])}"><figcaption>{H['photo_cap']}</figcaption></figure></div></section>
<section class="club"><div><h2>SPF Maker Club</h2><p>The full build journals live on the Maker Club site, which I've run since January 2023: every calculation, failed print and fix, project by project.</p></div><a class="btn big yellow" href="{WP}">Visit SPF Maker Club</a></section>
<section class="section"><div class="section-head"><h2>Projects</h2><a href="work.html">All {len(P)} projects</a></div><div class="mini-grid">{mini}</div></section>
<section class="section"><div class="section-head"><h2>From the notebook</h2><a href="notebook.html">Read the notebook</a></div><div class="mini-grid">{notes}</div></section>
<section class="section"><div class="section-head"><h2>Photography</h2><div class="link-row" style="margin:0"><a href="photographs.html">See all photos</a> &nbsp; <a href="assets/anwar-khan-photography-portfolio.pdf">Portfolio (PDF)</a></div></div><div class="wall">{photos}</div></section>
</div>''')
print('built')
