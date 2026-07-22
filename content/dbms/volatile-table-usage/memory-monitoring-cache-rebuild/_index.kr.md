---
title: '10.15 메모리 모니터링과 캐시 재구성'
weight: 150
toc: true
---

VOLATILE 테이블의 메모리 모니터링과 캐시 재구성 방법을 다룹니다. VOLATILE 테이블은 메모리에 저장되므로 행 수, 인덱스 수, 전체 메모리 한도를 운영 중에 확인해야 합니다.

<a id="monitor-volatile-row-count"></a>

## 행 수 확인

가장 먼저 테이블별 행 수를 확인합니다.

```sql
SELECT COUNT(*) FROM sensor_latest;
SELECT COUNT(*) FROM sensor_1min_summary;
```

행 수가 예상보다 빠르게 증가하면 보관 범위나 삭제 조건을 점검합니다.

```sql
-- 단건 삭제는 PRIMARY KEY 조건으로 수행
DELETE FROM sensor_1min_summary
WHERE summary_key = 'TEMP-01:202601011200';
```

시간 범위 기준으로 많은 행을 정리해야 하면 원본 영속 테이블에서 다시 만들 수 있는 범위만 남기도록 캐시를 재구성합니다.

<a id="monitor-volatile-memory-view"></a>

## 메모리 사용량 확인

VOLATILE 테이블의 메모리 상태는 시스템 뷰에서 확인합니다.

```sql
SELECT *
FROM V$STORAGE_DC_VOLATILE_TABLE;
```

서버 전체 메모리 상태도 함께 확인합니다.

```sql
SELECT *
FROM V$SYSMEM;
```

세션 단위 메모리가 의심되는 경우에는 세션 메모리 뷰를 확인합니다.

```sql
SELECT *
FROM V$SESMEM;
```

<a id="monitor-volatile-limit"></a>

## 메모리 한도 확인

Volatile/Lookup 테이블 전체 메모리 한도는 `VOLATILE_TABLESPACE_MEMORY_MAX_SIZE` 설정의 영향을 받습니다.

```sql
SELECT NAME, VALUE
FROM V$PROPERTY
WHERE NAME = 'VOLATILE_TABLESPACE_MEMORY_MAX_SIZE';
```

설정 변경이 필요한 경우에는 운영 환경의 전체 메모리, LOOKUP 테이블 사용량, 동시 쿼리 메모리를 함께 고려합니다.

<a id="rebuild-volatile-cache"></a>

## 캐시 재구성 절차

VOLATILE 캐시는 원본 영속 테이블에서 다시 만들 수 있어야 합니다. 기본 절차는 다음과 같습니다.

1. 현재 캐시 테이블의 행 수와 사용량을 확인합니다.
2. 필요한 경우 캐시 내용을 삭제합니다.
3. 원본 TAG, LOG, TRANSACTION 테이블에서 초기 데이터를 다시 적재합니다.
4. 재구성 후 행 수와 최신 시각을 확인합니다.

```sql
DROP TABLE sensor_latest;

CREATE VOLATILE TABLE sensor_latest (
    sensor_id  VARCHAR(64) PRIMARY KEY,
    value      DOUBLE,
    updated_at DATETIME
);

INSERT INTO sensor_latest
SELECT name, value, time
FROM sensor_data
WHERE time >= NOW - 60000000000;

SELECT COUNT(*) FROM sensor_latest;
```

캐시 구조 자체를 변경해야 하는 경우도 같은 방식으로 테이블을 삭제하고 다시 생성합니다.

```sql
DROP TABLE sensor_latest;

CREATE VOLATILE TABLE sensor_latest (
    sensor_id  VARCHAR(64) PRIMARY KEY,
    value      DOUBLE,
    updated_at DATETIME
);
```

<a id="rebuild-volatile-startup"></a>

## 서버 시작 시 재구성

서버 재시작 후 VOLATILE 테이블은 비어 있으므로, 시작 스크립트에 생성과 초기 적재 절차를 포함합니다.

```bash
machsql -u SYS -p MANAGER -f /etc/machbase/volatile_startup.sql
```

```sql
CREATE VOLATILE TABLE sensor_latest (
    sensor_id  VARCHAR(64) PRIMARY KEY,
    value      DOUBLE,
    updated_at DATETIME
);

INSERT INTO sensor_latest
SELECT name, value, time
FROM sensor_data
WHERE time >= NOW - 60000000000;
```

<a id="monitor-volatile-checklist"></a>

## 운영 체크리스트

- 테이블별 `COUNT(*)`를 주기적으로 확인합니다.
- `V$STORAGE_DC_VOLATILE_TABLE`로 VOLATILE 테이블 메모리 상태를 확인합니다.
- `VOLATILE_TABLESPACE_MEMORY_MAX_SIZE` 설정을 운영 메모리 정책과 맞춥니다.
- 캐시 재구성 SQL은 원본 영속 테이블 기준으로 작성합니다.
- 재시작 후 자동 생성·초기 적재가 실행되는지 점검합니다.
