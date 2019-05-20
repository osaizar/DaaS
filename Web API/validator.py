from functools import wraps
from datetime import datetime
import db_helper as db
from logger import Logger
from flask import jsonify, request, abort

logger = Logger().get_logger()

def validate_json(f):
    @wraps(f)
    def wrapper(*args, **kw):
        try:
            js = request.json
            if js == None:
                raise Exception
        except:
            logger.error("400 Error, JSON is not correct "+str(request.remote_addr))
            return jsonify({"error": "Incorrect request"}), 400
        return f(*args, **kw)
    return wrapper

def validate_token(f):
    @wraps(f)
    def wrapper(*args, **kw):
        try:
            if "token" not in request.headers:
                logger.warning("400 Error, no token provided."+str(request.remote_addr))
                return jsonify({"error" : "No token provided"}), 400

            token = request.headers["token"]
            user = db.get_user_by_token(token)
            if user == None:
                logger.warning("400 Error, incorrect token. "+str(request.remote_addr))
                return jsonify({"error" : "Incorrect token"}), 400

            session = db.get_session_by_token(token)

            if session.check_token_expired():
                logger.warning("400 Error,"+user.username+" users token is expired "+str(request.remote_addr))
                return jsonify({"error" : "Incorrect token"}), 400

        except Exception as e:
            logger.error("Exception 'validate_token': "+str(e)+" "+str(request.remote_addr))
            return jsonify({"error": "Incorrect request"}), 400

        return f(*args, **kw)
    return wrapper

def validate_schema(name):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            try:
                validate(request.json, name)
            except Exception as e:
                return jsonify({"error": e.message}), 400
            return f(*args, **kw)
        return wrapper
    return decorator

def validate(input, name): # TODO: input validation
    if name == "create_campaign":
        validate_create_campaign(input)
    if name == "create_character":
        validate_create_character(input)
    else:
        Exception("No schemas with that name")

def validate_create_campaign(input):
    try:
        name = input["name"]
        characters = input["characters"]
        ch0 = input["characters"][0]
    except:
        Exception("Invalid request")

def validate_create_character(input):
    try:
        name = input["name"]
        ch_class = input["character_class"]
    except:
        Exception("Invalid request")
