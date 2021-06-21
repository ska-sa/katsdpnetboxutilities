
open:
	xdg-open /reports/$(name)/$(name).pdf

build:
	docker build -t sysinfo .

run:
	docker run -v ${PWD}/reports:/reports sysinfo $(name)

devrun:
	docker run -v ${PWD}/reports:/reports -v ${PWD}:/src sysinfo $(name)
