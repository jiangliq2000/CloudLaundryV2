import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Dashboard from '@/components/Dashboard'
import Web from '@/components/Web'

import UserList from '@/components/user/userlist'
import UserChangePwd from '@/components/user/changepwd'
import UserProfile from '@/components/user/profile'


import SingleStats from '@/components/query/singleStats'
import DevidList from '@/components/query/deviceList'
import DevicesStats from '@/components/query/devicesStats'

import FormulaCfg from '@/components/setting/formulaCfg'
import PumpCfg from '@/components/setting/pumpCfg'



// 懒加载方式，当路由被访问的时候才加载对应组件
const Login = resolve => require(['@/components/Login'], resolve)
const LoginAgency = resolve => require(['@/components/LoginAgency'], resolve)

Vue.use(Router)

let router = new Router({
// mode: 'history',
  routes: [
    {
      path: '/',
      name: '主页',
      component: Web
    },

    {
      path: '/login',
      name: '登录',
      component: Login
    },

    {
      path: '/loginA',
      name: '登录A',
      component: LoginAgency
    },    
    {
      path: '/auth',
      name: 'home',
      component: Home,
      redirect: '/auth/dashboard',
      leaf: true, // 只有一个节点
      menuShow: true,
      iconCls: 'iconfont icon-home', // 图标样式class
      children: [
        {path: '/auth/dashboard', component: Dashboard, name: '首页', menuShow: true}
      ]
    },
    
    {
      path: '/auth',
      component: Home,
      name: '用户管理',
      menuShow: true,
      leaf: true, // 只有一个节点
      iconCls: 'iconfont icon-users', // 图标样式class
      children: [
        {path: '/auth/user/list', component: UserList, name: '用户列表', menuShow: true}
      ]
    },

    {
      path: '/auth',
      component: Home,
      name: '数据查询',
      menuShow: true,
      //leaf: true, // 只有一个节点
      iconCls: 'iconfont icon-users', // 图标样式class
      children: [
        
        {path: '/auth/data/devidlist', component: DevidList, name: '设备列表', menuShow: true},
        {path: '/auth/data/devicesstats', component: DevicesStats, name: '统计查询', menuShow: true},
        {path: '/auth/data/singlestats', component: SingleStats, name: '单设备统计', menuShow: true}
      ]
    },
    
    {
      path: '/auth',
      component: Home,
      name: '配置管理',
      menuShow: true,
      //leaf: true, // 只有一个节点
      iconCls: 'iconfont icon-users', // 图标样式class
      children: [
		    {path: '/auth/config/pumpcfg', component: PumpCfg, name: '泵阀管理', menuShow: true},
        {path: '/auth/config/formulacfg', component: FormulaCfg, name: '配方管理', menuShow: true}
      ]
    },

    {
      path: '/auth',
      component: Home,
      name: '设置',
      menuShow: true,
      iconCls: 'iconfont icon-setting1',
      children: [
        {path: '/auth/user/profile', component: UserProfile, name: '个人信息', menuShow: true},
        {path: '/auth/user/changepwd', component: UserChangePwd, name: '修改密码', menuShow: true}
      ]
    }
  ]
})

router.beforeEach((to, from, next) => {
  // console.log('to:' + to.path)
  if (to.path.startsWith('/login')) {
    //window.localStorage.removeItem('access-user')
    window.sessionStorage.removeItem('access-user')
    window.sessionStorage.removeItem('token')
    window.sessionStorage.removeItem('role')
    next()
  } else  if (to.path.startsWith('/auth')){
    //let user = JSON.parse(window.localStorage.getItem('access-user'))
    let user = JSON.parse(window.sessionStorage.getItem('access-user'))
    if (!user) {
      next({path: '/login'})
    } else {
      next()
    }
  }else {
      next()
  }

})

export default router
