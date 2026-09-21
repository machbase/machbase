---
title: 태그 테이블
type: docs
weight: 01
---

## 태그 테이블 데이터 모델 개요

이 문서는 Machbase 시계열 데이터베이스에서 센서 시계열 데이터를 저장·조회·관리하도록 최적화된 전용 테이블 구조인 Machbase 태그 테이블을 자세히 설명합니다.

### 개념 데이터 모델

센서 데이터를 다루는 전통적인 데이터 모델은 흔히 CSV와 비슷한 가로형(wide) 형식입니다. 각 행은 하나의 타임스탬프를 나타내고, 각 컬럼은 서로 다른 센서 측정값(태그)에 대응합니다.

**전통적인 데이터 모델(가로형):**

| timestamp           | temperature | humidity | pressure | vibration |
| :------------------ | :---------- | :------- | :------- | :-------- |
| 2023-04-15 09:34:12 | 23.5        | 78.9     | 11       | 55        |
| 2023-04-15 09:34:13 | 23.7        | 75.6     | 12       | 51        |
| ...                 | ...         | ...      | ...      | ...       |

*   **특징:**
    *   같은 시각에 측정한 값을 하나의 레코드로 관리합니다.
    *   원래의 가로형 형식 그대로 데이터를 볼 수 있습니다.
    *   센서나 태그를 추가·삭제할 때 스키마를 유연하게 바꾸기 어렵고, 테이블을 변경해야 하는 경우가 많습니다.

Machbase 태그 테이블은 이와 다른 방식을 사용합니다. 데이터를 세로형(tall/narrow) 형식으로 구성해, 각 행이 특정 시각에 특정 센서(태그)에서 측정한 값 하나를 나타냅니다.

**Machbase 태그 테이블 데이터 모델(세로형):**

| TAGID         | timestamp           | value |
| :------------ | :------------------ | :---- |
| temperature   | 2023-04-15 09:34:12 | 23.5  |
| humidity      | 2023-04-15 09:34:12 | 78.9  |
| pressure      | 2023-04-15 09:34:12 | 11    |
| vibration     | 2023-04-15 09:34:12 | 55    |
| temperature   | 2023-04-15 09:34:13 | 23.7  |
| humidity      | 2023-04-15 09:34:13 | 75.6  |
| ...           | ...                 | ...   |

*   **특징:**
    *   각 측정값을 개별 레코드로 변환해 저장합니다.
    *   태그(센서)를 추가·삭제해도 테이블 구조를 바꿀 필요가 없어 스키마 확장이 가장 유연합니다.
    *   태그별 집계와 통계 분석을 효율적으로 수행할 수 있습니다.
    *   가로형 모델보다 행 수는 늘어나지만, 전용 아키텍처 덕분에 일반적으로 조회와 적재 성능이 향상됩니다.

### 스키마로 보는 데이터 모델 비교

데이터 모델의 차이는 테이블 생성 구문에도 드러납니다.

**전통적인 스키마(예시):**

```sql
CREATE TABLE Vibration (
    time      DATETIME,
    temp      DOUBLE,
    humidity  DOUBLE,
    pressure  INTEGER,
    rms       LONG,
    tick      DOUBLE
    -- Additional columns for each new sensor type
);
```

*흔히 쓰는 설계 방식이지만, 변화가 잦은 IoT 환경에서는 스키마가 경직된다는 문제가 있습니다.*

**Machbase 태그 테이블 스키마:**

```sql
CREATE TAG TABLE Vibration (
    name  VARCHAR(80) PRIMARY KEY, -- Identifier for the specific tag/sensor
    time  DATETIME    BASETIME,    -- Timestamp of the measurement
    value DOUBLE                   -- The actual measured value
);
```

*이 구조는 시계열 데이터의 기본 요소인 식별자, 시간, 값에 집중해 핵심 데이터 스키마를 단순화합니다. 그 밖의 부가 정보는 메타데이터로 관리합니다.*

## 태그 테이블 기본

### 구조

태그 테이블은 구조화된 센서 데이터를 효율적으로 적재·조회·압축하도록 최적화된 테이블입니다. 기본 레코드 구조는 다음 세 가지 요소로 구성됩니다.

1.  **식별자(기본값은 `name` 컬럼):** 특정 센서나 데이터 소스를 식별하는 고유 문자열입니다(예: `"sensor-A"`, `"factory1-machine2-temp"`). 연결된 메타데이터 구조에서 기본 키 역할을 합니다.
2.  **시간(기본값은 `time` 컬럼):** 데이터가 생성되거나 기록된 시각을 나타내는 타임스탬프입니다. 64비트 정수로 저장되며 나노초 정밀도를 지원합니다.
3.  **값(기본값은 `value` 컬럼):** 지정한 시각에 식별자와 연결된 실제 측정값 또는 이벤트 데이터입니다. 여러 데이터 타입을 지원하지만 일반적으로 `DOUBLE`(64비트 부동소수점)을 사용하며, 다양한 분석 함수를 활용할 수 있습니다.

태그 테이블은 내부적으로 태그를 설명하는 메타데이터와 실제 시계열 데이터를 분리해 관리합니다.

```
       Tag Table: Vibration
+--------------------------------------+------------------------------------------+
|        Meta (Sensor Attributes)      |            Data (Sensor Readings)        |
| +---------+-----------+------------+ | +----+---------------------------+-----+ |
| | NAME    | Attribute1| Attribute2 | | | ID | TIME (nanoseconds)        |VALUE| |
| +---------+-----------+------------+ | +----+---------------------------+-----+ |
| | Sensor-A| LocationX | TypeY      | | | 0  | 1719292147529850600       |-1.3 | |
| | Sensor-B| LocationZ | TypeW      | | | 1  | 1719292148529850600       |-2.3 | |
| | Sensor-C| LocationX | TypeY      | | | 2  | 1719292149529850600       |-3.3 | |
| | ...     | ...       | ...        | | | 0  | 1719292150000000000       |-4.3 | |
| +---------+-----------+------------+ | | 0  | 1719292167529850600       |-5.3 | |
|                                      | | 2  | 1719292177529850600       |-6.3 | |
| (Managed in _Vibration_META table)   | | 1  | 1719292187529850600       |-7.3 | |
|                                      | | .. | ...                       | ... | |
|                                      | +----+---------------------------+-----+ |
|                                      | (Managed in _Vibration_DATA_N partitions)|
+--------------------------------------+------------------------------------------+
```

기본 `CREATE` 문에도 이 구조가 반영되어 있습니다.

```sql
CREATE TAG TABLE Vibration (
    name  VARCHAR(80) PRIMARY KEY, -- Links to Meta table, unique identifier
    time  DATETIME    BASETIME,    -- Core time column for indexing
    value DOUBLE                   -- Core value column
    -- Optional additional data columns can be defined here
);
-- Metadata columns are defined separately in the METADATA clause
```

### 지원 데이터 타입

Machbase 태그 테이블의 `value` 컬럼과 추가 데이터 컬럼은 다음 데이터 타입을 지원합니다.

| 타입       | 설명                             | 범위/표현                                                       | NULL 표현                     |
| :--------- | :------------------------------- | :-------------------------------------------------------------- | :---------------------------- |
| `SHORT`    | 16비트 부호 있는 정수            | -32767 ~ 32767                                                  | -32768                        |
| `USHORT`   | 16비트 부호 없는 정수            | 0 ~ 65534                                                       | 65535                         |
| `INTEGER`  | 32비트 부호 있는 정수            | -2147483647 ~ 2147483647                                        | -2147483648                   |
| `UINTEGER` | 32비트 부호 없는 정수            | 0 ~ 4294967294                                                  | 4294967295                    |
| `LONG`     | 64비트 부호 있는 정수            | -9223372036854775807 ~ 9223372036854775807                      | -9223372036854775808          |
| `ULONG`    | 64비트 부호 없는 정수            | 0 ~ 18446744073709551614                                        | 18446744073709551615          |
| `FLOAT`    | 32비트 부동소수점                | ±1.175494e-38 ~ ±3.402823e+38                                   | 3.402823466e+38               |
| `DOUBLE`   | 64비트 부동소수점                | ±2.225074e-308 ~ ±1.797693e+308                                 | 1.7976931348623158e+308       |
| `DATETIME` | 날짜와 시간(나노초 정밀도)       | 1970-01-01 00:00:00 000:000:000 UTC 이후                        | N/A                           |
| `VARCHAR`  | 가변 길이 문자열(UTF-8)          | 1바이트 ~ 32KB(32767바이트)                                     | NULL                          |
| `IPV4`     | IPv4 주소                        | "0.0.0.0" ~ "255.255.255.255"                                   | NULL                          |
| `IPV6`     | IPv6 주소                        | "::" ~ "FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF"                | NULL                          |
| `JSON`     | JSON 데이터 타입                 | 데이터 길이: 1바이트 ~ 32KB, 경로 길이: 1 ~ 512자               | NULL                          |

**참고:** 태그 테이블에서는 `TEXT` 데이터 타입을 **지원하지 않습니다**.

## 태그 테이블 생성과 내부 구조

### 태그 테이블 생성

태그 테이블을 생성하는 기본 구문은 다음과 같습니다.

```sql
CREATE TAG TABLE table_name (
    name_column VARCHAR(size) PRIMARY KEY, -- Tag identifier column
    time_column DATETIME BASETIME,         -- Time column with BASETIME property
    value_column datatype [SUMMARIZED]     -- Value column(s)
    [, additional_data_column datatype ...] -- Optional extra data columns
)
METADATA (
    meta_column1 datatype,                 -- Metadata columns
    meta_column2 datatype
    [, ...]
)
[ table_property = value [, ...] ];        -- Optional table properties
```

**주요 구성 요소:**

| 요소                          | 설명                                                                                                                                              | 영역        |
| :---------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------ | :---------- |
| `name_column` (`PRIMARY KEY`) | 센서 이름 같은 고유한 태그 식별자를 저장하는 컬럼입니다. 최대 길이를 지정한 `VARCHAR` 타입이어야 하며 `PRIMARY KEY`로 선언합니다.               | 데이터/메타 |
| `time_column` (`BASETIME`)    | 각 데이터의 타임스탬프를 저장하는 컬럼으로, 보통 `DATETIME` 타입입니다. 기본 시간 인덱스임을 나타내는 `BASETIME` 속성이 있어야 합니다.          | 데이터      |
| `value_column` [`SUMMARIZED`] | 측정값을 저장하는 컬럼입니다. 주로 `DOUBLE`, `LONG` 타입을 사용합니다. 선택 키워드인 `SUMMARIZED`를 지정하면 이 컬럼의 내장 통계 집계가 활성화됩니다. | 데이터      |
| `additional_data_column`      | 같은 타임스탬프에 기본 값과 함께 품질 플래그, 배치 번호 같은 보조 데이터를 저장하는 선택 컬럼입니다.                                              | 데이터      |
| `METADATA` 절                 | `name_column`으로 식별하는 각 태그의 설명 속성(메타데이터)을 저장할 컬럼을 정의합니다. 이 속성은 `name_column`으로 연결됩니다.                    | 메타        |
| `table_property`              | 파티션, 통계 등 테이블 동작과 자원 할당을 설정하는 선택적인 키-값 쌍입니다.                                                                       | 테이블      |

### 태그 테이블 속성

태그 테이블을 생성할 때 다음 속성을 설정해 성능과 자원 사용량을 최적화할 수 있습니다.

| 속성                           | 설명                                                                                                                  | 기본값  | 비고                                                                                                                         |
| :----------------------------- | :-------------------------------------------------------------------------------------------------------------------- | :------ | :--------------------------------------------------------------------------------------------------------------------------- |
| `TAG_PARTITION_COUNT`          | 생성할 내부 데이터 파티션(하위 테이블) 수입니다. 적재와 조회의 병렬성(동시성)에 영향을 줍니다.                       | 4       | 값을 높이면 동시성이 향상되지만 메모리 사용량도 늘어납니다. 자원이 제한된 엣지 장비에서는 1이나 2 같은 낮은 값을 사용합니다. |
| `TAG_DATA_PART_SIZE`           | 파티션 안의 데이터 저장 단위(데이터 블록)의 목표 크기(바이트)입니다.                                                  | 16MB    | 데이터 버퍼링과 인덱싱에 관련된 메모리 할당에 영향을 줍니다.                                                                 |
| `TAG_STAT_ENABLE`              | 태그별 통계 메타데이터(최솟값, 최댓값, 건수, 합계) 수집을 켜거나 끕니다. `V$tableName_STAT` 뷰를 사용하려면 필요합니다. | 1 (ON)  | 통계가 필요 없으면 0으로 설정해 비활성화할 수 있으며, 약간의 오버헤드를 줄일 수 있습니다.                                    |
| `TAG_DUPLICATE_CHECK_DURATION` | 적재 시 중복 레코드(같은 name과 time)를 무시하는 검사 기간(분)입니다.                                                 | 0       | 데이터를 가끔 재전송하는 소스에서 생기는 중복 데이터를 관리하는 데 도움이 됩니다.                                            |
| `VARCHAR_FIXED_LENGTH_MAX`     | 기본 데이터 저장 영역에 인라인으로 저장할 `VARCHAR` 데이터의 최대 길이(바이트)입니다. 더 긴 문자열은 외부에 저장될 수 있습니다. | 15      | 가변 길이 문자열의 저장 효율과 조회 성능에 영향을 줍니다.                                                                    |

**속성 지정 예시:**

```sql
CREATE TAG TABLE basic (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
)
METADATA (
    factory VARCHAR(32),
    equipment VARCHAR(64)
)
TAG_PARTITION_COUNT=2,
TAG_STAT_ENABLE=0,
TAG_DUPLICATE_CHECK_DURATION=3;
```

### 내부 테이블 구조

태그 테이블(예: `MYTAG`)을 생성하면 내부적으로 다음과 같은 관련 객체가 생성되고 관리됩니다.

1.  **`MYTAG`(가상 테이블):** 데이터를 조회하는 기본 인터페이스입니다. 메타데이터와 시계열 데이터를 합친 통합 뷰를 제공합니다.
2.  **`_MYTAG_META`(메타데이터 테이블):** `METADATA` 절에서 정의한 메타데이터 속성을 저장합니다. 이 테이블에서는 `name` 컬럼이 기본 키 역할을 해 태그별 메타데이터 항목의 고유성을 보장합니다. 빠른 조회를 위해 보통 메모리에 상주합니다.
3.  **`_MYTAG_DATA_N`(데이터 파티션 테이블):** 실제 시계열 데이터(`time`, `value`, 추가 데이터 컬럼)를 저장하는 내부 테이블입니다(`N`은 0부터 `TAG_PARTITION_COUNT - 1`까지). 데이터는 태그 `name`을 기준으로 각 파티션에 분산됩니다.
4.  **`V$MYTAG_STAT`(통계 뷰):** `TAG_STAT_ENABLE=1`일 때 제공되는 시스템 뷰로, 데이터 파티션에서 산출한 태그별 요약 통계(최소·최대 시간, 최솟값·최댓값, 건수, 합계)를 보여 줍니다.

```
      << Internal Structure of MYTAG >>

+---------------------------------------------------+
|                  MYTAG (Virtual Table)            |
|  (Query Interface)                                |
+---------------------+-----------------------------+
                      |                             |
+---------------------v-----------------------------+ +-----------------------+
|            _MYTAG_META (Metadata Table)           | |   V$MYTAG_STAT        |
| +-------+-----------+-----------+-----+           | | (Statistics View)     |
| | _ID   | NAME      | factory   | equip |         | +-----------------------+
| +-------+-----------+-----------+-----+           |           ^
| | 1     | sensor-A  | fac1      | eq1   | <------lookup-----+
| | 2     | sensor-B  | fac1      | eq2   |         |           |
| | ...   | ...       | ...       | ...   |         |           | (Aggregated From)
+---------+-----------+-----------+-------+         |           |
       (Memory Resident Lookup)                     |           |
                                                    |           |
                      +-----------------------------+-----------+
                      | (Data distributed by hash(NAME))
                      |
        +-------------+-------------+ ... +-------------+
        |             |             |     |             |
+-------v-------+ +---v-----------+ +-----+-------------v---+
| _MYTAG_DATA_0 | | _MYTAG_DATA_1 | | ... | | _MYTAG_DATA_3 |
| +---+ T | V + | | +---+ T | V + | |     | | +---+ T | V + |
| | 0 |...|...| | | | 1 |...|...| | |     | | | 3 |...|...| |
| | 0 |...|...| | | | 1 |...|...| | |     | | |.. |...|...| |
| +---+---+---+ | | +---+---+---+ | |     | | +---+---+---+ |
+---------------+ +---------------+ +-----+ +---------------+
   (Data Partition) (Data Partition)         (Data Partition)
```

## 태그 테이블의 메타데이터 관리

### 메타데이터의 역할

메타데이터는 원시 시계열 데이터에 꼭 필요한 맥락 정보를 제공합니다. 각 태그(`name`)에 위치, 장비 종류, 제조사, 측정 단위 같은 설명 속성을 연결하면 다음과 같은 작업이 가능해집니다.

*   **구조화된 검색:** 알아보기 어려운 태그 이름만이 아니라 특성을 기준으로 데이터를 필터링하고 조회합니다.
*   **계층적 구성:** 센서, 장비, 위치 등의 관계를 표현합니다.
*   **분석 확장:** 메타데이터로 정의한 의미 있는 범주별로 데이터를 그룹화하고 집계합니다.

**개념적 계층 구조 예시:**

```
Company
├── city1 Plant
│   ├── Air Conditioner
│   │   ├── Tag (Current Sensor)
│   │   ├── Tag (Voltage Sensor)
│   │   └── ...
│   ├── Refrigerator
│   ├── Compressor
│   └── Crane
├── city2 Plant
│   ├── ... (similar structure)
└── city3 Plant
    └── ... (similar structure)
```

각 태그는 공장, 장비 같은 자신의 맥락 정보를 함께 갖습니다.

**활용 예시:**

*   "울산 공장의 크레인에 연결된 모든 전류 센서의 최근 1분 데이터를 조회합니다."
*   "냉장고에 속하고 이름이 Current로 시작하는 센서의 2022년 1월 31일 11:00~12:00 데이터를 모두 가져옵니다."
*   "모든 공장에서 이름이 에어컨으로 시작하는 장비를 대상으로, Current-3이라는 태그의 지난달 최댓값을 찾습니다."

### 메타데이터 컬럼 정의와 활용

메타데이터 컬럼은 `CREATE TAG TABLE` 문의 `METADATA` 절에서 정의합니다.

```sql
CREATE TAG TABLE MYTAG (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
)
METADATA ( -- Define metadata columns here
    factory VARCHAR(32),
    equipment VARCHAR(64)
);
```

내부 메타데이터 테이블(`_tableName_META`)에 `ALTER TABLE`을 실행해 기존 태그 테이블의 메타데이터 구조에 컬럼을 추가할 수도 있습니다.

```sql
ALTER TABLE _mytag_meta ADD COLUMN (line VARCHAR(16) DEFAULT 'op01');
```

메타데이터는 `_tableName_META` 테이블에 저장되며, 가상 태그 테이블을 조회할 때 효율적으로 조인할 수 있도록 보통 메모리에 유지됩니다. `name` 컬럼은 메타데이터 속성과 시계열 데이터를 연결하는 고유 키입니다.

```
       Metadata Area (_mytag_meta)             Data Area (_mytag_data_N)
+---------+----------+------------+----------+   +----+---------------------+-------+
| NAME    | factory  | equipment  | line     |   | ID | TIME                | VALUE |
+---------+----------+------------+----------+   +----+---------------------+-------+
| Sensor-A| Seoul    | drill      | op01     |   | 0  | ...                 | -1.3  | <= Data for Sensor-A
| Sensor-B| Seoul    | punch      | op01     |   | 1  | ...                 | -2.3  | <= Data for Sensor-B
| Sensor-C| Ulsan    | rolling    | op01     |   | 2  | ...                 | -3.3  | <= Data for Sensor-C
+---------+----------+------------+----------+   | ...| ...                 | ...   |
       (Unique entries per NAME)                      (Time-series measurements)
```

### 메타데이터 적재

새 태그의 메타데이터는 보통 해당 태그의 데이터를 처음 적재할 때 함께 제공합니다. 데이터를 append할 때 태그 `name`이 `_tableName_META` 테이블에 없으면, 그 append 작업에서 전달한 값으로 새 메타데이터 레코드가 생성됩니다.

**주의할 점:** 태그 `name`이 이미 메타데이터 테이블에 있으면, 이후 해당 태그의 데이터를 append해도 기존 메타데이터 속성은 **갱신되지 않습니다**. 메타데이터를 갱신하려면 `UPDATE ... METADATA` 명령을 명시적으로 실행해야 합니다.

### 메타데이터 조건으로 데이터 조회

가상 태그 테이블을 조회하는 쿼리에는 데이터 컬럼(`time`, `value` 등)과 메타데이터 컬럼(`factory`, `equipment` 등) 모두에 조건을 지정할 수 있습니다. 데이터베이스 엔진은 태그 `name`을 기준으로 데이터 파티션과 메타데이터 테이블을 자동으로 조인합니다.

```sql
-- Retrieve data for a specific tag in a specific factory and equipment
-- within a given time range.
SELECT name, time, value, factory, equipment
FROM mytag
WHERE factory = 'Seoul'            -- Metadata filter
  AND equipment LIKE '%chill%'     -- Metadata filter (LIKE supported)
  AND name = 'tag-1'               -- Data/Tag identifier filter
  AND time BETWEEN TO_DATE('2022-01-01 00:00:00')
               AND TO_DATE('2022-12-31 23:59:59'); -- Time filter
```

### 메타데이터 항목 수정

특정 태그의 기존 메타데이터 속성은 `UPDATE ... METADATA SET` 구문으로 수정할 수 있습니다.

```sql
UPDATE mytag METADATA SET equipment = 'chiller_unit_01', factory = 'Busan'
WHERE name = 'tag-existing'; -- MUST specify the target tag via 'name = ...'
```

**제약 사항:**

*   `WHERE` 절에는 `name` 컬럼에 대한 동등 조건(`WHERE name = 'specific_tag_name'`)이 **반드시** 있어야 합니다.
*   내부 메타데이터 저장소가 키-값 구조이므로, 메타데이터를 갱신할 때는 `WHERE` 절에 다른 조건을 사용할 수 없습니다.
*   이 명령은 메타데이터 속성값을 기준으로 한 일괄 갱신을 직접 지원하지 않습니다(향후 개선될 수 있습니다).

### 메타데이터 항목 삭제

메타데이터 항목은 `DELETE FROM ... METADATA` 구문으로 삭제할 수 있습니다.

```sql
DELETE FROM mytag METADATA WHERE name = 'tag_to_remove';
```

**제약 사항:**

*   데이터 파티션에 해당 태그의 시계열 데이터가 남아 있으면 메타데이터 항목을 삭제할 수 **없습니다**.
*   메타데이터 항목을 삭제하려면 먼저 일반 `DELETE FROM table_name WHERE name = '...'` 명령으로 관련 시계열 데이터를 삭제해야 합니다.

### 활용 사례: 메타데이터를 이용한 동적 태그 분류

메타데이터 컬럼을 사용하면 핵심 데이터 구조를 바꾸지 않고도 태그를 동적으로 분류하거나 주석을 달 수 있습니다.

**시나리오:** 오류가 자주 발생하는 태그나 특정 보고서에 사용하는 태그를 추적합니다.

1.  **`alias` 메타데이터 컬럼 추가:**

    ```sql
    ALTER TABLE _basic_meta ADD COLUMN (alias VARCHAR(128) DEFAULT 'normal');
    ```

2.  **특정 태그의 메타데이터 갱신:**

    ```sql
    UPDATE basic METADATA SET alias = 'error' WHERE name = 'tag-2';
    UPDATE basic METADATA SET alias = 'report' WHERE name = 'tag-4';
    ```

3.  **동적 분류를 기준으로 데이터 조회:**

    ```sql
    -- Find data for tags marked as 'error' within a specific time range
    SELECT * FROM basic
    WHERE alias = 'error'
      AND time BETWEEN '2022-01-01' AND '2022-12-31';

    -- Find data for tags marked for 'report'
    SELECT * FROM basic
    WHERE alias = 'report'
      AND time BETWEEN '2022-01-01' AND '2022-12-31';
    ```

### `name` 컬럼의 고유성과 활용

`name` 컬럼(또는 태그 테이블 정의에서 `PRIMARY KEY`로 지정한 컬럼)은 다음과 같이 중요한 역할을 합니다.

*   **메타데이터의 기본 키:** `_tableName_META` 테이블에서 각 태그를 고유하게 식별해 메타데이터 속성의 생성·조회·수정·삭제(CRUD)를 가능하게 합니다. 태그 이름은 고유해야 합니다.
*   **데이터 조회 시 연결 고리:** 쿼리를 실행할 때 메타데이터 속성과 해당 시계열 데이터를 연결합니다.
*   **직접 데이터 필터링:** 특정 태그의 원시 데이터와 집계 데이터를 직접 선택하거나 필터링할 수 있습니다.

**`name` 값 구성 팁:**

*   **태그 수가 적고(100개 미만) 메타데이터가 없는 경우:** `'tag_001'`, `'temp_sensor_main'`처럼 사람이 읽기 쉬운 단순한 고유 문자열을 사용합니다. 보통 `name`으로 직접 조회합니다.
*   **태그 수가 많고(1000개를 크게 초과) 메타데이터가 풍부한 경우:** 전체 `name`으로 직접 조회하는 일은 드물 수 있습니다. 주요 메타데이터 필드를 이어 붙여 `name`을 구성하면(예: `'factoryA-equipmentX-sensorTypeZ-instance01'`) 고유성을 보장하고 어느 정도 맥락도 담을 수 있지만, 주된 조회에는 전용 메타데이터 컬럼으로 필터링해야 합니다(예: `WHERE factory = 'factoryA' AND equipment = 'equipmentX'`). 대규모의 복잡한 시스템에서는 이 방식이 태그 탐색과 필터링에 더 적합합니다.

## 태그 테이블 활용

### 태그 테이블 설계 예시

특정 생산 로트와 연결된 여러 센서 측정값을 추적하는 제조 시나리오를 예로 듭니다.

```sql
-- Tag table definition
CREATE TAG TABLE tag (
    name                   VARCHAR(100) PRIMARY KEY, -- Unique identifier, potentially combination of factory/equip/tag_id
    time                   DATETIME BASETIME,
    value                  DOUBLE SUMMARIZED,
    lot_no                 VARCHAR(32)             -- Additional data column specific to each reading
)
METADATA (
    factory_id             VARCHAR(16),             -- Metadata: Factory identifier
    equipment_id           VARCHAR(16),             -- Metadata: Equipment identifier
    tag_id                 VARCHAR(32)              -- Metadata: Base sensor identifier
);

-- Optional: Create an index on the additional data column for faster lookups by lot_no
CREATE INDEX idx_tag_lot_no ON tag (lot_no) INDEX_TYPE TAG;
```

**쿼리 예시:**

```sql
-- Retrieve all tag data for a specific factory
SELECT * FROM tag WHERE factory_id = 'fac01';

-- Retrieve data for a specific equipment within a specific factory
SELECT * FROM tag WHERE factory_id = 'fac01' AND equipment_id = 'equip01';

-- Retrieve specific columns for data associated with a particular production lot
SELECT name, time, value FROM tag WHERE lot_no = 'lot2001'; -- Uses idx_tag_lot_no if beneficial

-- Retrieve data for specific tags on specific equipment/factory within a time range
SELECT * FROM tag
WHERE factory_id = 'fac01'
  AND equipment_id = 'equip01'
  AND tag_id IN ('tag01', 'tag02', 'tag03') -- Filter using metadata tag_id
  AND time BETWEEN TO_DATE('2023-08-15 00:00:00') AND TO_DATE('2023-08-15 23:59:59');
```

### 기본 데이터 조회

표준 SQL `SELECT` 문을 사용하며, `name`과 `time`에 자동으로 적용되는 인덱스를 활용합니다.

```sql
-- Get total record count
SELECT count(*) FROM tag;

-- Get overall time range of data
SELECT min(time), max(time) FROM tag;

-- Retrieve raw data for a specific tag within a time range (ordered chronologically)
SELECT time, value FROM tag
WHERE name = 'TAG_00001'
  AND time BETWEEN TO_DATE('2023-01-01') AND TO_DATE('2023-01-31');

-- Retrieve raw data for multiple specific tags, ordered reverse chronologically
SELECT /*+ SCAN_BACKWARD(tag) */ time, value FROM tag
WHERE name IN ('TAG1', 'TAG2')
  AND time BETWEEN TO_DATE('2023-01-01') AND TO_DATE('2023-01-31');
```

**참고:** `name` 컬럼 조건에서는 일반적으로 동등 비교(`=`)와 `IN` 목록 비교를 효율적으로 처리합니다.

### 복합 분석 시나리오

태그 테이블을 메타데이터 및 선택 기능인 롤업과 함께 사용하면 정교한 분석을 수행할 수 있습니다.

**시나리오 설정 예시:**

```sql
CREATE TAG TABLE MYTAG (
    name VARCHAR(32) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
)
METADATA (
    factory VARCHAR(32),
    equipment VARCHAR(64),
    alias VARCHAR(64) -- For dynamic tagging
)
WITH ROLLUP EXTENSION; -- Enable automatic time-based aggregation, including FIRST()/LAST() (details in Rollup documentation)
```

**쿼리 유형:**

1.  **원시 데이터 추출:**
    *   Seoul 공장의 2024년 2월 12일 전체 태그 데이터.
    *   Seoul 공장 압축기의 2024년 7월 12일 12:00~13:00 데이터.
    *   모든 공장의 냉각 장치에 연결되고 이름이 Current로 시작하는 태그의 2024년 9월 13일 13:20~13:30 데이터.
    *   alias가 CriticalSensor인 모든 태그의 2024년 12월 23일~12월 29일 데이터.

2.  **통계 데이터 추출(롤업 사용):**
    *   Seoul 공장 크레인의 모든 태그에 대한 2024년 전체 월별 `value` 평균.
    *   Cheongju 공장에서 이름에 Current가 포함된 태그의 2024년 6월 일별 `value` 최댓값.
    *   모든 공장에서 alias가 CriticalSensor인 모든 태그의 2020년~2024년 월별 `value` 평균.

3.  **통계 데이터 기반 분석(롤업 사용):**
    *   최근 5년간 이름에 Power가 포함된 모든 센서에 대해, 최댓값이 기록된 주와 그 주의 최댓값을 찾습니다.
    *   최근 1년간 Cheongju 공장에서 이름에 Temperature가 포함된 모든 센서에 대해, 일별 최고 온도가 가장 높았던 날과 그날의 평균 온도를 찾습니다.
    *   최근 3개월간 모든 공장에서 이름에 Pressure가 포함된 센서에 대해, 일별 평균 압력이 가장 높았던 날과 그 평균값을 찾습니다.

**쿼리 예시(시간별 평균과 마지막 값):**

```sql
-- Get hourly average and last value for all tags in 'factory1' for a 12-hour period
SELECT
    name,
    ROLLUP('hour', 1, time) AS rollup_time, -- Aggregate time to the hour
    AVG(value) AS avg_value,
    LAST(time, value) AS last_value -- Get the last value within the hour
FROM mytag
WHERE name IN (SELECT name FROM _mytag_meta WHERE factory = 'factory1') -- Filter tags by metadata
  AND time BETWEEN TO_DATE('2000-01-01 00:00:00') AND TO_DATE('2000-01-01 11:59:59') -- Time range
GROUP BY name, rollup_time -- Group by tag and aggregated time interval
ORDER BY name, rollup_time;
```

### PIVOT을 이용한 데이터 모델 변환

`PIVOT` 절을 사용하면 세로형 태그 테이블 데이터를 전통적인 모델과 비슷한 가로형 형식으로 다시 변환해, 특정 분석이나 보고서 요구에 맞출 수 있습니다.

```sql
-- Pivot selected tag values into columns based on time
SELECT *
FROM (
    -- Subquery selecting relevant data
    SELECT time, name, value -- Assuming name corresponds to tagid, value to dvalue
    FROM mytag
    WHERE time BETWEEN TO_DATE('2018-12-07 00:00:00') AND TO_DATE('2018-12-08 05:00:00')
      AND name IN ('FRONT_AXIS_TORQUE', 'REAR_AXIS_TORQUE', 'HOIST_AXIS_TORQUE', 'SLIDE_AXIS_TORQUE')
)
PIVOT (
    SUM(value) -- Aggregation function applied if multiple values exist for the same time/tag
    FOR name -- The column whose unique values become the new column headers
    IN ('FRONT_AXIS_TORQUE', 'REAR_AXIS_TORQUE', 'HOIST_AXIS_TORQUE', 'SLIDE_AXIS_TORQUE') -- List of tag names to pivot into columns
)
WHERE "FRONT_AXIS_TORQUE" >= 40 AND "REAR_AXIS_TORQUE" >= 20; -- Optional filtering on pivoted columns
```

**출력 예시(개념):**

```
time                          'FRONT_AXIS_TORQUE' 'REAR_AXIS_TORQUE' 'HOIST_AXIS_TORQUE' 'SLIDE_AXIS_TORQUE'
----------------------------- ------------------- ------------------ ------------------- -------------------
2018-12-07 16:42:29 840:000:000 12158               7244               NULL                NULL
2018-12-07 14:56:26 220:000:000 3308                663                NULL                NULL
...                           ...                 ...                ...                 ...
```

*(참고: 피벗된 컬럼 이름이 키워드와 같거나 특수 문자를 포함하면 따옴표로 감싸야 할 수 있습니다.)*

### 데이터 삭제

태그 테이블의 데이터 삭제는 주로 시간이나 태그를 기준으로 합니다. append에 최적화된 구조이므로 개별 레코드 단위의 갱신이나 삭제는 일반적으로 지원하지 않습니다.

**삭제 구문 예시:**

```sql
-- Delete all data BEFORE a specific timestamp across all tags
DELETE FROM table_name BEFORE TO_DATE('2023-01-15 00:00:00');

-- Delete ALL data from the table (use with extreme caution)
DELETE FROM table_name;

-- Delete all data for a SPECIFIC tag
DELETE FROM table_name WHERE name = 'TAG01';

-- Delete data for a SPECIFIC tag BEFORE a specific timestamp
DELETE FROM table_name WHERE name = 'TAG01' AND time < TO_DATE('2023-02-01 00:00:00');
```

## 태그 테이블의 인덱스

### 내부 인덱스와 외부 인덱스

태그 테이블에는 (`name`, `time`) 컬럼에 자동으로 생성되는, 고도로 최적화된 **내부 인덱스**가 있습니다. 이 인덱스가 일반적인 시계열 쿼리 성능의 기반입니다. 결과를 시간 순서로 반환하려면 `ORDER BY time`을 지정하십시오.

*   **쿼리 `WHERE name = '...'`:** 내부 인덱스를 사용해 지정한 태그의 모든 데이터를 효율적으로 찾습니다.
*   **쿼리 `WHERE time BETWEEN ... AND ...`:** 내부 인덱스를 사용해 지정한 시간 범위에 있는 모든 태그의 데이터를 스캔합니다.
*   **쿼리 `WHERE name = '...' AND time BETWEEN ... AND ...`:** 내부 인덱스를 사용해 특정 시간 범위에 있는 특정 태그의 데이터를 매우 효율적으로 조회합니다.
*   **쿼리 `WHERE name = '...' AND time BETWEEN ... AND ... AND value > ...`:** 내부 인덱스로 해당 (`name`, `time`) 데이터 블록을 찾은 뒤, 조회한 데이터에 `value` 조건을 적용합니다.

**과제:** `name`이나 `time` 조건 없이 `value` 컬럼(또는 추가 데이터 컬럼)*만으로* 필터링하는 쿼리는 기본 내부 인덱스를 효과적으로 사용할 수 없습니다.

*   **쿼리 `WHERE name = '...' AND value > ...`(시간 조건 없음):** `value` 조건을 적용하려면 `'tag-1'`에 속한 *모든* 데이터 블록을 스캔해야 합니다. 성능은 해당 태그의 전체 데이터 양에 비례해 떨어집니다.

이런 경우에는 **외부 인덱스**를 생성할 수 있습니다.

### 외부 인덱스 생성과 활용

`value` 컬럼이나 그 밖의 추가 데이터 컬럼에 외부 인덱스를 명시적으로 생성하면, 주로 이 컬럼으로 필터링하는 쿼리를 빠르게 처리할 수 있습니다.

**구문:**

```sql
CREATE INDEX index_name ON table_name (column_name) [INDEX_TYPE TAG];
-- INDEX_TYPE TAG is specific for optimizing indexes on Tag Table data columns.
```

**예시:**

```sql
CREATE TAG TABLE mytag (
    name VARCHAR(100) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED,
    lot_no VARCHAR(32)
);

-- Create external indexes on 'value' and 'lot_no' columns
CREATE INDEX idx_mytag_value ON mytag(value) INDEX_TYPE TAG;
CREATE INDEX idx_mytag_lotno ON mytag(lot_no) INDEX_TYPE TAG;

-- This query can now potentially use the external index idx_mytag_value
SELECT * FROM mytag WHERE name = 'TAG-2' AND value > 33;

-- This query can potentially use the external index idx_mytag_lotno
SELECT * FROM mytag WHERE lot_no = 'LOTXYZ' AND time > TO_DATE('2024-01-01');
```

**외부 인덱스의 특징:**

*   **비동기:** 인덱스 갱신이 데이터 적재보다 약간 늦을 수 있습니다. 새로 적재한 데이터가 아직 외부 인덱스에 반영되지 않은 짧은 시간 차이가 생길 수 있습니다.
*   **로컬 구조:** 외부 인덱스는 보통 데이터 파티션과 함께 로컬로 분할됩니다. 전체 데이터 양이 늘어나면 외부 인덱스를 사용하는 쿼리도 성능이 다소 떨어질 수 있지만, 인덱스 없이 전체를 스캔할 때보다는 훨씬 빠릅니다.
*   **자원 소비:** 외부 인덱스는 추가 저장 공간을 사용하고, 데이터를 적재할 때 오버헤드를 발생시킵니다.

## 태그 테이블 데이터 적재

### 적재 방법 개요

Machbase Neo는 성능 요구 사항과 클라이언트 환경에 맞춰 태그 테이블에 데이터를 적재하는 여러 방법을 제공합니다.

```
+-------------------+      +-------------------+      +-------------------+
|    ODBC/JDBC/     |      |    MQTT/gRPC/     |      |    Machbase       |
|   .NET Clients    | ---> |   HTTP Clients    | ---> |     Native        | ---> Machbase Neo
+-------------------+      +-------------------+      |  CLI/SDK (C/Py)   |      (Tag Table)
                                                     +-------------------+
 (Standard SQL INSERT,      (REST API /append,       (High-Throughput
  or Append Protocol)        MQTT Subscription)        Append Protocol)
```

### 적재 방법 상세

1.  **SQL `INSERT` 문:**
    *   표준 `INSERT INTO table_name VALUES (...)` 구문을 사용합니다.
    *   요청/응답 방식으로 동작합니다.
    *   데이터 양이 적거나 입력이 드문 경우에 적합합니다.
    *   성능 제약 때문에 처리량이 높은 대용량 시계열 데이터에는 **권장하지 않습니다**.

2.  **Append 프로토콜:**
    *   대량 데이터 적재에 최적화된 Machbase 전용 고성능 프로토콜입니다.
    *   네트워크 오버헤드와 레코드별 서버 측 처리를 최소화합니다.
    *   다음 방법으로 사용할 수 있습니다.
        *   **Machbase CLI(Command Line Interface):** 파일에서 데이터를 대량으로 적재하는 유틸리티입니다.
        *   **ODBC/JDBC/.NET:** Machbase 드라이버가 제공하는 확장 API로 Append 작업을 수행할 수 있습니다.
        *   **C/C++/Go SDK:** 네이티브 라이브러리로 Append API에 직접 접근해 최대 성능을 얻을 수 있습니다.
        *   **Python(`machbaseAPI`):** Append 기능을 제공하는 래퍼 라이브러리입니다.
    *   높은 처리량이 필요한 대부분의 시계열 적재 시나리오에 **권장합니다**.

3.  **REST API:**
    *   Machbase Neo는 데이터 처리를 위한 HTTP 엔드포인트를 제공합니다.
    *   데이터 적재 엔드포인트는 `append` 메서드 파라미터를 지원하며, 내부적으로 효율적인 Append 프로토콜을 사용합니다.
    *   웹 기반 클라이언트나 HTTP로 연동하는 시스템에 적합합니다.

4.  **기타 언어(Python, Go, R):**
    *   보통 CLI나 ODBC/네이티브 SDK의 래퍼를 통해 효율적인 Append 프로토콜을 사용합니다.

**성능 참고:** 초당 수십만~수백만 건의 입력이 필요한 고주파 진동 데이터처럼 요구 조건이 까다로운 경우, 최고 적재 속도를 얻으려면 네이티브 C/C++ SDK의 Append API를 사용해야 하는 경우가 많습니다.

## 운영 시 고려 사항

### 주요 사용 주의 사항

*   **메모리 소비:** 각 태그 테이블은 파티션(`TAG_PARTITION_COUNT`)과 데이터 버퍼(`TAG_DATA_PART_SIZE`)에 따라 기본 메모리를 사용합니다. 태그 테이블을 많이 만들면 서버 전체 메모리 사용량이 크게 늘어날 수 있으므로, 사용 가능한 자원을 고려해 테이블 생성을 계획하십시오.
*   **쿼리 성능:** 인덱스가 있는 컬럼(`name`, `time` 또는 외부 인덱스가 있는 컬럼)에 조건이 없는 `SELECT` 쿼리는 전체 테이블 스캔이나 넓은 범위의 스캔이 되어, 데이터 양에 비례해 성능이 떨어집니다. 가능하면 항상 `name`이나 `time` 범위 조건을 포함하십시오.
*   **외부 인덱스:** 시간 조건 없이 데이터/값 컬럼*만으로* 필터링하는 쿼리가 잦을 때만 외부 인덱스를 생성하십시오. 외부 인덱스는 저장 공간과 적재 오버헤드를 늘립니다.
*   **데이터 불변성:** 태그 테이블은 추가(append) 전용 데이터를 위해 설계되었습니다. 기존 데이터 레코드의 갱신은 지원하지 않으며, 삭제는 주로 시간 기준이나 태그 전체 단위로 합니다.
*   **적재 방법:** 성능 요구 사항에 맞는 적재 방법을 선택하십시오. 대용량 데이터에는 SDK, CLI, 드라이버, REST API의 `append` 메서드 등을 통해 Append 프로토콜을 사용합니다.

### 메모리 소비 고려 사항

태그 테이블의 메모리 사용량에는 다음 요인이 영향을 줍니다.

*   **적재 버퍼:** `TAG_DATA_PART_SIZE`(기본값 16MB)에 비례합니다. 내부적으로 여러 버퍼를 사용합니다.
*   **파티션 수:** `TAG_PARTITION_COUNT`(기본값 4)입니다. 파티션마다 자체 버퍼와 인덱스 구조를 유지합니다.
*   **인덱스 공간:** 각 파티션의 데이터 양과 카디널리티에 따라 동적으로 할당됩니다. 대략 `TAG_DATA_PART_SIZE`와 평균 행 크기에 따라 달라집니다.

**테이블당 대략적인 메모리 계산식:**

`Memory ≈ (TAG_DATA_PART_SIZE * BufferFactor) + ((IndexSizeFactor * TAG_DATA_PART_SIZE / AvgRowSize) * IndexOverheadFactor) * TAG_PARTITION_COUNT`

*(내부 계수와 동적 할당 때문에 정확히 계산하기는 어렵지만, 이 식은 주요 요인을 보여 줍니다.)*

기본 설정(`TAG_PARTITION_COUNT=4`, `TAG_DATA_PART_SIZE=16MB`)에서 태그 테이블은 부하에 따라 주로 인덱싱과 버퍼링에 **최대 약 4GB**(파티션당 약 1GB)의 메모리를 동적으로 사용할 수 있습니다. 이 값은 부하에 따라 달라지는 추정치이며, 필요한 RAM 용량이나 사용량 상한을 보장하는 값이 아닙니다.

**메모리 사용량 관리:**

*   **`TAG_PARTITION_COUNT` 줄이기:** 테이블을 생성할 때 파티션 수를 1이나 2처럼 낮게 설정하면 병렬 처리 수준과 관련 메모리가 직접 줄어듭니다. 이 속성은 `ALTER TABLE`로 동적으로 변경할 수 없습니다. 자원이 제한된 환경에 적합하지만 최대 동시 처리 성능에 영향을 줄 수 있습니다.
*   **`TAG_DATA_PART_SIZE` 조정:** 서버 설정에서 이 속성 값을 줄이면(예: 4MB 또는 8MB, 1MB 이상이어야 함) 내부 버퍼와 인덱스 세그먼트 크기가 작아져 메모리 부담이 줄어듭니다. 변경 사항을 적용하려면 서버를 다시 시작해야 합니다.

## 기본 구성과 적재 예시

다음은 태그마다 `factory`와 `equipment` 속성을 갖는 `vibration` 테이블 예시입니다.

```sql
CREATE TAG TABLE vibration (
    name  VARCHAR(80) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
)
METADATA (
    factory   VARCHAR(32),
    equipment VARCHAR(64)
)
TAG_PARTITION_COUNT = 2,
TAG_STAT_ENABLE     = 1;
```

### 메타데이터 컬럼 추가와 등록

태그별 부가 정보는 메타 테이블 `_vibration_meta`에 저장합니다. 구조를 변경할 때는 `ALTER TABLE`을 사용하며, 메타데이터 컬럼은 `ADD COLUMN`으로 추가하고 `DROP COLUMN`으로 삭제할 수 있습니다.

```sql
ALTER TABLE _vibration_meta ADD COLUMN (location VARCHAR(32));
INSERT INTO vibration METADATA (name, factory, equipment)
VALUES ('sensor-A', 'factory-1', 'machine-1');
```

### 데이터 적재

#### import 도구

CSV 필드는 메타데이터 컬럼을 포함한 테이블의 컬럼 순서(`name`, `time`, `value`, `factory`, `equipment`, `location`)에 맞춥니다. 파일의 첫 줄에 `name,time,value`처럼 컬럼 이름이 있으면 `--header columns`로 그 이름에 따라 필드를 대응시킬 수 있습니다. `machbase-neo shell`은 현재 디렉토리를 `/work`에 마운트하므로 파일이 있는 디렉토리에서 명령을 실행합니다. 다음 예시는 시간을 초 단위 Unix epoch 시간으로 지정합니다.

```bash
machbase-neo shell import --input /work/data.csv --timeformat s vibration
machbase-neo shell import --input /work/data_header.csv --header columns --timeformat s vibration
```

#### REST API 사용

날짜·시간 문자열을 사용할 때는 `timeformat`을 명시합니다. JSON 페이로드에서는 HTTP 쓰기 API의 `data.columns`와 `data.rows`로 데이터를 지정합니다.

```http
POST /db/write/vibration?timeformat=DEFAULT
Content-Type: application/json

{
  "data": {
    "columns": ["name", "time", "value"],
    "rows": [
      ["sensor-A", "2024-03-01 10:00:00", 12.3],
      ["sensor-B", "2024-03-01 10:00:00", 15.7]
    ]
  }
}
```

### 롤업과 통계

- `WITH ROLLUP`을 지정하면 초·분·시간 단위의 집계 테이블이 자동으로 생성되어 시간 구간별 분석이 빨라집니다.
- `TAG_STAT_ENABLE=1`이면 `v$<table>_stat` 뷰에서 태그별 건수, 최솟값·최댓값, 최신 시각 등의 통계를 바로 확인할 수 있습니다.

### 뷰 구성 예시

```sql
CREATE VIEW vibration_view AS
SELECT m.name,
       m.factory,
       m.equipment,
       d.time,
       d.value
FROM vibration d
JOIN _vibration_meta m ON d.name = m.name;
```

### 운영 팁

- **중복 데이터 방지**: `TAG_DUPLICATE_CHECK_DURATION` 값을 설정하면 해당 기간 안에 들어온 동일한 `(name, time)` 데이터는 자동으로 무시됩니다.
- **보관 기간 관리**: 보관 정책(Retention Policy)을 추가해 일정 기간이 지난 데이터가 자동으로 삭제되도록 설정하십시오.
- **파티션 수 선택**: 테이블을 생성할 때 고성능 서버에는 높은 `TAG_PARTITION_COUNT`, 엣지 장비에는 낮은 값을 선택해 자원 사용량을 조절합니다.

Machbase 태그 테이블은 간단한 스키마로 대량의 시계열 데이터를 적재·분석할 수 있도록 설계되어 있으며, 롤업·통계·보관 정책과 결합해 완성도 높은 시계열 데이터 플랫폼을 구성할 수 있습니다.

## 요약

Machbase 태그 테이블은 센서 시계열 데이터를 효율적으로 관리하도록 설계된 전용 데이터베이스 객체입니다. 주요 특징은 다음과 같습니다.

*   **최적화된 구조:** 센서 측정값에 적합한 세로형 데이터 모델([식별자, 시간, 값])을 사용합니다.
*   **메타데이터와 데이터 분리:** 설명 속성(메타데이터)과 원시 시계열 측정값(데이터)을 분리해 메타데이터를 유연하게 관리하고 데이터를 효율적으로 저장합니다.
*   **메타데이터 관리:** 메타데이터는 고유한 태그 `name`(기본 키)으로 연결되며, 유연한 조회·추가·수정·삭제를 지원합니다. 단, 삭제하려면 먼저 해당 데이터를 삭제해야 합니다.
*   **데이터 작업:** 고속 append 작업에 최적화되어 있습니다. 태그 `name`이나 `time`으로 필터링하면 매우 효율적으로 조회할 수 있습니다. 데이터 갱신은 지원하지 않으며, 삭제는 주로 시간 범위나 태그 단위로 합니다.
*   **확장성:** 메타데이터 영역과 데이터 영역 모두 컬럼을 추가해 더 풍부한 맥락 정보나 측정 정보를 저장할 수 있습니다.
*   **성능:** 내부 파티셔닝과 전용 인덱스를 활용해 높은 적재 처리량과 빠른 시간 기반 조회 성능을 제공합니다.

태그 테이블은 Machbase 생태계에서 확장 가능한 시계열 애플리케이션을 구축하기 위한 견고하고 성능이 뛰어난 기반을 제공합니다.
