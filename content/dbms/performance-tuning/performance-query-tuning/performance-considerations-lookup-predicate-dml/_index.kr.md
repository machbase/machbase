---
type: docs
title: 'LOOKUP 일반 predicate DML 성능 고려사항'
weight: 50
---

LOOKUP 테이블은 태그 메타데이터나 설비 정보 등 소규모 참조 데이터를 저장하는 메모리 기반 테이블입니다. 현재 버전에서 DELETE와 UPDATE의 WHERE 조건은 PRIMARY KEY 동등 조건으로 제한됩니다.

## 현재 제약사항

### PK 기준 DELETE만 지원

현재 LOOKUP 테이블의 DELETE는 기본키(PK) 컬럼의 동등 조건을 사용해야 합니다.

```sql
-- 효율적: PK 기준 DELETE
DELETE FROM device_meta WHERE device_id = 'DEV-001';

-- 오류: non-PK 컬럼 조건 DELETE
DELETE FROM device_meta WHERE location = 'Building-A';
-- [ERR-02190: Invalid UPDATE/DELETE condition. Specify it as (primary key column) = (value)]
```

non-PK 컬럼만 조건으로 사용한 DELETE는 실행되지 않습니다. 먼저 SELECT로 대상 PK를 조회한 뒤 PK 기준 DELETE를 반복합니다.

### UPDATE 조건 제약

LOOKUP 테이블의 UPDATE도 PK 컬럼의 동등 조건을 사용해야 합니다.

```sql
-- 효율적: PK 기준 UPDATE
UPDATE device_meta SET status = 'INACTIVE' WHERE device_id = 'DEV-001';

-- 오류: non-PK 조건 UPDATE
UPDATE device_meta SET status = 'INACTIVE' WHERE location = 'Building-A';
-- [ERR-02190: Invalid UPDATE/DELETE condition. Specify it as (primary key column) = (value)]
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
DELETE FROM device_meta WHERE device_id = 'DEV-001';
DELETE FROM device_meta WHERE device_id = 'DEV-002';
-- ...
-- 다음 배치
DELETE FROM device_meta WHERE device_id = 'DEV-101';
DELETE FROM device_meta WHERE device_id = 'DEV-102';
-- ...
```

### 3. LOOKUP 테이블 크기 관리

LOOKUP 테이블은 메모리에 상주합니다. 불필요한 레코드가 누적되면 메모리 사용량이 증가하고 전체 스캔 시 성능이 저하됩니다.

```sql
-- 현재 LOOKUP 테이블 레코드 수 확인
SELECT COUNT(*) FROM device_meta;

-- 불필요한 레코드 주기적 정리도 PK 기준으로 수행
SELECT device_id FROM device_meta WHERE status = 'RETIRED';
DELETE FROM device_meta WHERE device_id = 'DEV-XXX';
```

## 현재 제약 요약

| DML 유형 | PK 조건 | non-PK 조건 |
|----------|---------|-------------|
| DELETE | 효율적 (해시 인덱스 직접 접근) | 오류 반환 (`ERR-02190`) |
| UPDATE | 효율적 (PK로 레코드 특정) | 오류 반환 (`ERR-02190`) |
| INSERT | PK 중복 시 오류 또는 UPDATE (설정에 따라) | — |

non-PK 조건의 대량 DML은 실행되지 않으므로, 위의 PK 목록 조회 후 반복 처리 패턴을 사용합니다.
