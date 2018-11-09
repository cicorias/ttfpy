#!/usr/bin/env python3
from argparse import ArgumentParser, FileType
from csv import reader as CsvReader, DictReader, DictWriter
from sys import stderr, stdout

parser = ArgumentParser()
parser.add_argument('tsv_file', type=FileType('r'))
parser.add_argument('metadata_file', type=FileType('r', encoding='utf-16'))
parser.add_argument('--tsv_file_delimiter', default='\t')
parser.add_argument('--metadata_file_delimiter', default=';')
args = parser.parse_args()

all_metadata = {}
metadata_reader = DictReader(args.metadata_file, delimiter=args.metadata_file_delimiter)
for row in metadata_reader:
    try:
        image_path = row.get('ImagePath', row['ThumbnailImageUrl'])[1:].replace('/', '__')
        image_path = image_path.replace('.thumb', '')
        image_path = '/hackfest-data/ttf-photos/' + image_path
        all_metadata[image_path] = row
    except Exception as ex:
        print(ex, file=stderr)

metadata_keys = sorted(metadata_reader.fieldnames)

output = DictWriter(stdout, fieldnames=['source', 'match', 'confidence'] +
                                       ['source_' + key for key in metadata_keys] +
                                       ['match_' + key for key in metadata_keys])
output.writeheader()

for (source, match, confidence) in CsvReader(args.tsv_file, delimiter=args.tsv_file_delimiter):
    source = source.replace('/images', '/hackfest-data/ttf-photos')
    match = match.replace('/images', '/hackfest-data/ttf-photos')

    row = {'source': source, 'match': match, 'confidence': confidence}

    for prefix, image_key in ('source_', source), ('match_', match):
        metadata = all_metadata.get(image_key, {})
        for key in metadata_keys:
            value = metadata.get(key, 'NULL')
            row[prefix + key] = value

    output.writerow(row)
