# -*- coding: utf-8 -*-

from app import utils
from app import db

from datetime import datetime


# 用户管理
# 类名定义 collection
class Notify(db.Document):
    meta = {
        'collection': 'notify',
        'strict': False,
    }
    # 字段
    devId = db.StringField()
    pumpcfg = db.StringField()
    valvecfg = db.StringField()
    formulacfg = db.StringField()


def UpdateNotifyByDevId(devid, data):
    errcode = 1
    record = Notify.objects(devId=devid).first()
    if record:
        record.update(**data)
        errcode = 0
    return errcode