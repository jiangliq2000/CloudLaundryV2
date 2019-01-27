# -*- coding: utf-8 -*-

from app import utils
from app import db
#from model.device import Device1


from playhouse.shortcuts import model_to_dict, dict_to_model

from datetime import datetime


# 用户管理
# 类名定义 collection
class User(db.Document):
    meta = {
        'collection': 'user_v2',
        'ordering': ['-create_at'],
        'strict': False,
    }

    # 字段
    username = db.StringField(required=True)
    devId = db.StringField()
    name = db.StringField()
    register = db.StringField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    contact = db.StringField()
    password = db.StringField()
    #isAdmin = db.BooleanField(default=False)
    blgAdmin = db.StringField()
    privilege = db.StringField()  # 0-super, 1-admin, 2-user(rw), 3-user(only read)
    lastloginip = db.StringField()
    lastlogintime = db.DateTimeField()

    def __str__(self):
        return "name:{} - username:{}".format(self.name, self.username)



def GetPayloadByUsername(username):
    #return Administrator.get_or_none(Administrator.username == username, Administrator.status == STATUS_VALID)
    return User.objects(username=username).only('username','password','privilege').first()
    """
    user = User.objects(username=username).first()
    if user:
        return {'id':user.username,'username':user.username, 'password':user.password, 'privilege':user.privilege}
    else:
        None
    """

def IsExist(username):
    return User.objects(username=username).first()

def GetPrivilege(username):
    user = User.objects(username=username).first()
    return user.privilege


def GetBlgAdmins():
    blgAdmins = []
    for user in User.objects(privilege='1').only('username').all():
        blgAdmins.append({'value':user.username, 'label':user.username})
    return blgAdmins


def GetBlgQMUsers(privilege,loginUser):
    blgQMUsers = []
    cnd = {'privilege':'2'}
    if privilege == '1':
        cnd['blgAdmin']=loginUser
    for user in User.objects(**cnd).only('username').all():
        blgQMUsers.append({'value':user.username, 'label':user.username})
    return blgQMUsers


def GetBlgQUsers(privilege,loginUser):
    blgQUsers = []
    cnd = {'privilege':'3'}
    if privilege == '1':
        cnd['blgAdmin'] = loginUser
    for user in User.objects(**cnd).only('username').all():
        blgQUsers.append({'value':user.username, 'label':user.username})
    return blgQUsers


def SearchUserByName(page_num, item_per_page,name, loginUser=None):
    condition = {'name__icontains':name}
    if loginUser:
        condition['blgAdmin'] = loginUser
    count = User.objects(**condition).count()
    users = []
    for user in User.objects(**condition).paginate(page=page_num, per_page=item_per_page).items:
        users.append({'username':user.username, 'name':user.name,'password':user.password,'register':user.register,\
                      'devId':user.devId,'lastloginip':user.lastloginip, 'lastlogintime':user.lastlogintime,\
                       'privilege':user.privilege,'contact':user.contact})

    return count, users


def GetUsers(page_num, item_per_page, loginUser=None):
    users = []
    if loginUser:
        count = User.objects(blgAdmin=loginUser).count()
        for user in User.objects(blgAdmin=loginUser).paginate(page=page_num, per_page=item_per_page).items:
            users.append({'username':user.username, 'name':user.name,'password':user.password, 'register':user.register,\
                          'devId':user.devId,'lastloginip':user.lastloginip, 'lastlogintime':user.lastlogintime,\
                           'privilege':user.privilege,'contact':user.contact})
    else:
        count = User.objects.count()
        for user in User.objects.paginate(page=page_num, per_page=item_per_page).items:
            users.append({'username':user.username, 'name':user.name,'password':user.password,\
                          'devId':user.devId,'lastloginip':user.lastloginip, 'lastlogintime':user.lastlogintime,\
                           'privilege':user.privilege,'contact':user.contact})

    return count, users

def CreateUser(**data):
    errcode = 1
    username = data.get('username',None)
    if username:
        User(**data).save()
        if User.objects(username=username):
            errcode = 0
    
    return errcode


def UpdateUser(userid, **data):
    errcode = 1
    user = User.objects(username=userid)
    print('updateuser')
    print(data)
    if user:
        user.update(**data)
        errcode = 0
    return errcode


def DeleteUser(username):
    errcode = 0
    user = User.objects(username=username)
    user.delete()
    if User.objects(username=username):
        errcode = 1
    return errcode