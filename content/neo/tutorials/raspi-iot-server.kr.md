---
title: Raspberry PI IoT 서버
type: docs
weight: 200
---

이 튜토리얼에서는 Raspberry PI에 machbase-neo를 설치하고 센서 데이터를 수집·조회하는 과정을 안내합니다.

## DHT11 센서를 Raspberry PI에 연결하기

DHT11 센서를 GPIO에 연결하기 전에 Raspberry PI의 전원을 반드시 꺼 주십시오.

![gpio](/images/raspi4-gpio.jpg)

DHT11에는 VCC, DAT, GND 3개의 핀이 있으며 각각 GPIO 2, 3, 6에 연결합니다.

![dht11](/images/dht11.png)



## 센서 데이터 읽기

- Raspberry PI 4 Model B (본 튜토리얼에서는 4GB 메모리 모델 사용)
- Adafruit_DHT 11 (센서)

센서 데이터를 읽기 위해 `Adafruit_DHT` 파이썬 모듈을 설치합니다.

```sh
pip3 install Adafruit_DHT
```

아래 코드는 DHT11 센서의 DATA 핀과 연결된 GPIO 2(`pinnum = 2`)에서 값을 읽습니다.
1초마다 표준 출력으로 `name, timestamp, value` 형식의 데이터를 내보내며,
machbase-neo가 나노초 단위 타임스탬프를 처리할 수 있도록 1000000000을 곱해 값을 생성합니다.

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

소스를 `dht.py`로 저장한 뒤 실행해 결과를 확인합니다.

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

## machbase-neo 설치

- SSH 또는 콘솔로 PI에 접속합니다.

```
$ ssh -l pi <ip address>
```

- `demo` 디렉터리를 생성합니다.

```sh
mkdir demo && cd demo
```

- machbase-neo를 다운로드합니다.

```sh
sh -c "$(curl -fsSL https://docs.machbase.com/install.sh)"
```

- 압축을 해제합니다.

```sh
$ unzip machbase-neo-{{ site.latest_version }}-linux-arm64.zip
$ cd machbase-neo-{{ site.latest_version }}-linux-arm64
```

- machbase-neo를 실행합니다.

```sh
./machbase-neo serve
```

![img](/images/raspi-install.gif)


종료할 때는 `Ctrl+C`를 누르십시오.

## machbase-neo 네트워크 설정

### 외부 접속을 위한 IP 바인딩

기본 설정에서는 machbase-neo가 localhost(`127.0.0.1`)에서만 대기합니다.
노트북이나 다른 애플리케이션 서버에서 HTTP 등으로 접속하려면 `--host <bind_ip_addr>` 옵션으로 호스트 IP를 바인딩해야 합니다.

```sh
./machbase-neo serve --host 0.0.0.0
```

## 데이터 저장

### `example` 테이블 생성

`machbase-neo serve`가 실행 중인 상태에서 아래 명령으로 `example` 테이블을 생성합니다.

```
./machbase-neo shell "create tag table if not exists EXAMPLE (name varchar(100) primary key, time datetime basetime, value double)"
```

### machbase-neo에 데이터 쓰기

`dht.py`를 실행하고 출력 결과를 `machbase-neo shell import`에 파이프합니다.
`import` 명령은 기본적으로 CSV 포맷을 받아들이며, EOF를 만날 때까지 행 단위로 지정한 테이블(여기서는 `example`)에 쌓습니다.

```sh
python dht.py | ./machbase-neo shell import example
```

파이프로 표준 출력을 넘겼기 때문에 별도의 출력 메시지는 표시되지 않습니다.

## machbase-neo에서 데이터 읽기

### 최근 저장된 데이터 확인

데이터를 쓰는 중에 다른 터미널을 열어 SQL을 실행하면 최신 데이터를 확인할 수 있습니다.
`--tz local` 옵션은 TIME 필드를 UTC 대신 로컬 시간대로 표시합니다.

```
./machbase-neo shell walk --tz local 'select * from example order by time desc'
```

`r` 키를 누르면 쿼리를 다시 실행해 최신 데이터를 갱신합니다.

![walk](/images/raspi-walk.gif)


### 애플리케이션에서 데이터 조회

machbase-neo는 저장된 데이터를 조회할 수 있는 HTTP API를 제공하므로 아래와 같이 SQL을 포함한 HTTP 요청으로 손쉽게 데이터를 가져올 수 있습니다.

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
