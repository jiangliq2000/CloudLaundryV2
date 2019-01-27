<template>
  <el-row class="warp">
    <el-col :span="24" class="warp-breadcrum">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }"><b>首页</b></el-breadcrumb-item>
        <el-breadcrumb-item>数据查询</el-breadcrumb-item>
        <el-breadcrumb-item>日期查询</el-breadcrumb-item>
      </el-breadcrumb>
    </el-col>
 

    <el-col :span="24" class="warp-main">
      <!--工具条-->
      <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
        <el-form :inline="true" :model="form" >
          <el-form-item label="起始时间">
            <el-date-picker type="date" placeholder="选择日期" v-model="form.starttime" value-format="yyyy-MM-dd" @change="sdateChanged" :picker-options="pickerOptions0" ></el-date-picker>
          </el-form-item>          
          <el-form-item label="结束时间">
            <el-date-picker type="date" placeholder="选择日期" v-model="form.endtime" value-format="yyyy-MM-dd" @change="edateChanged" :picker-options="pickerOptions0" ></el-date-picker>
          </el-form-item>       
          <el-form-item>
            <el-button type="primary" v-on:click="clickGetStats" icon="search">查询</el-button>
          </el-form-item>
        </el-form>
      </el-col>
    
    <el-alert  title="该时间段内未查询到任何数据"  type="warning" v-if="nodatashow">
    </el-alert>

    <el-alert  title="数据正在查询中..... 请耐心等候 " center type="warning" v-if="listLoading">
    </el-alert>

    <!-- 每台设备统计 -->
    <el-card class="box-card" v-for="stats in statsObj">
      <div slot="header" class="clearfix">
        <span style="line-height: 36px;">设备号：{{stats.devId}}   </span>
        <el-button  type="primary" @click="downloads(stats.devId)">下载明细</el-button>
        <span style="line-height: 36px;"> 位置: {{stats.position}}   </span>
        <span style="line-height: 36px;">备注：{{stats.comment2}}  </span>
      </div>      
	  
      <!--车数统计-->
      <el-table :data="stats.wash" style="width: 100%" >
        <el-table-column prop="wash0" label="总车数" width="80" header-align="center" align="center">
        </el-table-column>     
        <el-table-column prop="wash1" label="1号车数" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="wash2" label="2号车数" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="wash3" label="3号车数" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="wash4" label="4号车数"  header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="wash5" label="5号车数" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="wash6" label="6号车数" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="wash7" label="7号车数" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="wash8" label="8号车数" header-align="center" align="center">
        </el-table-column>     
      </el-table>
      <!--药剂统计-->
      <el-table :data="stats.drug" style="width: 100%" >
        <el-table-column prop="drugname" label="药剂名" header-align="center" align="center">
        </el-table-column	  
        <el-table-column prop="drug1" label="药剂1" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="drug2" label="药剂2" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="drug3" label="药剂3" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="drug4" label="药剂4" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="drug5" label="药剂5" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="drug6" label="药剂6" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="drug7" label="药剂7" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="drug8" label="药剂8" header-align="center" align="center">
        </el-table-column>
      </el-table>
      <!--配方统计-->
      <el-table :data="stats.formula" style="width: 100%" >
        <el-table-column prop="fmname" label="配方号" header-align="center" align="center">
        </el-table-column>	  
        <el-table-column prop="fm1" label="1" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="fm2" label="2" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="fm3" label="3" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="fm4" label="4" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="fm5" label="5" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="fm6" label="6" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="fm7" label="7" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="fm8" label="8" header-align="center" align="center">
        </el-table-column>      
        <el-table-column prop="fm9" label="9" header-align="center" align="center">
        </el-table-column>     
        <el-table-column prop="fm10" label="10" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="fm11" label="11" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="fm12" label="12" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="fm13" label="13" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="fm14" label="14" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="fm15" label="15" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="fm16" label="16" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="fm17" label="17" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="fm18" label="18" header-align="center" align="center">
        </el-table-column>   
        <el-table-column prop="fm19" label="19" header-align="center" align="center">
        </el-table-column>
        <el-table-column prop="fm20" label="20" header-align="center" align="center">
        </el-table-column>
      </el-table>
    </el-card>
	
	<!--工具条-->
    <el-col :span="24" class="toolbar">
        <el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="5" :total="total"
                       style="float:right;">
        </el-pagination>
    </el-col>
		
    </el-col>
  </el-row>
</template>
<script>
  import API from '../../api/api_query';


  export default{
    data(){
      return {
        form: {
          starttime: "",
          endtime: ""
        },
        pickerOptions0: {
          disabledDate(time) {
            return (time.getTime() > Date.now());
          }
        },

        statsObj: [],
          listLoading: false,
        //nodatashow: false,
        showDownLoad: false,
        total: 0,
        page: 1,
        limit: 3,
        loading: false,
        role: '3'		
      }
    },
    methods: {
	
      handleCurrentChange(val) {
        this.page = val;
        console.log("val is: ");
        console.log(val)
        this.getStats();
      },	
	
	  clickGetStats(){
		this.total = 0;
        this.page = 1;
		this.getStats()	  
	  },
      //获取统计数据
      getStats() {
	    let that = this;

        this.nodatashow = false;
		
        console.log(">. dateQuery getStatas")
        var userInfo = sessionStorage.getItem('access-user');
		var privilege = sessionStorage.getItem('privilege'); 
        console.log("username is: " + userInfo)

        if (userInfo) {
          var username = JSON.parse(userInfo);
        }

        let st = this.form.starttime;
        let et = this.form.endtime;
		console.log(st);
		console.log(et);
        let stdt = new Date(st.replace("-","/"));
        let etdt = new Date(et.replace("-","/"));
		
        let iDays = parseInt(Math.abs(stdt - etdt)/1000/60/60/24);
        console.log(iDays);
        console.log((iDays>31));
        if ((privilege != '0') && (iDays > 31 )){

          alert("查询时间长度不能超过1个月, 请重新输入");
          return ;
        }

        this.listLoading = true;		
		
        let para = {
          loginUser: username,
          starttime: this.form.starttime,
          endtime: this.form.endtime,
          page: that.page,
          limit: that.limit,
        };    

		/*
        const loading = this.$loading({
          lock: true,
          text: '数据正在查询中..... 请请耐心等候',
          spinner: 'el-icon-loading',
          background: 'rgba(0, 0, 0, 0.7)'
        });

		*/
		
        API.GetAllStats(para).then(function (result) {
          that.loading = false;
		  that.listLoading = false;
          if (result) {
            if (result.total > 0) {
               that.total = result.total;
               that.statsObj = result.stats;              
            } else{
               that.$message.error({showClose: true, message: '该时间段内未查询到任何数据！', duration: 5000});
            }
          }
        }, function (err) {
          that.loading = false;
		  that.listLoading = false;
          that.$message.error({showClose: true, message: err.toString(), duration: 2000});
        }).catch(function (error) {
          that.loading = false;
		  that.listLoading = false;
          console.log(error);
          that.$message.error({showClose: true, message: '请求出现异常', duration: 2000});
        });		
		
			
		
		
		
		/*

        API.GetAllStats(para).then((res) => {
          
          console.log('> reqGetStats recive 200 OK');
          console.log(res.data);

          if (res.data && res.data.length!==0 ) {
            console.log("will show download detail");
            that.statsObj = res.data
            that.showDownLoad = true
          } else {
            console.log("don't display download button");
            that.nodatashow = true
          }         

          console.log(res)
          that.listLoading = false;

          loading.close();
          
        })
        .catch((error) => {
          loading.close();
		  that.listLoading = false;
		  that.$message.error({showClose: true, message: "该时间段内未查询到任何数据", duration: 2000});
          console.log("download error")
          console.log(error);
        });
		
		*/
		

      },

      sdateChanged(val){
        console.log("time change");
        console.log(val);
        this.form.starttime = val;
        this.showDownLoad = false;   
        this.statsObj = {} 
      },
      edateChanged(val){
        console.log("time change");
        console.log(val);
        this.form.endtime = val;
        this.showDownLoad = false;   
        this.statsObj = {} 
      },

      //下载详细数据
      downloads(devId) {
        console.log("> dataQuery. download....")
        console.log(devId);

        let params = {}
        let stime =  this.form.starttime;
        let etime =  this.form.endtime;        
        let filename = devId +'_'+ stime +"_" +  etime + '.csv';
        
        params['filename'] = filename;
        params['condition'] = "?devId=" + devId + "&starttime=" + stime + "&endtime=" + etime ;

        API.reqDownloadStats(params);
        //window.open("http://127.0.0.1:10000/data/download/"+filename + "?user=admin&starttime=2017-02-28&endtime=2017-07-18");
  
      }

    },
    mounted() {
      console.log("> dataQuery mounted called")
      // set default query day
      //this.getStats();
      let d = new Date();
      console.log(d);
      console.log(d.getFullYear());
      console.log(d.getMonth() + 1);
      console.log(d.getDate());
      //this.form.starttime = d.getFullYear() + "-" + (d.getMonth()+1) + "-" + d.getDate();
      //this.form.endtime = d.getFullYear() + "-" + (d.getMonth()+1) + "-" + d.getDate();

    }
  }
</script>

<style>
  .demo-table-expand label {
    font-weight: bold;
  }
</style>
