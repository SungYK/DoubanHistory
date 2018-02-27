
function initChart(element, title, rating, id) {
    var myChart = echarts.init(element);
    var now = new Date()
    var data = []
    var dataX = []
    var dataY = []
    var today = 0

    empty_data_flag = 1

    // gap
    dataX.push(" ")
    dataY.push(null)
    for(var key in rating) {
        var year = key.substring(0,4)
        var month = key.substring(5, key.length)
        if(rating[key] != 0) {
            dataX.push(year+"\n"+month)
            dataY.push(rating[key])
            today = rating[key]
            empty_data_flag = 0
        }
        
        // data.push(getData(new Date(key), rating[key]))
            
    }
    // gap
    dataX.push(" ")
    dataY.push(null)
    // console.log(dataX)
    
    if (empty_data_flag == 1) {
        title = title + " (暂无数据)"
    }
    
    // 指定图表的配置项和数据
    var option = {
        title: {
            text: title,
            padding: [
                5,  // 上
                5, // 右
                5,  // 下
                30, // 左
            ],
            subtext : "豆瓣链接",
            sublink: 'https://movie.douban.com/subject/'+id
        },
        tooltip: {
            trigger: 'axis'
        },
        grid: {
            show: false
        },
        xAxis: {
            type: 'category',
            splitLine: {
                show: false
            },
            boundaryGap:false,
            data: dataX
        },
        yAxis: {
            min: function (value) {
                if(value.min - 0.5 <= 0)
                    return 0
                return value.min - 0.5;
            },
            max: function (value) {
                return value.max + 0.5;
            },
            // min:0,
            // max:10,
            // silent: true,
            
            type: 'value'
        },
        dataZoom: [
            {
                type: 'inside',
                start: 0,
                end: 100
            }
        ],
        series: [{
            data: dataY,
            type: 'line',
            markPoint: {
                data: [
                    {coord: [dataY.length-2, today], name: '今日评分', value: today},
                    
                ]
            },
        }],
    };
    // myChart.showLoading()
    // 使用刚指定的配置项和数据显示图表。
   
    myChart.setOption(option)

    
}

function getData(date, rate) {
    
    return {
        name: date.toString(),
        value: [
            [date.getFullYear(), date.getMonth() + 1, date.getDate()].join('-'),
            rate
        ]
    }
}

