import os
from flask import Flask
from .config import config
from .exts import db
from .api import api_blueprint
from .manage import migrate
from .api.models.user import UserModel
from flask_jwt_extended import JWTManager
from .api.models.revoked_token import RevokedTokenModel
from flask_cors import CORS

def create_app(config_name):
    # Initialize the Flask project
    app = Flask(__name__)

    CORS(app)

    # Load configuration settings
    app.config.from_object(config[config_name])

    # Initialize the ORM database
    db.init_app(app)

    # Initialize the ORM database migration plugin
    migrate.init_app(app, db)

    # Register the API blueprint
    app.register_blueprint(api_blueprint)

    # init jwt
    jwt = JWTManager(app)
    register_jwt_hooks(jwt)

    return app

def register_jwt_hooks(jwt):
    # Register JWT hooks to check if the token is in the blacklist
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, decrypted_token):
        # Retrieve the JWT identifier (jti) from the decrypted token
        jti = decrypted_token['jti']
        # Check if the jti is blacklisted using the RevokedTokenModel
        return RevokedTokenModel.is_jti_blacklisted(jti)

# Initialize the project
app = create_app(os.getenv('FLASK_ENV', 'development'))