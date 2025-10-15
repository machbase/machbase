---
title: 자동 이상값 제거
type: docs
weight: 41
---

## 소개

산업·환경 센서에서 수집되는 시계열 데이터는 노이즈, 순간 스파이크, 진동 간섭 등으로 인해 예상 범위를 벗어나는 이상값이 자주 발생합니다. 이러한 값은 분석 정확도를 떨어뜨리고 저장 공간과 처리 시간을 불필요하게 증가시킵니다. 애플리케이션에서 직접 필터링 로직을 구현하면 복잡도가 높고 비용도 큽니다.

Machbase는 TAG 테이블의 메타데이터에 정의한 사양 한계(Specification Limit)를 이용해 데이터 적재 단계에서 자동으로 이상값을 제거할 수 있는 기능을 제공합니다. 각 센서별 허용 범위를 선언적으로 정의해 두면 해당 범위를 벗어나는 데이터는 저장되지 않습니다.

## 핵심 개념: 사양 한계(LSL/USL)

자동 이상값 제거 기능은 태그 식별자(Tag ID)별로 허용 가능한 값의 범위를 정의해 동작합니다. 이는 TAG 테이블과 연결된 메타데이터 테이블에 다음 두 속성을 추가하여 설정합니다.

- **LSL (Lower Specification Limit)**: 측정값의 최소 허용 범위.
- **USL (Upper Specification Limit)**: 측정값의 최대 허용 범위.

데이터가 TAG 테이블에 삽입될 때 Machbase는 다음 절차로 유효성을 검사합니다.

1. **메타데이터 조회**: 입력되는 행의 `name`(Tag ID)에 해당하는 메타데이터 행에서 LSL, USL 값을 읽습니다.
2. **값 비교**: `SUMMARIZED` 속성이 선언된 `value` 컬럼의 입력값을 LSL/USL과 비교합니다.
3. **검증 규칙**: `LSL <= 값 <= USL` 조건을 충족할 때만 삽입이 허용됩니다.
   - LSL이 `NULL`이면 하한 검사를 생략합니다.
   - USL이 `NULL`이면 상한 검사를 생략합니다.
   - 둘 다 `NULL`이면 검사 없이 통과합니다.
4. **처리 결과**: 조건을 만족하면 행이 삽입되고, 벗어나면 삽입이 거부되며 오류(`ERR-02342`, `ERR-02341` 등)가 반환됩니다.

## 설정 방법

사양 한계는 `CREATE TAG TABLE` 문의 `METADATA` 절에서 `LOWER LIMIT`, `UPPER LIMIT` 키워드를 사용해 컬럼을 정의하거나, 이후 `ALTER TABLE`로 추가할 수 있습니다.

### 테이블 생성 시 한계 정의

```sql
CREATE TAG TABLE sensor_readings (
    tag_id VARCHAR(50) PRIMARY KEY,
    ts DATETIME BASETIME,
    reading DOUBLE SUMMARIZED
)
METADATA (
    min_acceptable DOUBLE LOWER LIMIT,
    max_acceptable DOUBLE UPPER LIMIT,
    location VARCHAR(100)
);
```

- `SUMMARIZED` 속성이 지정된 `reading` 컬럼에 대해 이상값 검사가 수행됩니다.
- `min_acceptable`, `max_acceptable`는 LSL, USL을 저장할 컬럼입니다.

### 기존 테이블에 한계 추가

메타데이터 테이블(`_TableName_meta`)에 컬럼을 추가하는 방식입니다.

```sql
ALTER TABLE _sensor_readings_meta
    ADD COLUMN (min_acceptable DOUBLE LOWER LIMIT);

ALTER TABLE _sensor_readings_meta
    ADD COLUMN (max_acceptable DOUBLE UPPER LIMIT);
```

### 한계 값 설정

LSL/USL 컬럼을 추가한 뒤에는 메타데이터 테이블에 값을 insert/update 합니다.

```sql
INSERT INTO sensor_readings metadata (tag_id, min_acceptable, max_acceptable, location)
VALUES ('TEMP_SENSOR_01', 10.0, 90.0, 'Boiler Room');

UPDATE sensor_readings metadata
SET min_acceptable = 15.0, max_acceptable = 85.0
WHERE tag_id = 'TEMP_SENSOR_01';
```

## 동작 및 제약 사항

- **SUMMARIZED 필수**: 적재 시 검증을 받으려면 대상 `value` 컬럼에 `SUMMARIZED`가 선언되어야 합니다.
- **데이터 타입 호환성**: LSL/USL 컬럼의 데이터 타입은 검사 대상 컬럼과 호환되어야 합니다.
- **LSL <= USL**: 두 값이 모두 존재하면 반드시 `LSL <= USL`을 만족해야 합니다.
- **검사 시점**: 새 데이터 `INSERT` 시에만 검사합니다. 기존 데이터에는 적용되지 않습니다.
- **메타데이터 변경**: 한계를 변경해도 이미 저장된 데이터는 수정되지 않습니다.
- **NULL 처리**: LSL 또는 USL이 `NULL`이면 해당 방향의 검사를 생략합니다.
- **편도 한계**: LSL만 정의하면 최소값 검사, USL만 정의하면 최대값 검사만 수행합니다.
- **메타데이터 의존성**: `_TableName_meta` 테이블 구조와 값에 전적으로 의존합니다.

## 예시

### 1. 스키마 정의 및 메타데이터 컬럼 추가

```sql
DROP TABLE IF EXISTS out_tag CASCADE;

CREATE TAG TABLE out_tag (
    tag_id VARCHAR(50) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
)
METADATA (
    lsl DOUBLE LOWER LIMIT,
    usl DOUBLE UPPER LIMIT
) TAG_PARTITION_COUNT=1;
```

### 2. 메타데이터에 한계 값 넣기

```sql
INSERT INTO out_tag metadata (tag_id, lsl, usl)
VALUES ('TAG_01', 100.0, 200.0);

SELECT * FROM _out_tag_meta WHERE tag_id = 'TAG_01';
```

### 3. 데이터 삽입 테스트

```sql
-- 하한 미만 → 거부
INSERT INTO out_tag VALUES ('TAG_01', NOW, 95.2);

-- 하한과 동일 → 허용
INSERT INTO out_tag VALUES ('TAG_01', NOW, 100.0);

-- 범위 내 → 허용
INSERT INTO out_tag VALUES ('TAG_01', NOW, 150.5);

-- 상한과 동일 → 허용
INSERT INTO out_tag VALUES ('TAG_01', NOW, 200.0);

-- 상한 초과 → 거부
INSERT INTO out_tag VALUES ('TAG_01', NOW, 205.5);
```

에러 메시지를 통해 어떤 한계를 위반했는지 확인할 수 있습니다.
