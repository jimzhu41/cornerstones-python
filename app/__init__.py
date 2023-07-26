from flask import Flask, current_app,request
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from config import config, Config


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view='auth.login'
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()

def create_app(config_class=Config):
    app = Flask(__name__,template_folder='/Users/jimzhu/PycharmProjects/cornerstones/templates')
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    from app.models  import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.main import main as main_bp
    app.register_blueprint(main_bp)

    from app.auth import auth as auth_bp
    app.register_blueprint(auth_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    return app

from app import models


