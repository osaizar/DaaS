#!/bin/bash

source /opt/stack/devstack/openrc
inst_name="inst_$RANDOM"

openstack server create --flavor DandD --image ubuntu --nic net-id=c45da0d4-ec13-4607-a416-82c1fa19a8bd $inst_name > /dev/null

openstack floating ip create public > /tmp/floating_ip.txt
floating_ip="$(grep floating_ip_address /tmp/floating_ip.txt)"
openstack server add floating ip $inst_name ${floating_ip:24:-1}
echo "${floating_ip:24:-1}"
rm /tmp/floating_ip.txt
