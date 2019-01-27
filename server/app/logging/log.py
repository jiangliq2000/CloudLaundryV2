# -*- coding:utf-8 -*-  
__author__ = 'liqiang'


import logging
import logging.config 

logging.config.fileConfig('app/logging/log-app.conf')
logger = logging.getLogger()