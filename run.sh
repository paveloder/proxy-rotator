#!/bin/bash
echo "Press [CTRL+C] to stop.."
while :
do
	echo "Downloading Proxies"
	python /scripts/gimmeproxy.py >> /scripts/files/proxy.log
	iptables -I INPUT -p tcp --dport $PORT 5566 -j DROP
	sleep 1
	python /scripts/parse_proxy_list.py
	service haproxy restart
	iptables -D INPUT -p tcp --dport $PORT 5566 -j DROP
	echo "Sleeping for 10 minutes"
	sleep 600
done
