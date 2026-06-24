---
type: docs
title: 'Volatile 테이블'
weight: 30
---

Volatile 테이블에 대한 완전한 참조입니다. Volatile 테이블은 Machbase의 비영구 메모리 primary-key 테이블 타입입니다.

## 개요

Volatile 테이블은 모든 데이터를 메모리에 저장하며 서버 재시작 후 row를 보존하지
않습니다. 각 Volatile 테이블은 단일 primary-key 메모리 인덱스를 가지며 `UPDATE`,
`DELETE`, point lookup은 이 primary key를 중심으로 사용합니다.

## 주요 기능

- **100% 인메모리** 저장소
- **비영구** row
- **단일 primary-key 메모리 인덱스**
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
- 비영구 key-value 형태의 상태

## 사용하지 말아야 할 때

- 영구 보존이 필요한 데이터
- 대용량 스트리밍 데이터 (대신 Tag/Log 사용)
- 대규모 데이터셋 (RAM으로 제한됨)

## 관련 문서

- [데이터 입력 및 갱신](./insert-update/)
- [핵심 개념: 테이블 유형](../../core-concepts/table-types-overview/)
