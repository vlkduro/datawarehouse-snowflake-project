# logger_setup.py

import os
import logging

def setup_logger(name: str) -> logging.Logger:
    log_dir = os.path.join(os.path.dirname(__file__),'..' ,'logs')
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, 'executions.log')

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Pour éviter les handlers dupliqués si setup_logger est appelé plusieurs fois
    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

        file_handler = logging.FileHandler(log_file, mode='a')
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger