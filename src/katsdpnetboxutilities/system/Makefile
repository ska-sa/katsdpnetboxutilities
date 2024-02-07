
open:
	xdg-open reports/$(name)/$(name).pdf

build:
	docker build -t sysinfo .

run:
	docker run -v /.config/sarao/netbox:/.config/sarao/netbox -v /home/kat/servers:/servers -v ${PWD}/reports:/reports -v ${PWD}:/src sysinfo2  $(name)

devrun:
	docker run -v /.config/sarao/netbox:/.config/sarao/netbox -v /home/kat/servers:/servers -v ${PWD}/reports:/reports -v ${PWD}:/src -v ${PWD}:/cache sysinfo2 $(name)
