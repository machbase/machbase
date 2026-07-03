---
type: docs
title: '첫 데이터 입력과 조회'
weight: 40
toc: true
---

테이블을 만든 뒤에는 `INSERT`로 데이터를 입력하고 `SELECT`로 바로 확인합니다. 데이터를
넣기만 하고 확인하지 않으면 영수증을 보지 않고 결제를 끝낸 것과 같습니다. 이 페이지의
예제는 두 행을 입력하고 `ORDER BY`로 결과 순서를 고정합니다.

시계열 데이터에서는 입력 순서와 조회 순서가 중요합니다. 특히 금융 틱이나 설비 이벤트처럼
짧은 시간에 많은 행이 들어오는 데이터는 시간 또는 순번 기준으로 결과를 재현할 수 있어야
분석과 검증이 쉬워집니다.

## INSERT와 SELECT 예제

```sql
CREATE TABLE DBMS_GS_SAMPLE (
  EVENT_ID INTEGER,
  LEVEL VARCHAR(10),
  MESSAGE VARCHAR(80)
);

INSERT INTO DBMS_GS_SAMPLE VALUES (1, 'INFO', 'service started');
INSERT INTO DBMS_GS_SAMPLE VALUES (2, 'WARN', 'queue depth high');

SELECT EVENT_ID, LEVEL, MESSAGE
FROM DBMS_GS_SAMPLE
ORDER BY EVENT_ID;

DROP TABLE DBMS_GS_SAMPLE;
```

위 SQL이 `/tmp/dbms_gs_insert_query.sql` 파일에 저장되어 있다고 가정하고 다음 명령을 실행합니다.

```bash
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER -f /tmp/dbms_gs_insert_query.sql
```

정상적으로 실행되면 `service started`, `queue depth high` 두 행이 출력됩니다. 첫 번째
행은 서비스가 시작된 상태를, 두 번째 행은 큐 적재량이 높아진 상태를 나타냅니다. 실제
운영 로그에서는 이런 작은 문장들이 모여 장애 원인 분석이나 성능 추세 분석의 재료가 됩니다.
재실행 중 `DBMS_GS_SAMPLE`이 이미 존재한다는 오류가 나면
`DROP TABLE DBMS_GS_SAMPLE;`를 실행한 뒤 다시 시작합니다.
