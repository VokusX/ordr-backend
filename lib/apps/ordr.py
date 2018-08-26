import json
import datetime
import logging
from uuid import uuid4

import webapp2

from ..supports.main import Handler
from ..supports.tables import Order, Item, SingleItemOrder
from ..supports.utils import sanitize_items_data

def create_single_item_order(item_data, orderUuid):
    identity = str(uuid4())
    singleItemOrder = SingleItemOrder(
        uuid = identity,
        itemUuid = item_data.uuid,
        orderUuid = orderUuid,
        fullfilled = False
    )

    singleItemOrder.put()

    return identity

class CreateOrder(Handler):
    def post(self):
        data = json.loads(self.request.body)
        
        items = [
            Item.query(Item.uuid == x.get("uuid")).fetch(1)[0]
            for x in data["items"]
        ]

        items = [sanitize_items_data(x) for x in items]

        identity = str(uuid4())

        order = Order(
            uuid = identity,
            userUuid = data["userUuid"],
            restaurantUuid = data["restaurantUuid"]
            amountPaid = 0,
            notes = data["notes"]
        )

        singleItemOrders = [
            create_single_item_order(x, identity) for x in items
        ]

        return {
            "status": "success",
            "items": singleItemOrders
        }

class FullfillOrder(Handler):
    def put(self):
        data = json.loads(self.request.body)

        singleItemOrder = SingleItemOrder.query(SingleItemOrder.uuid == data["uuid"]).get()

        singleItemOrder.fullfilled = data["fullfilled"]

        singleItemOrder.put()

        return {
            "status": "success"
        }



app = webapp2.WSGIApplication([
    (static_location + "/createOrder", CreateOrder)
    # (static_location + "/payOrder", PayOrder)
])