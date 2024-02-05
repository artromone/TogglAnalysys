import logging


def setup_logger():
    logger = logging.getLogger("my_app_logger")
    logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger
