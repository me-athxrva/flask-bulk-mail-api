from celery import Celery
from api.create_app import create_app
import os

broker_url = os.getenv('broker_url')
backend_url = os.getenv('result_backend')

def create_celery_app():
    app = create_app()

    celery_instance = Celery(
        app.import_name,
        broker=broker_url,
        backend=backend_url,
        include=["api.tasks"] 
    )
    celery_instance.conf.task_result_expires = 86400
    celery_instance.conf.update({
        'broker_url': broker_url,
        'result_backend': backend_url,
        'redis_backend_use_ssl': {
            'ssl_cert_reqs': 'CERT_REQUIRED'
        }
    })

    celery_instance.conf.update(app.config)

    class ContextTask(celery_instance.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_instance.Task = ContextTask
    return celery_instance

celery = create_celery_app()
