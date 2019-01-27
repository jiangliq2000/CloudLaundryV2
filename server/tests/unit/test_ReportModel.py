# -*- coding: utf-8 -*-
from datetime import datetime
from mongoengine import *


connect('heist')


# 用户管理
class Report(Document):
    meta = {
        'collection': 'reportdata',
        'ordering': ['-create_at'],
        'strict': False,
    }

    # 字段
    washId = StringField()
    startdate = StringField()
    enddate = StringField()
    seq = StringField()
    prio = StringField()
    devId = StringField()

    step = StringField()
    starttime = StringField()
    endtime = StringField()
    pumpnum = IntField()
    formula = IntField()
    pumps = DictField()


def test_gte_startdate():
    std = ''
    end = ''
    devId = '77db5e96'
    count = Report.objects(devId=devId,startdate__gte='2018-08-01',enddate__lte='2018-08-30').count()
    count1 = Report.objects(devId=devId,startdate__gte='2018-08-31',enddate__lte='2018-08-03').count()
    count2 = Report.objects(devId=devId,startdate__gte=std,enddate__lte=end).count()
    count3 = Report.objects(devId=devId,startdate__gte=std,enddate__lte='2018-08-30').count()
    print(count, count1, count2, count3)




if __name__ == '__main__':
    test_gte_startdate()