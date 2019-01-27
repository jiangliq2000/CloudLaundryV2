from flask import Flask, render_template
from flask_jwt import JWT
from conf.config import config
#import logging
#import logging.config
from app.logging.log import logger
import os

from flask_mongoengine import MongoEngine

db = MongoEngine()

#logging.config.fileConfig('conf/log-app.conf')



def get_basedir():
    return os.path.abspath(os.path.dirname(__file__))


def get_config():
    return config[os.getenv('FLASK_CONFIG') or 'default']


def create_app(config_name):
    app = Flask(__name__)
    print("__name__: " + __name__)
    print("config_name: " + config_name)
    print(config[config_name])
    app.config.from_object(config[config_name])

    #app.config['MONGODB_SETTINGS'] = {'db':'heist','host': '127.0.0.1','port': 27017}
    db.init_app(app)

    
    app.url_map.strict_slashes = False
    config[config_name].init_app(app)

    from app.auth.auths import Auth
    auth = Auth()
    jwt = JWT(app, auth.authenticate, auth.identity)
    #jwt.jwt_error_callback = auth.error_handler
   
    @app.route('/')
    def index():
        return render_template('index.html')
    

    from .rest import rest as rest_blueprint
    app.register_blueprint(rest_blueprint,url_prefix='/api/v1')

    print("regiseter blueprint")

    #from .auth import auth as auth_blueprint
    #app.register_blueprint(auth_blueprint,url_prefix='/auth')
    
    """
    from .member import member as member_blueprint
    app.register_blueprint(member_blueprint, url_prefix='/api/v1/members')

    from .student import student as student_blueprint
    app.register_blueprint(student_blueprint, url_prefix='/api/v1/students')
    """


    return app
