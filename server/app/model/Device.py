# -*- coding: utf-8 -*-

from app import utils
from app import db
#from model.device import Device1


from playhouse.shortcuts import model_to_dict, dict_to_model

from datetime import datetime
import logging

# 用户管理
# 类名定义 collection
class Device(db.Document):
    meta = {
        'collection': 'device',
        'ordering': ['-create_at'],
        'strict': False,
    }

    # 字段
    comment = db.StringField()
    devId = db.StringField()
    password = db.StringField()
    devPwd = db.StringField()
    position = db.StringField()
    comment2 = db.StringField()
    expiry = db.IntField()
    blgAdmin = db.StringField()
    blgQMUser = db.StringField()
    blgQUser = db.StringField()
    createtime = db.StringField()
    lastloginip = db.StringField()
    lastlogintime = db.DateTimeField()
    privilege = db.StringField()

def GetPayloadByUsername(username):
    return Device.objects(devId=username).only('devId','password').first()



def SearchDeviceByName(page_num, item_per_page,name, loginUser=None):
    condition = {'devId__icontains':name}
    if loginUser:
        condition['blgAdmin'] = loginUser
    count = Device.objects(**condition).count()
    devices = []
    for dev in Device.objects(**condition).paginate(page=page_num, per_page=item_per_page).items:
        devices.append({'devId':dev.devId, 'password':dev.password, 'devPwd':dev.devPwd, 'comment':dev.comment,'expiry':dev.expiry,\
                        'blgAdmin':dev.blgAdmin, 'blgQMUser':dev.blgQMUser,'blgQUser':dev.blgQUser,\
                        'createtime':dev.createtime, 'comment2':dev.comment2,'position':dev.position})

    return count, devices


def GetDevices(page_num, item_per_page, devId=None, addr=None, admin=None, loginUser=None, privilege=None):
    devices = []
    cnd = {}
    if devId:
        cnd['devId__icontains'] = devId
    if addr:
        cnd['comment2__icontains'] = addr
    if admin:
        cnd['blgAdmin__icontains'] = admin
    if loginUser:
        if privilege == '2':
            cnd['blgQMUser'] = loginUser
        if privilege == '3':
            cnd['blgQUser'] = loginUser
        if privilege == '1':
            cnd['blgAdmin'] = loginUser   
    count = Device.objects(**cnd).count()
    for dev in Device.objects(**cnd).paginate(page=page_num, per_page=item_per_page).items:
        devices.append({'devId':dev.devId, 'password':dev.password, 'devPwd':dev.devPwd, 'comment':dev.comment,'expiry':dev.expiry,\
                        'blgAdmin':dev.blgAdmin, 'blgQMUser':dev.blgQMUser,'blgQUser':dev.blgQUser,\
                        'createtime':dev.createtime, 'comment2':dev.comment2,'position':dev.position})

    return count, devices


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
    count = Device.objects(**cnd).count()
    for dev in Device.objects(**cnd).all():
        if dev.comment2:
            addrs.append(dev.comment2[:3])
        else:
            addrs.append("unkonw")


    return count, addrs



def GetDeviceByDevId(devId):
    return Device.objects(devId=devId).first()


def UpdateDevice(devid, **data):
    errcode = 1
    dev = Device.objects(devId=devid)
    if dev:
        dev.update(**data)
        errcode = 0
    return errcode


def DeleteDevice(devId):
    errcode = 0
    device = Device.objects(devId=devId)
    device.delete()
    if Device.objects(devId=devId):
        errcode = 1
    return errcode

def GetDevIds(privilege, loginUser, devid=None):
    devIds = []
    cnd = {}
    if privilege == '5':  # it mean login as devId
        cnd['devId'] = loginUser
    else:
        if privilege == '1':
            cnd['blgAdmin'] = loginUser
        if privilege == '2':
            cnd['blgQMUser'] = loginUser
        if privilege == '3':
            cnd['blgQUser'] = loginUser
        if devid:
            cnd['devId__icontains'] = devid
    for dev in Device.objects(**cnd).only('devId', 'comment2').all():
        #devIds.append(dev.devId+dev.)
        if dev.comment2:
            devIds.append({'value':dev.devId, 'label':dev.comment2+'('+dev.devId+')'})
        else:
            devIds.append({'value':dev.devId, 'label':'unknow'+'('+dev.devId+')'})
    return devIds