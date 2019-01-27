# CloudLaundryV2

基本功能：
1.前端采用vue.js 和 element-ui 开发用户界面，提供配置修改和数据查询
2.后端使用python flask 框架提供http api接口，接受前端的配置修改和参数查询。
3.服务器上还有一个接受远程数据的接受进程，负责远程数据的存储和配置下发。
4.采用mongodb作为存储数据。crontab实现每隔1个月进行数据自动备份。
