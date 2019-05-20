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

@app.route('/get_curr_user', methods=["GET"])
@validate_token
def get_curr_user():
    try:
        token = request.headers["token"]
        user = db.get_user_by_token(token)
        return jsonify({"username" : user.username, "token" : token}), 200
    except Exception as e:
        logger.error("Errorea 'get_curr_user' : "+str(e)+" "+str(request.remote_addr))
        abort(500)

@app.route('/login', methods=["POST"])
@validate_json
def login():
    try:
        data = request.get_json(silent = True) # username, password
        user = db.get_user_by_username(data["username"])
        if user == None:
            logger.warning("Login errorea, '"+data["username"]+"' erabiltzailea ez da esistitzen. "+str(request.remote_addr))
            return jsonify({"error": "Erabiltzaile izena ez da zuzena"}), 400
        elif not check_password_hash(user.password, data["password"]):
            logger.warning("Login errorea, '"+data["username"]+"' erabiltzaileak ez du pasahitz egokia erabili. "+str(request.remote_addr))
            return jsonify({"error": "Pasahitza ez da zuzena"}), 400
        else:
            token = token_generator()
            db.delete_session_by_user(user.id)
            if not db.add(Session(user.id, token)):
                abort(500)

            return jsonify({"token" : token}), 200

    except Exception as e:
        logger.error("Errorea 'login' : "+str(e)+" "+str(request.remote_addr))
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
        logger.error("Errorea 'logout' : "+str(e)+" "+str(request.remote_addr))
        abort(500)


if __name__ == '__main__':
   logger.info("Web server has started")
   app.run(host=ADDR, port=PORT)
