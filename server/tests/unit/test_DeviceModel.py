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
    devPwd = StringField()
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



def GetDevidsByUser(privilege, username):
    #return Administrator.get_or_none(Administrator.username == username, Administrator.status == STATUS_VALID)
    cnd = {}
    devIds = []
    if privilege != '0':
        cnd['blgAdmin'] = username
    print("cnd is ", cnd)
    for dev in Device.objects(**cnd).only('devId').all():
        devIds.append(dev.devId)

    return devIds
    



def test_get_devIds():
    """
    GIVEN a User model
    WHEN query a exit user
    THEN check username, password, privilege
    """
    privilege= '0'
    loginUser = 'heist'

    devIds = GetDevidsByUser(privilege, loginUser)
    print(devIds)
    
    #assert new_studguard.member_id == 22
    #assert new_studguard.relationship == 3
    #

def set_privilegefordevices():
    privilege = '5'
    for dev in Device.objects.all():
        dev.privilege = '5'
        dev.save()

def set_devPWDfordevices():
    for dev in Device.objects.all():
        dev.devPwd = '000000'
        dev.save()


def GetDevScatter(devId=None,loginUser=None, privilege=None):
    addrs = []
    cnd = {}
    if devId:
        cnd['devId__icontains'] = devId
    if loginUser:
        if privilege == '2':
            cnd['blgQMUser'] = loginUser
        if privilege == '3':
            cnd['blgQUser'] = loginUser
        if privilege == '1':
            cnd['blgAdmin'] = loginUser   
    print("cnd is ", cnd)
    count = Device.objects(**cnd).count()
    print("count is ", count)
    for dev in Device.objects(**cnd).all():
        print(dev.comment2)
        if dev.comment2:
            addrs.append(dev.comment2[:3])
    countDict =  {}
    for add in set(addrs):
        countDict[add] = addrs.count(add)


    return count, countDict

if __name__ == '__main__':
    #set_devPWDfordevices()
    #set_privilegefordevices()
    count, addrs = GetDevScatter(loginUser='heist', privilege='0')
    print(count, addrs)
    
