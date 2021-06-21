# Netbox device querying

## MD format

### Developer Mode
Run `make build` to create the docker container.
Run `make run name=cal1` to generate the documenattion for the Cal1 **server**.

## RST format

### Developer Mode

Run device.py in katsdpnetboxutilities/src/katsdpnetboxutilities/system
1) `sudo lshw --json > lshw.json`
2) `./device.py --device-info http://sdp-services.sdp.kat.ac.za/servers -o /tmp/doc lab1`

### Sphinx
1) docker pull ddidier/sphinx-doc:3.2.1-1
1) docker run -it -v /tmp/doc:doc1 -e USER_ID=$UID ddidier/sphinx-doc:3.2.1-1 sphinx-init --project=sdp-systems
1) docker run -it -v /tmp/doc:/doc -e USER_ID=$UID ddidier/sphinx-doc:3.2.1-1 sphinx-init -make clean
2) `./device.py --device-info http://sdp-services.sdp.kat.ac.za/servers -o /tmp/doc epyc01`
3) docker run -it -v /tmp/doc:/doc -e USER_ID=$UID ddidier/sphinx-doc:3.2.1-1 make html
4) docker run -it -v /tmp/doc:/doc -e USER_ID=$UID ddidier/sphinx-doc:3.2.1-1 make latexpdf

## Build with Pandoc

Sphinx is cumbersom to run, mkdocs produce very nice HTML reports fast but the PDF reports are not nice. A Quick check of pandocs seems to produce PDFs quickly and it can be used to convert from RST to MD.

docker run --rm --volume "`pwd`:/data" --user `id -u`:`id -g` pandoc/ubuntu-latex --toc --to pdf --variable sansfont="Arial" --variable monofont="Menlo" --variable fontsize=12pt -o /data/cal1-pandoc.pdf --defaults=pandoc.yaml cal1.md