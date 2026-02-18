from thursday.settings import RCELERY_HOST, RCELERY_CHANNEL, REDIS_PASSWORD
from kombu import Queue, Exchange

task_acks_late = True
# worker_send_task_events = True
broker_url = f'redis://:{REDIS_PASSWORD}@{RCELERY_HOST}:6379/{RCELERY_CHANNEL}'
result_backend = f'redis://:{REDIS_PASSWORD}@{RCELERY_HOST}:6379/{RCELERY_CHANNEL}'

beat_schedule_filename = '/tmp/thursday_celerybeat.db'
beat_schedule = {
    'scheduled-task-queue': {
        'task': 'thursday.worker.add',
        'schedule': 3600,  # 'every xx seconds' (NOTE: value should be float type)
        'args': (10, 10),
    },
}
timezone = 'UTC'
accept_content = ['pickle', 'json']
task_serializer = 'json'

task_default_queue = 'default'

default_exchange = Exchange('default', type='direct')

task_queues = (
    Queue('default', default_exchange, routing_key='thursday.default'),
)

task_routes = {
    # 'hivesac.celery.worker.send_push_notification': {'queue': 'notification', 'routing_key': 'hivesac.notification'},
    # 'hivesac.celery.worker.compound_thresholds': {'queue': 'compound', 'routing_key': 'hivesac.compound'},
    # 'hivesac.celery.worker.handleEvent': {'queue': 'issues', 'routing_key': 'hivesac.issues'},
    # 'hivesac.celery.worker.updateHealthscore': {'queue': 'health', 'routing_key': 'hivesac.health'},
    # 'hivesac.celery.worker.handleUplink': {'queue': 'uplink', 'routing_key': 'hivesac.uplink'}
}

ONCE = {
    'backend': 'celery_once.backends.Redis',
    'settings': {
        'url': broker_url,
        'default_timeout': 60 * 60
    }
}