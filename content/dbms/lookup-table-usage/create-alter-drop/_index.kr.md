---
title: '9.3 생성, 변경, 삭제'
weight: 30
toc: true
---
LOOKUP 테이블의 생성, 변경, 삭제 방법을 다룬다.


<a id="original-85-creating-lookup-tables"></a>

## Lookup 테이블 생성 및 관리


참조 테이블을 생성하는 방법은 다음과 같다.

### Lookup 테이블 생성

```sql
CREATE LOOKUP TABLE lktable (id INTEGER PRIMARY KEY, name VARCHAR(20));
```

Lookup 테이블은 반드시 Primary key를 지정해야 한다.


### Lookup 테이블 삭제

```sql
DROP TABLE lktable;
```
