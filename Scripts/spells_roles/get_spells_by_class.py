from urllib.request import urlopen
# import urllib2
import json
import os

# ruta_patras = /root/spells/
ruta_patras = "/home/ainhoa/repos/DaaS/Scripts/spells_roles/"

PARENT_FOLDER = "ch_class/"
SOURCE_PATH = "sp_lvl/"

# load all classes json
with open("classes.json") as f:
    classes = f.read()
classes = json.loads(classes)
classes = classes["results"]

# initialize spell list
spells_by_class = {}
for chclass in classes:
    spells_by_class[chclass["name"]] = []

# load all spells json
with open("spells.json") as f:
    spells = f.read()
spells = json.loads(spells)
spells = spells["results"]

# sepparate spells in lists per class
for spell in spells:
    url = spell["url"]
    # replace / with _ so it can be the name of a file
    name = spell["name"]
    name = name.replace("/", "_")
    name = name.replace(" ", "_")
    # content = urllib2.urlopen(url).read()
    content = urlopen(url).read().decode("UTF-8")
    content = json.loads(content)
    lvl = content["level"]
    # check the level of the spell to see which folder to put it into
    lvl = content["level"]
    if int(lvl) < 0:
        lvl = 0
    obj = {"name": name, "level": lvl}
    classes = content["classes"]
    for chclass in classes:
        spells_by_class[chclass["name"]].append(obj)

# save classes with their spells' links
for chclass in spells_by_class:
    class_spells = spells_by_class[chclass]
    if len(class_spells):
        # create folders for storing the spells by level
        for i in range(0, 10):
            newpath = PARENT_FOLDER + str(chclass) + "/" + str(i)
            if not os.path.exists(newpath):
                os.makedirs(newpath)
        # create spell files' links
        for spell in class_spells:
            sp_level = str(spell["level"])
            sp_name = str(spell["name"])
            src = ruta_patras + SOURCE_PATH + sp_level + "/" + sp_name + ".json"
            dst = ruta_patras + PARENT_FOLDER + str(chclass) + "/" + sp_level + "/" + sp_name + ".json"
            os.symlink(src, dst)