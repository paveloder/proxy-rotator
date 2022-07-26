FROM python:3.5
MAINTAINER Pavel Oderyakov

ENV CHECK_URL "https://www.google.com"
ENV CHECK_FOR "<title>Google</title>"
ENV PROXY_TIMEOUT "10.0"
ENV PROXY_FILE "/scripts/files/proxies.txt"

RUN mkdir -p /scripts
RUN mkdir -p /scripts/files

RUN echo deb [check-valid-until=no]  http://archive.debian.org/debian jessie-backports main | sed 's/\(.*\)-sloppy \(.*\)/&@\1 \2/' | tr @ '\n' | tee /etc/apt/sources.list.d/backports.list

RUN apt-get update
RUN apt-get install -y iptables zlib1g zlib1g-dev haproxy
RUN apt-get clean

COPY gimmeproxy.py /scripts/gimmeproxy.py
COPY parse_proxy_list.py /scripts/parse_proxy_list.py
COPY haproxy.cfg /scripts/haproxy.cfg
COPY requirements.txt /scripts/requirements.txt
COPY run.sh /scripts/run.sh
# COPY proxies.txt /scripts/files/proxies.txt
# COPY constant-proxies.txt /scripts/files/constant-proxies.txt

RUN pip install -r /scripts/requirements.txt

RUN chmod -R 777 /scripts
RUN chmod -R 777 /etc/haproxy

CMD ["/scripts/run.sh"]
EXPOSE 5577
