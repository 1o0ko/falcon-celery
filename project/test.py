# project/test.py

import unittest

from falcon import testing

from app import app, tasks


class TestAppRoutes(testing.TestCase):
    def setUp(self):
        super(TestAppRoutes, self).setUp()
        self.app = app

    def test_get_message(self):
        result = self.simulate_get('/ping')
        self.assertEqual(result.json, 'pong!')


class TestCeleryTasks(unittest.TestCase):

    def test_fib_task(self):
        self.assertEqual(tasks.fib.run(-1), [])
        self.assertEqual(tasks.fib.run(1), [0, 1])
        self.assertEqual(tasks.fib.run(3), [0, 1, 1, 2])
        self.assertEqual(tasks.fib.run(5), [0, 1, 1, 2, 3, 5])


if __name__ == '__main__':
    unittest.main()
