build:
	docker build -t rotating-proxy -f Dockerfile .

run:
	docker run -d --name rotating-proxy -p 5577:5577 --env-file='./.env' -v ${PWD}/files:/scripts/files --privileged rotating-proxy
stop:
	docker kill rotating-proxy 2>/dev/null; true
	docker rm rotating-proxy 2>/dev/null; true

all: build stop run
