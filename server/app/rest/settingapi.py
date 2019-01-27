from flask_jwt import jwt_required
from flask import request
from . import rest
from app import utils
from app.model import Device as DeviceModel
from app.model import User as UserModel
from app.model import Pump as PumpModel
from app.model import Wash as WashModel
from app.model import Formula as FormulaModel
from app.model import Notify as NotifyModel
from app.const import *
import logging, datetime
from logging.config import fileConfig
fileConfig('conf/log-app.conf')
logger = logging.getLogger(__name__)



#query all devices
@rest.route('setting/pump/<devId>', methods=['GET'])
@jwt_required()
def get_pump(devId):
    record = PumpModel.GetPumpByDevId(devId)
    pumpcfgs = []
    if record:        
        pumps = record.pumps
        for i in range(1,record.pumpnum+1):
            pumpcfgs.append(pumps['pump%d'%i]['speed'])

    return utils.jsonresp(jsonobj={'pumpcfgs':pumpcfgs})

# update one pumpcfg
@rest.route('setting/pump/<devid>', methods=['PUT'])
#@jwt_required()
def update_pump(devid):
    data = request.get_json(force=True) 
    print(data)
    print(type(data))
    errcode = PumpModel.UpdatePumpByDevId(devid, data['pumps'])
    if errcode == 0:
        NotifyModel.UpdateNotifyByDevId(devid, {'pumpcfg':'true'})

     # it mean update successfully, need update notify table

    return utils.jsonresp(jsonobj={'errcode':errcode})

"""
# delete one pump
@rest.route('setting/pump/<devId>', methods=['DELETE'])
#@jwt_required()
def delete_pump(devId):
    errcode = PumpModel.DeletePumpByDevId(devId)
    return utils.jsonresp(jsonobj={'errcode':errcode})
"""


@rest.route('setting/wash/<devId>', methods=['GET'])
@jwt_required()
def get_wash(devId):
    record = WashModel.GetWashByDevId(devId)
    washcfgs = []
    if record:        
        washs = record.washs
        for i in range(1,record.washnum+1):
            wash = dict()
            wash['ins'] = washs['wash%d'%i]['inopen']
            wash['inc'] = washs['wash%d'%i]['inclose']
            wash['outs'] = washs['wash%d'%i]['outopen']
            wash['outc'] = washs['wash%d'%i]['outclose']
            washcfgs.append(wash)

    return utils.jsonresp(jsonobj={'washcfgs':washcfgs})

# update one washcfg
@rest.route('setting/wash/<devid>', methods=['PUT'])
#@jwt_required()
def update_wash(devid):
    data = request.get_json(force=True) 
    #record = WashModel.GetWashByDevId(devId)
    errcode = WashModel.UpdateWashByDevId(devid, data['wash'], data['washIndex'])
    if errcode == 0:
        NotifyModel.UpdateNotifyByDevId(devid, {'valvecfg':'true'})
    return utils.jsonresp(jsonobj={'errcode':errcode})



@rest.route('setting/formula/<devId_washNo_formuNo>', methods=['GET'])
@jwt_required()
def get_formula(devId_washNo_formuNo):
    devId, washId, formuNo = devId_washNo_formuNo.split('_')
    washId = int(washId)
    formutype = 'formu' + formuNo
    record = FormulaModel.GetFormulaByDevId(devId, washId)
    formulacfg = []
    if record:        
        formula = record.formulas[formutype]
        for i in range(1,FORMULA_STEP_NUM+1):
            print(formula['step%d'%i])
            step = formula['step%d'%i]
            startDict = dict()
            volDict = dict()
            for i in range(1,FORMULA_STEPPUMP_NUM+1):
                volDict['p%d'%i] = step['pump%d'%i]['vol']
                startDict['p%d'%i] = step['pump%d'%i]['open']
            startDict['prio'] =''
            volDict['prio'] = step['prio']
            formulacfg.append(startDict)
            formulacfg.append(volDict)

    return utils.jsonresp(jsonobj={'formulacfg':formulacfg})

# update one washcfg
@rest.route('setting/formula/<devId_washNo_formuNo>', methods=['PUT'])
#@jwt_required()
def update_formula(devId_washNo_formuNo):
    devId, washId, formuNo = devId_washNo_formuNo.split('_')
    washId = int(washId)
    formutype = 'formu' + formuNo
    data = request.get_json(force=True) 

    errcode = FormulaModel.UpdateFormula(devId,washId,formutype,data['stepindex'], data['stepdata'])
    if errcode == 0:
        NotifyModel.UpdateNotifyByDevId(devId, {'formulacfg':'true'})
    return utils.jsonresp(jsonobj={'errcode':errcode})




"""
@rest.route('setting/wash/<devId>', methods=['DELETE'])
#@jwt_required()
def delete_wash(devId):
    errcode = WashModel.DeleteWashByDevId(devId)
    return utils.jsonresp(jsonobj={'errcode':errcode})
"""
