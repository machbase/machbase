---
toc: true
title: Raspberry PIのIoTサーバー
type: docs
weight: 200
---

このチュートリアルでは、Raspberry PIにmachbase-neoをインストールし、センサーデータを収集・検索する手順を説明します。

## DHT11センサーとRaspberry PIの接続 {#dht11-센서를-raspberry-pi에-연결하기}

DHT11センサーをGPIOに接続する前に、必ずRaspberry PIの電源を切ってください。

![gpio](/images/raspi4-gpio.jpg)

DHT11にはVCC、DAT、GNDの3本のピンがあり、それぞれGPIOヘッダーの物理ピン2、3、6に接続します。物理ピン3がGPIO 2です。

![dht11](/images/dht11.png)



## センサーデータの読み取り {#센서-데이터-읽기}

- Raspberry PI 4 Model B（このチュートリアルではメモリ4GBモデルを使用）
- Adafruit_DHT 11（センサー）

センサーデータを読み取るために、Pythonモジュール`Adafruit_DHT`をインストールします。

```sh
pip3 install Adafruit_DHT
```

以下のコードは、DHT11センサーのDATAピンに接続したGPIO 2（`pinnum = 2`）から値を読み取ります。
1秒ごとに標準出力へ`name, timestamp, value`形式のデータを出力します。
machbase-neoがナノ秒単位のタイムスタンプを処理できるように、1000000000を掛けた値を生成します。

```py
import Adafruit_DHT
from time import time
from time import sleep

pinnum = 2
sensor = Adafruit_DHT.DHT11
while (True):
    hum, temp = Adafruit_DHT.read_retry(sensor,pinnum)
    ts_ns = int(time() * 1000000000)
    if hum is not None and temp is not None:
        print(f'temperature,{ts_ns},{temp}')
        print(f'humidity,{ts_ns},{hum}')
        sleep(1)
```

ソースを`dht.py`として保存し、実行して結果を確認します。

```sh
$ python dht.py
temperature,1676008535430951936,28.0
humidity,1676008535430951936,33.0
temperature,1676008536956561152,28.0
humidity,1676008536956561152,33.0
temperature,1676008538482078464,28.0
humidity,1676008538482078464,33.0
temperature,1676008540007633664,28.0
humidity,1676008540007633664,33.0
^C
```

## machbase-neoのインストール {#machbase-neo-설치}

- SSHまたはコンソールでPIに接続します。

```
$ ssh -l pi <ip address>
```

- `demo`ディレクトリを作成します。

```sh
mkdir demo && cd demo
```

- machbase-neoをダウンロードします。

```sh
sh -c "$(curl -fsSL https://docs.machbase.com/install.sh)"
```

- アーカイブを展開します。

```sh
$ unzip machbase-neo-{{ site.latest_version }}-linux-arm64.zip
$ cd machbase-neo-{{ site.latest_version }}-linux-arm64
```

- machbase-neoを起動します。

```sh
./machbase-neo serve
```

![img](/images/raspi-install.gif)


停止するには`Ctrl+C`を押します。

## machbase-neoのネットワーク設定 {#machbase-neo-네트워크-설정}

### 外部接続用のIPバインド {#외부-접속을-위한-ip-바인딩}

既定の設定では、machbase-neoはlocalhost（`127.0.0.1`）でのみ待ち受けます。
ノートPCや他のアプリケーションサーバーからHTTPなどで接続するには、`--host <bind_ip_addr>`オプションでホストIPをバインドする必要があります。

```sh
./machbase-neo serve --host 0.0.0.0
```

## データの保存 {#데이터-저장}

### `example`テーブルの作成 {#example-테이블-생성}

`machbase-neo serve`の実行中に、以下のコマンドで`example`テーブルを作成します。

```
./machbase-neo shell "create tag table if not exists EXAMPLE (name varchar(100) primary key, time datetime basetime, value double)"
```

### machbase-neoへのデータ書き込み {#machbase-neo에-데이터-쓰기}

`dht.py`を実行し、出力を`machbase-neo shell import`にパイプで渡します。
`import`コマンドは既定でCSV形式を受け取り、EOFに達するまで、指定したテーブル（ここでは`example`）に1行ずつ取り込みます。

```sh
python dht.py | ./machbase-neo shell import example
```

標準出力をパイプで渡しているため、出力メッセージは表示されません。

## machbase-neoからのデータ読み取り {#machbase-neo에서-데이터-읽기}

### 直近に保存したデータの確認 {#최근-저장된-데이터-확인}

書き込み中に別のターミナルを開いてSQLを実行すると、最新のデータを確認できます。
`--tz local`オプションは、TIMEフィールドをUTCではなくローカルタイムゾーンで表示します。

```
./machbase-neo shell walk --tz local 'select * from example order by time desc'
```

`r`キーを押すと、クエリを再実行して最新のデータに更新します。

![walk](/images/raspi-walk.gif)


### アプリケーションからのデータ検索 {#애플리케이션에서-데이터-조회}

machbase-neoは保存したデータを検索するHTTP APIを提供しているため、以下のようにSQLを含むHTTPリクエストで容易にデータを取得できます。

```py
from urllib import parse
import pandas as pd
query_param = parse.urlencode({
    "q":"select * from example order by time limit 500",
    "format": "csv",
})
df = pd.read_csv(f"http://192.168.1.214:5654/db/query?{query_param}")
df
```

![query](/images/raspi-query.jpg)
