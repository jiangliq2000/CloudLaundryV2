<template>
  <el-row class="warp">
    <el-col :span="24" class="warp-breadcrum">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }"><b>首页</b></el-breadcrumb-item>
        <el-breadcrumb-item>设备列表</el-breadcrumb-item>
      </el-breadcrumb>
    </el-col>
    <el-col :span="24" class="warp-main" v-loading="loading" element-loading-text="拼命加载中">
      <!--工具条-->
      <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
        <el-form :inline="true" :model="filters">
          <el-form-item>
            <el-input v-model="filters.name" placeholder="设备号查询" @keyup.enter.native="handleSearch"></el-input>
          </el-form-item>
          <el-form-item>
            <el-input v-model="filters.address" placeholder="地址查询" @keyup.enter.native="handleSearch"></el-input>
          </el-form-item>		  
          <el-form-item>
            <el-input v-model="filters.admin" placeholder="VIP用户查询" v-if="role === '0'"  @keyup.enter.native="adminSearch"></el-input>
          </el-form-item>		  
          <el-form-item>
            <el-button type="primary" v-on:click="handleSearch">查询</el-button>
          </el-form-item>
        </el-form>
      </el-col>

      <!--列表-->
      <el-table :data="devices" highlight-current-row @selection-change="selsChange"
                style="width: 100%;">
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column type="index" width="60"></el-table-column>

        <el-table-column type="expand" >
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
                <el-form-item label="备注">
                  <span>{{ props.row.comment}}</span>
                </el-form-item>   
                <el-form-item label="登录密码">
                  <span>{{ props.row.password}}</span>
                </el-form-item>  
                <el-form-item label="设备密码">
                  <span>{{ props.row.devPwd}}</span>
                </el-form-item>                                      
				        <el-form-item label="有效期">
                    <span>{{ props.row.expiry}}</span>
                </el-form-item>   
				        <el-form-item label="位置">
                    <span>{{ props.row.position}}</span>
                </el-form-item>   
            </el-form>
          </template>
        </el-table-column>   
        <el-table-column prop="devId" label="设备号" sortable></el-table-column>
        <!--
        <el-table-column prop="password" label="登录密码" sortable></el-table-column>
        <el-table-column prop="devPwd" label="设备密码" sortable></el-table-column>
        <el-table-column prop="comment" label="备注" sortable></el-table-column>
        -->
        
        <el-table-column prop="blgAdmin" label="VIP化料公司" sortable></el-table-column>   
	  	<el-table-column prop="blgQMUser" label="五星用户" sortable></el-table-column>   
	  	<el-table-column prop="blgQUser" label="三星用户" sortable></el-table-column> 
      <el-table-column prop="comment2" label="地址" width="300"></el-table-column>  
       
        <el-table-column label="编辑">
          <template slot-scope="scope">
            <el-button type="warning" @click="showEditDialog(scope.$index,scope.row)" size="small">编辑</el-button>
          </template>
        </el-table-column>
        <el-table-column label="删除">
          <template slot-scope="scope">
            <el-button type="danger" @click="delDevice(scope.$index,scope.row)" v-if="role === '0'"  size="small">删除</el-button>
          </template>
        </el-table-column>		
      </el-table>

      <!--工具条-->
      <el-col :span="24" class="toolbar">
        <el-button type="danger" @click="batchDeleteUser" v-if="role === '0'"  :disabled="this.sels.length===0">批量删除</el-button>
        <el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="10" :total="total"
                       style="float:right;">
        </el-pagination>
      </el-col>

      <el-dialog title="编辑" :visible.sync ="editFormVisible" :close-on-click-modal="false">
        <el-form :model="editForm" label-width="100px" ref="editForm">
          <el-form-item label="设备号" prop="devId" >
            <el-input v-model="editForm.devId" auto-complete="off" :disabled="true"></el-input>
          </el-form-item>	
          <el-form-item label="登录密码" prop="password" >
            <el-input v-model="editForm.password" auto-complete="off"></el-input>
          </el-form-item>  
          <el-form-item label="备注" prop="comment" >
            <el-input v-model="editForm.comment" auto-complete="off" ></el-input>
          </el-form-item>
          <el-form-item label="VIP化料公司" prop="blgAdmin" auto-complete="off" >
			<el-select v-model="editForm.blgAdmin" placeholder="请选择管理员" >
               <el-option v-for="uname in blgAdmins" :label="uname.label" :value="uname.value" ></el-option>
            </el-select>
          </el-form-item> 		  
          <el-form-item label="五星用户" prop="blgQMUser" auto-complete="off" >
			<el-select v-model="editForm.blgQMUser" placeholder="请选用户名" >
               <el-option v-for="uname in blgQMUsers" :label="uname.label" :value="uname.value" ></el-option>
            </el-select>		
			
          </el-form-item> 			  
          <el-form-item label="三星用户" prop="blgQUser" auto-complete="off" >
			<el-select v-model="editForm.blgQUser" placeholder="请选用户名" >
               <el-option v-for="uname in blgQUsers" :label="uname.label" :value="uname.value" ></el-option>
            </el-select>		
          </el-form-item> 				  
          <el-form-item label="有效期" prop="expiry" auto-complete="off" >
            <el-input v-model="editForm.expiry" auto-complete="off"></el-input>
          </el-form-item> 		  
          <el-form-item label="地址" prop="comment2" auto-complete="off" >
            <el-input v-model="editForm.comment2" auto-complete="off"></el-input>
          </el-form-item>
        </el-form>        
		<div slot="footer" class="dialog-footer">
          <el-button @click.native="editFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="editSubmit">提交</el-button>
        </div>
      </el-dialog>
    </el-col>
  </el-row>
</template>

<style>
  .demo-table-expand {
    font-size: 0;
  }
  .demo-table-expand label {
    width: 90px;
    color: #99a9bf;
  }
  .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 50%;
  }
</style>

<script>
  import API from '../../api/api_device';
  import APIUSER from '../../api/api_user';
  
  export default{
    data(){
      return {
        filters: {
          devId: '',
          admin: ''
        },
        devices: [],
        total: 0,
        page: 1,
        limit: 10,
        loading: false,
        role: '3',
        sels: [], //列表选中列
		blgAdmins: '',
		blgQMUsers: '',
		blgQUsers: '',

        //编辑相关数据
        editFormVisible: false,//编辑界面是否显示
        editForm: {
          devId: '',
          password: '',
          devPwd:'',
          comment: '',
          blgAdmin: '',
          blgQMUser: '',
          blgQUser: '',
          expiry: '',
          comment2: ''
        }
      }
    },
    methods: {
    
      handleCurrentChange(val) {
        this.page = val;
        console.log("val is: ");
        console.log(val)
        this.search();
      },
	  
      handleSearch(){
        this.total = 0;
        this.page = 1;
        this.search();
      },
      search(){
        let that = this;
		    let loginUser = JSON.parse(window.sessionStorage.getItem('access-user'));
		    console.log(loginUser);
        let params = {
          page: that.page,
          limit: 10,
          name: that.filters.name,
		  address: that.filters.address,
		  admin: that.filters.admin,
          loginUser: loginUser
        };

        that.loading = true;
        API.findList(params).then(function (result) {
          that.loading = false;
          if (result) {
            if (result.total > 0) {
               that.total = result.total;
               that.devices = result.devices;              
            } else{
               that.$message.error({showClose: true, message: '查询不到设备信息', duration: 5000});
            }
          }

        }, function (err) {
          that.loading = false;
          that.$message.error({showClose: true, message: err.toString(), duration: 2000});
        }).catch(function (error) {
          that.loading = false;
          console.log(error);
          that.$message.error({showClose: true, message: '请求出现异常', duration: 2000});
        });
      },
      selsChange: function (sels) {
        this.sels = sels;
      },
      //删除
      delDevice: function (index, row) {
        let that = this;
        this.$confirm('确认删除该记录吗?', '提示', {type: 'warning'}).then(() => {
          that.loading = true;
          API.remove(row.devId).then(function (result) {
            that.loading = false;
            console.log('result is ');
            console.log(result);
            if (result && parseInt(result.errcode) === 0) {
              that.$message.success({showClose: true, message: '删除成功', duration: 2000});
            } else{
              that.$message.success({showClose: true, message: '删除失败，请重试', duration: 2000});
            }
            that.filters.name = '';
            that.filters.admin = '';
            that.search();       
          }, function (err) {
            that.loading = false;
            that.$message.error({showClose: true, message: err.toString(), duration: 2000});
          }).catch(function (error) {
            that.loading = false;
            console.log(error);
            that.$message.error({showClose: true, message: '请求出现异常', duration: 2000});
          });
        }).catch(() => {
        });
      },
      //显示编辑界面
      showEditDialog: function (index, row) {
	      let that = this;
        this.editFormVisible = true;
        this.editForm = Object.assign({}, row);
		    // get blgAdmins, blgQMUsers, blgQUsers
		    this.getBlgUers();
      },
      //编辑
      editSubmit: function () {
        let that = this;
        this.$refs.editForm.validate((valid) => {
          if (valid) {
            this.loading = true;
            let para = Object.assign({}, this.editForm);

            API.update(para.devId, para).then(function (result) {
              that.loading = false;
              if (result && parseInt(result.errcode) === 0) {
                that.$message.success({showClose: true, message: '修改成功', duration: 4000});
                that.$refs['editForm'].resetFields();
                that.editFormVisible = false;
                that.search();
              } else {
                that.$message.error({showClose: true, message: '修改失败', duration: 2000});
              }
            }, function (err) {
              that.loading = false;
              that.$message.error({showClose: true, message: err.toString(), duration: 2000});
            }).catch(function (error) {
              that.loading = false;
              console.log(error);
              that.$message.error({showClose: true, message: '请求出现异常', duration: 2000});
            });
          }
        });
      },
      //批量删除
      batchDeleteUser: function () {
        //let ids = this.sels.map(item => item.id).toString();
        let devIds = this.sels.map(item => item.devId).toString();
        let that = this;
        this.$confirm('确认删除选中记录吗？', '提示', {
          type: 'warning'
        }).then(() => {
          that.loading = true;
          API.removeBatch(devIds).then(function (result) {
            that.loading = false;
            if (result && parseInt(result.errcode) === 0) {
              that.$message.success({showClose: true, message: '删除成功', duration: 2500});
              that.filters.name = '';
              that.filters.admin = '';                
              that.search();
            }
          }, function (err) {
            that.loading = false;
            that.$message.error({showClose: true, message: err.toString(), duration: 2000});
          }).catch(function (error) {
            that.loading = false;
            console.log(error);
            that.$message.error({showClose: true, message: '请求出现异常', duration: 2000});
          });
        }).catch(() => {

        });
      },

      getBlgUers: function() {
        let that = this;
        var userInfo = sessionStorage.getItem('access-user');
        if (userInfo) {
          userInfo = JSON.parse(userInfo);
        }
		console.log('userinfo is');
		console.log(userInfo);
        APIUSER.GetBlgAdmins(userInfo).then(function (result) {
          that.loading = false;
          console.log(result);
          if (result) {
            if (result.errcode==0 && result.blgAdmins ) {
         that.blgAdmins = result.blgAdmins;     
            } else{
               that.$message.error({showClose: true, message: '该用户没有关联任何设备！', duration: 5000});
            }
          }
        }, function (err) {
          that.$message.error({showClose: true, message: err.toString(), duration: 2000});
        }).catch(function (error) {
          console.log(error);
          that.$message.error({showClose: true, message: '请求出现异常', duration: 2000});
        }); 
		
        APIUSER.GetBlgQMUsers(userInfo).then(function (result) {
          that.loading = false;
          console.log(result);
          if (result) {
            if (result.errcode==0 && result.blgQMUsers ) {
         that.blgQMUsers = result.blgQMUsers;     
            } else{
               that.$message.error({showClose: true, message: '该用户没有关联任何设备！', duration: 5000});
            }
          }
        }, function (err) {
          that.$message.error({showClose: true, message: err.toString(), duration: 2000});
        }).catch(function (error) {
          console.log(error);
          that.$message.error({showClose: true, message: '请求出现异常', duration: 2000});
        }); 		
		
        APIUSER.GetBlgQUsers(userInfo).then(function (result) {
          that.loading = false;
          console.log(result);
          if (result) {
            if (result.errcode==0 && result.blgQUsers ) {
               that.blgQUsers = result.blgQUsers;     
            } else{
               that.$message.error({showClose: true, message: '该用户没有关联任何设备！', duration: 5000});
            }
          }
        }, function (err) {
          that.$message.error({showClose: true, message: err.toString(), duration: 2000});
        }).catch(function (error) {
          console.log(error);
          that.$message.error({showClose: true, message: '请求出现异常', duration: 2000});
        }); 		
      
      }  


    },
	
    mounted() {
      this.handleSearch()
	  this.role = sessionStorage.getItem('privilege');
    }
  }
</script>

<style>
  .demo-table-expand label {
    font-weight: bold;
  }
</style>
