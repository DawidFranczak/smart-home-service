import logging
from logging.handlers import RotatingFileHandler


def setup_rabbit_consumer_logger():
    logger = logging.getLogger("rabbit_consumer")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = RotatingFileHandler(
        "rabbit_consumer.log", maxBytes=10 * 1024 * 1024, backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
