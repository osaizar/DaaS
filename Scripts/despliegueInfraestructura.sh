#!/bin/bash

opcion="mal"
i=0
IFS="/"
if [ "$1" == "desplegar" ];
then
	opcion="bien"
	while read nombreProyecto nombreAlumno nombreUsuario password
	do
		existe="no"
	
        	echo "El nombre del proyecto es        : $nombreProyecto"
        	echo "El nombre del alumno es          : $nombreAlumno"
       		echo "El nombre de usuario es	       : $nombreUsuario"
	
		source admin-openrc.sh
	
		openstack user list -f json | python -m json.tool > /root/openstack_users.txt	

		
		num=$(jq '. | length' /root/openstack_users.txt)
        	for (( i=0; i<=$num; i++ ));
        	do
	        	nombre="$(cat /root/openstack_users.txt | jq '.['$i'].Name')"
                	if [ ${nombre:1:-1} == "$nombreUsuario" ];
               		then
                       		echo "¡El usuario ya existe!"
				existe="si"
                        	break
                	fi
        	done
	
		if [ "$existe" == "no" ]
		then
			echo "Empezando despliegue"

			openstack project create --domain default --description "Proyecto $nombreProyecto de $nombreAlumno" $nombreProyecto
			openstack user create --domain default --password $password $nombreUsuario
			openstack role add --project $nombreProyecto --user $nombreUsuario user

			source user-openrc.sh $nombreProyecto $nombreUsuario $password
			openstack token issue
		
			neutron net-create RedPrivada_$nombreUsuario
	
			neutron subnet-create RedPrivada_$nombreUsuario 172.16.0.0/24 --name SubRedPrivada_$nombreUsuario --dns-nameserver 8.8.8.8 --gateway 172.16.0.1
			neutron router-create Router_$nombreUsuario
			neutron router-interface-add Router_$nombreUsuario SubRedPrivada_$nombreUsuario
			neutron router-gateway-set Router_$nombreUsuario public

			neutron net-list -f json | python -m json.tool > /root/json.txt
			num=$(jq '. | length' /root/json.txt)
			echo "num:	$num"
			for (( i=0; i<=$num; i++ ));
			do
				echo "$i iteracion:"
				echo	"$(cat /root/json.txt | jq '.['$i'].name')"
				echo "RedPrivada_$nombreUsuario"
				nombre="$(cat /root/json.txt | jq '.['$i'].name')"
				if [ ${nombre:1:-1} == "RedPrivada_$nombreUsuario" ]
				then
					subnet_id="$(cat /root/json.txt | jq '.['$i'].id')"
					echo "subnet_id:	$subnet_id"
					break
				fi
			done
			ssh-keygen -q -N "" -f ~/.ssh/id_rsa_$nombreUsuario
			nova keypair-add --pub-key ~/.ssh/id_rsa_$nombreUsuario.pub key-$nombreUsuario
			nova secgroup-create secgroup-$nombreUsuario
			nova secgroup-add-rule secgroup-$nombreUsuario icmp -1 -1 0.0.0.0/0
			nova secgroup-add-rule secgroup-$nombreUsuario tcp 1 65535 0.0.0.0/0
			nova boot --flavor m1.tiny --image cirros --nic net-id=${subnet_id:1:-1} --security-group secgroup-$nombreUsuario --key-name key-$nombreUsuario private-instance-$nombreUsuario
			neutron floatingip-create public -f shell > /root/floating_ip.txt
			floating_ip="$(grep floating_ip_address /root/floating_ip.txt)"
			nova floating-ip-associate private-instance-$nombreUsuario ${floating_ip:21:-1}
			echo "$nombreUsuario/$floating_ip" >> /root/ip_asociadas.txt
		
		fi
	done < /root/ficheroAlumnos.txt 
	rm /root/json.txt
	rm /root/floating_ip.txt
	rm /root/openstack_users.txt

elif [ "$1" == "eliminar" ]
then
	opcion="bien"
	while read nombreProyecto nombreAlumno nombreUsuario password
	do
        		source user-openrc.sh $nombreProyecto $nombreUsuario $password
			rm -f ~/.ssh/id_rsa_$nombreUsuario.pub*
        		nova delete private-instance-$nombreUsuario
			nova secgroup-delete secgroup-$nombreUsuario
			nova keypair-delete key-$nombreUsuario
        		neutron router-gateway-clear Router_$nombreUsuario
        		neutron router-interface-delete Router_$nombreUsuario SubRedPrivada_$nombreUsuario
        		neutron router-delete Router_$nombreUsuario
        		neutron subnet-delete SubRedPrivada_$nombreUsuario
        		neutron net-delete RedPrivada_$nombreUsuario
        		source admin-openrc.sh
			openstack user delete $nombreUsuario
			openstack project delete $nombreProyecto
	done < /root/eliminarAlumnos.txt
else
	echo "Las opciones son: desplegar | eliminar"
fi

