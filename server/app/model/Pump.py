# -*- coding: utf-8 -*-

from app import utils
from app import db

from datetime import datetime


# 用户管理
# 类名定义 collection
class Pump(db.Document):
    meta = {
        'collection': 'pumpcfg',
        'strict': False,
    }
    # 字段
    pumpnum = db.IntField()
    devId = db.StringField()
    pumps = db.DictField()


def GetPumpByDevId(devId):
    return Pump.objects(devId=devId).first()


def UpdatePumpByDevId(devid, pumps):
    errcode = 1
    record = Pump.objects(devId=devid).first()
    if record:
        for i in range(1, len(pumps)+1):
            record.pumps['pump%d'%i]['speed']= pumps['pump%d'%i]
        record.save()
        errcode = 0
    return errcode


def DeletePumpByDevId(devId):
    errcode = 0
    pump = Pump.objects(devId=devId)
    pump.delete()
    if Pump.objects(devId=devId):
        errcode = 1
    return errcode