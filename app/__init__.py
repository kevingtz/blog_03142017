# THIS IS THE APPLICATION FACTORY FILE

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

# HERE WE GONNA CREATED THE EXTENSION BUT UNINITIALIZED
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()


# CREATING A METHOD TO CREATE A INSTANCE OF THE APP
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])  # PASSING THE CONFIG NAME IN ORDER TO THE CONFIG YOU WANNA USE
    config[config_name].init_app(app)

    # HERE WE INITIALIZE THE EXTENSION PASSING THE INSTANCE OF THE APP
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    # IMPORTING THE 'MAIN_BLUEPRINT'
    from .main import main as main_blueprint  # AVOIDING THE CIRCULAR DEPENDENCIES
    app.register_blueprint(main_blueprint)

    return app
