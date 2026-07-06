---
type: docs
title: '인덱스 생성과 삭제'
weight: 70
---

Machbase는 테이블 타입에 따라 지원되는 인덱스 종류가 다릅니다. 인덱스는 조회 성능을 높이기 위해 사용하며, 불필요한 인덱스는 INSERT 성능에 영향을 줍니다.

## 인덱스 종류

| 인덱스 유형 | 대상 테이블 | 특징 |
|------------|------------|------|
| LSM (Log-Structured Merge) | LOG, TAG | 시계열 대량 입력에 최적화된 기본 인덱스 |
| BITMAP | LOG | 카디널리티가 낮은 컬럼에 유효. 복합 조건 쿼리 성능 향상 |
| REDBLACK | LOOKUP, VOLATILE, RDB | PRIMARY KEY 지정 시 자동 생성. 정확한 값 검색에 최적화 |
| KEYWORD | LOG | TEXT 컬럼 전문 검색용 |

## LOG 테이블 인덱스 생성

```sql
-- LSM 인덱스 (기본, 범위 검색에 유리)
CREATE INDEX idx_sensor_id ON sensor_log (sensor_id);

-- BITMAP 인덱스 (카디널리티 낮은 컬럼: 상태값, 등급 등)
CREATE BITMAP INDEX idx_status ON sensor_log (status);

-- KEYWORD 인덱스 (TEXT 컬럼 전문 검색)
CREATE KEYWORD INDEX idx_msg ON event_log (message);
```

### 복합 인덱스

```sql
-- 복합 LSM 인덱스
CREATE INDEX idx_composite ON sensor_log (sensor_id, status);
```

## TAG 테이블 인덱스

TAG 테이블의 메타데이터 컬럼에 JSON 인덱스를 생성할 수 있습니다.

```sql
-- TAG 메타데이터 JSON 컬럼 인덱스
CREATE TAG TABLE tag (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) METADATA (
    location VARCHAR(40),
    dept     VARCHAR(20)
);

-- 메타데이터 컬럼에 인덱스 생성
CREATE INDEX idx_location ON tag METADATA (location);
```

## LOOKUP/VOLATILE/RDB 테이블 인덱스

PRIMARY KEY를 지정하면 레드-블랙 트리 인덱스가 자동으로 생성됩니다. 별도의 `CREATE INDEX` 구문은 지원되지 않습니다.

```sql
-- LOOKUP: PK 지정 시 REDBLACK 인덱스 자동 생성
CREATE LOOKUP TABLE alarm_threshold (
    sensor_id VARCHAR(40) PRIMARY KEY,
    high_limit DOUBLE
);
-- → sensor_id에 REDBLACK 인덱스 자동 생성됨

-- RDB: PK 지정 시 REDBLACK 인덱스 자동 생성
CREATE RDB TABLE orders (
    order_id INTEGER PRIMARY KEY,
    product  VARCHAR(100)
);
```

## 인덱스 삭제

```sql
DROP INDEX idx_sensor_id;
DROP INDEX idx_status;
DROP KEYWORD INDEX idx_msg;
```

PRIMARY KEY에 의해 자동 생성된 인덱스는 별도로 삭제할 수 없으며, 테이블 삭제 시 함께 제거됩니다.

## 인덱스 정보 조회

```sql
-- 테이블의 인덱스 목록 조회
SELECT * FROM M$SYS_INDEXES WHERE TABLE_NAME = 'SENSOR_LOG';

-- 특정 인덱스 정보
SELECT * FROM M$SYS_INDEX_COLUMNS WHERE INDEX_NAME = 'IDX_SENSOR_ID';
```

## 인덱스 설계 원칙

- **LOG 테이블**: 쿼리 빈도가 높은 컬럼에만 선별적으로 생성. 상태값·등급 등 저카디널리티 컬럼은 BITMAP 고려
- **TAG 테이블**: 메타데이터 필터 조회가 잦은 경우 해당 컬럼에 인덱스 추가
- **LOOKUP/VOLATILE**: PK 인덱스만 지원; PK 설계가 곧 인덱스 설계
- **과도한 인덱스**: 대량 INSERT 성능 저하의 원인이 되므로 반드시 필요한 경우에만 생성
