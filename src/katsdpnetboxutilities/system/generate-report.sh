#!/bin/bash
set -eu
NAME=$1
mkdir -p /reports/${NAME}
mkdir -p /cache
./device-md.py --cache-path /cache -c /.config/sarao/netbox --device-info http://sdp-services.sdp.kat.ac.za/servers -o /reports/${NAME} ${NAME}
pandoc --toc --to pdf -o /reports/${NAME}/${NAME}.pdf --defaults=/reports/pandoc.yaml /reports/${NAME}/${NAME}.md
