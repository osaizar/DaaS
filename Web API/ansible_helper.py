from models import *
import db_helper as db
import os
import subprocess
import re

IP_RE = r"ip_addr(.*)ip_addr"
PREV_DIR = ""


# DO ANSIBLE THINGS
def generate_userlist(characters, campaign):
	with open(PREV_DIR+'csv/'+campaign.name+'_users.csv', 'w') as f: # TODO: dynamic name
		for i, c in enumerate(characters):
			passwd = db.get_user_by_id(c.user).password
			ch_class = db.get_character_class_by_id(c.ch_class).name
			f.write(c.name+","+passwd+","+str(i+1001)+","+ch_class+","+str(c.lvl)+"\n")

	
def generate_grouplist():
	with open(PREV_DIR+'csv/group_list.csv', 'w') as f:
		for i,c in enumerate(CLASSES):
			f.write(c+","+str(i+2001)+"\n")


def generate_admin_pass(admin):
	with open(PREV_DIR+'csv/mastercreds.csv', 'w') as f:
		f.write(admin.password)


def add_ip_to_inventory(ip):
	inv = open(PREV_DIR+'ansible/inventory', 'r').read()

	new_inv = ""
	for l in inv.split("\n"):
		new_inv += l+"\n"
		if "[instances]" in l:
			new_inv += str(ip)+"\n"

	with open(PREV_DIR+'ansible/inventory', 'w') as f:
		f.write(new_inv)


def start_instance():
	out = subprocess.getoutput("ansible-playbook -i "+PREV_DIR+"ansible/inventory "+PREV_DIR+"ansible/despliegue.yml")
	instance_ip = re.findall(IP_RE, out)[0]

	add_ip_to_inventory(instance_ip)

	print(subprocess.getoutput("ansible-playbook -i "+PREV_DIR+"ansible/inventory --limit "+instance_ip+" "+PREV_DIR+"ansible/create_class_groups.yml"))
	print(subprocess.getoutput("ansible-playbook -i "+PREV_DIR+"ansible/inventory --limit "+instance_ip+" "+PREV_DIR+"ansible/create_level_groups.yml"))
	print(subprocess.getoutput("ansible-playbook -i "+PREV_DIR+"ansible/inventory --limit "+instance_ip+" "+PREV_DIR+"ansible/create_user_fromfile.yml"))
	print(subprocess.getoutput("ansible-playbook -i "+PREV_DIR+"ansible/inventory --limit "+instance_ip+" "+PREV_DIR+"ansible/setpermissionss_bash.yml"))
	print(subprocess.getoutput("ansible-playbook -i "+PREV_DIR+"ansible/inventory --limit "+instance_ip+" "+PREV_DIR+"ansible/reset_root_pwd.yml"))

	return instance_ip