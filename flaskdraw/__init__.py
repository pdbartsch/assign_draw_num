import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


SECRET_KEY = os.urandom(32)

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "database.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = SECRET_KEY
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"

from flaskdraw.users.routes import users
from flaskdraw.drawproj.routes import drawproj
from flaskdraw.main.routes import main

# from flaskdraw.utils.filters import utils

app.register_blueprint(users)
app.register_blueprint(drawproj)
app.register_blueprint(main)
# app.register_blueprint(utils)


# def create_app(config_filename):
#     app = Flask(__name__)
#     app.config.from_pyfile(config_filename)

#     db = SQLAlchemy(app)
