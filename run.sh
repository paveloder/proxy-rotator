#!/bin/bash
echo "Press [CTRL+C] to stop.."
while :
do
	echo "Downloading Proxies"
	python /scripts/cloud_yandex.py >> /scripts/files/rotatingproxy.log
	iptables -I INPUT -p tcp --dport $PORT 5577 -j DROP
	sleep 1
	python /scripts/parse_proxy_list.py
	service haproxy restart
	iptables -D INPUT -p tcp --dport $PORT 5577 -j DROP
	echo "Sleeping for 10 minute"
	sleep 600
done
