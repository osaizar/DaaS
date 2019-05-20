from urllib.request import urlopen
# import urllib2
import json


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
    # content = urllib2.urlopen(url).read()
    content = urlopen(url).read().decode("UTF-8")
    content = json.loads(content)
    classes = content["classes"]
    for chclass in classes:
        spells_by_class[chclass["name"]].append(url)

# save classes with their spells in a file
with open("spells_by_class.txt", "w") as f:
    for chclass in spells_by_class:
        if len(spells_by_class[chclass]):
            f.write(str(chclass) + "\n")
            f.write(str(spells_by_class[chclass]) + "\n")
