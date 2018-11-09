#!/usr/bin/env python3
from argparse import ArgumentParser, FileType
from csv import DictReader

parser = ArgumentParser()
parser.add_argument('tsv_file', type=FileType('r'))
parser.add_argument('report_file', type=FileType('w'))
parser.add_argument('--min_confidence', type=float, default=0.75)
parser.add_argument('--max_confidence', type=float, default=1)
parser.add_argument('--max_results', type=float, default=float("inf"))
args = parser.parse_args()

report_file = args.report_file.name
args.report_file.close()

lines = []
for row in DictReader(args.tsv_file, delimiter='\t'):
    source = row['source'].strip()
    match = row['match'].strip()
    confidence = float(row['confidence'])
    if source == match or confidence >= args.max_confidence or confidence <= args.min_confidence:
        continue
    lines.append(row)

lines.sort(key=lambda r: float(r['confidence']), reverse=True)

with open(report_file, 'w', encoding='utf-8') as fobj:
    fobj.write('<html>\n')
    fobj.write('<head>\n')
    fobj.write('  <style>\n')
    fobj.write('    .result {\n')
    fobj.write('      margin: 1em;\n')
    fobj.write('      padding: 1em;\n')
    fobj.write('      background-color: silver;\n')
    fobj.write('    }\n')
    fobj.write('    .confidence {\n')
    fobj.write('      font-weight: bold;\n')
    fobj.write('      font-size: 20px;\n')
    fobj.write('      color: darkred;\n')
    fobj.write('    }\n')
    fobj.write('    img {\n')
    fobj.write('      width: 150px;\n')
    fobj.write('      border: 2px solid black;\n')
    fobj.write('    }\n')
    fobj.write('  </style>\n')
    fobj.write('<script src="https://ajax.aspnetcdn.com/ajax/jQuery/jquery-3.3.1.js"></script>\n')
    fobj.write('</head>\n')
    fobj.write('<body>\n')

    for i, row in enumerate(lines):
        if i >= args.max_results:
            break

        source = row['source']
        match = row['match']
        confidence = row['confidence']

        source = source.replace('/images', '/hackfest-data/ttf-photos')
        match = match.replace('/images', '/hackfest-data/ttf-photos')

        source_metadata = {key: value for (key, value) in row.items() if key.startswith('source_')}
        match_metadata = {key: value for (key, value) in row.items() if key.startswith('match_')}
        metadata_keys = sorted({
            key.replace(prefix, '')
            for (prefix, metadata) in [('source_', source_metadata), ('match_', match_metadata)]
            for key in metadata})

        source_url = source.replace("/hackfest-data/ttf-photos", "http://172.22.41.40:9999")
        match_url = match.replace("/hackfest-data/ttf-photos", "http://172.22.41.40:9999")
        source_url = source_url.replace("%", "%25")
        match_url = match_url.replace("%", "%25")
        source_url = source_url.replace(" ", "%20")
        match_url = match_url.replace(" ", "%20")

        fobj.write('<div class="result" data-confidence="%s">\n' % confidence)
        fobj.write('  <img class="source" src="%s" title="%s">\n' % (source_url, source))
        fobj.write('  <img class="match" src="%s" title="%s">\n' % (match_url, match))
        fobj.write('  <span class="confidence">%s</span>\n' % confidence)
        fobj.write('  <table class="metadata">\n')

        fobj.write('    <tr>\n')
        for key in metadata_keys:
            fobj.write('      <th scope="col">%s</th>\n' % key)
        fobj.write('    </tr>\n')

        for prefix, metadata in ('source_', source_metadata), ('match_', match_metadata):
            fobj.write('    <tr>\n')
            for key in metadata_keys:
                fobj.write('    <td>%s</td>\n' % metadata.get(prefix + key, 'NULL'))
            fobj.write('    </tr>\n')

        fobj.write('  </table>\n')
        fobj.write('</div>\n')

    fobj.write('</body>\n')
    fobj.write('</html>\n')
