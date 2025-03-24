from flask import Flask, render_template, jsonify
from flask_restful import Api
from config import Config 
from flask_limiter import Limiter 
from flask_limiter.util import get_remote_address
from api.extensions import mongo
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
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=1)

    mongo.init_app(app) # mongo db
    limiter.init_app(app) # rate limiting
    api = Api(app)
    jwt.init_app(app)

    from api.server_status import checkServerStatus
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
        if checkServerStatus() == True:
            return render_template('login.html')
        return jsonify({'error', 'server error'})      
    
    @app.route('/auth/store/')
    def store_token():
        return render_template('store_token.html')

    return app
