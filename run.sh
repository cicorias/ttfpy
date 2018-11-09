#!/usr/bin/env bash
python3 join_with_metadata.py ./data.tsv ./metadata.txt > ./data-with-metadata.tsv
python3 make_report.py ./data-with-metadata.tsv ./index.html