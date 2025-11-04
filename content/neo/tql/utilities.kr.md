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
| `PI`   | 원주율(3.141592…) [참고](https://oeis.org/A000796) |

## 컨텍스트

### key()

*Syntax*: `key()`

현재 레코드의 키를 반환합니다.

### value()

*Syntax*: `value([index])`

- `index` *integer* (선택) 값 배열의 인덱스

현재 레코드의 값 배열을 반환합니다.  
인덱스를 지정하면 해당 위치의 값을 반환합니다.

예) 현재 값이 `[0, true, "hello", "world"]`일 때
- `value()` → `[0, true, "hello", "world"]`
- `value(0)` → `0`
- `value(3)` → `"world"`

### payload()

*Syntax*: `payload()`

TQL 스크립트를 호출한 측(HTTP·MQTT 등)에서 전달한 입력 스트림을 반환합니다.  
HTTP 호출이면 POST 바디, MQTT 호출이면 PUBLISH 메시지의 페이로드가 반환됩니다.

### param()

*Syntax*: `param(name)`

- `name` *string* : 쿼리 파라미터 이름

HTTP로 TQL을 호출한 경우, 요청에 포함된 쿼리 파라미터를 조회할 수 있습니다.

### context()

*Syntax*: `context()`

스크립트 런타임의 컨텍스트 객체를 반환합니다.

## 문자열 함수

### escapeParam()

*Syntax*: `escapeParam(str) : string` {{< neo_since ver="8.0.7" />}}

문자열을 URL 쿼리에 안전하게 사용할 수 있도록 이스케이프합니다.

### strTrimSpace()

*Syntax*: `strTrimSpace(str) : string`

문자열 앞뒤의 공백을 제거합니다.

### strTrimPrefix()

*Syntax*: `strTrimPrefix(str, prefix) : string`

문자열 앞부분의 prefix를 제거합니다. prefix가 없으면 원본을 반환합니다.

### strTrimSuffix()

*Syntax*: `strTrimSuffix(str, suffix) : string`

문자열 끝부분의 suffix를 제거합니다. suffix가 없으면 원본을 반환합니다.

### strHasPrefix()

*Syntax*: `strHasPrefix(str, prefix) : boolean`

문자열이 prefix로 시작하는지 확인합니다.

### strHasSuffix()

*Syntax*: `strHasSuffix(str, suffix) : boolean`

문자열이 suffix로 끝나는지 확인합니다.

### strReplaceAll()

*Syntax*: `strReplaceAll(str, old, new) : string`

겹치지 않는 모든 old를 new로 교체합니다.

### strReplace()

*Syntax*: `strReplace(str, old, new, n) : string`

앞에서부터 n개의 old를 new로 교체합니다. n이 0보다 작으면 횟수 제한이 없습니다.

### strSub()

*Syntax*: `strSub(str, offset [, count]) : string`

문자열의 부분 문자열을 반환합니다.

### strIndex() / strLastIndex()

- `strIndex(str, substr)` : substr가 처음 나타나는 인덱스를 반환
- `strLastIndex(str, substr)` : substr가 마지막으로 나타나는 인덱스를 반환  
  (없으면 -1)

### strToUpper() / strToLower()

문자열을 각각 대문자/소문자로 변환합니다.

### strSprintf()

*Syntax*: `strSprintf(fmt, args...) : string`

포맷 문자열(fmt)에 따라 문자열을 생성합니다. (Go의 `fmt.Sprintf`와 유사)

### strTime()

*Syntax*: `strTime(time, format [, tz]) : string`

- `time` *time*
- `format` *string* \| *sqlTimeformat()*
- `tz` *timeZone* (선택, 기본값 `tz("UTC")`)

시간 값을 지정한 형식과 시간대에 맞춰 문자열로 변환합니다.

```js
MAPVALUE(0, strTime(time("now"), "2006/01/02 15:04:05.999", tz("UTC")), "result")
```

## 숫자 변환

### parseFloat()

*Syntax*: `parseFloat(str) : number`

문자열을 부동소수점 숫자로 변환합니다.

### parseBool()

*Syntax*: `parseBool(str) : boolean`

문자열이 `"true"`, `"false"` 등 불리언 표현인지 확인하고 대응하는 값을 반환합니다. 다른 문자열이면 오류가 발생합니다.

## 문자열 매칭

### glob()

*Syntax*: `glob(pattern, text) : boolean`

glob 패턴으로 문자열을 비교합니다.

### regexp()

*Syntax*: `regexp(expression, text) : boolean`

정규 표현식으로 문자열을 비교합니다.

## 시간 함수

### time()

*Syntax*: `time(number|string) : time`

시간 표현을 time 값으로 변환합니다.
- `time("now")` : 현재 시각
- `time("now-10s50ms")` : 현재보다 10.05초 이전 시각
- `time(1672531200*1000000000)` : 특정 epoch(ns) 시각

### timeYear() ~ timeNanosecond()

`timeYear(time)`, `timeMonth(time)`, `timeDay(time)`, `timeHour(time)` 등  
주어진 time의 연도/월/일/시/분/초/나노초 등을 반환합니다. 일부 함수는 시간대를 지정할 수 있습니다.

### timeISOYear(), timeISOWeek()

ISO 8601 규칙에 따라 연도/주차를 반환합니다.

### timeUnix(), timeUnixMilli(), timeUnixMicro(), timeUnixNano()

time 값을 Unix epoch(초/밀리초/마이크로초/나노초) 단위로 변환합니다.

### timeAdd()

*Syntax*: `timeAdd(value, offset) : time`

주어진 시간에 오프셋을 더한 값을 반환합니다.  
예: `timeAdd("now", "-10s")`

### roundTime()

*Syntax*: `roundTime(time, duration) : time`

지정한 단위(`1h`, `1s` 등)로 시간을 반올림합니다.

### parseTime()

*Syntax*: `parseTime(str, format [, tz]) : time`

문자열을 지정한 포맷과 시간대로 변환합니다. `format`은 `"DEFAULT"`, `"RFC3339"` 등 사전 정의된 값이나 `sqlTimeformat()` 등을 사용할 수 있습니다.

### tz()

*Syntax*: `tz(name) : timeZone`

시간대 이름(`"UTC"`, `"Asia/Seoul"` 등)에 해당하는 객체를 반환합니다.

### timeformat(), sqlTimeformat(), ansiTimeformat()

시간을 문자열로 출력할 때 사용할 포맷을 정의합니다.  
`timeformat("RFC3339")`, `sqlTimeformat("YYYY/MM/DD HH24:MI:SS")`, `ansiTimeformat("yyyy-mm-dd hh:nn:ss")` 등 다양한 포맷을 지원합니다.

## 수학 함수

각종 수학 연산을 제공합니다. {{< neo_since ver="8.0.6" />}}  
예: `abs(x)`, `sin(x)`, `pow(x, y)`, `sqrt(x)` 등

> 시스템 아키텍처에 따라 결과가 완전히 동일하지 않을 수 있습니다.

### random()

*Syntax*: `random() : number`

0 이상 1 미만의 실수 난수를 반환합니다.

### simplex()

*Syntax*: `simplex(seed, dim1 [, dim2 [, dim3 [, dim4]]]) : number`

Simplex 노이즈(최대 4차원)를 반환합니다.

## 리스트/딕셔너리

### count()

*Syntax*: `count(array|tuple) : number`

요소 개수를 반환합니다.

### list()

*Syntax*: `list(args...) : list`

지정한 값으로 구성된 리스트를 생성합니다.

### dict()

*Syntax*: `dict(name1, value1 [, name2, value2 ...])`

키-값 쌍으로 구성된 딕셔너리를 생성합니다.
