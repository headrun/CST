#!/usr/bin/env python

from settings.prod_settings import *

IN_CELERY = True


CELERY_DEFAULT_QUEUE = 'celery-prod'
CELERY_QUEUES = {
    CELERY_DEFAULT_QUEUE: {
        'exchange': CELERY_DEFAULT_QUEUE,
        'binding_key': CELERY_DEFAULT_QUEUE,
    }
}
CELERY_EMAIL_TASK_CONFIG['queue'] = CELERY_DEFAULT_QUEUE
CELERY_EMAIL_TASK_CONFIG = {}
