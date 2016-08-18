build:
	docker build -t jgontrum/rotatingproxy .

run:
	docker run -d --name rotatingproxy -p 127.0.0.0:5566:5566 --privileged jgontrum/rotatingproxy 2>/dev/null >/dev/null

run_rm:
	docker run --rm --name rotatingproxy -p 127.0.0.0:5566:5566 --privileged jgontrum/rotatingproxy

stop:
	docker kill rotatingproxy 2>/dev/null; true

all: build stop run
