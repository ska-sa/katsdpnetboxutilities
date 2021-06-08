
run:
	SERVER_NAME=$1
	mkdir -p docs/docs
	mkdir -p reports/$(name)
	/usr/bin/env python3.8 device-md.py --device-info http://sdp-services.sdp.kat.ac.za/servers -o ./docs/docs $(name)
	cp docs/docs/index.md reports/$(name)/$(name).md
	sudo docker run --rm --volume "`pwd`:/data" --user `id -u`:`id -g` pandoc/ubuntu-latex --toc --to pdf --variable --fontfamily="Courier" --variable fontsize=12pt --variable title='SDP Server $(name)' --metadata date="`date +%D`" -o reports/$(name)/$(name).pdf --defaults=pandoc.yaml reports/$(name)/$(name).md

build:
	docker build -t sysinfo .

open:
	xdg-open reports/$(name)/$(name).pdf
