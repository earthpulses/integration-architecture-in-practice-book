#!/usr/bin/env python3
"""Typeset the book: src/manifest.yaml + src/*.md  ->  build/book.html  ->  out/book.pdf

Manuscript macros (one per line unless noted):
  {{fig key | caption}}          place a diagram from registry.json (caption optional)
  {{figgrid k1 k2 ... | caption}} place several diagrams as one numbered figure
  {{tbl key | caption}}          number and caption the Markdown table that follows
  {{code file.py}}               include a file from code/ as a listing
  {{ref ch:slug}} {{ref app:slug}} {{ref fig:key}} {{ref tbl:key}}   inline cross-references
  !!! goals|why|warning|tip|example|note "Title"   admonition box (indented body)
Publication details come from book_meta.yaml. Run lint_refs.py before building.
"""
import re, os, sys, json, html as H, yaml, time, hashlib
import markdown
from bs4 import BeautifulSoup
from pygments.style import Style
from pygments.token import Token, Comment, Keyword, Name, String, Number, Operator, Generic, Punctuation
from pygments.formatters import HtmlFormatter

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
os.makedirs('build', exist_ok=True); os.makedirs('out', exist_ok=True)
os.chdir(ROOT)
import yaml as _yaml
META = _yaml.safe_load(open('book_meta.yaml', encoding='utf-8'))
TITLE = META['title']
SUBTITLE = META['subtitle']
AUTHOR = META['author']
TEXT_PT = 5.65 * 72          # text block width in points
FIG_MAX = 6.0 * 72           # figures may overhang the margins slightly
REG = {r['key']: r for r in json.load(open('registry.json'))}

# ------------------------------------------------------------------ code highlighting style (grayscale-safe)
class BookStyle(Style):
    background_color = '#f5f5f5'
    styles = {
        Comment: 'italic #666666', Keyword: 'bold #111111', Keyword.Type: '#111111', Name.Function: 'bold #111111', Name.Class: 'bold #111111',
        Name.Decorator: '#444444', Name.Builtin: '#222222', String: '#3d3d3d', Number: '#222222', Operator: '#222222', Name.Tag: 'bold #111111',
        Name.Attribute: '#222222', Generic.Heading: 'bold', Generic.Prompt: '#666666', Generic.Output: '#555555',
    }
CODE_CSS = HtmlFormatter(style=BookStyle, nobackground=True).get_style_defs('.codehilite')

# ------------------------------------------------------------------ helpers
def esc(s):
    return H.escape(s, quote=True)

def fig_size(key):
    """Return (css class, width in pt, height in pt) for a figure registry entry."""
    r = REG[key]
    w, h, fm = r['w'], r['h'], r['fmin'] or 12.0
    width = min(FIG_MAX, w * 8.6 / fm)
    if width > TEXT_PT:
        cls = 'wide'
    else:
        cls = 'norm'
    pt = fm * width / w
    if pt < 5.8:
        # rotate onto its own page when that gives a legible size
        avail_w, avail_h = 6.2 * 72, 7.2 * 72
        scale = min(avail_w / h, avail_h / w)
        if fm * scale >= 5.75:
            return 'rot', w * scale, h * scale
    return cls, width, width * h / w

def rotated_svg(key):
    """Write a 90-degree rotated copy of a figure and return its path."""
    r = REG[key]
    src = open(r['path'], encoding='utf-8').read()
    m = re.match(r'<svg\b([^>]*)>(.*)</svg>\s*$', src, re.S)
    attrs, inner = m.group(1), m.group(2)
    ff = re.search(r'font-family="([^"]*)"', attrs)
    w, h = r['w'], r['h']
    out = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %g %g" font-family="%s"><g transform="translate(%g 0) rotate(90)">%s</g></svg>' % (h, w, ff.group(1) if ff else 'sans-serif', h, inner)
    path = 'build/rot-%s.svg' % key
    open(path, 'w', encoding='utf-8').write(out)
    return path

# ------------------------------------------------------------------ manifest
manifest = yaml.safe_load(open('src/manifest.yaml', encoding='utf-8'))
items = []
chn = 0
appn = 0
partn = 0
ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']
for it in manifest['items']:
    it = dict(it)
    if it['type'] == 'chapter':
        chn += 1; it['num'] = chn; it['label'] = 'Chapter %d' % chn
    elif it['type'] == 'appendix':
        appn += 1; it['num'] = chr(64 + appn); it['label'] = 'Appendix %s' % it['num']
    elif it['type'] == 'part':
        partn += 1; it['num'] = ROMAN[partn - 1]; it['label'] = 'Part %s' % it['num']
    it['id'] = {'chapter': 'ch-', 'appendix': 'app-', 'part': 'part-', 'front': 'front-', 'back': 'back-'}[it['type']] + it['slug']
    items.append(it)
BYSLUG = {it['slug']: it for it in items}

# ------------------------------------------------------------------ pass 1: read sources, number figures and tables
FIG = re.compile(r'^\{\{fig\s+([\w-]+)\s*(?:\|\s*(.*?))?\}\}\s*$', re.M)
FIGGRID = re.compile(r'^\{\{figgrid\s+([\w\s-]+?)\s*\|\s*(.*?)\}\}\s*$', re.M)
TBL = re.compile(r'^\{\{tbl\s+(?:([\w-]+)\s*\|\s*)?(.*?)\}\}\s*$', re.M)
fignum, tblnum = {}, {}
FIGLIST, TBLLIST = [], []
def short_cap(c):
    c = re.sub(r'\s+', ' ', c).strip()
    m = re.match(r'(.{20,120}?[.:])(\s|$)', c)
    c = m.group(1).rstrip('.:') if m else (c[:117] + '...' if len(c) > 120 else c)
    return c

used_figs = set()
def defer_rotated(md, min_words=120):
    """Move full-page rotated figures forward to a heading boundary at least
    min_words of body text later, so the preceding page is not left nearly empty."""
    out, pending, in_code = [], [], False
    for line in md.split('\n'):
        if line.startswith('```'):
            in_code = not in_code
        m = None if in_code else FIG.match(line)
        if m and fig_size(m.group(1))[0] == 'rot':
            pending.append([line, 0]); continue
        if not in_code and re.match(r'^#{2,4}\s', line):
            keep = []
            for p in pending:
                if p[1] >= min_words:
                    out.extend(['', p[0], ''])
                else:
                    keep.append(p)
            pending = keep
        elif not in_code:
            for p in pending:
                p[1] += len(line.split())
        out.append(line)
    for p in pending:
        out.extend(['', p[0], ''])
    return '\n'.join(out)

for it in items:
    if it['type'] in ('part',) or 'file' not in it:
        it['md'] = it.get('text', '')
    else:
        fp = 'src/' + it['file']
        it['md'] = open(fp, encoding='utf-8').read() if os.path.exists(fp) else '# %s\n\n*Draft pending.*\n' % it['title']
    if it['type'] == 'chapter' or it['type'] == 'appendix':
        it['md'] = defer_rotated(it['md'])
    n = 0; t = 0
    pref = str(it.get('num', ''))
    for m in FIG.finditer(it['md']):
        n += 1; key = m.group(1)
        if key not in REG:
            sys.exit('unknown figure %s in %s' % (key, it['file']))
        if key in fignum:
            sys.exit('figure %s used twice' % key)
        fignum[key] = '%s-%d' % (pref, n); used_figs.add(key)
    for m in FIGGRID.finditer(it['md']):
        n += 1
        keys = m.group(1).split()
        for k in keys:
            if k not in REG:
                sys.exit('unknown figure %s in %s' % (k, it['file']))
            used_figs.add(k)
        fignum['grid:' + keys[0]] = '%s-%d' % (pref, n)
    for m in TBL.finditer(it['md']):
        t += 1
        if m.group(1):
            tblnum[m.group(1)] = '%s-%d' % (pref, t)

# ------------------------------------------------------------------ pass 2: macros -> html
def expand_macros(it):
    md = it['md']
    pref = str(it.get('num', ''))
    # protect fenced code
    parts = re.split(r'(^```.*?^```)', md, flags=re.M | re.S)
    cnt = {'f': 0, 't': 0}
    def figure_html(m):
        key, cap = m.group(1), (m.group(2) or '').strip()
        r = REG[key]
        cls, w, h = fig_size(key)
        cnt['f'] += 1
        label = fignum[key]
        caption = cap or r['orig_caption'] or r['title']
        FIGLIST.append((label, 'fig-' + key, short_cap(caption)))
        notes = ''
        if r['notes']:
            notes = '<div class="fnotes">' + ''.join('<p><span class="fl">%s</span> %s</p>' % (chr(65 + i), esc(n)) for i, n in enumerate(r['notes'])) + '</div>'
        if cls == 'rot':
            path = rotated_svg(key)
            return ('\n<figure class="fig rot" id="fig-%s"><img src="%s" style="width:%.1fpt;height:%.1fpt" alt="%s"><figcaption><span class="fnum">Figure %s.</span> %s</figcaption>%s</figure>\n'
                    % (key, path, h, w, esc(r['title']), label, esc_cap(caption), notes))
        return ('\n<figure class="fig %s" id="fig-%s"><img src="%s" style="width:%.1fpt" alt="%s"><figcaption><span class="fnum">Figure %s.</span> %s</figcaption>%s</figure>\n'
                % (cls, key, r['path'], w, esc(r['title']), label, esc_cap(caption), notes))
    def grid_html(m):
        keys = m.group(1).split(); cap = m.group(2).strip()
        label = fignum['grid:' + keys[0]]
        FIGLIST.append((label, 'fig-' + keys[0], short_cap(cap)))
        cells = ''
        for i, k in enumerate(keys):
            r = REG[k]
            cells += '<div class="gcell"><img src="%s" alt="%s"><div class="gsub">(%s) %s</div></div>' % (r['path'], esc(r['title']), chr(97 + i), esc(r['title'].split(':')[0]))
        return '\n<figure class="fig grid" id="fig-%s"><div class="ggrid">%s</div><figcaption><span class="fnum">Figure %s.</span> %s</figcaption></figure>\n' % (keys[0], cells, label, esc_cap(cap))
    def tbl_html(m):
        cnt['t'] += 1
        label = '%s-%d' % (pref, cnt['t'])
        key = m.group(1)
        if key: TBLLIST.append((label, 'tbl-' + key, short_cap(m.group(2).strip())))
        return '\n<p class="tblcap"%s><span class="fnum">Table %s.</span> %s</p>\n' % (' id="tbl-%s"' % key if key else '', label, esc_cap(m.group(2).strip()))
    out = []
    def code_inc(m):
        path = 'code/' + m.group(1)
        return '```%s\n%s\n```' % (m.group(2) or 'python', open(path, encoding='utf-8').read().rstrip('\n'))
    for i, p in enumerate(parts):
        if i % 2 == 1:
            out.append(p); continue
        p = re.sub(r'^\{\{code\s+(\S+)\s*(?:\|\s*(\w+))?\}\}\s*$', code_inc, p, flags=re.M)
        p = FIGGRID.sub(grid_html, p)
        p = FIG.sub(figure_html, p)
        p = TBL.sub(tbl_html, p)
        out.append(p)
    return ''.join(out)

def esc_cap(s):
    s = H.escape(s, quote=False)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    return s

def resolve_refs(text):
    def r(m):
        kind, key = m.group(1), m.group(2)
        if kind == 'fig':
            lab = fignum.get(key) or fignum.get('grid:' + key)
            if not lab:
                sys.exit('bad figure ref ' + key)
            return '<a class="xref" href="#fig-%s">Figure %s</a>' % (key, lab)
        if kind == 'tbl':
            return '<a class="xref" href="#tbl-%s">Table %s</a>' % (key, tblnum[key])
        if kind in ('ch', 'app', 'part'):
            it = BYSLUG.get(key)
            if not it:
                sys.exit('bad ref ' + m.group(0))
            return '<a class="xref" href="#%s">%s</a>' % (it['id'], re.sub(r'^(Chapter|Appendix|Part)\s+', '', it['label']))
        sys.exit('bad ref ' + m.group(0))
    return re.sub(r'\{\{ref\s+(\w+):([\w-]+)\}\}', r, text)

class FootnoteExt:
    pass

def footnotes(md):
    return re.sub(r'\^\[(.+?)\]', lambda m: '<span class="fn">%s</span>' % m.group(1), md)

MD = markdown.Markdown(extensions=['tables', 'fenced_code', 'admonition', 'attr_list', 'def_list', 'sane_lists', 'md_in_html', 'smarty',
                                  'codehilite'], extension_configs={'codehilite': {'guess_lang': False, 'use_pygments': True, 'noclasses': False, 'pygments_style': 'default'},
                                                                   'smarty': {'smart_dashes': True, 'smart_quotes': True, 'smart_ellipses': True}})

def render_md(it):
    md = expand_macros(it)
    md = footnotes(md)
    MD.reset()
    htm = MD.convert(md)
    return resolve_refs(htm)

# ------------------------------------------------------------------ sections
body_parts = []
toc = []
h2count = 0
glossary_terms = []
for it in items:
    if it['type'] == 'part':
        htm = render_md(it)
        body_parts.append('<section class="part%s" id="%s"><div class="partnum">%s</div><h1 class="parttitle">%s</h1><div class="partintro">%s</div></section>' % (' firstpart' if it['num'] == 'I' else '', it['id'], it['label'], esc(it['title']), htm))
        toc.append(('part', it['id'], it['label'] + '  ' + it['title'], ''))
        continue
    htm = render_md(it)
    soup = BeautifulSoup(htm, 'html.parser')
    h1 = soup.find('h1')
    title = it.get('title') or (h1.get_text() if h1 else it['slug'])
    if h1:
        h1.decompose()
    for h2 in soup.find_all('h2'):
        h2count += 1
        h2['id'] = 'h2-%d' % h2count
        toc.append(('h2', h2['id'], h2.get_text(), it['id']))
    body = str(soup)
    typ = it['type']
    if typ == 'chapter':
        opener = '<div class="chapnum">%s</div><h1 class="chaptitle">%s</h1>' % (it['label'], esc(title))
        toc.append(('chapter', it['id'], '%d' % it['num'] + '\t' + title, ''))
    elif typ == 'appendix':
        opener = '<div class="chapnum">%s</div><h1 class="chaptitle">%s</h1>' % (it['label'], esc(title))
        toc.append(('chapter', it['id'], it['label'] + '. ' + title, ''))
    else:
        opener = '<h1 class="chaptitle front">%s</h1>' % esc(title)
        toc.append(('chapter', it['id'], title, ''))
    # TOC order: chapter entry must precede its h2 entries
    cls = 'chapter' if typ == 'chapter' else ('appendix' if typ == 'appendix' else ('backsec' if typ == 'back' else 'frontsec'))
    body_parts.append('<section class="%s" id="%s">%s<div class="content" data-title="%s">%s</div></section>' % (cls, it['id'], opener, esc(title), body))
# fix TOC ordering (h2 collected before chapter entry)
ordered = []
buf = []
for e in toc:
    if e[0] == 'h2':
        buf.append(e)
    else:
        if e[0] == 'chapter':
            ordered.append(e); ordered.extend(buf); buf = []
        else:
            ordered.extend(buf); buf = []; ordered.append(e)
ordered.extend(buf)
toc = ordered

# ------------------------------------------------------------------ automatic index
terms = []
if os.path.exists('src/index_terms.txt'):
    for line in open('src/index_terms.txt', encoding='utf-8'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = [p.strip() for p in line.split('|', 1)]
        disp = parts[0]; pat = parts[1] if len(parts) > 1 and parts[1] else re.escape(disp)
        terms.append((disp, re.compile(r'(?<![\w-])(%s)(?![\w-])' % pat, re.I)))
full = '\n'.join(body_parts)
soup = BeautifulSoup(full, 'html.parser')
soup = BeautifulSoup(full, 'html.parser')
from bs4 import NavigableString
ixrefs = {}
ixn = 0
SKIP = ['pre', 'code', 'h1', 'h2', 'h3', 'h4', 'figcaption', 'th', 'a', 'figure']
def index_node(node, seen):
    global ixn
    txt = str(node)
    if len(txt) < 3:
        return
    best = None
    for disp, rx in terms:
        if disp in seen:
            continue
        m = rx.search(txt)
        if m and (best is None or m.start() < best[1].start()):
            best = (disp, m)
    if not best:
        return
    disp, m = best
    seen.add(disp)
    ixn += 1
    aid = 'ix-%d' % ixn
    ixrefs.setdefault(disp, []).append(aid)
    marker = soup.new_tag('span', id=aid); marker['class'] = 'ixm'; marker.string = '\u200b'
    left, right = NavigableString(txt[:m.start()]), NavigableString(txt[m.start():])
    node.insert_before(left); node.insert_before(marker); node.insert_before(right)
    node.extract()
    index_node(right, seen)
for sec in soup.find_all('section', class_=['chapter', 'appendix']):
    seen = set()
    for node in list(sec.find_all(string=True)):
        if node.find_parent(SKIP):
            continue
        index_node(node, seen)
full = str(soup)

def build_index():
    if not ixrefs:
        return ''
    out = ['<section class="backsec" id="index"><h1 class="chaptitle front">Index</h1><div class="index">']
    letter = ''
    for disp in sorted(ixrefs, key=lambda s: re.sub(r'[^a-z0-9]', '', s.lower())):
        first = re.sub(r'[^A-Za-z]', '', disp)[:1].upper() or '#'
        if first != letter:
            letter = first; out.append('<div class="ixl">%s</div>' % letter)
        refs = ixrefs[disp][:6]
        out.append('<p class="ix"><span class="term">%s</span>%s</p>' % (esc(disp), ''.join('<a href="#%s"></a>' % a for a in refs)))
    out.append('</div></section>')
    return ''.join(out)

# ------------------------------------------------------------------ front matter
def front_matter():
    M = META
    f = []
    f.append('<section class="halftitle" id="halftitle"><h1>%s</h1></section>' % esc(TITLE))
    f.append('<section class="titlepage" id="titlepage"><div class="tp-top">%s</div><h1 class="tp-title">%s</h1><div class="tp-sub">%s</div><div class="tp-author">%s</div><div class="tp-role">%s</div><div class="tp-bottom">%s, %s</div><div class="tp-ai">Written with AI assistance (Claude, by Anthropic)</div></section>' % (esc(M['edition']), esc(TITLE), esc(SUBTITLE), esc(AUTHOR), esc(M['role']), esc(M['city']), esc(str(M['year']))))
    pub = M.get('publisher') or ('the author, %s, %s' % (M['city'], M['country']))
    lines = ['<p><b>%s</b><br>%s</p>' % (esc(TITLE), esc(SUBTITLE)),
             '<p>Copyright &copy; %s %s. All rights reserved.</p>' % (M['year'], esc(M['copyright_holder'])),
             '<p>No part of this publication may be reproduced, stored in a retrieval system, or transmitted in any form or by any means without the prior written permission of the author, except for brief quotations in reviews and the companion code, which is licensed under the %s License.</p>' % esc(M['code_license']),
             '<p>Author: %s, %s, %s, %s.</p>' % (esc(AUTHOR), esc(M['role']), esc(M['city']), esc(M['country'])),
             '<p>Published by %s.</p>' % esc(pub),
             '<p>%s, %s.<br>Revision history: %s: first release.</p>' % (esc(M['edition']), esc(M['edition_date']), esc(M['edition_date']))]
    if M.get('isbn'): lines.append('<p>ISBN %s</p>' % esc(M['isbn']))
    if M.get('email') or M.get('website'):
        lines.append('<p>Contact: %s</p>' % esc(' &middot; '.join(x for x in (M.get('email'), M.get('website')) if x)).replace('&amp;middot;', '&middot;'))
    lines.append('<p><b>Use of artificial intelligence.</b> %s The text, diagrams, index, cover, and companion code of this book were produced with an AI assistant. See the section &ldquo;How This Book Was Made.&rdquo;</p>' % esc(M['ai_statement']))
    lines.append('<p>The publisher and the author have used good-faith efforts to ensure that the information and instructions contained in this work are accurate, but disclaim all responsibility for errors or omissions, including without limitation responsibility for damages resulting from the use of or reliance on this work. Use of the information and instructions contained in this work is at your own risk. If any code samples or other technology this work contains or describes is subject to open source licenses or the intellectual property rights of others, it is your responsibility to ensure that your use thereof complies with such licenses and/or rights.</p>')
    lines.append('<p>Product names, company names, and logos mentioned in this book are trademarks or registered trademarks of their respective owners and are used for identification only; their use does not imply endorsement. The fictional companies, people, and incidents in the examples are composites created for teaching; any resemblance to real organizations or events is coincidental.</p>')
    f.append('<section class="copyright" id="copyright"><div class="cr">%s</div></section>' % '\n'.join(lines))
    return '\n'.join(f)

def build_lists():
    out = []
    for sid, title, items, pre in (('lof', 'List of Figures', FIGLIST, 'Figure'), ('lot', 'List of Tables', TBLLIST, 'Table')):
        li = ''.join('<li class="lf"><a href="#%s"><span class="tn">%s %s</span>%s</a></li>' % (i, pre, lab, esc_cap(c)) for lab, i, c in items)
        out.append('<section class="tocsec" id="%s"><h1 class="chaptitle front">%s</h1><ul class="toc">%s</ul></section>' % (sid, title, li))
    return ''.join(out)

def build_toc():
    out = ['<section class="tocsec" id="toc"><h1 class="chaptitle front">Contents</h1><ul class="toc">']
    for kind, tid, text, parent in toc:
        if kind == 'part':
            out.append('<li class="t-part"><a href="#%s">%s</a></li>' % (tid, esc(text)))
        elif kind == 'chapter':
            if '\t' in text:
                n, t = text.split('\t', 1)
                out.append('<li class="t-ch"><a href="#%s"><span class="tn">%s</span><span class="tt">%s</span></a></li>' % (tid, n, esc(t)))
            else:
                out.append('<li class="t-ch"><a href="#%s"><span class="tt">%s</span></a></li>' % (tid, esc(text)))
        else:
            out.append('<li class="t-h2"><a href="#%s">%s</a></li>' % (tid, esc(text)))
    out.append('</ul></section>')
    return ''.join(out)

# ------------------------------------------------------------------ assemble
def assemble():
    front_items = [s for s in re.findall(r'<section class="frontsec".*?</section>\s*(?=<section|$)', full, re.S)]
    # split body into front sections (preface etc.), then everything else
    soup2 = BeautifulSoup(full, 'html.parser')
    fronts = soup2.find_all('section', class_='frontsec')
    for s in fronts:
        s.extract()
    rest = str(soup2)
    fronts_html = ''.join(str(s) for s in fronts)
    doc = ['<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>%s: %s</title><meta name="author" content="%s"><meta name="description" content="%s"><meta name="keywords" content="integration architecture, APIs, Kafka, event-driven architecture, enterprise integration, AI-assisted"><meta name="generator" content="Generated with AI assistance (Claude, Anthropic); typeset with WeasyPrint">' % (esc(TITLE), esc(SUBTITLE), esc(AUTHOR), esc(SUBTITLE)),
           '<link rel="stylesheet" href="book.css"><style>%s</style></head><body>' % CODE_CSS,
           '<div class="frontmatter">', front_matter(), build_toc(), build_lists(), fronts_html, '</div>',
           '<div class="bodymatter">', rest, '</div>', build_index(), '</body></html>']
    return '\n'.join(doc)

if __name__ == '__main__':
    t0 = time.time()
    os.makedirs('build', exist_ok=True); os.makedirs('out', exist_ok=True)
    htm = assemble()
    open('build/book.html', 'w', encoding='utf-8').write(htm)
    unused = sorted(set(REG) - used_figs)
    print('figure list entries %d, table list entries %d' % (len(FIGLIST), len(TBLLIST)))
    print('html written: %d KB; chapters %d; appendices %d; figures used %d of %d; tables numbered %d; index terms hit %d' % (len(htm) // 1024, chn, appn, len(used_figs), len(REG), sum(1 for _ in TBL.finditer(' '.join(i['md'] for i in items))), len(ixrefs)))
    if unused:
        print('UNUSED FIGURES (%d):' % len(unused), ' '.join(unused))
    if '--html-only' in sys.argv:
        sys.exit(0)
    from weasyprint import HTML
    out = 'out/book.pdf' if '--sample' not in sys.argv else 'out/sample.pdf'
    def roman(n):
        v = [(10, 'x'), (9, 'ix'), (5, 'v'), (4, 'iv'), (1, 'i')]; r = ''
        for k, sy in v:
            while n >= k: r += sy; n -= k
        return r
    def stamp(h, pn):
        def toc_block(m):
            return re.sub(r'<a href="#([^"]+)">', lambda x: '<a href="#%s" data-pn="%s">' % (x.group(1), pn.get(x.group(1), '000')), m.group(0))
        h = re.sub(r'<ul class="toc">.*?</ul>', toc_block, h, flags=re.S)
        def ix_para(m):
            refs = re.findall(r'<a href="#([^"]+)"></a>', m.group(2))
            seen, outp = set(), []
            for r in refs:
                lab = pn.get(r, '000')
                if lab in seen and pn:
                    continue
                seen.add(lab); outp.append('<a href="#%s" data-pn="%s"></a>' % (r, lab))
            if pn:
                outp.sort(key=lambda a: _sortkey(re.search(r'data-pn="([^"]*)"', a).group(1)))
            return m.group(1) + ''.join(outp) + '</p>'
        h = re.sub(r'(<p class="ix"><span class="term">.*?</span>)((?:<a href="#[^"]+"></a>)*)</p>', ix_para, h, flags=re.S)
        return h
    def _sortkey(lab):
        if lab.isdigit(): return (1, int(lab))
        return (0, len(lab), lab)
    html1 = stamp(htm, {})
    d1 = HTML(string=html1, base_url=ROOT + '/').render()
    anchor_page = {}
    for i, pg in enumerate(d1.pages, 1):
        for k in pg.anchors:
            anchor_page.setdefault(k, i)
    first_part = next(i['id'] for i in items if i['type'] == 'part')
    fb = anchor_page[first_part]
    pn = {k: (roman(p) if p < fb else str(p - fb + 1)) for k, p in anchor_page.items()}
    print('physical pages %d; first body page is physical %d' % (len(d1.pages), fb))
    html2 = stamp(htm, pn)
    open('build/book_final.html', 'w', encoding='utf-8').write(html2)
    try:
        HTML(string=html2, base_url=ROOT + '/').write_pdf(out, optimize_images=True, pdf_variant='pdf/a-2b')
        print('PDF variant: PDF/A-2b')
    except Exception as e:
        print('PDF/A-2b failed (%s); writing plain PDF' % str(e)[:120])
        HTML(string=html2, base_url=ROOT + '/').write_pdf(out, optimize_images=True)
    print('pdf written', out, '%.0fs' % (time.time() - t0))
