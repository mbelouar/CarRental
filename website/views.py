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

@views.route('/managerDashboard')
def managerHome():
    return render_template("ManagerDashboard.html")

@views.route('/reservation')
def reservation():
    return render_template("Reservation.html")

@views.route('/clients')
def clients():
    return render_template("Clients.html")


@views.route('/', methods=['GET', 'POST'])
def signin():
    error_message = None  # Initialize error_message as None initially

    if request.method == "POST":
        sign_email = request.form['sign_email']
        sign_password = request.form['sign_password']
        sign_profile = request.form['sign_profile']

        user = users.find_one({'email': sign_email})
        # print(sign_email)
        # print(user['email'])
        print(sign_profile)
        # print(user['profile'])
        if user and user['password'] == sign_password and user['profile'] == sign_profile == "Admin":
            # Authentication successful
            return redirect(url_for('views.adminHome'))  # Redirect to dashboard or another page
        elif user and user['password'] == sign_password and user['profile'] == sign_profile ==  "Manager":
            # Authentication successful
            return redirect(url_for('views.managerHome'))  # Redirect to dashboard or another page
        elif user and user['password'] != sign_password:
            error_message = "Incorrect password. Please try again."
        elif user and user['profile'] != sign_profile:
            error_message = "Incorrect profile. Please try again."

    # Pass error_message to the template when rendering it
    return render_template('signin.html', error_message=error_message)

@views.route('/registre', methods=('GET', 'POST'))
def registre():

    if request.method == "POST":   # if the request method is post, then insert the todo document in todos collection
        name = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        adresse = request.form['address']
        profile = request.form['profile']
        password = request.form['password']
        passwordChck = request.form['passwordChck']
        
        users.insert_one({'name': name, 
                          'phone': phone, 
                          'email': email, 
                          'adresse': adresse, 
                          'profile': profile, 
                          'password': password, 
                          'passwordChck': passwordChck})
        
        return redirect(url_for('views.signin')) # redirect the user to home page

    # Pass `feedback` to the template
    feedback = {'type': 'register', 'data': {'firstname': ''}}
    return render_template("registre.html", feedback=feedback)

