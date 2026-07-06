---
type: docs
title: 'LOOKUP 일반 조건식 DELETE (planned: dbms-nfx#3696)'
weight: 10
---

> **계획된 기능**: LOOKUP 테이블의 일반 조건식(non-PK 컬럼 기준) DELETE는 dbms-nfx#3696에서 개발 중입니다. 현재 버전(8.6)에서는 PRIMARY KEY 기준 DELETE를 사용하세요.

## 현재 지원 범위

현재 LOOKUP 테이블의 DELETE는 PK 기준 조건을 사용하는 것이 안전합니다.

```sql
-- 현재 권장: PK 기준 삭제
DELETE FROM alarm_threshold WHERE sensor_id = 'TEMP-01';
```

## 향후 지원 예정 (dbms-nfx#3696)

```sql
-- 향후 지원 예정: 비활성 장치 설정 일괄 삭제
DELETE FROM device_config WHERE active = 0;

-- 기간 조건 삭제
DELETE FROM alarm_history WHERE occurred_at < DATEADD('d', -90, NOW);
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

> LOOKUP JSON 컬럼 및 일반 조건 UPDATE/DELETE는 모두 dbms-nfx#3696에서 함께 구현 예정입니다.
