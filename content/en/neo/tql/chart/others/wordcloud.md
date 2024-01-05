---
title: Word Cloud
type: docs
weight: 940
---

```js
FAKE(csv(
`Deep Learning,6181
Computer Vision,4386
Artificial Intelligence,4055
Neural Network,3500
Algorithm,3333
Model,2700
Supervised,2500
Unsupervised,2333
Natural Language Processing,1900
Chatbot,1800
Virtual Assistant,1500
Speech Recognition,1400
Convolutional Neural Network,1325
Reinforcement Learning,1300
Training Data,1250
Classification,1233
Regression,1000
Decision Tree,900
K-Means,875
N-Gram Analysis,850
Microservices,833
Pattern Recognition,790
APIs,775
Feature Engineering,700
Random Forest,650
Bagging,600
Anomaly Detection,575
Naive Bayes,500
Autoencoder,400
Backpropagation,300
TensorFlow,290
word2vec,280
Object Recognition,250
Python,235
Predictive Analytics,225
Predictive Modeling,215
Optical Character Recognition,200
Overfitting,190
JavaScript,185
Text Analytics,180
Cognitive Computing,175
Augmented Intelligence,160
Statistical Models,155
Clustering,150
Topic Modeling,145
Data Mining,140
Data Science,138
Semi-Supervised Learning,137
Artificial Neural Networks,125
`))
MAPVALUE(0, dict("name", value(0), "value", value(1)))
POPVALUE(1)
CHART(
    plugins("wordcloud"),
    chartOption({
        series: {
            type: "wordCloud",
            gridSize: 8,
            sizeRange: [12, 50],
            rotationRange: [-90, 90],
            shape: "circle",
            width: 580,
            height: 580,
            drawOutOfBound: false,
            left: "center",
            top: "center",
            data: column(0),
            emphasis: {
                focus: "self",
                textStyle: {
                    textShadowBlur: 10,
                    textShadowColor: "#333"
                }
            },
            layoutAnimation: true,
            textStyle: {
                fontFamily: "sans-serif",
                fontWeight: "bold",
                color: wordColor
            }
        }
    }),
    chartJSCode({
        function wordColor() {
                // Random color
                return 'rgb(' + [
                    Math.round(Math.random() * 160),
                    Math.round(Math.random() * 160),
                    Math.round(Math.random() * 160)
                ].join(',') + ')';
            }
    })
)
```

{{< figure src="../../img/wordcloud.jpg" width="500" >}}
