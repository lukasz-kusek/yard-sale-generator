#!/usr/bin/env bash
cd "$(dirname "$0")"

cd ../
drive pull -desktop-links=false -export txt -no-prompt yard-sale

cd yard-sale-generator
python3.8 generate.py

cd ../yard-sale-html
git add *
git add -u
git commit -m "Update"
git push