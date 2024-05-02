from flask import Flask, jsonify

class User:

    def registre(self):

        user = {
            "_id": "",
            "name": "",
            "phone": "",
            "email": "",
            "adresse": "",
            "profile": "",
            "password": ""
        }
        return jsonify(user), 200
    
