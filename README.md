# Proxies Rotator
Dockerfile for Proxy Rotation  

1) Pulls proxies from GimmeProxy.com  
2) Test the proxies against a configurable URL  
3) Rotate the proxies using HAProxy (round robin)   
4) Repeat every 5 minutes  
5) Expose port 5577 as a proxy

## Settings

You can set the URL that is used for testing the proxy.
This can be beneficial since some proxies may block certain websites.

In addition, you must set a keyword for which we search in the returned
website. This prevents the usage of proxies that always return a default
site for every URL.

Another setting is the timeout. If a proxy takes longer than this amount
in seconds to retrieve the given URL, we will ignore it.

Default values:

CHECK_URL = http://www.google.com

CHECK_FOR = Google Inc.

PROXY_TIMEOUT = 10.0

## Usage

### Testing
```
curl --proxy 127.0.0.1:5566 http://www.google.com
```

### Build
```
sudo docker build -t proxy-rotator-gimme .
```

### Run:
Stop and prune if needed:
```
docker stop rotating-proxy
docker container prune
```
Run new made image
```
docker run -d --name rotating-proxy -p 5577:5577 --privileged proxy-rotator-gimme
```

## Run for Krasnoe i Beloe optimized

```
docker run \
  --env CHECK_URL="https://krasnoeibeloe.ru" \
  --env CHECK_FOR="Красное" \
  --restart always \
  -d --name rotating-proxy -p 5577:5577 \
  --privileged proxy-rotator-gimme
```


### Parse proxy logs at Docker image:
```
docker exec -it rotating-proxy cat /scripts/files/rotatingproxy.log
```

### Parsed and tested proxies list
``` 
docker exec -it rotating-proxy cat /scripts/files/proxies.txt
```

### What HaProxy config is used?
```
docker exec -it rotating-proxy cat /etc/haproxy/haproxy.cfg
```