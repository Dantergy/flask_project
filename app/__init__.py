from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from .config import Config
from .auth import auth
from .models import UserModel

#Create the login manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(username):
    """ 
    This returns the query of the User model
     """
    return UserModel.query(username)

def create_app():
    #Create a new instance from flask
    app = Flask(__name__)
    bootstrap = Bootstrap(app)

    #Init the login manager
    login_manager.init_app(app)

    #Configure session
    app.config.from_object(Config)
    app.register_blueprint(auth)

    return app
