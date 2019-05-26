#!/bin/bash


source /root/keystonerc_admin

openstack server create --flavor m1.tiny --image cirros --nic net-id=62bc9b97-24fb-46d6-a484-afabbd2806b9 instance

neutron floatingip-create public -f shell > /root/floating_ip.txt
floating_ip="$(grep floating_ip_address /root/floating_ip.txt)"
nova floating-ip-associate instance ${floating_ip:21:-1}
echo "$floating_ip" >> /root/ip_asociadas.txt