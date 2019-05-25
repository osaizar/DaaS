from models import *
import db_helper as db


# DO ANSIBLE THINGS
def generate_userlist(characters, campaign):
	with open('csv/'+campaign.name+'_users.csv', 'w') as f: # TODO: dynamic name
		for i, c in enumerate(characters):
			passwd = db.get_user_by_id(c.user).password
			ch_class = db.get_character_class_by_id(c.ch_class).name
			f.write(c.name+","+passwd+","+str(i+1001)+","+ch_class+","+str(c.lvl)+"\n")

	

def generate_grouplist():
	with open('csv/group_list.csv', 'w') as f:
		for i,c in enumerate(CLASSES):
			f.write(c+","+str(i+2001)+"\n")
