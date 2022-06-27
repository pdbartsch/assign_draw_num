from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "bp_users.login"
login_manager.login_message_category = "info"


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from flaskdraw.bp_main.routes import bp_main
    from flaskdraw.bp_users.routes import bp_users
    from flaskdraw.bp_drawings.routes import bp_drawings
    from flaskdraw.bp_projects.routes import bp_projects
    from flaskdraw.bp_locations.routes import bp_locations

    app.register_blueprint(bp_main)
    app.register_blueprint(bp_users)
    app.register_blueprint(bp_drawings)
    app.register_blueprint(bp_projects)
    app.register_blueprint(bp_locations)

    return app
