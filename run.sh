#!/bin/bash
echo "Press [CTRL+C] to stop.."

echo "Connection to yandex cloud serving proxies"
python /scripts/cloud_yandex.py
iptables -I INPUT -p tcp --dport $PORT 5577 -j DROP
sleep 10
python /scripts/parse_proxy_list.py
echo " " >> /etc/haproxy/haproxy.cfg
echo "Starting service"
# service haproxy restart
iptables -D INPUT -p tcp --dport $PORT 5577 -j DROP
haproxy -d -f /etc/haproxy/haproxy.cfg -db
