import logging
from logging.handlers import TimedRotatingFileHandler
import os

log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')

if not os.path.exists(log_dir):
    os.makedirs(log_dir)


def setup_logging():
    log_file = os.path.join(log_dir, 'app.log')
    # Create a logger
    logger = logging.getLogger('app_logger')

    # Check if the logger already has handlers to avoid duplicates
    if not logger.hasHandlers():
        # Set the logger level
        logger.setLevel(logging.INFO)

        # Create a timed rotating file handler
        handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=7)
        handler.suffix = "%Y-%m-%d"

        # Set the handler level
        handler.setLevel(logging.INFO)

        # Create a formatter and set it for the handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(handler)

        logger.info('Logging setup complete')

    return logger
