FROM python:3.9.6-slim-buster
MAINTAINER Pavel Oderyakov

ENV CHECK_URL="https://www.google.com" \
    CHECK_FOR="<title>Google</title>" \
    PROXY_TIMEOUT="10.0" \
    PROXY_FILE="/scripts/files/proxies.txt"

RUN mkdir -p /scripts && \
    mkdir -p /scripts/files

RUN apt-get update && \
    apt-get install --no-install-recommends -y iptables zlib1g zlib1g-dev haproxy && \
    apt-get clean

COPY requirements.txt /scripts/requirements.txt
RUN pip install -r /scripts/requirements.txt

COPY parse_proxy_list.py cloud_yandex.py haproxy.cfg run.sh  /scripts/

RUN chmod -R 777 /scripts && \
    chmod -R 777 /etc/haproxy

CMD ["/scripts/run.sh"]
EXPOSE 5577
