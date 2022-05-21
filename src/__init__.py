"""Initialize Flask app."""
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_table import Table, Col, LinkCol

# Database setup
from src.config import DevelopmentConfig, TestingConfig

db = SQLAlchemy()


def init_app(test=False):
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False)

    if not test:
        # configure app using the Config class defined in src/config.py
        app.config.from_object(DevelopmentConfig)

        login_manager = LoginManager()
        login_manager.login_view = 'client_bp.login'
        login_manager.init_app(app)

        from .models import User

        @login_manager.user_loader
        def load_user(user_id):
            # since the user_id is just the primary key of our user table, use it in the query for the user
            return User.query.get(int(user_id))



        from src.models import Book, User, Borrow
        db.init_app(app)  # initialise the database for the app
        with app.app_context():
            db.create_all()
    else:
        app.config.from_object(TestingConfig)  # configure app test config

    with app.app_context():
        from src.routes import api_bp,  client_bp
        app.register_blueprint(api_bp)
        app.register_blueprint(client_bp)
        return app
