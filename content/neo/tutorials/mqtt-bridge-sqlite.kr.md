---
title: MQTT와 RDBMS 브리지
type: docs
weight: 300
---

이 튜토리얼은 외부 MQTT 브로커에서 JSON 데이터를 수신해 다른 브리지 데이터베이스에 저장하는 과정을 다룹니다.

**사전 준비**

외부 MQTT 브로커로 `mosquitto`를 사용합니다.
설치가 필요하다면 [공식 홈페이지](https://mosquitto.org)를 참고하십시오.

예시에서는 `mosquitto` 서버가 `127.0.0.1:1883`에서 실행 중이라고 가정합니다.

## TQL 파일 생성

외부 MQTT 브로커에서 들어오는 메시지를 처리할 TQL 파일을 만듭니다.
현재 스크립트는 메시지 페이로드를 받아 버리는 최소한의 동작만 수행합니다.

machbase-neo 웹 UI의 파일 탐색기를 이용해 `/mqtt-bridge.tql` 파일을 생성하고 다음 내용을 입력합니다.

```js
STRING(payload())
DISCARD()
```

{{< figure src="../img/mqtt-sqlite-bridge-tql-1.png" width="600" >}}

## MQTT 브리지 정의

이제 machbase-neo에 MQTT 브리지 "mosquitto"를 등록합니다.

- Name: `mosquitto`
- Type: `MQTT`
- Connection String: `broker=127.0.0.1:1883 cleansession=true`

연결 문자열 옵션에 대한 자세한 내용은 [문서](/neo/bridges/21.mqtt/)를 참고하십시오.

{{< figure src="../img/mqtt-sqlite-bridge-mqtt.png" width="600" >}}

"Test" 버튼을 눌러 연결을 확인합니다. 오류가 발생한다면 연결 문자열을 수정해 성공할 때까지 다시 시도합니다.

{{< figure src="../img/mqtt-sqlite-bridge-mqtt-test.png" width="600" >}}


## MQTT 브리지에 TQL 연결

브리지를 정의하고 테스트한 뒤에는 `mosquitto` 브로커의 특정 토픽에 `mqtt-bridge.tql`을 연결할 수 있습니다.

"Test" 버튼 아래의 "New subscriber"를 클릭해 다음과 같이 설정합니다.

- Name: `mosquitto-sub`
- Topic: `demo/#`
- Destination: "TQL Script"를 선택한 후 방금 만든 TQL 파일을 지정합니다.

{{< figure src="../img/mqtt-sqlite-bridge-sub1.png" width="600" >}}

구독자를 생성하고 상태를 "RUNNING"으로 설정합니다.

{{< figure src="../img/mqtt-sqlite-bridge-sub2.png" width="600" >}}

## 대상 DB 브리지 정의

이제 외부 데이터베이스로 연결할 브리지를 추가합니다. 예시에서는 SQLite를 사용하지만, 다른 데이터베이스도 연결 문자열만 다를 뿐 절차는 유사합니다.

- Name: `destdb`
- Type: `SQLite`
- Connection String `file:///tmp/mqtt.db`

{{< figure src="../img/mqtt-sqlite-bridge-sqlite.png" width="600" >}}

> 수신 데이터를 machbase-neo 내부에만 저장하려면 외부 데이터베이스 브리지를 추가할 필요가 없습니다.

## TQL

이제 mosquitto 브리지가 `demo/#` 토픽에서 메시지를 받을 때마다 실행될 TQL 코드를 작성합니다.

- 2~11행: 이 JSON 문자열은 테스트 실행 시 사용됩니다. 실제 메시지가 없어 `payload()`가 NULL을 반환하면 `??` 연산자가 지정한 JSON 문자열을 대신 사용합니다.
- 13행: `SCRIPT({}, {})`는 자바스크립트를 실행하는 TQL MAP 함수입니다. 자세한 내용은 [문서](/neo/tql/script/)를 참고하십시오.
- 44행: 이 예제에서는 SCRIPT MAP 함수가 모든 작업을 처리하므로 SINK에서 별도 처리가 필요하지 않습니다. TQL은 반드시 SINK 함수로 끝나야 하므로 `DISCARD()`를 사용합니다.

```js {linenos=table,hl_lines=["17-22","33-40"],linenostart=1}
STRING( payload() ?? `
    {
    "timestamp": 1732653071807,
        "message": {
            "totalCar": "1",
            "reason": "test",
            "total": "1",
            "resetTime": "2024-01-01T23:00:00Z",
            "scenario": "Scenario 0"
        }
    }
`)
SCRIPT({
    // Initialization code block:
    // This code block executes once for every new message that arrives,
    // before the first record is passing to the main code block.
    err = $.db({bridge:"destdb"}).exec("CREATE TABLE IF NOT EXISTS DATA ("+
        "TS INTEGER,"+
        "TOTAL_CAR INTEGER,"+
        "REASON TEXT,"+
        "TOTAL INTEGER,"+
        "RESET_TIME DATETIME)");
    if (err instanceof Error) {
        console.error("Fail to create table", err.message);
    }
}, {
    // Main code block:
    // This code block executes for every record.
    // In this example, a message contains only one record.
    //
    // parse json
    obj = JSON.parse($.values[0]);    
    err = $.db({bridge:"destdb"}).exec("INSERT INTO DATA VALUES(?, ?, ?, ?, ?)",
        obj.timestamp,
        parseInt(obj.message.totalCar),
        obj.message.reason,
        parseInt(obj.message.total),
        obj.message.resetTime,
        obj.message.scenario);
    if (err instanceof Error) {
        console.error("Fail to insert into table", err.message);
    }
})
DISCARD()
```


## 데이터 발행

먼저 테스트용 JSON 파일을 준비합니다.

**mqtt-test.json**

```json
{
  "timestamp": 1732653071807,
  "message": {
     "totalCar": "3683",
     "reason": "car",
     "total": "3956",
     "resetTime": "2024-11-25T23:00:00Z",
     "scenario": "Scenario 1"
  }
}
```

이제 `demo/sensor_1` 토픽으로 메시지를 발행합니다. 페이로드로 방금 만든 파일 내용을 사용합니다.

```sh
mosquitto_pub -h 127.0.0.1 -p 1883 \
  -t demo/sensor_1 \
  -f ./mqtt-test.json
```

## 브리지 DB 조회

데이터가 대상 데이터베이스에 저장되었는지 확인합니다. machbase-neo의 SQL 에디터에서 `-- env: bridge=destdb` 주석을 사용하면 브리지 DB에서 직접 쿼리를 실행할 수 있습니다.

```sql
-- env: bridge=destdb
SELECT * FROM DATA;
-- env: reset
```

{{< figure src="../img/mqtt-sqlite-bridge-select.png" width="600" >}}
