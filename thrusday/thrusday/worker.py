import logging

from thrusday.settings import APP_TITLE
from celery import Celery

log = logging.getLogger('%s.worker' % (APP_TITLE))
log.setLevel(logging.DEBUG)

retry_delay = 10
max_retries = 3

celery = Celery('thrusday_celery')
celery.conf.task_max_retries = 3
try:
    celery.config_from_object('thrusday.celery_config')
except:
    import celeryconfig
    celery.config_from_object(celeryconfig)
# celery_inspect = celery.control.inspect()


#Task
@celery.task(bind=True, max_retries=max_retries, default_retry_delay=retry_delay, queue='default')
def add(self, num1, num2):
    log.info('adding 2 numbers: %s', self)
    result = num1 + num2
    log.info('result: %s', result)
    return result

