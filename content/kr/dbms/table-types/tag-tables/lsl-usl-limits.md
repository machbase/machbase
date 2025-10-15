---
title: 'LSL/USL을 통한 데이터 품질 관리'
type: docs
weight: 80
---

## 개요

LSL (Lower Specification Limit)과 USL (Upper Specification Limit)은 태그 값에 대한 자동 데이터 검증을 제공하여 범위를 벗어난 센서 읽기가 데이터를 손상시키는 것을 방지합니다.

## LSL/USL 소개

`LSL(Lower Specification Limit)`은 하한 사양 제한을 나타내고, `USL(Upper Specification Limit)`은 상한 사양 제한을 의미합니다.
Machbase에서 LSL/USL 기능은 Tag 테이블에 종속된 태그 메타데이터 테이블에서만 지원됩니다.
LSL/USL 기능은 특정 TAG ID에 대한 상한 및 하한 사양 제한을 설정하여 예기치 않은 데이터 입력에 대한 보호 조치로 사용됩니다.  

## 제약 조건

LSL/USL 설정에는 몇 가지 제약 조건이 있습니다.

* `CLUSTER EDITION`은 LSL/USL 기능을 지원하지 않습니다.
* LSL/USL을 설정하려면 Tag 테이블의 세 번째 컬럼인 __Value__가 __SUMMARIZED__로 설정되어야 합니다.
* LSL은 USL보다 작거나 같아야 하며, __Value__ 컬럼의 입력 값은 LSL과 USL 사이에 있어야 합니다 (포함). __(LSL <= Value <= USL)__
* LSL/USL 설정을 부여하기 전에 입력된 데이터는 검증되지 않습니다.
* LSL/USL 컬럼을 NULL로 설정하면 입력 데이터를 검증하지 않습니다.
* LSL/USL 기능은 개별적으로 사용할 수 있습니다. 상한 사양만 일치시키려면 USL만 설정할 수 있습니다.
* USL 기능만 사용하는 경우 USL보다 낮은 데이터는 검증되지 않습니다.

### 지원되는 데이터 타입

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

## LSL/USL 설정 및 사용

LSL/USL 기능을 사용하려면 태그 메타데이터 테이블의 컬럼에 특정 키워드를 설정해야 합니다.

* LSL의 경우 `LOWER LIMIT` 키워드를 사용합니다.
* USL의 경우 `UPPER LIMIT` 키워드를 사용합니다.

이러한 설정은 Tag 테이블을 생성할 때 또는 메타데이터 컬럼을 추가할 때 할 수 있습니다. 다음은 몇 가지 예제입니다.

### CRAETE

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

두 컬럼을 함께 사용할 수도 있지만 원하는 경우 하나만 사용할 수도 있습니다.
LSL만 설정하면 LSL보다 높은 데이터는 검증되지 않습니다. 이는 `USL == NULL`로 설정하는 것과 같습니다.

```sql
CREATE TAG TABLE example (
    tag_id  VARCHAR(50) PRIMARY KEY,
    time    DATETIME    BASETIME,
    value   INTEGER     SUMMARIZED)
METADATA (
    lsl    INTEGER LOWER LIMIT  
);
```

### ADD COLUMN

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

### INSERT

LSL/USL 기능이 설정되고 특정 TAG ID에 대한 LSL/USL이 설정되면 데이터를 입력할 준비가 됩니다.

```sql
INSERT INTO example metadata VALUES ('TAG_01', 100, 200);
```

설정 후 태그 데이터를 입력할 때 다음과 같이 작동합니다.

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

값을 입력한 후 Tag 테이블을 보면 검증된 데이터만 입력되었음을 확인할 수 있습니다.

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

### UPDATE

태그 메타 테이블에 설정된 LSL/USL 컬럼의 값을 수정할 수 있습니다.
태그 데이터 테이블에 이미 입력된 데이터는 검증하지 않으므로 주의해서 사용하십시오.

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

### DELETE

태그 메타 테이블은 `DROP COLUMN` 기능을 지원하지 않으므로 LSL/USL 컬럼만 삭제할 수 있는 직접적인 방법이 없습니다.
컬럼을 삭제할 수는 없지만 LSL/USL 컬럼 값을 NULL로 설정하면 제약 없이 데이터를 입력할 수 있습니다.

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

[^1]: [IEEE 754](https://en.wikipedia.org/wiki/IEEE_754)
