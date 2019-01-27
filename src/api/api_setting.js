/**
 * Created by liqiang on 2018/07/18.
 * 套餐相关api
 */
import * as API from './'

export default {

  //获取设备列表
  GetDevidLists: params => {
    return API.GET('/api/v1/devices/devids', params)
  },


  //查询获取pump 配置
  GetPumpByDevId: devId => {
    return API.GET(`/api/v1/setting/pump/${devId}`)
  },

  UpdatePumpByDevId: (id, params) => {
    return API.PUT(`/api/v1/setting/pump/${id}`, params)
  },


  //查询获取wash 配置
  GetWashByDevId: devId => {
    return API.GET(`/api/v1/setting/wash/${devId}`)
  },

  UpdateWashByDevId: (id, params) => {
    return API.PUT(`/api/v1/setting/wash/${id}`, params)
  },


  //查询获取formula 配置
  GetFormulaByDevId: devId_washNo_formuNo => {
    return API.GET(`/api/v1/setting/formula/${devId_washNo_formuNo}`)
  },

  UpdateFormulaByDevId: (devId_washNo_formuNo, params) => {
    return API.PUT(`/api/v1/setting/formula/${devId_washNo_formuNo}`, params)
  },





  add: params => {
    return API.POST(`/api/v1/courses`, params)
  },
  update: (id, params) => {
    return API.PUT(`/api/v1/courses/${id}`, params)
  },

  //单个删除course
  remove: id => {
    return API.DELETE(`/api/v1/courses/${id}`)
  },

  //批量删除，传ids数组
  removeBatch: (ids) => {
    return API.DELETE(`/api/v1/courses/batch/${ids}`)
  }

}
