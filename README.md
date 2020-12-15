# Assignment 4

## Author: Joshua Nathan
## Section: CPSC 362-05
## CWID: 889505749

**Summary** 
Resturant Catalog service that exposes an API for Users, Cart, and Resturaunt view services. Uses gateway routing pattern to pass requests upstream in a microservice architecture.
Cart, Resturant View, and the rest of the Users services are to be implimented in future iterations. 


## Files

- /database         # Directory to contain data stores
-  -schema.sql      # Schema for backend datastores
-  -database.db
-  -Makefile        # Makefile to build .db files 
- /test
-  -blackbox_test.txt # File containing output of blackbox unit tests
-  -whitebox_text.txt # File containing output of whitebox tests
-  -demo_commands.txt # File containing example CURL commands to interact with the api
-  -test.py # Python3 script to run blackbox unit tests
-  -test_carts.json # Json data for test.py
-  -test.json #json data for test.py
- .env              # Flask environment dotfile
- app_classes.py    # Helper classes to be used in gateway.py
- gateway.py        # Script to forward requests upstream and return their repsonse 
- Procfile          # Profile definitions to run with foreman
- README.md         # This file
- routes.cfg        # Config file 
- users_app.py      # Script for the users microservice
- carts_app.py      # Script for the carts microservice
- restaurants_app.py # Script for restaurants microservice
- assignment4_report.PDF   # Document containing the text report for Assignment 3
- requirements.txt  # Doc containing python3 dependancies 
- project_4_demo.mp4 # Video demo of the application 

## Requirements
The following requirements are to produce an environemnt similar to development
The application is intended to be ran in a python3 venv

- python3.8 or higher
- ubuntu 20.04 or higher 
- foreman (used to start and manage Procfile-based applications see https://github.com/ddollar/foreman, can be installed with gem package manager)
- sqlite3
- GNU make

## Getting started

Use the following commands to get up and running:

```shell-session
$ pip3 install -r requirements.txt                        # install utilities
$ cd database/ && make                                    # create database (NOTE: A .db file is already included for evaluation purposes)
$ cd ..                                                   # Navigate back to top level directory 
$ foreman start -m gateway=1,restaurants=3,users=3,carts=3 -p 5000              

# start user service, restaurant service, cart service instances on port 5100x and gateway instance on port 5000
```

## API Definitions and useage 

Can be found in assignemnt4_report.pdf


### Usage Examples
Additional Usage Examples can be found in demo_commands.txt


`createUser('email', 'password', 'first', 'last', 'address', 'city', 'zip', 'state', 'phone')`

http PUT localhost:5000/api/users data=foo

data={email: "test@test.com", 
    password: "toor", 
    first: "John",
    last: "Smith",
    address: "1 Silicon Lane",
    city: "San Diego",
    zip: "92104",
    state: "CA",
    phone: "14215556769}

RETURN JSON EXAMPLE ON SUCCESSFUL REGISTRATION:

{
    "message": {
        "status": "New user created sucsessfully."
    }
}


RETURN JSON EXAMPLE WHEN EMAIL IS ALREADY REGISTERED:

{
    "message": {
        "error": "Account for email already exists."
    }
}

`authenticateUser(email, password)`

http GET localhost:5000/api/users email="test@test.com" password=toor

OR example json format
{email: "test@test.com", password="toor"}

RETURN JSON EXAMPLE:

{
    "message": {
        "verify": true
    }
}


### Gateway.py

gateway.py forwards requests upstream to predefined URLs in routes.cfg, and returns the response. Uses round robin load balancing to distribute requests across all healthy microservices. 

The URLs in routes.cfg are loaded into a pool as values in keys for a dict (users or timelines).

Itertools.cycle objects are then created for the users values, resturaunt values, and cart values. 

function rr_balancer(uri) takes a uri and returns the next base URL to be requested to. 

A route forwards to the proper route upstream and returns the request. If the request returns HTTP CODE 500 or above, it removes the upstream URL from the list to be skipped in the load balancer. 
