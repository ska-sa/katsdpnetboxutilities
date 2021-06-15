
run:
	mkdir -p docs/docs reports/$(name)
	./make_config.py $(name)
	./device-md.py --device-info http://sdp-services.sdp.kat.ac.za/servers -o ./docs/docs $(name)
	cp docs/docs/index.md reports/$(name)/$(name).md
	docker run --rm --volume "`pwd`:/data" --user `id -u`:`id -g` pandoc/ubuntu-latex --toc --to pdf --variable --fontfamily="Courier" --metadata date="`date +%D`"  --variable fontsize=12pt -o reports/$(name)/$(name).pdf --defaults=pandoc.yaml reports/$(name)/$(name).md

open:
	xdg-open reports/$(name)/$(name).pdf

build:
	docker build -t sysinfo .
