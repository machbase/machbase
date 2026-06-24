---
type: docs
title: 'Lookup 테이블'
weight: 40
---

참조 데이터를 위한 Machbase의 영구 primary-key 테이블 타입인 Lookup 테이블에 대한 완전한 레퍼런스입니다.

## 개요

Lookup 테이블은 영구 참조 데이터를 저장하고 단일 primary-key 메모리 인덱스를
유지합니다. 전체 CRUD 작업을 지원하지만 쿼리와 row 변경은 primary key 중심으로
설계해야 합니다.

## 주요 기능

- **전체 CRUD 지원** (INSERT, UPDATE, DELETE, SELECT)
- **영구 데이터**
- **단일 primary-key 메모리 인덱스**
- **빠른 primary-key 읽기**
- **시계열 테이블과의 JOIN**

## 기본 구문

```sql
CREATE LOOKUP TABLE table_name (
    key_column data_type PRIMARY KEY,
    column2 data_type,
    ...
);
```

## 사용 시기

- 디바이스 레지스트리
- 설정 테이블
- 카테고리/차원 테이블
- 마스터 데이터
- 하나의 primary key로 접근하는 참조 데이터

## 사용하지 말아야 할 경우

- 고빈도 삽입 (Tag/Log 테이블 사용)
- 시계열 데이터
- 초당 수백만 건의 쓰기가 필요한 데이터
- 여러 보조 인덱스 또는 일반 predicate가 필요한 워크로드 (RDB 사용)

## 관련 문서

- [Lookup 데이터 입력](./inserting-data/)
- [핵심 개념: 테이블 타입](../../core-concepts/table-types-overview/)
