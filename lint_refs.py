import re, json, glob, difflib, os, yaml
reg = {r['key'] for r in json.load(open('registry.json'))}
man = yaml.safe_load(open('src/manifest.yaml'))['items']
slugs = {i['slug']: i['type'] for i in man}
files = sorted(glob.glob('src/*.md'))
FIG = re.compile(r'^\{\{fig\s+([\w-]+)', re.M); GRID = re.compile(r'^\{\{figgrid\s+([\w\s-]+?)\s*\|', re.M)
used, errs, gridfirst = {}, [], set()
tbl_def, tbl_ref = set(), []
for f in files:
    t = open(f, encoding='utf-8').read()
    base = os.path.basename(f)
    if base in ('sample1.md', 'sampleapp.md'): continue
    for m in FIG.finditer(t):
        k = m.group(1); used.setdefault(k, []).append(base)
        if k not in reg: errs.append((base, 'fig', k, difflib.get_close_matches(k, reg, 1, 0.8)))
    for m in GRID.finditer(t):
        ks = m.group(1).split(); gridfirst.add(ks[0])
        for k in ks:
            used.setdefault(k, []).append(base)
            if k not in reg: errs.append((base, 'grid', k, difflib.get_close_matches(k, reg, 1, 0.8)))
    for m in re.finditer(r'\{\{tbl\s+([\w-]+)\s*\|', t): tbl_def.add(m.group(1))
    for m in re.finditer(r'\{\{ref\s+(\w+):([\w-]+)\}\}', t):
        kind, key = m.group(1), m.group(2)
        if kind == 'fig':
            if key not in reg: errs.append((base, 'ref-fig-unknown', key, difflib.get_close_matches(key, reg, 1, 0.8)))
            else: tbl_ref.append((base, 'figref', key))
        elif kind == 'tbl': tbl_ref.append((base, 'tbl', key))
        elif kind in ('ch', 'app', 'part'):
            if key not in slugs: errs.append((base, 'ref-slug', key, difflib.get_close_matches(key, slugs, 1, 0.7)))
    for m in re.finditer(r'^\{\{code\s+(\S+?)\s*\}\}', t, re.M):
        if not os.path.exists('code/' + m.group(1)): errs.append((base, 'code', m.group(1), []))
dups = {k: v for k, v in used.items() if len(v) > 1}
for b, kind, key in tbl_ref:
    if kind == 'tbl' and key not in tbl_def: errs.append((b, 'tbl-ref-undefined', key, []))
    if kind == 'figref' and key not in used: errs.append((b, 'figref-not-placed', key, []))
    if kind == 'figref' and key in used and key not in gridfirst and any(re.search(r'^\{\{figgrid[^|]*\b%s\b' % re.escape(key), open('src/' + u, encoding='utf-8').read(), re.M) for u in used[key]) and not any(re.search(r'^\{\{fig\s+%s\b' % re.escape(key), open('src/' + u, encoding='utf-8').read(), re.M) for u in used[key]):
        errs.append((b, 'figref-to-non-first-grid-member', key, []))
print('files', len(files), '| figures placed', len(used), 'of', len(reg), '| duplicate placements', dups)
print('ERRORS', len(errs))
for e in errs: print(e)
un = sorted(reg - set(used))
print('UNUSED (%d):' % len(un), ' '.join(un))
