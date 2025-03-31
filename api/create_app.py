import logging
from flask import Flask, render_template, session
from flask_restful import Api
from config import Config 
from flask_limiter import Limiter 
from flask_limiter.util import get_remote_address
from api.extensions import mongo
from flask_cors import CORS
import os
import datetime
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, get_jwt

logger = logging.getLogger("flask_limiter")
logger.setLevel(logging.DEBUG)

limiter = Limiter(
    get_remote_address, 
    storage_uri=os.getenv('redis_url'),
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

    from api.routes import BulkMailSender, TaskHistory
    from api.auth import auth_logout, auth_login, auth_callback, auth_status, auth_delete

    # API Routes
    api.add_resource(BulkMailSender, '/sendMails')
    api.add_resource(TaskHistory, '/tasks')
    api.add_resource(auth_login, '/auth/login')
    api.add_resource(auth_callback, '/auth/callback')
    api.add_resource(auth_status, '/auth/status')
    api.add_resource(auth_logout, '/logout')
    api.add_resource(auth_delete, '/auth/delete/<jwt_token>')

    # Page Routes
    @app.route('/')
    @limiter.limit('50 per 1 minute')
    @jwt_required(optional=True)
    def home():
        return render_template('login.html')      
    
    @app.route('/account')
    def account():
        return render_template('account.html')

    @app.route('/auth/account_data', methods=['GET'])
    @limiter.limit("5 per minute")
    @jwt_required()
    def account_data():
        user = get_jwt_identity()
        user_data =  mongo.db.users.find_one({"email": user}, {"_id": 0, "oauth_token": 1})
        from api.auth import getUserInfo

        if not user_data or "oauth_token" not in user_data:
            return {"error": "User not found or not authenticated"}, 404

        if "user" not in session or session["user"] != user:
            return {"error": "Session mismatch. Please log in again."}, 401
        
        access_token = user_data["oauth_token"].get("access_token")
        if not access_token:
            return {"error": "Access token not found"}, 401

        if not user_data.get("profile_picture"):
            profile = getUserInfo(access_token)
            mongo.db.users.update_one(
                {"email": user},
                {"$set": {"profile_picture": profile['picture']}},
                upsert=True
            )
            profile_picture=profile['picture']
        else:
            profile_picture=user_data.get("profile_picture")
        return {'user': user, 'profile_picture': profile_picture}, 200     
    
    @app.route('/auth/store/')
    def store_token():
        return render_template('store_token.html')

    return app
