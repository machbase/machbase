---
type: docs
title: 'LOOKUP non-PK DELETE 미지원'
weight: 10
---

LOOKUP 테이블의 일반 조건식(non-PK 컬럼 기준) DELETE는 현재 빌드에서 지원되지 않습니다.
PRIMARY KEY equality 조건만 사용할 수 있습니다.

## 현재 지원 범위

현재 LOOKUP 테이블의 DELETE는 PK 기준 조건만 허용합니다.

```sql
-- 현재 권장: PK 기준 삭제
DELETE FROM alarm_threshold WHERE sensor_id = 'TEMP-01';
```

## 지원하지 않는 조건식

```sql
DELETE FROM device_config WHERE active = 0;
-- [ERR-02190: Invalid UPDATE/DELETE condition. Specify it as (primary key column) = (value)]

DELETE FROM alarm_history WHERE occurred_at < NOW - 7776000000000000;
-- [ERR-02190: Invalid UPDATE/DELETE condition. Specify it as (primary key column) = (value)]
```

## 현재 대안

PK가 아닌 조건으로 여러 행을 삭제해야 할 경우:

1. **PK 목록 조회 후 개별 DELETE**:
```sql
-- 1단계: 삭제 대상 PK 조회
SELECT sensor_id FROM alarm_threshold WHERE device_type = 'DECOMMISSIONED';

-- 2단계: 각 PK에 대해 DELETE 실행 (애플리케이션 루프)
DELETE FROM alarm_threshold WHERE sensor_id = 'TEMP-99';
DELETE FROM alarm_threshold WHERE sensor_id = 'FLOW-88';
```

2. **전체 재구성**: 필요한 행만 SELECT하여 새 테이블에 저장하고 기존 테이블 재생성

> LOOKUP 테이블의 JSON 타입 컬럼도 현재 빌드에서 지원되지 않습니다.
