from flask import Flask, request, render_template, abort, jsonify, after_this_request
from werkzeug.security import generate_password_hash, check_password_hash
import random, string
import os

import db_helper as db
from validator import validate_json, validate_schema, validate_token
from logger import Logger
from models import *

PORT = 5000
ADDR = "0.0.0.0"

app = Flask(__name__)
logger = Logger().get_logger()

# Help functions
def token_generator(size=15, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# User Management START
@app.route('/get_curr_user', methods=["GET"])
@validate_token
def get_curr_user():
    try:
        token = request.headers["token"]
        user = db.get_user_by_token(token)
        return jsonify({"username" : user.username, "token" : token}), 200
    except Exception as e:
        print ("[DEBUG] Error "+str(e))
        logger.error("Error in 'get_curr_user' : "+str(e)+" "+str(request.remote_addr))
        abort(500)

@app.route("/sign_up", methods=["POST"])
@validate_json
def sign_up():
    try:
        data = request.get_json(silent = True)
        if db.get_user_by_username(data["username"]) != None:
            return jsonify({"error": "This user is not available"}), 400
        else:
            saltedPsw = generate_password_hash(data["password"])
            if db.add(User(data["username"], saltedPsw)):
                logger.info("New account created:  "+data["username"]+" : "+str(request.remote_addr))
                return jsonify({}), 200
            else:
                abort(500)
    except Exception as e:
        print ("[DEBUG] Error "+str(e))
        logger.error("Error in 'sign_up' : "+str(e)+" "+str(request.remote_addr))
        abort(500)

@app.route('/login', methods=["POST"])
@validate_json
def login():
    try:
        data = request.get_json(silent = True) # username, password
        user = db.get_user_by_username(data["username"])
        if user == None:
            logger.warning("Login error, '"+data["username"]+"' user doesn't exist. "+str(request.remote_addr))
            return jsonify({"error": "User doesn't exist"}), 400
        elif not check_password_hash(user.password, data["password"]):
            logger.warning("Login error, '"+data["username"]+"' password is not correct "+str(request.remote_addr))
            return jsonify({"error": "Incorrect password"}), 400
        else:
            token = token_generator()
            db.delete_session_by_user(user.id)
            if not db.add(Session(user.id, token)):
                abort(500)

            return jsonify({"token" : token}), 200

    except Exception as e:
        print ("[DEBUG] Error "+str(e))
        logger.error("Error in 'login' : "+str(e)+" "+str(request.remote_addr))
        abort(500)

@app.route('/logout', methods=["GET"])
@validate_token
def logout():
    try:
        token = request.headers["token"]
        user = db.get_user_by_token(token)
        db.delete_session_by_user(user.id)
        return jsonify({}), 200
    except Exception as e:
        print ("[DEBUG] Error "+str(e))
        logger.error("Error in 'logout' : "+str(e)+" "+str(request.remote_addr))
        abort(500)

# User Management END
@app.route('/create_campaign', methods=["POST"])
@validate_token
@validate_json
@validate_schema("create_campaign")
def create_campaign():
    try:
        token = request.headers["token"]
        user = db.get_user_by_token(token)

        data = request.get_json(silent = True) # name & chclass

        name = data["name"]
        characters = data["characters"]

        for c in characters:
            if db.get_character_by_id(c) == None:
                return jsonify({"error": "Character is not correct"}), 400

        campaign = db.add(Campaign(user.id, name))
        if not campaign:
            abort(500)

        for c in characters:
            db.add(CampaignCharacter(c, campaign.id))


        return jsonify({"campaign_id" : campaign.id})

    except Exception as e:
        print("[DEBUG] Error in 'create_campaign' : "+str(e))
        logger.error("Error in 'create_campaign' : "+str(e)+" "+str(request.remote_addr))
        abort(500)

@app.route('/create_character', methods=["POST"])
@validate_token
@validate_json
@validate_schema("create_character")
def create_character():
    try:
        token = request.headers["token"]
        user = db.get_user_by_token(token)

        data = request.get_json(silent = True) # name & chclass
        ch_class = db.get_character_class_by_name(data["character_class"])
        name = data["name"]

        if ch_class == None:
            return jsonify({"error": "Character class is not correct"}), 400

        character = db.add(Character(name, ch_class.id, user.id))
        if not character:
            abort(500)

        return jsonify({"character_id" : character.id})

    except Exception as e:
        print("[DEBUG] Error in 'create_character' : "+str(e))
        logger.error("Error in 'create_character' : "+str(e)+" "+str(request.remote_addr))
        abort(500)


if __name__ == '__main__':
   logger.info("Web server has started")
   app.run(host=ADDR, port=PORT)
