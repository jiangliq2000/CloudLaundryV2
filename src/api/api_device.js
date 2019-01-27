/**
 * Created by liqiang on 2018/06/13.
 * 用户相关api
 */
import * as API from './'

export default {

  //查询获取user列表(通过page分页)
  findList: params => {
    return API.GET('/api/v1/devices', params)
  },


  getDevScatter: params => {
    return API.GET('/api/v1/deviceScatter', params)
  },


  add: params => {
    return API.POST(`/api/v1/devices`, params)
  },
  update: (devId, params) => {
    return API.PUT(`/api/v1/devices/${devId}`, params)
  },

  //单个删除教师
  remove: devID => {
    return API.DELETE(`/api/v1/devices/${devId}`)
  },

  //批量删除，传ids数组
  removeBatch: (devIds) => {
    return API.DELETE(`/api/v1/devices/batch/${devIds}`)
  }
}
