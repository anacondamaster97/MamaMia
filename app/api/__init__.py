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
    from .api.users import users_blueprint
    from .api.posts import posts_blueprint
    app.register_blueprint(users_blueprint, url_prefix='/api/v1/users')
    app.register_blueprint(posts_blueprint, url_prefix='/api/v1/posts')

    return app
