'''
Stupid Model wrapper
'''
import logging
import os

from celery import Celery
from celery import Task

CELERY_BROKER = os.environ.get('CELERY_BROKER')
CELERY_BACKEND = os.environ.get('CELERY_BACKEND')

app = Celery('tasks', broker=CELERY_BROKER, backend=CELERY_BACKEND)


class TaskWithModel(Task):
    name = 'task_with_a_model'

    def __init__(self, model):
        self.model = model

    def run(self, x):
        logger = logging.getLogger(__name__)
        logger.debug(f"Calling model: {x}")

        return self.model.predict(x)
