import json
from sqlite3.dbapi2 import DatabaseError
import flask
import sqlite3
import pprint
from app_classes import Authenticate, UserObject, Registration
from flask import g, request, jsonify, abort
from werkzeug.security import generate_password_hash, check_password_hash

app = flask.Flask(__name__)
app.config.from_envvar('APP_CONFIG')

DATABASE = './database/database.db'
required_registration_args = app.config['CREATE_USER_REQUIRED']
required_auth_args = app.config['AUTH_USER_REQUIRED']

###################################
#   Error Handling Definitions    #
###################################

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify(error=str(e)), 405

@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400

@app.errorhandler(500)
def internal_error(e):
    return jsonify(error=str(e)), 500


#####################################
#   Database Handling Definitions   #
#####################################

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def end_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


#############################
#   Endpoint Definitions    #
#############################

@app.route('/api/users', methods=['DELETE'])
def delete_user():
    if not request.json:
        abort(400, description="Input data-type is not JSON.")

    query_params = request.get_json()

    if not all(elem in query_params.keys() for elem in required_auth_args):
        app.logger.info(f"DELETE USER: ABORTED; Missing parameter value(s). PASS")
        abort(400, description="Delete User, missing parameter value")
        # return jsonify({"message":{"error":"Missing parameter value"}}), 400
    auth = Authenticate(query_params,get_db())

    if auth.check() == False:
        app.logger.info(f"User could not be authenticated, aborting with HTTP 400. PASS")
        abort(400, description="Authenticate: Incorrect Password")
        # return jsonify({"message":{"error": "Incorrect pasword"}}), 400

    user = UserObject(query_params['email'])
    database = get_db()
    c = database.cursor()
    c.execute("SELECT COUNT(*) FROM orders WHERE user_id = ?", (user.id,))
    r = c.fetchall()[0][0]
    if r > 0:
        abort(400, description="Error: Cannot delete account while orders are still active on the account")
        # return jsonify({"message":{"error": "Cannot delete account while orders are still active on the account."}}), 400
    c.execute("DELETE FROM users WHERE user_id = ?", (user.id,))
    database.commit()
    # Should use rollbacks if database errors, should change code to upate this later if we have time. 
    return jsonify({"message": "Account deleted."}), 200

    


@app.route('/api/users', methods=['GET']) # Endpoint that authenticates users. Takes HTTP GET method. json payload. Parameters are (email, password)
def authenticate_user():
    if not request.json:
        abort(400, description="Input data-type is not JSON.")
    
    query_params = request.get_json()
    
    if not all(elem in query_params.keys() for elem in required_auth_args):
        return jsonify({"message":{"error":"Missing parameter value"}}), 400
    
    user_auth = Authenticate(query_params, get_db())
    if user_auth.check():
        return jsonify({"message":{"verify": True}}), 200
    else:
        return jsonify({"message":{"verify": False}}), 400


@app.route('/api/users', methods=['PUT']) # Endpoint to register users, takes HTTP "PUT" method. Data must be json payload. 
def user_creator():
    if not request.json:
        abort(400, description="Input data-type is not JSON.")
    
    query_params = request.get_json()
    if not all(elem in required_registration_args for elem in query_params.keys()):
        app.logger.info(f"\nRegistration aborted. Logging keys for Registration query parameters: {list(query_params.keys())} \n Logging arguments required for registration: {required_registration_args}")
        abort(400, description="Missing required Parameter(s).")
    
    if not 'password' in query_params.keys():
        app.logger.info(f"Password not found in parameters for creating ")
        abort(400, description="Registration Aborted, no password given.")

    params = Registration(query_params)

    database = get_db()
    c = database.cursor()
    c.execute("SELECT EXISTS(SELECT email FROM users WHERE email=? LIMIT 1)", (params.email,))
    if c.fetchall()[0][0] > 0:
        abort(409, description="Account for email already exists.")
    c.execute("INSERT INTO users (email, hash_pass, first_name, last_name, user_address, user_city, user_zip, user_state, user_phone) VALUES (?,?,?,?,?,?,?,?,?)", (params.email, params.hash_pass, params.first, params.last, params.address, params.city, params.zip, params.state, params.phone))
    database.commit()
    c.close()
   

    return jsonify({"message":{"status": "New user created sucsessfully."}}), 201



if __name__ == '__main__':
    app.run()