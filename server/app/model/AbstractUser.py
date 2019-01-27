# -*- coding: utf-8 -*-

from app import utils
from app import db
from datetime import datetime

from app.model import User as UserModel
from app.model import Device as DeviceModel


def GetPayloadByUsername(username):
    user = UserModel.User.objects(username=username).first()
    if user:
        return {'id':user.username,'username':user.username, 'password':user.password, 'privilege':user.privilege}
    else:
        device = DeviceModel.Device.objects(devId=username).first()
        if device:
            return {'id':device.devId,'username':device.devId, 'password':device.password, 'privilege':'5'}

def IsExist(username):
    return (UserModel.User.objects(username=username).first() or DeviceModel.Device.objects(devId=username).first())

def GetPrivilege(username):
    user = UserModel.User.objects(username=username).first()
    if user:
        return user.privilege
    else:
        device = DeviceModel.Device.objects(devId=username).first()
        if device:
            return device.privilege
        else:
            return None

def updateLoginInfo(username, **data):
    user = UserModel.User.objects(username=username)
    if user:
        user.update(**data)
    else:
        device = DeviceModel.Device.objects(devId=username)
        if device:
            device.update(**data)

def ChangePwd(username, oldpwd, newpwd):
    errcode = 1
    user = UserModel.User.objects(username=username).first()
    if user:
        #user.update(**data)
        # compare new password and old password
        if oldpwd == user.password:
            user.password = newpwd
            user.save()
            errcode = 0
    else:
        device = DeviceModel.Device.objects(devId=username).first()
        if device:
            # compare new password and old password
            if oldpwd == device.password:
                device.password = newpwd
                device.save()
                errcode = 0

    return errcode

