export default {
          title : {
              text: '海斯特分配器--分布云图',
              //subtext: '纯属虚构',
              x:'center'
          },          
          grid:{
              x:5,
              y:5,
              x2:5,
              y2:5,
              borderWidth:1
          },

          // 新建一个地理坐标系 geo ，
          geo: {
            map: 'china',//地图类型为中国地图,要是世界那就是world,要是省市区：例如beijing、shanghai
            itemStyle:{ // 定义样式
              normal:{       // 普通状态下的样式
                //areaColor:'#6699CC',
                areaColor: '#40E0D0',
                borderColor: '#fff',
              },
              emphasis: {         // 高亮状态下的样式
                areaColor: '#e9fbf1'
              }
            }
 
          },
          // hover显示目标数据
          tooltip : {
            trigger: 'item',
            // tooltip的trigger的值可以有'item'、'axis'。
            //'item':数据项图形触发，主要在散点图，饼图等无类目轴的图表中使用。
            //'axis':坐标轴触发，主要在柱状图，折线图等会使用类目轴的图表中使用
            "confine": true,
            "formatter": (p)=>{//自定义提示信息
                  let dataCon = p.data;
                  let txtCon =dataCon.name+'<br>数量:'+dataCon.value[2];
                  return txtCon;
            },            
            textStyle:{
              align:'left'
            },
          },
          // 图表背景色
          //backgroundColor: '#404a59',  
          backgrounColor: '#BEBEBE',

          // 标志颜色
          color:'green',
          // 新建散点图series
          series:[{
            name:'',//series名称
            type:'scatter',//为散点类型
            zoom: 2.2,
            coordinateSystem: 'geo',// series坐标系类型
            data:[
                    {name: "上海市", value: 20},
                    {name: "浙江省", value: 20},
                    {name: "海南省", value: 30}
                    ],
            symbol:'pin',
            symbolSize:[20,20]
          }],

          // 添加视觉映射组件
          
          visualMap: {
            type: 'continuous', // 连续型
            min: 0,           // 值域最小值，必须参数
            max: 600,     // 值域最大值，必须参数
            calculable: true, // 是否启用值域漫游
            inRange: {
              color: ['green']
               // 指定数值从低到高时的颜色变化
            },
            textStyle: {
              color: '#fff' // 值域控件的文本颜色
            }
          }
          
};