---
type: docs
title: 'RDB 테이블'
weight: 50
---

RDB 테이블은 Lookup 테이블의 단일 primary-key 모델을 넘어 `INSERT`, `UPDATE`,
`DELETE`, 인덱스 기반 `SELECT`가 필요한 워크로드를 위한 Machbase DBMS의 범용
디스크 row 테이블입니다.

## 개요

RDB 테이블은 대량 `TAG` 또는 `LOG` 데이터 옆에서 범용 디스크 테이블이 필요할 때
사용합니다. 장비 마스터, 알람 룰, 현재 알람 상태, 작업 큐, 조인에 사용하는 차원
테이블이 대표적인 예입니다. 데이터가 영구 참조 데이터이고 모든 row 접근이 하나의
primary key를 중심으로 동작한다면 Lookup 테이블을 사용합니다.

RDB 테이블은 `CREATE RDB TABLE`로 명시적으로 생성합니다. 기존 `CREATE TABLE` 구문은 계속 `LOG` 테이블을 생성합니다.

## 주요 기능

- **범용 디스크 row 저장소**
- **전체 DML 지원**: `INSERT`, `UPDATE`, `DELETE`, `SELECT`
- **선택적 primary key**: 생성 시 선언하거나 `CREATE PRIMARY KEY INDEX`로 나중에 추가
- **일반, unique, JSON path 인덱스**
- **`TAG`, `LOG`, `VOLATILE`, `LOOKUP`, `VIEW`와 조인**
- **backup, restore, mounted database read 지원**
- **machloader 및 SDK prepared statement, append API 지원**

## 기본 구문

```sql
CREATE RDB TABLE device_master (
    id         INTEGER PRIMARY KEY,
    name       VARCHAR(64) NOT NULL,
    site       VARCHAR(32) DEFAULT 'SEOUL',
    state      VARCHAR(16),
    info       JSON,
    updated_at DATETIME
);

INSERT INTO device_master(id, name, state, info, updated_at)
VALUES (1, 'pump-01', 'READY', '{"owner":"ops"}', NOW);

UPDATE device_master
   SET state = 'RUNNING',
       info = JSON_SET(info, '$.status', 'normal')
 WHERE id = 1;

SELECT id, name, state
  FROM device_master
 WHERE id = 1;

DELETE FROM device_master
 WHERE id = 1;
```

## 인덱스

조회 조건에는 일반 인덱스를 사용하고, unique 제약에는 unique 인덱스를 사용합니다. primary key가 필요한 테이블에는 primary key 인덱스를 사용합니다.

```sql
CREATE INDEX idx_device_site ON device_master(site);
CREATE UNIQUE INDEX uidx_device_name ON device_master(name);
CREATE PRIMARY KEY INDEX pk_device_id ON device_master(id);
CREATE INDEX idx_device_owner ON device_master(info->'$.owner');
```

`CREATE PRIMARY KEY INDEX`는 primary key가 없는 RDB 테이블에만 사용할 수 있습니다. 대상 컬럼의 기존 row에 `NULL` 또는 중복 값이 있으면 실패하고 테이블은 변경되지 않습니다. Primary key 인덱스는 삭제할 수 없습니다.

RDB index scan은 안전한 equality 및 range predicate를 최적화합니다. pushdown할 수 없는 predicate도 Machbase query processor가 다시 평가하므로 쿼리 결과는 유지됩니다.

## DML과 트랜잭션

RDB 테이블은 다음 DML을 지원합니다.

- `INSERT`, `INSERT ... SELECT`
- `UPDATE ... SET ... WHERE ...`
- `UPDATE ... SET ...` without `WHERE`: 모든 row 갱신
- `DELETE FROM ... WHERE ...`
- `DELETE FROM table_name` without `WHERE`: 모든 row 삭제
- `TRUNCATE TABLE table_name`

plain `BEGIN`, `COMMIT`, `ROLLBACK`을 RDB DML과 함께 사용할 수 있습니다. 활성 RDB transaction이 있으면 같은 테이블의 `ALTER TABLE`, `CREATE INDEX`, `DROP TABLE` 같은 충돌 가능한 RDB DDL은 transaction 종료 전까지 차단됩니다.

## 지원 데이터 타입

RDB 테이블은 SQL 및 machloader 경로에서 다음 데이터 타입을 지원합니다.

| 분류 | 타입 |
| --- | --- |
| 정수 | `SHORT`, `USHORT`, `INTEGER`, `UINTEGER`, `LONG`, `ULONG` |
| 실수 | `FLOAT`, `DOUBLE` |
| 텍스트 | `VARCHAR`, `TEXT`, `CLOB` |
| 바이너리 | `BINARY`, `BLOB` |
| 날짜/시간 | `DATETIME` |
| 네트워크 | `IPV4`, `IPV6` |
| JSON | `JSON` |

`NUMERIC`, `DECIMAL`은 RDB 테이블에서 지원하지 않습니다.

## RDB 테이블 변경

RDB 테이블은 테이블 이름 변경, 컬럼 이름 변경, 컬럼 추가, 컬럼 삭제를 지원합니다.

```sql
ALTER TABLE device_master RENAME TO device_registry;
ALTER TABLE device_registry RENAME COLUMN state TO run_state;
ALTER TABLE device_registry ADD COLUMN score INTEGER DEFAULT 0;
ALTER TABLE device_registry DROP COLUMN (score);
```

삭제 대상 컬럼이 primary key, unique index, normal index, JSON path index에 사용 중이면 RDB `ALTER TABLE DROP COLUMN`은 실패합니다.

## Backup, Restore, Mount

RDB 테이블 데이터는 RDB sidecar 파일에 저장됩니다. Database backup과 table backup은 Machbase catalog metadata와 함께 RDB sidecar snapshot을 포함합니다.

- `RESTORE DATABASE`는 catalog restore 뒤 RDB sidecar를 복원합니다.
- `machadmin -r`도 RDB sidecar를 복원합니다.
- `MOUNT DATABASE`는 RDB sidecar를 read-only로 열고 mounted RDB 테이블과 view를 조회할 수 있습니다.
- mounted RDB 객체 대상 DML, DDL, backup, schema write는 거부됩니다.
- RDB 테이블에 대한 `MOUNT TABLE`은 지원하지 않습니다.

## machloader 및 SDK 지원

`machloader`는 RDB 테이블 import/export, schema export, replace mode, CSV header matching, invalid input row의 bad file 기록을 지원합니다.

Client SDK는 RDB 테이블에 prepared 또는 parameterized execution을 사용할 수 있습니다. SQLCLI, JDBC, Python, Node.js, .NET 경로는 RDB regression suite에서 검증됩니다. JDBC와 Node.js는 append batch 경로를 지원하고, SQLCLI/Python/.NET은 append stream 경로를 지원합니다.

## 제한사항

- RDB 테이블은 standard edition에서 지원합니다. Cluster edition은 RDB DDL, DML, SELECT, VIEW, INDEX 작업을 거부합니다.
- backend native SQL passthrough는 제공하지 않습니다.
- table-level constraint, composite primary key, foreign key, trigger, generated column, partial index, arbitrary expression index, collation option은 지원하지 않습니다.
- `CREATE TABLE`은 계속 `LOG` 테이블을 생성합니다. RDB 테이블은 `CREATE RDB TABLE`을 사용합니다.

## 관련 문서

- [테이블 타입 개요](../../core-concepts/table-types-overview/)
- [SQL 레퍼런스](../../sql-reference/)
- [도구 레퍼런스](../../tools-reference/)
