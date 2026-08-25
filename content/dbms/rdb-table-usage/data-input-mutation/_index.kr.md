---
title: '8.4 데이터 입력과 변경'
weight: 40
toc: true
aliases:
  - /dbms/rdb-table-usage/sdk-append-scope/
---
TRANSACTION 테이블은 일반 `INSERT`, `UPDATE`, `DELETE`와 `INSERT ... SELECT`를 지원합니다.
UPSERT는 [INSERT ON DUPLICATE KEY UPDATE](../insert-on-duplicate-key-update/), 자동 번호 키는
[AUTO_INCREMENT](/dbms/reference/sql/syntax-dictionary-sql/auto-increment-syntax/)를 참고하십시오.

<a id="modeling-rdb-update-delete"></a>

## UPDATE·DELETE

다음 예제는 스키마와 초기 데이터를 포함하므로 그대로 실행할 수 있습니다.

```sql
CREATE TRANSACTION TABLE mutation_orders (
    order_id   LONG PRIMARY KEY,
    customer   VARCHAR(64),
    amount     DOUBLE,
    status     VARCHAR(16),
    order_time DATETIME
);

INSERT INTO mutation_orders
VALUES (1001, 'CUST-001', 19900, 'PENDING',
        TO_DATE('2026-01-01', 'YYYY-MM-DD'));
INSERT INTO mutation_orders
VALUES (1002, 'CUST-002', 29900, 'CANCELLED',
        TO_DATE('2026-01-02', 'YYYY-MM-DD'));

UPDATE mutation_orders
   SET status = 'SHIPPED'
 WHERE order_id = 1001 AND status = 'PENDING';

DELETE FROM mutation_orders
 WHERE status = 'CANCELLED';

SELECT order_id, customer, amount, status
  FROM mutation_orders
 ORDER BY order_id;
```

조건 없는 `UPDATE`와 `DELETE`는 전체 행을 대상으로 합니다. 운영 전에 같은 `WHERE` 조건의
`SELECT`로 대상 건수를 확인하고, 자주 사용하는 조건 컬럼에는 실제 실행 계획을 확인한 뒤
인덱스를 설계하십시오.

<a id="reference-self-rdb-insert-select"></a>

## INSERT SELECT

다른 테이블의 결과를 복사하거나 같은 테이블의 행을 변환해 삽입할 수 있습니다.

```sql
CREATE TRANSACTION TABLE mutation_order_archive (
    order_id   LONG PRIMARY KEY,
    customer   VARCHAR(64),
    amount     DOUBLE,
    status     VARCHAR(16),
    order_time DATETIME
);

INSERT INTO mutation_order_archive
SELECT order_id, customer, amount, status, order_time
  FROM mutation_orders
 WHERE order_time < TO_DATE('2026-02-01', 'YYYY-MM-DD');

INSERT INTO mutation_orders
    (order_id, customer, amount, status, order_time)
SELECT order_id + 10000, 'TEST-001', amount, status, order_time
  FROM mutation_orders
 WHERE customer = 'CUST-001';

SELECT COUNT(*) FROM mutation_order_archive;

DROP TABLE mutation_order_archive;
DROP TABLE mutation_orders;
```

SELECT 결과의 컬럼 수와 타입은 대상 컬럼 목록과 일치해야 합니다. constraint 오류가 발생하면
해당 statement의 삽입은 롤백됩니다. 대량 이관은 재시작 가능한 범위로 나누고 처리 건수를
기록하십시오.

<a id="unsupported-rejected-rdb-append-api"></a>
<a id="support-scope-rdb-sdk"></a>

## 대량 입력과 Append

TRANSACTION 테이블도 Append API를 지원하지만 TAG·LOG의 지속 수집 경로와 같은 처리량을
가정하지 않습니다. 관계형 제약과 transaction 경로를 거치므로 대표 데이터로 일반 INSERT,
prepared batch와 Append를 비교하십시오.

| 입력 방식 | 사용 기준 |
|---|---|
| prepared batch | transaction 단위와 오류 위치를 명확히 관리할 때 |
| Append API | 지원 SDK에서 정형 batch를 연속 입력할 때 |
| machloader | 파일과 schema mapping으로 일괄 입력할 때 |

`AUTO_INCREMENT` 컬럼을 SQLCLI `SQLAppendBatch()`에서 처리하는 방식과 DECIMAL 입력 타입은
[SQLCLI와 ODBC](/dbms/development-tools-integration/cli-odbc/)를 참고하십시오. 언어별 Append
지원은 [SDK 기능 지원 범위](/dbms/development-tools-integration/sdk-support-scope/#support-scope-sdk-append)를
확인합니다.
