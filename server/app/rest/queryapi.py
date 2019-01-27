# -*- coding:utf-8 -*-  
from flask_jwt import jwt_required
from flask import request, Response
from . import rest
from app import utils
from app.model import Device as DeviceModel
from app.model import User as UserModel
from app.model import Report as ReportModel
from app.model import AbstractUser as AUserModel
from pymongo import MongoClient

import logging, datetime
from logging.config import fileConfig
fileConfig('conf/log-app.conf')
logger = logging.getLogger(__name__)



YAOJIMap = {'jian-ye':1, 'zhu-ji':2, 'yang-piao':3, 'lv-piao':4,'rou-ruan-ji':5,'suan-ji':6, 'shui-chu-li':7, 'ru-hua-ji':8}
PRIOMap = {0:u'低',1:u'普通',2:u'高',3:u'紧急'}
caption = [u'起始时间',u'结束时间',u'设备号',u'洗衣机',u'配方',u'步骤',u'优先级',u'药剂1',u'药剂2',u'药剂3',u'药剂4',u'药剂5',u'药剂6',u'药剂7',u'药剂8']
FORMULAMap = {1:u'配方1',2:u'配方2',3:u'配方3',4:u'配方4',5:u'配方5',6:u'配方6',7:u'配方7',8:u'配方8',9:u'配方9',10:u'配方10', \
              11:u'配方11',12:u'配方12',13:u'配方13',14:u'配方14',15:u'配方15',16:u'配方16',17:u'配方17',18:u'配方18',19:u'配方19',20:u'配方20'}


def calcStats(records):
    # if records is None, set all stats value is to 0
    # washList[0]: total, [1]:wash1, [2]:wash2
    stats = dict()
    washList = [0,0,0,0,0,0,0,0,0]
    drugList = [0,0,0,0,0,0,0,0,0]
    formulaList = [0,0,0,0,0,0,0,0,0,0,\
                   0,0,0,0,0,0,0,0,0,0]
    for record in records:
        if record['step'] == '1':
            washList[record['washId']] += 1
            formulaList[record['formula']-1] += 1
        for k,v in record['pumps'].items():
            drugList[YAOJIMap[k]] += v
    drugList.pop(0)

    washList[0] = sum(washList)
    
    #  calc wash
    washDict = dict()
    for i in range(len(washList)):
        washDict['wash%d'%i] = washList[i]
    stats['wash'] = []
    stats['wash'].append(washDict)
    
    # calc drug
    drugDict = dict()
    for i in range(len(drugList)):
        #drugDict['drug%d'%(i+1)] = drugList[i]
        drugDict['drug%d'%(i+1)] = format(float(drugList[i])/float(1000),'.2f')
    drugDict['drugname'] = u'使用剂量'
    stats['drug'] = []
    stats['drug'].append(drugDict)

    #calc formula
    formulaDict = dict()
    for i in range(len(formulaList)):
        formulaDict['fm%d'%(i+1)] = formulaList[i]
    formulaDict['fmname'] = u'洗涤车数'
    stats["formula"] = []
    stats["formula"].append(formulaDict)
    return stats

# it is used to download file
def parseRecord(record):
    rList = [0]*15
    rList[0] = record['startdate'] +' ' + record['starttime']
    rList[1] = record['enddate'] + ' ' + record['endtime']
    rList[2] = str(record['devId'])
    rList[3] = str(record['washId'])
    rList[4] = FORMULAMap[record['formula']]
    rList[5] = record['step']
    rList[6] = PRIOMap[int(record['prio'])]
    rList[7] = str(record['pumps']['jian-ye'])
    rList[8] = str(record['pumps']['zhu-ji'])
    rList[9] = str(record['pumps']['yang-piao'])
    rList[10] = str(record['pumps']['lv-piao'])
    rList[11] = str(record['pumps']['rou-ruan-ji'])
    rList[12] = str(record['pumps']['suan-ji'])
    rList[13] = str(record['pumps']['shui-chu-li'])
    rList[14] = str(record['pumps']['ru-hua-ji'])
    return rList


# get all devices stats
@rest.route('query/allstats/', methods=['GET'])
@jwt_required()
def GetDateStats():
    loginUser = request.args.get('loginUser')
    stime = request.args.get('starttime')
    etime = request.args.get('endtime')
    limit = int(request.args.get('limit'))
    page = int(request.args.get('page'))

    # get all device list under the loginuser
    #  if privilege == 0, get all device, else only get this admin
    total, totalStats = 0, []
    user = AUserModel.IsExist(loginUser)
    if user:
        if user.privilege == '0': # super admin, return all devId
            total, devices = DeviceModel.GetDevices(page, limit)
        elif user.privilege == '5':  # it mean login as devId
            total, devices = [loginUser]
        else:  #  for admin, return all devId which belong to loginUser  
            total, devices = DeviceModel.GetDevices(page, limit, loginUser)         
    print(total)
    #print(devices)
    for dev in devices:
        devId = dev['devId']
        result = ReportModel.GetRecordsByDevIdDate(devId, stime, etime)
        stats = calcStats(result)           
        stats['devId'] = devId
        device = DeviceModel.GetDeviceByDevId(devId)
        stats['position'] = device['position']
        stats['comment2'] = device['comment2']        
        totalStats.append(stats)
    print(totalStats)
    return utils.jsonresp(jsonobj={'total':total, 'limit':limit, 'stats':totalStats})

# get all devices stats
@rest.route('query/devidstats/', methods=['GET'])
@jwt_required()
def GetDevIdStats():
    devId = request.args.get('devId')
    loginUser = request.args.get('loginUser')
    stime = request.args.get('starttime')
    etime = request.args.get('endtime')
    limit = int(request.args.get('limit'))
    page = int(request.args.get('page'))

    # get all device list under the loginuser
    #  if privilege == 0, get all device, else only get this admin
    total, totalStats, devices = 0, [], []
    user = AUserModel.IsExist(loginUser)
    if user:
        if user.privilege == '0': # super admin, return all devId
            total, devices = DeviceModel.GetDevices(page, limit,devId=devId)
        elif user.privilege == '5':  # it mean login as devId
            #total, devices = (1,[loginUser])
            total, devices = DeviceModel.GetDevices(page, limit,devId=loginUser)
        
        else:  #  for admin, return all devId which belong to loginUser  
            total, devices = DeviceModel.GetDevices(page, limit, devId=devId, loginUser=loginUser, privilege=user.privilege)         

    for i in range(len(devices)):
        dev = devices[i]
        devId = dev['devId']
        result = ReportModel.GetRecordsByDevIdDate(devId, stime, etime)
        stats = calcStats(result)           
        stats['devId'] = devId
        stats['devNo'] = (page-1)*limit + (i+1)
        device = DeviceModel.GetDeviceByDevId(devId)
        stats['position'] = device['position']
        stats['comment2'] = device['comment2']        
        totalStats.append(stats)
    print(totalStats)
    return utils.jsonresp(jsonobj={'total':total, 'limit':limit, 'stats':totalStats})




@rest.route('query/download/<filename>', methods=['GET'])
#@jwt_required()
def DownloadFile(filename):
    devid = request.args.get('devId')
    stime = request.args.get('starttime')
    etime = request.args.get('endtime')    

    def generate():
    
        #yield ','.join(caption).encode('GB18030') + '\n'
        #yield ','.join(caption).encode('utf-8') + '\n'
        yield ','.join(caption) + '\n'
        conn = MongoClient('127.0.0.1', 27017)
        # get deviceId
        #devIdList = DbOpt.GetDevidbyUser(user)
        #condition = {"devId":{"$in":devIdList},"startdate":{"$gte":stime, "$lte":etime}}
        condition = {"devId":devid,"startdate":{"$gte":stime, "$lte":etime}}
        #print devIdList
    
        db_heist = conn['heist']
        tb_heist = db_heist['reportdata']
        buf = tb_heist.find(condition) 
        result = []
        for x in buf:
            recd = parseRecord(x)
            #yield ','.join(recd).encode('GB18030') + '\n'
            #yield ','.join(recd).encode('utf-8') + '\n'
            yield ','.join(recd) + '\n'
    

        conn.close()

    #filename = user + '_'+stime + '_' + etime + '.csv'
    return Response(generate(), mimetype='text/csv')



#query/devices
#search devices by user
@rest.route('query/searchdevs', methods=['GET'])
@jwt_required()
def SearchDevIdsByUser():
    loginUser = request.args.get('loginUser')
    devId = request.args.get('devId')

    devIds = []
    errcode = 2 #  2 mean cannot get the loginUser

    if loginUser:
        user = AUserModel.IsExist(loginUser)
        if user:
            devIds = DeviceModel.GetDevIds(user.privilege, loginUser,devid=devId)  
            errcode = 0
        else:
            errcode = 1  # 1 mean the user is not exist        

    return utils.jsonresp(jsonobj={'errcode':errcode, 'devIds':devIds})
