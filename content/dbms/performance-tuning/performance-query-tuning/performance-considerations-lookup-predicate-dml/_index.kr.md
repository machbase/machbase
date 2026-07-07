---
type: docs
title: 'LOOKUP 일반 predicate DML 성능 고려사항 (planned: dbms-nfx#3696)'
weight: 50
---

LOOKUP 테이블은 태그 메타데이터나 설비 정보 등 소규모 참조 데이터를 저장하는 메모리 기반 테이블입니다. 현재 버전에서 DELETE와 UPDATE의 WHERE 조건에는 제약이 있으며, 이로 인해 대량 DML 시 성능에 영향이 있을 수 있습니다.

## 현재 제약사항

### PK 기준 DELETE만 지원

현재 LOOKUP 테이블의 DELETE는 기본키(PK) 컬럼을 조건으로 사용할 때 가장 효율적으로 동작합니다.

```sql
-- 효율적: PK 기준 DELETE
DELETE FROM device_meta WHERE device_id = 'DEV-001';

-- 비효율적: non-PK 컬럼 조건 DELETE (전체 스캔 후 삭제)
DELETE FROM device_meta WHERE location = 'Building-A';
```

non-PK 컬럼을 조건으로 DELETE하면 내부적으로 전체 테이블을 스캔해 조건에 맞는 레코드를 찾은 후 삭제합니다. LOOKUP 테이블이 소용량이라면 큰 문제가 없지만, 수만 건 이상이 되면 응답 시간이 증가합니다.

> **계획된 기능 (dbms-nfx#3696)**: non-PK 컬럼 조건을 사용한 DELETE·UPDATE를 효율적으로 처리하는 기능이 개발 예정입니다.

### UPDATE 조건 제약

LOOKUP 테이블의 UPDATE는 PK 기준으로 단건 또는 소수 건 처리 시 효율적입니다. non-PK 조건으로 다수 레코드를 한 번에 UPDATE하면 전체 스캔이 발생할 수 있습니다.

```sql
-- 효율적: PK 기준 UPDATE
UPDATE device_meta SET status = 'INACTIVE' WHERE device_id = 'DEV-001';

-- 전체 스캔 가능: non-PK 조건 UPDATE
UPDATE device_meta SET status = 'INACTIVE' WHERE location = 'Building-A';
```

## 임시 대안: PK 목록 SELECT 후 PK 기준 DELETE 반복

non-PK 조건으로 대량 삭제가 필요한 경우, PK 목록을 먼저 조회한 뒤 PK 기준으로 반복 삭제하는 패턴을 사용합니다.

### 패턴 1: 애플리케이션에서 PK 목록 기반 삭제

```sql
-- 1단계: 삭제할 레코드의 PK 목록 조회
SELECT device_id
FROM   device_meta
WHERE  location = 'Building-A'
  AND  status = 'INACTIVE';

-- 2단계: 조회된 PK로 개별 삭제 (애플리케이션에서 반복)
DELETE FROM device_meta WHERE device_id = 'DEV-001';
DELETE FROM device_meta WHERE device_id = 'DEV-005';
DELETE FROM device_meta WHERE device_id = 'DEV-012';
-- ...
```

애플리케이션 코드에서 SELECT 결과를 받아 PK 목록을 순회하며 DELETE를 실행합니다.

### 패턴 2: 임시 테이블을 활용한 일괄 삭제

삭제 대상이 많은 경우 임시 LOG 테이블에 PK를 적재한 뒤 처리합니다.

```sql
-- 임시 테이블 생성 (일회성)
CREATE TABLE tmp_delete_keys (device_id VARCHAR(64));

-- 삭제 대상 PK 적재
INSERT INTO tmp_delete_keys
SELECT device_id FROM device_meta
WHERE  location = 'Building-A' AND status = 'INACTIVE';

-- 임시 테이블의 PK로 LOOKUP 테이블 삭제
-- (애플리케이션에서 tmp_delete_keys를 순회하며 DELETE 실행)

-- 작업 완료 후 임시 테이블 삭제
DROP TABLE tmp_delete_keys;
```

## LOOKUP 테이블 DML 성능 최적화 가이드

### 1. PK 인덱스 활용 최대화

LOOKUP 테이블의 PK는 해시 인덱스로 관리됩니다. WHERE 절에 PK를 포함하면 O(1) 수준의 접근이 가능합니다.

```sql
-- 효율적 패턴: PK를 항상 조건에 포함
SELECT * FROM device_meta WHERE device_id = 'DEV-001' AND status = 'ACTIVE';
-- device_id(PK)로 레코드를 찾은 후 status 조건을 추가로 검사
```

### 2. 소규모 배치 단위로 DML 분할

대량 UPDATE 또는 DELETE가 필요한 경우, 한 번에 모든 레코드를 처리하지 않고 소규모 배치로 분할합니다. 이렇게 하면 잠금 경합을 줄이고 다른 쿼리의 응답성을 유지할 수 있습니다.

```sql
-- 권장: 배치 단위 삭제 (애플리케이션에서 반복)
-- 1회에 100건씩 삭제
DELETE FROM device_meta WHERE device_id IN ('DEV-001', 'DEV-002', ..., 'DEV-100');
-- 다음 배치
DELETE FROM device_meta WHERE device_id IN ('DEV-101', 'DEV-102', ..., 'DEV-200');
```

### 3. LOOKUP 테이블 크기 관리

LOOKUP 테이블은 메모리에 상주합니다. 불필요한 레코드가 누적되면 메모리 사용량이 증가하고 전체 스캔 시 성능이 저하됩니다.

```sql
-- 현재 LOOKUP 테이블 레코드 수 확인
SELECT COUNT(*) FROM device_meta;

-- 불필요한 레코드 주기적 정리
DELETE FROM device_meta WHERE status = 'RETIRED' AND device_id = 'DEV-XXX';
```

## 현재 제약 요약

| DML 유형 | PK 조건 | non-PK 조건 |
|----------|---------|-------------|
| DELETE | 효율적 (해시 인덱스 직접 접근) | 전체 스캔 후 삭제 |
| UPDATE | 효율적 (PK로 레코드 특정) | 전체 스캔 후 업데이트 |
| INSERT | PK 중복 시 오류 또는 UPDATE (설정에 따라) | — |

non-PK 조건의 대량 DML은 현재 전체 스캔이 발생하므로, 위의 임시 대안 패턴을 사용하거나 dbms-nfx#3696 기능 릴리스를 기다려 주세요.
