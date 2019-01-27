# -*- coding: utf-8 -*-

from app import utils
from app import db

# 用户管理
# 类名定义 collection
class Formula(db.Document):
    meta = {
        'collection': 'formulacfg',
        'ordering': ['-devId'],
        'strict': False,
    }

    # 字段
    washId = db.IntField()
    formunum = db.IntField()
    devId = db.StringField()
    formulas = db.DictField()


def GetFormulaByDevId(devId, washId):
    return Formula.objects(devId=devId,washId=washId).first()


def UpdateFormula(devId, washId, formutype,step,data):
    print("formutype is ", formutype)
    print("step is ", step)
    print("data is : " ,data)
    errcode = 1
    record = Formula.objects(devId=devId,washId=washId).first()
    if record:
        if (len(data) == 8):
            # it mean update open time
            upLabel = 'open'
        else:  # it mean update vol and prio
            upLabel = 'vol'
            record.formulas[formutype]['step%d'%step]['prio'] = data.pop(8)
        for i in range(len(data)):
            record.formulas[formutype]['step%d'%step]['pump%d'%(i+1)][upLabel] = data[i]        

        record.save()
        errcode = 0
    return errcode


def DeleteFormula(devId):
    errcode = 0
    formula = Formula.objects(devId=devId)
    formula.delete()
    if Formula.objects(devId=devId):
        errcode = 1
    return errcode


