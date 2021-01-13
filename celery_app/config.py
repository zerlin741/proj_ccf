from kombu import Queue, Exchange

CELERY_TIMEZONE = "Asia/Shanghai"
BROKER_URL = "pyamqp://guest:guest@localhost:5672/celery"
CELERY_RESULT_BACKEND = "rpc://"
CELERY_IMPORTS = ["celery_pyrunner", ]
MAX_TASKS_PER_CHILD = 10
CELERY_QUEUES = (
  Queue('celery', Exchange('celery'), routing_key='celery', queue_arguments={'x-max-priority': 10}),
  Queue('high_priority', Exchange('high_priority'), routing_key='priority.#', queue_arguments={'x-max-priority': 10}),
)
# CELERY_ROUTES = {
#   'high_priority_runner.run_job': {'queue': 'high_priority', 'routing_key': 'priority.run_job'},
# }

CELERYD_PREFETCH_MULTIPLIER = 0
CELERY_ACKS_LATE = True
CELERY_QUEUE_MAX_PRIORITY = 10



