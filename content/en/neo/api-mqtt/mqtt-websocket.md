---
title: Websocket and Javascript
type: docs
weight: 63
---

Since machbase-neo v8.0.27, it supports MQTT over websocket.

We will be utilizing the MQTT.js library for our JavaScript client, which can be found at [https://github.com/mqttjs/MQTT.js](https://github.com/mqttjs/MQTT.js).

To include mqtt.js in our project, we can simply embed it from the CDN using the following script tag: `<script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>`.

By default, the web socket address for MQTT is set to `ws://127.0.0.1:5654/web/api/mqtt`, and it is served by the machbase-neo HTTP server.


```html
<html>

<head>
    <script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>
</head>

<body>
    <script type="text/javascript">
        const url = 'ws://localhost:5654/web/api/mqtt'

        // Create an MQTT client instance
        const options = {
            // Clean session
            clean: true,
            connectTimeout: 4000,
            // Authentication
            clientId: 'mqtt_test',
            username: 'mqtt_test',
            password: 'mqtt_test',
        }
        const client = mqtt.connect(url, options)
        client.on('connect', function () {
            console.log('Connected')
            // Subscribe to a 'db/reply' topic to receive the result of our query
            client.subscribe('db/reply', function (err) {
                if (!err) {
                    // Publish a query to a topic 'db/query'
                    const req = '{"q": "SELECT * FROM example limit 10", "format":"box", "precision": 2}'
                    client.publish('db/query', req)
                }
            })
        })

        // Receive messages
        client.on('message', function (topic, message) {
            // display the message we received
            document.getElementById("rspQuery").innerHTML = '<pre>'+message.toString()+'</pre>'
            client.end()
        })

    </script>
    <div id="rspQuery"></div>
</body>

</html>
```