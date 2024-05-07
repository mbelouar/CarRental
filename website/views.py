# importing from flask module the Flask class, the render_template function, the request function, url_for 
# and redirect function to redirect to index home page after updating the app database
from flask import Flask, Blueprint, render_template, request, url_for, redirect, jsonify, flash, session
# Mongoclient is used to create a mongodb client, so we can connect on the localhost 
# with the default port
from pymongo import MongoClient
# ObjectId function is used to convert the id string to an objectid that MongoDB can understand
from bson.objectid import ObjectId
# from main import app

views = Blueprint('views', __name__)

client = MongoClient('localhost', 27017)
db = client.RentCars_db # creating your flask database using your mongo client 
# collections
admins = db.admins
managers = db.managers


@views.route('/adminDashboard')
def adminHome():
    user_data = session.get('user_data')
    if not user_data:
        redirect(url_for("views.signin"))
    # Fetch all managers from MongoDB
    all_managers = managers.find()
    
    # Count the number of managers
    manager_count = managers.count_documents({})
    
    # Pass the managers data and manager count to the template
    return render_template("AdminDashboard.html", managers=all_managers, manager_count=manager_count, user_data=user_data)


@views.route('/profile')
def profile():
    user_id = request.args.get('id')
    # Assuming you have a way to identify the logged-in admin, fetch their details
    admin = admins.find_one({'_id': ObjectId(user_id)})  # Modify with your actual logic
    
    # Pass the admin's data to the template
    return render_template('editProfil.html', admin=admin)

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

        # print(sign_email)
        # print(user['email'])
        # print(sign_profile)
        # print(user['profile'])

        if sign_profile == "Admin":
            admin = admins.find_one({'email': sign_email})
            if admin and admin['password'] == sign_password:
                session['user_data'] = {
                    'name': admin["name"],
                    'id': str(admin["_id"]),
                    'email': admin["email"]
                }
                return redirect(url_for('views.adminHome'))
            elif admin and admin['password'] != sign_password:
                # error_message = "Incorrect password. Please try again."
                flash("Incorrect password. Please try again.", "danger")
            else:
                # error_message = "Incorrect profile. Please try again."
                flash("Incorrect profile. Please try again.", "danger")
        
        elif sign_profile == "Manager":
            manager = managers.find_one({'email': sign_email})
            if manager and manager['password'] == sign_password:
                return redirect(url_for('views.managerHome'))
            elif manager and manager['password'] != sign_password:
                # error_message = "Incorrect password. Please try again."
                flash("Incorrect password. Please try again.", "danger")
            else:
                # error_message = "Incorrect profile. Please try again."
                flash("Incorrect profile. Please try again.", "danger")

    # Pass error_message to the template when rendering it
    return render_template('signin.html')

@views.route('/registre', methods=('GET', 'POST'))
def registre():

    if request.method == "POST":   # if the request method is post, then insert the todo document in todos collection
        name = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        profile = request.form['profile']
        password = request.form['password']
        passwordCheck = request.form['passwordCheck']
        
        if profile == "Admin":
            admins.insert_one({'name': name, 
                            'phone': phone, 
                            'email': email, 
                            'adress': address, 
                            'profile': profile, 
                            'password': password, 
                            'passwordCheck': passwordCheck})
            flash("Admin saved successfully!", "success")
            return redirect(url_for('views.signin')) # redirect the user to home page
        
        elif profile == "Manager":
            managers.insert_one({'name': name, 
                            'phone': phone, 
                            'email': email, 
                            'address': address, 
                            'profile': profile, 
                            'password': password, 
                            'passwordCheck': passwordCheck})
            flash("Manager saved successfully!", "success")
            return redirect(url_for('views.signin'))

    # Pass `feedback` to the template
    feedback = {'type': 'register', 'data': {'firstname': ''}}
    return render_template("registre.html", feedback=feedback)

@views.route('/add_manager', methods=['POST'])
def add_manager():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        phone = request.form['phone']
        password = request.form['password']
        password_check = request.form['passwordCheck']

        # Check if password matches passwordCheck
        if password != password_check:
            flash("Passwords do not match. Please try again.", "danger")
            return redirect(url_for("views.adminHome"))

        # Check if password meets minimum length requirement
        if len(password) < 6:
            flash("Password must be at least 6 characters long. Please try again.", "danger")
            return redirect(url_for("views.adminHome"))

        # Create a new manager document
        new_manager = {
            'name': name,
            'email': email,
            'phone': phone,
            'address': address,
            'profile': "Manager",
            'password': password
        }

        # Insert the new manager document into the database
        managers.insert_one(new_manager)
        flash("Manager added successfully!", "success")

        return redirect(url_for("views.adminHome"))  # Redirect to the homepage after adding manager

    # Handle invalid HTTP methods (though this route is configured for POST only)
    return "Method Not Allowed", 405

@views.route('/<string:id>/delete_manager/', methods=['POST'])
def delete_manager(id):
    if request.method == 'POST':
        managers.delete_one({"_id": ObjectId(id)})
        flash("Manager deleted successfully!", "success")
        return redirect(url_for('views.adminHome'))
    
@views.route('/<string:id>/edit_manager/', methods=['POST'])
def edit_manager(id):
    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        phone = request.form['phone']

        managers.update_one({"_id": ObjectId(id)}, {"$set": {'name': name, 'email': email, 'address': address, 'phone': phone}})
        flash("Manager updated successfully!", "success")
        return redirect(url_for('views.adminHome'))
    
@views.route('/<string:id>/edit_admin/', methods=['POST'])
def edit_admin(id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        phone = request.form['phone']
        password = request.form['password']
        passwordCheck = request.form['passwordCheck']
        
        # Check if password matches passwordCheck
        if password == passwordCheck and len(password) >= 6:
            # Update admin details in MongoDB
            admins.update_one({"_id": ObjectId(id)}, {"$set": {'name': name, 'email': email, 'address': address, 'phone': phone, 'password': password, 'passwordCheck': passwordCheck}})
            flash("Admin updated successfully!", "success")  # Flash success message
            return redirect(url_for('views.profile', id=id))
        elif password != passwordCheck :
            # Passwords do not match, flash error message
            flash("Passwords do not match. Please try again.", "danger")
            return redirect(url_for('views.profile', id=id))  # Redirect to profile with error message
        else:
            flash("The password must contain 6 at least characters.", "danger")
            return redirect(url_for('views.profile', id=id))  # Redirect to profile with error message

    # Handle invalid HTTP methods (though this route is configured for POST only)
    return "Method Not Allowed", 405