<template>
  <el-row class="warp">
    <el-col :span="24" class="warp-breadcrum">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }"><b>首页</b></el-breadcrumb-item>
      </el-breadcrumb>
    </el-col>
    <el-col :span="24" class="warp-main">
      <section class="chart-container">
        <el-row>
            <div id="chartMap" style="width:100%; height:800px;"></div>
        </el-row>
      </section>
    </el-col>
  </el-row>
</template>
<style>

</style>

<script>
  import echarts from 'echarts'  
  import china from '../assets/map/china.js'
  import shine from '../assets/map/shine.js'
  import chinaJson from '../assets/map/china.json'
  import API from '../api/api_device';
  import option from '../assets/map/map-option1.js'


  export default {
    data() {
      return {
        chartMap: null,
        loading: false
      };
    },

    methods: {

      getData(){
        let that = this;
        let loginUser = JSON.parse(window.sessionStorage.getItem('access-user'));
        let params = {
          loginUser: loginUser
        };
        that.loading = true;
        API.getDevScatter(params).then(function (result) {
          that.loading = false;
          if (result) {
            if (result.total > 0) {
           
                that.total = result.total;
                option.series[0].data = that.convertData(result.dataScatter);
                var _this = that;
                echarts.registerMap('china', chinaJson);
                //基于准备好的dom，初始化echarts实例
                //this.chartMap = echarts.init(document.getElementById('chartMap'));
                that.chartMap = echarts.init(document.getElementById('chartMap'),'shine');
                that.chartMap.setOption(option);
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

      convertData(data){
        var geoCoordMap = {
        "新疆维":[84.9023,42.148],"西藏自":[87.8695,31.6846],"内蒙古":[111.65,40.82 ],
        "青海省":[101.9199,30.1904],"四川省":[101.9199,30.1904],"黑龙江":[126.1445,48.7156],
        "甘肃省":[99.7129,38.166],"云南省":[101.0652,25.1807], "广西壮":[107.7813,23.6426],"湖南省":[111.5332,27.3779],"陕西省":[109.5996,35.7396],
        "广东省":[113.4668,22.8076],"吉林省":[125.7746,43.5938],"河北省":[115.4004,39.4688],
        "湖北省":[112.2363,31.1572],"贵州省":[106.6113,26.9385],"山东省":[118.7402,36.4307],
        "江西省":[116.0156,27.29],"河南省":[113.0668,33.8818],"辽宁省":[122.0438,41.0889],
        "山西省":[112.4121,37.6611],"安徽省":[117.2461,32.0361],"福建省":[118.3008,25.9277],
        "浙江省":[120.498,29.0918],"江苏省":[118.8586,32.915],"重庆市":[107.7539,30.1904],
        "宁夏回":[105.9961,37.3096],"海南省":[109.9512,19.2041],"台湾省":[120.0254,23.5986],
        "北京市":[116.4551,40.2539],"天津市":[117.4219,39.4189],"上海市":[121.4648,31.2891],
        "香港特":[114.1178,22.3242],"澳门特":[111.5547,22.1484]
        };

        var res = [];
        for (var i = 0; i < data.length; i++) {
            var geoCoord = geoCoordMap[data[i].name];//获取坐标
            if (geoCoord) {//如果有坐标
              res.push({//创建对象数组，
                        name: data[i].name,  
                        value: geoCoord.concat(data[i].value)  //用连接数组的形式将value值加入
                    });  
                //res.push(geoCoord.concat(data[i].value));
                //res.push(geoCoord.concat(data[i].name));
            }
        }
        return res;
      }

    },

    mounted: function () {
      // get device scatter data
      this.getData();
    }
  }
</script>
