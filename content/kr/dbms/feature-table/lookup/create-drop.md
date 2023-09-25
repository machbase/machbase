---
title : '참조 테이블 생성 및 관리'
type: docs
weight: 10
---

참조 테이블의 생성 방법은 다음과 같다.

## 생성

참조 테이블은 Primary Key를 반드시 지정해야한다.

```sql
CREATE LOOKUP TABLE lktable (id INTEGER PRIMARY KEY, name VARCHAR(20));
```

## 삭제

```sql
DROP TABLE lktable;
```
