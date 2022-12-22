
# Production of SDP documents by Pandoc using markdown format

## Collect hardware informantion from the remote host
### ssh onto the vm: hardwaredocuments.sdp.kat.ac.za

2. 'cd /home/kat/gitworld/katsdpnetboxutilities/src/katsdpnetboxutilities/system/katsdpinfrastructure/ansible/system/katsdpinfrastructure/ansible'
1. For example, to run the ansible role on host 'cal1' enter the following command.
1. 'bin/ansible-role -i hosts -l cal1 get-hardware-information'
1. The output is saved in 'home/kat/servers/cal1'.

## Build the hardware report
### In the directory katsdpnetboxutilities/src/katsdpnetboxutilities/system run the following commands
1. Run `make build` to create the docker container.
1. Run `make run name=cal1` to generate the Cal1 **server** documentation.
1. Run `make open name=cal1` to view the Cal1 **server** documentation.
1. The report are store in `/home/kat/gitworld/katsdpnetboxutilities/src/katsdpnetboxutilities/system/reports`



