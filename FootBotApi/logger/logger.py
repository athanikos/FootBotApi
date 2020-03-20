import logging

from FootBotApi import config
from flask import current_app as app


def log_error(exception, match_id, web_method_name):
    logging.basicConfig(filename=app.config['LOGS_PATH'], level=logging.ERROR)
    logging.error(str(match_id) + ' ' + str(web_method_name) + ' ' + str(exception))
