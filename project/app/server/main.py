'''
Super smart tasks
'''
import os
import json
import logging
logging.basicConfig(
    format="%(asctime)s [%(threadName)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO)

import falcon

from celery.result import AsyncResult
from server.tasks import task_with_model
from server import images


class CreateTask:
    def __init__(self, task):
        self.task = task

    def on_post(self, req, resp):
        # loads the data from request
        raw_json = req.stream.read()
        result = json.loads(raw_json, encoding='utf-8')
        number = int(result['number'])

        # do the task
        task = self.task.delay(number)

        # repares the response
        resp.status = falcon.HTTP_200
        result = {
            'status': 'success',
            'data': {
                'task_id': task.id
            }
        }
        resp.body = json.dumps(result)


class CheckStatus:
    def on_get(self, req, resp, task_id):
        task_result = AsyncResult(task_id)
        result = {
            'task_id': task_id,
            'status': task_result.status,
            'result': task_result.result
        }

        resp.status = falcon.HTTP_200
        resp.body = json.dumps(result)


def create_app(image_store):
    logger = logging.getLogger(__name__)
    app = falcon.API()

    # Model API
    app.add_route('/create', CreateTask(task_with_model))
    app.add_route('/status/{task_id}', CheckStatus())

    # Images API
    app.add_route('/images', images.Collection(image_store))
    app.add_route('/images/{name}', images.Item(image_store))

    logger.info('Ready to serve!')
    return app


def get_app():
    storage_path = os.environ.get('STORAGE_PATH', '.')
    image_store = images.ImageStore(storage_path)
    return create_app(image_store)
