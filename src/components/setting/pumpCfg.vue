<template>
<el-form ref="form" :model="form" label-width="80px">
  <el-col :span="24" class="warp-breadcrum">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }"><b>首页</b></el-breadcrumb-item>
        <el-breadcrumb-item>泵阀管理</el-breadcrumb-item>
      </el-breadcrumb>
  </el-col>
  <el-row :gutter="20">
  <el-col :span="6">
  <el-form-item label="设备号">
    <el-select v-model="form.devId" placeholder="请选择设备号" @change="devidChanged" >
      <el-option v-for="item in devids" :label="item.label" :value="item.value" ></el-option>
    </el-select>
  </el-form-item>
  </el-col>
  </el-row> 
  <el-col :span="24" class="warp-breadcrum">
      <P><strong>泵流速(ml/S)</strong></P>
      <!--列表-->
      <el-table :data="pumpData" v-loading="Loading" style="width: 100%;">
        <el-table-column prop="p1" label="泵1"  header-align="center" align="center"></el-table-column>
        <el-table-column prop="p2" label="泵2"  header-align="center" align="center"></el-table-column>
        <el-table-column prop="p3" label="泵3"  header-align="center" align="center"></el-table-column>
        <el-table-column prop="p4" label="泵4"  header-align="center" align="center"></el-table-column>
        <el-table-column prop="p5" label="泵5"  header-align="center" align="center"></el-table-column>
        <el-table-column prop="p6" label="泵6"  header-align="center" align="center"></el-table-column>
        <el-table-column prop="p7" label="泵7"  header-align="center" align="center"></el-table-column>
        <el-table-column prop="p8" label="泵8"  header-align="center" align="center"></el-table-column>
        <el-table-column label="操作" width="100" header-align="center" align="center">
          <template scope="scope">
            <el-button size="small" @click="showPumpEditDialog(scope.$index,scope.row)">流速修正</el-button>
          </template>
        </el-table-column>
      </el-table>
  </el-col> 
      <el-dialog title="编辑" :visible.sync="editPumpFormVisible" :close-on-click-modal="false">
        <el-form :model="editPumpForm" label-width="100px" ref="editPumpForm">
		  <el-row>
		  <el-col :span="12">
          <el-form-item label="泵1" prop="p1" >
            <el-input v-model="editPumpForm.p1" auto-complete="off"></el-input>
          </el-form-item>
		  </el-col>
		  <el-col :span="12">
          <el-form-item label="泵2" prop="p2">
            <el-input v-model="editPumpForm.p2" auto-complete="off"></el-input>
          </el-form-item>
          </el-col>		  
		  </el-row>
		  <el-row>
		  <el-col :span="12">
          <el-form-item label="泵3" prop="p3">
            <el-input v-model="editPumpForm.p3" auto-complete="off"></el-input>
          </el-form-item>   
		  </el-col>
		  <el-col :span="12">
          <el-form-item label="泵4" prop="p4">
            <el-input v-model="editPumpForm.p4" auto-complete="off"></el-input>
          </el-form-item>   
          </el-col>
		  </el-row>
		  <el-row>
          <el-col :span="12">		  
          <el-form-item label="泵5" prop="p5">
            <el-input v-model="editPumpForm.p5" auto-complete="off"></el-input>
          </el-form-item>   
		  </el-col>
		  <el-col :span="12">
          <el-form-item label="泵6" prop="p6">
            <el-input v-model="editPumpForm.p6" auto-complete="off"></el-input>
          </el-form-item>   
		  </el-col>
		  </el-row>
		  <el-row>
		  <el-col :span="12">
          <el-form-item label="泵7" prop="p7">
            <el-input v-model="editPumpForm.p7" auto-complete="off"></el-input>
          </el-form-item>   
		  </el-col>
		  <el-col :span="12">
          <el-form-item label="泵8" prop="p8">
            <el-input v-model="editPumpForm.p8" auto-complete="off"></el-input>
          </el-form-item>   
		  </el-col>
		  </el-row>
          
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="editPumpFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="editPumpSubmit" :loading="editPumpLoading">提交</el-button>
        </div>
      </el-dialog>
    
    <el-col :span="24" class="warp-breadcrum">
      <P><strong>阀门配置</strong></P>
      <!--列表-->
      <el-table :data="washData" highlight-current-row v-loading="Loading" height="402" style="width: 100%;">
        <caption>阀门配置</caption>
        <el-table-column prop="washNo" label="洗衣机" ></el-table-column>
        <el-table-column label="进水阀" header-align="center">
          <el-table-column prop="inopen" label="开启延时(S)"  header-align="center" align="center">
          </el-table-column>
          <el-table-column prop="inclose" label="关闭延时(S)(冲水时间)"  header-align="center" align="center">
          </el-table-column>
        </el-table-column>
        <el-table-column label="出水阀" header-align="center">
          <el-table-column prop="outopen" label="开启延时(S)"  header-align="center" align="center">
          </el-table-column>
          <el-table-column prop="outclose" label="关闭延时(S)"  header-align="center" align="center">
          </el-table-column>        
        </el-table-column>
        <el-table-column label="操作" width="150" header-align="center" align="center">
          <template scope="scope">
            <el-button size="small" @click="showEditDialog(scope.$index,scope.row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-col>

      <el-dialog title="编辑" :visible.sync="editFormVisible" :close-on-click-modal="false">
        <el-form :model="editForm" label-width="100px" ref="editForm">
          <el-form-item label="洗衣机" prop="washNo" >
            <el-input v-model="editForm.washNo" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="进水开启延时" prop="inopen">
            <el-input v-model="editForm.inopen" auto-complete="off"></el-input>
          </el-form-item>       
          <el-form-item label="进水关闭延时" prop="inclose">
            <el-input v-model="editForm.inclose" auto-complete="off"></el-input>
          </el-form-item>      
          <el-form-item label="出水开启延时" prop="outopen">
            <el-input v-model="editForm.outopen" auto-complete="off"></el-input>
          </el-form-item>       
          <el-form-item label="出水关闭延时" prop="outclose">
            <el-input v-model="editForm.outclose" auto-complete="off"></el-input>
          </el-form-item>      
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native="editFormVisible = false">取消</el-button>
          <el-button type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>
        </div>
      </el-dialog>
        

</el-form>

</template>
<script>
  import APISET from '../../api/api_setting';
  import APIDEV from '../../api/api_device';

  export default{
    data(){
      return {
        devids: '',
        arrPumpCfg: ['碱液', '助剂','氧漂','氯漂','柔软剂','酸剂','水处理','乳化剂'],
        form: { devId: '', date1: '', date2: '',delivery: false, type: [], resource: '', unwater: true, desc: ''},
        pumpData: [{p1:'',p2:'',p3:'',p4:'',p5:'',p6:'',p7:'',p8:''}],
        washData: [{washNo: "1号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "2号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "3号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "4号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "5号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "6号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "7号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "8号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""}
        ],

        //编辑pump相关数据
        editPumpFormVisible: false,//编辑界面是否显示
        editPumpLoading: false,
        editPumpFormindex: 0,
        editPumpForm: {p1: '', p2: '', p3: '', p4: '', p5: '', p6: '', p7: '', p8: '' },

        //编辑相关数据
        editFormVisible: false,//编辑界面是否显示
        editLoading: false,
        editFormindex: 0,
        editForm: { washNo: '', inopen: '', inclose: '',  outopen: '', outclose: '' },
        Loading: false
      }
    },
    methods: {

      //获取当期用户设备号
      getDevidByUser() {
	  let that = this;
        var userInfo = sessionStorage.getItem('access-user');
        if (userInfo) {
          userInfo = JSON.parse(userInfo);
        }
        let para = {
          loginUser: userInfo
        };
        APISET.GetDevidLists(para).then(function (result) {
          that.loading = false;
          console.log(result);
          if (result) {
            if (result.errcode==0 && result.devIds ) {
		 	   that.devids = result.devIds;			
            } else{
               that.$message.error({showClose: true, message: '该用户没有关联任何设备！', duration: 5000});
            }
          }
        }, function (err) {
          that.loading = false;
		  that.Loading = false;
          that.$message.error({showClose: true, message: err.toString(), duration: 2000});
        }).catch(function (error) {
          that.loading = false;
		  that.Loading = false;
          console.log(error);
          that.$message.error({showClose: true, message: '请求出现异常', duration: 2000});
        });	
        
      },


      // dev change event
      devidChanged: function(){
        
        console.log(">. device changed ");
		
        this.pumpData = [{p1:'',p2:'',p3:'',p4:'',p5:'',p6:'',p7:'',p8:''}];
        this.washData = [{washNo: "1号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "2号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "3号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "4号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "5号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "6号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "7号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "8号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""}
        ];
		
        console.log(">. current devid is ");
        console.log(this.form.devId);
        this.getPumpCfg();
        this.getWashCfg();
      },


      //获取当前设备泵配置信息
      getPumpCfg() {
	    let that = this;
		let devId = this.form.devId;
        // get pump cfg
		
        that.loading = true;
        APISET.GetPumpByDevId(devId).then(function (result) {
          that.loading = false;
          if (result) {
            let pumpcfg = result.pumpcfgs;
            that.pumpData[0].p1 = pumpcfg[0];
            that.pumpData[0].p2 = pumpcfg[1];
            that.pumpData[0].p3 = pumpcfg[2];
            that.pumpData[0].p4 = pumpcfg[3];
            that.pumpData[0].p5 = pumpcfg[4];
            that.pumpData[0].p6 = pumpcfg[5];
            that.pumpData[0].p7 = pumpcfg[6];
            that.pumpData[0].p8 = pumpcfg[7];
          }

        }, function (err) {
          that.loading = false;
          that.$message.error({showClose: true, message: err.toString(), duration: 2000});
        }).catch(function (error) {
          that.loading = false;
          console.log(error);
          that.$message.error({showClose: true, message: '请求出现异常', duration: 2000});
        });		
        this.Loading = false;
      },
   	  
      //获取当前设备wash配置信息
      getWashCfg() {
	    let that = this;
        let devId = this.form.devId;
        this.Loading = true;
        
        APISET.GetWashByDevId(devId).then(function (result) {
            that.loading = false;
            console.log("receive get all users result")
            console.log(result)
            if (result) {
                let washcfg = result.washcfgs;
                for(var i=0; i<that.washData.length; i++ ){
                    that.washData[i].inopen = washcfg[i].ins;
                    that.washData[i].inclose = washcfg[i].inc;
                    that.washData[i].outopen = washcfg[i].outs;
                    that.washData[i].outclose = washcfg[i].outc;
                }	  
            }
        }, function (err) {
            that.loading = false;
            that.$message.error({showClose: true, message: err.toString(), duration: 2000});
            that.washData=[
                   {washNo: "1号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "2号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "3号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "4号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "5号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "6号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "7号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "8号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""}
            ];		  
        }).catch(function (error) {
            that.loading = false;
            console.log(error);
            that.$message.error({showClose: true, message: '请求出现异常', duration: 2000});
            that.washData=[
                   {washNo: "1号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "2号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "3号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "4号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "5号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "6号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "7号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""},
                   {washNo: "8号洗衣机", inopen: "", inclose: "", outopen: "", outclose: ""}
            ];			
        });		
				
        this.Loading = false;
      },

      //显示编辑界面
      showPumpEditDialog: function (index, row) {
        console.log(">. showPumpEditDialog index:" + index );
        console.log(row);
        this.editPumpFormVisible = true;
		console.log(this.editPumpFormVisible);
        this.editPumpForm = Object.assign({}, row);
        console.log(this.editPumpForm);
        this.editPumpFormindex = index;
      },

      //编辑 pump
      editPumpSubmit: function () {
	    let that = this;
        this.$refs.editPumpForm.validate((valid) => {
          if (valid) {
		      console.log("valid is ");
			  console.log(valid);
              this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.editPumpLoading = true;
              let editpump = Object.assign({}, this.editPumpForm);
              console.log(">. editPumpForm para output");
              console.log(editpump);   
			  /*
              this.pumpData[this.editPumpFormindex].p1 = editpump.p1;
              this.pumpData[this.editPumpFormindex].p2 = editpump.p2;
              this.pumpData[this.editPumpFormindex].p3 = editpump.p3;
              this.pumpData[this.editPumpFormindex].p4 = editpump.p4;
              this.pumpData[this.editPumpFormindex].p5 = editpump.p5;
              this.pumpData[this.editPumpFormindex].p6 = editpump.p6;
              this.pumpData[this.editPumpFormindex].p7 = editpump.p7;
              this.pumpData[this.editPumpFormindex].p8 = editpump.p8;
              */
              // here, need update this data to mongodb            
              let pumps = {};
              pumps['pump1'] = editpump.p1;
              pumps['pump2'] = editpump.p2;
              pumps['pump3'] = editpump.p3;
              pumps['pump4'] = editpump.p4;
              pumps['pump5'] = editpump.p5;
              pumps['pump6'] = editpump.p6;
              pumps['pump7'] = editpump.p7;
              pumps['pump8'] = editpump.p8;

              let para = {
                devId: that.form.devId,
                pumps: pumps
              };
              console.log("parra is");
              console.log(para);              
  

            APISET.UpdatePumpByDevId(that.form.devId, para).then(function (result) {
              that.editPumpLoading = false;
              if (result && parseInt(result.errcode) === 0) {
                that.$message.success({showClose: true, message: '修改成功', duration: 4000});
                that.$refs['editPumpForm'].resetFields();
                that.editPumpFormVisible = false;
                that.getPumpCfg();
              } else {
                that.$message.error({showClose: true, message: '修改失败', duration: 2000});
              }
            }, function (err) {
              that.editPumpLoading = false;
              that.$message.error({showClose: true, message: err.toString(), duration: 2000});
            }).catch(function (error) {
              that.editPumpLoading = false;
              console.log(error);
              that.$message.error({showClose: true, message: '请求出现异常', duration: 2000});
            });  

/*
		   reqEditPumpCfg(para).then((res) => {
                this.editPumpLoading = false;
                this.$message({
                  message: '提交成功',
                  type: 'success'
                });
                this.$refs['editPumpForm'].resetFields();
                this.editPumpFormVisible = false;
                this.getPumpCfg();
              }).catch(() => {
                  this.editPumpLoading = false;
                  console.log("edit failed")
                  this.$message({
                      message: '编辑失败，请重新操作',
                      type: 'error'
                  });
                  this.$refs['editPumpForm'].resetFields();
                  this.editPumpFormVisible = false;
                  this.getPumpCfg();
              });
*/
            });
          }
        });
      },

      //显示编辑界面
      showEditDialog: function (index, row) {
        console.log(">. showEditDialog index:" + index );
        console.log(row);
        this.editFormVisible = true;
        this.editForm = Object.assign({}, row);
        this.editFormindex = index;
      },
      //编辑 wash
      editSubmit: function () {
	    let that = this;
        this.$refs.editForm.validate((valid) => {
          if (valid) {
            this.$confirm('确认提交吗？', '提示', {}).then(() => {
              this.editLoading = true;
              let editWash = Object.assign({}, this.editForm);
              this.washData[this.editFormindex].inopen = editWash.inopen;
              this.washData[this.editFormindex].inclose = editWash.inclose;
              this.washData[this.editFormindex].outopen = editWash.outopen;
              this.washData[this.editFormindex].outclose = editWash.outclose;
              let wash = {};
              let washIndex = this.editFormindex + 1;
              wash['inopen'] = parseInt(editWash.inopen);
              wash['inclose'] = parseInt(editWash.inclose);
              wash['outopen'] = parseInt(editWash.outopen);
              wash['outclose'] = parseInt(editWash.outclose);

              let para = {
                devId: this.form.devId,
                washIndex: washIndex,
                wash: wash
              };
            
			        APISET.UpdateWashByDevId(that.form.devId, para).then(function (result) {
                 that.editLoading = false;
                 if (result && parseInt(result.errcode) === 0) {
                   that.$message.success({showClose: true, message: '修改成功', duration: 4000});
                   that.$refs['editForm'].resetFields();
                   that.editFormVisible = false;
                   that.getWashCfg();
                 } else {
                   that.$message.error({showClose: true, message: '修改失败', duration: 2000});
                 }
              }, function (err) {
                 that.editLoading = false;
                 that.$message.error({showClose: true, message: err.toString(), duration: 2000});
              }).catch(function (error) {
                 that.editLoading = false;
                 console.log(error);
                 that.$message.error({showClose: true, message: '请求出现异常', duration: 2000});
              });  			  
			  
			  
/*
              reqEditWashCfg(para).then((res) => {

                this.editLoading = false;
                //NProgress.done();
                this.$message({ message: '提交成功', type: 'success'});
                this.$refs['editForm'].resetFields();
                this.editFormVisible = false;
                this.getWashCfg();
              }).catch(() => {
                  this.editLoading = false;
                  console.log("edit failed")
                  this.$message({message: '编辑洗衣机阀门配置失败，请重新操作',type: 'error'});
                  this.$refs['editForm'].resetFields();
                   this.editFormVisible = false;
                  this.getWashCfg();
              });
              this.editLoading = false;
              this.$message({ message: '提交成功', type: 'success' });
              this.$refs['editForm'].resetFields();
              this.editFormVisible = false;
*/

            });
				
          }
		  });
      },


      onSubmit() {
        console.log('submit!');
        console.log('form is ');
        console.log(this.form);
      },
      handleClick(tab, event) {
        console.log(tab, event);
      }
    },
    mounted() {
      this.getDevidByUser();
    }
  }

</script>

<style>
  .demo-table-expand label {
    font-weight: bold;
  }
</style>
