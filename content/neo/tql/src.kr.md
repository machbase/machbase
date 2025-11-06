---
title: SRC
type: docs
weight: 11
---

모든 *tql* 스크립트는 반드시 데이터 소스 함수를 하나 이상 사용해 시작해야 합니다.

SRC 함수는 다양합니다. 예를 들어 `SQL()`은 Machbase Neo 또는 브리지를 통해 연결한 외부 데이터베이스에서 SQL을 실행해 레코드를 생성합니다. `FAKE()`는 가상 데이터를 만들어 주며, `CSV()`는 CSV 파일을 읽고, `BYTES()`는 파일 시스템·HTTP 요청·MQTT 페이로드에서 바이너리 데이터를 수집합니다.

![tql_src](/neo/tql/img/tql_src.jpg)

## SQL()

*구문*: `SQL( [bridge(),] sqltext [, params...])`

- `bridge()` *bridge('name')`: 지정하면 해당 브리지에서 SQL을 실행합니다.
- `sqltext` *string*: 데이터베이스에서 조회할 SQL SELECT 문입니다. 여러 줄을 사용할 때는 백틱(`)을 활용해 주십시오.
- `params`: 바인드 파라미터를 위한 가변 인자입니다.

**예시**

- Machbase 쿼리

```js
SQL (`
    SELECT time, value 
    FROM example 
    WHERE name ='temperature'
    LIMIT 10000
`)
```

- 가변 인자 쿼리

```js
SQL(`SELECT time, value FROM example WHERE name = ? LIMIT ?`,
    param('name') ?? 'temperature',
    param('limit') ?? 10)
```

- 브리지 데이터베이스 쿼리

```js
SQL( bridge('sqlite'), `SELECT * FROM EXAMPLE`)
```

```js
SQL(
    bridge('sqlite'),
    `SELECT time, value FROM example WHERE name = ?`,
    param('name') ?? "temperature")
```

## SQL_SELECT()

*구문*: `SQL_SELECT( fields..., from(), between() [, limit()] )` {{< neo_since ver="8.0.15" />}}

- `fields` *string*: 조회할 컬럼 이름. 여러 컬럼을 지정할 수 있습니다.

*SQL_SELECT()*는 `SQL()`과 동일한 기능을 제공하지만, 원시 SQL 대신 옵션 함수로 조건을 기술해 더 간단히 사용할 수 있습니다. 특히 시간 범위를 손쉽게 지정할 수 있습니다.

아래 예시는 내부적으로 `SELECT time, value FROM example WHERE NAME = 'temperature' AND time BETWEEN ...` 형태의 SQL을 생성합니다.

```js
SQL_SELECT(
    'time', 'value',
    from('example', 'temperature'),
    between('last-10s', 'last')
)
```

위 코드는 다음 SQL과 동일합니다.

```js
SQL(`SELECT
        time, value
    FROM
        EXAMPLE
    WHERE
        name = 'TAG1'
    AND time BETWEEN (
        SELECT MAX_TIME-10000000000
        FROM V$EXAMPLE_STAT
        WHERE name = 'temperature')
    AND (
        SELECT MAX_TIME
        FROM V$EXAMPLE_STAT
        WHERE name = 'temperature')
    LIMIT 0, 1000000
`)
```

### from()

*구문*: `from( table, tag [, time_column [, name_column] ] )`

테이블 이름과 태그 이름을 지정합니다. 내부적으로 `... FROM <table> WHERE NAME = <tag> ...` 조건을 구성합니다.

- `table` *string*: 테이블 이름
- `tag` *string*: 태그 이름
- `time_column` *string*: 시간 컬럼 이름(기본값 `'time'`)
- `name_column` *string*: 태그 컬럼 이름(기본값 `'name'`) {{< neo_since ver="8.0.5" />}}

### between()

*구문*: `between( fromTime, toTime [, period] )`

시간 범위를 지정합니다. 내부적으로 `... WHERE ... TIME BETWEEN <fromTime> AND <toTime> ...` 조건을 구성합니다.

- `fromTime` *string|number*: `'now'`, `'last'` 같은 표현 또는 나노초 단위 Unix epoch 값
- `toTime` *string|number*: 종료 시점
- `period` *string|number*: 구간 길이. 양수만 의미가 있습니다.

예) `'now-1h30m'`은 현재 시각에서 1시간 30분 전을 의미합니다. `'last-30s'`는 최신 시간 기준 30초 전을 의미합니다.

`period`를 지정하면 `GROUP BY time` 구문과 집계 함수를 포함해 SQL을 생성합니다. 이때 `fields` 인자에 기본 시간 컬럼을 포함해야 합니다.

문자열 시간을 사용해야 한다면 `parseTime()`으로 나노초 타임스탬프로 변환해 주십시오. 자세한 정보는 [parseTime()](/neo/tql/utilities/#parsetime) 문서를 참고해 주십시오.

```js
between( parseTime("2023-03-01 14:00:00", "DEFAULT", tz("Local")),
         parseTime("2023-03-01 14:05:00", "DEFAULT", tz("Local")))
```

### limit()

*구문*: `limit( [offset ,] count )`

`SELECT ... LIMIT offset, count` 구문을 생성합니다.

- `offset` *number*: 기본값 `0`
- `count` *number*

## CSV()

*구문*: `CSV( file(file_path_string) | payload() [, charset()] [,field()...[, header()]] )`

CSV를 읽어 키-값 레코드를 생성합니다. 키는 순번이며, CSV 필드가 값이 됩니다. `file()` 인자는 절대 경로를 사용해야 합니다. `payload()`를 사용하면 HTTP POST 본문에서 CSV를 직접 읽어올 수 있어, 원격 클라이언트가 데이터를 전송하면 바로 데이터베이스에 저장하는 API를 만들 때 유용합니다.

- `file() | payload()`: 입력 스트림
- `field(idx, type, name)`: 필드 정의
- `header(bool)`: 첫 줄을 헤더로 처리할지 여부
- `charset(string)`: CSV가 UTF-8이 아닐 때 사용할 문자셋 {{< neo_since ver="8.0.8" />}}
- `logProgress([int])`: `n`행마다 진행 상황을 로그로 출력합니다(기본값 500,000). {{< neo_since ver="8.0.29" />}}

```js
// HTTP 요청 본문에서 CSV 읽기 예시
// 예)
// barn,1677646800,0.03135
// dew_point,1677646800,24.4
// dishwasher,1677646800,3.33e-05
CSV(payload(), 
    field(0, stringType(), 'name'),
    field(1, timeType('s'), 'time'),
    field(2, floatType(), 'value'),
    header(false)
)
APPEND(table('example'))
```

위와 같이 `CSV()`와 `APPEND()`를 조합하면 간단하면서도 유용한 API를 구성할 수 있습니다. 커맨드라인 import보다는 약 5배 느리지만, HTTP 요청당 수천 건 이상의 데이터를 처리할 때는 `INSERT()`보다 빠릅니다.

HTTP POST가 없을 때도 동작하도록 `??` 연산자를 활용할 수 있습니다.

```js
CSV(payload() ?? file('/absolute/path/to/data.csv'),
    field(0, floatType(), 'freq'),
    field(1, floatType(), 'ampl')
)
CHART_LINE()
```

### file()

*구문*: `file(path)`

지정한 경로의 파일을 열어 입력 스트림을 반환합니다. HTTP URL을 지정하면 해당 자원도 가져올 수 있습니다 {{< neo_since ver="8.0.7" />}}.

- `path` *string*: 파일 절대 경로 또는 HTTP/HTTPS URL

```js
CSV( file(`http://127.0.0.1:5654/db/query?`+
        `format=csv&`+
        `q=`+escapeParam(`select * from example limit 10`)
))
CSV() // 또는 JSON()
```

### payload()

*구문*: `payload()`

HTTP POST 또는 MQTT PUBLISH 요청으로 전달된 본문을 입력 스트림으로 반환합니다.

### field()

*구문*: `field(idx, typefunc, name)`

CSV 필드 타입을 지정합니다.

- `idx` *number*: 0부터 시작하는 필드 인덱스
- `typefunc`: 필드 타입을 지정하는 함수
- `name` *string*: 필드 이름

| 타입 함수         | 타입      |
|:------------------|:---------|
| `stringType()`    | string   |
| `doubleType()`    | double   |
| `datetimeType()`  | datetime |
| `boolType()`      | boolean {{< neo_since ver="8.0.20" />}} |
| ~~`floatType()`~~ | *사용 중단, `doubleType()` 사용* {{< neo_since ver="8.0.20" />}} |
| ~~`timeType()`~~  | *사용 중단, `datetimeType()` 사용* {{< neo_since ver="8.0.20" />}} |

`stringType()`, `boolType()`은 인자를 받지 않습니다. `datetimeType()`은 시간 단위나 포맷을 지정할 수 있습니다.

Unix epoch로 시간을 제공한다면 다음과 같이 단위를 지정해 주십시오.

- `datetimeType('s')`
- `datetimeType('ms')`
- `datetimeType('us')`
- `datetimeType('ns')`

사람이 읽을 수 있는 형식이라면 포맷과 타임존을 함께 지정합니다.

- `datetimeType('DEFAULT', 'Local')`

```js
CSV(payload() ??
`name,2006-01-02 15:04:05.999,10`,
field(1, datetimeType('DEFAULT', 'Local'), 'time'))
CSV()
```

- `datetimeType('RFC3339', 'EST')`

```js
CSV(payload() ??
`name,2006-01-02T15:04:05.999Z,10`,
field(1, datetimeType('RFC3339', 'EST'), 'time'))
CSV()
```

타임존을 생략하면 기본값은 `UTC`입니다.

- `datetimeType('RC822')`

첫 번째 인자는 `timeformat()` 함수와 동일한 문법을 사용합니다. 자세한 내용은 [timeformat](../utilities/#timeformat)을 참고해 주십시오.

### charset()

*구문*: `charset(name)` {{< neo_since ver="8.0.8" />}}

- `name` *string*: 문자셋 이름

지원하는 문자셋:

UTF-8, ISO-2022-JP, EUC-KR, SJIS, CP932, SHIFT_JIS, EUC-JP, UTF-16, UTF-16BE, UTF-16LE,
CP437, CP850, CP852, CP855, CP858, CP860, CP862, CP863, CP865, CP866, LATIN-1,
ISO-8859-1, ISO-8859-2, ISO-8859-3, ISO-8859-4, ISO-8859-5, ISO-8859-6, ISO-8859-7,
ISO-8859-8, ISO-8859-10, ISO-8859-13, ISO-8859-14, ISO-8859-15, ISO-8859-16,
KOI8R, KOI8U, MACINTOSH, MACINTOSHCYRILLIC, WINDOWS1250, WINDOWS1251, WINDOWS1252,
WINDOWS1253, WINDOWS1254, WINDOWS1255, WINDOWS1256, WINDOWS1257, WINDOWS1258, WINDOWS874,
XUSERDEFINED, HZ-GB2312

## SCRIPT()

사용자 정의 스크립트 언어를 지원합니다.  
예시는 [SCRIPT](../script/) 문서에서 확인해 주십시오.

## HTTP()

간단한 DSL로 HTTP 요청을 보낼 수 있습니다.  
예시는 [HTTP](../http/) 문서를 참고해 주십시오.

## BYTES(), STRING()

*구문*: `BYTES( src [, separator(char), trimspace(boolean) ] )`

*구문*: `STRING( src [, separator(char), trimspace(boolean) ] )`

- `src`: 데이터 소스. `payload()`, `file()`, 문자열 상수를 사용할 수 있습니다.
- `separator(char)`: 선택 사항. `separator("\n")`처럼 지정하면 줄 단위로 분리합니다.
- `trimspace(boolean)`: 선택 사항. 공백 제거 여부(기본값 `false`)

입력 데이터를 구분자로 분리해 레코드를 생성합니다. 키는 증가하는 정수입니다.

**예시**

- `STRING('A,B,C', separator(","))` → `["A"]`, `["B"]`, `["C"]` 3개 레코드
- `STRING('A,B,C')` → `["A,B,C"]` 1개 레코드

`BYTES()`와 `STRING()`은 반환 타입만 다릅니다. 전자는 바이트 배열, 후자는 문자열을 반환합니다.

```js
STRING(payload() ?? `12345
                    23456
                    78901`, separator("\n"))
```

위 코드는 세 개의 레코드 `["12345"]`, `["          23456"]`, `["          78901"]`를 생성합니다.

```js
STRING(payload() ?? `12345
                    23456
                    78901`, separator("\n"), trimspace(true))
```

공백을 제거하면 `["12345"]`, `["23456"]`, `["78901"]`가 생성됩니다.

```js
STRING( file(`http://example.com/data/words.txt`), separator("\n") )
```

HTTP 주소에서 데이터를 받아오는 예시입니다. `file()`은 HTTP URL을 지원합니다 {{< neo_since ver="8.0.7" />}}.

## ARGS()

*구문*: `ARGS()` {{< neo_since ver="8.0.7" />}}

부모 TQL 플로우에서 전달한 인자를 값으로 갖는 레코드를 생성합니다. 주로 `WHEN...do()` 하위 플로우의 SRC로 사용합니다.

```js {linenos=table,hl_lines=[6],linenostart=1}
FAKE( json({
    [ 1, "hello" ],
    [ 2, "world" ]
}))
WHEN( value(0) == 2, do( value(0), strToUpper(value(1)), {
    ARGS()
    WHEN( true, doLog("OUTPUT:", value(0), value(1)) )
    DISCARD()
}))
CSV()
```

실행하면 콘솔에 아래와 같이 출력됩니다.

```
OUTPUT: 2 WORLD
```

## FAKE()

*구문*: `FAKE( generator )`

- `generator`: `oscillator()`, `meshgrid()`, `linspace()`, `arrange()`, `csv()`, `json()` 중 하나

지정한 제너레이터로 테스트용 데이터를 생성합니다.

### oscillator()

*구문*: `oscillator( freq() [, freq()...], range() )`

주파수와 시간 범위를 지정해 파형 데이터를 생성합니다. `freq()`를 여러 개 지정하면 합성 파형이 만들어집니다.

{{< tabs items="Clean,Add noise">}}
{{< tab >}}
```js {{linenos=table,hl_lines=[1],linenostart=1}}
FAKE( oscillator( freq(3, 1.0), range("now-3s", "3s", "5ms") ))
// | 0        1
// | time     amplitude
MAPVALUE(0, list(value(0), value(1)))
// | 0                  1
// | (time, amplitude)  amplitude
POPVALUE(1)
// | 0
// | (time, amplitude)
CHART(
    chartOption({
        xAxis: { type: "time" },
        yAxis: {},
        series:[ { type: "line", data: column(0) } ]
    })
)
```
{{< /tab >}}
{{< tab >}}
```js {{linenos=table,hl_lines=[4],linenostart=1}}
FAKE( oscillator( freq(3, 1.0), range("now-3s", "3s", "5ms") ))
// | 0        1
// | time     amplitude
MAPVALUE(1, value(1) + (random()-0.5) * 0.2 )
// | 0        1
// | time     amplitude
MAPVALUE(0, list(value(0), value(1)))
// | 0                  1
// | (time, amplitude)  amplitude
POPVALUE(1)
// | 0
// | (time, amplitude)
CHART(
    chartOption({
        xAxis: { type: "time" },
        yAxis: {},
        series:[ { type: "line", data: column(0) } ]
    })
)
```
{{< /tab >}}
{{< /tabs >}}

#### freq()

*구문*: `freq( frequency, amplitude [, bias, phase])`

`amplitude * SIN( 2*Pi * frequency * time + phase) + bias` 형태의 사인파를 생성합니다.

- `frequency` *number*: 헤르츠(Hz) 단위 주파수
- `amplitude` *number*
- `bias` *number*
- `phase` *number*: 라디안 값

#### range()

*구문*: `range( fromTime, duration, period )`

`fromTime`부터 `fromTime + duration`까지의 시간 범위를 정의합니다.

- `fromTime` *string|number*: `'now'`, `'last'` 또는 나노초 단위 epoch 값
- `duration` *string|number*: 지속 시간(예: `'-1d2h30m'`, `'1s100ms'`)
- `period` *string|number*: 샘플 간격. 양수만 의미 있습니다.

### arrange()

*구문*: `arrange(start, stop, step)` {{< neo_since ver="8.0.12" />}}

- `start` *number*
- `stop` *number*
- `step` *number*

```js {{linenos="table",hl_lines=[2]}}
FAKE(
   arrange(1, 2, 0.5)
)
CSV()
```

```csv
1
1.5
2
```

### linspace()

*구문*: `linspace(start, stop, num)`

1차원 등간격 시퀀스를 생성합니다.

{{< tabs items="CSV,CHART">}}
{{< tab >}}
```js {{linenos="table",hl_lines=[2]}}
FAKE(
   linspace(1, 3, 3)
)
CSV()
```

```csv
1
2
3
```
{{< /tab >}}
{{< tab >}}

```js {{linenos="table",hl_lines=[1]}}
FAKE( linspace(0,4*PI,100) )
MAPVALUE(1, sin(value(0)))
MAPVALUE(2, cos(value(0)))
CHART(
  theme("dark"),
  size("600px", "340px"),
  chartOption({
    title: {text: "sin-cos"},
    xAxis:{ data: column(0) },
    yAxis:{},
    series: [
      { name:"SIN", type: "line", data: column(1), 
          markLine:{ data: [{yAxis: 0.5}], label:{show: true, formatter: "half {c} "} } },
      { name:"COS", type: "line", data: column(2) },
    ]
  })
)
```

{{< figure src="/neo/tql/img/linspace_chart.jpg" width="600px" >}}

{{< /tab >}}
{{< /tabs >}}

### meshgrid()

*구문*: `meshgrid(xseries, yseries)`

x축과 y축 값을 조합한 메쉬 데이터를 생성합니다.

{{< tabs items="CSV,CHART">}}
{{< tab >}}
```js {{linenos="table",hl_lines=[2]}}
FAKE(
    meshgrid( linspace(1, 3, 3), linspace(10, 30, 3) )
)
CSV()
```

```csv
1,10
1,20
1,30
2,10
2,20
2,30
3,10
3,20
3,30
```
{{< /tab >}}
{{< tab >}}
```js {{linenos="table",hl_lines=[1]}}
FAKE(meshgrid(linspace(0,2*3.1415,30), linspace(0, 3.1415, 20)))

SET(x, cos(value(0))*sin(value(1)))
SET(y, sin(value(0))*sin(value(1)))
SET(z, cos(value(1)))
MAPVALUE(0, list($x, $y, $z))
POPVALUE(1)

CHART(
  plugins("gl"),
  size("600px", "600px"),
  chartOption({
    grid3D:{},
    xAxis3D:{}, yAxis3D:{}, zAxis3D:{},
    visualMap:[{ 
      min:-1, max:1, 
      inRange:{color:["#313695",  "#74add1", "#ffffbf","#f46d43", "#a50026"]
    }}],
    series:[
      { type:"scatter3D", data: column(0)}
    ]
  })
)
```

{{< figure src="/neo/tql/img/meshgrid_chart.jpg" width="350px" >}}

{{< /tab >}}
{{< /tabs >}}

### csv()

*구문*: `csv(content)` {{< neo_since ver="8.0.7" />}}

- `content` *string*: CSV 문자열

지정한 CSV 내용을 레코드로 변환합니다.

```js {{linenos="table",hl_lines=["2-6"]}}
FAKE(
    csv( strTrimSpace(`
        A,1,true
        B,2,false
        C,3,true
    `))
)
MAPVALUE(0, strTrimSpace(value(0)))
MAPVALUE(1, parseFloat(value(1))*10)
MAPVALUE(2, parseBool(value(2)))
CSV()
```

```csv
A,10,true
B,20,false
C,30,true
```

### json()

*구문*: `json({...})` {{< neo_since ver="8.0.7" />}}

여러 JSON 배열을 레코드로 변환합니다.

```js {{linenos="table",hl_lines=["2-6"]}}
FAKE(
    json({
        ["A", 1, true],
        ["B", 2, false],
        ["C", 3, true]
    })
)
MAPVALUE(1, value(1)*10)
CSV()
```

```csv
A,10,true
B,20,false
C,30,true
```
