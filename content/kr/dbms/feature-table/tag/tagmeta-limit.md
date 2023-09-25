---
type: docs
title : '태그 메타 LSL/USL 설정'
weight: 80
---

## LSL/USL 소개

`LSL(Lower Specification Limit)`은 규격 하한의 뜻을 가지고 `USL(Upper Specification Limit)`은 규격 상한을 의미한다.  
마크베이스에서 지원하는 LSL/USL 기능은 태그 테이블에 종속된 테그 메타 테이블에 대해서만 동작한다.  
LSL/USL 기능은 특정 TAG ID에 대해 규격 상한과 하한을 가지도록 하는 기능으로써 예상하지 못한 데이터의 입력을 방지하는 기능이다.

## 제약 조건

현재 LSL/USL 설정 기능은 몇 가지 제약 조건이 존재한다. 

* `CLUSTER EDITION` 에서는 LSL/USL 기능을 지원하지 않습니다.
* LSL/USL 를 설정하려면 태그 테이블 생성 시 세 번째 컬럼인 __Value__ 컬럼에 __SUMMARIZED__ 설정이 되어있어야 한다.
* __Value__ 컬럼과 형식(Type)이 같아야 하며 __SUMMARIZED__ 속성처럼 숫자형 타입만을 받을 수 있다.
* LSL은 USL보다 작거나 같아야 하고 __Value__ 컬럼의 입력 값은 LSL의 이상과 USL의 미만이다. __(LSL <= Value <= USL)__
* LSL/USL 설정 부여 이전에 입력된 데이터는 검증하지 않는다.
* LSL/USL 컬럼을 __NULL__ 로 입력할 경우 입력 데이터를 검증하지 않는다.
* LSL/USL 기능은 하나씩 사용 가능하다. 즉 규격 상한만을 맞춰주고 싶을 때에는 USL만 설정하면 된다.
* USL 기능 하나만을 사용할 경우 USL보다 낮은 데이터에 대해서는 검증하지 않는다.

## LSL/USL 기능 설정 및 활용

LSL/USL 기능을 사용하려면 태그 메타 테이블의 컬럼에 특정 키워드를 설정해야 한다.  

* LSL은 `LOWER LIMIT` 키워드를 사용한다.
* USL은 `UPPER LIMIT` 키워드를 사용한다.

태그 테이블을 생성할 때, 메타 컬럼을 추가할 때 설정이 가능하며 아래는 그 예시다.

### CRAETE

```sql
CREATE TAG TABLE example (
    tad_id  VARCHAR(50) PRIMARY KEY,
    time    DATETIME    BASETIME,
    value   INTEGER     SUMMARIZED)
METADATA (
    lsl     INTEGER LOWER LIMIT,  -- LSL 설정
    usl     INTEGER UPPER LIMIT   -- USL 설정
);
```

두 개의 컬럼 같이 사용할 수도 있지만 원한다면 LSL/USL 둘 중 하나만을 사용할 수도 있다.  
LSL 하나만을 설정할 경우 LSL보다 높은 데이터에 대해서는 검증하지 않는다. 즉 `USL == NULL` 과 같다.

```sql
CREATE TAG TABLE example (
    tad_id VARCHAR(50) PRIMARY KEY,
    time   DATETIME    BASETIME,
    value  INTEGER     SUMMARIZED)
METADATA (
    lsl    INTEGER LOWER LIMIT         -- LSL 하나만 설정
);
```

### ADD COLUMN

태그 데이터가 이미 입력된 상태로 `ADD COLUMN` 을 이용하여 추가할 경우 기본 값은 __NULL__ 값이다.  
필요하다면 `DEFAULT` 속성으로 기본 값을 설정할 수 있다. 하지만 이전에 입력된 데이터에 대해서는 검증하지 않는다.

```sql
CREATE TAG TABLE example (
    tad_id  VARCHAR(50) PRIMARY KEY,
    time    DATETIME    BASETIME,
    value   INTEGER     SUMMARIZED
);
 
ALTER TABLE _example_meta ADD COLUMN (lsl INTEGER LOWER LIMIT)              -- LSL 설정
ALTER TABLE _example_meta ADD COLUMN (usl INTEGER DEFAULT 200 UPPER LIMIT)  -- USL 설정 및 기본값 부여
```

[CREATE](#craete)와 같이 하나의 속성만을 추가해줄 수도 있다.

```sql
CREATE TAG TABLE example (
    tad_id  VARCHAR(50) PRIMARY KEY,
    time    DATETIME    BASETIME,
    value   INTEGER     SUMMARIZED
);

ALTER TABLE _example_meta ADD COLUMN (usl INTEGER DEFAULT 200 UPPER LIMIT)  -- USL 하나만 설정
```

### INSERT

LSL/USL 기능을 설정하고 특정 TAG ID에 대해 LSL/USL을 설정하면 데이터 입력 준비가 완료된다.

```sql
INSERT INTO example metadata VALUES ('TAG_01', 100, 200);
```

이렇게 설정한 뒤 태그 데이터를 입력하면 아래와 같이 동작하게 된다.

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

값을 입력한 뒤 태그 테이블을 조회해보면 확실하게 검증된 데이터만 입력된 것을 확인할 수 있다.

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

태그 메타 테이블에 설정된 LSL/USL 컬럼의 값을 수정할 수 있다.
이미 태그 데이터 테이블에 입력된 데이터에 대해서는 검증하지 않기 때문에 주의해서 사용한다.

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

태그 메타 테이블에는 `DROP COLUMN` 기능을 지원하지 않기 때문에 LSL/USL 컬럼만을 직접적으로 삭제할 수 있는 방법은 없다.  
컬럼을 삭제하는 것은 불가능하지만 LSL/USL 의 제약 조건을 역이용하여 LSL/USL 컬럼 값을 __NULL__ 로 설정한다면 제약 없이 데이터 입력이 가능하다.

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
