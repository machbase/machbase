---
type: docs
title: '인덱스 생성과 삭제'
weight: 70
---

Machbase는 테이블 타입에 따라 지원되는 인덱스 종류가 다릅니다. 인덱스는 조회 성능을 높이기 위해 사용하며, 불필요한 인덱스는 INSERT 성능에 영향을 줍니다.

## 인덱스 종류

| 인덱스 유형 | 대상 테이블 | 특징 |
|------------|------------|------|
| LSM (Log-Structured Merge) | LOG | 시계열 대량 입력에 최적화된 LOG 컬럼 인덱스 |
| BITMAP | LOG | 카디널리티가 낮은 컬럼에 유효. 복합 조건 쿼리 성능 향상 |
| REDBLACK | LOOKUP, VOLATILE, TAG 메타데이터 | 정확한 값 검색에 최적화 |
| BTREE | RDB | PRIMARY KEY 및 보조 인덱스에 사용 |
| KEYWORD | LOG | TEXT 컬럼 전문 검색용 |
| TAG/KV | TAG | TAG 값 컬럼 조건 조회를 보조하는 secondary index |

## LOG 테이블 인덱스 생성

```sql
-- LSM 인덱스 (기본, 범위 검색에 유리)
CREATE INDEX idx_sensor_id ON sensor_log (sensor_id);

-- BITMAP 인덱스 (카디널리티 낮은 컬럼: 상태값, 등급 등)
CREATE BITMAP INDEX idx_status ON sensor_log (status);

-- KEYWORD 인덱스 (TEXT 컬럼 전문 검색)
CREATE KEYWORD INDEX idx_msg ON event_log (message);
```

> LOG/TAG/LOOKUP/VOLATILE 인덱스는 단일 컬럼 중심으로 설계합니다. RDB 테이블은 일반 복합
> 인덱스를 지원하지만, 복합 JSON path 인덱스와 복합 PRIMARY KEY 인덱스는 지원하지 않습니다.

## TAG 테이블 인덱스

TAG 테이블은 태그명과 시간 축에 대한 내부 인덱스를 자동으로 관리합니다. 추가로
METADATA 컬럼 인덱스와 값 컬럼 TAG/KV secondary index를 사용할 수 있습니다.

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

-- 값 컬럼 TAG/KV 인덱스 생성
CREATE INDEX idx_value ON tag (value) INDEX_TYPE TAG;
```

## LOOKUP/VOLATILE/RDB 테이블 인덱스

LOOKUP과 VOLATILE은 Red-Black Tree 인덱스를 사용합니다. RDB는 BTREE로 표시되는 PRIMARY
KEY 인덱스와 보조 인덱스를 사용합니다.

```sql
-- LOOKUP: PK 지정 시 REDBLACK 인덱스 자동 생성
CREATE LOOKUP TABLE alarm_threshold (
    sensor_id VARCHAR(40) PRIMARY KEY,
    high_limit DOUBLE
);
-- → sensor_id에 REDBLACK 인덱스 자동 생성됨

-- RDB: PK 지정 시 BTREE 인덱스로 표시
CREATE RDB TABLE orders (
    order_id INTEGER PRIMARY KEY,
    product  VARCHAR(100),
    status   VARCHAR(16)
);

-- RDB 보조 인덱스
CREATE INDEX idx_orders_product ON orders(product);

-- RDB 복합 보조 인덱스
CREATE INDEX idx_orders_product_status ON orders(product, status);
```

```sql
-- RDB PRIMARY KEY 인덱스 사후 생성
CREATE RDB TABLE order_work (
    order_id INTEGER,
    product  VARCHAR(100)
);

CREATE PRIMARY KEY INDEX pk_order_work ON order_work(order_id);
```

## 인덱스 삭제

```sql
DROP INDEX idx_sensor_id;
DROP INDEX idx_status;
DROP INDEX idx_msg;
```

PRIMARY KEY에 의해 자동 생성된 인덱스는 별도로 삭제할 수 없으며, 테이블 삭제 시 함께 제거됩니다.

## 인덱스 정보 조회

```sql
-- 인덱스 목록 조회
SHOW INDEXES;

-- 테이블/컬럼과 조합해 상세 조회
SELECT t.name AS table_name,
       c.name AS column_name,
       i.name AS index_name,
       i.type AS index_type
  FROM m$sys_indexes i,
       m$sys_index_columns ic,
       m$sys_tables t,
       m$sys_columns c
 WHERE i.id = ic.index_id
   AND i.table_id = t.id
   AND ic.table_id = c.table_id
   AND ic.col_id = c.id
   AND t.name = 'SENSOR_LOG';
```

## 인덱스 설계 원칙

- **LOG 테이블**: 쿼리 빈도가 높은 컬럼에만 선별적으로 생성. 상태값·등급 등 저카디널리티 컬럼은 BITMAP 고려
- **TAG 테이블**: 태그명·시간 조건을 기본으로 사용하고, 메타데이터 필터나 값 조건이 잦은 경우 해당 인덱스 추가
- **LOOKUP/RDB**: PK 인덱스와 필요한 보조 인덱스 사용. RDB는 복합 보조 인덱스도 가능
- **VOLATILE**: PK 인덱스 중심으로 설계
- **과도한 인덱스**: 대량 INSERT 성능 저하의 원인이 되므로 반드시 필요한 경우에만 생성
