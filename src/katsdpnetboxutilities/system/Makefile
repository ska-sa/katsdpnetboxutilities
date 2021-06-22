
open:
	xdg-open reports/$(name)/$(name).pdf

build:
	docker build -t sysinfo .

run:
	docker run -v ~/.config/sarao/netbox:/.config/sarao/netbox -v ${PWD}/reports:/reports sysinfo $(name)

devrun:
	docker run  -v ~/.config/sarao/netbox:/.config/sarao/netbox -v ${PWD}/reports:/reports -v ${PWD}:/src sysinfo $(name)
