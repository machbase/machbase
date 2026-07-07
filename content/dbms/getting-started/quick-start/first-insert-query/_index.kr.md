---
type: docs
title: '첫 데이터 입력과 조회'
weight: 40
toc: true
---

테이블을 만든 뒤에는 `INSERT`로 데이터를 입력하고 `SELECT`로 즉시 확인합니다. 데이터를 넣기만 하고 확인하지 않으면 결과를 모른 채 작업을 진행하는 것과 같습니다. 이 페이지의 예제는 두 행을 입력하고 `ORDER BY`로 결과 순서를 고정해 재현 가능한 출력을 보장합니다.

시계열 데이터에서는 입력 순서와 조회 순서가 중요합니다. 금융 틱이나 설비 이벤트처럼 짧은 시간에 많은 행이 유입되는 데이터는 시간 또는 순번 기준으로 결과를 재현할 수 있어야 분석과 검증이 수월해집니다.

이 예제의 `ORDER BY EVENT_ID`는 출력 재현성을 위한 것입니다. LOG 테이블의 최근 데이터 확인은 `_arrival_time` 기준으로 이해해야 하며, 명시적으로 고정하려면 `ORDER BY _arrival_time DESC`를 사용합니다.

## INSERT와 SELECT 예제

```sql
CREATE TABLE DBMS_GS_SAMPLE (
  EVENT_ID INTEGER,
  LEVEL VARCHAR(10),
  MESSAGE VARCHAR(80)
);

INSERT INTO DBMS_GS_SAMPLE VALUES (1, 'INFO', 'service started');
INSERT INTO DBMS_GS_SAMPLE VALUES (2, 'WARN', 'queue depth high');

SELECT _arrival_time, EVENT_ID, LEVEL, MESSAGE
FROM DBMS_GS_SAMPLE
ORDER BY EVENT_ID;

SELECT _arrival_time, EVENT_ID, LEVEL, MESSAGE
FROM DBMS_GS_SAMPLE
DURATION 10 MINUTE;

DROP TABLE DBMS_GS_SAMPLE;
```

위 SQL이 `/tmp/dbms_gs_insert_query.sql` 파일에 저장되어 있다고 가정하고 다음 명령을 실행합니다.

```bash
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER -f /tmp/dbms_gs_insert_query.sql
```

정상적으로 실행되면 `service started`, `queue depth high` 두 행이 순서대로 출력됩니다. `_arrival_time`은 LOG 테이블에 자동 추가되는 서버 수신 시각입니다. 실제 이벤트 발생 시각이 필요하면 별도 `DATETIME` 컬럼을 정의합니다. `DURATION`은 LOG 테이블에서 `_arrival_time` 기준으로 동작하고, TAG 테이블에서는 `BASETIME` 컬럼 기준으로 동작합니다. 재실행 중 `DBMS_GS_SAMPLE`이 이미 존재한다는 오류가 나면 `DROP TABLE DBMS_GS_SAMPLE;`를 실행한 뒤 다시 시작합니다.
