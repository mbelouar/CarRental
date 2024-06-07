from flask import flash
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('localhost', 27017)
db = client.RentCars_db
managers = db.managers

class Command:
    def execute(self) -> bool:
        pass

class AddManagerCommand(Command):
    def __init__(self, request_form):
        self.request_form = request_form

    def execute(self) -> bool:
        name = self.request_form['name']
        email = self.request_form['email']
        address = self.request_form['address']
        phone = self.request_form['phone']
        password = self.request_form['password']
        password_check = self.request_form['passwordCheck']

        # Check if password matches passwordCheck
        if password != password_check:
            flash("Passwords do not match. Please try again.", "danger")
            return False

        # Your logic to add manager to the database
        manager_data = {
            'name': name,
            'email': email,
            'address': address,
            'phone': phone,
            'password': password
        }
        managers.insert_one(manager_data)
        return True

class DeleteManagerCommand(Command):
    def __init__(self, manager_id):
        self.manager_id = manager_id

    def execute(self) -> bool:
        result = managers.delete_one({"_id": ObjectId(self.manager_id)})
        if result.deleted_count == 1:
            return True
        else:
            return False

class EditManagerCommand(Command):
    def __init__(self, manager_id, request_form):
        self.manager_id = manager_id
        self.request_form = request_form

    def execute(self) -> bool:
        name = self.request_form['name']
        email = self.request_form['email']
        address = self.request_form['address']
        phone = self.request_form['phone']

        # Your logic to edit manager in the database
        update_data = {
            'name': name,
            'email': email,
            'address': address,
            'phone': phone
        }
        result = managers.update_one({"_id": ObjectId(self.manager_id)}, {"$set": update_data})
        if result.modified_count == 1:
            return True
        else:
            return False
