FROM pandoc/ubuntu-latex:2.12

MAINTAINER SDP <sdp-direct@ska.ac.za>

RUN apt-get update -y; apt-get install -y python3.8 pip git


RUN mkdir /src
WORKDIR /src

COPY requirements.txt .
RUN python3.8 -m pip install -r ./requirements.txt

COPY . /src
RUN chmod -R 777 /src/generate-report.sh
ENTRYPOINT ["bash","/src/generate-report.sh"]
