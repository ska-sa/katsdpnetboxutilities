#!/bin/bash
set -eu
NAME=$1
mkdir -p docs/docs reports/${NAME}
python3.8 device-md.py --device-info http://sdp-services.sdp.kat.ac.za/servers -o ./docs/docs ${NAME}
python3.8 make-config.py ${NAME}
cp docs/docs/index.md reports/${NAME}/${NAME}.md
pandoc --toc --to pdf  --metadata date="`date +%D`"  --variable fontsize=12pt -o reports/${NAME}/${NAME}.pdf --defaults=pandoc.yaml reports/${NAME}/${NAME}.md
