#from . import auth
from flask_jwt import JWT, current_identity,jwt_required
from app.model import User as UserModel
from app.model import AbstractUser as AUserModel
from app.model import Device as DeviceModel
from app import utils
from flask import Response, request
from werkzeug.security import check_password_hash, generate_password_hash,safe_str_cmp
from datetime import datetime
from bson import json_util


class User(object):
    def __init__(self, id, username, password,privile):
        self.id = id
        self.username = username
        self.password = password
        self.privile = privile

    def __str__(self):
        return "User(id='%s')" % self.id



class Auth():
    def error_handler(self, e):
        print(e)
        return "password is not correct", 400

    def authenticate(self, username, password):
        print("authenitcate func")
        # 1. query user on user table
        auser = AUserModel.GetPayloadByUsername(username) 
        if auser:
            if safe_str_cmp(auser['password'].encode('utf-8'), password.encode('utf-8')):
                AUserModel.updateLoginInfo(username,lastloginip=request.remote_addr, lastlogintime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                return User(auser['username'], auser['username'], auser['password'], auser['privilege'])
            else:
                self.error_handler('password is not correct')
           
        else:
            """
            # 2. if cannot find user on user table, check device table
            device = DeviceModel.GetPayloadByUsername(username)
            if device:
                if safe_str_cmp(device.password.encode('utf-8'), password.encode('utf-8')):
                    device.update(lastloginip=request.remote_addr, lastlogintime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    #for deviId user, the privilege is to set '2'
                    return User(device.devId, device.devId, device.password, '5')
                else:
                    self.error_handler('password is not correct')
            else:
            """
            self.error_handler('cannot find user')


    def identity(self, payload):
        print('start to identity')
        username = payload['identity']
        print('username is ' + username)

        auser = AUserModel.GetPayloadByUsername(username)
        if auser:
            return User(auser['username'], auser['username'], auser['password'], auser['privilege'])
