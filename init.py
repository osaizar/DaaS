# coding: latin-1
from database import Base, db_session, engine
from werkzeug.security import generate_password_hash
from sqlalchemy_utils import database_exists, create_database, drop_database
from models import CharacterClass

CLASSES = ["Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard"]

def add(data):
    db_session.add(data)
    db_session.commit()

def add_character_classes():
    for c in CLASSES:
        add(CharacterClass(c))


def main():

    if database_exists(engine.url):
        ans = input("[+] DaaS database found, delete? (y/n) ")
        if ans.lower() == "y":
            ans = input("[!] Are you sure? (y/n) ")
            if ans.lower() == "y":
                print ("[+] Deleting database...")
                drop_database(engine.url)
                print ("[+] Creating new database...")
                create_database(engine.url)
                Base.metadata.create_all(engine)
                add_character_classes()
    else:
        ans = input("[+] DaaS database not found, create it? (y/n) ")
        if ans.lower() == "y":
                print ("[+] Creating new database...")
                create_database(engine.url)
                Base.metadata.create_all(engine)
                print("[+] Filling database")
                add_character_classes()

if __name__ == "__main__":
    main()
