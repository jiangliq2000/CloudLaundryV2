from flask_jwt import jwt_required
from flask import request
from . import rest
from app import utils
from app.model import Device as DeviceModel
from app.model import User as UserModel
from app.model import AbstractUser as AUserModel
import logging, datetime
from logging.config import fileConfig
fileConfig('conf/log-app.conf')
logger = logging.getLogger(__name__)



#query all devices
@rest.route('devices/', methods=['GET'])
@jwt_required()
def get_devices():
    limit = int(request.args.get('limit'))
    page = int(request.args.get('page'))
    # there name it mean devid, maybe part name of devId
    name = request.args.get('name')
    address = request.args.get('address')
    admin =request.args.get('admin')
    # 
    total, devices = 0, "null"
    loginUser = request.args.get('loginUser')
    ## here, need verify if loginUser has privilege to get user list
    if loginUser:
        user = AUserModel.IsExist(loginUser)
        logging.info("-- get_device---- loginuser privilege ：", user.privilege)
        if user:
            if user.privilege == '0': # super admin, return all devices
                total, devices = DeviceModel.GetDevices(page, limit, devId=name, addr=address,admin=admin)
            elif user.privilege == '5': # it mean login as devId, so devId = loginUser
                total, devices = DeviceModel.GetDevices(page, limit, devId=loginUser, addr=address)
            else:  #  for admin, return all devices which belong to loginUser  
                total, devices = DeviceModel.GetDevices(page, limit, devId=name, addr=address, loginUser=loginUser, privilege=user.privilege)           

    return utils.jsonresp(jsonobj={'total':total, 'limit':limit, 'devices':devices})



#query device scatter data
@rest.route('deviceScatter/', methods=['GET'])
@jwt_required()
def get_devScatter():
    total, devices = 0, "null"
    loginUser = request.args.get('loginUser')
    ## here, need verify if loginUser has privilege to get user list
    if loginUser:
        user = AUserModel.IsExist(loginUser)
        logging.info("-- get_device---- loginuser privilege ：", user.privilege)
        if user:
            if user.privilege == '0': # super admin, return all devices
                total, addrs = DeviceModel.GetDevScatter(privilege='0')
            elif user.privilege == '5': # it mean login as devId, so devId = loginUser
                total, addrs = DeviceModel.GetDevScatter(devId=loginUser)
            else:  #  for admin, return all devices which belong to loginUser  
                total, addrs = DeviceModel.GetDevScatter(loginUser=loginUser, privilege=user.privilege)           
        if total>0:
            # handle address, split address
            devCount = {}
            for addr in set(addrs):
                devCount[addr] = addrs.count(addr)

            dataScatter =[]
            for k,v in devCount.items():
                dataScatter.append({"name":k, "value":v})

    return utils.jsonresp(jsonobj={'total':total, 'dataScatter':dataScatter})



# update one device
@rest.route('devices/<devid>', methods=['PUT'])
#@jwt_required()
def update_device(devid):
    data = request.get_json(force=True) 
    print(data)
    print(type(data))
    errcode = DeviceModel.UpdateDevice(devid, **data)
    return utils.jsonresp(jsonobj={'errcode':errcode})

# delete one device
@rest.route('devices/<devId>', methods=['DELETE'])
#@jwt_required()
def delete_device(devId):
    errcode = DeviceModel.DeleteDevice(devId)
    return utils.jsonresp(jsonobj={'errcode':errcode})

# patch del devices
@rest.route('devices/batch/<devices>', methods=['DELETE'])
#@jwt_required()
def delete_devices(devices):
    errcode = 0
    #nameList = names.split(',')
    for devId in devices.split(','):
        ret = DeviceModel.DeleteDevice(devId)
        if ret != 0:
            errcode = 1

    return utils.jsonresp(jsonobj={'errcode':errcode})


#query all devices by user
@rest.route('devices/devids', methods=['GET'])
@jwt_required()
def GetDevIdByUser():
    loginUser = request.args.get('loginUser')
    devIds = []
    errcode = 2 #  2 mean cannot get the loginUser

    if loginUser:
        user = AUserModel.IsExist(loginUser)
        if user:
            devIds = DeviceModel.GetDevIds(user.privilege, loginUser)   
            errcode = 0
        else:
            errcode = 1  # 1 mean the user is not exist        

    return utils.jsonresp(jsonobj={'errcode':errcode, 'devIds':devIds})
