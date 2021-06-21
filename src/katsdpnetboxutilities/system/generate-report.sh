#!/bin/bash
set -eu
NAME=$1
mkdir -p docs/docs /reports/${NAME}
./device-md.py --device-info http://sdp-services.sdp.kat.ac.za/servers -o ./docs/docs ${NAME}
cp docs/docs/index.md /reports/${NAME}/${NAME}.md
pandoc --toc --to pdf  --metadata date="`date +%D`"  --variable fontsize=12pt -o /reports/${NAME}/${NAME}.pdf --defaults=/reports/pandoc.yaml /reports/${NAME}/${NAME}.md
