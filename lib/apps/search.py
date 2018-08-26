import json
import datetime
import logging

import webapp2

from ..supports.main import Handler
from ..supports.tables import Restaurant, Item, ItemCategory
from ..supports.utils import sanitize_items_data

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
        "hours": [],
        # "checkInAllowed": True
        "pictures": data.pictures["pictures"]
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

        categories = ItemCategory.query(ItemCategory.restaurantUuid == data["uuid"]).fetch()

        categories = [sanatize_categories(x) for x in categories]

        result = {
            "other": []
        }

        # Create the categories
        for cat in categories:
            result[cat["uuid"]] = []

        # Fill in the categories with the items
        for item in items:
            if (item.get("categoryUUID")):
                result[str(item.get("categoryUUID"))].append(item)
            else:
                result["other"].append(item)

        for cat in categories:
            result[cat["name"]] = result.pop(cat["uuid"])

        self.respondToJson(result)

app = webapp2.WSGIApplication([
    (static_lication + "/findNearby", FindNearby),
    (static_lication + "/details", Details),
    (static_lication + "/menu", Menu)
], debug=True)