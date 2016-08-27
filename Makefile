build:
	docker build -t jgontrum/rotatingproxy .

run:
	docker run -d --restart=always -v /root/logs:/scripts/files --name rotatingproxy -e "CHECK_URL=https://www.immobilienscout24.de" -e "CHECK_FOR=IS24" -e "PROXY_TIMEOUT=10.0" --privileged jgontrum/rotatingproxy 2>/dev/null >/dev/null

run_rm:
	docker run -v /root/logs:/scripts/files --rm --name rotatingproxy -e "CHECK_URL=https://www.immobilienscout24.de" -e "CHECK_FOR=IS24" -e "PROXY_TIMEOUT=10.0" --privileged jgontrum/rotatingproxy

stop:
	docker kill rotatingproxy 2>/dev/null; true
	docker rm rotatingproxy 2>/dev/null; true

all: build stop run
