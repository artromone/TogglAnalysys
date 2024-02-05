import logging

class SingletonLogger:
    _instance = None

    def __init__(self):
        self._logger = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(SingletonLogger, cls).__new__(cls)
            cls._instance._logger = None
        return cls._instance

    def setup_logger(self):
        if not self._logger:
            self._logger = logging.getLogger("my_app_logger")
            self._logger.setLevel(logging.DEBUG)

            stream_handler = logging.StreamHandler()

            formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
            stream_handler.setFormatter(formatter)
            self._logger.addHandler(stream_handler)

    @staticmethod
    def instance():
        if not SingletonLogger._instance or not SingletonLogger._instance._logger:
            SingletonLogger._instance.setup_logger()

        return SingletonLogger._instance._logger
