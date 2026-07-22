---
type: docs
title: '17.1.1.13 INDEX syntax'
weight: 130
toc: true
---

Machbase에서 인덱스는 데이터 검색 성능을 높이기 위해 사용합니다. 테이블 타입에 따라 사용 가능한 인덱스 타입이 다릅니다.

## CREATE INDEX

```sql
CREATE [INDEX_TYPE type] INDEX index_name ON table_name (column_name)
    [TABLESPACE tablespace_name]
    [index_property]
```

```sql
-- 문법 구조
CREATE INDEX index_name ON table_name (column_name) [INDEX_TYPE { LSM | KEYWORD | BITMAP | REDBLACK }]
```

### 인덱스 타입별 지원 테이블

| 인덱스 타입 | LOG 테이블 | VOLATILE 테이블 | LOOKUP 테이블 |
|------------|:---------:|:--------------:|:------------:|
| LSM | O (기본값) | X | X |
| KEYWORD | O | X | X |
| BITMAP | O | X | X |
| REDBLACK | X | O (기본값) | O (기본값) |

타입을 지정하지 않으면 테이블 타입에 따라 기본 인덱스 타입이 적용됩니다.

### LSM Index

Big Data 저장 및 검색에 최적화된 인덱스 타입입니다. LOG 테이블의 기본 인덱스 타입입니다.

```sql
-- 기본 인덱스 (LOG 테이블 → LSM)
CREATE INDEX idx_ts ON log_table (ts);

-- LSM 인덱스 명시
CREATE INDEX idx_lsm ON log_table (c1) INDEX_TYPE LSM;
```

LSM 인덱스 속성:

| 속성 | 기본값 | 설명 |
|------|--------|------|
| `MAX_LEVEL` | 3 | LSM 인덱스 최대 레벨 (0~3) |
| `PAGE_SIZE` | 524288 (512KB) | 인덱스 페이지 크기 |
| `BITMAP_ENCODE` | EQUAL | EQUAL: 동등 비교 최적화, RANGE: 범위 조회 최적화 |
| `PART_VALUE_COUNT` | - | 파티션당 저장 행 수 |

### KEYWORD Index

VARCHAR 및 TEXT 컬럼의 텍스트 검색을 위한 인덱스입니다. LOG 테이블의 단일 컬럼에만 생성 가능합니다. `SEARCH`, `ESEARCH` 연산에 활용됩니다.

```sql
CREATE INDEX idx_msg ON app_log (message) INDEX_TYPE KEYWORD;

-- 페이지 크기 지정
CREATE INDEX idx_kw ON app_log (message) INDEX_TYPE KEYWORD PAGE_SIZE=100000;
```

### BITMAP Index

데이터 분석을 위한 인덱스입니다. LOG 테이블의 VARCHAR, TEXT, BINARY를 제외한 컬럼에 생성 가능합니다.

```sql
CREATE INDEX idx_code ON sensor_log (status_code) INDEX_TYPE BITMAP;

-- RANGE 인코딩 (범위 조회에 최적화)
CREATE INDEX idx_val ON sensor_log (value) INDEX_TYPE BITMAP BITMAP_ENCODE=RANGE;
```

### REDBLACK Index

실시간 데이터 검색을 위한 메모리 인덱스입니다. VOLATILE 및 LOOKUP 테이블의 기본 인덱스 타입입니다.

```sql
CREATE INDEX idx_id ON lookup_table (id) INDEX_TYPE REDBLACK;
```

### JSON 컬럼 경로 인덱스

JSON 컬럼의 특정 멤버에 인덱스를 생성할 수 있습니다.

```sql
CREATE TAG TABLE tag_json (
    name  VARCHAR(40) PRIMARY KEY,
    time  DATETIME BASETIME,
    value JSON
);

-- JSON dot 축약 문법
CREATE INDEX idx_sensor ON tag_json (value.sensor.name);

-- JSONPath arrow 문법
CREATE INDEX idx_metric ON tag_json (value->'$.metric');

-- 배열 인덱스
CREATE INDEX idx_item ON tag_json (value.items[0]."product-id");
```

## DROP INDEX

```sql
DROP INDEX index_name
```

```sql
DROP INDEX idx_ts;
```

- 해당 테이블을 검색 중인 다른 세션이 있으면 삭제가 실패합니다.

## 예시

```sql
-- LOG 테이블에 BITMAP 인덱스 생성
CREATE LOG TABLE sensor_log (ts DATETIME, device VARCHAR(32), value DOUBLE, status INTEGER);
CREATE INDEX idx_status ON sensor_log (status) INDEX_TYPE BITMAP;
CREATE INDEX idx_ts     ON sensor_log (ts);

-- KEYWORD 인덱스를 이용한 텍스트 검색
CREATE LOG TABLE app_log (ts DATETIME, level VARCHAR(10), message TEXT);
CREATE INDEX idx_msg ON app_log (message) INDEX_TYPE KEYWORD;

SELECT * FROM app_log WHERE message SEARCH 'error AND timeout';
```

## 관련 문서

- [SEARCH / ESEARCH / REGEXP syntax](../search-esearch-regexp-syntax/) — 키워드 인덱스 활용 검색
