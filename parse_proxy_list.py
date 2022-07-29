s = """
global
        log 127.0.0.1   local0
        log 127.0.0.1   local1 notice
        maxconn 4096
        #chroot /usr/share/haproxy
        user haproxy
        group haproxy
        daemon
        stats socket /tmp/haproxy

defaults
        log global
        mode http
        option httplog
        option dontlognull
        retries 3
        option redispatch
        maxconn 2000
        timeout connect 5000
        timeout client 50000
        timeout server 50000
        #clitimeout 50000
        #srvtimeout 50000

frontend rotating_proxies
  bind *:5577
  default_backend tor
  mode http
  option httpclose

backend tor
  balance roundrobin """

import os

hostCount = 1


for line in open('/scripts/files/constant-proxies.txt'):
    line = line.strip()
    if len(line) > 0:
        results = ("\nserver srv{hostCount} {line} " +
                   "weight 1 maxconn 100 check").format(hostCount=hostCount,
                                                        line=line)
        s += results
        hostCount += 1

with open("/etc/haproxy/haproxy.cfg", "w") as text_file:
    text_file.write(s)
with open("/scripts/haproxy.cfg", "w") as text_file:
    text_file.write(s)
