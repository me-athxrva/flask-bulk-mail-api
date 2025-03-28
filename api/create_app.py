from flask import Flask, render_template
from flask_restful import Api
from config import Config 
from flask_limiter import Limiter 
from flask_limiter.util import get_remote_address
from api.extensions import mongo
from flask_cors import CORS
import os
import datetime
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required

limiter = Limiter(
    get_remote_address, 
    storage_uri="redis://localhost:6379",
    default_limits=["10 per minute"] # default limit
)
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config) # config for credentials

    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    app.config["APP_SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=12)

    mongo.init_app(app) # mongo db
    limiter.init_app(app) # rate limiting
    CORS(app)
    api = Api(app)
    jwt.init_app(app)

    from api.routes import BulkMailSender, TaskStatus
    from api.auth import auth_logout, auth_login, auth_callback, auth_status

    # API Routes
    api.add_resource(BulkMailSender, '/sendMails')
    api.add_resource(TaskStatus, '/taskStatus/<task_id>')
    api.add_resource(auth_login, '/auth/login')
    api.add_resource(auth_callback, '/auth/callback')
    api.add_resource(auth_status, '/auth/status')
    api.add_resource(auth_logout, '/logout')

    # Page Routes
    @app.route('/')
    @jwt_required(optional=True)
    def home():
        decorators = [limiter.limit("50 per 1 minute")]
        return render_template('login.html')      
    
    @app.route('/auth/store/')
    def store_token():
        return render_template('store_token.html')

    return app
