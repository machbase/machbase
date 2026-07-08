---
type: docs
title: '실시간 상태판 만들기'
weight: 50
---

## 시나리오 개요

TAG 테이블에 수집된 최신 센서값을 폴링하여 실시간 상태판(대시보드)을 구성하는 패턴입니다. 각 센서의 현재값, 상태 등급, 임계값 초과 여부를 화면에 표시하고, REST API 또는 외부 시각화 도구와 연동하는 방법을 설명합니다.

---

## 사전 준비

다음과 같은 TAG 테이블이 존재한다고 가정합니다.

```sql
CREATE TAG TABLE sensor_tag (
    name    VARCHAR(64) PRIMARY KEY,
    time    DATETIME BASETIME,
    value   DOUBLE SUMMARIZED
);
```

테스트 데이터 삽입:

```sql
INSERT INTO sensor_tag METADATA VALUES ('TEMP_01');
INSERT INTO sensor_tag METADATA VALUES ('TEMP_02');
INSERT INTO sensor_tag METADATA VALUES ('PRESS_01');

INSERT INTO sensor_tag VALUES ('TEMP_01',  NOW(), 72.3);
INSERT INTO sensor_tag VALUES ('TEMP_02',  NOW(), 88.1);
INSERT INTO sensor_tag VALUES ('PRESS_01', NOW(), 1.04);

EXEC TABLE_FLUSH(sensor_tag);
```

---

## 1단계: 최신 센서값 조회

TAG 테이블에서 특정 태그의 가장 최근 값을 조회하려면 역방향 스캔(SCAN_BACKWARD) 힌트와 LIMIT을 함께 사용합니다.

```sql
-- 단일 태그 최신값 1건 조회
SELECT /*+ SCAN_BACKWARD(sensor_tag) */
       name, time, value
  FROM sensor_tag
 WHERE name = 'TEMP_01'
 LIMIT 1;
```

TAG 테이블의 통계 가상 테이블(`v$<테이블명>_stat`)을 활용하면 모든 태그의 최신 시각을 한 번에 조회할 수 있습니다.

```sql
-- v$sensor_tag_stat 으로 각 태그의 최신 입력 시각 확인
SELECT name,
       recent_row_time,
       max_value,
       min_value,
       row_count
  FROM v$sensor_tag_stat
 ORDER BY name;
```

---

## 2단계: 여러 센서의 최신값 동시 조회

여러 태그의 최신값을 한 쿼리로 조회할 때는 `IN` 조건으로 태그를 지정하고, 서브쿼리로 각 태그의 최신 시각과 조인합니다.

```sql
-- 각 태그의 최신 시각을 기준으로 최신값 조회
SELECT t.name, t.time, t.value
  FROM sensor_tag t
  JOIN (
      SELECT name, recent_row_time AS max_time
        FROM v$sensor_tag_stat
       WHERE name IN ('TEMP_01', 'TEMP_02', 'PRESS_01')
  ) s ON t.name = s.name
     AND t.time = s.max_time;
```

태그 수가 적고 폴링 주기가 짧을 때는 개별 쿼리를 병렬로 실행하는 것이 더 단순합니다.

```sql
-- 태그별로 개별 조회 (폴링 방식)
SELECT /*+ SCAN_BACKWARD(sensor_tag) */ name, time, value
  FROM sensor_tag WHERE name = 'TEMP_01' LIMIT 1;

SELECT /*+ SCAN_BACKWARD(sensor_tag) */ name, time, value
  FROM sensor_tag WHERE name = 'TEMP_02' LIMIT 1;

SELECT /*+ SCAN_BACKWARD(sensor_tag) */ name, time, value
  FROM sensor_tag WHERE name = 'PRESS_01' LIMIT 1;
```

---

## 3단계: 상태 임계값 판정 로직

`CASE WHEN` 구문으로 센서값에 따른 상태 등급을 계산합니다.

```sql
-- 온도 임계값 판정: 정상/경고/위험
SELECT s.name,
       t.time                                       AS last_time,
       t.value                                      AS current_value,
       CASE
           WHEN t.value >= 90 THEN 'CRITICAL'
           WHEN t.value >= 80 THEN 'WARNING'
           ELSE                    'NORMAL'
       END                                          AS status,
       CASE
           WHEN t.value >= 90 THEN 2
           WHEN t.value >= 80 THEN 1
           ELSE                    0
       END                                          AS severity
  FROM sensor_tag t
  JOIN (
      SELECT name, recent_row_time AS max_time
        FROM v$sensor_tag_stat
       WHERE name IN ('TEMP_01', 'TEMP_02')
  ) s ON t.name = s.name
     AND t.time = s.max_time
 ORDER BY severity DESC, t.name;
```

여러 임계값 기준을 테이블로 관리하고 싶다면, LOOKUP 테이블에 임계값 설정을 저장한 뒤 JOIN으로 연결하는 방법을 권장합니다.

```sql
-- 임계값 설정 LOOKUP 테이블 (예시)
CREATE LOOKUP TABLE threshold_config (
    tag_name    VARCHAR(64) PRIMARY KEY,
    warn_value  DOUBLE,
    crit_value  DOUBLE
);

INSERT INTO threshold_config VALUES ('TEMP_01',  80.0, 90.0);
INSERT INTO threshold_config VALUES ('TEMP_02',  80.0, 90.0);
INSERT INTO threshold_config VALUES ('PRESS_01', 1.10, 1.20);

-- 임계값 테이블과 결합하여 동적 상태 판정
SELECT t.name,
       t.time                                          AS last_time,
       t.value                                         AS current_value,
       c.warn_value,
       c.crit_value,
       CASE
           WHEN t.value >= c.crit_value THEN 'CRITICAL'
           WHEN t.value >= c.warn_value THEN 'WARNING'
           ELSE                              'NORMAL'
       END                                             AS status
  FROM sensor_tag t
  JOIN (
      SELECT name, recent_row_time AS max_time
        FROM v$sensor_tag_stat
  ) s ON t.name = s.name AND t.time = s.max_time
  JOIN threshold_config c ON t.name = c.tag_name
 ORDER BY t.name;
```

---

## 4단계: REST API로 대시보드 연동

Machbase의 HTTP REST API(`/machbase?q=...`)를 사용하면 별도의 미들웨어 없이 대시보드에서 직접 쿼리를 실행할 수 있습니다.

```bash
# machbase.conf에서 HTTP 활성화
HTTP_ENABLE  = 1
HTTP_PORT_NO = 5657
```

```bash
# curl로 최신값 조회
curl -G "http://localhost:5657/machbase" \
     --data-urlencode "q=SELECT /*+ SCAN_BACKWARD(sensor_tag) */ name, time, value FROM sensor_tag WHERE name='TEMP_01' LIMIT 1"
```

응답 예시 (JSON):

```json
{
  "data": {
    "columns": ["NAME", "TIME", "VALUE"],
    "rows": [
      ["TEMP_01", "2024-01-15 10:23:45 000:000:000", 72.3]
    ]
  },
  "success": true,
  "reason": "success",
  "elapse": "1.234ms"
}
```

JavaScript(브라우저)에서 폴링하는 예시:

```javascript
async function fetchLatestValues() {
    const tags = ['TEMP_01', 'TEMP_02', 'PRESS_01'];
    const results = await Promise.all(
        tags.map(tag =>
            fetch(`/machbase?q=${encodeURIComponent(
                `SELECT /*+ SCAN_BACKWARD(sensor_tag) */ name, time, value
                   FROM sensor_tag WHERE name='${tag}' LIMIT 1`
            )}`).then(r => r.json())
        )
    );
    updateDashboard(results);
}

// 2초마다 폴링
setInterval(fetchLatestValues, 2000);
```

---

## 5단계: 폴링 주기 최적화

| 폴링 주기 | 적합한 사용 사례 | 주의사항 |
|-----------|-----------------|---------|
| 1초 이하 | 긴급 알람, 안전 시스템 | DB 부하 증가, 연결 수 관리 필요 |
| 1~2초 | 실시간 모니터링 (권장) | 일반적인 대시보드에 적합 |
| 3~5초 | 일반 상태판, KPI 화면 | 센서 수집 주기보다 짧게 유지 |
| 10초 이상 | 요약·집계 지표 | 집계 쿼리와 조합 가능 |

폴링 요청을 줄이려면 여러 태그를 단일 쿼리로 묶어 조회하고, 변경된 값만 화면에 업데이트하는 방식을 사용합니다.

```python
import requests
import time

MACHBASE_URL = "http://localhost:5657/machbase"

def get_dashboard_data():
    query = """
    SELECT t.name, t.time, t.value,
           CASE WHEN t.value >= 90 THEN 'CRITICAL'
                WHEN t.value >= 80 THEN 'WARNING'
                ELSE 'NORMAL' END AS status
      FROM sensor_tag t
      JOIN (SELECT name, recent_row_time AS mt FROM v$sensor_tag_stat) s
        ON t.name = s.name AND t.time = s.mt
     ORDER BY t.name
    """
    resp = requests.get(MACHBASE_URL, params={"q": query})
    return resp.json()

while True:
    data = get_dashboard_data()
    for row in data["data"]["rows"]:
        name, ts, value, status = row
        print(f"{name:12s} | {ts} | {value:8.2f} | {status}")
    print("---")
    time.sleep(2)
```

---

## 6단계: Grafana 등 외부 도구 연동 시 고려사항

Grafana와 같은 외부 시각화 도구를 연동할 때는 다음 사항을 고려합니다.

**데이터 소스 설정**

Machbase는 JDBC(또는 ODBC) 드라이버를 통해 Grafana의 Generic JDBC 데이터 소스 플러그인과 연동됩니다.

```
JDBC URL: jdbc:machbase://localhost:5656/machbasedb
Driver:   com.machbase.jdbc.MachbaseDriver
```

**패널 쿼리 작성 시 주의사항**

- Grafana의 시간 범위 변수(`$__timeFrom`, `$__timeTo`)를 Machbase의 `TO_DATE()` 함수로 변환해야 합니다.
- TAG 테이블 조회 시 `name` 조건을 반드시 지정해 전체 테이블 스캔을 방지합니다.
- 대시보드 리프레시 주기는 Grafana 패널 설정의 "Refresh" 옵션으로 제어합니다.

```sql
-- Grafana 패널용 쿼리 예시 (시간 범위 변수 활용)
SELECT time       AS "time",
       value      AS "온도(°C)"
  FROM sensor_tag
 WHERE name = 'TEMP_01'
   AND time BETWEEN TO_DATE('$__timeFrom', 'YYYY-MM-DD HH24:MI:SS')
               AND TO_DATE('$__timeTo',   'YYYY-MM-DD HH24:MI:SS')
 ORDER BY time;
```

**연결 풀 설정**

여러 Grafana 패널이 동시에 쿼리를 실행하면 연결 수가 급증할 수 있습니다. Machbase 서버의 최대 연결 수 설정을 확인합니다.

```ini
# machbase.conf
MAX_SESSION_COUNT = 100
```

---

## 참고

- TAG 테이블 조회 패턴: [../../../core-concepts/data-model](../../../core-concepts/data-model)
- 통계 가상 테이블(`v$<table>_stat`) 활용은 대량 태그 환경에서 최신값 조회 성능을 크게 향상시킵니다.
- 상태 알람 자동화는 [../stream-log-tag](../stream-log-tag) 시나리오를 참고하세요.
