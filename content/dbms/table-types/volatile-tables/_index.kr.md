---
type: docs
title: 'Volatile 테이블'
weight: 30
---

Volatile 테이블에 대한 완전한 참조 - 실시간, 빈번하게 업데이트되는 데이터를 위한 Machbase의 인메모리 테이블 유형입니다.

## 개요

Volatile 테이블은 최대 속도를 위해 모든 데이터를 메모리에 저장합니다. PRIMARY KEY로 UPDATE 및 DELETE 작업을 지원하여 실시간 대시보드와 세션 관리에 이상적입니다.

## 주요 기능

- **100% 인메모리** 저장소
- PRIMARY KEY로 **UPDATE 및 DELETE** 지원
- 초당 **수만 건의 작업** 처리
- **빠른 키 기반 조회** (O(log n))
- **경고: 종료 시 데이터 손실**

## 기본 구문

```sql
CREATE VOLATILE TABLE table_name (
    key_column data_type PRIMARY KEY,
    column1 data_type,
    column2 data_type,
    ...
);
```

## 사용 시기

- 실시간 대시보드
- 사용자 세션
- 실시간 상태 보드
- 캐싱 레이어
- 임시 계산

## 사용하지 말아야 할 때

- 영구 보존이 필요한 데이터
- 대용량 스트리밍 데이터 (대신 Tag/Log 사용)
- 대규모 데이터셋 (RAM으로 제한됨)

## 관련 문서

- [튜토리얼: 실시간 분석](../../tutorials/realtime-analytics/)
- [핵심 개념: 테이블 유형](../../core-concepts/table-types-overview/)
- 원본 참조: [Volatile 테이블](../../../dbms/feature-table/volatile/)
