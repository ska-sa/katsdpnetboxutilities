katsdpnetboxutilities
=====================

Utilities used at SARAO to maintain infrastructure information stored in [Netbox](https://github.com/netbox-community/netbox).

Installation
------------

katsdpnetboxutilities can be installed with pip directly from [github](https://github.com/ska-sa/katsdpnetboxutilities).
It is advised to install katsdpnetboxutilities in a virtual environment.
`pip install -U git+https://github.com/ska-sa/katsdpnetboxutilities.git`

Configure
---------

Configuration file can be passed in with the `-c` flag or the default config at `~/.config/sarao/netbox` will be used.

Example config file:
    token=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    url=https://netbox.kat.ac.za
 
Use the Netbox UI to obtain your token.

Network Diagrams
-----------------

The command `netboxutilities-network-diagram` can be used to draw basic network diagrams based on the information in Netbox.

`netboxutilities-network-diagram --output-path /tmp/network-diagrams --cache-path /tmp/netbox_cache -n CHPC --live site=chpc`
