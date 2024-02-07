#!/bin/bash
set -eu
NAME=$1
mkdir -p /reports/${NAME}
mkdir -p /cache
./device-md.py --cache-path /cache -c /.config/sarao/netbox -o /reports/${NAME} ${NAME}
pandoc --toc --to pdf -o /reports/${NAME}/${NAME}.pdf --defaults=/reports/pandoc.yaml /reports/${NAME}/${NAME}.md
