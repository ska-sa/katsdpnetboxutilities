#!/bin/bash
set -eu

SERVER_NAME=$1

WORK_DIR=/tmp/server-docs/$SERVER_NAME
mkdir -p $WORK_DIR
./device.py --device-info http://sdp-services.sdp.kat.ac.za/servers -o $WORK_DIR $SERVER_NAME
cp sites/index.md docs/docs/.

#docker pull ddidier/sphinx-doc:3.2.1-1
#docker run -it -v ${WORK_DIR}:/doc -e USER_ID=$UID ddidier/sphinx-doc:3.2.1-1 sphinx-init --project=sdp-systems
#docker run -it -v ${WORK_DIR}:/doc -e USER_ID=$UID ddidier/sphinx-doc:3.2.1-1 sphinx-init -make clean
#docker run -it -v ${WORK_DIR}:/doc -e USER_ID=$UID ddidier/sphinx-doc:3.2.1-1 make html
#docker run -it -v ${WORK_DIR}:/doc -e USER_ID=$UID ddidier/sphinx-doc:3.2.1-1 make latexpdf
