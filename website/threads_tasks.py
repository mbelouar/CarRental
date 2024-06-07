import csv
import os
from website import mail
from flask import current_app as app

def send_email_in_background(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")


def save_data_in_background(user_info):
    file_exists = os.path.isfile('data.csv')
    
    with open('data.csv', 'a', newline='') as csvfile:
        fieldnames = ['Client Name', 'Client Email', 'Car Rented', 'Duration', 'Total Price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader() 
        
        writer.writerow(user_info)
    
    print("Data saved successfully")
