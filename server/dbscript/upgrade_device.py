# -*- coding: utf-8 -*-
from datetime import datetime
from mongoengine import *


connect('heist')


# 用户管理
# 类名定义 collection
class Device(Document):
    meta = {
        'collection': 'device',
        'ordering': ['-devId'],
        'strict': False,
    }

    # 字段
    comment = StringField()
    devId = StringField()
    password = StringField()
    position = StringField()
    comment2 = StringField()
    expiry = IntField()
    blgAdmin = StringField()
    blgQMUser = StringField()
    blgQUser = StringField()
    createtime = StringField()
    lastloginip = StringField()
    lastlogintime = DateTimeField()
    privilege = StringField()    

class User(Document):
    meta = {
        'collection': 'user_v2',
        'ordering': ['-create_at'],
        'strict': False,
    }

    # 字段
    username = StringField(required=True)
    devId = StringField()
    name = StringField()
    register = StringField()
    contact = StringField()
    password = StringField()
    isAdmin = BooleanField(default=False)
    belongAdmin = StringField()
    privilege = StringField()
    createtime = DateTimeField()
    lastloginip = StringField()
    lastlogintime = DateTimeField(default=datetime.now)




def UpdateDeviceBlgUser(devidList, username, privilege):
    for devid in devidList:
        cnd = {}
        if privilege == '1':
            cnd = {'blgAdmin':username}
        elif privilege == '2':
            cnd = {'blgQMUser':username}
        else:
            cnd = {'blgQUser':username}
        device = Device.objects(devId=devid).first()
        if device:
            device.update(**cnd)


if __name__ == '__main__':
    # 1. get devId list from user_v2.devId and split it
    for user in User.objects.only('devId','username', 'privilege').all():
        if user.username == 'heist':
            continue
        print(user.devId, user.username, user.privilege)
        devIdList = user.devId.split(',')
        UpdateDeviceBlgUser(devIdList, user.username, user.privilege)
        print("update %s user done"%user.username)
