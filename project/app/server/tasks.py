import os
import logging

from celery import Celery
from celery import Task

CELERY_BROKER = os.environ.get('CELERY_BROKER')
CELERY_BACKEND = os.environ.get('CELERY_BACKEND')

app = Celery('tasks', broker=CELERY_BROKER, backend=CELERY_BACKEND)


class TaskWithModel(Task):
    name = 'model_task'

    def __init__(self, model):
        self.model = model

    def run(self, x):
        logger = logging.getLogger(__name__)
        logger.info(f"Calling model: {x}")

        return self.model.predict(x)
