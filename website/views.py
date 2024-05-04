# importing from flask module the Flask class, the render_template function, the request function, url_for 
# and redirect function to redirect to index home page after updating the app database
from flask import Flask, Blueprint, render_template, request, url_for, redirect 
# Mongoclient is used to create a mongodb client, so we can connect on the localhost 
# with the default port
from pymongo import MongoClient
# ObjectId function is used to convert the id string to an objectid that MongoDB can understand
from bson.objectid import ObjectId
# from main import app

views = Blueprint('views', __name__)

client = MongoClient('localhost', 27017)
db = client.RentCars_db # creating your flask database using your mongo client 
users = db.users # creating a collection called "users"

@views.route('/adminDashboard')
def adminHome():
    return render_template("AdminDashboard.html")

@views.route('/profile')
def profile():
    return render_template('editProfil.html')

@views.route('/', methods=('GET', 'POST'))
def signin():
    # Define or obtain the `feedback` variable
    # feedback = {'type': 'register', 'data': {'firstname': 'John'}}
    
    # Pass `feedback` to the template
    return render_template('signin.html')

@views.route('/registre', methods=('GET', 'POST'))
def registre():
    # Define or obtain the `feedback` variable
    # feedback = {'type': 'register', 'data': {'firstname': 'John'}}
    # print(request.method)
    if request.method == "POST":   # if the request method is post, then insert the todo document in todos collection
        name = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        adresse = request.form['adresse']
        profile = request.form['profile']
        password = request.form['password']
        users.insert_one({'name': name, 'phone': phone, 'email': email, 'adresse': adresse, 'profile': profile, 'password': password})
        # return redirect(url_for('signin')) # redirect the user to home page

    # Pass `feedback` to the template
    feedback = {'type': 'register', 'data': {'firstname': "name"}}
    return render_template("registre.html", feedback=feedback)

