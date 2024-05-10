# importing from flask module the Flask class, the render_template function, the request function, url_for 
# and redirect function to redirect to index home page after updating the app database
from flask import Flask, Blueprint, render_template, request, url_for, redirect, jsonify, flash, session
# Mongoclient is used to create a mongodb client, so we can connect on the localhost 
# with the default port
from pymongo import MongoClient
# ObjectId function is used to convert the id string to an objectid that MongoDB can understand
from bson.objectid import ObjectId
# from main import app
from website.commands import AddManagerCommand, DeleteManagerCommand, EditManagerCommand

views = Blueprint('views', __name__)

client = MongoClient('localhost', 27017)
db = client.RentCars_db # creating your flask database using your mongo client 
# collections
admins = db.admins
managers = db.managers
clients = db.clients
reservations = db.reservations
cars = db.cars


@views.route('/adminDashboard')
def adminHome():
    user_data = session.get('user_data')
    if not user_data:
        redirect(url_for("views.signin"))
    # Fetch all managers from MongoDB
    all_managers = managers.find()
    
    # Count the number of managers
    manager_count = managers.count_documents({})
    car_count = cars.count_documents({})
    reservation_count = reservations.count_documents({})
    
    # Pass the managers data and manager count to the template
    return render_template("AdminDashboard.html", managers=all_managers, manager_count=manager_count, user_data=user_data, car_count=car_count, reservation_count=reservation_count)


@views.route('/profile')
def profile():
    user_id = request.args.get('id')
    # Assuming you have a way to identify the logged-in admin, fetch their details
    admin = admins.find_one({'_id': ObjectId(user_id)})  # Modify with your actual logic
    
    # Pass the admin's data to the template
    return render_template('editProfil.html', admin=admin)

@views.route('/managerDashboard')
def managerHome():
    user_data = session.get('user_data')
    if not user_data:
        redirect(url_for("views.signin"))

    all_cars = db.cars.find()

    return render_template("ManagerDashboard.html", user_data=user_data, cars=all_cars, filter={'category':'all','status':'all'})


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
        add_manager_command = AddManagerCommand(request.form)
        add_manager_command.execute()
        flash("Manager added successfully!", "success")
        return redirect(url_for("views.adminHome"))  # Redirect to the homepage after adding manager

    return "Method Not Allowed", 405

@views.route('/<string:id>/delete_manager/', methods=['POST'])
def delete_manager(id):
    if request.method == 'POST':
        delete_manager_command = DeleteManagerCommand(id)
        delete_manager_command.execute()
        flash("Manager deleted successfully!", "success")
        return redirect(url_for('views.adminHome'))

    return "Method Not Allowed", 405

@views.route('/<string:id>/edit_manager/', methods=['POST'])
def edit_manager(id):
    if request.method == 'POST':
        edit_manager_command = EditManagerCommand(id, request.form)
        edit_manager_command.execute()
        flash("Manager updated successfully!", "success")
        return redirect(url_for('views.adminHome'))

    return "Method Not Allowed", 405

# @views.route('/add_manager', methods=['POST'])
# def add_manager():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         address = request.form['address']
#         phone = request.form['phone']
#         password = request.form['password']
#         password_check = request.form['passwordCheck']

#         # Check if password matches passwordCheck
#         if password != password_check:
#             flash("Passwords do not match. Please try again.", "danger")
#             return redirect(url_for("views.adminHome"))

#         # Check if password meets minimum length requirement
#         if len(password) < 6:
#             flash("Password must be at least 6 characters long. Please try again.", "danger")
#             return redirect(url_for("views.adminHome"))

#         # Create a new manager document
#         new_manager = {
#             'name': name,
#             'email': email,
#             'phone': phone,
#             'address': address,
#             'profile': "Manager",
#             'password': password
#         }

#         # Insert the new manager document into the database
#         managers.insert_one(new_manager)
#         flash("Manager added successfully!", "success")

#         return redirect(url_for("views.adminHome"))  # Redirect to the homepage after adding manager

#     # Handle invalid HTTP methods (though this route is configured for POST only)
#     return "Method Not Allowed", 405

# @views.route('/<string:id>/delete_manager/', methods=['POST'])
# def delete_manager(id):
#     if request.method == 'POST':
#         managers.delete_one({"_id": ObjectId(id)})
#         flash("Manager deleted successfully!", "success")
#         return redirect(url_for('views.adminHome'))
    
# @views.route('/<string:id>/edit_manager/', methods=['POST'])
# def edit_manager(id):
#     if request.method == 'POST':

#         name = request.form['name']
#         email = request.form['email']
#         address = request.form['address']
#         phone = request.form['phone']

#         managers.update_one({"_id": ObjectId(id)}, {"$set": {'name': name, 'email': email, 'address': address, 'phone': phone}})
#         flash("Manager updated successfully!", "success")
#         return redirect(url_for('views.adminHome'))
    
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

@views.route('/clients', methods=['POST', 'GET'])
def clients():
    user_data = session.get('user_data')
    if not user_data:
        return redirect(url_for("views.signin"))  # Redirect if user is not authenticated

    # Access the clients collection directly using db
    all_clients = db.clients.find()
    client_count = db.clients.count_documents({})

    return render_template("Clients.html", clients=all_clients, client_count=client_count, user_data=user_data)


@views.route('/add_client', methods=['POST'])
def add_client():
    if request.method == 'POST':
        name = request.form['name']
        cin = request.form['cin']
        address = request.form['address']
        phone = request.form['phone']

        # Create a new client document
        new_client = {
            'name': name,
            'cin': cin,
            'phone': phone,
            'address': address
        }

        # Insert the new client document into the database
        db.clients.insert_one(new_client)
        flash("Client added successfully!", "success")

        return redirect(url_for("views.clients"))  # Redirect to the homepage after adding manager

    # Handle invalid HTTP methods (though this route is configured for POST only)
    return "Method Not Allowed", 405

@views.route('/<string:id>/edit_client/', methods=['POST'])
def edit_client(id):
    if request.method == 'POST':

        name = request.form['name']
        cin = request.form['cin']
        address = request.form['address']
        phone = request.form['phone']

        db.clients.update_one({"_id": ObjectId(id)}, {"$set": {'name': name, 'cin': cin, 'address': address, 'phone': phone}})
        flash("Client updated successfully!", "success")
        return redirect(url_for('views.clients'))
    
@views.route('/<string:id>/delete_client/', methods=['POST'])
def delete_client(id):
    if request.method == 'POST':
        db.clients.delete_one({"_id": ObjectId(id)})
        flash("Client deleted successfully!", "success")
        return redirect(url_for('views.clients'))
    
@views.route('/reservation')
def reservation():
    user_data = session.get('user_data')
    if not user_data:
        return redirect(url_for("views.signin"))  # Redirect if user is not authenticated

    # Access the clients collection directly using db
    all_reservations = db.reservations.find()
    reservation_count = db.reservations.count_documents({})
    # Query confirmed reservations count
    confirmed_count = db.reservations.count_documents({'status': 'Confirmed'})

    # Query pending reservations count (assuming 'pending' is another status)
    pending_count = db.reservations.count_documents({'status': 'Not Confirmed'})

    return render_template("Reservation.html", reservations=all_reservations, reservation_count=reservation_count, user_data=user_data, confirmed_count=confirmed_count, pending_count=pending_count)

@views.route('/add_reservation', methods=['POST'])
def add_reservation():
    if request.method == 'POST':
        carId = request.form['carId']
        clientName = request.form['clientName']
        duration = request.form['duration']
        price = request.form['price']

        # Create a new reservation document
        new_reservation = {
            'carId': carId,
            'clientName': clientName,
            'price': price,
            'duration': duration,
            'status': 'Not Confirmed'
        }

        # Insert the new reservation document into the database
        db.reservations.insert_one(new_reservation)
        flash("Reservation added successfully!", "success")

        return redirect(url_for("views.reservation"))  # Redirect to the homepage after adding manager

    # Handle invalid HTTP methods (though this route is configured for POST only)
    return "Method Not Allowed", 405

@views.route('/<string:id>/edit_reservation/', methods=['POST'])
def edit_reservation(id):
    if request.method == 'POST':

        carId = request.form['carId']
        clientName = request.form['clientName']
        duration = request.form['duration']
        price = request.form['price']

        db.reservations.update_one({"_id": ObjectId(id)}, {"$set": {'carId': carId, 'clientName': clientName, 'duration': duration, 'price': price}})
        flash("Reservation updated successfully!", "success")
        return redirect(url_for('views.reservation'))
    
@views.route('/<string:id>/delete_reservation/', methods=['POST'])
def delete_reservation(id):
    if request.method == 'POST':
        db.reservations.delete_one({"_id": ObjectId(id)})
        flash("Reservation deleted successfully!", "success")
        return redirect(url_for('views.reservation'))
    
@views.route('/<string:id>/confirm_reservation', methods=['POST'])
def confirm_reservation(id):
    if request.method == 'POST':
        # Update reservation status to 'confirmed' in MongoDB
        reservations.update_one({'_id': ObjectId(id)}, {'$set': {'status': 'Confirmed'}})

        # Store the confirmed reservation ID in the session
        session['confirmed_reservation_id'] = id

        res = db.reservations.find_one({'_id': ObjectId(id)})
        res_id = str(res['carId']) 

        db.cars.update_one({"carid": res_id}, {"$set": {'status': "Rented"}})


        flash("Reservation was confirmed successfully!", "success")
        return redirect(url_for('views.reservation'))
    
@views.route('/add_car', methods=['POST'])
def add_car():
    if request.method == 'POST':
        carname = request.form['carname']
        category = request.form['category']
        model = request.form['model']
        carid = request.form['carid']
        price = request.form['price']

        # Create a new car document
        new_car = {
            'carname': carname,
            'category': category,
            'status': "Available",
            'model': model,
            'carid': carid,
            'price': price
        }

        # Insert the new car document into the database
        db.cars.insert_one(new_car)
        flash("Car added successfully!", "success")

        return redirect(url_for("views.managerHome"))  # Redirect to the homepage after adding manager

    # Handle invalid HTTP methods (though this route is configured for POST only)
    return "Method Not Allowed", 405

@views.route('/apply_filter', methods=['POST'])
def apply_filter():
    if request.method == 'POST':
        category = request.form['category']
        status = request.form['status']

        # Build the filter criteria based on selected category and status
        filter_criteria = {}

        if category and category != 'all':
            filter_criteria['category'] = category
        
        if status and status != 'all':
            filter_criteria['status'] = status

        # Query MongoDB with the filter criteria
        filtered_cars = db.cars.find(filter_criteria)

        # Render the managerHome template with the filtered reservations
        return render_template("ManagerDashboard.html", cars=filtered_cars, filter={'category':category,'status':status})
    else:
        # Handle other HTTP methods (e.g., GET) gracefully
        return redirect(url_for('views.managerHome'))