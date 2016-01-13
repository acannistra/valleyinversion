#!/bin/bash


PREV=$(TZ=America/Denver date --date="3 hours ago" +"%m/%d/%Y-%H")
DATE=$(TZ=America/Denver date +"%m/%d/%Y-%H")

python inversion_paired.py $PREV $DATE Aspen --stations "ASPEN/SARDY FIEL" "ASPEN SKI AREA - GE" --image "images/now.png"

git add images/now.png
git commit -am "added new image on $DATE"
git push origin gh-pages
