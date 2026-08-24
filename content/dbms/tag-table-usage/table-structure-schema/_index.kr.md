---
title: '5.2 테이블 구조와 스키마'
weight: 20
toc: true
---


<a id="tag-table-design"></a>

## TAG 테이블 설계

태그(센서) 이름을 `PRIMARY KEY`로, 시간 또는 거리 기준 컬럼을 축으로 대량의 시계열 데이터를 저장합니다.

- **[시간축 TAG 테이블 설계](/dbms/tag-table-usage/time-distance-axis/#time-axis-design-tag)**
- **[거리축 TAG 테이블 설계](/dbms/tag-table-usage/time-distance-axis/#distance-axis-design-tag)**
- **[활용 사례](/dbms/tag-table-usage/patterns-scenarios/#use-cases-tag)**
- **[METADATA 설계](/dbms/tag-table-usage/tag-metadata/#metadata-design-tag)**
- **[JSON METADATA 설계](/dbms/tag-table-usage/tag-metadata/#metadata-design-json)**
- **[값 컬럼 설계](/dbms/tag-table-usage/table-structure-schema/#tag-table-design-design-column)**
- **[이진 데이터 컬럼 설계](/dbms/tag-table-usage/table-structure-schema/#tag-table-design-design-column-binary)**
- **[VARCHAR 스토리지 최적화](/dbms/tag-table-usage/table-structure-schema/#tag-table-design-storage-varchar)**
- **[스토리지 전략](/dbms/tag-table-usage/table-structure-schema/#tag-table-design-strategy)**
- **[데이터 보정 설계](/dbms/tag-table-usage/tag-data-update-correction/#design-correction-tag)**
- **[LSL·USL 설계](/dbms/tag-table-usage/table-structure-schema/#tag-table-design-lsl-usl)**
- **[제약 및 주의사항](/dbms/tag-table-usage/constraints-errors-troubleshooting/#limitations-tag)**
- **[자동 중복 제거](/dbms/tag-table-usage/table-structure-schema/#tag-table-design-duplication-removal)**

<a id="tag-table-design-design-column"></a>

### 값 컬럼 설계

TAG 테이블의 값 컬럼(BASETIME 또는 BASEDISTANCE 이외의 컬럼)은 계측값을 저장합니다.

#### 지원 타입

| 타입 | 설명 | 저장 크기 |
|------|------|---------|
| `DOUBLE` | 64비트 부동소수점 | 8바이트 |
| `FLOAT` | 32비트 부동소수점 | 4바이트 |
| `LONG` | 64비트 정수 | 8바이트 |
| `INTEGER` (`INT`) | 32비트 정수 | 4바이트 |
| `SHORT` | 16비트 정수 | 2바이트 |
| `VARCHAR(n)` | 가변 문자열 | 최대 n바이트 |

#### 권장 타입 선택

| 데이터 | 권장 타입 |
|--------|---------|
| 온도, 습도, 압력 등 아날로그 값 | `DOUBLE` |
| 카운터, 상태 코드 | `INTEGER` |
| 플래그, 이진 상태 | `SHORT` |
| 에너지, 유량 누적값 | `DOUBLE` 또는 `LONG` |
| 태그 문자열 값 | `VARCHAR(n)` |

#### 다중 값 컬럼 설계

한 테이블에 여러 계측항목을 함께 저장할 때는 NULL 값이 발생할 수 있습니다. 계측항목이 서로 동시에 수집되는 경우에 적합합니다.

```sql
CREATE TAG TABLE weather_station (
    name        VARCHAR(64) PRIMARY KEY,
    time        DATETIME    BASETIME,
    temperature DOUBLE,     -- 항상 수집
    humidity    DOUBLE,     -- 항상 수집
    wind_speed  DOUBLE,     -- 옵션
    rainfall    DOUBLE      -- 옵션
);
```

#### NULL 허용 설계

TAG 테이블 값 컬럼은 기본적으로 NULL을 허용합니다. 특정 태그가 일부 항목만 수집하는 경우 나머지 컬럼에 NULL을 삽입합니다.

```sql
-- wind_speed와 rainfall이 없는 경우
INSERT INTO weather_station VALUES ('WS-01', NOW, 22.5, 65.0, NULL, NULL);
```

<a id="tag-table-design-design-column-binary"></a>

### 이진 데이터 컬럼 설계

TAG 테이블에 이미지, 파형, 스펙트럼 등 이진(Binary) 데이터를 함께 저장해야 하는 경우 `BINARY` 타입을 사용합니다.

#### BINARY 타입

```sql
CREATE TAG TABLE waveform_data (
    name     VARCHAR(64) PRIMARY KEY,
    time     DATETIME    BASETIME,
    rms      DOUBLE,
    waveform BINARY(1024) -- 파형 데이터 (이진)
);
```

#### 삽입

```sql
-- machsql에서는 0x로 시작하는 hex 문자열 사용
INSERT INTO waveform_data VALUES (
    'sensor-01', NOW,
    0.354,
    '0x0102030405060708'
);
```

#### 주의사항

- TAG 테이블의 `BINARY(n)` 컬럼은 1~32767바이트 범위에서 크기를 지정합니다.
- `BINARY` 데이터에는 집계 함수(`AVG`, `SUM` 등)를 적용할 수 없습니다.
- 대용량 이진 데이터를 자주 조회하면 성능에 영향이 있을 수 있습니다. 이진 데이터는 별도 파일 스토리지에 저장하고, TAG 테이블에는 파일 경로 또는 참조 키만 저장하는 패턴도 고려합니다.

#### 이진 데이터를 외부 참조로 대체하는 패턴

```sql
CREATE TAG TABLE waveform_ref (
    name      VARCHAR(64) PRIMARY KEY,
    time      DATETIME    BASETIME,
    rms       DOUBLE,
    file_path VARCHAR(512)  -- 외부 파일 참조
);
```

<a id="tag-table-design-storage-varchar"></a>

### VARCHAR 스토리지 최적화

`VARCHAR` 컬럼은 크기와 성능의 균형을 고려해 설정합니다.

#### VARCHAR 크기 설정

```sql
-- 태그 이름: 충분히 여유 있게
CREATE TAG TABLE sensor_data (
    name   VARCHAR(128) PRIMARY KEY,  -- 128자 여유
    time   DATETIME     BASETIME,
    status VARCHAR(32),               -- 상태 문자열
    label  VARCHAR(256)               -- 레이블
);
```

#### 권장 크기

| 용도 | 권장 크기 |
|------|---------|
| 태그 이름 (`PRIMARY KEY`) | 64~256 |
| 상태 코드 | 16~32 |
| 단위 | 8~16 |
| 설명 | 128~512 |
| 경로/URL | 512~1024 |

#### 주의사항

- `PRIMARY KEY`(`VARCHAR`) 컬럼은 태그 이름으로 사용됩니다. 너무 짧게 설정하면 실제 센서 이름이 잘릴 수 있습니다.
- `VARCHAR`는 짧은 값을 내부 영역에, 일정 길이를 넘는 값을 외부 영역에 저장합니다.
- 넉넉한 크기 지정은 스키마 유연성을 높이지만, 집계 쿼리나 정렬 시 내부 처리 버퍼 크기에 영향을 주므로 과도하게 큰 값은 피합니다.

#### 태그 이름 설계 패턴

태그 이름을 구조화하면 범위 조회가 쉬워집니다.

```sql
-- 구조화된 태그 이름: {site}/{building}/{floor}/{sensor_id}
INSERT INTO sensor_data VALUES ('HQ/A-BLDG/3F/TEMP-01', NOW, 'NORMAL', '3F temperature sensor 01');
INSERT INTO sensor_data VALUES ('HQ/A-BLDG/3F/TEMP-02', NOW, 'NORMAL', '3F temperature sensor 02');

-- 같은 건물의 센서 조회
SELECT name, time, status
FROM sensor_data
WHERE name LIKE 'HQ/A-BLDG/%'
  AND time >= NOW - 3600000000000;
```

<a id="tag-table-design-strategy"></a>

### 스토리지 전략

데이터는 태그별로 분리된 컬럼 스토리지에 저장됩니다. 데이터 양과 조회 패턴에 따라 적절한 전략을 선택합니다.

#### 단일 테이블 vs 다중 테이블

##### 단일 TAG 테이블 (권장)

같은 종류의 센서는 하나의 TAG 테이블에 모아서 관리합니다.

```sql
-- 권장: 모든 온도 센서를 하나의 테이블로
CREATE TAG TABLE temperature_sensor (
    name  VARCHAR(64) PRIMARY KEY,
    time  DATETIME    BASETIME,
    value DOUBLE
);
```

**장점**
- 관리 포인트 최소화
- 크로스-태그 집계 용이
- 운영 간소화

##### 다중 TAG 테이블

측정 항목이 완전히 다른 경우(컬럼 구성이 다른 경우)만 테이블을 분리합니다.

```sql
-- 온도·습도 센서 (DOUBLE 값)
CREATE TAG TABLE thermo_sensor (
    name  VARCHAR(64) PRIMARY KEY,
    time  DATETIME    BASETIME,
    temp  DOUBLE,
    humid DOUBLE
);

-- 진동 센서 (DOUBLE + BINARY 파형)
CREATE TAG TABLE vibration_sensor (
    name     VARCHAR(64) PRIMARY KEY,
    time     DATETIME    BASETIME,
    rms      DOUBLE,
    waveform BINARY
);
```

#### 태그 수 관리

- 태그 수 증가에 따른 태그 인덱스와 메타데이터 메모리 사용량을 운영 규모의 데이터로
  측정합니다.
- 센서 계층 구조를 태그 이름에 인코딩하여 관리합니다.
- 태그 이름이 매 레코드마다 고유한 값이 되는 설계는 피합니다 (안티패턴).

#### 파티션 전략

Machbase는 `_arrival_time` 또는 `BASETIME` 기준으로 데이터를 내부적으로 파티션화합니다. 별도 파티션 설정 없이도 시간 범위 쿼리가 효율적으로 실행됩니다. 보존 기간 설정은 [운영 및 구성](/dbms/operations-configuration-recovery/)을 참고하십시오.

<a id="tag-table-design-duplication-removal"></a>

### 자동 중복 제거

동일한 태그·시간 조합의 데이터가 반복 입력되면, 설정된 시간 창 내에서 중복이 자동 제거됩니다.

#### 설정: TAG_DUPLICATE_CHECK_DURATION

테이블 생성 시 `TAG_DUPLICATE_CHECK_DURATION` 속성으로 중복 제거 기간(분 단위)을 지정합니다.

```sql
-- 1440분(24시간) 이내 중복 자동 제거
CREATE TAG TABLE tag (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) TAG_DUPLICATE_CHECK_DURATION = 1440;
```

새로 삽입된 데이터의 시간이 현재 서버 시각으로부터 설정된 기간 내에 이미 존재하는 데이터와 동일하면, 해당 행은 삽입되지 않습니다.

#### 동작 예시

```sql
-- 동일 시각 데이터를 두 번 삽입
INSERT INTO tag VALUES ('tag1', DATE_TRUNC('day', NOW), 0);
INSERT INTO tag VALUES ('tag1', DATE_TRUNC('day', NOW), 0);  -- 중복 → 무시됨

EXEC TABLE_FLUSH(tag);

-- 결과: 1건만 저장됨
SELECT * FROM tag WHERE name = 'tag1';
```

`INSERT` 직후 같은 세션에서 태그 이름 조건으로 결과를 확인할 때는 `EXEC TABLE_FLUSH`를 먼저 실행합니다. Flush 전에는 전체 조회에서는 보이더라도 태그 이름 조건 조회가 아직 인덱스에 반영되지 않을 수 있습니다.

#### 설정 변경

Standard Edition에서는 생성 후 변경할 수 있습니다. Cluster Edition에서는 0이 아닌 값으로 생성하거나 `ALTER TABLE`로 변경하는 것이 제한될 수 있습니다.

```sql
ALTER TABLE tag SET TAG_DUPLICATE_CHECK_DURATION = 2880;  -- 48시간으로 변경
```

현재 설정값 확인:

```sql
SELECT * FROM m$sys_table_property
WHERE name = 'TAG_DUPLICATE_CHECK_DURATION';
```

#### 제약 사항

| 항목 | 내용 |
|------|------|
| 최대 기간 | 43,200분 (30일) |
| 단위 | 분(minute) |
| 기본값 | 0 (중복 제거 비활성) |

- 기간이 0이면 중복 제거가 동작하지 않습니다.
- 중복 제거로 무시된 데이터가 이후 삭제되어 빈 자리가 생겨도, 그 자리에 동일 데이터를 재입력할 때는 중복으로 간주하지 않습니다.

#### TRACE 로그로 중복 제거 확인

`TRACE_LOG_LEVEL`에 32(SM_2)를 추가하면 중복 제거 시 로그가 출력됩니다.

```sql
-- 현재 레벨 확인
SELECT name, value FROM v$property WHERE name = 'TRACE_LOG_LEVEL';

-- 32 추가 (예: 기존 277이면 277 + 32 = 309)
ALTER SYSTEM SET TRACE_LOG_LEVEL = 309;
```

로그 위치: `$MACHBASE_HOME/trc/machbase.trc`

```bash
tail -f $MACHBASE_HOME/trc/machbase.trc | grep DUP_DROP
```

로그 포맷: `DUP_DROP Table=<테이블명> TAG=<tag id> TIME=<시간> COL<n>=<값>`

```
[SM-INFO] DUP_DROP Table=TAG TAG=1 TIME=1998-12-24 09:00:00 000:000:012 COL3=12.000000
```

<a id="tag-table-design-lsl-usl"></a>

### LSL·USL 설계

품질 관리나 설비 모니터링에서는 하한 규격값(LSL, Lower Specification Limit)과 상한 규격값(USL, Upper Specification Limit)을 함께 저장하여 이상 감지에 활용합니다.

#### METADATA에 LSL·USL 저장

태그별로 고정된 규격값은 `LOWER LIMIT`과 `UPPER LIMIT` METADATA 컬럼에 저장합니다. 이
제약은 `SUMMARIZED` 값 컬럼에 적용됩니다.

```sql
CREATE TAG TABLE quality_sensor (
    name    VARCHAR(64) PRIMARY KEY,
    time    DATETIME    BASETIME,
    value   DOUBLE SUMMARIZED
) METADATA (
    lsl     DOUBLE LOWER LIMIT,   -- 하한 규격값
    usl     DOUBLE UPPER LIMIT,   -- 상한 규격값
    target  DOUBLE    -- 목표값
);

-- 센서 초기화 시 규격값 설정
INSERT INTO quality_sensor METADATA (name, lsl, usl, target)
VALUES ('QS-MOTOR-01', 70.0, 90.0, 80.0);
```

#### 이상 감지 쿼리

```sql
-- 규격 이탈 데이터 조회
SELECT q.name, q.time, q.value, m.lsl, m.usl
FROM quality_sensor q
JOIN quality_sensor METADATA m ON q.name = m.name
WHERE q.time >= NOW - 3600000000000
  AND (q.value < m.lsl OR q.value > m.usl);
```

#### 동적 LSL·USL 패턴

규격값이 시간에 따라 변하는 경우, 별도 LOOKUP 테이블에 저장합니다.

```sql
CREATE LOOKUP TABLE spec_limits (
    sensor_name VARCHAR(64) PRIMARY KEY,
    lsl         DOUBLE,
    usl         DOUBLE,
    updated_at  DATETIME
);

-- 규격값 변경
UPDATE spec_limits SET lsl = 68.0, usl = 92.0, updated_at = NOW
WHERE sensor_name = 'QS-MOTOR-01';
```

#### 알람 임계값과의 차이

| 값 | 설명 |
|-----|------|
| LSL (Lower Spec Limit) | 품질 규격 하한 — 이 미만은 불량 |
| USL (Upper Spec Limit) | 품질 규격 상한 — 이 초과는 불량 |
| LCL (Lower Control Limit) | 통계적 관리 하한 (±3σ) |
| UCL (Upper Control Limit) | 통계적 관리 상한 (±3σ) |

<a id="original-85-lsl-usl-limits"></a>

## LSL/USL을 통한 데이터 품질 관리


### LSL/USL 소개

LSL(Lower Specification Limit)은 하한 규격값, USL(Upper Specification Limit)은 상한 규격값입니다. Tag 테이블에 종속된 메타데이터 테이블에서 이 기능을 지원하며, 특정 TAG ID에 규격 범위를 설정하여 범위 밖 데이터의 입력을 차단합니다.

### 제약 조건

다음 제약 조건이 적용됩니다.

* `CLUSTER EDITION`은 LSL/USL 기능을 지원하지 않습니다.
* LSL/USL을 설정하려면 Tag 테이블의 세 번째 컬럼인 __Value__가 __SUMMARIZED__로 설정되어야 합니다.
* LSL은 USL보다 작거나 같아야 하며, __Value__ 컬럼의 입력 값은 LSL과 USL 사이에 있어야 합니다 (포함). __(LSL <= Value <= USL)__
* LSL/USL 설정을 부여하기 전에 입력된 데이터는 검증되지 않습니다.
* LSL/USL 컬럼을 NULL로 설정하면 입력 데이터를 검증하지 않습니다.
* LSL/USL 기능은 개별적으로 사용할 수 있습니다. 상한 사양만 일치시키려면 USL만 설정할 수 있습니다.
* USL 기능만 사용하는 경우 USL보다 낮은 데이터는 검증되지 않습니다.

#### 지원되는 데이터 타입

__Value__ 컬럼 타입과 일치해야 하며, __SUMMARIZED__ 속성과 마찬가지로 숫자 타입만 허용됩니다.

|타입|설명|범위|유효 자릿수|
|----|------|-----|----|
|short|16비트 부호 있는 정수 데이터 타입|-32767 ~ 32767|-|
|ushort|16비트 부호 없는 정수 데이터 타입|0 ~ 65534|-|
|integer|32비트 부호 있는 정수 데이터 타입|-2147483647 ~ 2147483647|-|
|uinteger|32비트 부호 없는 정수 데이터 타입|0 ~ 4294967294|-|
|long|64비트 부호 있는 정수 데이터 타입|-9223372036854775807 ~ 9223372036854775807|-|
|ulong|64비트 부호 없는 정수 데이터 타입|0~18446744073709551614|-|
|float|32비트 부동 소수점 데이터|-|6[^1]|
|double|64비트 부동 소수점 데이터|-|15[^1]|

### LSL/USL 설정 및 사용

태그 메타데이터 테이블의 컬럼에 `LOWER LIMIT`(LSL) 또는 `UPPER LIMIT`(USL) 키워드를 지정합니다. Tag 테이블 생성 시 또는 메타데이터 컬럼 추가 시 설정할 수 있습니다.

#### CRAETE

```sql
CREATE TAG TABLE example (
    tag_id  VARCHAR(50) PRIMARY KEY,
    time    DATETIME    BASETIME,
    value   INTEGER     SUMMARIZED)
METADATA (
    lsl     INTEGER LOWER LIMIT,
    usl     INTEGER UPPER LIMIT
);
```

두 컬럼을 함께 사용하거나 하나만 사용할 수 있습니다.
LSL만 설정하면 LSL보다 높은 데이터는 검증하지 않습니다. `USL == NULL`과 동일한 효과입니다.

```sql
CREATE TAG TABLE example (
    tag_id  VARCHAR(50) PRIMARY KEY,
    time    DATETIME    BASETIME,
    value   INTEGER     SUMMARIZED)
METADATA (
    lsl    INTEGER LOWER LIMIT
);
```

#### ADD COLUMN

데이터가 이미 입력된 후 `ADD COLUMN`을 사용하여 추가하는 경우 기본값은 __NULL__입니다.

```sql
CREATE TAG TABLE example (
    tag_id  VARCHAR(50) PRIMARY KEY,
    time    DATETIME    BASETIME,
    value   INTEGER     SUMMARIZED
);

ALTER TABLE _example_meta ADD COLUMN (lsl INTEGER LOWER LIMIT);
ALTER TABLE _example_meta ADD COLUMN (usl INTEGER UPPER LIMIT);
```

[CREATE](#craete)와 마찬가지로 하나의 속성만 추가할 수도 있습니다.

```sql
CREATE TAG TABLE example (
    tag_id  VARCHAR(50) PRIMARY KEY,
    time    DATETIME    BASETIME,
    value   INTEGER     SUMMARIZED
);

ALTER TABLE _example_meta ADD COLUMN (usl INTEGER UPPER LIMIT);
```

#### INSERT

특정 TAG ID에 대한 LSL/USL 값을 설정합니다.

```sql
INSERT INTO example metadata VALUES ('TAG_01', 100, 200);
```

설정 후 태그 데이터를 입력하면 다음과 같이 동작합니다.

```sql
Mach> INSERT INTO example VALUES ('TAG_01', NOW, 95);  -- Failure
[ERR-02342: SUMMARIZED value is less than LOWER LIMIT.]

Mach> INSERT INTO example VALUES ('TAG_01', NOW, 100); -- Success (Inclusive)
1 row(s) inserted.
Elapsed time: 0.000

Mach> INSERT INTO example VALUES ('TAG_01', NOW, 150); -- Success
1 row(s) inserted.
Elapsed time: 0.000

Mach> INSERT INTO example VALUES ('TAG_01', NOW, 200); -- Success (Inclusive)
1 row(s) inserted.
Elapsed time: 0.000

Mach> INSERT INTO example VALUES ('TAG_01', NOW, 205); -- Failure
[ERR-02341: SUMMARIZED value is greater than UPPER LIMIT.]
```

Tag 테이블을 조회하면 규격 범위 내 데이터만 입력된 것을 확인할 수 있습니다.

```sql
Mach> SELECT * FROM example;
TAG_ID                                              TIME                            VALUE       LSL         USL
------------------------------------------------------------------------------------------------------------------------------
TAG_01                                              2023-09-12 09:31:27 923:289:631 100         100         200
TAG_01                                              2023-09-12 09:31:27 929:013:232 150         100         200
TAG_01                                              2023-09-12 09:31:27 939:209:248 200         100         200
[3] row(s) selected.
Elapsed time: 0.001
```

#### UPDATE

LSL/USL 컬럼의 값을 수정합니다. 이미 입력된 데이터에는 소급 적용되지 않으므로 주의가 필요합니다.

```sql
Mach> UPDATE example metadata SET lsl = 10, usl = 100 WHERE tag_id = 'TAG_01';
1 row(s) updated.
Elapsed time: 0.001

Mach> SELECT * FROM _example_meta;
_ID                  TAG_ID                                              LSL         USL
------------------------------------------------------------------------------------------------------
1                    TAG_01                                              10          100
[1] row(s) selected.
Elapsed time: 0.001
```

#### DELETE

태그 메타 테이블은 `DROP COLUMN`을 지원하지 않으므로 LSL/USL 컬럼 자체를 삭제할 수는 없습니다. 대신 값을 NULL로 설정하면 제약 없이 데이터를 입력할 수 있습니다.

```sql
Mach> UPDATE EXAMPLE METADATA SET lsl = NULL, usl = NULL WHERE tag_id = 'TAG_01';
1 row(s) updated.
Elapsed time: 0.001

Mach> SELECT * FROM _example_meta;
_ID                  TAG_ID                                              LSL         USL
------------------------------------------------------------------------------------------------------
1                    TAG_01                                              NULL        NULL
[1] row(s) selected.
Elapsed time: 0.001
```

### TRACE 로그로 LSL/USL 위반 확인
- 위치: `$MACHBASE_HOME/trc/machbase.trc`
- 빠른 필터:
  ```bash
  grep LIMIT_DROP $MACHBASE_HOME/trc/machbase.trc | tail -n 20
  ```
- 로그 포맷: `LIMIT_DROP (TYPE=<UPPER|LOWER>) TABLE=<테이블명> TAG=<tag name> <컬럼명=값 ...>`
  - TYPE=LOWER/UPPER로 어떤 한계가 위반됐는지 구분.
  - DATETIME은 `YYYY-MM-DD HH24:MI:SS mmm:uuu:nnn` 형태.
- 실제 예시:
  ```
  [2025-11-29 13:50:34 P-151395 T-126343511537344][QP-INFO] LIMIT_DROP (TYPE=LOWER) TABLE=TAG3 TAG=tag-1  TIME=2020-01-01 00:00:00 000:000:000 VALUE=5.55
  [2025-11-29 13:50:34 P-151395 T-126343511537344][QP-INFO] LIMIT_DROP (TYPE=UPPER) TABLE=TAG3 TAG=tag-1  TIME=2020-01-01 00:00:04 000:000:000 VALUE=30.55
  [2025-11-29 13:50:35 P-151395 T-126344475694784][QP-INFO] LIMIT_DROP (TYPE=LOWER) TABLE=TAG3 TAG=tag-2  TIME=1998-12-24 09:00:00 000:000:000 VALUE=0
  [2025-11-29 13:50:35 P-151395 T-126344475694784][QP-INFO] LIMIT_DROP (TYPE=UPPER) TABLE=TAG3 TAG=tag-2  TIME=1998-12-24 09:00:00 000:000:008 VALUE=45
  ```
- 활용 포인트
  - TAG별로 LOWER/UPPER 위반 시각과 값을 한눈에 파악.
  - grep으로 TAG/테이블명을 추가 필터하면 특정 대상만 추적 가능.
- 주의: 한 줄 최대 약 4KB라 컬럼이 많을 때 뒤가 잘릴 수 있으며, 기동 직후 메타 캐시 준비 전에는 테이블명이 ID로 보일 수 있습니다.

[^1]: [IEEE 754](https://en.wikipedia.org/wiki/IEEE_754)

<a id="original-85-binary-columns"></a>

## Binary 컬럼


`BINARY(n)`은 Tag 테이블에서 센서 프레임용 고정 길이 바이너리 값을 저장합니다.
다른 테이블 타입이나 프로토콜에서는 허용되지 않습니다. 길이는 1~32K-1
(1~32767)바이트만 유효하며, 인덱스를 생성할 수 없습니다.

명시적 binary literal로 `BINARY` 값을 입력합니다.

### DDL 규칙

```sql
CREATE TAG TABLE t1(
  name VARCHAR(32) PRIMARY KEY,
  time DATETIME BASETIME,
  frame BINARY(4)
);
```

- 유효 길이: `1 <= n <= 32767` (32K-1).
- 범위를 벗어나면 생성 시 오류가 발생합니다(`BINARY(0)` 등).
- `DESC`와 테이블 메타데이터는 선언된 바이트 길이(헥스 폭 아님)를 표시합니다.
  SQL `LENGTH(binary_col)`는 짧은 입력값에 붙은 뒤쪽 0 패딩을 제외한 표시
  값 길이를 반환합니다.

### 지원 입력 형식

```sql
X'hex_digits'
x'hex_digits'
B'bit_digits'
b'bit_digits'
O'octal_digits'
o'octal_digits'
```

| 형식 | 의미 | 단위 |
| --- | --- | --- |
| `X'...'`, `x'...'` | 16진수 literal | 16진수 2자리 = 1바이트 |
| `B'...'`, `b'...'` | 2진수 literal | bit 8자리 = 1바이트 |
| `O'...'`, `o'...'` | 8진수 literal | 8진수 3자리 = 1바이트 |

prefix는 대소문자 모두 허용됩니다.

```sql
CREATE TAG TABLE t_bin (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value BINARY(4)
);

INSERT INTO t_bin VALUES('hex1', '2024-01-01 00:00:00', X'0A');
INSERT INTO t_bin VALUES('hex2', '2024-01-01 00:00:01', x'00010203');
INSERT INTO t_bin VALUES('bit1', '2024-01-01 00:00:02', B'00001010');
INSERT INTO t_bin VALUES('oct1', '2024-01-01 00:00:03', O'012');
```

`X'0A'`, `B'00001010'`, `O'012'`는 모두 1바이트 값 `0x0A`를 의미합니다.

### Binary literal 규칙

#### 16진수 literal

`X'...'`와 `x'...'`에는 `0-9`, `A-F`, `a-f`를 사용할 수 있습니다.

```sql
X'00'
X'0AFF'
x'abcdef'
```

16진수 문자는 반드시 짝수 개여야 합니다. 두 자리가 1바이트에 해당합니다.

#### 2진수 literal

`B'...'`와 `b'...'`에는 `0`과 `1`만 사용할 수 있습니다.

```sql
B'00000000'  -- 0x00
B'00001010'  -- 0x0A
b'11111111'  -- 0xFF
```

bit 수는 반드시 8의 배수여야 합니다. 8자리가 1바이트에 해당합니다.

#### 8진수 literal

`O'...'`와 `o'...'`에는 `0-7`만 사용할 수 있습니다.

```sql
O'000'  -- 0x00
O'012'  -- 0x0A
o'377'  -- 0xFF
```

8진수 문자는 반드시 3자리 단위여야 합니다. 각 3자리 값은 `000`부터
`377`까지의 1바이트 범위여야 합니다.

#### 빈 값

작은따옴표 안을 비워 길이 0인 binary 값을 표현합니다.

```sql
X''
B''
O''
```

### 길이 제한

`BINARY(n)` 컬럼에는 최대 `n`바이트까지만 입력 가능합니다.

```sql
CREATE TAG TABLE t_limit (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value BINARY(2)
);

INSERT INTO t_limit VALUES('ok_hex', '2024-01-01 00:00:00', X'0AFF');
INSERT INTO t_limit VALUES('ok_bit', '2024-01-01 00:00:01', B'0000101011111111');
INSERT INTO t_limit VALUES('ok_oct', '2024-01-01 00:00:02', O'012377');

INSERT INTO t_limit VALUES('bad_hex', '2024-01-01 00:00:03', X'000102'); -- 실패: 3바이트
```

source 종류와 무관하게 최종 binary 값이 대상 `BINARY(n)` 길이를 초과하면
입력은 실패합니다. 이 규칙은 binary literal뿐 아니라 일반 문자열, 기존
`'0x...'` 문자열 입력, 다른 `BINARY` 컬럼 값을 `INSERT ... SELECT`로
복사하는 경우에도 동일하게 적용됩니다.

```sql
CREATE TAG TABLE t_src (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value BINARY(8)
);

CREATE TAG TABLE t_dst (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value BINARY(4)
);

INSERT INTO t_src VALUES('k1', '2024-01-01 00:00:00', X'0102030405060708');
INSERT INTO t_dst SELECT name, time, value FROM t_src; -- 실패: 8바이트 값을 BINARY(4)에 입력
```

`CASE`, `INSERT ... SELECT`, view 등 SQL expression 안에서 사용하더라도
최종 binary 값이 대상 `BINARY(n)` 길이를 초과하면 입력은 실패합니다.

### 올바르지 않은 입력

다음 입력은 유효하지 않습니다.

```sql
X'0'        -- 16진수 문자가 홀수 개
X'0G'       -- G는 16진수 문자가 아님
B'0101'     -- bit 수가 8의 배수가 아님
B'00000002' -- 2는 2진수 문자가 아님
O'12'       -- 8진수 문자가 3자리 단위가 아님
O'400'      -- 1바이트 범위 초과
X'0102      -- 닫는 작은따옴표가 없음
```

잘못된 값이나 길이 초과 입력은 다음 오류로 실패합니다.

```text
[ERR-02233: Error occurred at column (n): (Invalid insert value.)]
```

### 기존 문자열 입력과의 차이

기존 호환성을 위해 문자열 형태의 `'0x...'` 입력도 사용할 수 있습니다.
`'0x...'`는 문자열에서 `BINARY` 컬럼으로 변환되는 방식이고,
`X'...'`, `B'...'`, `O'...'`는 SQL에서 binary 값임을 명확히 표시하는
binary literal입니다.

일반 문자열을 `BINARY(n)` 컬럼에 입력하는 것도 가능하지만, 문자열 byte 길이가 `n`을
초과하면 실패합니다. 새 SQL 작성 시에는 의미가 명확한 binary literal 형식을
권장합니다.

`'0b...'`, `'0o...'`, 따옴표 없는 `0x...`, `0b...`, `0o...` 형식은
binary literal로 지원하지 않습니다.

### 출력 및 도구 메모

- machsql은 `0x` 없는 대문자 헥스로 출력합니다. 짧은 입력값에 붙은 뒤쪽
  0 패딩은 텍스트 출력에 표시되지 않습니다.
- machloader: 스키마에 `BINARY(n)`을 선언하고, 잘못된 값이나 길이 초과는
  실패합니다.
- Machbase SQLCLI, ODBC, Java, C#, Node.js 드라이버는 고정 길이 버퍼로 송수신하며 메타데이터
  `LENGTH`는 바이트 길이입니다.

<a id="original-85-varchar-storage"></a>

## VARCHAR 저장소 최적화


### VARCHAR 저장소 옵션
varchar 데이터를 고정 영역에 저장하는 최대 크기입니다.
이 값보다 긴 varchar 값은 가변 영역에 저장됩니다. 15에서 127까지 지정 가능하며, 기본값은 15입니다.

```sql
-- 입력 VARCHAR 데이터의 크기가 15 이하이면 확장 파일 대신 고정 데이터 파일에 저장됩니다.

CREATE TAG TABLE tag (name VARCHAR(20) PRIMARY KEY, time DATETIME BASETIME, value DOUBLE SUMMARIZED, strval VARCHAR(100)) VARCHAR_FIXED_LENGTH_MAX = 15;
```

VARCHAR 저장소 옵션 값의 속성은 테이블 m$sys_table_property에 표시됩니다.
```sql
SELECT * FROM m$sys_table_property WHERE id={table_id} AND name = 'VARCHAR_FIXED_LENGTH_MAX';
```
