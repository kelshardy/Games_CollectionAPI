from flask import Flask
from init import db, ma, bcrypt, jwt
import os
from controllers.cli_controller import db_commands
from controllers.auth_controller import auth_bp
from controllers.collection_controller import collections_bp
from controllers.review_controller import reviews_bp
from controllers.game_controller import games_bp

def create_app():
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"]=os.environ.get("DATABASE_URL")
    app.config["JWT_SECRET_KEY"]=os.environ.get("JWT_SECRET_KEY")
    
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    app.register_blueprint(db_commands)
    app.register_blueprint(auth_bp)
    app.register_blueprint(collections_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(games_bp)
    
    return app