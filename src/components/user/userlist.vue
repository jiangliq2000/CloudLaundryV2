<template>
  <el-row class="warp">
    <el-col :span="24" class="warp-breadcrum">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }"><b>首页</b></el-breadcrumb-item>
        <el-breadcrumb-item>用户列表</el-breadcrumb-item>
      </el-breadcrumb>
    </el-col>

    <el-col :span="24" class="warp-main" v-loading="loading" element-loading-text="拼命加载中">
      <!--工具条-->
      <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
        <el-form :inline="true" :model="filters">
          <el-form-item>
            <el-input v-model="filters.name" placeholder="用户姓名" @keyup.enter.native="handleSearch"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" v-on:click="handleSearch">查询</el-button>
          </el-form-item>
          <el-form-item>
            <el-input v-model="filters.mobile" placeholder="手机号" @keyup.enter.native="mobileSearch"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" v-on:click="mobileSearch">查询</el-button>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="showAddDialog">新增</el-button>
          </el-form-item>
        </el-form>
      </el-col>

      <!--列表-->
      <el-table :data="users" highlight-current-row @selection-change="selsChange"
                style="width: 100%;">
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column type="index" width="60"></el-table-column>

        <el-table-column type="expand" >
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-row :gutter="15">
                  <el-form-item label="设备列表">
                    <span>{{ props.row.devId }}</span>
                  </el-form-item>                         

                  <el-form-item label="上次登录ip">
                    <span>{{ props.row.lastloginip}}</span>
                  </el-form-item>   

            </el-row>
            </el-form>
          </template>
        </el-table-column>   
        <el-table-column prop="username" label="用户名" sortable></el-table-column>
        <el-table-column prop="name" label="姓名" sortable></el-table-column>
        <el-table-column prop="password" label="密码" sortable></el-table-column>
        <el-table-column prop="privilege" label="权限" :formatter="formatRole" sortable></el-table-column>   
        <el-table-column prop="contact" label="手机" ></el-table-column>
        <el-table-column prop="register" label="创建日期" ></el-table-column>
       
        <el-table-column label="编辑" >
          <template slot-scope="scope">
            <el-button type="warning" @click="showEditDialog(scope.$index,scope.row)" size="small">编辑</el-button>
          </template>
        </el-table-column>
        <el-table-column label="删除">
          <template slot-scope="scope">
            <el-button type="danger" @click="delUser(scope.$index,scope.row)" size="small">删除</el-button>
          </template>
        </el-table-column>			
		
      </el-table>

      <!--工具条-->
      <el-col :span="24" class="toolbar">
        <el-button type="danger" @click="batchDeleteUser" :disabled="this.sels.length===0">批量删除</el-button>
        <el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="10" :total="total"
                       style="float:right;">
        </el-pagination>
      </el-col>

      <el-dialog title="编辑" :visible.sync ="editFormVisible" :close-on-click-modal="false">
        <el-form :model="editForm" label-width="100px" :rules="editFormRules" ref="editForm">
          <el-form-item label="用户名" prop="username" >
            <el-input v-model="editForm.username" auto-complete="off" :disabled="true"></el-input>
          </el-form-item>	
          <el-form-item label="姓名" prop="name" >
            <el-input v-model="editForm.name" auto-complete="off" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password" >
            <el-input v-model="editForm.password" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="权限" prop="privilege" auto-complete="off" >
            <el-select v-model="editForm.privilege" placeholder="请选择权限">
			    <el-option label="超级管理员" v-if="role === '0'"   value="0"></el-option>
                <el-option label="VIP化料公司" v-if="role === '0'"   value="1"></el-option>
			    <el-option label="五星用户" value="2"></el-option>
                <el-option label="三星用户" value="3"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="手机" prop="contact" auto-complete="off" >
            <el-input v-model="editForm.contact" auto-complete="off"></el-input>
          </el-form-item>

        </el-form>        
		<div slot="footer" class="dialog-footer">
          <el-button @click.native="editFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="editSubmit">提交</el-button>
        </div>
      </el-dialog>

      <!--新增界面-->
      <el-dialog title="新增" :visible.sync ="addFormVisible" :close-on-click-modal="false">
        <el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
          <el-row>
            <el-col :span="8">
              <el-form-item label="姓名" prop="name">
                <el-input v-model="addForm.name" auto-complete="off"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="用户名" prop="username">
                <el-input v-model="addForm.username" auto-complete="off"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="权限">
                <el-select v-model="addForm.privilege" placeholder="请选择权限">
                  <el-option label="VIP化料公司" v-if="role === '0'" value="1"></el-option>
				  <el-option label="五星用户" value="2"></el-option>
                  <el-option label="三星用户" value="3"></el-option>
                </el-select>
              </el-form-item>  
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="8">
              <el-form-item label="密码" prop="password">
                <el-input v-model="addForm.password" auto-complete="off"></el-input>
              </el-form-item>  
            </el-col>
            <el-col :span="10">
              <el-form-item label="手机号" prop="contact">
                <el-input v-model="addForm.contact" auto-complete="off"></el-input>
              </el-form-item>  
            </el-col>          
          </el-row>  
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="addFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="addSubmit" :loading="addLoading">提交</el-button>
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
  import API from '../../api/api_user';
  import APIDEV from '../../api/api_device';

  export default{
    data(){
      return {
        filters: {
          name: '',
          mobile: ''
        },
        users: [],
        total: 0,
        page: 1,
        limit: 10,
        loading: false,
		role: '1',
        sels: [], //列表选中列

        //编辑相关数据
        editFormVisible: false,//编辑界面是否显示
        editFormRules: {
          name: [
            {required: true, message: '请输入用户姓名', trigger: 'blur'}
          ]
        },
        editForm: {
          username: '',
          name: '',
          password: '',
          privilege: '',
          contact: ''
        },

        //新增相关数据
        addFormVisible: false,//新增界面是否显示
        addLoading: false,
        addFormRules: {
          name: [
            {required: true, message: '请输入姓名', trigger: 'blur'}
          ],
          username: [
            {required: true, message: '请输入用户名', trigger: 'blur'}
          ],         
          mobile: [
            {required: true, message: '请输入手机号', trigger: 'blur'}
          ]          
        },
        addForm: {
          name: '',
          password: '',
          privilege: '',
          username: '',       
          contact: ''
        }
      }
    },
    methods: {
      formatRole(row, column){
        return row.privilege == 0 ? "超级管理员" : row.privilege == 1 ? "VIP化料公司" : row.privilege == 2 ? "五星用户" : "三星用户";
      },      
      handleCurrentChange(val) {
        this.page = val;
        console.log("val is: ");
        console.log(val)
        this.search();
      },

      mobileSearch(){
        console.log("mobile search");
        if (this.filters.mobile === '') {
          this.total = 0;
          this.page = 1;
          this.search();
        } else {
          this.total = 0;
          this.page = 1;
          this.SearchByMobile();
        }
      },
      SearchByMobile(){
        let that = this;
        that.loading = true;
        that.page = 1;
        that.total = 0;
        let param = that.filters.mobile;
        API.findByMobile(param).then(function (result) {
          that.loading = false;
          if (result && result.users) {
            if (result.users.length > 0) {
               that.users = result.users;
               that.total = result.users.length;
            } else{
               that.$message.error({showClose: true, message: '查询不到该用户信息, 请确认手机号码！', duration: 5000});
            }
          }
          that.filters.mobile = '';

        }, function (err) {
          that.loading = false;
          that.$message.error({showClose: true, message: err.toString(), duration: 2000});
        }).catch(function (error) {
          that.loading = false;
          console.log(error);
          that.$message.error({showClose: true, message: '请求出现异常', duration: 2000});
        });

      },

      handleSearch(){
        this.total = 0;
        this.page = 1;
        this.search();
      },
      search(){
        let that = this;
		console.log("loginuser is ");
		let loginUser = JSON.parse(window.sessionStorage.getItem('access-user'));
		console.log(loginUser);
        let params = {
          page: that.page,
          limit: 10,
          name: that.filters.name,
		  loginUser: loginUser
        };

        that.loading = true;
        API.findList(params).then(function (result) {
          that.loading = false;
          console.log("receive get all users result")
          console.log(result)
          if (result) {
            if (result.total > 0) {
               that.total = result.total;
               that.users = result.users;              
            } else{
               that.$message.error({showClose: true, message: '查询不到用户信息', duration: 5000});
			   that.users = []
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
      delUser: function (index, row) {
        let that = this;
        this.$confirm('确认删除该记录吗?', '提示', {type: 'warning'}).then(() => {
          that.loading = true;
          console.log("row.username is");
          console.log(row.username);
          API.remove(row.username).then(function (result) {
            that.loading = false;
            console.log('result is ');
            console.log(result);
            if (result && parseInt(result.errcode) === 0) {
              that.$message.success({showClose: true, message: '删除成功', duration: 2000});
            } else{
              that.$message.success({showClose: true, message: '删除失败，请重试', duration: 2000});
            }
            that.filters.name = '';
            that.filters.mobile = '';
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
        this.editFormVisible = true;
        this.editForm = Object.assign({}, row);
      },
      //编辑
      editSubmit: function () {
        let that = this;
        this.$refs.editForm.validate((valid) => {
          if (valid) {
            this.loading = true;
            let para = Object.assign({}, this.editForm);
            console.log("para.username is ");
            console.log(para);
            API.update(para.username, para).then(function (result) {
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
      showAddDialog: function () {
        this.addFormVisible = true;
        this.addForm = {
          username: '',
          name: '',
          password: '',
          contact:'',
		  privilege:''
        };
      },
      //新增
      addSubmit: function () {
        let that = this;
        this.$refs.addForm.validate((valid) => {
          if (valid) {
            that.loading = true;
            let para = Object.assign({}, this.addForm);
			let loginUser = JSON.parse(window.sessionStorage.getItem('access-user'));
			para['blgAdmin'] = loginUser;
            API.add(para).then(function (result) {
			  console.log('add user result');
			  console.log(result);
              that.loading = false;
              if (result) {
                if (parseInt(result.errcode) === 0){
                   that.$message.success({showClose: true, message: '添加用户信息成功', duration: 2000});
                  that.$refs['addForm'].resetFields();
                  that.addFormVisible = false;
                  that.search();
                } else if (parseInt(result.errcode) === 2) {
                  that.$message.error({showClose: true, message: '该用户名已经存在，请重新输入', duration: 2000});
                }else {
                   that.$message.error({showClose: true, message: '添加用户信息失败', duration: 2000});
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

          }
        });
      },
      //批量删除
      batchDeleteUser: function () {
        //let ids = this.sels.map(item => item.id).toString();
        let usernames = this.sels.map(item => item.username).toString();
        let that = this;
        this.$confirm('确认删除选中记录吗？', '提示', {
          type: 'warning'
        }).then(() => {
          that.loading = true;
          API.removeBatch(usernames).then(function (result) {
            that.loading = false;
            if (result && parseInt(result.errcode) === 0) {
              that.$message.success({showClose: true, message: '删除成功', duration: 2500});
              that.filters.name = '';
              that.filters.mobile = '';                
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
      }
    },
    mounted() {
      this.handleSearch()
	  this.role = sessionStorage.getItem('privilege');
	  console.log("userlist mount role is:");
	  console.log(this.role);
    }
  }
</script>

<style>
  .demo-table-expand label {
    font-weight: bold;
  }
</style>
