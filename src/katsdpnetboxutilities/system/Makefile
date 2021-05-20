
run:
	SERVER_NAME=$1
	mkdir -p docs/docs
	./device-md.py --device-info http://sdp-services.sdp.kat.ac.za/servers -o ./docs/docs $(name)
	docker run -it -v ${PWD}/docs:/docs -v ${PWD}/mkdocs.yml:/docs/mkdocs.yml:ro -v ${PWD}/page.css:/docs/docs/page.css sysinfo build
	cp docs/site/pdf/combined.pdf $(name).pdf
	cp docs/docs/index.md $(name).md
	curl -Ffile=@$(name).md 'http://sdp-services.sdp.kat.ac.za:25478/upload?token=f9403fc5f537b4ab332d'
	curl -Ffile=@$(name).pdf 'http://sdp-services.sdp.kat.ac.za:25478/upload?token=f9403fc5f537b4ab332d'

build:
	docker build -t sysinfo .

open:
	xdg-open ./docs/site/pdf/combined.pdf
