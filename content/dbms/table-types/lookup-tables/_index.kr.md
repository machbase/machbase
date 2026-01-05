---
type: docs
title: 'Lookup 테이블'
weight: 40
---

참조 데이터, 마스터 데이터 및 차원 테이블을 위한 Machbase의 테이블 타입인 Lookup 테이블에 대한 완전한 레퍼런스입니다.

## 개요

Lookup 테이블은 드물게 변경되지만 자주 읽히는 참조 데이터에 최적화된 디스크 기반 테이블입니다. 전체 CRUD 작업을 지원하며 디바이스 레지스트리 및 설정 정보에 이상적입니다.

## 주요 기능

- **전체 CRUD 지원** (INSERT, UPDATE, DELETE, SELECT)
- **영구 디스크 스토리지**
- **빠른 읽기 성능**
- **시계열 테이블과의 JOIN**
- **선택적 LSM 인덱싱**

## 기본 구문

```sql
CREATE LOOKUP TABLE table_name (
    column1 data_type,
    column2 data_type,
    ...
);
```

## 사용 시기

- 디바이스 레지스트리
- 설정 테이블
- 카테고리/차원 테이블
- 마스터 데이터
- 드물게 변경되는 참조 데이터

## 사용하지 말아야 할 경우

- 고빈도 삽입 (Tag/Log 테이블 사용)
- 시계열 데이터
- 초당 수백만 건의 쓰기가 필요한 데이터

## 관련 문서

- [튜토리얼: 참조 데이터](../../tutorials/reference-data/)
- [핵심 개념: 테이블 타입](../../core-concepts/table-types-overview/)
- 원본 레퍼런스: [Lookup Tables](../../../dbms/feature-table/lookup/)
