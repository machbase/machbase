---
title : Lookup 인덱스 생성 및 관리
type: docs
weight: 50
---

Lookup 테이블은 primary key에 대한 단일 메모리 인덱스를 사용합니다. Lookup 쿼리,
업데이트, 삭제는 primary-key predicate 중심으로 설계합니다. `KEYWORD` 인덱스는
LOG 테이블에서만 사용할 수 있으며, 여러 보조 인덱스나 JSON path 인덱스가 필요한
영구 row 테이블에는 RDB 테이블을 사용합니다.

```sql
CREATE LOOKUP TABLE lookup_table (code INTEGER PRIMARY KEY, name VARCHAR(20));

SELECT name FROM lookup_table WHERE code = 100;
UPDATE lookup_table SET name = 'sensor-a' WHERE code = 100;
```
