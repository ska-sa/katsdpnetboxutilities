FROM harbor.sdp.kat.ac.za/dockerhub_proxy/library/python

MAINTAINER Kgomotso Monnakgotla <kmonnakgotla@sarao.ac.za>

RUN mkdir /src

EXPOSE 8080/tcp

WORKDIR /src

COPY . .

RUN rm -rf /src/.*.sw*


CMD ["python", "./python-server.py","--directory /src/reports/"]


