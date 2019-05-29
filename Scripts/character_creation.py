#!/usr/bin/python3

import os
import grp
import json
from urllib.request import urlopen
import random
import subprocess

STATS = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]


def roll_the_dice():
    dice = [0, 0, 0, 0]
    for i, die in enumerate(dice):
        dice[i] = random.randint(1, 6)
    dice[dice.index(min(dice))] = 0
    return sum(dice)


print("[S]\tLoading GM...")
# user's groups ids
gid = os.getgroups()
# group's name
group_names = []
for group in gid:
    gname = grp.getgrgid(group)[0]
    group_names.append(gname)

ch_class = group_names[1]
ch_lvl = group_names[2].replace("splv", "")
ch_name = os.getlogin()

classes = {"count":12,"results":[{"name":"Barbarian","url":"http://www.dnd5eapi.co/api/classes/1"},{"name":"Bard","url":"http://www.dnd5eapi.co/api/classes/2"},{"name":"Cleric","url":"http://www.dnd5eapi.co/api/classes/3"},{"name":"Druid","url":"http://www.dnd5eapi.co/api/classes/4"},{"name":"Fighter","url":"http://www.dnd5eapi.co/api/classes/5"},{"name":"Monk","url":"http://www.dnd5eapi.co/api/classes/6"},{"name":"Paladin","url":"http://www.dnd5eapi.co/api/classes/7"},{"name":"Ranger","url":"http://www.dnd5eapi.co/api/classes/8"},{"name":"Rogue","url":"http://www.dnd5eapi.co/api/classes/9"},{"name":"Sorcerer","url":"http://www.dnd5eapi.co/api/classes/10"},{"name":"Warlock","url":"http://www.dnd5eapi.co/api/classes/11"},{"name":"Wizard","url":"http://www.dnd5eapi.co/api/classes/12"}]}
classes = classes["results"]
hit_die = 0

for op_class in classes:
    if op_class["name"].upper() == str(ch_class).upper():
        url = op_class["url"]
        content = urlopen(url).read().decode("UTF-8")
        content = json.loads(content)
        hit_die = content["hit_die"]
        break

print("[GM]\tHello! You must be " + str(ch_name) + ", the level " + str(ch_lvl)
      + " " + str(ch_class) + "!\n\tI've heard great things about you, but"
      + " tell me, what is your race?")

races = {"count":9,"results":[{"name":"Dwarf","url":"http://www.dnd5eapi.co/api/races/1"},{"name":"Elf","url":"http://www.dnd5eapi.co/api/races/2"},{"name":"Halfling","url":"http://www.dnd5eapi.co/api/races/3"},{"name":"Human","url":"http://www.dnd5eapi.co/api/races/4"},{"name":"Dragonborn","url":"http://www.dnd5eapi.co/api/races/5"},{"name":"Gnome","url":"http://www.dnd5eapi.co/api/races/6"},{"name":"Half-Elf","url":"http://www.dnd5eapi.co/api/races/7"},{"name":"Half-Orc","url":"http://www.dnd5eapi.co/api/races/8"},{"name":"Tiefling","url":"http://www.dnd5eapi.co/api/races/9"}]}
races = races["results"]
for race in races:
    print(race["name"])

ch_race = input("\n[S]\tType your race: ")
print("[GM]\tLet me check...")

ability_bonuses = []
for race in races:
    if race["name"].upper() == str(ch_race).upper():
        url = race["url"]
        content = urlopen(url).read().decode("UTF-8")
        content = json.loads(content)
        ability_bonuses = content["ability_bonuses"]
        break

print("[GM]\tOh! That's good to know, it will boost some of your stats. "
      + "\n\tThe stats are the values representing your habilities. We'll call"
      + " them:\n\tStrenght [STR], Dexterity [DEX], Constitution [CON], "
      + "Intelligence [INT], Wisdom [WIS], and Charisma [CHA].\n\tI will"
      + " generate some random values now and you tell me to which stat you"
      + " want to assign each of them.")
print("[S]\tYour values are: ")

ability_scores = {"STR": 0, "DEX": 0, "CON": 0, "INT": 0, "WIS": 0, "CHA": 0}
dice_rolls = []

for i in range(0, 6):
    dice_rolls.append(roll_the_dice())

dice_rolls = sorted(dice_rolls, reverse=True)
print("[S]\t" + str(dice_rolls))

print("[GM]\tNow will go through each value, from highest to lowest. "
      + "\n\tYou just have to input the code of the stat you want to assign it"
      + " to.\n\tReady?")

for roll in dice_rolls:
    print("[S]\tYour highest available roll is: " + str(roll) + "\n\tWhich"
          + " stat do you want to assign it to?")
    stat = input("\t" + str(ability_scores) + "\n")
    ability_scores[str(stat.upper())] = roll

for i, bonus in enumerate(ability_bonuses):
    ability_scores[STATS[i]] = ability_scores[STATS[i]] + bonus

print("[GM]\tWell done! With this your character is complete. Let me show you"
      + "a summary of everything:\n[S]\t\nName: " + str(ch_name) + "\n\tRace: "
      + str(ch_race) + "\n\tClass: " + str(ch_class) + "\n\tHP: "
      + str(hit_die) + "\n\tAbility scores: " + str(ability_scores))

print("[GM]\tThat's about it when it comes to your character.\n\tNow that we"
      + " have gotten to an agreement, I shall show you the spells you have"
      + " access to. Enjoy ;)")

print("[S]\tAvailable spells for level " + str(ch_lvl) + " " + str(ch_class)
      + ":")
spells_path = "/opt/ch_class/" + ch_class + "/" + ch_lvl + "/"
available_spells = subprocess.check_output(['ls', spells_path]).decode('utf-8')
print("\t" + str(available_spells))

character_path = "/home/" + str(ch_name) + "/character.txt"
with open(character_path, "w") as f:
    f.write("Name: " + str(ch_name) + "\n\tRace: "
            + str(ch_race) + "\n\tClass: " + str(ch_class) + "\n\tHP: "
            + str(hit_die) + "\n\tAbility scores: " + str(ability_scores)
            + "\nAvailable spells:\n" + str(available_spells))

print("[GM]\t A file has been created in " + str(character_path) + " with this"
      + " information.\n\t Have, fun! :D")
finish = "n"
while(finish!="y"):
  finish = input("[S]\tType 'y' to exit")


