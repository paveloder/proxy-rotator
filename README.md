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

To build and run a container Makefile should be used:
```bash
make all
```

To add new constant servers use `./files/constant_proxies.txt`.
