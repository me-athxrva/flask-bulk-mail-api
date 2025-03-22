from flask import Flask
from flask_restful import Api
from flask_mail import Mail
from config import Config 
from flask_limiter import Limiter 
from flask_limiter.util import get_remote_address

mail = Mail()
limiter = Limiter(
    get_remote_address, 
    storage_uri="redis://localhost:6379",
    default_limits=["10 per minute"] # default limit
)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config) # config for credentials

    mail.init_app(app) # flask mailer
    limiter.init_app(app) # rate limiting
    api = Api(app)

    from api.routes import BulkMailSender, TaskStatus  
    api.add_resource(BulkMailSender, '/sendMails')
    api.add_resource(TaskStatus, '/taskStatus/<task_id>')

    return app
