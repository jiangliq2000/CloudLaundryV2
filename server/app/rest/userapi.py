from flask_jwt import jwt_required
from flask import request
from . import rest
from app import utils
from app.model import User as UserModel
from app.model import AbstractUser as AUserModel
import logging, datetime
#from logging.config import fileConfig
#fileConfig('conf/log-app.conf')
#logger = logging.getLogger(__name__)


#query all users
@rest.route('users/privilege/<loginUser>', methods=['GET'])
@jwt_required()
def get_privilege(loginUser):
    #  default is lowest privilege
    privilege = 3
    errcode = 1
    ## here, need verify if loginUser has privilege to get user list
    user = AUserModel.IsExist(loginUser)
    logging.debug("user is %s"%user)
    if user:
        privilege =user.privilege
        errcode = 0
    return utils.jsonresp(jsonobj={'errcode':errcode,'privilege':privilege})

@rest.route('users/blgadmin/<loginUser>', methods=['GET'])
@jwt_required()
def get_blgAdmins(loginUser):
    errcode = 1
    blgAdmins = []
    user = UserModel.IsExist(loginUser)
    if user:
        if user.privilege == '0':    # only super admin can return all admin users
            blgAdmins = UserModel.GetBlgAdmins()
            errcode = 0
    return utils.jsonresp(jsonobj={'errcode':errcode,'blgAdmins':blgAdmins})

@rest.route('users/blgqmuser/<loginUser>', methods=['GET'])
@jwt_required()
def get_blgQMUsers(loginUser):
    errcode = 1
    blgQMUsers = []
    user = UserModel.IsExist(loginUser)
    if user:
        blgQMUsers = UserModel.GetBlgQMUsers(user.privilege, loginUser)
        errcode = 0

    return utils.jsonresp(jsonobj={'errcode':errcode,'blgQMUsers':blgQMUsers})


@rest.route('users/blgquser/<loginUser>', methods=['GET'])
@jwt_required()
def get_blgQUsers(loginUser):
    errcode = 1
    blgQUsers = []
    user = UserModel.IsExist(loginUser)
    if user:
        blgQUsers = UserModel.GetBlgQUsers(user.privilege, loginUser)
        errcode = 0

    return utils.jsonresp(jsonobj={'errcode':errcode,'blgQUsers':blgQUsers})



#query all users
@rest.route('users/', methods=['GET'])
@jwt_required()
def get_users():
    limit = int(request.args.get('limit'))
    page = int(request.args.get('page'))
    # this name allow none, if no value, it mean query all user list under this amdin
    name = request.args.get('name')
    # 
    total, users = 0, "null"
    loginUser = request.args.get('loginUser')
    ## here, need verify if loginUser has privilege to get user list
    if loginUser:
        user = UserModel.IsExist(loginUser)
        if user:
            if user.privilege == '0': # super admin
                if name:
                    total, users = UserModel.SearchUserByName(page, limit, name)
                else:
                    total, users = UserModel.GetUsers(page, limit)
            
            if user.privilege == '1':  #  admin        
                if name:
                    total, users = UserModel.SearchUserByName(page, limit, name, loginUser)
                else:
                    total, users = UserModel.GetUsers(page, limit, loginUser)                   
  


    return utils.jsonresp(jsonobj={'total':total, 'limit':limit, 'users':users})



# create one user
@rest.route('users/', methods=['POST'])
#@jwt_required()
def create_user():
    data = request.get_json('content')
    print(type(data))
    print(data)
    # need check if username already exist
    username = data.get('username')
    if username:
        user = UserModel.IsExist(username)
        if user:
            errcode = 2  #  2 mean username already exist
        else:
            errcode = UserModel.CreateUser(**data)
    else:
        errcode = 1

    return utils.jsonresp(jsonobj={'errcode':errcode})

# update one user
@rest.route('users/<userid>', methods=['PUT'])
#@jwt_required()
def update_user(userid):
    data = request.get_json(force=True) 
    print(data)
    print(type(data))
    errcode = UserModel.UpdateUser(userid, **data)
    return utils.jsonresp(jsonobj={'errcode':errcode})

# delete one user
@rest.route('users/<username>', methods=['DELETE'])
#@jwt_required()
def delete_user(username):
    errcode = UserModel.DeleteUser(username)
    return utils.jsonresp(jsonobj={'errcode':errcode})

# patch del users
@rest.route('users/batch/<usernames>', methods=['DELETE'])
#@jwt_required()
def delete_users(usernames):
    errcode = 0
    #nameList = names.split(',')
    for username in usernames.split(','):
        ret = UserModel.DeleteUser(username)
        if ret != 0:
            errcode = 1

    return utils.jsonresp(jsonobj={'errcode':errcode})


# change password
@rest.route('users/password/<username>', methods=['PUT'])
#@jwt_required()
def change_password(username):
    data = request.get_json(force=True) 
    oldpwd = data.get('oldpwd')
    newpwd = data.get('newpwd')
    errcode = 1
    # check if username is exist
    #
    # check privi
    errcode = AUserModel.ChangePwd(username, oldpwd, newpwd )
    #errcode = UserModel.UpdateUser(userid, **data)
    return utils.jsonresp(jsonobj={'errcode':errcode})
