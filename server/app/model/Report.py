# -*- coding: utf-8 -*-

from app import utils
from app import db
#from model.device import Device1


from playhouse.shortcuts import model_to_dict, dict_to_model

from datetime import datetime


# 用户管理
# 类名定义 collection
class Report(db.Document):
    meta = {
        'collection': 'reportdata',
        'ordering': ['-startdate'],
        'strict': False,
    }

    # 字段
    washId = db.StringField()
    startdate = db.StringField()
    enddate = db.StringField()
    seq = db.StringField()
    prio = db.StringField()
    devId = db.StringField()

    step = db.StringField()
    starttime = db.StringField()
    endtime = db.StringField()
    pumpnum = db.IntField()
    formula = db.IntField()
    pumps = db.DictField()




def GetRecordsByDevIdDate(devId, startdate, enddate):
    records = []
    for rec in Report.objects(devId=devId,startdate__gte=startdate,enddate__lte=enddate).all():
        records.append({'step':rec.step,'washId':rec.washId,'formula':rec.formula, 'pumps':rec.pumps})
    
    return records



def UpdateUser(devid, **data):
    errcode = 1
    dev = Device.objects(devId=devid)
    if dev:
        dev.update(**data)
        errcode = 0
    return errcode


def DeleteUser(devId):
    errcode = 0
    device = Device.objects(devId=devId)
    device.delete()
    if Device.objects(devId=devId):
        errcode = 1
    return errcode