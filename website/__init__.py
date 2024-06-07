from flask import Flask
from flask_mail import Mail

mail = Mail()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '@Bickle211991'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'cardioriskpredict@gmail.com'
    app.config['MAIL_PASSWORD'] = 'xrji dbqg pvdf wsxf'
    app.config['MAIL_DEFAULT_SENDER'] = 'cardioriskpredict@gmail.com' 


    mail.init_app(app)

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    return app
