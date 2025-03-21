from flask import Flask
from flask_restful import Api
from flask_mail import Mail
from config import Config  

mail = Mail()

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    mail.init_app(app)
    api = Api(app)

    from api.routes import BulkMailSender, TaskStatus  
    api.add_resource(BulkMailSender, '/sendMails')
    api.add_resource(TaskStatus, '/taskStatus/<task_id>')

    return app
