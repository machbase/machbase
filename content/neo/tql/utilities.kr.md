---
title: 유틸리티 함수
type: docs
weight: 41
---

유틸리티 함수는 여러 함수의 인수로 공통적으로 활용할 수 있는 보조 기능을 제공합니다.

## 상수

| 상수   | 설명                     |
|:-------|:-------------------------|
| `NULL` | null 값                  |
| `PI`   | 원주율(3.141592...) [참고](https://oeis.org/A000796) |

## 컨텍스트

### key()

*구문*: `key()`

현재 레코드의 키를 반환합니다.

### value()

*구문*: `value( [index] )`

- `index` *integer* (선택) 값 배열의 인덱스

현재 레코드의 값 전체를 배열로 반환합니다.
인덱스를 지정하면 해당 위치의 요소를 반환합니다.

예를 들어 현재 값이 `[0, true, "hello", "world"]`이면 다음과 같습니다.

- `value()`는 값 배열 전체인 `[0, true, "hello", "world"]`를 반환합니다.
- `value(0)`은 첫 번째 요소인 `0`을 반환합니다.
- `value(3)`은 마지막 요소인 `"world"`를 반환합니다.

### payload()

*구문*: `payload()`

*tql* 스크립트를 호출한 측에서 보낸 현재 입력 스트림을 반환합니다.
*tql* 스크립트를 HTTP로 호출하면 `payload()`는 POST 요청 본문의 스트림을 반환합니다.
*tql* 스크립트를 MQTT로 호출하면 `payload()`는 PUBLISH 메시지의 페이로드를 반환합니다.

### param()

*구문*: `param( name )`

- `name` *string* 쿼리 파라미터 이름

*tql* 스크립트를 HTTP로 호출한 경우 `param()` 함수로 요청에 포함된 쿼리 파라미터를 조회할 수 있습니다.

### context()

*구문*: `context()`

스크립트 런타임의 컨텍스트 객체를 반환합니다.

## 문자열 함수

### escapeParam()

*구문*: `escapeParam( str ) : string` {{< neo_since ver="8.0.7" />}}

`escapeParam()`은 문자열을 URL 쿼리에 안전하게 넣을 수 있도록 이스케이프합니다.

```js {linenos=table,hl_lines=["3"],linenostart=1}
CSV(
    file(`http://127.0.0.1:5654/db/query?format=csv&q=`+
        escapeParam(`select count(*) from example`)
    )
)
CSV()
```

### strTrimSpace()

*구문*: `strTrimSpace(str) : string` {{< neo_since ver="8.0.7" />}}

`strTrimSpace`는 문자열 str의 앞뒤 공백을 모두 제거한 문자열을 반환합니다.

### strTrimPrefix()

*구문*: `strTrimPrefix(str, prefix) : string` {{< neo_since ver="8.0.7" />}}

`strTrimPrefix`는 str의 앞부분에서 prefix를 제거한 문자열을 반환합니다. str이 prefix로 시작하지 않으면 str을 그대로 반환합니다.

### strTrimSuffix()

*구문*: `strTrimSuffix(str, suffix) : string` {{< neo_since ver="8.0.7" />}}

`strTrimSuffix`는 str의 끝부분에서 suffix를 제거한 문자열을 반환합니다. str이 suffix로 끝나지 않으면 str을 그대로 반환합니다.

### strHasPrefix()

*구문*: `strHasPrefix(str, prefix) : boolean` {{< neo_since ver="8.0.7" />}}

`strHasPrefix`는 문자열 str이 prefix로 시작하는지 확인합니다.

### strHasSuffix()

*구문*: `strHasSuffix(str, suffix) : boolean` {{< neo_since ver="8.0.7" />}}

`strHasSuffix`는 문자열 str이 suffix로 끝나는지 확인합니다.

### strReplaceAll()

*구문*: `strReplaceAll(str, old, new) : string` {{< neo_since ver="8.0.7" />}}

`strReplaceAll`은 문자열 str에서 서로 겹치지 않는 모든 old를 new로 바꾼 사본을 반환합니다.
old가 빈 문자열이면 문자열의 시작 위치와 각 UTF-8 시퀀스 바로 뒤에서 일치하므로, 룬 k개로 이루어진 문자열에서는 최대 k+1번 교체합니다.

### strReplace()

*구문*: `strReplace(str, old, new, n) : string` {{< neo_since ver="8.0.7" />}}

- `str` *string*
- `old` *string*
- `new` *string*
- `n` *integer*

`strReplace`는 문자열 str에서 서로 겹치지 않는 old를 앞에서부터 n개까지 new로 바꾼 사본을 반환합니다.
old가 빈 문자열이면 문자열의 시작 위치와 각 UTF-8 시퀀스 바로 뒤에서 일치하므로, 룬 k개로 이루어진 문자열에서는 최대 k+1번 교체합니다.
n이 0보다 작으면 교체 횟수에 제한이 없습니다.

### strSub()

*구문*: `strSub(str, offset [, count]) : string` {{< neo_since ver="8.0.7" />}}

`strSub`는 str의 부분 문자열을 반환합니다.

### strIndex()

*구문*: `strIndex(str, substr) : number` {{< neo_since ver="8.0.15" />}}

str에서 substr이 처음 나타나는 인덱스를 반환합니다. str에 substr이 없으면 -1을 반환합니다.

### strLastIndex()

*구문*: `strLastIndex(str, substr) : number` {{< neo_since ver="8.0.15" />}}

str에서 substr이 마지막으로 나타나는 인덱스를 반환합니다. str에 substr이 없으면 -1을 반환합니다.

### strToUpper()

*구문*: `strToUpper(str) : string` {{< neo_since ver="8.0.7" />}}

`strToUpper`는 str의 모든 유니코드 문자를 대문자로 바꿔 반환합니다.

### strToLower()

*구문*: `strToLower(str) : string` {{< neo_since ver="8.0.7" />}}

`strToLower`는 str의 모든 유니코드 문자를 소문자로 바꿔 반환합니다.

### strSprintf()

*구문*: `strSprintf(fmt, args...) : string` {{< neo_since ver="8.0.7" />}}

`strSprintf()`는 포맷 지정자에 따라 문자열을 만들어 반환합니다(Go의 `fmt.Sprintf`와 유사).

포맷 문자열 `fmt`의 구문은 `%[flags][width][.precision]verb`입니다.

마지막에 오는 verb는 대응하는 인수의 타입과 해석 방법을 정합니다.

| verb  | 설명            |
| :---- | :-------------- |
| f     | 10진 부동소수점, 소문자 |
| F     | 10진 부동소수점, 대문자 |
| e     | 지수 표기(가수/지수), 소문자 |
| E     | 지수 표기(가수/지수), 대문자 |
| g     | %e와 %f 중 더 짧은 표현 |
| G     | %E와 %F 중 더 짧은 표현 |
| q     | 따옴표로 감싼 문자열 |
| t     | true 또는 false |
| s     | 문자열 |
| v     | 기본 형식 |
| %%    | % 문자 하나 |

```js {linenos=table,hl_lines=["3"],linenostart=1}
FAKE( csv(`world,3.141792`) )
MAPVALUE(1, parseFloat(value(1)))
MAPVALUE(2, strSprintf(`hello %s? %1.2f`, value(0), value(1)))
CSV()
```

```csv
world,3.141792,hello world? 3.14
```

### strTime()

*구문*: `strTime(time, format [, tz]) : string` {{< neo_since ver="8.0.7" />}}

- `time` *time*
- `format` *string*|*sqlTimeformat()*
- `tz` *tz()* (선택) 시간대, 생략하면 기본값은 `tz('UTC')`입니다.

`strTime()`은 시간 값을 지정한 형식과 시간대에 맞춰 문자열로 변환합니다.

```js
MAPVALUE(0, strTime(time("now"), "2006/01/02 15:04:05.999", tz("UTC")), "result")
```

**숫자 형식 timeformat**

```js {linenos=table,hl_lines=["2"],linenostart=1}
FAKE( linspace(0, 1, 1))
MAPVALUE(0, strTime(time("now"), "2006/01/02 15:04:05.999", tz("UTC")), "result")
MARKDOWN(rownum(true))
```

**sqlTimeformat()**

```js {linenos=table,hl_lines=["2"],linenostart=1}
FAKE( linspace(0, 1, 1))
MAPVALUE(0, strTime(time("now"), sqlTimeformat("YYYY/MM/DD HH24:MI:SS.nnn"), tz("UTC")), "result")
MARKDOWN(rownum(true))
```

|ROWNUM|result|
|:-----|:-----|
|1|2024/01/10 07:27:29.667|

**이름으로 지정하는 timeformat**

{{< neo_since ver="8.0.12" />}}

```js {linenos=table,hl_lines=["2"],linenostart=1}
FAKE( linspace(0, 1, 1))
MAPVALUE(0, strTime(time("now"), "RFC822", tz("UTC")), "time")
MARKDOWN(rownum(true))
```

|ROWNUM|time|
|:-----|:-----|
|1|10 Jan 24 07:23 UTC|


### parseFloat()

*구문*: `parseFloat( str )  : number` {{< neo_since ver="8.0.7" />}}

- `str` *string*

`str`을 부동소수점 숫자로 변환합니다.

{{< tabs >}}
{{< tab name="CODE" >}}
```js {linenos=table,hl_lines=["2"],linenostart=1}
FAKE( csv(`world,3.141792`) )
MAPVALUE(1, parseFloat(value(1)))
JSON()
```
{{< /tab >}}
{{< tab name="RESULT" >}}
```json
{
    "data": {
        "columns": [ "column0", "column1" ],
        "types": [ "string", "string" ],
        "rows": [ [ "world", 3.141792 ] ]
    },
    "success": true,
    "reason": "success",
    "elapse": "140.125µs"
}
```
{{< /tab >}}
{{< /tabs >}}

### parseBool()

*구문*: `parseBool( str ) : boolean` {{< neo_since ver="8.0.7" />}}

- `str` *string*

허용되는 문자열 "1", "t", "T", "TRUE", "true", "True", "0", "f", "F", "FALSE", "false", "False" 중 하나를 받아
대응하는 불리언 값 true 또는 false로 변환합니다. 그 밖의 문자열이면 오류를 반환합니다.

{{< tabs >}}
{{< tab name="CODE" >}}
```js {linenos=table,hl_lines=["2"],linenostart=1}
FAKE( csv(`world,True`) )
MAPVALUE(1, parseBool(value(1)))
JSON()
```
{{< /tab >}}
{{< tab name="RESULT" >}}
```json
{
    "data": {
        "columns": [ "column0", "column1" ],
        "types": [ "string", "string" ],
        "rows": [ [ "world", true ] ]
    },
    "success": true,
    "reason": "success",
    "elapse": "122.667µs"
}
```
{{< /tab >}}
{{< /tabs >}}

## 문자열 매칭

### glob()

*구문*: `glob(pattern, text) : boolean` {{< neo_since ver="8.0.7" />}}

`glob`은 `text`가 `pattern`과 일치하면 true를 반환합니다.

```js {linenos=table,hl_lines=["3"],linenostart=1}
FAKE( linspace(1, 4, 4))
PUSHVALUE(0, "map."+value(0))
WHEN( glob("*.3", value(0)), doLog("found", value(1)))
CSV()
```

### regexp()

*구문*: `regexp(expression, text) : boolean` {{< neo_since ver="8.0.7" />}}

`regexp`는 `text`가 정규 표현식 `expression`과 일치하면 true를 반환합니다.

```js {linenos=table,hl_lines=["3"],linenostart=1}
FAKE( linspace(1, 4, 4))
PUSHVALUE(0, "map."+value(0))
WHEN( regexp(`^map\.[2,3]$`, value(0)), doLog("found", value(1)))
CSV()
```

## 시간 함수

### time()

*구문*: `time( number|string ) : time`

- `time('now')`는 현재 시각을 반환합니다.
- `time('now -10s50ms')`는 현재보다 10.05초 이전 시각을 반환합니다.
- `time(1672531200*1000000000)`은 2023년 1월 1일 오전 0시 0분 0초 시각을 반환합니다.

{{< tabs >}}
{{< tab name="time('now')" >}}
```js {linenos=table}
SQL(`select to_char(time), value from example where time < ?`, time('now'))
CSV()
```
{{< /tab >}}
{{< tab name="time(epoch)" >}}
```js
SQL(`select to_char(time), value from example where time = ?`, time(1628737200123456789))
CSV()
```
{{< /tab >}}
{{< /tabs >}}

### timeYear()

*구문*: `timeYear( time [, timezone] ) : number`  {{< neo_since ver="8.0.15" />}}

timeYear()는 *time*의 연도를 반환합니다.

### timeMonth()

*구문*: `timeMonth( time [, timezone] ) : number`  {{< neo_since ver="8.0.15" />}}

timeMonth()는 *time*의 월을 반환합니다.

### timeDay()

*구문*: `timeDay( time [, timezone] ) : number`  {{< neo_since ver="8.0.15" />}}

timeDay()는 *time*의 일(그달의 날짜)을 반환합니다.

### timeHour()

*구문*: `timeHour( time [, timezone] ) : number`  {{< neo_since ver="8.0.15" />}}

timeHour()는 *time*의 시를 [0, 23] 범위로 반환합니다.

### timeMinute()

*구문*: `timeMinute( time [, timezone] ) : number`  {{< neo_since ver="8.0.15" />}}

timeMinute()는 *time*의 분을 [0, 59] 범위로 반환합니다.

### timeSecond()

*구문*: `timeSecond( time ) : number`  {{< neo_since ver="8.0.15" />}}

timeSecond()는 *time*의 초를 [0, 59] 범위로 반환합니다.

### timeNanosecond()

*구문*: `timeNanosecond( time ) : number`  {{< neo_since ver="8.0.15" />}}

timeNanosecond()는 *time*의 초 미만 부분을 나노초 단위로 [0, 999999999] 범위에서 반환합니다.

### timeISOYear()

*구문*: `timeISOYear( time [, timezone] ) : number`  {{< neo_since ver="8.0.15" />}}

timeISOYear()는 *time*이 속한 ISO 8601 연도를 반환합니다.

### timeISOWeek()

*구문*: `timeISOWeek( time [, timezone] ) : number`  {{< neo_since ver="8.0.15" />}}

timeISOWeek()는 *time*이 속한 ISO 8601 주차를 반환합니다.
주차는 1부터 53까지입니다. n년 1월 1일부터 3일까지는 n-1년의 52주차나 53주차에, 12월 29일부터 31일까지는 n+1년의 1주차에 속할 수 있습니다.

한 해의 첫 번째 주는 그해의 첫 번째 목요일이 들어 있는 주이고, 마지막 주는 다음 해 첫 번째 주의 바로 앞 주입니다.
자세한 내용은 https://www.iso.org/obp/ui#iso:std:iso:8601:-1:ed-1:v1:en:term:3.1.1.23 을 참고해 주십시오.

### timeYearDay()

*구문*: `timeYearDay( time [, timezone] ) : number`  {{< neo_since ver="8.0.15" />}}

timeYearDay()는 *time*이 그해의 몇 번째 날인지 반환합니다. 평년은 [1,365], 윤년은 [1,366] 범위입니다.

### timeWeekDay()

*구문*: `timeWeekDay( time [, timezone] ) : number`  {{< neo_since ver="8.0.15" />}}

timeWeekDay()는 *time*의 요일을 반환합니다(일요일 = 0, ...).

```js {{linenos=table,hl_lines=[3]}}
FAKE(arrange(1, 7, 1))
MAPVALUE(0, time(strSprintf("now - %.fd",value(0))))
GROUP( lazy(true), by(timeWeekDay(value(0))), count(value(0)) )
CSV()
```

### timeUnix()

*구문*: `timeUnix( time ) : number` {{< neo_since ver="8.0.13" />}}

*timeUnix*는 `time`을 Unix 시간, 즉 1970년 1월 1일 UTC부터 경과한 초 수로 반환합니다. 결과는 `time`에 연결된 시간대와 관계없이 같습니다.

### timeUnixMilli()

*구문*: `timeUnixMilli( time ) : number` {{< neo_since ver="8.0.13" />}}

*timeUnixMilli*는 `time`을 Unix 시간, 즉 1970년 1월 1일 UTC부터 경과한 밀리초 수로 반환합니다. 결과는 `time`에 연결된 시간대와 관계없이 같습니다.

### timeUnixMicro()

*구문*: `timeUnixMicro( time ) : number` {{< neo_since ver="8.0.13" />}}

*timeUnixMicro*는 `time`을 Unix 시간, 즉 1970년 1월 1일 UTC부터 경과한 마이크로초 수로 반환합니다. 결과는 `time`에 연결된 시간대와 관계없이 같습니다.

### timeUnixNano()

*구문*: `timeUnixNano( time ) : number` {{< neo_since ver="8.0.13" />}}

*timeUnixNano*는 `time`을 Unix 시간, 즉 1970년 1월 1일 UTC부터 경과한 나노초 수로 반환합니다. 결과는 `time`에 연결된 시간대와 관계없이 같습니다.

### timeAdd()

*구문*: `timeAdd( number|string|time [, timeExpression] ) : time`

*예*

- `timeAdd('now', 0)`은 현재 시각을 반환합니다.
- `timeAdd('now', '-10s50ms')`는 현재보다 10.05초 이전 시각을 반환합니다.
- `timeAdd(value(0), '1m')`은 value(0)이 time 값이면 value(0)보다 1분 뒤의 시각을 반환합니다.

{{< tabs >}}
{{< tab name="timeAdd('now')" >}}
```js {linenos=table}
SQL(`select to_char(time), value from example where time < ?`, timeAdd('now', '-10s'))
CSV()
```
{{< /tab >}}
{{< tab name="timeAdd(epoch)" >}}
```js
SQL(`select to_char(time), value from example where time = ?`, timeAdd(1628737200123456789, '-5s'))
CSV()
```
{{< /tab >}}
{{< /tabs >}}

### roundTime()

*구문*: `roundTime( time, duration ) : time`

Unix epoch부터 경과한 시간이 `duration`의 정수배가 되도록 시각을 내림합니다. `duration`에는 `1h`, `1s` 같은 단위를 지정합니다.

*예*

- `roundTime(time('now'), '1h')`
- `roundTime(value(0), '1s')`

### parseTime()

*구문*: `parseTime( time, format [, timezone] ) : time`

- `time` *string* 시간 표현
- `format` *string* 시간 형식 표현. `"DEFAULT"`, `"RFC3339"` 같은 미리 정의된 이름이나 `sqlTimeformat()` 등을 사용할 수 있습니다.
- `timezone` *tz* 시간대. `tz()`로 원하는 지역을 지정하며, 생략하면 기본값은 `tz("UTC")`입니다.

*예*

- `parseTime("2023-03-01 14:01:02", "DEFAULT", tz("Asia/Tokyo"))`
- `parseTime("2023-03-01 14:01:02", "DEFAULT", tz("local"))`

### tz()

*구문*: `tz( name ) : timeZone`

지정한 이름에 해당하는 시간대를 반환합니다.

*예*
- `tz('local')`
- `tz('UTC')`
- `tz('EST')`
- `tz("Europe/Paris")`

<a id="timeformat-sqltimeformat-ansitimeformat"></a>

### timeformat()

*구문*: `timeformat( format )`

- `format` *string*

```js {linenos=table,hl_lines=["6"],linenostart=1}
FAKE( json({
    [ 1701345032123456789, 10],
    [ 1701345043219876543, 11]
}))
MAPVALUE(0, time(value(0)) )
CSV(timeformat("DEFAULT"), tz("Asia/Seoul"))
```

```
2023-11-30 20:50:32.123,10
2023-11-30 20:50:43.219,11
```

| format         | 출력 형식                                         |
|:---------------|:------------------------------------------------- |
| DEFAULT        | 2006-01-02 15:04:05.999                           |
| NUMERIC        | 01/02 03:04:05PM '06 -0700                        |
| ANSIC          | Mon Jan _2 15:04:05 2006                          |
| UNIX           | Mon Jan _2 15:04:05 MST 2006                      |
| RUBY           | Mon Jan 02 15:04:05 -0700 2006                    |
| RFC822         | 02 Jan 06 15:04 MST                               |
| RFC822Z        | 02 Jan 06 15:04 -0700                             |
| RFC850         | Monday, 02-Jan-06 15:04:05 MST                    |
| RFC1123        | Mon, 02 Jan 2006 15:04:05 MST                     |
| RFC1123Z       | Mon, 02 Jan 2006 15:04:05 -0700                   |
| RFC3339        | 2006-01-02T15:04:05Z07:00                         |
| RFC3339NANO    | 2006-01-02T15:04:05.999999999Z07:00               |
| KITCHEN        | 3:04:05PM                                         |
| STAMP          | Jan _2 15:04:05                                   |
| STAMPMILLI     | Jan _2 15:04:05.000                               |
| STAMPMICRO     | Jan _2 15:04:05.000000                            |
| STAMPNANO      | Jan _2 15:04:05.000000000                         |
| s              | 초 단위 Unix epoch 시간                           |
| ms             | 밀리초 단위 Unix epoch 시간                       |
| us             | 마이크로초 단위 Unix epoch 시간                   |
| ns             | 나노초 단위 Unix epoch 시간                       |
| s_ms           | 초와 밀리초(05.999)                               |
| s_us           | 초와 마이크로초(05.999999)                        |
| s_ns           | 초와 나노초(05.999999999)                         |
| s.ms           | 초와 밀리초, 0으로 채움(05.000)                   |
| s.us           | 초와 마이크로초, 0으로 채움(05.000000)            |
| s.ns           | 초와 나노초, 0으로 채움(05.000000000)             |

### sqlTimeformat()

*구문*: `sqlTimeformat( format )`

- `format` *string*

| format         | 출력 형식                                         |
|:---------------|:------------------------------------------------- |
| YYYY           | 4자리 연도                                        |
| YY             | 2자리 연도                                        |
| MM             | 01~12 범위의 2자리 월                             |
| DD             | 01~31 범위의 2자리 일                             |
| HH24           | 00~23 범위의 2자리 시                             |
| HH12           | 01~12 범위의 2자리 시                             |
| HH             | 1~12 범위의 시(0으로 채우지 않음)                 |
| MI             | 00~59 범위의 2자리 분                             |
| SS             | 0~59 범위의 2자리 초                              |
| nnn...         | 1~9자리 소수 초                                   |

```js {linenos=table,hl_lines=["6"],linenostart=1}
FAKE( json({
    [ 1701345032123456789, 10],
    [ 1701345043219876543, 11]
}))
MAPVALUE(0, time(value(0)) )
CSV( sqlTimeformat("YYYY-MM-DD HH24:MI:SS.nnnnnn"), tz("Asia/Seoul") )
```

```
2023-11-30 20:50:32.123456,10
2023-11-30 20:50:43.219876,11
```

### ansiTimeformat()

*구문*: `ansiTimeformat( format )`

- `format` *string*

```js {linenos=table,hl_lines=["6"],linenostart=1}
FAKE( json({
    [ 1701345032123456789, 10],
    [ 1701345043219876543, 11]
}))
MAPVALUE(0, time(value(0)) )
CSV( ansiTimeformat("yyyy-mm-dd hh:nn:ss.ffffff"), tz("UTC"))
```

```
2023-11-30 11:50:32.123456,10
2023-11-30 11:50:43.219876,11
```

| format         | 출력 형식                                         |
|:---------------|:------------------------------------------------- |
| yyyy           | 4자리 연도                                        |
| mm             | 01~12 범위의 2자리 월                             |
| dd             | 01~31 범위의 2자리 일                             |
| hh             | 00~23 범위의 2자리 시                             |
| nn             | 00~59 범위의 2자리 분                             |
| ss             | 0~59 범위의 2자리 초                              |
| fff...         | 1~9자리 소수 초                                   |


## 수학 함수

수학 함수입니다. {{< neo_since ver="8.0.6" />}}

> 시스템 아키텍처가 다르면 결과가 비트 단위까지 같다고 보장하지 않습니다.

| 함수             | 설명                                |
|:---------------- | :---------------------------------- |
| `abs(x)`         | x의 절댓값                          |
| `acos(x)`        | x의 아크코사인(라디안)              |
| `acosh(x)`       | x의 역쌍곡코사인                    |
| `asin(x)`        | x의 아크사인(라디안)                |
| `asinh(x)`       | x의 역쌍곡사인                      |
| `atan(x)`        | x의 아크탄젠트(라디안)              |
| `atanh(x)`       | x의 역쌍곡탄젠트                    |
| `ceil(x)`        | x보다 크거나 같은 최소 정수 값      |
| `cos(x)`         | 라디안 값 x의 코사인                |
| `cosh(x)`        | x의 쌍곡코사인                      |
| `exp(x)`         | e**x, 밑이 e인 x의 지수 함수        |
| `exp2(x)`        | 2**x, 밑이 2인 x의 지수 함수        |
| `floor(x)`       | x보다 작거나 같은 최대 정수 값      |
| `log(x)`         | x의 자연로그                        |
| `log2(x)`        | x의 이진 로그. 특수한 경우의 동작은 log와 같습니다. |
| `log10(x)`       | x의 상용로그. 특수한 경우의 동작은 log와 같습니다. |
| `max(x,y)`       | x와 y 중 큰 값                      |
| `min(x,y)`       | x와 y 중 작은 값                    |
| `mod(x,y)`       | x/y의 부동소수점 나머지.<br/>결과의 크기는 y보다 작고 부호는 x와 같습니다. |
| `pow(x, y)`      | x**y, 밑이 x인 y의 지수 함수        |
| `pow10(x)`       | 10**x, 밑이 10인 x의 지수 함수      |
| `remainder(x,y)` | x/y의 IEEE 754 부동소수점 나머지    |
| `round(x)`       | 가장 가까운 정수. 정확히 중간이면 0에서 먼 쪽으로 반올림합니다. |
| `sin(x)`         | 라디안 값 x의 사인                  |
| `sinh(x)`        | x의 쌍곡사인                        |
| `sqrt(x)`        | x의 제곱근                          |
| `tan(x)`         | 라디안 값 x의 탄젠트                |
| `tanh(x)`        | x의 쌍곡탄젠트                      |
| `trunc(x)`       | x의 정수 부분                       |

`MAPVALUE`에서 수학 함수를 사용하는 예입니다.

{{< tabs >}}
{{< tab name="CODE" >}}
```js {linenos=table,hl_lines=["3"],linenostart=1}
FAKE(meshgrid(linspace(-4,4,100), linspace(-4,4, 100)))
MAPVALUE(2,
    sin(pow(value(0), 2) + pow(value(1), 2)) / (pow(value(0), 2) + pow(value(1), 2))
)
MAPVALUE(0, list(value(0), value(1), value(2)))
POPVALUE(1, 2)
CHART(
    plugins("gl"),
    size("600px", "600px"),
    chartOption({
        grid3D:{},
        xAxis3D:{},
        yAxis3D:{},
        zAxis3D:{},
        series:[
            {type: "line3D", data: column(0)},
        ]
    })
)
```
{{< /tab >}}
{{< tab name="RESULT" >}}
{{< figure src="/neo/tql/img/tql-math-example.jpg" width="380px" >}}
{{< /tab >}}
{{< /tabs >}}

### random()

*구문*: `random() : number` {{< neo_since ver="8.0.7" />}}

`random()`은 반열린 구간 [0.0,1.0)에 속하는 부동소수점 의사 난수를 반환합니다.

### simplex()

*구문*: `simplex(seed, dim1 [, dim2 [, dim3 [, dim4]]]) : number` {{< neo_since ver="8.0.7" />}}

- `seed` *int* 시드 값
- `dim1` ~ `dim4` *float number*

`simplex()`는 지정한 시드와 차원 값으로 Simplex 노이즈([wikipedia](https://en.wikipedia.org/wiki/Simplex_noise))를 반환합니다. 최대 4차원까지 지정할 수 있습니다.

{{< tabs >}}
{{< tab name="CODE" >}}
```js {linenos=table,hl_lines=["6"],linenostart=1}
FAKE(
    meshgrid(
        linspace(0, 10, 100), linspace(0, 10, 100)
    )
)
MAPVALUE(2, abs( simplex(123, value(0), value(1)) ) * 10)
MAPVALUE(0, list(value(0), value(1), value(2)))
CHART(
    plugins("gl"),
    size("600px", "600px"),
    chartOption({
        visualMap: {
            max: 8,
            inRange:{ color:[ 
                    "#313695", "#74add1", "#e0f3f8",
                    "#fee090",  "#f46d43", "#a50026"]}
        },
        grid3D:{ boxWidth:100, boxDepth:100, boxHeight:20},
        xAxis3D:{}, yAxis3D:{}, zAxis3D:{},
        series:[
            {type: "bar3D", data: column(0), itemStyle:{opacity:1.0}},
        ]
    })
)
```
{{< /tab >}}
{{< tab name="RESULT" >}}
{{< figure src="/neo/tql/img/map_simplex.jpg" width="430px" >}}
{{< /tab >}}
{{< /tabs >}}

## 리스트/딕셔너리

### count()

*구문*: `count( array|tuple ) : number`

요소 개수를 반환합니다.

### list()

*구문*: `list(args...) : list` {{< neo_since ver="8.0.7" />}}

`list()`는 `args`를 요소로 하는 새 튜플을 반환합니다.

### dict()

*구문*: `dict( name1, value1 [, name2, value2 ...]) : dictionary` {{< neo_since ver="8.0.8" />}}

`dict()`는 name*n*:value*n* 쌍으로 구성된 새 딕셔너리를 반환합니다.
