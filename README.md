# Proxies Rotator
Dockerfile for Proxy Rotation  

1) Pulls proxies from Yandex Cloud
2) Rotate the proxies using HAProxy (round robin)   
3) Repeat every 5 minutes  
4) Expose port 5577 as a proxy

## Settings


Default values:

CHECK_URL = http://www.google.com

CHECK_FOR = Google Inc.

PROXY_TIMEOUT = 10.0

## Envs

`./.env` file must be created in work dir containing envs below:

YANDEX_CLOUD_TOKEN = ***********

YANDEX_CLOUD_ID = ***********

## Usage

To build and run a container Makefile should be used:
```bash
make all
```

To add new constant servers use `./files/constant_proxies.txt`.
