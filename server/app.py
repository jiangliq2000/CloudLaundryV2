#!/usr/bin/env python3
import os
#import logging
#import logging.config 
from app import create_app
from app.logging.log import logger
import datetime
from flask import redirect, render_template



#logging.config.fileConfig('conf/log-app.conf',disable_existing_loggers=False)
#logger = logging.getLogger()


#gunicorn_error_handlers = logging.getLogger('gunicorn.error').handlers

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

#app.logger.handlers.extend(gunicorn_error_handlers )

"""
@app.before_request
def before_request():
    print("receive request")
    print(datetime.datetime.now())


@app.after_request
def record_loginUser(response):
    print("after request")
    print(datetime.datetime.now())    
    return response

@app.route('/')
def index():
    return render_template('index.html')
"""


if __name__ == '__main__':
    logger.debug("###########################################################")
    logger.debug("----------receiver restart --------------")
    logger.debug("###########################################################")
    app.run(host="0.0.0.0", port=80, debug = True)
