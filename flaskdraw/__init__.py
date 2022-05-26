from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from flaskdraw.users.routes import users
    from flaskdraw.drawproj.routes import drawproj
    from flaskdraw.main.routes import main

    app.register_blueprint(users)
    app.register_blueprint(drawproj)
    app.register_blueprint(main)

    return app
