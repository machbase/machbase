---
type: docs
title: 'RDB 테이블 설계'
weight: 30
---

RDB 테이블은 Machbase 8.6에서 도입된 일반 관계형 테이블입니다. SELECT·INSERT·UPDATE·DELETE를 모두 지원하며, PRIMARY KEY 인덱스와 보조 인덱스를 사용합니다.

```sql
CREATE RDB TABLE order_history (
    order_id  LONG,
    item_id   INTEGER,
    qty       INTEGER,
    amount    DOUBLE
);

UPDATE order_history SET qty = 10 WHERE order_id = 1001;
DELETE FROM order_history WHERE order_id = 1001;
```

## 이 섹션의 구성

- **[활용 사례](/dbms/rdb-table-usage/patterns-scenarios/use-cases-rdb/)**
- **[스키마 설계](/dbms/rdb-table-usage/table-structure-schema/rdb-table-design/design-schema-type-rdb/)**
- **[PRIMARY KEY·UNIQUE·일반 인덱스 전략](/dbms/rdb-table-usage/rdb-index-json-path/index-strategy-rdb-primary-key-unique-normal/)**
- **[JSON 경로 인덱스](/dbms/rdb-table-usage/rdb-index-json-path/index-strategy-rdb-json-path/)**
- **[트랜잭션 설계](/dbms/rdb-table-usage/transaction/design-transaction-rdb/)**
- **[UPDATE·DELETE 설계](/dbms/rdb-table-usage/data-input-mutation/modeling-rdb-update-delete/)**
- **[잠금·충돌·타임아웃 설계](/dbms/rdb-table-usage/locking-conflict-timeout/design-locking-conflict-rdb-busy-timeout-ddl-dml/)**
- **[자기 참조·INSERT SELECT](/dbms/rdb-table-usage/data-input-mutation/reference-self-rdb-insert-select/)**
- **[JOIN 설계](/dbms/rdb-table-usage/join-relational-query/join-design-rdb/)**
- **[백업·마운트](/dbms/rdb-table-usage/backup-mount-sidecar/design-backup-mount-rdb/)**
- **[Append API](/dbms/rdb-table-usage/sdk-append-scope/unsupported-rejected-rdb-append-api/)**
- **[SDK 지원 범위](/dbms/rdb-table-usage/sdk-append-scope/support-scope-rdb-sdk/)**
- **[Edition 제한](/dbms/rdb-table-usage/constraints-errors-troubleshooting/limitations-rdb-edition/)**
