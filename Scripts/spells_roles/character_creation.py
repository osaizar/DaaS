import os
import grp
import json
from urllib.request import urlopen
import random

STATS = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]


def roll_the_dice():
    dice = [0, 0, 0, 0]
    for i, die in enumerate(dice):
        dice[i] = random.randint(1, 6)
    dice[dice.index(min(dice))] = 0
    return sum(dice)


print("[S] Loading GM...")
# user's groups ids
gid = os.getgroups()
# group's name
group_names = []
for group in gid:
    gname = grp.getgrgid(group)[0]
    group_names.append(gname)

ch_class = group_names[1]
ch_class = "Warlock"  # TODO Delete
ch_lvl = group_names[2].replace("splv", "")
ch_lvl = 0  # TODO Delete
ch_name = os.getlogin()

origin_path = "json/"
with open(str(origin_path) + "classes.json") as f:
    classes = f.read()
classes = json.loads(classes)
classes = classes["results"]
hit_die = 0
for op_class in classes:
    if op_class["name"].upper() == str(ch_class).upper():
        url = op_class["url"]
        content = urlopen(url).read().decode("UTF-8")
        content = json.loads(content)
        hit_die = content["hit_die"]
        break

print("[GM] Hello! You must be " + str(ch_name) + ", the level " + str(ch_lvl)
      + " " + str(ch_class) + "! I've heard great things about you, but tell"
      + " me, what is your race?")

with open(str(origin_path) + "races.json") as f:
    races = f.read()
races = json.loads(races)
races = races["results"]
for race in races:
    print(race["name"])

ch_race = input("\n[S] Type your race: ")
print("[GM] Let me check...")

ability_bonuses = []
for race in races:
    if race["name"].upper() == str(ch_race).upper():
        url = race["url"]
        content = urlopen(url).read().decode("UTF-8")
        content = json.loads(content)
        ability_bonuses = content["ability_bonuses"]
        break

print("[GM] Oh! That's good to know, it will boost some of your stats. ")
print("     The stats are the values representing your habilities. We'll call"
      + " them:")
print("     Strenght [STR], Dexterity [DEX], Constitution [CON], "
      + "Intelligence [INT], Wisdom [WIS], and Charisma [CHA].")
print("     I will generate some random values now and you tell me to which"
      + " stat you want to assign each of them.")
print("[S] Your values are: ")

ability_scores = {"STR": 0, "DEX": 0, "CON": 0, "INT": 0, "WIS": 0, "CHA": 0}
dice_rolls = []

for i in range(0, 6):
    dice_rolls.append(roll_the_dice())

dice_rolls = sorted(dice_rolls, reverse=True)
print("[S] " + str(dice_rolls))

print("[GM] Now will go through each value, from highest to lowest. ")
print("     You just have to input the code of the stat you want to assign it to. ")
print("     Ready?")

for roll in dice_rolls:
    print("[S] Your highest available roll is: " + str(roll))
    print("    Which stat do you want to assign it to?")
    stat = input("    " + str(ability_scores) + "\n")
    ability_scores[str(stat.upper())] = roll

for i, bonus in enumerate(ability_bonuses):
    ability_scores[STATS[i]] = ability_scores[STATS[i]] + bonus

print("[GM] Well done! With this your character is complete. Let me show you"
      + "a summary of everything:")
print("[S] Name: " + str(ch_name))
print("    Race: " + str(ch_race))
print("    Class: " + str(ch_class))
print("    HP: " + str(hit_die))
print("    Ability scores: " + str(ability_scores))

print("[GM] That's about it when it comes to your character. Now that we have"
      + " gotten to an agreement, I shall show you the spells you have access"
      + " to. Enjoy ;)")

print("[S] Available spells for level " + str(ch_lvl) + " " + str(ch_class) + ":")
print("    spells")  # TODO add spell search
