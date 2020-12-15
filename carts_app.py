import flask
import sqlite3
import pprint
from app_classes import *
from datetime import date, datetime
from flask import request, jsonify, abort, g, Flask

app = flask.Flask(__name__)
app.config.from_envvar('APP_CONFIG')

DATABASE = './database/database.db'
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


###############################
# Auxillary Backend Functions #
###############################

# def get_userinfo(email):
#     conn = get_db()
#     c = conn.cursor()
#     c.execute("SELECT user_id, user_city, user_zip, user_state FROM users WHERE email=?", (email,))
#     id, city, zip, state = c.fetchone()

#     return (id, city, zip, state)


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


@app.route('/api/carts', methods=['GET'])
def get_cart():
    """ Gets Current Cart for a user"""
    if not request.json:
        abort(400, description="Input data-type not JSON.")

    query_params = request.get_json()
    user = UserObject(query_params['email'], get_db())

    conn = get_db()
    conn.row_factory = lambda cursor, row: row
    c = conn.cursor()
    c.execute("SELECT * FROM products INNER JOIN cart ON products.product_id = cart.product_id WHERE cart.user_id = ?", (user.id,))
    cart = c.fetchall()
    subtotal = sum([foo[2] for foo in cart])
    data = {"Items": [{"ID": foo[0], "Name": foo[1], "Price": foo[2]} for foo in cart]}
    data["Subtotal"] = subtotal
    app.logger.info(f"\n\n{cart}\n\n{data}\n\n")

    return jsonify(data), 200





@app.route('/api/carts', methods=['PUT'])
def add_item():
    """ Adds an item to a users cart, item must come from the same restaurant ID """
    if not request.json:
        abort(400, description="Input data-type not JSON.")

    query_params = request.get_json()


    if 'items' not in query_params.keys():
        app.logger.info(f"{query_params.keys()}Cart Add parameters missing, aborting: PASS")
        abort(400, description="Missing parameter(s): items")
    if 'email' not in query_params.keys():
        app.logger.info(f"'email' parameter not in json payload keys")
        abort(400, description="Missing parameter(s): email")


    p_ids = query_params['items']
    email = query_params['email']
    app.logger.info(f"\n\nPID's in parameters: {p_ids}\n\n")
    user_info = UserObject(email, get_db())

    conn = get_db()
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    temp = []

    for id in p_ids:
        foo = c.execute("SELECT restaurant_id FROM products WHERE product_id=?", (id,)).fetchall()
        app.logger.info(f"\n\nExecuting query for adding to restaurant_id's: {foo}\n\n")
        temp += foo

    if not all(x == temp[0] for x in temp):
        app.logger.info(f"Restaurants do not match when adding items to cart: PASS")
        abort(400, description="Mismatching restaurant id's. Items must be from the same restaurant.")

    for item in p_ids:
        app.logger.info(f"\n\nadding item id: {item} to {user_info.email}'s cart\n\n")
        c.execute("INSERT INTO cart (user_id, product_id) VALUES(?,?)", (user_info.id, item))
        conn.commit()



    app.logger.info(f"\n\nRestaurant ID's that belond to items, all same. {temp}\n\n")

    rdata = {"Added": [{"item": item} for item in p_ids]}

    return jsonify(rdata), 201

@app.route('/api/carts', methods=['DELETE'])
def delete_item():
    """ Remove items from a list of items (can be only one value as well) from a users cart """
    if not request.json:
        abort(400, description="Input data-type not JSON.")

    query_params = request.get_json()
    user = UserObject(query_params['email'], get_db())
    conn = get_db()
    c = conn.cursor()

    p_ids = query_params['items']

    temp = []
    for item in p_ids:
        c.execute("DELETE FROM cart WHERE user_id = ? AND product_id = ?", (user.id, item))
        conn.commit()
        temp.append(item)

    data = {"Deleted": [{"Item ID": id} for id in p_ids]}

    return jsonify(data), 204


@app.route('/api/carts', methods=['POST'])
def make_order():
    """ Sends items in the cart to the orders database """
    if not request.json:
        abort(400, description="Input data-type not JSON.")
    
    now = datetime.now()
    created = now.strftime("%m/%d/%y %H:%M:%S")

    app.logger.info(f"\n\nCreated Time is: {created}\n\n")

    query_params = request.get_json()
    user = UserObject(query_params['email'], get_db())
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO orders(user_id, product_id) SELECT user_id, product_id FROM cart WHERE user_id=?", (user.id,))
    c.execute("UPDATE orders SET created_at = ? WHERE user_id=?", (created, user.id))
    conn.commit()

    c.execute("DELETE FROM cart WHERE user_id=?", (user.id,))
    conn.commit()
    return jsonify({"message": f"Order created at {created}"}),200