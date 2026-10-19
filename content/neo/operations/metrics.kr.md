---
title: 메트릭
type: docs
weight: 101
toc: true
---

{{< neo_since ver="8.7.0" />}}

Machbase Neo는 서버 상태와 요청 처리 통계를 수집하여 `SYS._NEO_STATZ` 테이블에 저장합니다.
SQL로 필요한 메트릭과 기간을 조회하고, TQL의 `SQL()`과 `CHART()`를 조합하여 시각화할 수 있습니다.

이 문서의 예시는 `sys` 사용자로 접속하여 실행합니다.
`_NEO_STATZ`는 서버가 자동으로 생성하고 관리하므로 직접 생성하거나 데이터를 입력할 필요가 없습니다.

## 저장 구조와 수집 주기

`_NEO_STATZ`는 다음 세 컬럼을 가진 일반 트랜잭션 테이블입니다. TAG 테이블이 아닙니다.

| 컬럼 | 타입 | 설명 |
|:-----|:-----|:-----|
| `NAME` | `VARCHAR(100)` | 메트릭 키 |
| `TIME` | `DATETIME` | 1분 집계 구간의 시작 시각 |
| `VALUE` | `DOUBLE` | 해당 구간의 메트릭 값 |

`(NAME, TIME)`에는 고유 인덱스가 있습니다.
진행 중인 구간의 값은 같은 행을 갱신하고, 다음 구간으로 넘어가면 새 행을 저장합니다.

- **수집 주기:** 시스템 상태 등 주기적으로 수집하는 항목은 10초마다 측정합니다.
  HTTP 요청 통계는 요청이 처리될 때 수집합니다.
- **저장 해상도:** 1분입니다. 10초마다 수집하더라도 각 샘플을 별도 행으로 저장하지 않습니다.
- **현재 구간:** 아직 끝나지 않은 1분 구간도 저장하므로, 같은 `TIME`의 `VALUE`가 바뀔 수 있습니다.
- **보관 기간:** 8일입니다. 저장 작업 중 15분 간격으로 오래된 데이터를 정리하므로,
  8일이 지난 행이 다음 정리 시점까지 남아 있을 수 있습니다.

### 값 해석

모든 `VALUE`가 서버 시작 이후의 누적값이거나 1분 평균인 것은 아닙니다.
항목의 수집 방식에 따라 다음과 같이 해석합니다.

| 방식 | 저장되는 값 | 예 |
|:-----|:------------|:---|
| 상태값(Gauge) | 해당 구간에서 마지막으로 측정한 값 | `runtime:heap_inuse`, `sys:session:count` |
| 합계(Counter) | 해당 구간에 수집한 값의 합계 | `http:count`, `http:send_bytes` |
| 누적값의 차이(Odometer) | 누적 카운터의 기준값 대비 마지막 값의 차이 | `sys:execute:count`, `sys:pool:wait_count` |
| 분포(Histogram) | 표본 수와 백분위수 | `http:latency`, `http:latency:p99` |

예를 들어 `http:latency`는 지연 시간이 아니라 **해당 구간의 표본 수**이고,
실제 지연 시간은 `http:latency:p50`, `http:latency:p90`, `http:latency:p99`에 저장됩니다.
시간 단위가 `ns`인 값은 `1000000`으로 나누면 `ms`가 됩니다.

요청이 없었던 구간에는 HTTP 메트릭 행이 없을 수 있습니다.
**행이 없는 것과 값이 0인 것은 다릅니다.**
현재 구간의 합계·차이·백분위수는 구간이 끝나기 전까지의 값이며,
1분 구간의 차이를 그대로 초당 처리량으로 해석하지 마십시오.

## 메트릭 키 찾기

설정과 사용 중인 기능에 따라 수집되는 키가 다릅니다.
먼저 현재 서버에 실제로 저장된 키를 확인하십시오.

```sql
SELECT NAME FROM _NEO_STATZ GROUP BY NAME ORDER BY NAME;
```

특정 영역만 확인하려면 `LIKE`로 필터링합니다.

```sql
SELECT NAME FROM _NEO_STATZ WHERE NAME LIKE 'http:%'
GROUP BY NAME
ORDER BY NAME;
```

각 키의 저장 범위와 행 수를 함께 확인할 수도 있습니다.

```sql
SELECT NAME, MIN(TIME) AS FIRST_TIME, MAX(TIME) AS LAST_TIME, COUNT(*) AS POINTS
FROM _NEO_STATZ
GROUP BY NAME
ORDER BY NAME;
```

HTTP 관련 키는 요청을 처리한 뒤 나타납니다.
MQTT 관련 키는 MQTT 브로커를 사용 중일 때, 롤업 관련 키는 수집 대상 롤업이 있을 때 나타납니다.
이전에 저장된 키는 해당 기능을 더 이상 사용하지 않더라도 보관 기간 동안 조회될 수 있습니다.

## SQL로 조회하기

다음 쿼리는 최근 1시간 동안의 Go 힙 사용량을 시간순으로 조회합니다.
`SYSDATE - 1h`를 `SYSDATE - 30m`, `SYSDATE - 1d` 등으로 바꾸면 조회 기간을 조정할 수 있습니다.

```sql
SELECT TIME, VALUE
FROM _NEO_STATZ
WHERE NAME = 'runtime:heap_inuse'
  AND TIME >= SYSDATE - 1h
ORDER BY TIME;
```

진행 중인 1분 구간을 제외하고 완료된 구간만 조회하려면 다음 조건을 추가합니다.

```sql
SELECT TIME, VALUE
FROM _NEO_STATZ
WHERE NAME = 'runtime:heap_inuse'
  AND TIME >= SYSDATE - 1h
  AND TIME < DATE_TRUNC('minute', SYSDATE)
ORDER BY TIME;
```

## TQL로 시각화하기

웹 UI의 TQL 편집기에서 아래 예시를 실행합니다.
`SQL()`로 조회한 `TIME`과 값을 `list()`로 묶으면 시간 축 차트의 한 점이 됩니다.
다른 메트릭을 그리려면 `NAME` 조건, 단위 변환 및 차트의 이름을 바꾸십시오.
조회 결과는 `ORDER BY TIME`으로 정렬합니다.

### 힙 사용량

바이트 단위의 힙 사용량을 MiB로 변환하여 표시합니다.

```js
SQL(`
    SELECT TIME, VALUE / 1048576.0 AS HEAP_MIB
    FROM _NEO_STATZ
    WHERE NAME = 'runtime:heap_inuse'
      AND TIME >= SYSDATE - 1h
    ORDER BY TIME
`)
MAPVALUE(1, list(value(0), value(1)))
CHART(
    size("800px", "350px"),
    chartOption({
        animation: false,
        xAxis: { type: "time" },
        yAxis: { type: "value", name: "MiB" },
        tooltip: { trigger: "axis" },
        legend: {},
        series: [
            { name: "Go heap", type: "line", showSymbol: false, data: column(1) }
        ]
    })
)
```

### 데이터베이스 연결 풀

서로 다른 키를 한 차트에 표시하려면 `CASE`와 `GROUP BY TIME`으로 같은 시각의 값을 한 행에 모읍니다.
다음 예시는 열려 있는 연결 수와 사용 중인 연결 수를 비교합니다.
여기서 `MAX()`는 여러 시점의 최댓값을 구하는 것이 아니라,
같은 `TIME`에서 각 키에 해당하는 값을 선택하는 역할입니다.

```js
SQL(`
    SELECT TIME,
        MAX(CASE WHEN NAME = 'sys:pool:open' THEN VALUE END) AS OPEN_CONNS,
        MAX(CASE WHEN NAME = 'sys:pool:in_use' THEN VALUE END) AS IN_USE_CONNS
    FROM _NEO_STATZ
    WHERE NAME IN ('sys:pool:open', 'sys:pool:in_use')
      AND TIME >= SYSDATE - 1h
    GROUP BY TIME
    ORDER BY TIME
`)
MAPVALUE(1, list(value(0), value(1)))
MAPVALUE(2, list(value(0), value(2)))
CHART(
    size("800px", "350px"),
    chartOption({
        animation: false,
        xAxis: { type: "time" },
        yAxis: { type: "value", name: "Connections", minInterval: 1 },
        tooltip: { trigger: "axis" },
        legend: {},
        series: [
            { name: "Open", type: "line", showSymbol: false, data: column(1) },
            { name: "In use", type: "line", showSymbol: false, data: column(2) }
        ]
    })
)
```

### HTTP 응답 지연

전체 HTTP 요청의 p50·p90·p99 지연 시간을 ms 단위로 비교합니다.
백분위수는 각 1분 구간에서 수집한 표본의 분포를 나타냅니다.
요청이 없으면 결과가 비어 있을 수 있으므로, 먼저 서버의 HTTP API를 사용한 뒤 실행하십시오.

```js
SQL(`
    SELECT TIME,
        MAX(CASE WHEN NAME = 'http:latency:p50' THEN VALUE END) / 1000000.0 AS P50,
        MAX(CASE WHEN NAME = 'http:latency:p90' THEN VALUE END) / 1000000.0 AS P90,
        MAX(CASE WHEN NAME = 'http:latency:p99' THEN VALUE END) / 1000000.0 AS P99
    FROM _NEO_STATZ
    WHERE NAME IN ('http:latency:p50', 'http:latency:p90', 'http:latency:p99')
      AND TIME >= SYSDATE - 1h
    GROUP BY TIME
    ORDER BY TIME
`)
MAPVALUE(1, list(value(0), value(1)))
MAPVALUE(2, list(value(0), value(2)))
MAPVALUE(3, list(value(0), value(3)))
CHART(
    size("800px", "350px"),
    chartOption({
        animation: false,
        xAxis: { type: "time" },
        yAxis: { type: "value", name: "ms" },
        tooltip: { trigger: "axis" },
        legend: {},
        series: [
            { name: "p50", type: "line", showSymbol: false, data: column(1) },
            { name: "p90", type: "line", showSymbol: false, data: column(2) },
            { name: "p99", type: "line", showSymbol: false, data: column(3) }
        ]
    })
)
```

쿼리의 키를 `http:query:latency:p50` 등으로 바꾸면 `/db/query` 요청만 비교할 수 있습니다.
조회 기간을 늘려도 저장된 1분 해상도는 바뀌지 않습니다.
또한 여러 구간의 p99를 단순 평균한 값은 전체 기간의 p99가 아닙니다.

## 주요 메트릭 목록

아래 목록은 서버에 내장된 주요 수집 항목입니다.
실제 키의 존재 여부는 앞의 SQL로 확인하십시오.
표의 "상태"는 마지막 측정값, "합계"는 구간 내 합계,
"차이"는 누적 카운터의 차이를 의미합니다.

### 시스템과 Go 런타임

CPU·메모리 비율과 TCP 연결 수는 호스트 시스템 기준입니다.
Go 런타임 항목은 Machbase Neo 프로세스 기준입니다.

| 키 | 방식 | 설명 / 단위 |
|:---|:-----|:------------|
| `ps:cpu_percent` | 상태 | 호스트 CPU 사용률 / % |
| `ps:mem_percent` | 상태 | 호스트 메모리 사용률 / % |
| `runtime:goroutines` | 상태 | Go 고루틴 수 |
| `runtime:heap_inuse` | 상태 | Go 힙에서 사용 중인 스팬의 크기 / bytes |
| `runtime:cgo_call` | 차이 | cgo 호출 수 |
| `netstat:tcp_established` | 상태 | ESTABLISHED TCP 연결 수 |
| `netstat:tcp_fin_wait1` | 상태 | FIN_WAIT1 TCP 연결 수 |
| `netstat:tcp_fin_wait2` | 상태 | FIN_WAIT2 TCP 연결 수 |
| `netstat:tcp_time_wait` | 상태 | TIME_WAIT TCP 연결 수 |
| `netstat:tcp_close_wait` | 상태 | CLOSE_WAIT TCP 연결 수 |
| `netstat:tcp_listen` | 상태 | LISTEN TCP 소켓 수 |

### 데이터베이스

| 키 | 방식 | 설명 / 단위 |
|:---|:-----|:------------|
| `sys:sysmem` | 상태 | `V$SYSMEM`의 `USAGE` 합계 / bytes |
| `sys:session:count` | 상태 | 닫히지 않은 DB 세션 수 |
| `sys:append:open` | 차이 | APPEND 열기 횟수 |
| `sys:append:close` | 차이 | APPEND 닫기 횟수 |
| `sys:append:data:success` | 차이 | `APPEND_DATA_SUCCESS` 증가량 |
| `sys:append:data:failure` | 차이 | `APPEND_DATA_FAILURE` 증가량 |
| `sys:execute:count` | 차이 | `V$SYSTIME`의 `EXECUTE` 실행 횟수 증가량 |
| `sys:execute:time:avg` | 상태 | `V$SESTIME.MAX_MSEC`의 세션 간 평균 / ns |
| `sys:execute:time:max` | 상태 | `V$SESTIME.MAX_MSEC`의 세션 간 최댓값 / ns |

`sys:execute:time:avg`는 개별 SQL 실행 시간 전체의 평균이 아니라,
각 세션의 `MAX_MSEC` 값을 평균한 결과입니다.

### 서버 내부 연결 풀

서버가 사용하는 기본 `database/sql` 연결 풀의 통계입니다.
서버 전체 DB 세션 수인 `sys:session:count`와 구분하십시오.

| 키 | 방식 | 설명 / 단위 |
|:---|:-----|:------------|
| `sys:pool:max_open` | 상태 | 최대 연결 수 설정. 0이면 제한 없음 |
| `sys:pool:open` | 상태 | 열려 있는 연결 수 |
| `sys:pool:in_use` | 상태 | 사용 중인 연결 수 |
| `sys:pool:idle` | 상태 | 유휴 연결 수 |
| `sys:pool:wait_count` | 차이 | 연결을 기다린 횟수 |
| `sys:pool:wait_duration` | 차이 | 연결 대기 시간의 합계 / ns |
| `sys:pool:max_idle_closed` | 차이 | 최대 유휴 연결 수 제한으로 닫힌 연결 수 |
| `sys:pool:max_idletime_closed` | 차이 | 최대 유휴 시간 초과로 닫힌 연결 수 |
| `sys:pool:max_lifetime_closed` | 차이 | 최대 수명 초과로 닫힌 연결 수 |

### HTTP

요청 수·바이트 수·상태 코드별 횟수는 구간 내 합계입니다.
지연 시간의 기본 키에는 표본 수가, `:p50`·`:p90`·`:p99` 키에는 ns 단위의 지연이 저장됩니다.

| 키 | 설명 |
|:---|:-----|
| `http:count` | 전체 HTTP 요청 수 |
| `http:latency` | 전체 HTTP 요청 지연의 표본 수 |
| `http:latency:p50`,<br/> `http:latency:p90`,<br/> `http:latency:p99` | 전체 HTTP 요청 지연의 백분위수 / ns |
| `http:write:count` | `/db/write` 요청 수 |
| `http:write:latency` | `/db/write` 요청 지연의 표본 수 |
| `http:write:latency:p50`,<br/> `http:write:latency:p90`,<br/> `http:write:latency:p99` | `/db/write` 요청 지연의 백분위수 / ns |
| `http:query:count` | `/db/query` 요청 수 |
| `http:query:latency` | `/db/query` 요청 지연의 표본 수 |
| `http:query:latency:p50`,<br/> `http:query:latency:p90`,<br/> `http:query:latency:p99` | `/db/query` 요청 지연의 백분위수 / ns |
| `http:tql:count` | `/db/tql` 요청 수 |
| `http:tql:latency` | `/db/tql` 요청 지연의 표본 수 |
| `http:tql:latency:p50`,<br/> `http:tql:latency:p90`,<br/> `http:tql:latency:p99` | `/db/tql` 요청 지연의 백분위수 / ns |
| `http:recv_bytes` | 수집된 요청 본문 크기의 합계 / bytes |
| `http:send_bytes` | 수집된 응답 본문 크기의 합계 / bytes |
| `http:status_1xx`, `http:status_2xx`,<br/> `http:status_3xx`, `http:status_4xx`,<br/> `http:status_5xx` | 상태 코드 계열별 응답 수 |

### MQTT

아래 항목은 모두 브로커 통계의 마지막 측정값입니다.
특히 수신·송신 바이트 수와 메시지 수 등 누적 통계도
HTTP의 구간 합계와 달리 **브로커가 제공하는 누적값 자체**를 저장합니다.

| 키 | 설명 / 단위 |
|:---|:------------|
| `mqtt:recv_bytes` | 수신한 누적 바이트 수 / bytes |
| `mqtt:send_bytes` | 송신한 누적 바이트 수 / bytes |
| `mqtt:recv_msgs` | 수신한 누적 PUBLISH 메시지 수 |
| `mqtt:send_msgs` | 송신한 누적 PUBLISH 메시지 수 |
| `mqtt:drop_msgs` | 드롭된 누적 메시지 수 |
| `mqtt:recv_pkts` | 수신한 누적 패킷 수 |
| `mqtt:send_pkts` | 송신한 누적 패킷 수 |
| `mqtt:retained` | 보관 중인 retain 메시지 수 |
| `mqtt:subscriptions` | 구독 수 |
| `mqtt:clients` | 연결 중이거나 세션이 유지되는 클라이언트 수 |
| `mqtt:clients_connected` | 연결 중인 클라이언트 수 |
| `mqtt:clients_disconnected` | 연결이 끊겼으나 세션이 유지되는 클라이언트 수 |
| `mqtt:inflight` | 전송 중인 메시지 수 |
| `mqtt:inflight_dropped` | 전송 중 드롭된 누적 메시지 수 |

### TQL 캐시

아래 항목도 마지막 측정값을 저장합니다.
`items`는 현재 항목 수이고, 나머지는 캐시가 집계한 누적 횟수입니다.

| 키 | 설명 |
|:---|:-----|
| `tql:cache:items` | 현재 캐시 항목 수 |
| `tql:cache:evictions` | 캐시에서 제거된 누적 항목 수 |
| `tql:cache:insertions` | 캐시에 삽입된 누적 횟수 |
| `tql:cache:hits` | 누적 캐시 히트 수 |
| `tql:cache:misses` | 누적 캐시 미스 수 |

### 롤업

`<rollup_table>`에는 소문자로 변환된 롤업 테이블 이름이 들어갑니다.
모든 항목은 마지막 측정값을 저장합니다.

| 키 | 설명 / 단위 |
|:---|:------------|
| `sys:rollup:<rollup_table>:gap` | 원본 테이블과 해당 롤업 처리 위치의 RID 차이 합계 |
| `sys:rollup:<rollup_table>:last_elapse` | 해당 롤업의 `LAST_ELAPSED_MSEC` 최댓값을 ns로 변환한 값 |
| `sys:rollup_global:gap` | 수집 대상 롤업 전체의 gap 합계 |
| `sys:rollup_global:last_elapse` | 직전 수집 간격 내 실행된 롤업 중 최대 실행 시간 / ns |

`sys:rollup_global:last_elapse`는 직전 수집 간격 내 실행된 롤업이 없으면 0입니다.
