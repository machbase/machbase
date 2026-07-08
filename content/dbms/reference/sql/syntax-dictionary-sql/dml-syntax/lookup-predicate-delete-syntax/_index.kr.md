---
type: docs
title: 'LOOKUP predicate DELETE syntax (planned: dbms-nfx#3696)'
weight: 40
---

> **계획 중 (planned: dbms-nfx#3696)**: 일반 predicate 기반 LOOKUP DELETE는 현재 구현 중입니다. 이 문서는 현재 지원 범위와 향후 계획을 함께 기술합니다.

## 현재 지원 상태

LOOKUP 및 VOLATILE 테이블의 DELETE는 현재 **PRIMARY KEY 등치 조건**만 WHERE 절에 사용할 수 있습니다.

```sql
DELETE FROM table_name WHERE pk_column = pk_value
```

```sql
-- 지원: PK 조건 기반 DELETE
CREATE LOOKUP TABLE device_config (
    device_id VARCHAR(40) PRIMARY KEY,
    threshold DOUBLE,
    enabled   INTEGER
);

DELETE FROM device_config WHERE device_id = 'TEMP-01';
```

## 향후 계획 (planned: dbms-nfx#3696)

향후 릴리스에서는 PK가 아닌 일반 컬럼 조건(predicate)으로도 DELETE가 가능하도록 지원할 예정입니다.

```sql
-- 계획 중인 문법 (현재 미지원)
DELETE FROM table_name WHERE non_pk_column = some_value;

-- 예시: enabled = 0 인 모든 row 삭제
DELETE FROM device_config WHERE enabled = 0;
```

현재 이 문법은 지원되지 않으며, 실행하면 오류가 반환됩니다.

```
ERR-02XXX: Only primary key condition is allowed in WHERE clause for DELETE.
```

## 현재 제약사항

| WHERE 조건 | 현재 상태 |
|-----------|-----------|
| `pk_col = value` | O (지원) |
| `pk_col IN (...)` | 확인 중 |
| `non_pk_col = value` | X (계획 중: dbms-nfx#3696) |
| 복합 조건 (AND/OR) | X (계획 중: dbms-nfx#3696) |
| WHERE 절 없이 전체 삭제 | O (전체 삭제: `DELETE FROM table_name`) |

## 임시 방법

일반 조건 기반 DELETE가 필요한 경우 다음 절차를 사용합니다.

```sql
-- 1. 삭제 대상 PK 값 조회
SELECT device_id FROM device_config WHERE enabled = 0;

-- 2. PK 조건으로 개별 DELETE
DELETE FROM device_config WHERE device_id = 'TEMP-01';
DELETE FROM device_config WHERE device_id = 'TEMP-02';
-- ...
```

애플리케이션에서 조회 결과를 반복 처리해 PK 조건으로 DELETE하거나, 전체 삭제 후 필요한 행만 재입력하는 방법을 고려합니다.

```sql
-- 전체 삭제 후 필요한 행만 재입력
DELETE FROM device_config;
INSERT INTO device_config (device_id, threshold, enabled) VALUES ('TEMP-01', 50.0, 1);
INSERT INTO device_config (device_id, threshold, enabled) VALUES ('TEMP-03', 60.0, 1);
```

## 관련 문서

- [LOOKUP predicate UPDATE syntax](../lookup-predicate-update-syntax/) — LOOKUP predicate UPDATE 계획
