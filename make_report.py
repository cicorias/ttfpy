#!/usr/bin/env python3
import os
from argparse import ArgumentParser, FileType
from collections import Counter
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

metadata_excludes = {
    'ThumbnailImageUrl',
    'WatermarkedImageUrl',
}


def inject_content(path):
    dirpath = os.path.dirname(__file__)
    script = os.path.join(dirpath, path)
    print('injecting js file %s....' % script)
    with open(script, 'r') as myfile:
        data = myfile.read()

    return data


rows = []
for row in DictReader(args.tsv_file, delimiter='\t'):
    source = row['source'].strip()
    match = row['match'].strip()
    confidence = float(row['confidence'])
    if source == match or confidence >= args.max_confidence or confidence <= args.min_confidence:
        continue
    rows.append(row)

rows.sort(key=lambda r: float(r['confidence']), reverse=True)

image_placeholder = 'data:image/gif;base64,R0lGODdhAQABAPAAAMPDwwAAACwAAAAAAQABAAACAkQBADs='

js_dependencies = [
    'https://ajax.aspnetcdn.com/ajax/jQuery/jquery-3.3.1.js',
    'https://cdnjs.cloudflare.com/ajax/libs/jquery.lazyload/1.9.1/jquery.lazyload.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.5/js/select2.full.min.js',
]

css_dependencies = [
    'https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.5/css/select2.min.css',
]

js_scripts = [
    'confidence.js',
    'dropdowns.js',
]

with open(report_file, 'w', encoding='utf-8') as fobj:
    fobj.write('<html>\n')
    fobj.write('<head>\n')
    fobj.write('<title>TTF Report - index.html</title>')
    fobj.write('  <style>%s</style>\n' % inject_content('style.css'))
    for dependency in js_dependencies:
        fobj.write('  <script src="%s"></script>\n' % dependency)
    for dependency in css_dependencies:
        fobj.write('  <link rel="stylesheet" href="%s">\n' % dependency)
    fobj.write('</head>\n')
    fobj.write('<body>\n')

    fobj.write('<div class="controls">\n')
    fobj.write('''
      <label for="confidence-min">Minimum</label> 
      <input id="confidence-min" type="number" value="0.90">
      <label for="confidence-max">Maximum</label>
      <input id="confidence-max" type="number" value="1.0">
      <input id="apply" type="button" value="Apply" title="Apply...">
    ''')

    for dropdown in 'ContentType', 'CountryOfBirth', 'Nationality', 'FamilyLinksGender', 'FamilyLinksStatus', 'Source':
        fobj.write('<label for="{0}">{0}\n'.format(dropdown))
        fobj.write('  <select name="{0}" id="{0} value="Apply filters" title="Apply filters">">\n'.format(dropdown))
        fobj.write('    <option value="">ALL</option>\n')
        dropdown_values = Counter(row[key + dropdown] for row in rows for key in ['source_', 'match_'])
        total_count = sum(dropdown_values.values())
        for dropdown_value, count in dropdown_values.most_common():
            fobj.write('    <option value="{0}">{0} ({1:.0f}%)</option>\n'.format(dropdown_value, count / total_count * 100.))
        fobj.write('  </select>\n')
        fobj.write('</label>\n')
    fobj.write('</div>\n')

    fobj.write('<div class="results">\n')
    for i, row in enumerate(rows):
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
            for key in metadata} - metadata_excludes)

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
                fobj.write('    <td data-{0}="{1}">{1}</td>\n'.format(key, metadata.get(prefix + key, 'NULL')))
            fobj.write('    </tr>\n')

        fobj.write('  </table>\n')
        fobj.write('</div>\n')
    fobj.write('</div>\n')

    fobj.write('<script>$(document).ready(function(){$("img").lazyload();});</script>')
    fobj.write('<script>$(document).ready(function(){$("select").select2({dropdownAutoWidth:true,width:"auto"});});</script>')
    for js_script in js_scripts:
        fobj.write('<script>%s</script>' % inject_content(js_script))
    fobj.write('</body>\n')
    fobj.write('</html>\n')
