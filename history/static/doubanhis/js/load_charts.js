
function initChart(element, title, rating, id) {
    var myChart = echarts.init(element);
    var now = new Date()
    var data = []
    var dataX = []
    var dataY = []
    
    empty_data_flag = 1
    for(var key in rating) {
        var year = key.substring(0,4)
        var month = key.substring(5, key.length)
        dataX.push(year+"\n"+month)
        dataY.push(rating[key])
        
        // data.push(getData(new Date(key), rating[key]))
        if(rating[key] != 0)
            empty_data_flag = 0
    }
    
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
            data: dataX
        },
        yAxis: {
            min: function (value) {
                return value.min - 0.5;
            },
            max: function (value) {
                return value.max + 0.5;
            },
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
            type: 'line'
        }],
    };
    // myChart.showLoading()
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
    myChart.hideLoading()
    return rating
    
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

