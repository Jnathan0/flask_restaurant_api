import flask
import sqlite3
import pprint
from app_classes import *
from datetime import date
from flask import request, jsonify, abort, g, Flask

app = flask.Flask(__name__)
app.config.from_envvar('APP_CONFIG')

DATABASE = './database/database.db'
required_auth_args = app.config['AUTH_USER_REQUIRED']
required_restaurant_args = app.config['CREATE_RESTAURANT_REQUIRED']
advanced_args = app.config['ADVANCED_ARGS']


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


###############################
# Auxillary Backend Functions #
###############################

def get_products(id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE restaurant_id = ?", (id,))
    data = c.fetchall()
    app.logger.info(f"\n\nGetting data from db for get_products(): {data}\n\n")
    return data



#############################
#   Endpoint Definitions    #
#############################


@app.route('/api/restaurants', methods=['GET'])

def get_restaurants():
    """ Get a list of restaurants based on certain parameters, return a list of rstaurants that satisfy those parameters """
    if not request.json:
        abort(400, description="Input data-type is not JSON.")
    query_params = request.get_json()
    num_params = len(query_params)
    
    if num_params<=1:
        if "zipcode" not in query_params:
            app.logger.info(f"Zipcode not found in parameters: PASS")
            abort(400, description="Must provide at least ZIP CODE if only one parameter is to be specified.")
        elif num_params==0:
            app.logger.info(f"Special Case Where No Parameters are sent: PASS")
            abort(400, description="Insufficient parameters specified (must specify at least 'zipcode')")


    params = Query_Advanced(query_params)
    app.logger.info(f"Object created parameters: {params.__attrlist__()}")
    try:
        params.__query_map__(advanced_args)
        app.logger.info(f"Query Map created for params object: PASS")
    except Exception as e:
        app.logger.info(f"Error raised for making params.__query_map__\n{e}\n")
        abort(400, description=f"{e}")

    app.logger.info(f"This is supposed to be a tuple of db name and value: {params.zipcode}")
    queries = []
    values = []
    for item in params.__attrlist__():
        queries.append(params.__dict__[item][0])
        values.append(params.__dict__[item][1])
        app.logger.info(f"Variable Name: {item} - Variable Value: {params.__dict__[item]}")
    full_query = build_query(queries, "restaurants")
    app.logger.info(f"Built query is:{full_query}")
    sqlite_connection = get_db()
    values = tuple(values)
    app.logger.info(f"Displaying values for query placeholders. \n{values}")
    data = get_query(full_query, values, sqlite_connection)
    data = {"Restaurants":[{"Address": item[2], "Business Hours": item[8], 'Name': item[1], 'ID Number': item[0], 'Zipcode': item[5], 'Pickup': item[12], 'Delivery': item[11], 'Latitude': item[9], 'Longitude': item[10], "Phone": item[7], "City": item[4], "Description": item[3], 'State': item[6]} for item in data]}
    for item in data['Restaurants']:
        app.logger.info(f"\n\nItem ID number IS: {item['ID Number']} PASS\n\n")
        p = get_products(item['ID Number'])
        item.update({"_Products": [{"ID": foo[0], "Name": foo[1], "Desc": foo[3], "Price": foo[2], "Stock": foo[5]} for foo in p]})

    app.logger.info(f"\n Data build for query against restuaraunts: {data}\n")
    return (jsonify(data),200)
    

@app.route('/api/restaurants', methods=['PUT'])
def create_restaurant():
    if not request.json:
        abort(400, description="Input data-type is not JSON.")
    
    query_params = request.get_json()
    if not all(elem in required_restaurant_args for elem in query_params.keys()):
        app.logger.info(f"\n{list(query_params.keys())} \n{required_restaurant_args}")
        return jsonify({"message":{"error":"Missing required parameter value"}}), 400

    params = Restaurant_Registration(query_params)

    database = get_db()
    c = database.cursor()
    c.execute("SELECT EXISTS(SELECT restaurant_address, restaurant_city FROM restaurants WHERE restaurant_address=? AND restaurant_city=?)", (params.address, params.city))
    if c.fetchall()[0][0] != 0:
        return jsonify({"message":{"error": "Restaurant already exists for this address at this city."}}), 409

    c.execute("INSERT INTO restaurants (restaurant_name, restaurant_address, restaurant_city, restaurant_zip, restaurant_state, restaurant_phone, latitude, longitude, delivery, pickup, hours) VALUES (?,?,?,?,?,?,?,?,?,?)", (params.name, params.address, params.city, params.zip, params.state, params.phone, params.lat, params.long, params.delivery, params.pickup, params.hours))
    database.commit()
    c.close()

    return jsonify({"message":{"status": "New restaurant added to catalog."}}), 201


   



@app.route('/api/restaurants', methods=['DELETE'])
def addFollow():
    if not request.json:
        abort(400, description="Input data-type is not JSON.")
    query_params = request.get_json()

    if len(query_params)!=3:
        abort(400, description="Incorrect amount of parameters")

    username = query_params['username']

    database = get_db()
    c = database.cursor()
    c.execute("SELECT users.username, posts.date, posts.body FROM (SELECT * FROM posts WHERE user_id IN (SELECT subscribed_to_id FROM relationships WHERE user_id=(SELECT user_id FROM users WHERE username=?))) AS POSTS INNER JOIN users ON posts.user_id = users.user_id ORDER BY posts.date DESC LIMIT 25", (username,))
    data = c.fetchall()
    data = {"posts":[{"username": post[0], "date": post[1], "body":post[2]} for post in data]}
    return jsonify(data), 200

if __name__ == '__main__':
    app.run()