---
title : '휘발성 테이블 생성 및 관리'
type : docs
weight: 10
---

휘발성 테이블의 생성과 삭제 방식은 다음과 같다.

## 생성

```sql
create volatile table vtable (id1 integer, name varchar(20));
```

## 삭제

```sql
drop table vtable;
```
