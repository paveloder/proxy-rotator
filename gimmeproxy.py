import asyncio
import json
import re
import os
from time import sleep, time
from aiohttp import ClientSession, ProxyConnector, Timeout
import requests

number_of_proxies = 30
request_proxies = 25
timeout = float(os.environ.get("PROXY_TIMEOUT")) or 10.0

proxies = []
new_proxies = []
ips = set()

proxy_provider_url = "http://gimmeproxy.com/api/getProxy?get=true&" +\
                     "protocol=http&supportsHttps=true&maxCheckPeriod=3600"
test_url = os.environ.get("CHECK_URL")
test_for = os.environ.get("CHECK_FOR")

async def fetch(proxy):
    conn = ProxyConnector(proxy=proxy)
    with Timeout(timeout):
        try:
            async with ClientSession(connector=conn) as session:
                async with session.get(test_url) as r:
                    if r.status == 200:
                        if re.search(test_for, str(await r.read())):
                            return True
        except Exception:
            pass

async def test_server(proxy):
    t = time()
    if not await fetch(proxy['address']):
        return
    proxy['time'] = time() - t
    proxy['last_test'] = time()
    new_proxies.append(proxy)


def get_proxy_servers(r):
    responses = [requests.get(proxy_provider_url).text for i in range(r)]

    for resp in responses:
        try:
            response = json.loads(resp)
            if response['ipPort'] in ips:
                continue
            ips.add(response['ipPort'])

            proxies.append({
                'port': response['port'],
                'ip': response['ip'],
                'ipPort': response['ipPort'],
                'address': response['curl'],
                'time': -1,
                'last_test': 0
            })
        except Exception:
            pass


def test_proxy_servers():
    loop = asyncio.get_event_loop()

    tasks = []
    for proxy in proxies:
        task = asyncio.ensure_future(test_server(proxy))
        tasks.append(task)
    loop.run_until_complete(asyncio.wait(tasks))


def sort_proxies():
    global proxies
    prx = sorted(new_proxies, key=lambda x: x['time'])
    proxies = prx[:number_of_proxies]

if __name__ == '__main__':
    get_proxy_servers(request_proxies)
    test_proxy_servers()
    sort_proxies()

    for proxy in proxies:
        print(proxy['ipPort'])
