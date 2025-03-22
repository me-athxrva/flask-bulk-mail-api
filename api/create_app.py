from flask import Flask
from flask_restful import Api
from config import Config 
from flask_limiter import Limiter 
from flask_limiter.util import get_remote_address
from api.extensions import mongo
import os

limiter = Limiter(
    get_remote_address, 
    storage_uri="redis://localhost:6379",
    default_limits=["10 per minute"] # default limit
)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config) # config for credentials

    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    app.config["APP_SECRET_KEY"] = os.getenv("SECRET_KEY")
    mongo.init_app(app) # mongo db
    limiter.init_app(app) # rate limiting
    api = Api(app)

    from api.routes import BulkMailSender, TaskStatus
    from api.auth import auth_logout, oauth_login, auth_callback  
    api.add_resource(BulkMailSender, '/sendMails')
    api.add_resource(TaskStatus, '/taskStatus/<task_id>')
    api.add_resource(oauth_login, '/auth/login')
    api.add_resource(auth_callback, '/auth/callback')
    api.add_resource(auth_logout, '/logout')

    return app
