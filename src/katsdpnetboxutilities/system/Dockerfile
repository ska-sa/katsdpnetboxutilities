FROM pandoc/ubuntu-latex

MAINTAINER Martin Slabber <martin@ska.ac.za>

RUN mkdir /docs

WORKDIR /docs

COPY requirements.txt /docs

RUN pip install --no-cache-dir -r requirements.txt 

COPY . /docs

CMD device-md.py
