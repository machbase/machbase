---
title: '9.4 데이터 입력과 변경'
weight: 40
toc: true
---
LOOKUP 테이블의 데이터 입력, 갱신, 삭제 방법을 다룬다.


<a id="original-85-inserting-data"></a>

## Lookup 데이터 입력

LOOKUP 테이블은 `INSERT`, `UPDATE`, `DELETE`로 기준 데이터를 관리한다. 기준 코드, 장비 마스터, 임계값처럼 운영 중 변경되는 참조 데이터를 저장하므로, 변경 전 영향 범위를 확인하는 절차를 함께 둔다.

<a id="insert-lookup-basic"></a>

## INSERT

LOOKUP 테이블은 `PRIMARY KEY`가 필수이므로 입력 시 키 값을 함께 넣는다.

```sql
CREATE LOOKUP TABLE sensor_master (
    sensor_id VARCHAR(64) PRIMARY KEY,
    site      VARCHAR(32),
    unit      VARCHAR(16),
    status    VARCHAR(16),
    updated_at DATETIME
);

INSERT INTO sensor_master
VALUES ('TEMP-01', 'SEOUL', 'Celsius', 'ACTIVE', NOW);
```

SEQUENCE 컬럼을 사용하는 경우에는 `NEXTVAL()`로 키 값을 생성한다.

```sql
CREATE LOOKUP TABLE alarm_history (
    seq        LONG PROPERTY(SEQUENCE=1) PRIMARY KEY,
    sensor_id  VARCHAR(64),
    alarm_type VARCHAR(32),
    occurred_at DATETIME
);

INSERT INTO alarm_history
VALUES (NEXTVAL(seq), 'TEMP-01', 'HIGH', NOW);
```

<a id="update-lookup-basic"></a>

## UPDATE

단건 변경은 PRIMARY KEY 조건으로 처리한다.

```sql
UPDATE sensor_master
SET status = 'INACTIVE',
    updated_at = NOW
WHERE sensor_id = 'TEMP-01';
```

LOOKUP 테이블은 일반 조건식 기반 UPDATE도 사용할 수 있다. 조건에 맞는 모든 행이 변경되므로, 실행 전에 같은 조건으로 대상 건수를 확인한다.

```sql
SELECT COUNT(*)
FROM sensor_master
WHERE site = 'SEOUL'
  AND status = 'READY';

UPDATE sensor_master
SET status = 'ACTIVE',
    updated_at = NOW
WHERE site = 'SEOUL'
  AND status = 'READY';
```

PRIMARY KEY 컬럼 자체는 변경하지 않는 것이 원칙이다. 키를 바꿔야 하면 기존 행을 삭제하고 새 키로 다시 입력한다.

<a id="upsert-lookup"></a>

## 중복 키 처리

SQL INSERT에서 키 중복 시 갱신이 필요하면 `ON DUPLICATE KEY UPDATE`를 사용한다.

```sql
INSERT INTO sensor_master
VALUES ('TEMP-01', 'SEOUL', 'Celsius', 'ACTIVE', NOW)
ON DUPLICATE KEY UPDATE SET status = 'ACTIVE', updated_at = NOW;
```

Append로 데이터를 삽입할 때 primary key가 중복되면 `LOOKUP_APPEND_UPDATE_ON_DUPKEY` 설정에 따라 해당 행을 업데이트할 수 있다. 이 설정은 LOOKUP 테이블 append 경로의 중복 키 처리 정책이므로, 운영 환경에서는 현재 설정값을 확인한 뒤 사용한다.

```sql
SELECT name, value
FROM v$property
WHERE name = 'LOOKUP_APPEND_UPDATE_ON_DUPKEY';
```

<a id="refresh-lookup-table"></a>

## TABLE_REFRESH

Lookup 노드에서 데이터를 리로드하려면 EXEC TABLE_REFRESH 명령을 사용한다.

```sql
EXEC TABLE_REFRESH(lktable);
```

대량 입력이나 외부 도구를 통한 반영 후 조회 노드의 참조 데이터를 갱신해야 하는 상황에서 사용한다. 운영 중에는 새 데이터가 반영되는 시점과 애플리케이션 조회 시점을 맞춘다.

<a id="original-85-deleting-data"></a>

## Lookup 데이터 삭제

단건 삭제는 PRIMARY KEY 조건을 사용한다.

```sql
DELETE FROM sensor_master
WHERE sensor_id = 'TEMP-01';
```

LOOKUP 테이블은 일반 조건식 기반 DELETE도 사용할 수 있다. 일괄 삭제 전에는 대상 건수를 먼저 확인한다.

```sql
SELECT COUNT(*)
FROM sensor_master
WHERE status = 'RETIRED';

DELETE FROM sensor_master
WHERE status = 'RETIRED';
```

<a id="mutation-lookup-checklist"></a>

## 변경 작업 체크리스트

- 단건 변경은 PRIMARY KEY 조건을 사용한다.
- 일괄 UPDATE/DELETE 전에는 `SELECT COUNT(*)`로 대상 범위를 확인한다.
- PRIMARY KEY 값 변경은 DELETE 후 INSERT로 처리한다.
- Append 중복 키 처리는 `LOOKUP_APPEND_UPDATE_ON_DUPKEY` 설정을 확인한다.
- 대량 변경 후 필요하면 `EXEC TABLE_REFRESH(table_name)`으로 참조 데이터를 갱신한다.
