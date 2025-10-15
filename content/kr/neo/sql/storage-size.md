---
title: 자동 저장소 관리
type: docs
weight: 51
---

## 소개

초당 수백만 건의 센서 데이터를 수집하는 시계열 데이터베이스는 저장 용량 관리가 가장 큰 과제입니다. 주기적으로 디스크 사용량을 점검하고 오래된 데이터를 수동으로 삭제하는 방식은 번거롭고 오류 가능성이 높습니다. 또한 많은 시스템은 특정 기간까지만 데이터를 보관하고 이후에는 자동으로 삭제되기를 원합니다.

Machbase는 **Retention Policy** 기능을 통해 일정 기간 이상 지난 데이터를 자동으로 삭제해 저장 공간을 안정적으로 유지할 수 있는 메커니즘을 제공합니다. 정책을 선언적으로 정의하기만 하면 백그라운드에서 주기적으로 데이터를 정리합니다.

## 핵심 개념: Retention Policy

Retention Policy는 두 가지 요소로 구성됩니다.

- **DURATION**: 데이터를 보관할 기간입니다. 현재 시스템 시각에서 DURATION을 뺀 시점보다 오래된 데이터는 삭제 대상이 됩니다. 단위는 `MONTH` 또는 `DAY`입니다.
- **INTERVAL**: 정책을 실행할 주기입니다. 지정한 간격마다 Machbase가 테이블을 검사하여 삭제를 수행합니다. 단위는 `DAY` 또는 `HOUR`입니다.

정책을 적용하면 Machbase가 주기적으로(`INTERVAL`) 테이블을 스캔하여 `BASETIME` 컬럼 기준으로 DURATION을 초과한 행을 자동으로 삭제합니다.

사용 흐름은 다음과 같습니다.
1. `CREATE RETENTION`으로 정책을 생성합니다.
2. `ALTER TABLE ... ADD RETENTION`으로 테이블에 정책을 적용합니다.
3. Machbase가 정책에 따라 주기적으로 데이터를 삭제합니다.
4. 필요 시 `ALTER TABLE ... DROP RETENTION`으로 정책 적용을 해제합니다.
5. 정책이 더 이상 필요 없으면 `DROP RETENTION`으로 삭제합니다.

## Retention Policy 생성

```sql
CREATE RETENTION policy_name
    DURATION duration_value { MONTH | DAY }
    INTERVAL interval_value { DAY | HOUR };
```

- `policy_name`: 정책 이름
- `duration_value`: 보관 기간(정수)
- `interval_value`: 검사 주기(정수)

예시:

```sql
CREATE RETENTION policy_1d_1h
    DURATION 1 DAY
    INTERVAL 1 HOUR;

CREATE RETENTION policy_1m_3d
    DURATION 1 MONTH
    INTERVAL 3 DAY;
```

## 테이블에 정책 적용

```sql
ALTER TABLE table_name ADD RETENTION policy_name;
```

```sql
CREATE TAG TABLE sensor_data (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

ALTER TABLE sensor_data ADD RETENTION policy_1d_1h;
```

테이블에는 한 번에 하나의 Retention Policy만 적용할 수 있습니다.

## 정책 모니터링

- `M$RETENTION`: 등록된 정책 목록과 설정(DURATION/INTERVAL)을 확인합니다.

  ```sql
  SELECT * FROM M$RETENTION;
  ```

- `V$RETENTION_JOB`: 어떤 테이블에 어떤 정책이 적용되어 있는지, 마지막 삭제 시각은 언제인지 확인합니다.

  ```sql
  SELECT * FROM V$RETENTION_JOB;
  ```

## 정책 해제 및 삭제

### 테이블에서 해제

```sql
ALTER TABLE table_name DROP RETENTION;
```

### 정책 객체 삭제

```sql
DROP RETENTION policy_name;
```

정책이 테이블에 적용 중이면 삭제할 수 없습니다. 먼저 해당 테이블에서 정책을 해제해야 합니다.

```sql
-- 적용 중이면 오류 발생
DROP RETENTION policy_1d_1h;

-- 정책 해제 후 삭제
ALTER TABLE sensor_data DROP RETENTION;
DROP RETENTION policy_1d_1h;
```

## 사용 예제

### 1. 테이블 및 정책 설정

```sql
DROP TABLE IF EXISTS ret_tag CASCADE;

CREATE TAG TABLE ret_tag (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) WITH ROLLUP(MIN) TAG_PARTITION_COUNT=1;

CREATE RETENTION policy_1d_1h
    DURATION 1 DAY
    INTERVAL 1 HOUR;

ALTER TABLE ret_tag ADD RETENTION policy_1d_1h;
```

### 2. 데이터 적재(예: 최근 2일간 데이터)

```tql
FAKE(range(1, 150000, 1))
MAPVALUE(1, sin((2*PI*value(0)/100)))
MAPVALUE(0, timeAdd("now-2d", strSprintf("+%.fs", value(0)*100)))
PUSHVALUE(0, "sensor-a")
APPEND(table("ret_tag"))
```

```sql
SELECT COUNT(*) FROM ret_tag; -- 약 150,000건
```

### 3. 정책 실행 및 결과 확인

1시간 이상 경과하면 백그라운드 작업이 실행되어 1일보다 오래된 데이터가 삭제됩니다.

```sql
SELECT * FROM V$RETENTION_JOB WHERE TABLE_NAME = 'RET_TAG';
SELECT COUNT(*) FROM ret_tag; -- 초기보다 적은 건수
```

### 4. 정책 해제 및 제거

```sql
ALTER TABLE ret_tag DROP RETENTION;
DROP RETENTION policy_1d_1h;
```

자동 저장소 관리를 활용하면 일정 기간만 데이터를 유지하고 오래된 데이터는 자동으로 정리할 수 있어 운영 부담과 오류 가능성을 크게 줄일 수 있습니다.
