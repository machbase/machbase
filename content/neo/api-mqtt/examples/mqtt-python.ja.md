---
toc: true
title: Python クライアント
type: docs
weight: 65
---

## 準備 {#준비}

### pahoのインストール {#paho-설치}

```sh
pip install paho-mqtt
```

### プロジェクトディレクトリの作成 {#프로젝트-디렉터리-생성}

```sh
mkdir python-mqtt && cd python-mqtt
```

## パブリッシャー {#퍼블리셔}

### クライアント {#클라이언트}

```python
import paho.mqtt.client as mqtt

mqttClient = mqtt.Client("python_pub") # パブリッシャー名
```

### 接続コールバック {#연결-콜백}

```python
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("CONNACK OK")
    else:
        print("CONNACK KO code=", rc)
```

### 接続（TLSなし） {#연결-비-tls}

MQTTの平文ソケットでmachbase-neoに接続します。

```python
mqttClient = mqtt.Client("python_pub", clean_session=True)
mqttClient.on_connect = on_connect
mqttClient.connect("127.0.0.1", port=5653, keepalive=10, clean_session=True)
mqttClient.loop_start()
```

### 切断 {#연결-종료}

```python
mqttClient.disconnect()
mqttClient.loop_stop()
```

### 発行コールバック {#발행-콜백}

```python
def on_publish(client, userdata, mid):
    print("PUBACK mid=",mid)
```

### 発行 {#발행}

```python
mqttClient.on_publish = on_publish

mqttClient.publish("db/append/example", """[
    ["temperature",1677033057000000000, 21.1],
    ["humidity",   1677033057000000000, 0.53]
]""", qos=1)
```

## ソースコード全体 {#전체-소스-코드}


```python
import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("CONNACK OK")
    else:
        print("CONNACK KO code:", rc)

def on_publish(client, userdata, mid):
    print("PUBACK mid:",mid)

mqttClient = mqtt.Client("python_pub", clean_session=True)
mqttClient.on_connect = on_connect
mqttClient.on_publish = on_publish
mqttClient.connect("127.0.0.1", port=5653, keepalive=10)
mqttClient.loop_start()

mqttClient.publish("db/append/example", """[
    ["temperature",1677033057000000000, 21.1],
    ["humidity",   1677033057000000000, 0.53]
]""", qos=1)

time.sleep(1)

mqttClient.disconnect()
mqttClient.loop_stop()
```
