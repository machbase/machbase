---
type: docs
title: '테이블 타입별 기능 지원표'
weight: 20
---

Machbase는 용도에 따라 다섯 가지 테이블 유형을 제공합니다. 각 테이블 유형은 설계 목적에 따라 지원하는 기능 범위가 다릅니다.

## 테이블 유형 개요

| 테이블 유형 | 주요 용도 |
|------------|----------|
| **TAG** | 시계열 센서 데이터 고속 수집 및 집계 (ROLLUP) |
| **LOG** | 비정형 로그/이벤트 데이터 순차 저장, 텍스트 검색 |
| **LOOKUP** | 메타데이터, 코드 테이블, 참조 데이터 (UPDATE/DELETE 지원) |
| **VOLATILE** | 메모리 기반 임시 데이터, 세션 내 캐시 |
| **RDB** | 트랜잭션이 필요한 일반 관계형 데이터 |

## 테이블 유형별 기능 지원 종합 표

| 기능 | TAG | LOG | LOOKUP | VOLATILE | RDB |
|------|:---:|:---:|:------:|:--------:|:---:|
| **쓰기** | | | | | |
| INSERT (SQL) | O | O | O | O | O |
| Append API | O | O | O | X | X |
| **수정/삭제** | | | | | |
| UPDATE | △ | X | O | O | O |
| DELETE | O | O | O | O | O |
| **트랜잭션** | | | | | |
| Transaction (COMMIT/ROLLBACK) | X | X | △ | O | O |
| **집계 및 검색** | | | | | |
| ROLLUP | O | X | X | X | X |
| 텍스트 검색 (KEYWORD INDEX) | X | O | X | X | X |
| **JSON** | | | | | |
| JSON 컬럼 | X | O | △ | O | O |
| JSON path query | X | O | X | X | O |
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

## 주요 제약 상세

### TAG 테이블 UPDATE 제약 (△)

TAG 테이블의 UPDATE는 다음 조건을 모두 만족해야 합니다.

- `WHERE` 절에 반드시 `name` (TAGNAME, PK 컬럼) 조건 포함
- SET 대상은 SUMMARIZED 속성 컬럼만 가능
- `time` (BASETIME) 컬럼과 `name` 컬럼은 UPDATE 불가

```sql
-- 가능: SUMMARIZED 컬럼을 name 조건으로 업데이트
UPDATE sensor_data SET min_value = 0.0 WHERE name = 'sensor01';

-- 불가: BASETIME 컬럼 업데이트
UPDATE sensor_data SET time = NOW() WHERE name = 'sensor01';
```

상세 내용은 [TAG data UPDATE 지원표](../tag-data-update/)를 참고하세요.

### LOOKUP 테이블 Transaction 제약 (△)

LOOKUP 테이블은 개별 DML(INSERT/UPDATE/DELETE)에 대해 트랜잭션이 지원되지만, 복합 트랜잭션(여러 DML을 하나의 트랜잭션으로 묶기)은 제한적입니다. PK 기반 조작을 권장합니다.

### LOOKUP 테이블 JSON 컬럼 (△)

JSON 컬럼 저장은 지원되지만, JSON path query(`$.key` 형식의 조건 검색)는 현재 계획 중입니다. 상세 내용은 [LOOKUP SQL/JSON 지원표](../lookup-sql-json/)를 참고하세요.

### Append API 대상 테이블

Append API는 TAG 테이블과 LOG 테이블에만 사용할 수 있습니다. LOOKUP, VOLATILE, RDB 테이블에는 일반 `INSERT` SQL을 사용하세요.

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
