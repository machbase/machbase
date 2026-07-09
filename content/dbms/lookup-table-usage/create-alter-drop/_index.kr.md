---
title: '9.3 생성, 변경, 삭제'
weight: 30
toc: true
---
생성, 변경, 삭제에 해당하는 세부 문서를 모았습니다.


<a id="original-85-creating-lookup-tables"></a>

## Lookup 테이블 생성 및 관리

> **8.5 원문 보강 자료**: 이 문서는 기존 8.5 매뉴얼의 내용을 새 장 구조에 맞춰 보존한 것입니다. Machbase 8.6 기준과 표현이 다른 부분은 같은 절의 최신 리뉴얼 문서를 우선합니다.

참조 테이블을 생성하는 방법은 다음과 같습니다.

### Lookup 테이블 생성

```sql
CREATE LOOKUP TABLE lktable (id INTEGER PRIMARY KEY, name VARCHAR(20));
```

Lookup 테이블은 반드시 Primary key를 지정해야 합니다.


### Lookup 테이블 삭제

```sql
DROP TABLE lktable;
```
