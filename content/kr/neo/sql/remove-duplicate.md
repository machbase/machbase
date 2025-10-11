---
title: 중복 데이터 제거
type: docs
weight: 31
---

## 소개

분산 환경에서 센서 데이터를 수집·전송할 때 네트워크 불안정이나 장비 설정에 따라 동일한 데이터가 재전송되는 일이 잦습니다. 데이터 손실을 막기 위한 의도이지만 결과적으로 데이터베이스에는 중복 레코드가 쌓이게 됩니다. 애플리케이션 측에서 중복을 식별·제거하려면 많은 리소스와 복잡한 로직이 필요합니다.

Machbase는 TAG 테이블에 대해 데이터베이스 수준에서 중복 전송을 자동으로 제거하는 기능을 제공합니다. 특정 시간 창 윈도우를 지정하면 동일한 태그 ID·시간 조합의 데이터가 해당 윈도우 내에 다시 들어올 때 자동으로 걸러져 데이터 일관성을 유지할 수 있습니다.

## 핵심 개념

중복 제거 기능은 TAG 테이블 생성 시 설정한 “조회 기간”을 기준으로 동작합니다. 데이터가 삽입될 때 Machbase는 다음을 확인합니다.

1. **식별**: 입력 행의 `PRIMARY KEY`(보통 Tag ID)와 `BASETIME`(타임스탬프)를 기존 행과 비교합니다.
2. **탐색**: 동일한 `PRIMARY KEY`, `BASETIME` 값을 가진 행이 이미 존재하는지 확인합니다.
3. **시간 조건**: 동일한 행이 존재하고 그 `BASETIME`이 설정한 조회 기간 안(현재 시스템 시각 기준 과거 방향)에 포함되면 중복으로 판단합니다.
4. **처리**: 중복으로 판정된 행은 자동으로 폐기되어 TAG 테이블에 저장되지 않습니다.

즉, 지정한 시간 창 안에서는 최초 입력된 데이터만 유지되고 동일 키·시간 조합의 이후 입력은 모두 무시됩니다. 비교 대상은 기본키와 `BASETIME`만이며 다른 컬럼 값이 달라도 시간·키가 같으면 중복으로 처리됩니다.

## 설정 방법

TAG 테이블 생성 시 테이블 속성으로 `TAG_DUPLICATE_CHECK_DURATION`을 지정합니다.

```sql
CREATE TAG TABLE table_name (
    name_column datatype PRIMARY KEY,
    time_column DATETIME BASETIME,
    value_column datatype [SUMMARIZED],
    ...
)
TAG_DUPLICATE_CHECK_DURATION = duration_in_minutes;
```

- 값은 분(minute) 단위 정수이며 최소 1, 최대 43200(30일)입니다.
- 기본값은 `0`이며 이때는 기능이 비활성화됩니다.

### 설정 확인

```sql
-- 1) 테이블 ID 조회 (테이블명은 대문자로)
SELECT id
FROM m$sys_tables
WHERE name = 'YOUR_TABLE_NAME';

-- 2) 속성값 조회
SELECT value
FROM m$sys_table_property
WHERE id = {위에서 조회한 ID}
  AND name = 'TAG_DUPLICATE_CHECK_DURATION';
```

### 설정 변경

```sql
ALTER TABLE {table_name}
SET TAG_DUPLICATE_CHECK_DURATION = {분 단위 값};
```

## 동작 및 제약 사항

- **단위**: 분 단위로만 지정할 수 있으며 최대 30일(43200분)까지 가능합니다.
- **데이터 삭제와의 관계**: 최초 삽입된 데이터를 삭제하면 이후 도착한 동일 데이터는 새 데이터로 인정되어 저장됩니다.
- **동작 방식**: “첫 번째 데이터가 승리(first-write-wins)” 방식입니다. 가장 먼저 들어온 행이 유지되고 이후 중복은 모두 무시됩니다.
- **일관성 모델**: 대량 실시간 적재 환경에서는 내부 구조에 반영되기까지 약간의 지연이 발생할 수 있습니다.
- **타깃 기반 중복 제거**: 데이터베이스 내부에서 중복을 걸러내며, 소스 시스템에서 중복 전송을 막는 것은 아닙니다.
- **리소스 사용**: 데이터베이스에서 검증을 수행하므로 애플리케이션에서 걸러내는 것보다 CPU/I/O가 추가로 소요될 수 있습니다.

## 예시

### 1. 테이블 생성

```sql
DROP TABLE IF EXISTS dup_tag;

CREATE TAG TABLE dup_tag (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
)
TAG_DUPLICATE_CHECK_DURATION = 1440; -- 1일(1440분) 동안 중복 체크
```

### 2. 데이터 삽입 테스트

```sql
-- 최초 입력
INSERT INTO dup_tag VALUES('tag1', '2024-01-01 09:00:00 000:000:001', 0);
INSERT INTO dup_tag VALUES('tag1', '2024-01-02 09:00:00 000:000:001', 0);
INSERT INTO dup_tag VALUES('tag1', '2024-01-02 09:00:00 000:000:002', 0);

-- 동일한 name, time → 중복으로 거부
INSERT INTO dup_tag VALUES('tag1', '2024-01-02 09:00:00 000:000:002', 1);

-- 다른 시간 → 허용
INSERT INTO dup_tag VALUES('tag1', '2024-01-03 09:00:00 000:000:003', 0);

-- tag2에 대한 중복 테스트
INSERT INTO dup_tag VALUES('tag2', '2024-01-04 09:00:00 000:000:001', 0);
INSERT INTO dup_tag VALUES('tag2', '2024-01-04 09:00:00 000:000:001', 1); -- 거부
INSERT INTO dup_tag VALUES('tag2', '2024-01-04 09:00:00 000:000:001', 2); -- 거부

INSERT INTO dup_tag VALUES('tag2', '2024-01-04 09:00:00 000:000:002', 1); -- 허용
INSERT INTO dup_tag VALUES('tag2', '2024-01-04 09:00:00 000:000:003', 2); -- 허용
```

### 3. 결과 확인

```sql
SELECT * FROM dup_tag WHERE name = 'tag1';

SELECT * FROM dup_tag WHERE name = 'tag2';
```

각 태그별로 최초 입력된 시간·키 조합만 남아 있는 것을 확인할 수 있습니다. 이후 동일 조합으로 들어온 데이터는 설정한 시간 창 내에서는 자동으로 방지됩니다.
