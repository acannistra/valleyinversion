#!/bin/bash

EMBEDCODE="$(python inversion.py)"

cp index_template.md index.md

echo ${EMBEDCODE} >> index.md

pandoc index.md -o index.html

echo "created index.html"