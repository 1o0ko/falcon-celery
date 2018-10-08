# project/app/server/__init__.py
'''
Super smart tasks
'''
import json
import falcon

from server.ml import Model
from server.tasks import TaskWithModel
from server.tasks import app as celery_app

from celery.result import AsyncResult


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
            'status': task_result.status,
            'result': task_result.result
        }

        resp.status = falcon.HTTP_200
        resp.body = json.dumps(result)


task = TaskWithModel(Model())
celery_app.tasks.register(task)

app = falcon.API()
app.add_route('/create', CreateTask(task))
app.add_route('/status/{task_id}', CheckStatus())
