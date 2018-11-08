from argparse import ArgumentParser, FileType
from csv import DictReader
from collections import defaultdict

parser = ArgumentParser()
parser.add_argument('tsv_file', type=FileType('r'))
parser.add_argument('report_file', type=FileType('w'))
parser.add_argument('--metadata_file', type=FileType('r', encoding="utf-8"), default=None)
parser.add_argument('--min_confidence', type=float, default=0.75)
parser.add_argument('--max_confidence', type=float, default=1)
parser.add_argument('--max_results', type=float, default=float("inf"))
args = parser.parse_args()

tsv_file = args.tsv_file.name
args.tsv_file.close()
report_file = args.report_file.name
args.report_file.close()
max_confidence = args.max_confidence
min_confidence = args.min_confidence
max_results = args.max_results

metadata = {}
if args.metadata_file is not None:
    for row in DictReader(args.metadata_file, delimiter="\t"):
        try:
            image_path = row.get('ImagePath', row["ThumbnailImageUrl"])[1:].replace('/', '__')
            image_path = image_path.replace(".thumb", "")
            image_path = '/hackfest-data/ttf-photos/' + image_path
            metadata[image_path] = row
        except Exception:
            pass

    args.metadata_file.close()

matches = defaultdict(lambda: defaultdict(list))

with open(tsv_file) as fobj:
    for line in fobj:
        (source, match, confidence) = line.strip().split('\t')
        source = source.strip()
        match = match.strip()
        confidence = float(confidence.strip())
        if source == match or confidence >= max_confidence or confidence <= min_confidence:
            continue

        matches[source][match] = confidence

lines = []
for source in list(matches):
    for match in matches[source]:
        confidence = matches[source][match]
        lines.append((source, match, confidence))

lines.sort(key=lambda t: float(t[2]), reverse=True)

metadata_keys = (
  'FamilyLinksFullName',
  'FamilyLinksGender',
  'FatherName',
  'MotherName',
  'DateOfBirth',
  'CountryOfBirth',
  'PlaceOfBirth',
  'CountryOfOrigin',
  'Source',
  'FamilyLinksStatus',
  'ContentType',
)

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
    fobj.write('<script src=\"https://ajax.aspnetcdn.com/ajax/jQuery/jquery-3.3.1.js\"></script>')
    fobj.write('</head>\n')
    fobj.write('<body>\n')

    for i, (source, match, confidence) in enumerate(lines):
        if i >= max_results:
            break

        source = source.replace('/images', '/hackfest-data/ttf-photos')
        match = match.replace('/images', '/hackfest-data/ttf-photos')

        source_metadata = metadata.get(source, {})
        match_metadata = metadata.get(match, {})

        source_url = source.replace("/hackfest-data/ttf-photos", "C:\g\irc\py\\ttf-html\images") # "http://172.22.41.40:9999")
        match_url = match.replace("/hackfest-data/ttf-photos", "C:\g\irc\py\\ttf-html\images") # "http://172.22.41.40:9999")
        source_url = source_url.replace("%", "%25")
        match_url = match_url.replace("%", "%25")
        source_url = source_url.replace(" ", "%20")
        match_url = match_url.replace(" ", "%20")

        fobj.write('<div class="result" data-confidence="%s" >\n' % confidence)
        fobj.write('  <img class="source" src="%s" title="%s">\n' % (source_url, source))
        fobj.write('  <img class="match" src="%s" title="%s">\n' % (match_url, match))
        fobj.write('  <span class="confidence">%s</span>\n' % confidence)
        fobj.write('  <table class="metadata">\n')

        fobj.write('    <tr>\n')
        for key in metadata_keys:
            fobj.write('      <th scope="col">%s</th>\n' % key)
        fobj.write('    </tr>\n')

        for mm in source_metadata, match_metadata:
            fobj.write('    <tr>\n')
            for key in metadata_keys:
                fobj.write('    <td>%s</td>\n' % mm.get(key, 'NULL'))
            fobj.write('    </tr>\n')

        fobj.write('  </table>\n')
        fobj.write('</div>\n')

    fobj.write('</body>\n')
    fobj.write('</html>\n')
