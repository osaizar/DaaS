# 1

from urllib.request import urlopen
# import urllib2
import json
import os

PARENT_FOLDER = "/opt/sp_lvl/"

# load all spells json
with open("spells.json") as f:
    spells = f.read()
spells = json.loads(spells)
spells = spells["results"]

# create folders for storing the spells by level
for i in range(0, 10):
    newpath = PARENT_FOLDER + str(i)
    if not os.path.exists(newpath):
        os.makedirs(newpath)

# retrieve all spell info
for spell in spells:
    url = spell["url"]
    # content = urllib2.urlopen(url).read()
    content = urlopen(url).read().decode("UTF-8")
    content = json.loads(content)
    # replace / with _ so it can be the name of a file
    name = spell["name"]
    name = name.replace("/", "_")
    name = name.replace(" ", "_")
    # check the level of the spell to see which folder to put it into
    lvl = content["level"]
    if int(lvl) < 0:
        lvl = 0
    # save each spells into a json file
    with open(PARENT_FOLDER + str(lvl) + "/" + str(name) + '.json', 'w') as fp:
        json.dump({name: content}, fp)
