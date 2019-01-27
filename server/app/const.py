# -*- coding:utf-8 -*-  
__author__ = 'liqiang'

# database name
DATABASE = 'heist'

# table name define
TB_USER = 'user'
TB_DEVIDCOMMS = 'devidcomms'
TB_REPORT = 'reportdata'
TB_SYNCSTATUS = 'syncstatus'
TB_PUMPCFG = 'pumpcfg'
TB_VALVECFG = 'valvecfg'
TB_FORMULACFG = 'formulacfg'
TB_NOTIFY = 'notify'
TB_LOGIN = 'loginRecord'

# all records field define
HEIST = 'heist'
DEVID = 'devId'
HEAD = 'head'
TYPE = 'type'
CFGTYPE = 'cfgtype'
MODEL = 'model'
HWVER = 'hwVer'
FWVER = 'fwVer'
LANG = 'language'
DATE = 'date'
TIME = 'time'
ACTDAY = 'activeday'
STATUS= 'status'
PASSWORD = 'password'
POSITION = 'position'
ADMIN = 'admin'
USER = 'user'
USERNAME = 'username'
NULL = 'null'
COMMENT  = 'comment'
COMMENT2  = 'comment2'
EXPIRY = 'expiry'
WASHID = 'washid'
SEQ = 'seq'
FORMU = 'formula'
STEP = 'step'
PRIO = 'prio'
STARTDATE = 'startdate'
STARTTIME = 'starttime'
ENDDATE = 'enddate'
ENDTIME = 'endtime'
PUMPNUM = 'pumpnum'
VOL = 'vol'
PUMPTYPEDICT = {0:'jian-ye', 1:'zhu-ji', 2:'yang-piao',3:'lv-piao',4:'rou-ruan-ji',5:'suan-ji',6:'shui-chu-li',7:'ru-hua-ji'}
PUMPS = 'pumps'
SPEED = 'speed'
WASHNUM = 'washnum'
WASHS = 'washs'
FORMUNUM = 'formunum'
FORMULAS = 'formulas'


# all kinds of length define
PUMP_LEN = 3
PUMPCFG_LEN = 3
VALVE_LEN = 6
# formula lenght
# type(1) + 4xstep(prio(1) + 8xpump(5)) = 1 + 4x(1+8x5) = 165
FORMULA_LEN = 165
FORMULA_PUMP_LEN = 5
FORMULA_STEP_LEN = 41
FORMULA_STEP_NUM = 4
FORMULA_STEPPUMP_NUM = 8

