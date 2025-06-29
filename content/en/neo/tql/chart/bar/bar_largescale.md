---
title: Large Scale Bar Chart
type: docs
weight: 140
---

```js {{linenos=table,linenostart=1}}
FAKE(linspace(0,1,1))
CHART(
    chartJSCode({
        const data = generateData(5e5);
        function generateData(count) {
            let baseValue = Math.random() * 1000;
            let time = +new Date(2011, 0, 1);
            let smallBaseValue;
            function next(idx) {
                smallBaseValue =
                    idx % 30 === 0
                        ? Math.random() * 700
                        : smallBaseValue + Math.random() * 500 - 250;
                baseValue += Math.random() * 20 - 10;
                return Math.max(0, Math.round(baseValue + smallBaseValue) + 3000);
            }
            const categoryData = [];
            const valueData = [];
            for (let i = 0; i < count; i++) {
                categoryData.push(
                    echarts.format.formatTime('yyyy-MM-dd\nhh:mm:ss', time, false)
                );
                valueData.push(next(i).toFixed(2));
                time += 1000;
            }
            return {
                categoryData: categoryData,
                valueData: valueData
            };
        }
    }),
    chartOption({
        title: {
            text: "500,000 Data",
            left: 10
        },
        toolbox: {
            feature: {
                dataZoom: {
                    yAxisIndex: false
                },
                saveAsImage: {
                    pixelRatio: 2
                }
            }
        },
        tooltip: {
            trigger: "axis",
            axisPointer: {
                type: "shadow"
            }
        },
        grid: {
            bottom: 90
        },
        dataZoom: [
            {
                "type": "inside"
            },
            {
                "type": "slider"
            }
        ],
        xAxis: {
            data: data.categoryData,
            silent: false,
            splitLine: {
                show: false
            },
            splitArea: {
                show: false
            }
        },
        yAxis: {
            splitArea: {
                show: false
            }
        },
        series: [
            {
                type: "bar",
                data: data.valueData,
                large: true
            }
        ]
    })
)
```

{{< figure src="../../img/bar_largescale.jpg" width="500" >}}
