# Inspired by <https://github.com/vishnuvardhan-kumar/loadbalancer.py>
#
#   $ python3 -m pip install Flask python-dotenv
#
# TODO: 
#   - Fix round robin load balancer know when to skip a broken endpoint
#   - Program health checks on broken endpoints to add them back into the pools
#   - Program broken endpoints to be added into the DO NOT FORWARD list 
#   - Add user authentication decorators to block functionality behind sessions or auth headers
#   - Maybe rewrite the whole thing 

import sys

import flask
import requests
import itertools
import werkzeug
from flask import jsonify, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.exceptions import HTTPException

app = flask.Flask(__name__)
app.config.from_envvar('APP_CONFIG')

# auth = HTTPBasicAuth()

users_list = app.config['UPSTREAM_USERS'] # Assign initial URLs for each service from the list in the config
restaurants_list = app.config['UPSTREAM_RESTAURANTS']
carts_list = app.config['UPSTREAM_CARTS']

pool = {'users':users_list, 'restaurants':restaurants_list, 'carts':carts_list} # Dict containing different service types as keys, and URLs as values

upstream_users = itertools.cycle(pool['users'])
upstream_restaurants = itertools.cycle(pool['restaurants'])
upstream_carts = itertools.cycle(pool['carts'])

blocklist = [] # List containing the upstream URLs that have encountered problems and should not be forwarded to by the balancer

def rr_balancer(uri):
    """ Takes a label for which service. Returns a base URL. """
    if uri == '/api/users':
        return next(upstream_users)
    if uri == '/api/restaurants':
        return next(upstream_restaurants)
    if uri == '/api/carts':
        return next(upstream_carts)


## To be implemented later ##

# @auth.verify_password
# def verify_password(username, password):
#     """ Takes a username and password from httpie -a switch returns true or false result from 
#         authenticateUser of a users service instance """

#     url = "http://localhost:5200/api/authenticateUser" # set url to send authenticateUser request to 
#     data = {'username': username, 'password': password}
#     req = requests.post(url, json=data) # Send request 
#     return req.json()['message']['verify'] # If request successful, return the result



@app.errorhandler(500)
def req_exept(e):
    return jsonify(error=str(e)), 500


@app.errorhandler(404)
def route_page(upstream):
    try:
        response = requests.request(
            flask.request.method,
            upstream + flask.request.full_path,
            data=flask.request.get_data(),
            headers=flask.request.headers,
            cookies=flask.request.cookies,
            stream=True,
        )
        app.logger.info(f"{response}, {upstream}") # Log the response and URL to see if requests are being routed from the URLs in the pool




    except requests.exceptions.RequestException as e:
        app.log_exception(sys.exc_info())
        return flask.json.jsonify({
            'method': e.request.method,
            'url': e.request.url,
            'exception': type(e).__name__,
        }), 503
        

    headers = remove_item(
        response.headers,
        'Transfer-Encoding',
        'chunked'
    )

    return flask.Response(
        response=response.content,
        status=response.status_code,
        headers=headers,
        direct_passthrough=True,
    )


def remove_item(d, k, v):
    if k in d:
        if d[k].casefold() == v.casefold():
            del d[k]
    return dict(d)




##################
# Users Services #
##################

@app.route('/api/users', methods=['GET', 'PUT', 'DELETE'])
def user_authenticator():
    uri = request.path
    upstream = rr_balancer(uri)
    return route_page(upstream)


#######################
# RESTAURANTS SERVICE #
#######################

@app.route('/api/restaurants', methods=['GET', 'PUT', 'POST', 'DELETE'])
def restaurant_creator():
    uri = request.path
    upstream = rr_balancer(uri)
    return route_page(upstream)

#################
# CARTS SERVICE #
#################

@app.route('/api/carts', methods=['GET', 'PUT', 'POST', 'DELETE'])
def carts_get_cart():
    uri = request.path
    upstream = rr_balancer(uri)
    return route_page(upstream)

# @app.route('/api/carts', methods=['POST'])
# def carts_make_order():
#     uri = request.path
#     upstream = rr_balancer(uri)
#     return route_page(upstream)
