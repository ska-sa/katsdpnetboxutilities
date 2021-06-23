#!/bin/bash
set -eu
NAME=$1
mkdir -p /reports/${NAME}
./device-md.py -c /.config/sarao/netbox --device-info http://sdp-services.sdp.kat.ac.za/servers -o /reports/${NAME} ${NAME}
pandoc --toc --to pdf  --metadata date="`date +%D`"  --variable fontsize=12pt  -o /reports/${NAME}/${NAME}.pdf --defaults=/reports/pandoc.yaml /reports/${NAME}/${NAME}.md
