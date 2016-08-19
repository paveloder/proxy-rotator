# Proxies Rotator
Dockerfile for Proxy Rotation  

1) Pulls proxies from GimmeProxy.com  
2) Test the proxies against a configurable URL  
3) Rotate the proxies using HAProxy (round robin)   
4) Repeat every 5 minutes  
5) Expose port 5566 as a proxy

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
```
docker pull jgontrum/rotatingproxy

docker run -d --name rotatingproxy -p 127.0.0.0:5566:5566 --privileged jgontrum/rotatingproxy

OR:

docker run --rm --name rotatingproxy -e "CHECK_URL=https://www.immobilienscout24.de" -e "CHECK_FOR=IS24" -e "PROXY_TIMEOUT=10.0" --privileged --net=host jgontrum/rotatingproxy
```

## Testing
```
curl --proxy 127.0.0.1:5566 http://www.google.com
```
