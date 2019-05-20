from database import db_session
from sqlalchemy import and_, or_, func
from models import Device, User, Session, Message, Permission

def add(data):
    try:
        db_session.add(data)
        db_session.commit()
        return data
    except:
        db_session.flush()
        return False

# User and Session

def get_user_by_id(userId):
    try:
        return User.query.filter(User.id == userId).one()
    except:
        return None

def get_user_by_username(username):
    try:
        return User.query.filter(User.username == username).first()
    except:
        return None

def get_user_by_token(token):
    try:
        session = get_session_by_token(token)
        return get_user_by_id(session.user)
    except:
        return None

def get_session_by_token(token):
    try:
        return Session.query.filter(Session.token == token).one()
    except:
        return None

def get_all_users():
    try:
        return User.query.all()
    except:
        return None

def delete_session_by_user(userId):
    try:
        Session.query.filter(Session.user == userId).delete()
        db_session.commit()
        return True
    except:
        return None
