---
title: '6.4 ROLLUP 생성과 삭제'
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
-- 기본 1초 롤업
CREATE ROLLUP _tag_ru_1s ON tag(value) INTERVAL 1 SEC;

-- 1초 롤업을 소스로 1분 롤업 생성
CREATE ROLLUP _tag_ru_1m FROM _tag_ru_1s INTERVAL 1 MIN;

-- 1분을 소스로 1시간 롤업
CREATE ROLLUP _tag_ru_1h FROM _tag_ru_1m INTERVAL 1 HOUR;

-- 30초 단위 롤업
CREATE ROLLUP _tag_ru_30s ON tag(value) INTERVAL 30 SEC;

-- EXTENSION 롤업 (FIRST/LAST 지원)
CREATE ROLLUP _tag_ru_1s_ext ON tag(value) INTERVAL 1 SEC EXTENSION;

-- 조건 롤업 (value >= 0 인 데이터만 집계)
CREATE ROLLUP _tag_ru_valid ON tag(value) INTERVAL 1 MIN WHERE value >= 0;
```

#### TAG 테이블 생성 시 자동 생성 (WITH ROLLUP)

```sql
-- SEC 이상 전체 계층(SEC/MIN/HOUR) 자동 생성
CREATE TAG TABLE tag (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) WITH ROLLUP (SEC);
```

자동 생성 롤업 이름: `_TAG_ROLLUP_SEC`, `_TAG_ROLLUP_MIN`, `_TAG_ROLLUP_HOUR`

> 롤업 이름이 이미 존재하면 TAG 테이블은 생성되지만 WITH ROLLUP 처리는 실패합니다.

#### 제약사항

- 집계 대상 컬럼은 숫자형(DOUBLE, INTEGER 등)이어야 합니다.
- FROM으로 참조하는 상위 롤업의 주기는 소스 롤업 주기의 정수배여야 합니다.
- ROLLUP은 시간축(BASETIME) TAG 테이블에서만 동작합니다. 거리축 TAG 테이블은 지원하지 않습니다.
- JSON SUMMARIZED 컬럼은 별도 JSON ROLLUP 구문을 사용합니다.

### DROP ROLLUP

```sql
DROP ROLLUP rollup_name;
```

#### 삭제 규칙

다른 롤업이 해당 롤업을 소스로 참조하는 경우 삭제할 수 없습니다. 의존 순서의 역순으로 삭제해야 합니다.

```sql
-- 잘못된 순서 (오류 발생)
DROP ROLLUP _tag_ru_1s;  -- ERR-02651: Dependent ROLLUP table exists.

-- 올바른 순서
DROP ROLLUP _tag_ru_1h;
DROP ROLLUP _tag_ru_1m;
DROP ROLLUP _tag_ru_1s;
```

#### TAG 테이블 삭제 시 일괄 삭제

```sql
-- CASCADE: TAG 테이블과 종속 ROLLUP을 모두 삭제
DROP TABLE tag CASCADE;
```
