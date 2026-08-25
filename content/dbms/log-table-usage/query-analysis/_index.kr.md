---
title: '7.5 조회와 분석'
weight: 50
toc: true
---
LOG 테이블은 `_arrival_time` 범위와 업무 조건을 함께 사용해 조회 범위를 줄입니다. 결과
순서가 중요하면 기본 스캔 방향에 기대지 말고 `ORDER BY`를 명시하십시오.

<a id="original-85-select-data"></a>

## 기본 조회

다음 예제는 고정된 수신 시각을 사용해 조건 조회와 시간 범위 조회를 재현합니다.

```sql
CREATE LOG TABLE query_log (
    event_time DATETIME,
    device     VARCHAR(32),
    value      DOUBLE
);

INSERT INTO query_log(_arrival_time, event_time, device, value)
VALUES (TO_DATE('2026-01-01', 'YYYY-MM-DD'),
        TO_DATE('2026-01-01', 'YYYY-MM-DD'), 'DEV-01', 10.0);
INSERT INTO query_log(_arrival_time, event_time, device, value)
VALUES (TO_DATE('2026-01-02', 'YYYY-MM-DD'),
        TO_DATE('2026-01-02', 'YYYY-MM-DD'), 'DEV-02', 20.0);

SELECT _arrival_time, device, value
  FROM query_log
 WHERE value >= 10
 ORDER BY _arrival_time;
```

`_arrival_time`은 서버가 행을 받은 시각입니다. 이벤트가 실제로 발생한 시각이 필요하면 예제의
`event_time`처럼 별도 컬럼을 저장하고 두 의미를 구분하십시오.

<a id="original-85-select-time-data"></a>

## DURATION 시간 범위

`DURATION`은 `_arrival_time`을 기준으로 상대 또는 절대 범위를 지정합니다.

```sql
SELECT _arrival_time, device, value
  FROM query_log
  DURATION 2 DAY
  BEFORE TO_DATE('2026-01-03', 'YYYY-MM-DD');
```

`BEFORE`, `AFTER`, `FROM ... TO ...`의 경계와 결과 방향은
[상대 시간 표현 사전](/dbms/reference/sql/relative-time-dictionary/)을 기준으로
확인하십시오. 사용자 정의 `event_time` 범위에는 일반 `WHERE` 조건을 사용합니다.

## 스캔 방향과 실행 계획

스캔 힌트가 필요한 쿼리는 대표 데이터로 결과 순서와 실행 시간을 먼저 확인합니다. 전역
`TABLE_SCAN_DIRECTION` 설정은 다른 쿼리에도 영향을 주므로, 단순히 출력 순서를 바꾸려는
목적으로 변경하지 마십시오.

- [SELECT와 스캔 힌트](/dbms/reference/sql/syntax-dictionary-sql/select-hint-syntax/)
- [쿼리 튜닝](/dbms/performance-tuning/query-tuning/)

<a id="original-85-simple-join"></a>

## LOOKUP 조인

장치 이름·위치 같은 기준 정보는 작은 LOOKUP 테이블에 저장하고 LOG의 식별자와 조인할 수
있습니다. 조인 전에 LOG 시간 범위를 가능한 한 제한합니다.

```sql
CREATE LOOKUP TABLE query_device (
    device VARCHAR(32) PRIMARY KEY,
    label  VARCHAR(64)
);

INSERT INTO query_device VALUES ('DEV-01', 'Boiler');
INSERT INTO query_device VALUES ('DEV-02', 'Pump');

SELECT q.device, d.label, q.value
  FROM query_log q
  JOIN query_device d ON q.device = d.device
 ORDER BY q.device;

DROP TABLE query_device;
DROP TABLE query_log;
```

조인 조건 없는 Cartesian join은 사용하지 않습니다. 여러 대형 LOG 테이블을 직접 조인해야
한다면 시간 조건, 인덱스와 비정규화 대안을 함께 검토하십시오.

문자열·정규식·네트워크 주소 검색은 [정규식과 네트워크 조회](../regex-network-query/)를,
전문 검색은 [텍스트 검색과 KEYWORD 인덱스](../text-search-keyword-index/)를 참고하십시오.
