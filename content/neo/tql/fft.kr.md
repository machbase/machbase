---
title: FFT()
type: docs
weight: 70
---

## 고속 푸리에 변환

{{< callout emoji="📌" >}}
원활한 실습을 위해 아래 쿼리를 실행하여 테이블과 데이터를 미리 준비해 주십시오.
{{< /callout >}}

```sql
CREATE TAG TABLE IF NOT EXISTS EXAMPLE (
    NAME VARCHAR(20) PRIMARY KEY,
    TIME DATETIME BASETIME,
    VALUE DOUBLE SUMMARIZED
);
```

## 샘플 데이터 생성

웹 UI에서 새로운 *tql* 편집기를 열고 아래 코드를 복사해 실행해 주십시오.

이 예시에서는 `oscillator()`가 15Hz 1.0과 24Hz 1.5를 합성한 파형을 생성합니다.
또한 `CHART_SCATTER()`에는 x축 하단에 슬라이더를 제공하는 `dataZoom()` 옵션 함수가 포함되어 있습니다.

```js {linenos=table,hl_lines=["2-5"],linenostart=1}
FAKE( 
  oscillator(
    freq(15, 1.0), freq(24, 1.5),
    range('now', '10s', '1ms')
  )
)
CHART_SCATTER( size("600px", "350px"), dataZoom('slider', 95, 100) )
```

{{< figure src="/images/web-fft-tql-fake.png" width="500" >}}

## 생성한 데이터를 데이터베이스에 저장하기

생성된 데이터를 'signal' 태그 이름으로 데이터베이스에 저장해 주십시오.

```js {linenos=table,hl_lines=["10"],linenostart=1}
FAKE(
  oscillator(
    freq(15, 1.0), freq(24, 1.5),
    range('now', '10s', '1ms')
  )
)
// |    0      1
// +--> time   magnitude
// |
INSERT( 'time', 'value', table('example'), tag('signal') )
```

실행 결과 창에는 "10000 rows inserted." 메시지가 표시됩니다.

참고로 테스트 머신(Apple Mac mini M1)에서는 약 270ms가 소요되었으며, 아래 예시처럼 `APPEND()` 방식을 사용하면 약 65ms(약 4배 빠르게)로 단축할 수 있습니다.

```js {linenos=table,hl_lines=["14"],linenostart=1}
FAKE(
  oscillator(
    freq(15, 1.0), freq(24, 1.5),
    range('now', '10s', '1ms')
  )
)
// |    0      1
// +--> time   magnitude
// |
PUSHVALUE(0,'signal')
// |    0         1      2
// +--> 'signal' time   magnitude
// |
APPEND( table('example') )
```

{{< callout type="warning" >}}
`APPEND`는 입력 레코드의 필드가 테이블 컬럼과 순서 및 타입까지 정확히 일치할 때만 동작합니다.
{{< /callout >}}

## 데이터베이스에서 데이터 읽기

아래 코드는 'example' 테이블에서 저장된 데이터를 읽어옵니다.

```js
SQL_SELECT('time', 'value', from('example', 'signal'), between('last-10s', 'last'))
CHART_LINE( size("600px", "350px"), dataZoom('slider', 95, 100))
```

{{< figure src="/images/web-fft-tql-query.png" width="500" >}}

## 고속 푸리에 변환 수행

`SQL_SELECT()` 소스와 `CHART_LINE()` 싱크 사이에 몇 가지 데이터 변환 함수를 추가합니다.

{{< tabs items="GROUPBYKEY,SCRIPT">}}
{{< tab >}}
```js {linenos=table,hl_lines=["2-4"],linenostart=1}
SQL_SELECT('time', 'value', from('example', 'signal'), between('last-10s', 'last'))
MAPKEY('sample')
GROUPBYKEY()
FFT()
CHART_LINE(
  size("600px", "350px"), 
  xAxis(0, 'Hz'),
  yAxis(1, 'Amplitude'),
  dataZoom('slider', 0, 10) 
)
```
{{< /tab >}}
{{< tab >}}

```js {linenos=table,hl_lines=[10,12],linenostart=1}
SQL_SELECT('time', 'value', from('example', 'signal'), between('last-10s', 'last'))
SCRIPT({
    var list = [];
    function finalize() {
        $.yield(list);
    }
},{
    ts = $.values[0];
    val = $.values[1];
    list.push([ts, val]);
})
FFT()
CHART_LINE(
  size("600px", "350px"), 
  xAxis(0, 'Hz'),
  yAxis(1, 'Amplitude'),
  dataZoom('slider', 0, 10) 
)
```
{{< /tab >}}
{{< /tabs >}}

{{< figure src="/images/web-fft-tql-2d.png" width="500" >}}

## 동작 방식

{{% steps %}}

### SQL_SELECT()
`SQL_SELECT(...)` 함수는 쿼리 결과를 `{key: rownum, value: (time, value)}` 형태의 레코드로 전달합니다.

### MAPKEY('sample')
`MAPKEY('sample')` 함수는 모든 레코드에 'sample'이라는 고정 키를 설정합니다. 그 결과 모든 레코드의 *key* 값이 `'sample'`으로 같아지고 *value*에는 `(time, value)`가 유지됩니다. `{key: 'sample', value:(time, value)}`

### GROUPBYKEY()
`GROUPBYKEY()`는 동일한 키를 가진 레코드를 병합합니다. 이 예시에서는 모든 쿼리 결과가 하나의 레코드로 합쳐져 `{key: 'sample', value:[ (time1, value1), (time2, value2), ..., (timeN, valueN) ]}` 형태가 됩니다.

### FFT()
`FFT()`는 레코드의 값을 대상으로 고속 푸리에 변환을 적용하여 `(time, value)` 배열을 `(frequency, amplitude)` 배열로 변환합니다. `{key: 'sample', value:[ (Hz1, Ampl1), (Hz2, Ampl2), ... ]}`

{{% /steps %}}

## 시간 축 추가

다음 예시는 시간 축을 추가하여 주파수 변환 결과를 시계열 형태로 시각화합니다.

```js {linenos=table,hl_lines=["3-7"],linenostart=1}
SQL_SELECT( 'time', 'value', from('example', 'signal'), between('last-10s', 'last'))

MAPKEY( roundTime(value(0), '500ms') )
GROUPBYKEY()
FFT(minHz(0), maxHz(100))
FLATTEN()
PUSHKEY('fft')
CHART_BAR3D(
      xAxis(0, 'time', 'time'),
      yAxis(1, 'Hz'),
      zAxis(2, 'Amp'),
      size('600px', '600px'), visualMap(0, 1.5), theme('westeros')
)
```

{{< figure src="/images/web-fft-tql-3d.png" width="500" >}}

## 시간 축 추가 동작 방식

{{% steps %}}

### SQL_SELECT()

`SQL_SELECT(...)` 함수는 쿼리 결과를 `{key: time, value: (value) }` 형태로 전달합니다.

### MAPKEY()
`MAPKEY( roundTime(value(0), '500ms'))`는 `value(0)`을 500밀리초 단위로 반올림한 결과를 새 키로 설정합니다. 그 결과 레코드는 `{key: (time/500ms)*500ms, value:(time, value)}` 형태로 변환됩니다.

### GROUPBYKEY()
`GROUPBYKEY()`는 레코드를 500밀리초 단위로 그룹화합니다. `{key: time1In500ms, value:[(time1, value1), (time2, value2)...]}`

### FFT()
`FFT()`는 각 레코드에 대해 고속 푸리에 변환을 적용합니다. 선택 옵션인 `minHz(0)`와 `maxHz(100)`은 시각화를 위해 출력 범위를 제한합니다. `{key:time1In500ms, value:[(Hz1, Ampl1), ...]}`, `{key:'time2In500ms', value:[(Hz1, Ampl1), ...]}`, ...

### FLATTEN()
`FLATTEN()`은 값 배열의 차원을 줄여 여러 레코드로 분할합니다. 그 결과 각 주파수-진폭 쌍이 개별 레코드로 방출됩니다.

### PUSHKEY()
`PUSHKEY('fft')`는 모든 레코드에 'fft'라는 고정 키를 설정하며, 이전 키를 값 배열의 첫 번째 위치로 이동시킵니다. `{key:'fft', value:(time1In500ms, Hz1, Ampl1)}`, `{key:'fft', value:(time1In500ms, Hz2, Ampl2)}`...

{{% /steps %}}
