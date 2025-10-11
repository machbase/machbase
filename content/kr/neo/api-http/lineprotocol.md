---
title: ILP 라인 프로토콜
type: docs
weight: 50
---

Machbase Neo는 데이터를 적재하기 위해 InfluxData 라인 프로토콜 형식의 메시지를 수신하는 호환 API를 제공합니다.
이를 통해 telegraf 같은 라인 프로토콜 메시지를 생성하는 기존 클라이언트 소프트웨어를 그대로 활용할 수 있습니다.

{{< callout emoji="📢">}}
Machbase는 influxdb와 스키마가 다르기 때문에 일부 항목은 자동으로 변환됩니다.
{{< /callout >}}

**변환 규칙**

| Machbase            | line protocol of influxdb                   |
| ------------------- | ------------------------------------------- |
| table               | db                                          |
| tag name            | measurement + `.` + field name              |
| time                | timestamp                                   |
| value               | 필드 값(숫자 타입이 아니면 무시되어 적재되지 않습니다) |

**라인 프로토콜 예시**

{{< tabs items="HTTP,cURL">}}
{{< tab >}}
~~~
```http
POST http://127.0.0.1:5654/metrics/write?db=tagdata

my-car speed=87.6 167038034500000
```
~~~
{{< /tab >}}
{{< tab >}}
```sh
curl -o - -X POST "http://127.0.0.1:5654/metrics/write?db=tagdata" \
    --data-binary 'my-car speed=87.6 167038034500000'
```
{{< /tab >}}
{{< /tabs >}}

위 예시는 `name`=`my-car.speed`, `value`=87.6, `time`=167038034500000 값을 `tagdata` 테이블에 삽입합니다.

**telegraf.conf 예시**

telegraf의 출력 설정을 Machbase Neo의 HTTP 포트로 지정하면,
수집된 메트릭이 바로 Machbase Neo에 입력됩니다.

```
[[outputs.http]]
url = "http://127.0.0.1:5654/metrics/write?db=tagdata"
data_format = "influx"
content_encoding = "gzip"
```
