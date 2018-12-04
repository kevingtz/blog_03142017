# THIS IS THE APPLICATION FACTORY FILE

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_pagedown import PageDown
from config import config

# HERE WE GONNA CREATED THE EXTENSION BUT UNINITIALIZED
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()

login_manager = LoginManager()  # THIS CREATE A INSTANCE OF THE LOGIN MANAGER CLASS
login_manager.session_protection = 'strong'  # [NONE, BASIC, STRONG] THESE ARE THE SECURITY LEVELS
# SETTING TO STRONG WILL KEEP TRACK THE CLIENT'S IP ADDRESS AND BROWSER AGENT AND WILL LOG THE USER OUT
# IF IT DETECT A CHANGE
login_manager.login_view = 'auth.login'  # THE LOGIN ROUTE


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
    login_manager.init_app(app)
    pagedown.init_app(app)

    # IMPORTING THE 'MAIN_BLUEPRINT'
    from .main import main as main_blueprint  # AVOIDING THE CIRCULAR DEPENDENCIES
    app.register_blueprint(main_blueprint)

    # IMPORTING THE 'AUTH_BLUEPRINT'
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
