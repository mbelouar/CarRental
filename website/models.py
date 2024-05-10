from flask import flash
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.RentCars_db # creating your flask database using your mongo client 

# collections
admins = db.admins
managers = db.managers
clients = db.clients
reservations = db.reservations
cars = db.cars