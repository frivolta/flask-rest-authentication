from flask import Flask
from auth.config import configurations
from auth.extensions import db, migrate
import auth.models

from auth.blueprints.products import products
from auth.blueprints.users import users


def create_app(environment_name='dev'):
    app = Flask(__name__)
    app.config.from_object(configurations[environment_name])

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    app.register_blueprint(products, url_prefix="/product")
    app.register_blueprint(users)
    return app
