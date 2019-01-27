# -*- coding: utf-8 -*-

import DeviceModel
import UserModel


#  写这个脚本的目的，是之前三星权限的用户改成了五星用户
# 1. 查询设备列表获取目前三星用户名，
# 2  查询这个三星用户名 目前在 用户列表的权限
# 3  如果是修改成五星用户了，则修改设备列表中的五星用户，三星用户修改为空
# 4  如果是修改成VIP用户，则修改设备列表中的VIP用户，三星用户为空


for dev in DeviceModel.Device.objects.all():
	username = dev.blgQUser

	if dev.blgQUser:
		print("----- current device(%s) ----------" %dev.devId)
		print(dev.blgAdmin, dev.blgQMUser, dev.blgQUser)
		privilege = UserModel.GetPrivilege(dev.blgQUser)
		print("username is %s, privilege is %s" %(username, privilege))
		if privilege == "2":
			dev.blgAdmin = ""
			dev.blgQMUser = username
			dev.blgQUser = ""
			cnd = {'blgAdmin':"", 'blgQMUser':username, 'blgQUser':""}

		elif privilege == "1":
			dev.blgAdmin = username
			dev.blgQMUser = ""
			dev.blgQUser = ""	
			cnd = {'blgAdmin':username, 'blgQMUser':"", 'blgQUser':""}

		print("admin=%s,  5start=%s, 3start=%s" %(dev.blgAdmin, dev.blgQMUser, dev.blgQUser))

		dev.update(**cnd)		
