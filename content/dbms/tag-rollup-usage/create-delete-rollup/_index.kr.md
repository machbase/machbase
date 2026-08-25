---
title: '6.3 ROLLUP 생성과 삭제'
weight: 30
toc: true
---


<a id="create-delete-rollup"></a>

## ROLLUP 생성과 삭제

### CREATE ROLLUP

#### 기본 구문

```text
CREATE ROLLUP [IF NOT EXISTS] rollup_name
  ON source_table(column_name)
  INTERVAL n (SEC|MIN|HOUR)
  [WAKEUP INTERVAL m (SEC|MIN|HOUR)]
  [EXTENSION]
  [WHERE predicate];
```

상위 롤업(롤업을 소스로 쓰는 경우):

```text
CREATE ROLLUP [IF NOT EXISTS] rollup_name
  FROM source_rollup_table
  INTERVAL n (SEC|MIN|HOUR)
  [WAKEUP INTERVAL m (SEC|MIN|HOUR)]
  [EXTENSION]
  [WHERE predicate];
```

#### 생성 예시

```sql
CREATE TAG TABLE create_rollup_demo (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

CREATE ROLLUP create_ru_1s
    ON create_rollup_demo(value) INTERVAL 1 SEC;

CREATE ROLLUP create_ru_1m
    FROM create_ru_1s INTERVAL 1 MIN;

CREATE ROLLUP create_ru_1h
    FROM create_ru_1m INTERVAL 1 HOUR;
```

조건, 확장, 사용자 정의 ROLLUP은 각각의 상세 문서에서 실행 가능한 예제를 제공합니다.

#### TAG 테이블 생성 시 자동 생성 (WITH ROLLUP)

```sql
-- SEC 이상 전체 계층(SEC/MIN/HOUR) 자동 생성
CREATE TAG TABLE tag (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) WITH ROLLUP (SEC);
```

자동 생성된 이름은 원본 테이블 이름에서 파생됩니다. 이름을 추측하지 말고 `V$ROLLUP`에서
확인하십시오. 같은 이름의 객체가 있으면 `WITH ROLLUP` 처리가 실패할 수 있습니다.

#### 제약사항

- 집계 대상 컬럼은 숫자형(DOUBLE, INTEGER 등)이어야 합니다.
- FROM으로 참조하는 상위 롤업의 주기는 소스 롤업 주기의 정수배여야 합니다.
- ROLLUP은 시간축(BASETIME) TAG 테이블에서만 동작합니다. 거리축 TAG 테이블은 지원하지 않습니다.
- JSON SUMMARIZED 컬럼은 별도 JSON ROLLUP 구문을 사용합니다.

### DROP ROLLUP

```text
DROP ROLLUP rollup_name;
```

#### 삭제 규칙

다른 롤업이 해당 롤업을 소스로 참조하는 경우 삭제할 수 없습니다. 의존 순서의 역순으로 삭제해야 합니다.

```sql
DROP ROLLUP create_ru_1h;
DROP ROLLUP create_ru_1m;
DROP ROLLUP create_ru_1s;
DROP TABLE create_rollup_demo;
```

#### TAG 테이블 삭제 시 일괄 삭제

원본 TAG와 종속 ROLLUP을 함께 삭제해야 한다면 `DROP TABLE table_name CASCADE`를 사용합니다.
