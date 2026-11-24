"""Concatenate the manuscript into one standalone Markdown reference file."""
import re, yaml, os
man = yaml.safe_load(open('src/manifest.yaml'))
items = man['items']; ROM = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']
chn = appn = partn = 0; lab = {}
for it in items:
    if it['type'] == 'chapter': chn += 1; it['num'] = str(chn)
    elif it['type'] == 'appendix': appn += 1; it['num'] = chr(64 + appn)
    elif it['type'] == 'part': partn += 1; it['num'] = ROM[partn - 1]
    lab[it['slug']] = it.get('num', '')
def conv(md):
    md = re.sub(r'\{\{ref\s+(ch|app|part):([\w-]+)\}\}', lambda m: lab.get(m.group(2), '?'), md)
    md = re.sub(r'\{\{ref\s+fig:([\w-]+)\}\}', 'the figure', md)
    md = re.sub(r'\{\{ref\s+tbl:([\w-]+)\}\}', 'the table', md)
    md = re.sub(r'^\{\{fig\s+([\w-]+)\s*(?:\|\s*(.*?))?\}\}\s*$', lambda m: '*[Figure: %s]*' % (m.group(2) or m.group(1)), md, flags=re.M)
    md = re.sub(r'^\{\{figgrid\s+[\w\s-]+?\s*\|\s*(.*?)\}\}\s*$', lambda m: '*[Figure grid: %s]*' % m.group(1), md, flags=re.M)
    md = re.sub(r'^\{\{tbl\s+(?:[\w-]+\s*\|\s*)?(.*?)\}\}\s*$', lambda m: '**Table: %s**' % m.group(1), md, flags=re.M)
    md = re.sub(r'^\{\{code\s+(\S+?)\s*\}\}\s*$', lambda m: '```python\n%s\n```' % open('code/' + m.group(1), encoding='utf-8').read().rstrip('\n'), md, flags=re.M)
    md = re.sub(r'^!!!\s+(\w+)\s+"(.*?)"\s*$', lambda m: '> **%s**' % m.group(2), md, flags=re.M)
    return md
out = ['# Integration Architecture in Practice\n\n*Designing, Building, and Running Enterprise Integrations from REST to Kafka*\n\n**Author:** Stefan Živanović, Solution Architect, Prague, Czech Republic  \n**Edition:** First Edition, November 2026  \n**Copyright:** © 2026 Stefan Živanović. All rights reserved.  \n**AI statement:** Generated with AI assistance (Claude, by Anthropic), under the author\'s direction. See the section "How This Book Was Made".\n\nReference copy of the manuscript (Markdown). Figures appear as bracketed captions; see the PDF for diagrams. Companion code is in the `code` folder of the build workspace.\n']
for it in items:
    if it['type'] == 'part':
        out.append('\n\n---\n\n# Part %s. %s\n\n%s\n' % (it['num'], it['title'], it.get('text', '')))
    elif 'file' in it and os.path.exists('src/' + it['file']):
        md = conv(open('src/' + it['file'], encoding='utf-8').read())
        if it['type'] == 'chapter': md = re.sub(r'^# ', '# Chapter %s. ' % it['num'], md, count=1, flags=re.M)
        elif it['type'] == 'appendix': md = re.sub(r'^# ', '# Appendix %s. ' % it['num'], md, count=1, flags=re.M)
        out.append('\n\n' + md)
txt = '\n'.join(out)
open('out/integration-architecture-in-practice.md', 'w', encoding='utf-8').write(txt)
print('md written: %d KB, %d words' % (len(txt) // 1024, len(txt.split())))
