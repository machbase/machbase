---
type: docs
title: 'Log 테이블'
weight: 20
---

Log 테이블에 대한 완전한 참조 - 이벤트 스트림, 애플리케이션 로그 및 타임스탬프 데이터를 위한 Machbase의 유연한 테이블 타입입니다.

## 개요

Log 테이블은 유연한 스키마를 가진 추가 전용 이벤트 데이터에 최적화되어 있습니다. 나노초 정밀도의 타임스탬프를 자동으로 추가하고 전체 텍스트 검색을 지원합니다.

## 주요 기능

- **초당 수백만 건의 삽입**
- **자동 _arrival_time** 컬럼 (나노초 정밀도)
- **유연한 스키마** (모든 컬럼)
- **전체 텍스트 검색** (SEARCH 키워드 사용)
- **최신 데이터 우선** (자동 정렬)
- **선택적 LSM 인덱싱**

## 기본 구문

```sql
CREATE TABLE table_name (
    column1 data_type,
    column2 data_type,
    ...
);
-- _arrival_time 자동 추가
```

## 사용 시기

- 애플리케이션 로그
- HTTP 액세스 로그
- 이벤트 스트림
- 트랜잭션 로그
- 타임스탬프가 있는 모든 이벤트 데이터

## 관련 문서

- [튜토리얼: 애플리케이션 로그](../../tutorials/application-logs/)
- [핵심 개념: 테이블 타입](../../core-concepts/table-types-overview/)
- 원본 참조: [Log 테이블](../../../dbms/feature-table/log/)
