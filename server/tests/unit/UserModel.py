# -*- coding: utf-8 -*-
from datetime import datetime
from mongoengine import *


connect('heist')



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
    register = StringField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    contact = StringField()
    password = StringField()
    blgAdmin = StringField()
    privilege = StringField()  # 0-super, 1-admin, 2-user(rw), 3-user(only read)
    lastloginip = StringField()
    lastlogintime = DateTimeField()

def GetPrivilege(username):
    user = User.objects(username=username).first()
    return user.privilege

if __name__ == '__main__':
    pass