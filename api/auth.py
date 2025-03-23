from authlib.integrations.requests_client import OAuth2Session
from flask import session, redirect, request, render_template
from flask_restful import Resource
import os
import requests
from api.create_app import limiter
from api.extensions import mongo
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

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

class auth_login(Resource):
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
        
        jwt_email = create_access_token(identity=user_email)

        # storing tokens in mongodb
        mongo.db.users.update_one(
            {"email": user_email},
            {"$set": {"oauth_token": token}},
            upsert=True
        )

        session["user"] = user_email
        frontend_url = f'/auth/store/?tk={jwt_email}'
        return redirect(frontend_url)
    
class auth_logout(Resource):
    def get(self):
        session.pop("user", None)
        frontend_url = '/'
        return redirect(frontend_url)
    
class auth_status(Resource):
    @jwt_required()
    def get(self):
        user = get_jwt_identity()
        user_data = mongo.db.users.find_one({"email": user}, {"_id": 0, "oauth_token": 1})

        if not user_data or "oauth_token" not in user_data:
            return {"error": "User not found or not authenticated"}, 404

        if "user" not in session or session["user"] != user:
            return {"error": "Session mismatch. Please log in again."}, 401
        
        access_token = user_data["oauth_token"].get("access_token")

        if not access_token:
            return {"error": "Access token not found"}, 401
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get("https://www.googleapis.com/oauth2/v3/userinfo", headers=headers)

        if response.status_code == 200:
            profile_info = response.json()
            profile_picture = profile_info.get("picture") 

        html_content = render_template('main.html', profile_pic=profile_picture)
        return {"message": "User authenticated",'html': html_content}, 200