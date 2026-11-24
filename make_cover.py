import cairosvg, math, random
random.seed(7)
W, H = 700, 919.4
o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %g %g" width="%gpt" height="%gpt">' % (W, H, W * 0.72, H * 0.72)]
o.append('<defs><marker id="ah" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="#ffc933"/></marker><marker id="ag" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="#7f94b8"/></marker>'
         '<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b1c36"/><stop offset="1" stop-color="#14325c"/></linearGradient></defs>')
o.append('<rect width="%g" height="%g" fill="url(#bg)"/>' % (W, H))
# dot grid
for gx in range(30, 700, 40):
    for gy in range(30, 919, 40):
        o.append('<circle cx="%d" cy="%d" r="1.3" fill="#2d4b7a"/>' % (gx, gy))
# network nodes (lower two thirds)
nodes = {'a': (110, 560), 'b': (260, 500), 'c': (430, 560), 'd': (590, 500), 'e': (170, 700), 'f': (340, 680), 'g': (520, 720), 'h': (620, 640), 'i': (90, 820), 'j': (400, 830), 'k': (600, 830)}
edges = [('a', 'b'), ('b', 'c'), ('c', 'd'), ('a', 'e'), ('b', 'f'), ('c', 'f'), ('d', 'h'), ('f', 'g'), ('e', 'f'), ('g', 'h'), ('e', 'i'), ('f', 'j'), ('g', 'k'), ('j', 'k'), ('i', 'j')]
for a, b in edges:
    (x1, y1), (x2, y2) = nodes[a], nodes[b]; d = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / d, (y2 - y1) / d
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#7f94b8" stroke-width="1.6" marker-end="url(#ag)" opacity=".75"/>' % (x1 + ux * 20, y1 + uy * 20, x2 - ux * 22, y2 - uy * 22))
path = ['a', 'b', 'f', 'g', 'k']
for a, b in zip(path, path[1:]):
    (x1, y1), (x2, y2) = nodes[a], nodes[b]; d = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / d, (y2 - y1) / d
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#ffc933" stroke-width="4" marker-end="url(#ah)"/>' % (x1 + ux * 20, y1 + uy * 20, x2 - ux * 24, y2 - uy * 24))
for k, (x, y) in nodes.items():
    hl = k in path
    o.append('<circle cx="%d" cy="%d" r="%d" fill="%s" stroke="%s" stroke-width="3"/>' % (x, y, 17 if hl else 14, '#ffc933' if hl else '#12294d', '#ffc933' if hl else '#7f94b8'))
for x, y, w in [(180, 530, 18), (345, 590, 16), (460, 700, 16)]:
    o.append('<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="#ffffff" opacity=".9"/>' % (x, y, w, w * 0.7))
F = "font-family=\"'Source Serif 4','DejaVu Serif',serif\""; S = "font-family=\"'Source Sans 3','DejaVu Sans',sans-serif\""
o.append('<text x="60" y="92" %s font-size="15" letter-spacing="5" fill="#ffc933" font-weight="600">FIRST EDITION</text>' % S)
for i, t in enumerate(['Integration', 'Architecture', 'in Practice']):
    o.append('<text x="56" y="%d" %s font-size="66" font-weight="700" fill="#ffffff">%s</text>' % (170 + i * 74, F, t))
o.append('<rect x="60" y="352" width="90" height="5" fill="#ffc933"/>')
for i, t in enumerate(['Designing, Building, and Running', 'Enterprise Integrations', 'from REST to Kafka']):
    o.append('<text x="60" y="%d" %s font-size="24" fill="#d5def0">%s</text>' % (395 + i * 31, S, t))
o.append('<text x="60" y="878" %s font-size="26" font-weight="600" fill="#ffffff">Stefan Živanović</text>' % S)
o.append('<text x="60" y="907" %s font-size="15" fill="#b9c7e2">Solution Architect · Prague</text>' % S)
o.append('<text x="640" y="907" %s font-size="11" fill="#8fa3c8" text-anchor="end">Written with AI assistance (Claude, Anthropic)</text>' % S)
o.append('</svg>')
svg = '\n'.join(o)
__import__('os').makedirs('out', exist_ok=True); open('out/cover.svg', 'w').write(svg)
cairosvg.svg2pdf(bytestring=svg.encode(), write_to='out/cover.pdf', output_width=504, output_height=661.7)
cairosvg.svg2png(bytestring=svg.encode(), write_to='out/cover.png', output_width=2100, output_height=2758)
cairosvg.svg2png(bytestring=svg.encode(), write_to='/tmp/cover_small.png', output_width=520, output_height=683)
print('cover ok')
