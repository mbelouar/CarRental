from flask import Blueprint, render_template
# from main import app

views = Blueprint('views', __name__)

@views.route('/adminDashboard')
def adminHome():
    return render_template("AdminDashboard.html")

@views.route('/profile')
def profile():
    return render_template('editProfil.html')

@views.route('/')
def signin():
    # Define or obtain the `feedback` variable
    # feedback = {'type': 'register', 'data': {'firstname': 'John'}}
    
    # Pass `feedback` to the template
    return render_template('signin.html')

@views.route('/registre')
def registre():
    # Define or obtain the `feedback` variable
    # feedback = {'type': 'register', 'data': {'firstname': 'John'}}
    
    # Pass `feedback` to the template
    feedback = {'type': 'register', 'data': {'firstname': 'John'}}
    return render_template("registre.html", feedback=feedback)
