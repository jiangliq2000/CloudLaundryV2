/**
 * Created by liqiang on 2018/07/18.
 * 套餐相关api
 */
import * as API from './'

export default {

  //查询获取套餐列表(通过page分页)
  GetAllStats: params => {
    return API.GET('/api/v1/query/allstats', params)
  },

  GetDevidStats: params => {
    return API.GET('/api/v1/query/devidstats', params)
  },


  reqDownloadStats: params => {
    return window.open('api/v1/query/download/'+ params.filename + params.condition)
  },
  

  SearchDevids: params => {
    return API.GET('/api/v1/query/searchdevs', params)
  },


  updateDevid: (devid, params) => {
    return API.PUT(`/api/v1/query/device/${devid}`, params)
  },


  DeleteDevid: id => {
    return API.DELETE(`/api/v1/query/device/${devid}`)
  }

}
