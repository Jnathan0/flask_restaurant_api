from typing import ClassVar
import unittest
import json
import os
import time
from warnings import catch_warnings
from flask.helpers import make_response
from flask.wrappers import Response
import requests
from requests.api import request




class TestUsers(unittest.TestCase):

    currentResult = None
    
    @classmethod
    def setResult(cls, amount, errors, failures, skipped, name):
        cls.amount, cls.errors, cls.failures, cls.skipped , cls.name = amount, errors, failures, skipped, name
    
    def tearDown(self):
        amount = self.currentResult.testsRun
        errors = self.currentResult.errors
        failures = self.currentResult.failures
        skipped = self.currentResult.skipped
        name = self.__class__.__name__
        self.setResult(amount, errors, failures, skipped, name)
    
    @classmethod
    def tearDownClass(cls):
        print(f"\nResults for {cls.name}: \n-------------")
        print(f"Tests run: {cls.amount}")
        print(f"Errors: {len(cls.errors)}")
        for e in cls.errors:
            print(f"    * {e}")
        print(f"Failures: {len(cls.failures)}")
        for f in cls.failures:
            print(f"    * {f}\n")
        print(f"Success: {cls.amount - len(cls.errors) - len(cls.failures)}")
        print(f"Skipped: {len(cls.skipped)}")
        for s in cls.skipped:
            print(f"    * {s}\n")

    def run(self, result=None):
        self.currentResult = result
        unittest.TestCase.run(self, result)

    def testEdgecaseCreate(self):
        data = {'email': 'blackboxtest@test.com', 'password': 'password', 'first': 'whitebox_first', 'last': 'whitebox_last', 'address': 'whitebox_address', 'city': 'whitebox_address', 'zip': 555555550052355555555, 'state': 'CA', 'phone': 17145235235556767}
        response = requests.put('http://localhost:5000/api/users', json=data)
        # Test if user is created and returns HTTP 201
        self.assertEqual(response.status_code, 201)


    def testCreateDuplicated(self):
        data = {'email': 'blackbox@test.com'}
        response = requests.put('http://localhost:5000/api/users', json=data)

        # Check if users service will make a new account without all the required parameters
        self.assertNotEqual(response.status_code, 201) 

        # Test to see if response is 409
        self.assertEqual(response.status_code, 409)

    def testAuth(self):
        data = {'email': 'blackboxtest@test.com', 'password': 'password'}
        response = requests.get('http://localhost:5000/api/users', json=data)
        self.assertTrue(response.json()['message']['verify'], True)

    def testNotAuth(self):
        response = requests.get('http://localhost:5000/api/users', json={'email': 'blackboxtest@test.com', 'password': 'wrongpassword'})
        self.assertFalse(response.json()['message']['verify'], True)

    def testDelBadAuth(self):
        data = {'email': 'blackboxtest@test.com', 'password': 'a;wletjk'}
        response = requests.delete('http://localhost:5000/api/users', json=data)
        self.assertNotEqual(response.status_code, 200)
        
class TestRestaurants(unittest.TestCase):
    currentResult = None
    
    @classmethod
    def setResult(cls, amount, errors, failures, skipped, name):
        cls.amount, cls.errors, cls.failures, cls.skipped , cls.name = amount, errors, failures, skipped, name
    
    def tearDown(self):
        amount = self.currentResult.testsRun
        errors = self.currentResult.errors
        failures = self.currentResult.failures
        skipped = self.currentResult.skipped
        name = self.__class__.__name__
        self.setResult(amount, errors, failures, skipped, name)
    
    @classmethod
    def tearDownClass(cls):
        print(f"\nResults for {cls.name}: \n-------------")
        print(f"Tests run: {cls.amount}")
        print(f"Errors: {len(cls.errors)}")
        for e in cls.errors:
            print(f"    * {e}")
        print(f"Failures: {len(cls.failures)}")
        for f in cls.failures:
            print(f"    * {f}\n")
        print(f"Success: {cls.amount - len(cls.errors) - len(cls.failures)}")
        print(f"Skipped: {len(cls.skipped)}")
        for s in cls.skipped:
            print(f"    * {s}\n")

    def run(self, result=None):
        self.currentResult = result
        unittest.TestCase.run(self, result)


    def setUp(self):
        with open('test.json') as f:
            data = json.load(f)
        self.catalog = data

    def testCatalog(self):
        data = {'zipcode': 92691}
        response = requests.get('http://localhost:5000/api/restaurants', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.catalog['catalogs'])

    def testNothing(self):
        response = requests.get('http://localhost:5000/api/restaurants', json={'zipcode':00000})
        self.assertEqual(response.json(), {'Restaurants':[]})

    def testNoParams(self):
        response = requests.get('http://localhost:5000/api/restaurants', json={})
        self.assertEqual(response.status_code, 400)

class TestCart(unittest.TestCase):
    currentResult = None
    
    @classmethod
    def setResult(cls, amount, errors, failures, skipped, name):
        cls.amount, cls.errors, cls.failures, cls.skipped , cls.name = amount, errors, failures, skipped, name
    

    def setUp(self):
        request = requests.put('http://localhost:5000/api/users', json={'email': 'cartuser@user.com', 'password': 'password', 'first': 'cart_first', 'last': 'cart_last', 'address': 'cart_test_address', 'city': 'cart_test_city', 'zip': 55555, 'state': 'CA', 'phone': 17145556767} )

    def tearDown(self):
        amount = self.currentResult.testsRun
        errors = self.currentResult.errors
        failures = self.currentResult.failures
        skipped = self.currentResult.skipped
        name = self.__class__.__name__
        self.setResult(amount, errors, failures, skipped, name)
    
    @classmethod
    def tearDownClass(cls):
        print(f"\nResults for {cls.name}: \n-------------")
        print(f"Tests run: {cls.amount}")
        print(f"Errors: {len(cls.errors)}")
        for e in cls.errors:
            print(f"    * {e}")
        print(f"Failures: {len(cls.failures)}")
        for f in cls.failures:
            print(f"    * {f}\n")
        print(f"Success: {cls.amount - len(cls.errors) - len(cls.failures)}")
        print(f"Skipped: {len(cls.skipped)}")
        for s in cls.skipped:
            print(f"    * {s}\n")

    def run(self, result=None):
        self.currentResult = result
        unittest.TestCase.run(self, result)

    def testCartadd(self):
        response = requests.put('http://localhost:5000/api/carts', json={'email': 'cartuser@user.com', 'items': [11,10]})
        self.assertEqual(response.status_code, 201)

    def testNonsimilarRestauraunt(self):
        response = requests.put('http://localhost:5000/api/carts', json={'email': 'cartuser@user.com', 'items':[2,10]})
        self.assertEqual(response.status_code, 400)
    #     # TODO:
        #  - test adding item(s) to cart 
        #  - Test adding to cart with bad parameters
        #  - Test getting cart 
        #  - Test making an order 
        #  - Test to verify that an order was placed

if __name__=='__main__':
    unittest.main()