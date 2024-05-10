from website.models import cars, managers, reservations, MongoClient
from bson.objectid import ObjectId

# Define repository classes
class ManagerRepository:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.RentCars_db
        self.collection = self.db.managers

    def get_all_managers(self):
        return self.collection.find()

    def get_manager_by_id(self, manager_id):
        return self.collection.find_one({'_id': ObjectId(manager_id)})

    def add_manager(self, manager_data):
        return self.collection.insert_one(manager_data)

    def update_manager(self, manager_id, update_data):
        return self.collection.update_one({'_id': ObjectId(manager_id)}, {'$set': update_data})

    def delete_manager(self, manager_id):
        return self.collection.delete_one({'_id': ObjectId(manager_id)})
    
class CarRepository:
    def __init__(self) -> None:
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.RentCars_db
        self.collection = self.db.cars

    def get_all_cars(self):
        return self.collection.find()
    
class ResRepository:
    def __init__(self) -> None:
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.RentCars_db
        self.collection = self.db.reservations

    def get_all_reservations(self):
        return self.collection.find()

