import json
import logging
import hashlib
from uuid import uuid4

import webapp2

from ..supports.main import Handler
from ..supports.tables import Restaurant, ItemCategory, Item

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
            lat = data["lat"],
            pictures = {
                "pictures": data["pictures"]
            }
        )

        restaurant.put()

        self.respondToJson({
            "status": "success",
            "uuid": identification
        })

class CategoryHandler(Handler):
    def post(self):
        data = json.loads(self.request.body)
        
        identification = str(uuid4())

        category = ItemCategory(
            uuid = identification,
            name = data["name"],
            restaurantUuid = data["restaurantUuid"]
        )

        category.put()

        self.respondToJson({
            "status": "success",
            "uuid": identification
        })
        

class ItemHandler(Handler):
    def post(self):
        data = json.loads(self.request.body)
        identification = str(uuid4())

        item = Item(
            uuid = identification,
            name = data.get("name"),
            description = data.get("description"),
            restaurantUuid = data.get("restaurantUuid"),
            price = data.get("price"),
            categoryUuid = data.get("categoryUuid")
        )

        item.put()

        self.respondToJson({
            "status": "success",
            "uuid": identification
        })
        

app = webapp2.WSGIApplication([
    (static_location + "/register", Register),
    (static_location + "/category", CategoryHandler),
    (static_location + "/item", ItemHandler)
], debug=True)