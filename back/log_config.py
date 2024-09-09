import logging
from logging.handlers import TimedRotatingFileHandler
import os

log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

def setup_logging():
    log_file = os.path.join(log_dir, 'app.log')
    handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=7)
    handler.suffix = "%Y-%m-%d"
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger('app_logger')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    logger.info('Logging setup complete')

    return logger
