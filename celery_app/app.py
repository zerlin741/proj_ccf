from celery import Celery

app = Celery('celery_demo')
app.config_from_object('celery_app.config')


