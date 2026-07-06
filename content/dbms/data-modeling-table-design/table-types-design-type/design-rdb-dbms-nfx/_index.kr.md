---
type: docs
title: 'RDB 테이블 설계'
weight: 30
---

RDB 테이블은 Machbase 8.6에서 도입된 관계형 구조의 테이블 타입입니다. Key-Value 기반 스토리지를 사용하며, 대량 데이터의 SELECT·INSERT·DELETE 워크로드에 적합합니다.

```sql
CREATE RDB TABLE order_history (
    order_id  LONG,
    item_id   INTEGER,
    qty       INTEGER,
    amount    DOUBLE
);
```

## 이 섹션의 구성

- **[활용 사례](/dbms/data-modeling-table-design/table-types-design-type/design-rdb-dbms-nfx/use-cases-rdb/)**
- **[스키마 설계](/dbms/data-modeling-table-design/table-types-design-type/design-rdb-dbms-nfx/design-schema-type-rdb/)**
- **[PRIMARY KEY·UNIQUE·일반 인덱스 전략](/dbms/data-modeling-table-design/table-types-design-type/design-rdb-dbms-nfx/index-strategy-rdb-primary-key-unique-normal/)**
- **[JSON 경로 인덱스](/dbms/data-modeling-table-design/table-types-design-type/design-rdb-dbms-nfx/index-strategy-rdb-json-path/)**
- **[트랜잭션 설계](/dbms/data-modeling-table-design/table-types-design-type/design-rdb-dbms-nfx/design-transaction-rdb/)**
- **[UPDATE·DELETE 모델링](/dbms/data-modeling-table-design/table-types-design-type/design-rdb-dbms-nfx/modeling-rdb-update-delete/)**
- **[잠금·충돌·타임아웃 설계](/dbms/data-modeling-table-design/table-types-design-type/design-rdb-dbms-nfx/design-locking-conflict-rdb-busy-timeout-ddl-dml/)**
- **[자기 참조·INSERT SELECT](/dbms/data-modeling-table-design/table-types-design-type/design-rdb-dbms-nfx/reference-self-rdb-insert-select/)**
- **[JOIN 설계](/dbms/data-modeling-table-design/table-types-design-type/design-rdb-dbms-nfx/join-design-rdb/)**
- **[백업·마운트](/dbms/data-modeling-table-design/table-types-design-type/design-rdb-dbms-nfx/design-backup-mount-rdb/)**
- **[Append API 미지원](/dbms/data-modeling-table-design/table-types-design-type/design-rdb-dbms-nfx/unsupported-rejected-rdb-append-api/)**
- **[SDK 지원 범위](/dbms/data-modeling-table-design/table-types-design-type/design-rdb-dbms-nfx/support-scope-rdb-sdk/)**
- **[Edition 제한](/dbms/data-modeling-table-design/table-types-design-type/design-rdb-dbms-nfx/limitations-rdb-edition/)**
