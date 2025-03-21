from celery_worker import celery
from flask_mail import Message
from api.create_app import create_app

app = create_app()

@celery.task
def send_bulk_mail(recipients, subject, body):
    with app.app_context():
        try:
            mail = app.extensions['mail']
            for email in recipients:
                msg = Message(
                    subject=subject,
                    recipients=[email],
                    body=body,
                    sender=app.config['MAIL_USERNAME']
                )
                mail.send(msg)
            return {"status": "Emails are being sent"}
        except Exception as e:
            return {"error": str(e)}
