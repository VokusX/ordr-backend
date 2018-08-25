import json
import datetime
import logging

import webapp2

from ..supports.main import Handler
from ..supports.tables import Restaurant, Item, Category

static_lication = "/search"

def sanitaize_restaurant_data(data):
    return {
        "name": data.name,
        "uuid": data.uuid,
        # "rating":
        # "num_reviews"
        "description": data.description,
        "address": data.address,
        "location": {
            "lon": data.lon,
            "lat": data.lat,
        },
        # "hours": [
            
        # ],
        # "checkInAllowed": True
        # "pictures": []
    }

def sanitize_items_data(data):
    return {
        "name": data.name,
        "price": data.price
        "categoryUUID": data.categoryUuid
        "description": data.description
        # "pictures":
    }

def sanatize_categories(data):
    return {
        "name": data.name,
        "uuid": data.uuid
    }

class FindNearby(Handler):
    def post(self):
        data = json.loads(self.request.body)

        nearby = Restaurant.query(
            Restaurant.lon < data["boundaries"][0]["lon"],
            Restaurant.lon > data["boundaries"][1]["lon"],
            ).fetch()

        for restaurant in list(nearby):
            if not (restaurant.lat < data["boundaries"][0]["lat"] and restaurant.lat > data["boundaries"][1]["lon"]):
                nearby.remove(restaurant)

        resultant = [sanitaize_restaurant_data(x) for x in nearby]

        self.respondToJson({
            "status": "success",
            "restaurants": resultant
        })

class Details(Handler):
    def post(self):
        data = json.loads(self.request.body)

        restaurant = Restaurant.query(Restaurant.uuid == data["uuid"]).fetch(1)

        if len(restaurant) == 1:

            result = sanitaize_restaurant_data(restaurant[0])
            result["status"] = "success"
            self.respondToJson(result)
        else:
            self.respondToJson({
                "status": "failed",
                "error": "did not find restaurant with uuid of %s" % (data["uuid"],)
            })

class Menu(Handler):
    def post(self):
        data = json.loads(self.request.body)

        items = Item.query(Item.restaurantUuid == data["uuid"]).fetch()

        items = [sanitize_items_data(x) for x in items]

        categories = Category.query(Category.restaurantUuid == data["uuid"]).fetch

        categories = [sanatize_categories(x) for x in categories]

        self.respondToJson({
            "items": items,
            "categories": categories
        })



app = webapp2.WSGIApplication([
    (static_lication + "/findNearby", FindNearby),
    (static_lication + "/details", Details)
], debug=True)