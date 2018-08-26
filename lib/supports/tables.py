import logging

from google.appengine.ext import ndb
from uuid import uuid4

class Auth(ndb.Model):
    userUuid = ndb.StringProperty(required = True)
    token = ndb.StringProperty(required = True)
    expiry = ndb.DateTimeProperty(required = True)

class Restaurant(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add = True)
    uuid = ndb.StringProperty(required = True)
    email = ndb.StringProperty(required = True)
    passwordHash = ndb.StringProperty(required = True)
    name = ndb.StringProperty(required = True)
    description = ndb.StringProperty(required = True)
    address = ndb.StringProperty(required = True)
    lon = ndb.FloatProperty(required = True)
    lat = ndb.FloatProperty(required = True)
    pictures = ndb.JsonProperty()

class Hours(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add = True)
    uuid = ndb.StringProperty(required = True)
    dayOfWeek = ndb.StringProperty(required = True)
    open = ndb.TimeProperty(required = True)
    close = ndb.TimeProperty(required = True)

class ItemCategory(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add = True)
    uuid = ndb.StringProperty(required = True)
    name = ndb.StringProperty(required = True)
    restaurantUuid = ndb.StringProperty(required = True)

class Item(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add = True)
    uuid = ndb.StringProperty(required = True)
    name = ndb.StringProperty()
    description = ndb.StringProperty()
    imagesUuid = ndb.StringProperty()
    categoryUuid = ndb.StringProperty()
    restaurantUuid = ndb.StringProperty()
    price = ndb.FloatProperty()
    
class Image(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add = True)
    uuid = ndb.StringProperty(required = True)
    parentUuid = ndb.StringProperty(required = True)

class SingleItemOrder(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add = True)
    uuid = ndb.StringProperty(required = True)
    itemUuid = ndb.StringProperty(required = True)
    orderUuid = ndb.StringProperty(required = True)
    fullfilled = ndb.BooleanProperty()

class Order(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add = True)
    uuid = ndb.StringProperty(required = True)
    userUuid = ndb.StringProperty(required = True)
    restaurantUuid = ndb.StringProperty(required = True)
    amountPaid = ndb.FloatProperty(required=True)
    notes = ndb.TextProperty()

class Reservation(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add = True)
    uuid = ndb.StringProperty(required = True)