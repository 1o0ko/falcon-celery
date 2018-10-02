import logging
from time import sleep


class Model:
    def __init__(self):
        self.called = 0

    def predict(self, x):
        self.called += 1
        sleep(2)

        logger = logging.getLogger(__name__)
        logger.info(self.called)
        return x + 1
