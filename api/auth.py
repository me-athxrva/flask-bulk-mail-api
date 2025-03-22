from authlib.integrations.requests_client import OAuth2Session
from flask import session, redirect, request
from flask_restful import Resource
import os
from api.create_app import limiter
from api.extensions import mongo

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_AUTH_REDIRECT_URI = os.getenv("GOOGLE_AUTH_REDIRECT_URI")
GOOGLE_SCOPE = os.getenv("GOOGLE_SCOPE")

def get_google_oauth():
    return OAuth2Session(
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        redirect_uri=GOOGLE_AUTH_REDIRECT_URI,
        scope=GOOGLE_SCOPE,
        token_endpoint_auth_method="client_secret_post" 
    )

class oauth_login(Resource):
    decorators = [limiter.limit("1 per 30 seconds")]
    def get(self):
        google = get_google_oauth()
        authorization_url, state = google.create_authorization_url(
            "https://accounts.google.com/o/oauth2/auth",
            access_type="offline",
            prompt="consent" 
        )
        session["oauth_state"] = state 
        return redirect(authorization_url)
    
class auth_callback(Resource):
    def get(self):
        if "error" in request.args:
            return {"error": request.args["error"]}, 400

        google = get_google_oauth()
        token = google.fetch_token(
            "https://oauth2.googleapis.com/token",
            authorization_response=request.url
        )

        # Fetch user info
        google = get_google_oauth()
        google.token = token
        user_info = google.get("https://www.googleapis.com/oauth2/v3/userinfo").json()

        if not user_info:
            return {"error": "Failed to retrieve user info"}, 400

        user_email = user_info["email"]
        
        # storing tokens in mongodb
        mongo.db.users.update_one(
            {"email": user_email},
            {"$set": {"oauth_token": token}},
            upsert=True
        )

        session["user"] = user_email
        return {"message": "Login successful", "email": user_email}
    
class auth_logout(Resource):
    def get(self):
        session.pop("user", None)
        return {"message": "Logged out"}