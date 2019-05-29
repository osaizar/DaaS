#!/bin/bash
# This script needs to  be in /root/ of the OpenStack server

source /opt/stack/devstack/openrc demo > /dev/null 2> /dev/null
inst_name="inst_$RANDOM"
dport=$(shuf -i 20000-65000 -n 1)

openstack server create --flavor DandD --image ubuntu --nic net-id=c45da0d4-ec13-4607-a416-82c1fa19a8bd $inst_name > /dev/null 2> /dev/null

openstack floating ip create public > /tmp/floating_ip.txt
floating_ip="$(grep floating_ip_address /tmp/floating_ip.txt)"
floating_ip=$(echo ${floating_ip} | grep -Eo "([0-9]{1,3}[\.]){3}[0-9]{1,3}")
openstack server add floating ip $inst_name ${floating_ip}
echo "ip_addr${floating_ip}:${dport}ip_addr"

iptables -t nat -I PREROUTING 1 -d 10.0.2.5 -p tcp --dport $dport -j DNAT --to-destination $floating_ip:22

rm /tmp/floating_ip.txt
