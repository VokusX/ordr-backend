import json
import logging
import hashlib
from uuid import uuid4

import webapp2

from google.appengine.ext import ndb

from ..supports.main import Handler
from ..supports.tables import Restaurant, Category, Item

static_location = "/register"

class Register(Handler):
    def post(self):
        data = json.loads(self.request.body)

        identification  = str(uuid4())

        restaurant = Restaurant(
            uuid = identification,
            email = data["email"],
            passwordHash = str(hashlib.sha224(data["password"]).hexdigest()),
            name = data["name"],
            description = data["description"],
            address = data["address"],
            lon = data["lon"],
            lat = data["lat"]
        )

        restaurant.put()

        self.respondToJson({
            "status": "success",
            "uuid": identification
        })

class Category(Handler):
    def post(self):
        data = json.loads(self.request.body)
        
        identification = str(uuid4())

        category = Category(
            uuid = identification,
            name = data["name"],
            restaurantUuid = data["restaurantUuid"]
        )
        # Call the validation service

        category.put()

        self.respondToJson({
            "status": "success",
            "uuid": identification
        })
        

class Item(Handler):
    def post(self):
        data = json.loads(self.request.body)
        identification = str(uuid4())

        item = Item(
            uuid = identification,
            name = data["name"],
            description = data["description"],
            restaurantUuid = data["restaurantUuid"],
            price = data["price"]
        )

        item.put()

        self.respondToJson({
            "status": "success",
            "uuid": identification
        })
        

app = webapp2.WSGIApplication([
    (static_location + "/register", Register),
], debug=True)