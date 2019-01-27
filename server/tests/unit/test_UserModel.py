# -*- coding: utf-8 -*-
from datetime import datetime
from mongoengine import *


connect('heist')


# 用户管理
# 类名定义 collection
class User(Document):
    meta = {
        'collection': 'user_v2',
        'ordering': ['-create_at'],
        'strict': False,
    }

    # 字段
    username = StringField(required=True)
    devId = StringField()
    name = StringField()
    register = StringField()
    contact = StringField()
    password = StringField()
    isAdmin = BooleanField(default=False)
    belongAdmin = StringField()
    privilege = StringField()
    createtime = DateTimeField()
    lastloginip = StringField()
    lastlogintime = DateTimeField(default=datetime.now)

    def __str__(self):
        return "name:{} - username:{}".format(self.name, self.username)



def GetRecordByUsername(username):
    #return Administrator.get_or_none(Administrator.username == username, Administrator.status == STATUS_VALID)
    return User.objects(username=username).only('username','password','privilege').first()
    

def IsExist(username):
    return User.objects(username=username).first()

def GetPrivilege(username):
    user = User.objects(username=username).first()
    return user.privilege


def test_get_existuser():
    """
    GIVEN a User model
    WHEN query a exit user
    THEN check username, password, privilege
    """
    username='heist'
    dataDict = {'username':'heist', 'password':'111', 'privilege':1}

    user = GetRecordByUsername(username=username)
    print(user.username, user.password)
    print(user.privilege)
    #assert new_studguard.member_id == 22
    #assert new_studguard.relationship == 3
    #

def test_contains_query(name):
    users = User.objects(name__icontains=name)
    if users:
        for user in users:
            print(user)


def test_get_notexistuser():
    """
    GIVEN a User model
    WHEN query a exit user
    THEN check username, password, privilege
    """
    username='1111'
    dataDict = {'username':'heist', 'password':'111', 'privilege':1}

    user = GetRecordByUsername(username=username)
    print(user)
    #assert new_studguard.member_id == 22

def test_queryCondition():
    cnd = {}
    count = User.objects(cnd).count()
    count1 = User.objects().count()
    print(count, count1)



if __name__ == '__main__':
    test_get_existuser()
    test_get_notexistuser()
    name = u'潘'
    #test_contains_query(name)
    test_queryCondition()