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

with open(report_file, 'w', encoding='utf-8') as fobj:
    fobj.write('<html>\n')
    fobj.write('<head>\n')
    fobj.write('<title>TTF Report - index.html</title>')
    fobj.write('  <style>\n%s\n</style>\n' % css)
    for dependency in js_dependencies:
        fobj.write('  <script src="%s"></script>\n' % dependency)
    for dependency in css_dependencies:
        fobj.write('  <link rel="stylesheet" href="%s">\n' % dependency)
    fobj.write('</head>\n')
    fobj.write('<body>\n')
    fobj.write(inject_script('inject1.html'))

    for dropdown in 'ContentType', 'CountryOfBirth', 'Nationality', 'FamilyLinksGender', 'FamilyLinksStatus', 'Source':
        fobj.write('<label for="{0}">{0}\n'.format(dropdown))
        fobj.write('  <select name="{0}" id="{0}">\n'.format(dropdown))
        for dropdown_value in sorted({row[key + dropdown] for row in rows for key in ['source_', 'match_']}):
            fobj.write('    <option value="{0}">{0}</option>\n'.format(dropdown_value))
        fobj.write('  </select>\n')
        fobj.write('</label>\n')

    fobj.write('''
    <script>
    $("select").change(function() {
      var $select = $(this);
      var searchDimension = $select.attr("name");
      var searchTerm = $select.val();
      $(".result").each(function() {
        var $result = $(this);
        var $metadatas = $result.find("[data-" + searchDimension + "]");
        var hasSearchTerm = $metadatas.filter(function(i, metadata) {
          var value = $(metadata).attr("data-" + searchDimension) || "";
          return value.indexOf(searchTerm) !== -1;
        }).length > 0;
        
        if (hasSearchTerm) {
          $result.show();
        } else {
          $result.hide();
        }
      });
    });
    </script>
    ''')

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
                fobj.write('    <td data-{0}="{1}">{1}</td>\n'.format(key, metadata.get(prefix + key, 'NULL')))
            fobj.write('    </tr>\n')

        fobj.write('  </table>\n')
        fobj.write('</div>\n')

    fobj.write('<script>$(document).ready(function(){$("img").lazyload();});</script>')
    fobj.write('<script>$(document).ready(function(){$("select").select2({dropdownAutoWidth:true,width:"auto"});});</script>')
    fobj.write('</body>\n')
    fobj.write('</html>\n')
