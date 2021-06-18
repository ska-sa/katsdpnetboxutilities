FROM pandoc/ubuntu-latex

MAINTAINER Martin Slabber <martin@ska.ac.za>

RUN mkdir /src

WORKDIR /src

COPY requirements.txt .

COPY generate-report.sh .

RUN apt-get update -y; apt-get install python3.8 -y

RUN apt-get install pip -y

RUN apt-get install git -y

RUN python3.8 -m pip install -r ./requirements.txt

RUN chmod -R 777 ./generate-report.sh

COPY . /src

ENTRYPOINT ["bash","/src/generate-report.sh"]
