from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import config_by_name

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    Migrate(app, db)

    # Register Blueprints (APIs)
    from .api.recipes import recipes_blueprint
    from .api.impages import images_blueprint
    app.register_blueprint(recipes_blueprint, url_prefix='/api/v1/recipe')
    app.register_blueprint(images_blueprint, url_prefix='/api/v1/images')

    return app
