---
type: docs
title: 'LOG 인덱스 튜닝'
weight: 20
---

LOG 테이블은 기본적으로 `_arrival_time` 기준의 시간 순차 저장 구조를 사용하며, 추가 인덱스는 선택적으로 생성합니다. 이 페이지에서는 어떤 컬럼에 어떤 인덱스를 생성해야 Append 성능 손실을 최소화하면서 조회 성능을 극대화할 수 있는지 설명합니다.

## `_arrival_time` 기반 파티션 Pruning (인덱스 불필요)

LOG 테이블은 `_arrival_time`(데이터 도착 시각)을 기준으로 자동 파티셔닝됩니다. `_arrival_time` 또는 `DURATION` 절로 시간 범위를 지정하면 해당 파티션만 스캔합니다. 별도 인덱스 없이 자동으로 동작합니다.

```sql
-- DURATION 키워드: 최근 N 시간/일/분 데이터만 스캔
SELECT * FROM device_log DURATION 1 HOUR;

-- 명시적 시간 범위: 지정한 파티션만 스캔
SELECT * FROM device_log
WHERE _arrival_time BETWEEN TO_DATE('2026-07-01 08:00:00', 'YYYY-MM-DD HH24:MI:SS')
                        AND TO_DATE('2026-07-01 09:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

> 시간 필터 없이 조회하면 모든 파티션을 전체 스캔합니다. LOG 테이블 쿼리에는 항상 시간 조건을 포함하세요.

## LSM 인덱스: 등가·범위 조건 컬럼

`device_id`, `event_type`처럼 WHERE 조건에 자주 등장하는 컬럼에는 LSM(Log-Structured Merge-tree) 인덱스를 생성합니다.

```sql
-- 기본 LSM 인덱스 생성
CREATE INDEX idx_device ON device_log (device_id);

-- MAX_LEVEL 속성으로 LSM 레벨 수 지정 (기본값 사용 권장)
CREATE INDEX idx_event ON device_log (event_type) INDEX_TYPE LSM MAX_LEVEL=3;
```

```sql
-- 인덱스 사용 예시
SELECT * FROM device_log
WHERE device_id = 'DEV-1234'
DURATION 1 DAY;
```

**LSM 인덱스 특성**:

- 삽입 시 메모리 버퍼에 먼저 기록하고, 배경 스레드가 주기적으로 디스크의 정렬된 파일로 병합합니다.
- 순차 삽입이 많은 환경에서 B-Tree보다 삽입 성능이 우수합니다.
- 병합(compaction) 중에 I/O 부하가 일시적으로 증가할 수 있습니다.

## BITMAP 인덱스: 카디널리티 낮은 컬럼

`status`, `level`, `type`처럼 가능한 값의 수가 적은(카디널리티 낮은) 컬럼에는 BITMAP 인덱스를 사용합니다. BITMAP 인덱스는 동등 조건과 OR 조합 조건에서 특히 효율적입니다.

```sql
-- level 컬럼: ERROR, WARN, INFO, DEBUG 등 소수의 고정값
CREATE INDEX idx_level ON device_log (level) INDEX_TYPE BITMAP;

-- status 컬럼: ACTIVE, INACTIVE, FAULT 등
CREATE INDEX idx_status ON device_log (status) INDEX_TYPE BITMAP;

-- KEY_COMPRESS 속성으로 압축 활성화
CREATE INDEX idx_type ON device_log (event_type) INDEX_TYPE BITMAP KEY_COMPRESS=1;
```

```sql
-- BITMAP 인덱스 활용 쿼리
SELECT COUNT(*) FROM device_log
WHERE level = 'ERROR'
DURATION 1 DAY;

-- OR 조합 (BITMAP 인덱스에서 효율적)
SELECT * FROM device_log
WHERE level IN ('ERROR', 'WARN')
DURATION 6 HOUR;
```

> `SHOW INDEX FROM device_log`에서 BITMAP 인덱스는 `LSM`으로 표시됩니다. 이는 내부 구현 방식에 따른 표시로, 정상적인 동작입니다.

## KEYWORD 인덱스: 긴 텍스트 컬럼

`message`, `description`처럼 긴 텍스트에서 특정 단어를 포함하는 행을 검색할 때 KEYWORD 인덱스를 사용합니다. VARCHAR 및 TEXT 컬럼에만 생성할 수 있습니다.

```sql
-- message 컬럼에 KEYWORD 인덱스 생성
CREATE INDEX idx_msg ON device_log (message) INDEX_TYPE KEYWORD;
```

```sql
-- SEARCH 연산자로 단어 검색
SELECT * FROM device_log
WHERE message SEARCH 'timeout'
DURATION 1 HOUR;

-- 여러 단어 조합 검색
SELECT * FROM device_log
WHERE message SEARCH 'connection AND refused'
DURATION 6 HOUR;
```

## 인덱스별 적합한 컬럼 선택 기준

| 인덱스 유형 | 적합한 컬럼 | 부적합한 컬럼 |
|------------|-----------|------------|
| LSM | 카디널리티 높은 컬럼 (device_id, user_id) | 시간 컬럼 (_arrival_time), 고유값 수 매우 많은 컬럼 |
| BITMAP | 카디널리티 낮은 컬럼 (level, status, type) | 카디널리티 높은 컬럼 (UUID, 세션 ID) |
| KEYWORD | 긴 텍스트 (message, description) | 숫자형, 짧은 코드값 |

## 인덱스 남발 금지: Append 성능 영향

각 인덱스는 데이터 삽입 시마다 갱신 비용이 발생합니다. LOG 테이블에서 인덱스 1개 추가 시 **Append 처리량이 약 5~10% 감소**합니다.

```
인덱스 없음        : Append 기준 성능 100%
LSM 인덱스 1개     : Append 약 90~95%
LSM 인덱스 2개     : Append 약 82~88%
LSM + BITMAP 각 1개 : Append 약 80~88%
```

**권장 원칙**:

- 실제 WHERE 조건에 사용되는 컬럼만 인덱스를 생성합니다.
- 새 인덱스 생성 전에 해당 컬럼이 쿼리에 실제로 자주 등장하는지 확인합니다.
- `_arrival_time` 기반 DURATION 필터로 해결되는 경우 추가 인덱스는 불필요합니다.

## 인덱스 관리 명령어

```sql
-- 현재 인덱스 목록 확인
SHOW INDEX FROM device_log;

-- 전체 인덱스 현황
SHOW INDEXES;

-- 인덱스 구축 진행 상황 (대량 데이터 후 인덱스 생성 시)
SHOW INDEXGAP;

-- 인덱스 삭제 (조회 중인 세션이 없을 때)
DROP INDEX idx_device;
```

## 실전 예시: device_log 테이블 인덱스 설계

```sql
-- 테이블 생성
CREATE TABLE device_log (
    device_id   VARCHAR(64),
    event_type  VARCHAR(32),
    level       VARCHAR(16),
    status      VARCHAR(16),
    message     VARCHAR(2000),
    value       DOUBLE
);

-- 자주 사용하는 WHERE 조건 컬럼에만 선별 생성
CREATE INDEX idx_device   ON device_log (device_id);              -- LSM: 장치 ID 조회
CREATE INDEX idx_level    ON device_log (level) INDEX_TYPE BITMAP; -- BITMAP: 로그 레벨 필터
CREATE INDEX idx_msg      ON device_log (message) INDEX_TYPE KEYWORD; -- KEYWORD: 메시지 텍스트 검색

-- event_type, status는 DURATION 필터와 조합하므로 인덱스 미생성
```

## 핵심 정리

| 항목 | 권장 사항 |
|------|---------|
| `_arrival_time` 조건 | 인덱스 불필요, DURATION 또는 시간 범위 사용 |
| device_id, user_id 등 | LSM 인덱스 생성 |
| level, status, type 등 | BITMAP 인덱스 생성 |
| message, description 등 | KEYWORD 인덱스 생성 |
| 인덱스 수 | 최소화 (각 인덱스는 Append 5~10% 감소) |
