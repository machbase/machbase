---
title: GROUP()
type: docs
weight: 60
math: true
---

{{< neo_since ver="8.0.7" />}}

## 구문

```
GROUP( [lazy(boolean)] [, by()] [, aggregator ...] )
```

- `lazy(boolean)` : 지연 모드를 설정합니다(기본값 `false`).
- `by(value [, timewindow()] [, name])` : 그룹을 어떻게 나눌지 지정합니다.  
  {{< neo_since ver="8.0.14" />}}부터는 `by()` 없이 전체 데이터에 대해 집계기를 적용하는 것도 가능합니다.
- `aggregator` : 하나 이상의 집계 함수. 쉼표로 구분합니다.

```js {linenos=table,hl_lines=["7-12"],linenostart=1}
FAKE(json({
    ["A", 1],
    ["A", 2],
    ["B", 3],
    ["B", 4]
}))
GROUP(
    by(value(0), "CATEGORY"),
    avg(value(1), "AVG"),
    sum(value(1), "SUM"),
    first(value(1) * 10, "x10")
)
CSV(header(true))
```

**결과**
{{< figure src="/neo/tql/img/group-type1-ex1.jpg" width="600" >}}

### `by()`

*Syntax*: `by(value [, timewindow] [, label])`

- `value` : 그룹의 기준 값. 보통 시간 또는 문자열입니다.
- `timewindow(from, until, period)` : 시간 범위를 명시합니다.
- `label` : 새로운 컬럼 이름(기본값 `"GROUP"`).

### `lazy()`

*Syntax*: `lazy(boolean)`

기본값 `false`인 경우, `GROUP()`은 현재 레코드와 이전 레코드의 `by()` 값이 달라질 때마다 결과를 출력합니다.  
즉 연속된 레코드의 값이 같을 때만 하나의 그룹이 만들어집니다.  
`lazy(true)`로 설정하면 입력 스트림의 끝까지 데이터를 모은 뒤 그룹을 계산하므로 정렬되지 않은 데이터도 그룹화할 수 있지만, 메모리를 많이 사용합니다.

### `timewindow()`

*Syntax*: `timewindow(from, until, period)` {{< neo_since ver="8.0.13" />}}

- `from`, `until` : 포함-제외 형태의 시간 범위입니다. 실데이터 유무와 상관없이 원하는 구간을 지정할 수 있습니다.
- `period` : `from`과 `until` 사이의 시간 간격을 나타냅니다.

> [timewindow 예제](#timewindow-1)를 참고해 주십시오.

고정된 시간 간격으로 데이터를 시각화할 때, 조회 결과에 비어 있는 구간이나 과도하게 촘촘한 구간이 존재하면 원하는 모양으로 데이터를 다듬기 어렵습니다.  
`timewindow()`를 이용하면 이러한 작업을 TQL 내에서 처리할 수 있습니다.

### 집계기(aggregator)

집계기를 지정하지 않으면 `GROUP()`은 기본적으로 원본 레코드들을 배열로 그대로 묶어 반환합니다.  
연속된 레코드가 같은 `by()` 값을 가지면 `[[v1,v2], [v3,v4], ...]` 형태의 배열을 생성합니다.

집계 함수는 두 가지 유형이 있습니다.
- **Type 1** : 결과 후보만 유지하고 최종 값만 반환합니다.
- **Type 2** : 그룹 전체 데이터를 보관하여 계산 후 메모리를 해제합니다. `lazy(true)`와 함께 사용하면 관련 컬럼 전체 데이터를 모두 메모리에 유지합니다.

#### 공통 옵션

`where()`, `nullValue()`, `predict()`, `label`은 모든 집계 함수에서 사용할 수 있는 선택 옵션입니다.

- `where(predicate)` : 조건식을 만족하는 값만 집계합니다. {{< neo_since ver="8.0.13" />}}
- `nullValue(alternative)` : 집계 결과가 없을 때 대체할 값을 지정합니다. {{< neo_since ver="8.0.13" />}}
- `predict(algorithm)` : 값이 없을 때 보간 알고리즘을 적용해 대체합니다. {{< neo_since ver="8.0.13" />}}
- `label` : 결과 컬럼 이름(디폴트는 함수명)

| algorithm            | 설명 |
|:---------------------|:-----|
| `PiecewiseConstant`  | 왼쪽 연속(piecewise constant) 1차원 보간 |
| `PiecewiseLinear`    | 선형 1차원 보간 |
| `AkimaSpline`        | 연속 값과 1차 미분을 갖는 1차원 cubic 보간 |
| `FritschButland`     | 단조성이 보장되는 cubic 보간 |
| `LinearRegression`   | 인접 값으로 선형 회귀 보간 |

## 집계 함수

- `avg(x [, option...])` : 평균 (Type 1)
- `sum(x [, option...])` : 합계 (Type 1)
- `count(x [, option...])` : 개수 (Type 1) {{< neo_since ver="8.0.13" />}}
- `first(x [, option...])` : 첫 번째 값 (Type 1)
- `last(x [, option...])` : 마지막 값 (Type 1)
- `min(x [, option...])` : 최소값 (Type 1)
- `max(x [, option...])` : 최대값 (Type 1)
- `rss(x [, option...])` : Root Sum Square (Type 1)
- `rms(x [, option...])` : Root Mean Square (Type 1)
- `list(x [, option...])` : 모든 값을 리스트로 묶음 (Type 2) {{< neo_since ver="8.0.15" />}}

### `list()` 예시

```js {linenos=table,hl_lines=[4]}
FAKE(json({["A",1], ["A",2], ["B",3], ["B",4], ["C",5]}))
GROUP(
    by(value(0)),
    list(value(1))
)
JSON()
```

```json
{
    "data": {
        "columns": ["GROUP", "LIST"],
        "types": ["string", "list"],
        "rows": [
            ["A", [1,2]],
            ["B", [3,4]],
            ["C", [5]]
        ]
    },
    "success": true,
    "reason": "success",
    "elapse": "220.375µs"
}
```

### 고급: rowsArray/FLATTEN 조합

`JSON(rowsArray(true))`나 `FLATTEN()`과 조합하면 다양한 형태로 결과를 가공할 수 있습니다.

```js {linenos=table,hl_lines=[4,7]}
FAKE(json({["A",1], ["A",2], ["B",3], ["B",4], ["C",5]}))
GROUP(
    by(value(0), "name"),
    avg(value(1), "avg"),
    list(value(1), "values")
)
JSON(rowsArray(true))
```

```json
{
    "data": {
        "columns": ["name", "values", "avg"],
        "types": ["string", "list", "float64"],
        "rows": [
            { "name": "A", "avg": 1.5, "values": [1, 2] },
            { "name": "B", "avg": 3.5, "values": [3, 4] },
            { "name": "C", "avg": 5,   "values": [5] }
        ]
    },
    "success": true,
    "reason": "success",
    "elapse": "270.25µs"
}
```

```js {linenos=table,hl_lines=[4,7],linenostart=1}
FAKE(json({["A",1], ["A",2], ["B",3], ["B",4], ["C",5]}))
GROUP(
    by(value(0)),
    list(value(1))
)
POPVALUE(0)
FLATTEN()
JSON()
```

```json
{
    "data": {
        "columns": ["LIST"],
        "types": ["list"],
        "rows": [
            [1,2],
            [3,4],
            [5]
        ]
    },
    "success": true,
    "reason": "success",
    "elapse": "252.625µs"
}
```
