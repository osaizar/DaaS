from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date, DateTime
import datetime, string, random
from database import Base

CLASSES = ["Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard"]


# User & Session control
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def serialize(self):
        return {"id" : self.id , "username" : self.username}

class Session(Base):
    __tablename__ = "session"
    user = Column(Integer, ForeignKey("user.id"), primary_key=True)
    token = Column(String(20), nullable=False)
    token_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, user, token):
        self.user = user
        self.token = token

    def check_token_expired(self):
        cur_time = datetime.datetime.utcnow()
        expire_date = self.token_date + datetime.timedelta(days=2) # tokenak 2 egun irauten ditu
        if cur_time > expire_date:
            return True
        else:
            return False

# Our things
class Campaign(Base):
    __tablename__ = "campaign"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    master = Column(Integer, ForeignKey("user.id"))
    # TODO: server id...

    def __init__(self, master, name):
        self.master = master
        self.name = name


class Character(Base):
    __tablename__ = "character"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(Integer, ForeignKey("user.id"))
    name = Column(String(250), nullable=False)
    lvl = Column(Integer, nullable=False)
    ch_class = Column(Integer, ForeignKey("ch_class.id"))

    def __init__(self, name, ch_class, lvl, user):
        self.name = name
        self.ch_class = ch_class
        self.lvl = lvl
        self.user = user


class CharacterClass(Base):
    __tablename__ = "ch_class"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)

    def __init__(self, name):
        self.name = name


class CampaignCharacter(Base):
    __tablename__ = "campaign_character"
    id = Column(Integer, primary_key=True, autoincrement=True)
    character = Column(Integer, ForeignKey("character.id"), nullable=False)
    campaign = Column(Integer, ForeignKey("campaign.id"), nullable=False)

    def __init__(self, character, campaign):
        self.character = character
        self.campaign = campaign
