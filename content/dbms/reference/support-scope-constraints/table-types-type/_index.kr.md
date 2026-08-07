---
type: docs
title: '18.8.2 테이블 타입별 기능 지원표'
weight: 20
toc: true
---

Machbase는 용도에 따라 다섯 가지 테이블 유형을 제공합니다. 각 테이블 유형은 설계 목적에 따라 지원하는 기능 범위가 다릅니다.

## 테이블 유형 개요

| 테이블 유형 | 주요 용도 |
|------------|----------|
| **TAG** | 시계열 센서 데이터 고속 수집 및 집계 (ROLLUP) |
| **LOG** | 비정형 로그/이벤트 데이터 순차 저장, 텍스트 검색 |
| **LOOKUP** | 메타데이터, 코드 테이블, 참조 데이터 (UPDATE/DELETE 지원) |
| **VOLATILE** | 메모리 기반 서버 상태·캐시, 재시작 시 데이터 소멸 |
| **TRANSACTION** | 트랜잭션이 필요한 일반 관계형 데이터 |

## 테이블 유형별 기능 지원 종합 표

| 기능 | TAG | LOG | LOOKUP | VOLATILE | TRANSACTION |
|------|:---:|:---:|:------:|:--------:|:---:|
| **쓰기** | | | | | |
| INSERT (SQL) | O | O | O | O | O |
| Append API | O | O | O | X | O |
| **수정/삭제** | | | | | |
| UPDATE | △ | X | O | O | O |
| DELETE | O | O | O | O | O |
| **트랜잭션** | | | | | |
| Transaction (COMMIT/ROLLBACK) | X | X | X | X | O |
| **집계 및 검색** | | | | | |
| ROLLUP | O | X | X | X | X |
| 텍스트 검색 (KEYWORD INDEX) | X | O | X | X | X |
| **JSON** | | | | | |
| JSON 컬럼 | O | O | O | X | O |
| JSON path query | O | O | O | X | O |
| **고정소수점** | | | | | |
| DECIMAL / NUMERIC 컬럼 | O | O | O | O | O |
| **인덱스** | | | | | |
| 기본 인덱스 | O | O | O | O | O |
| LSM 인덱스 | X | O | X | X | X |
| **조회** | | | | | |
| SELECT | O | O | O | O | O |
| RECENT N | O | O | X | X | X |
| JOIN (다른 테이블과) | △ | △ | O | O | O |
| Subquery | O | O | O | O | O |
| VIEW | O | O | O | O | O |

> 기호: O = 지원, X = 미지원, △ = 일부 지원 또는 제약 있음

DECIMAL은 모든 public 테이블 타입의 공통 exact fixed-point 타입입니다. `NUMERIC`, `DEC`,
`FIXED`, `NUMBER`는 DECIMAL alias이며, precision은 최대 65, scale은 최대 30입니다. 상세 규칙은
[DECIMAL과 NUMERIC 고정소수점 타입](../../sql/type-data-types-dictionary/decimal-numeric-fixed-point/)을
참고하십시오.

## 주요 제약 상세

### TAG 테이블 UPDATE 제약 (△)

TAG 테이블의 UPDATE는 다음 조건을 모두 만족해야 합니다.

- `WHERE` 절에 태그 선택 조건(`name =`, `name IN`, `name LIKE`) 포함
- `WHERE` 절에 BASETIME 컬럼 조건 포함
- SET 대상은 실제 데이터 컬럼
- `time` (BASETIME) 컬럼과 `name` 컬럼, 메타데이터 컬럼은 data UPDATE로 수정 불가

```sql
-- 가능: 태그 조건과 시간 조건으로 데이터 컬럼 업데이트
UPDATE sensor_data
   SET value = value + 1
 WHERE name = 'sensor01'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');

-- 불가: BASETIME 컬럼 업데이트
UPDATE sensor_data
   SET time = NOW()
 WHERE name = 'sensor01'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');
```

상세 내용은 [TAG data UPDATE 지원표](../tag-data-update/)를 참고하십시오.

### LOOKUP과 VOLATILE의 트랜잭션 범위

LOOKUP과 VOLATILE 테이블의 각 DML은 statement 단위로 반영됩니다. 여러 DML을 `BEGIN`과
`COMMIT`/`ROLLBACK`으로 묶는 TRANSACTION 테이블 트랜잭션에는 참여하지 않습니다.

### JSON 컬럼 지원 범위

JSON 컬럼은 TAG, LOG, LOOKUP, TRANSACTION 테이블에서 지원합니다. VOLATILE 테이블은 JSON 타입 컬럼 생성을 지원하지 않습니다. LOOKUP 테이블의 JSON 컬럼은 일반 컬럼으로 사용할 수 있지만 primary key로는 사용할 수 없습니다. 상세 내용은 [JSON 타입의 테이블 타입별 지원 범위](../../sql/type-data-types-dictionary/table-types-type-support-scope-json/)를 참고하십시오.

### Append API 대상 테이블

Append API는 TAG, LOG, LOOKUP 테이블에 사용할 수 있습니다. LOOKUP 테이블은 중복 키 처리
정책(`LOOKUP_APPEND_UPDATE_ON_DUPKEY`)을 함께 확인하십시오. TRANSACTION 테이블은 지원되는 client의
appendBatch 또는 append stream 경로를 사용하며, VOLATILE 테이블에는 일반 `INSERT` SQL을
사용합니다.

## TAG 테이블 시간 범위 조회

TAG 테이블은 시계열 조회에 최적화된 특수 문법을 지원합니다.

```sql
-- 최신 5개 값 조회
SELECT * FROM sensor_data RECENT 5;

-- 시간 범위 조회
SELECT * FROM sensor_data
WHERE name = 'sensor01'
  AND time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02');
```
