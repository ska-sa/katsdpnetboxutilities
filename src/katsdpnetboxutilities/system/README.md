
# Production of SDP documents by Pandoc using markdown format

### In the directory katsdpnetboxutilities/src/katsdpnetboxutilities/system run the following commands
1. Run `make build` to create the docker container.
1. Run `make run name=cal1` to generate the Cal1 **server** documentation.
1. Run `make open name=cal1` to view the Cal1 **server** documentation.

### Documents can also be made using the docker image from habor using the commands below.

1. `docker pull harbor.sdp.kat.ac.za/infra/sysinfo`
1. `docker run -v ~/.config/sarao/netbox:/.config/sarao/netbox -v ${PWD}/reports:/reports sysinfo cal1` to generate the Cal1 **server** documentation.
1. `xdg-open reports/$(name)/$(name).pdf` to view the Cal1 **server** documentation.
