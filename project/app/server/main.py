'''
Super smart tasks
'''
import json
import falcon

from celery.result import AsyncResult
from server.tasks import task_with_model


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


app = falcon.API()
app.add_route('/create', CreateTask(task_with_model))
app.add_route('/status/{task_id}', CheckStatus())
