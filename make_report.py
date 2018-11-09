#!/usr/bin/env python3
import os
from argparse import ArgumentParser, FileType
from csv import DictReader

parser = ArgumentParser()
parser.add_argument('tsv_file', type=FileType('r'))
parser.add_argument('report_file', type=FileType('w'))
parser.add_argument('--min_confidence', type=float, default=0.75)
parser.add_argument('--max_confidence', type=float, default=1)
parser.add_argument('--max_results', type=float, default=float("inf"))
args = parser.parse_args()

css = '''
.result {
  margin: 1em;
  padding: 1em;
  background-color: silver;
}

.confidence {
  font-weight: bold;
  font-size: 20px;
  color: darkred;
}

img {
  width: 150px;
  border: 2px solid black;
}
'''

report_file = args.report_file.name
args.report_file.close()


def inject_script(path):
    dirpath = os.path.dirname(__file__)
    script = os.path.join(dirpath, path)
    print('injecting js file %s....' % script)
    with open(script, 'r') as myfile:
        data = myfile.read()

    return data


lines = []
for row in DictReader(args.tsv_file, delimiter='\t'):
    source = row['source'].strip()
    match = row['match'].strip()
    confidence = float(row['confidence'])
    if source == match or confidence >= args.max_confidence or confidence <= args.min_confidence:
        continue
    lines.append(row)

lines.sort(key=lambda r: float(r['confidence']), reverse=True)

image_placeholder = 'data:image/gif;base64,R0lGODdhAQABAPAAAMPDwwAAACwAAAAAAQABAAACAkQBADs='

dependencies = [
    'https://ajax.aspnetcdn.com/ajax/jQuery/jquery-3.3.1.js',
    'https://cdnjs.cloudflare.com/ajax/libs/jquery.lazyload/1.9.1/jquery.lazyload.min.js',
]

with open(report_file, 'w', encoding='utf-8') as fobj:
    fobj.write('<html>\n')
    fobj.write('<head>\n')
    fobj.write('<title>TTF Report - index.html</title>')
    fobj.write('  <style>\n%s\n</style>\n' % css)
    for dependency in dependencies:
        fobj.write('  <script src="%s"></script>\n' % dependency)
    fobj.write('</head>\n')
    fobj.write('<body>\n')
    fobj.write(inject_script('inject1.html'))

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

        source_url = source.replace("%", "%25")
        match_url = match.replace("%", "%25")
        source_url = source_url.replace(" ", "%20")
        match_url = match_url.replace(" ", "%20")

        fobj.write('<div class="result" data-confidence="%s">\n' % confidence)
        fobj.write('  <img class="source" src="%s" data-original="%s" title="%s">\n' % (image_placeholder, source_url, source))
        fobj.write('  <img class="match" src="%s"  data-original="%s" title="%s">\n' % (image_placeholder, match_url, match))
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

    fobj.write('<script>$(document).ready(function(){$("img").lazyload();});</script>')
    fobj.write('</body>\n')
    fobj.write('</html>\n')
