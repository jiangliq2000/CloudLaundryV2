# -*- coding: utf-8 -*-

from app import utils
from app import db

from datetime import datetime


# 用户管理
# 类名定义 collection
class Wash(db.Document):
    meta = {
        'collection': 'valvecfg',
        'strict': False,
    }
    # 字段
    washnum = db.IntField()
    devId = db.StringField()
    washs = db.DictField()


def GetWashByDevId(devId):
    return Wash.objects(devId=devId).first()


def UpdateWashByDevId(devid, wash, washIndex):
    errcode = 1
    record = Wash.objects(devId=devid).first()
    if record:
        record.washs['wash%d'%washIndex]['inopen'] = wash['inopen']
        record.washs['wash%d'%washIndex]['inclose'] = wash['inclose']
        record.washs['wash%d'%washIndex]['outopen'] = wash['outopen']
        record.washs['wash%d'%washIndex]['outclose'] = wash['outclose']
        record.save()
        errcode = 0
    return errcode


def DeleteWashByDevId(devId):
    errcode = 0
    wash = Wash.objects(devId=devId)
    wash.delete()
    if Wash.objects(devId=devId):
        errcode = 1
    return errcode