#!/bin/bash
#while true
echo "Press [CTRL+C] to stop.."
while :
do
	cd /scripts
	echo "Downloading Proxies"
	python /scripts/gimmeproxy.py -o /scripts/proxies.txt
	iptables -I INPUT -p tcp --dport $PORT 5566 -j DROP
	sleep 1
	python /scripts/parseProxyList.py
	service haproxy restart
	iptables -D INPUT -p tcp --dport $PORT 5566 -j DROP
	echo "Sleeping for 5 minutes"
	sleep 300
done
