import asyncio
import json
import re
import os
from time import sleep, time
from aiohttp import ClientSession, ProxyConnector, Timeout
import requests

number_of_proxies = 100
request_proxies = 15
timeout = os.environ.get("PROXY_TIMEOUT")
timeout = float(timeout) if timeout else 10.0
filepath = os.environ.get("PROXY_FILE") or "./proxies.txt"

proxies = []
new_proxies = []
ips = set()

proxy_provider_url = "http://gimmeproxy.com/api/getProxy?get=true&" +\
                     "protocol=http&supportsHttps=true"
test_url = os.environ.get("CHECK_URL") or "https://www.google.com"
test_for = os.environ.get("CHECK_FOR") or "initHistory"

async def fetch(proxy):
    conn = ProxyConnector(proxy=proxy)
    with Timeout(timeout):
        try:
            async with ClientSession(connector=conn) as session:
                async with session.get(test_url) as r:
                    if r.status == 200:
                        text = str(await r.read())
                        if re.search(test_for, str(await r.read())):
                            return True
        except Exception:
            pass

async def test_server(proxy):
    t = time()
    if not await fetch(proxy['address']):
        return
    proxy['time'] = time() - t
    new_proxies.append(proxy)


def get_proxy_servers(r):
    responses = [requests.get(proxy_provider_url).text for i in range(r)]

    for resp in responses:
        try:
            response = json.loads(resp)
            if response.get('status') == 429:
                print("Too many requests :(")
                continue

            if response['ipPort'] in ips:
                continue
            ips.add(response['ipPort'])

            proxies.append({
                'ipPort': response['ipPort'],
                'address': response['curl'],
                'time': -1,
            })
        except Exception:
            continue


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


def load_old_proxies():
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                proxies.append({
                    'ipPort': line,
                    'address': "http://%s" % line,
                    'time': -1,
                })
                ips.add("http://%s" % line)
    except:
        pass
    print("Loaded %s old proxies." % len(proxies))

if __name__ == '__main__':
    load_old_proxies()
    get_proxy_servers(request_proxies)
    test_proxy_servers()
    sort_proxies()

    new = set([proxy['ipPort'].strip() for proxy in proxies])

    with open(filepath, 'w') as f:
        for proxy in new:
            f.write("%s\n" % proxy)
    print("Saved %s new proxies." % len(new))
