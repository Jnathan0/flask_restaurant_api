import sqlite3
from sqlite3.dbapi2 import DatabaseError
from types import MethodType
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

#######################
# AUXILLARY FUNCTIONS #
#######################

def build_query(list, table_name):
    """ Takes a list of table attributes to use with a "SELECT" statement and a table name to query against.
    Returns a string that will result in the SQL query"""
    column_query = "SELECT * FROM "+table_name+" WHERE "
    values_placeholder = ""
    for i, item in enumerate(list):
        if i==len(list)-1:
            values_placeholder += f"{item}=?"
        else:
            values_placeholder += f"{item}=? AND "
    return str(column_query+values_placeholder)

def get_query(query, values, conn_object):
    """ 
    Sends a query to a sqlite3 database and returns a list of values. Builds the query with parameter values.
    The number of "?" placeholder values should be the same number of the amount if items in the "values" parameter.
    Parameters:
        query - A fully built SQL query with "?" placeholder syntax to send against a database
        values - A list of values to assign for each "?" in the query
        conn_object - A connection object to a sqlite3 database
    """
    # conn_object.row_factory = lambda cursor, row: row[0]
    c = conn_object.cursor()
    c.execute(query, values)
    data = c.fetchall()
    return data
    

#################
# CUSTOM ERRORS #
#################

class InvalidParameterError(Exception):
    def __init__(self, parameter):
        self.parameter = parameter
        self.message = f"Parameter '{self.parameter}' is not valid."
        super().__init__(self.message)






#######################
# CUSTOM DATA OBJECTS #
#######################

class Registration:
    """ Class that takes parameters to register a user. Class method hash(self) takes password parameter and generates a SHA256 hash using werkzeug.security library functions """
    def __init__(self, dict):
        for key in dict:
            setattr(self, key, dict[key])
        self.hash_pass = self.hash()

    def hash(self):
        return generate_password_hash(self.password, "sha256")


class Authenticate:
    """ Class that takes a dict of request parameters, does database query and password validation using werkzeug.security library functions """
    def __init__(self, dict, func):
        for key in dict:
            setattr(self, key, dict[key])
        self.func = MethodType(func, self)

    def check(self):
        database = self.func
        c = database.cursor()
        c.execute("SELECT EXISTS(SELECT email FROM users WHERE email=? LIMIT 1)", (self.email,))

        if c.fetchall()[0][0] == 0:
            return jsonify({"message":{"error": "Username not found."}}), 303

        c.execute("SELECT hash_pass FROM users WHERE email=?", (self.email,))
        users_hash = c.fetchall()[0][0]
        c.close()

        return check_password_hash(users_hash, self.password)

class Restaurant_Registration:
    def __init__(self, dict):
        for key in dict:
            setattr(self, key, dict[key])

class Query_Advanced:
    def __init__(self, dict):
        for key in dict:
            setattr(self, key, dict[key])

    def __attrlist__(self):
        """ Return a list of filtered attributes for the object that aren't built-in or are unwanted """
        return [a for a in dir(self) if not a.startswith('__')]
    
    def __query_map__(self, dict):
        """ Sets the instance variable value to a tuple of its attribute name in the database and the value retrieved from the request """
        for attribute in self.__attrlist__():
            if attribute not in dict:
                raise InvalidParameterError(attribute)
            else:
                temp = self.__dict__[attribute]
                self.__dict__[attribute] = (dict[attribute], temp)
            
class UserObject:
    def __init__(self, email, func):
        self.email = email
        self.db_object = func
        self.id, self.address, self.city, self.zip, self.state = self.set_userinfo(self)

    def set_userinfo(self, arg):
        database = self.db_object
        c = database.cursor()
        c.execute("SELECT user_id, user_address, user_city, user_zip, user_state FROM users WHERE email=?",(self.email,))
        data = c.fetchall()
        return (data[0][0], data[0][1], data[0][2], data[0][3], data[0][4])
        


