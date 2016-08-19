build:
	docker build -t jgontrum/rotatingproxy .

run:
	docker run -d --restart=always --name rotatingproxy -v /scripts/files/:/usr/flatfinder/logs -e "CHECK_URL=https://www.immobilienscout24.de" -e "CHECK_FOR=IS24" -e "PROXY_TIMEOUT=10.0" --privileged --net=host jgontrum/rotatingproxy 2>/dev/null >/dev/null

run_rm:
	docker run --rm --name rotatingproxy -e "CHECK_URL=https://www.immobilienscout24.de" -e "CHECK_FOR=IS24" -e "PROXY_TIMEOUT=10.0" --privileged --net=host jgontrum/rotatingproxy

stop:
	docker kill rotatingproxy 2>/dev/null; true
	docker rm rotatingproxy 2>/dev/null; true

all: build stop run
