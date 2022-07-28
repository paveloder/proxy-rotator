FROM python:3.10
MAINTAINER Pavel Oderyakov

ENV CHECK_URL "https://www.google.com"
ENV CHECK_FOR "<title>Google</title>"
ENV PROXY_TIMEOUT "10.0"
ENV PROXY_FILE "/scripts/files/proxies.txt"

RUN mkdir -p /scripts
RUN mkdir -p /scripts/files

RUN apt-get update
RUN apt-get install -y iptables zlib1g zlib1g-dev haproxy
RUN apt-get clean

COPY requirements.txt /scripts/requirements.txt
RUN pip install -r /scripts/requirements.txt

COPY gimmeproxy.py /scripts/gimmeproxy.py
COPY parse_proxy_list.py /scripts/parse_proxy_list.py
COPY cloud_yandex.py /scripts/cloud_yandex.py
COPY haproxy.cfg /scripts/haproxy.cfg
COPY run.sh /scripts/run.sh

RUN chmod -R 777 /scripts
RUN chmod -R 777 /etc/haproxy

CMD ["/scripts/run.sh"]
EXPOSE 5577
