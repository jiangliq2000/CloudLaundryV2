/**
 * Created by liqiang on 2018/06/13.
 * 用户相关api
 */
import * as API from './'

export default {
  //登录
  login: params => {
    return API.POST('/api/v1/users/login', params)
  },

  //登录
  getPrivilege: username => {
    return API.GET(`/api/v1/users/privilege/${username}`)
  },

  GetBlgAdmins: username => {
    return API.GET(`/api/v1/users/blgadmin/${username}`)
  },

  GetBlgQMUsers: username => {
    return API.GET(`/api/v1/users/blgqmuser/${username}`)
  },
  GetBlgQUsers: username => {
    return API.GET(`/api/v1/users/blgquser/${username}`)
  },


  //登出
  logout: params => {
    return API.GET('/api/v1/users/logout', params)
    // because used token to access, for logout, don't need notify server side
  },
  //修改个人信息
  changeProfile: params => {
    return API.PATCH('/api/v1/users/profile', params)
  },

    //修改密码
  changePassword: (username, params) => {
    return API.PUT(`/api/v1/users/password/${username}`, params)
  },


  //查询获取user列表(通过page分页)
  findList: params => {
    return API.GET('/api/v1/users', params)
  },

  add: params => {
    return API.POST(`/api/v1/users`, params)
  },
  update: (username, params) => {
    return API.PUT(`/api/v1/users/${username}`, params)
  },

  //单个删除教师
  remove: username => {
    return API.DELETE(`/api/v1/users/${username}`)
  },

  //批量删除，传ids数组
  removeBatch: (usernames) => {
    return API.DELETE(`/api/v1/users/batch/${usernames}`)
  }
}
