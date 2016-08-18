FROM python:3.5
MAINTAINER Johannes Gontrum <https://github.com/jgontrum>

RUN mkdir -p /scripts

COPY gimmeproxy.py /scripts/gimmeproxy.py
COPY haproxy.cfg /scripts/haproxy.cfg
COPY requirements.txt /scripts/requirements.txt
COPY run.sh /scripts/run.sh

RUN apt-get update
RUN apt-get install -y iptables zlib1g zlib1g-dev

RUN pip install -r /scripts/requirements.txt

RUN echo "deb http://httpredir.debian.org/debian jessie-backports main" >> /etc/apt/sources.list.d/backports.list
RUN echo "deb http://haproxy.debian.net jessie-backports-1.6 main" >> /etc/apt/sources.list.d/haproxy.list
RUN curl http://haproxy.debian.net/bernat.debian.org.gpg | apt-key add -
RUN apt-get update
RUN apt-get install haproxy -y --force-yes --fix-missing
RUN apt-get clean & rm -rf /var/lib/apt/lists/*

RUN rm -rf /var/lib/{apt,dpkg,cache,log}/

RUN chmod -R 777 /scripts
RUN chmod -R 777 /etc/haproxy

CMD ["/scripts/run.sh"]
EXPOSE 5566
