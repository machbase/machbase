---
title : Lookup 테이블 생성 및 관리
type: docs
weight: 10
---

참조 테이블을 생성하는 방법은 다음과 같습니다.

## Lookup 테이블 생성

```sql
CREATE LOOKUP TABLE lktable (id INTEGER PRIMARY KEY, name VARCHAR(20));
```

Lookup 테이블은 반드시 Primary key를 지정해야 합니다.


## Lookup 테이블 삭제

```sql
DROP TABLE lktable;
```
