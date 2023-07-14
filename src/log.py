import os
import logging

log_file = os.path.abspath("../logs/app.log")

logging.basicConfig(
    level=logging.DEBUG,
    filename=log_file,
    filemode='w',
    format='%(asctime)s [%(levelname)s] %(message)s'
)

logging.debug('Log start')
