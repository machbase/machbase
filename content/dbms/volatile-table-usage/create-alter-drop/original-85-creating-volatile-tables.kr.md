---
title : Volatile 테이블 생성 및 관리
type : docs
weight: 10
---

> **8.5 원문 보강 자료**: 이 문서는 기존 8.5 매뉴얼의 내용을 새 장 구조에 맞춰 보존한 것입니다. Machbase 8.6 기준과 표현이 다른 부분은 같은 절의 최신 리뉴얼 문서를 우선합니다.

volatile 테이블의 생성 및 삭제 방법은 다음과 같습니다.

## 생성

```sql
create volatile table vtable (id1 integer, name varchar(20));
```


## 삭제

```sql
drop table vtable;
```
