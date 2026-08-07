---
type: docs
title: '14.2 다중 데이터베이스'
weight: 20
toc: true
---

<span class="badge-since">Machbase 8.6.0부터 지원되는 기능</span>

## 1. 이 기능으로 할 수 있는 일

다중 데이터베이스 기능을 사용하면 **하나의 Machbase Standard 인스턴스 안에
여러 개의 논리 데이터베이스**를 만들 수 있습니다.

예를 들어 공장별로 다음과 같이 데이터를 나눌 수 있습니다.

```text
MACHBASEDB
FACTORY_A
FACTORY_B
```

`FACTORY_A`와 `FACTORY_B`에는 이름이 같은 테이블을 각각 만들 수 있습니다.
각 데이터베이스의 테이블과 권한은 서로 구분됩니다.

> 이 기능은 논리적인 이름 공간과 권한을 분리합니다. 별도 서버, CPU, 메모리,
> 디스크를 제공하는 물리적 격리 기능은 아닙니다.

### 적용 범위

- 이 매뉴얼은 **Standard edition**을 기준으로 합니다.
- Cluster edition에서는 이 기능을 지원하지 않습니다.
- 데이터베이스별 CPU, 메모리, 디스크 quota는 제공하지 않습니다.
- 기존 기본 데이터베이스인 `MACHBASEDB`와 기존 SQL은 그대로 사용할 수
  있습니다.

### 격리되는 것과 공유되는 것

다중 데이터베이스는 하나의 서버 안에서 catalog를 분리하는 기능입니다.

| 영역 | 동작 |
| --- | --- |
| 테이블, view, index, rollup 이름 | 데이터베이스별로 분리됩니다. |
| 테이블 데이터와 객체 권한 | database identity를 기준으로 분리됩니다. |
| Catalog-local 객체 metadata | 사용자의 database 및 table 권한에 따라 표시됩니다. |
| 사용자와 인증 정보 | 인스턴스 전체에서 공유됩니다. 사용자를 DB마다 만들지 않습니다. |
| Instance-global `M$`/`V$` 정보 | 인스턴스 범위이며 catalog-local 객체 정보와 범위가 다를 수 있습니다. |
| CPU, 메모리, 디스크, server process | 모든 데이터베이스가 공유합니다. |

따라서 이 기능을 별도 서버와 같은 보안·자원 격리 수단으로 사용하면 안 됩니다.
물리적 격리가 필요하면 인스턴스를 분리합니다.

## 2. 먼저 알아둘 네 가지

### 2.1 기본 데이터베이스는 `MACHBASEDB`입니다

연결할 때 데이터베이스를 지정하지 않으면 `MACHBASEDB`를 사용합니다.

현재 데이터베이스는 다음 SQL로 확인합니다.

```sql
SELECT CURRENT_DATABASE();
```

### 2.2 현재 데이터베이스는 연결마다 다릅니다

`USE`로 현재 데이터베이스를 변경합니다.

```sql
USE factory_a;
SELECT CURRENT_DATABASE();
```

다른 사용자의 연결에는 영향을 주지 않습니다.

### 2.3 객체 이름은 최대 세 부분입니다

테이블 계열 객체를 참조할 때는 최대 세 부분 이름을 사용합니다.

| 형식 | 의미 |
| --- | --- |
| `sensor_log` | 현재 데이터베이스의 현재 사용자 테이블 |
| `sys.sensor_log` | 현재 데이터베이스의 `SYS` 사용자 테이블 |
| `factory_a.sys.sensor_log` | `FACTORY_A` 데이터베이스의 `SYS` 사용자 테이블 |

두 부분 이름은 항상 `사용자.테이블`입니다.

```sql
SELECT * FROM factory_a.sensor_log;
```

위 SQL의 `FACTORY_A`는 데이터베이스가 아니라 사용자 이름으로 해석됩니다.
데이터베이스를 직접 지정하려면 세 부분을 모두 씁니다.

```sql
SELECT * FROM factory_a.sys.sensor_log;
```

존재하지 않는 database, owner 또는 table을 다른 database에서 다시 찾는 fallback은
하지 않습니다. 잘못된 qualifier를 지정하면 명시적으로 실패합니다.

> 세 부분 이름은 모든 종류의 객체 이름에 공통으로 적용되는 문법이 아닙니다.
> Table/view 대상과 DML에는 세 부분 이름을 사용할 수 있지만 index 이름과
> `LOAD DATA` 등은 별도 제한이 있습니다. 자세한 내용은 4.4절을 참고합니다.

### 2.4 Active database와 mounted database

| 구분 | Active database | Mounted database |
| --- | --- | --- |
| 생성 | `CREATE DATABASE` 또는 `RESTORE DATABASE` | `MOUNT DATABASE` |
| `USE` | `CONNECT` 권한이 있으면 가능 | 불가 |
| 읽기 | 가능 | `USAGE`와 table `SELECT`가 모두 필요 |
| 쓰기 | READ WRITE 상태에서 가능 | 항상 불가 |
| Access mode | READ WRITE 또는 READ ONLY | 항상 READ ONLY |
| 제거 | `DROP DATABASE` | `UMOUNT DATABASE` |

Mounted database는 backup image를 조회하기 위한 별도 namespace입니다. Active
database로 자동 변환되거나 current database가 되지 않습니다.

## 3. 5분 빠른 시작

이 예제는 두 데이터베이스를 만들고 같은 이름의 TAG 테이블을 각각 생성합니다.

### 3.1 관리자가 데이터베이스와 사용자를 만듭니다

다음 내용을 `create_factory_databases.sql` 파일에 작성합니다.

```sql
CREATE DATABASE factory_a;
CREATE DATABASE factory_b;

CREATE USER app_a IDENTIFIED BY 'AppA#1234';
CREATE USER app_b IDENTIFIED BY 'AppB#1234';

GRANT CONNECT ON DATABASE factory_a TO app_a;
GRANT CONNECT ON DATABASE factory_b TO app_b;

USE factory_a;

CREATE TAG TABLE sys.sensor_log (
    name VARCHAR(80) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

USE factory_b;

CREATE TAG TABLE sys.sensor_log (
    name VARCHAR(80) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

GRANT SELECT, INSERT ON TABLE factory_a.sys.sensor_log TO app_a;
GRANT SELECT, INSERT ON TABLE factory_b.sys.sensor_log TO app_b;

USE MACHBASEDB;
SHOW DATABASES;
```

`SYS` 사용자로 실행합니다.

```bash
machsql -s 127.0.0.1 -u sys -p manager \
    -f create_factory_databases.sql
```

`SHOW DATABASES` 결과에서 `MACHBASEDB`, `FACTORY_A`, `FACTORY_B`를
확인합니다.

### 3.2 애플리케이션 사용자가 데이터를 입력합니다

다음 내용을 `insert_factory_a.sql` 파일에 작성합니다.

```sql
SELECT CURRENT_DATABASE();

INSERT INTO sys.sensor_log
VALUES (
    'pump-1',
    TO_DATE('2026-07-30 10:00:00', 'YYYY-MM-DD HH24:MI:SS'),
    12.5
);

SELECT name, time, value
FROM sys.sensor_log
WHERE name = 'pump-1';
```

`-D` 옵션으로 처음 사용할 데이터베이스를 지정합니다.

```bash
machsql -s 127.0.0.1 -u app_a -p 'AppA#1234' \
    -D factory_a -f insert_factory_a.sql
```

첫 번째 조회 결과가 `FACTORY_A`이면 정상입니다.

### 3.3 두 데이터베이스가 분리되었는지 확인합니다

`APP_A`는 `FACTORY_B` 권한이 없으므로 다음 SQL은 실패해야 정상입니다.

```sql
SELECT COUNT(*)
FROM factory_b.sys.sensor_log;
```

다른 데이터베이스의 테이블을 읽으려면 대상 데이터베이스의 `CONNECT`와
대상 테이블의 `SELECT`가 모두 필요합니다.

## 4. 데이터베이스 선택과 조회

### 4.1 현재 데이터베이스 확인

다음 표현은 같은 데이터베이스 이름을 반환합니다.

```sql
SELECT CURRENT_DATABASE();
SELECT DATABASE();
SELECT CURRENT_CATALOG;
SHOW CURRENT DATABASE;
```

권장 표현은 `CURRENT_DATABASE()`입니다.

### 4.2 현재 데이터베이스 변경

```sql
USE factory_a;
```

다음 호환 문법도 사용할 수 있습니다.

```sql
USE DATABASE factory_a;
```

다음 경우에는 `USE`가 실패하며 기존 데이터베이스가 유지됩니다.

- 데이터베이스가 존재하지 않는 경우
- 사용자에게 `CONNECT` 권한이 없는 경우
- mounted database를 선택한 경우
- transaction이 진행 중인 경우

transaction을 `COMMIT` 또는 `ROLLBACK`한 뒤 다시 실행합니다.

### 4.3 다른 데이터베이스를 직접 조회

현재 데이터베이스를 바꾸지 않고 세 부분 이름으로 다른 데이터베이스를
조회할 수 있습니다.

```sql
USE factory_a;

SELECT COUNT(*)
FROM factory_b.sys.sensor_log;

SELECT CURRENT_DATABASE();
```

마지막 결과는 계속 `FACTORY_A`입니다.

### 4.4 명시적 객체 이름과 statement 대상

다음 작업은 세 부분 table/view 이름으로 다른 active database를 직접 지정할 수
있습니다. 실행 후 session의 current database는 바뀌지 않습니다.

| 작업 | 명시적 database 지정 |
| --- | --- |
| `SELECT`, `INSERT`, `DELETE`, 지원되는 `UPDATE` | `[database.]owner.table` |
| `CREATE`, `ALTER`, `DROP TABLE`, `TRUNCATE TABLE` | `[database.]owner.table` |
| `CREATE`, `DROP VIEW` | `[database.]owner.view` |
| `CREATE INDEX` | 대상 table에 database를 지정하고 index 이름은 1/2-part로 지정 |
| 다른 database의 `DROP INDEX` | 해당 database로 `USE`한 뒤 실행 |
| `LOAD DATA ... INTO TABLE` | 1-part target이며 current database 사용 |

명시적 target을 가진 statement의 무수식 source는 target database를 기준으로
해석될 수 있습니다. 실수와 권한 혼동을 피하려면 cross-database 복합 SQL에서는
target과 source를 모두 세 부분 이름으로 지정합니다.

```sql
INSERT INTO factory_a.app_a.sensor_copy
SELECT name, time, value
FROM factory_a.app_a.sensor_source;
```

다른 database에 view를 생성할 때도 view 내부의 무수식 source는 view target
database에 속합니다.

```sql
USE factory_b;

CREATE VIEW factory_a.app_a.sensor_view AS
SELECT * FROM app_a.sensor_source;
```

위 view의 `APP_A.SENSOR_SOURCE`는 `FACTORY_A`에서 해석됩니다. 다른 active
database를 참조하는 view는 lifecycle과 logical restore를 복잡하게 만들므로,
저장 view는 같은 database의 객체만 참조하도록 구성합니다.

### 4.5 Transaction과 current database

Transaction이 진행 중이면 `USE`는 실패하고 기존 current database와 미커밋
데이터는 유지됩니다. `COMMIT` 또는 `ROLLBACK`한 뒤 database를 변경합니다.

TRANSACTION table은 세 부분 이름을 사용해 하나의 transaction에서 여러
database의 table을 변경할 수 있습니다. `COMMIT`과 `ROLLBACK`은 그 transaction의
모든 변경에 함께 적용됩니다.

```sql
BEGIN;

UPDATE factory_a.app_a.device_state
SET value = 10
WHERE id = 1;

UPDATE factory_b.app_b.device_state
SET value = 20
WHERE id = 1;

COMMIT;
```

활성 transaction에서는 SELECT, transaction 제어문과 TRANSACTION table DML만
사용합니다. 일반 table DDL이나 비transaction table 쓰기는 transaction을 종료한
뒤 실행합니다.

## 5. 데이터베이스와 객체 찾기

자주 사용하는 조회 명령은 다음과 같습니다.

```sql
SHOW DATABASES;
SHOW CURRENT DATABASE;
SHOW TABLES;
SHOW TABLES FROM factory_a;
SHOW TABLES FROM factory_a LIKE 'SENSOR%';
SHOW VIEWS FROM factory_a;
SHOW OWNERS FROM factory_a;
SHOW USERS;
DESC factory_a.sys.sensor_log;
```

`SHOW`와 `DESC`는 machsql이 metadata query로 변환하는 client 명령입니다.
JDBC, ODBC, Python 등에서 server-side SQL 또는 prepared statement로 실행하지
말고 해당 client의 metadata API나 `M$`/`V$` view를 사용합니다.

- `SHOW OWNERS FROM database`는 그 database에 객체를 소유한 owner를 표시합니다.
- `SHOW USERS`는 인스턴스 전체 사용자를 표시합니다.
- `SHOW TABLES`와 `SHOW VIEWS`는 current 또는 명시한 database 범위입니다.

일반 사용자의 `SHOW DATABASES`에는 자신이 사용할 수 있는 데이터베이스만
표시됩니다.

- active database: `CONNECT` 권한이 필요합니다.
- mounted database: `USAGE` 권한이 필요합니다.
- 권한을 회수한 기존 session의 즉시 표시 여부에 의존하지 말고, 권한 변경 후
  새 연결에서 접근 가능 범위를 다시 확인합니다.

`SHOW USERS`는 인스턴스 전체의 사용자를 표시합니다. 사용자는 데이터베이스마다
별도로 생성하지 않습니다. 권한 row는 `SYS`가 다음과 같이 확인합니다.

```sql
SELECT database_id, db_name, user_name, owner_name, table_name, priv
FROM M$SYS_USER_ACCESS
WHERE user_name = 'APP_A'
ORDER BY database_id, owner_name, table_name;
```

## 6. 사용자와 권한

사용자는 database별 계정이 아니라 인스턴스 전역 principal입니다. 같은 사용자가
여러 active/mounted database에 서로 다른 권한을 가질 수 있습니다.

`CREATE USER`는 기존 Machbase 호환 동작에 따라 `MACHBASEDB`에
`SELECT`, `INSERT`, `DELETE`, `UPDATE`, `CREATE`, `DROP`, `CONNECT` 기본 비트를
등록합니다. 이 중 DML 비트는 다른 owner의 모든 table에 대한 권한이 아니며,
실제 table 접근은 table identity에 부여한 권한을 별도로 검사합니다. 새 논리
database에는 기본 권한이 자동으로 복제되지 않습니다. 최소 권한 계정은 생성
직후 실제 권한을 확인하고 불필요한 권한을 회수합니다.

```sql
SELECT database_id, db_name, user_name, owner_name, table_name, priv
FROM M$SYS_USER_ACCESS
WHERE user_name = 'APP_A';

-- 객체 생성과 삭제가 불필요한 계정의 예
REVOKE DDL ON DATABASE MACHBASEDB FROM app_a;
```

기존 버전에서 업그레이드한 사용자도 `MACHBASEDB` 접근 호환을 위해 `CONNECT`를
가집니다.

### 6.1 권한 종류

| 권한 | 대상 | 용도 |
| --- | --- | --- |
| `CONNECT` | active database | 연결, `USE`, 데이터베이스 탐색 |
| `CREATE` | active database | 비SYS 사용자의 자기 owner 객체 생성 |
| `DROP` | active database | 비SYS 사용자의 자기 owner 객체 삭제 |
| `ALTER` | active database | 비SYS 사용자의 자기 owner 객체 변경 |
| `BACKUP` | active database | 해당 데이터베이스 백업 |
| `MOUNT` | `MACHBASEDB` | backup image mount와 umount |
| `USAGE` | mounted database | mounted database 탐색 |
| `SELECT` | table | 조회 |
| `INSERT` | table | 입력 |
| `DELETE` | table | 삭제 |
| `UPDATE` | table | VOLATILE, LOOKUP 또는 TRANSACTION 테이블 수정 |

`DROP ON DATABASE`는 데이터베이스 안의 객체를 삭제하는 권한입니다.
`DROP DATABASE` 권한이 아닙니다.

다음 작업은 `SYS`만 할 수 있습니다.

- `CREATE USER`, `DROP USER`
- 모든 `GRANT`, `REVOKE`
- `CREATE DATABASE`
- `DROP DATABASE`
- `ALTER DATABASE ... READ ONLY|READ WRITE`
- `RESTORE DATABASE`

`BACKUP DATABASE`와 `MOUNT`/`UMOUNT`는 각각 `BACKUP`, `MOUNT` 권한으로
일반 사용자에게 위임할 수 있습니다.

### 6.2 권한 부여

```sql
GRANT CONNECT ON DATABASE factory_a TO report_user;
GRANT SELECT ON TABLE factory_a.sys.sensor_log TO report_user;
```

다른 데이터베이스의 테이블을 사용할 때는 다음 두 권한이 모두 필요합니다.

1. 대상 데이터베이스의 `CONNECT`
2. 대상 테이블의 `SELECT`, `INSERT`, `DELETE`, `UPDATE` 중 필요한 권한

데이터베이스 전체에 `SELECT`를 부여하는 문법은 지원하지 않습니다. 테이블마다
부여합니다.

### 6.3 권한 회수

```sql
REVOKE SELECT ON TABLE factory_a.sys.sensor_log FROM report_user;
REVOKE CONNECT ON DATABASE factory_a FROM report_user;
```

### 6.4 GRANT/REVOKE 기본 문법

다중 데이터베이스 권한은 **데이터베이스 권한**과 **테이블 권한**을
구분합니다. `GRANT`와 `REVOKE`는 `SYS`만 실행할 수 있습니다.

| 대상 | 부여 문법 | 회수 문법 |
| --- | --- | --- |
| 데이터베이스 | `GRANT 권한 ON DATABASE db TO user;` | `REVOKE 권한 ON DATABASE db FROM user;` |
| 테이블 | `GRANT 권한 ON TABLE [db.]owner.table TO user;` | `REVOKE 권한 ON TABLE [db.]owner.table FROM user;` |

쉼표로 여러 권한을 한 번에 지정할 수 있습니다.

```sql
GRANT CONNECT, CREATE, ALTER ON DATABASE factory_a TO app_a;
REVOKE CREATE, ALTER ON DATABASE factory_a FROM app_a;

GRANT SELECT, INSERT, DELETE ON TABLE factory_a.sys.sensor_log TO app_a;
REVOKE INSERT, DELETE ON TABLE factory_a.sys.sensor_log FROM app_a;
```

한 문장은 한 사용자에게만 적용합니다. `PUBLIC`, role, `WITH GRANT OPTION`을
사용한 재위임은 지원하지 않습니다.

### 6.5 데이터베이스 권한 전체 조합

| 권한 | Active database | `MACHBASEDB` | Mounted database | 허용하는 작업 | 주의사항 |
| --- | --- | --- | --- | --- | --- |
| `CONNECT` | 가능 | 가능 | 불가 | 연결, `USE`, 객체 탐색 | 테이블 DML 권한을 포함하지 않습니다. |
| `CREATE` | 가능 | 가능 | 불가 | 비SYS 사용자의 자기 owner 객체 생성 | `CONNECT`도 필요합니다. |
| `DROP` | 가능 | 가능 | 불가 | 비SYS 사용자의 자기 owner 객체 삭제 | `DROP DATABASE` 권한이 아닙니다. `CONNECT`도 필요합니다. |
| `ALTER` | 가능 | 가능 | 불가 | 비SYS 사용자의 자기 owner 객체 변경 | `ALTER DATABASE ... READ ONLY/READ WRITE` 권한이 아닙니다. `CONNECT`도 필요합니다. |
| `BACKUP` | 가능 | 가능 | 불가 | `BACKUP DATABASE` | 대상 database의 `CONNECT` 없이도 backup할 수 있습니다. |
| `DDL` | 가능 | 가능 | 불가 | `CREATE, DROP` | `ALTER`는 포함하지 않습니다. |
| `MOUNT` | 불가 | 가능 | 불가 | backup image의 `MOUNT`, `UMOUNT` | 반드시 `ON DATABASE MACHBASEDB`로 부여합니다. mounted 데이터 조회 권한은 포함하지 않습니다. |
| `USAGE` | 불가 | 불가 | 가능 | mounted database 탐색 | 실제 조회에는 테이블 `SELECT`도 필요합니다. |
| `ALL` | 가능 | 가능 | 불가 | `CONNECT, CREATE, DROP, ALTER, BACKUP` | 테이블 DML과 `MOUNT`를 포함하지 않습니다. |

`GRANT`와 `REVOKE`는 위 표에서 가능한 조합에 동일한 scope 규칙을
적용합니다. 예를 들어 active database에는 `CONNECT`를 부여하고 회수할 수
있지만 `USAGE`를 부여하거나 회수할 수 없습니다.

```sql
GRANT ALL ON DATABASE factory_a TO app_a;
REVOKE ALL ON DATABASE factory_a FROM app_a;

GRANT MOUNT ON DATABASE MACHBASEDB TO backup_operator;
REVOKE MOUNT ON DATABASE MACHBASEDB FROM backup_operator;

GRANT USAGE ON DATABASE factory_a_backup TO report_user;
REVOKE USAGE ON DATABASE factory_a_backup FROM report_user;
```

> `ALL ON DATABASE`는 database 안의 모든 테이블을 읽고 쓰게 하는 권한이
> 아닙니다. 필요한 각 테이블에 `SELECT`, `INSERT`, `DELETE`, `UPDATE`를
> 별도로 부여합니다.

### 6.6 Active database의 테이블 권한 전체 조합

| 객체 종류 | `SELECT` | `INSERT` | `DELETE` | `UPDATE` | `ALL ON TABLE` |
| --- | --- | --- | --- | --- | --- |
| LOG table | 가능 | 가능 | 가능 | 불가 | `SELECT, INSERT, DELETE` |
| TAG table | 가능 | 가능 | 가능 | 권한을 부여해도 SQL 기능상 불가 | 실제 지원 DML은 `SELECT, INSERT, DELETE`입니다. |
| VOLATILE table | 가능 | 가능 | 가능 | 가능 | 네 DML 권한 전체 |
| LOOKUP table | 가능 | 가능 | 가능 | 가능 | 네 DML 권한 전체 |
| TRANSACTION table | 가능 | 가능 | 가능 | 가능 | 네 DML 권한 전체 |
| View | 가능 | 불가 | 불가 | 불가 | `GRANT ALL`은 거부되므로 `SELECT`를 명시합니다. |

LOG table에 `GRANT UPDATE`만 지정하면 오류가 됩니다. 다른 권한과 `UPDATE`를
함께 `GRANT`하면 지원되는 권한만 남고 `UPDATE`는 제거됩니다. 반면 `UPDATE`를
명시한 LOG table `REVOKE`는 다른 권한과 함께 지정해도 오류가 되므로,
지원되는 권한만 회수해야 합니다. LOG와 TAG table 자체가 `UPDATE` SQL을
지원하지 않으므로 `UPDATE` 권한으로 이 제한을 해제할 수 없습니다.

LOG의 `ALL ON TABLE`은 `SELECT`, `INSERT`, `DELETE`로 저장됩니다. TAG는
`ALL` 권한 비트에 `UPDATE`가 포함될 수 있지만 TAG table 자체가 일반 UPDATE를
지원하지 않으므로 UPDATE SQL은 계속 실패합니다. 권한 비트와 table 종류의 SQL
기능을 같은 의미로 해석하면 안 됩니다. 권한 하나를 `REVOKE`해도 나머지 권한은
유지됩니다.

Active view에는 `GRANT ALL ON TABLE`을 사용할 수 없지만, 기존 `SELECT` 권한을
정리할 때 `REVOKE ALL ON TABLE`은 사용할 수 있습니다. 새 권한은 `GRANT SELECT`로
명시하는 방식을 권장합니다.

```sql
GRANT ALL ON TABLE factory_a.sys.device_lookup TO app_a;
REVOKE UPDATE ON TABLE factory_a.sys.device_lookup FROM app_a;

GRANT SELECT ON TABLE factory_a.sys.sensor_view TO report_user;
REVOKE SELECT ON TABLE factory_a.sys.sensor_view FROM report_user;
```

### 6.7 Mounted database의 테이블 권한 조합

Mounted database의 테이블과 view에는 `SELECT`만 부여하거나 회수할 수
있습니다. `INSERT`, `DELETE`, `UPDATE`, `ALL ON TABLE`은 허용되지 않습니다.

| `USAGE` | 테이블 `SELECT` | Metadata 탐색 | 테이블 조회 |
| --- | --- | --- | --- |
| 없음 | 없음 | 불가 | 불가 |
| 있음 | 없음 | database는 보이나 대상 테이블 사용 불가 | 불가 |
| 없음 | 있음 | database 사용 불가 | 불가 |
| 있음 | 있음 | 가능 | 가능 |

```sql
GRANT USAGE ON DATABASE factory_a_backup TO report_user;
GRANT SELECT ON TABLE factory_a_backup.sys.sensor_log TO report_user;

REVOKE SELECT ON TABLE factory_a_backup.sys.sensor_log FROM report_user;
REVOKE USAGE ON DATABASE factory_a_backup FROM report_user;
```

`MOUNT` 권한은 위 두 권한을 대신하지 않습니다. 즉 backup을 mount한 사용자도
데이터를 읽으려면 해당 mounted database의 `USAGE`와 대상 테이블의 `SELECT`를
별도로 받아야 합니다.

### 6.8 Active database 접근 조합

다른 사용자가 소유한 테이블을 사용하려면 database 권한과 table 권한이 모두
필요합니다.

| Database `CONNECT` | 필요한 table 권한 | 결과 |
| --- | --- | --- |
| 없음 | 없음 | 접근 불가 |
| 있음 | 없음 | database 연결/탐색은 가능하지만 해당 DML은 불가 |
| 없음 | 있음 | table 권한이 있어도 database 접근 불가 |
| 있음 | 있음 | 해당 table 권한 범위에서 실행 가능 |

| 실행할 SQL | 함께 필요한 권한 |
| --- | --- |
| `SELECT` | database `CONNECT` + table `SELECT` |
| `INSERT` 또는 Appender | database `CONNECT` + table `INSERT` |
| `DELETE` | database `CONNECT` + table `DELETE` |
| `UPDATE` | database `CONNECT` + table `UPDATE` + UPDATE 지원 테이블 |
| `CREATE TABLE` | database `CONNECT` + database `CREATE` |
| `ALTER TABLE` | database `CONNECT` + database `ALTER` |
| `DROP TABLE` | database `CONNECT` + database `DROP` |
| `BACKUP DATABASE` | database `BACKUP` (`CONNECT`는 필수 아님) |

Database가 `READ ONLY`이면 권한을 모두 가지고 있어도 `INSERT`, `DELETE`,
`UPDATE`, 객체 `CREATE`, `ALTER`, `DROP`과 대상 database/table의 `GRANT`,
`REVOKE`는 실패합니다. 권한을 변경하려면 먼저 READ WRITE로 전환합니다.

### 6.9 허용되지 않는 대표 조합

| 잘못된 조합 | 거부 이유 |
| --- | --- |
| `GRANT SELECT ON DATABASE factory_a ...` | DML 권한은 table scope입니다. |
| `GRANT CONNECT ON TABLE factory_a.sys.t1 ...` | `CONNECT`는 database scope입니다. |
| `GRANT BACKUP ON TABLE factory_a.sys.t1 ...` | `BACKUP`은 database scope입니다. |
| `GRANT USAGE ON DATABASE factory_a ...` | `USAGE`는 mounted database 전용입니다. |
| `GRANT CONNECT ON DATABASE mounted_db ...` | Mounted database에는 `USAGE`를 사용합니다. |
| `GRANT MOUNT ON DATABASE factory_a ...` | `MOUNT` 대상은 `MACHBASEDB`뿐입니다. |
| `GRANT ALL ON DATABASE mounted_db ...` | Mounted database에는 `USAGE`만 부여합니다. |
| `GRANT INSERT ON TABLE mounted_db.sys.t1 ...` | Mounted 객체는 `SELECT`만 허용합니다. |
| `GRANT ALL ON TABLE active_db.sys.view1 ...` | View에는 `SELECT`를 명시해야 합니다. |

잘못된 조합은 전체 문장이 실패하며 기존 권한은 변경되지 않습니다.

### 6.10 기존 GRANT/REVOKE 문법과의 차이

기존 문법은 `TABLE`과 `DATABASE`를 키워드로 구분하지 않고 권한 종류와 대상
이름으로 scope를 판별했습니다. 다중 데이터베이스에서는 대상 종류를 명확하게
표현할 수 있도록 `ON TABLE`과 `ON DATABASE` 문법을 추가했습니다.

| 구분 | 기존 문법 | 다중 데이터베이스 권장 문법 |
| --- | --- | --- |
| 테이블 권한 | `GRANT SELECT ON owner.table TO user` | `GRANT SELECT ON TABLE [db.]owner.table TO user` |
| 테이블 권한 회수 | `REVOKE SELECT ON owner.table FROM user` | `REVOKE SELECT ON TABLE [db.]owner.table FROM user` |
| 데이터베이스 권한 | `GRANT CREATE ON MACHBASEDB TO user` | `GRANT CREATE ON DATABASE db TO user` |
| 데이터베이스 권한 회수 | `REVOKE CREATE ON MACHBASEDB FROM user` | `REVOKE CREATE ON DATABASE db FROM user` |
| Active database 범위 | 기본 database인 `MACHBASEDB` 중심 | 모든 active database를 이름으로 지정 |
| 연결 권한 | 별도 권한 없음 | Active database용 `CONNECT` 추가 |
| Mounted database 접근 | Mounted table의 `SELECT` 중심 | Mounted database `USAGE` + table `SELECT` |
| 대상 판별 | 권한과 이름으로 table/database를 추론 | `TABLE`/`DATABASE` 키워드로 명시 |

기존 테이블 문법은 하위 호환성을 위해 계속 사용할 수 있습니다.

```sql
GRANT SELECT ON DB_A.SYS.T1 TO APP_USER;
REVOKE SELECT ON DB_A.SYS.T1 FROM APP_USER;
```

새 SQL은 다음처럼 대상 종류를 명시하는 방식을 권장합니다.

```sql
GRANT SELECT ON TABLE DB_A.SYS.T1 TO APP_USER;
REVOKE SELECT ON TABLE DB_A.SYS.T1 FROM APP_USER;

GRANT CONNECT, CREATE ON DATABASE DB_A TO APP_USER;
REVOKE CREATE ON DATABASE DB_A FROM APP_USER;
```

#### 기존 `ALL ON MACHBASEDB`와의 차이

다음 두 문장은 같은 문법이 아닙니다.

```sql
-- 기존 호환 문법
GRANT ALL ON MACHBASEDB TO APP_USER;

-- 다중 데이터베이스 명시 문법
GRANT ALL ON DATABASE MACHBASEDB TO APP_USER;
```

기존 호환 문법은 과거 `MACHBASEDB`의 복합 권한 의미를 유지합니다. 명시적인
`ALL ON DATABASE`는 대상 database의 다음 권한으로 정규화됩니다.

```text
CONNECT, CREATE, DROP, ALTER, BACKUP
```

따라서 `ALL ON DATABASE`에는 table `SELECT`, `INSERT`, `DELETE`, `UPDATE`와
database `MOUNT`가 포함되지 않습니다. 새로 작성하는 SQL에서는 `ON DATABASE`와
`ON TABLE`을 명시하고 필요한 권한을 각각 부여합니다.

```sql
GRANT ALL ON DATABASE DB_A TO APP_USER;
GRANT SELECT, INSERT ON TABLE DB_A.SYS.T1 TO APP_USER;

GRANT MOUNT ON DATABASE MACHBASEDB TO BACKUP_OPERATOR;
```

### 6.11 권한의 수명과 정리

권한은 이름 문자열이 아니라 database, user, table의 실제 identity에 연결됩니다.

| 작업 | 기존 권한 처리 |
| --- | --- |
| Table drop 후 동명 table 재생성 | 기존 table grant는 삭제되며 부활하지 않습니다. |
| Database drop 후 동명 database 재생성 | 기존 database/table grant는 승계되지 않습니다. |
| User drop 후 동명 user 재생성 | 과거 user의 grant는 승계되지 않습니다. |
| UMOUNT 후 같은 alias로 remount | alias의 `USAGE`와 table grant를 다시 부여해야 합니다. |
| Backup image mount | 원본 active database의 grant는 승계되지 않습니다. |
| RESTORE 또는 REPLACE | image와 기존 target의 grant를 사용하지 않으며 완료 후 다시 부여합니다. |
| 정상 server restart | 현재 grant와 revoke 상태가 유지됩니다. |

`DROP USER`는 해당 사용자가 소유한 객체가 어느 database에든 남아 있으면
실패합니다. 소유 객체를 먼저 정리한 뒤 user를 삭제합니다.

## 7. 데이터베이스 운영

Database lifecycle 명령은 `SYS`가 실행합니다.

```sql
CREATE DATABASE [IF NOT EXISTS] database_name;
ALTER DATABASE database_name READ ONLY;
ALTER DATABASE database_name READ WRITE;
DROP DATABASE [IF EXISTS] database_name
    [RESTRICT | CASCADE | FORCE | CASCADE FORCE | FORCE CASCADE];
```

### 7.1 생성

```sql
CREATE DATABASE tenant1;
CREATE DATABASE IF NOT EXISTS tenant1;
SHOW CREATE DATABASE tenant1;
```

다음 이름은 사용할 수 없습니다.

- `MACHBASEDB`: 기본 데이터베이스 예약 이름
- `DATA`: 기존 client 호환을 위한 예약 이름
- `__REPLACED_`로 시작하는 이름: REPLACE 내부 lifecycle 예약 영역
- 이미 존재하는 active 또는 mounted database 이름

Database 이름은 대소문자를 구분하지 않고 canonical 대문자로 표시됩니다.
이식성이 필요한 운영 SQL에서는 영문자, 숫자, `_`, `$`, `#`로 구성한 일반
identifier를 사용합니다. Quoted 또는 Unicode 이름의 세부 경계에 의존하지
않습니다.

`IF NOT EXISTS`는 동일 이름의 정상 active database가 이미 있는 경우만 작업을
생략합니다. Mounted alias, 비정상 lifecycle 상태 또는 예약 이름 충돌은 오류입니다.

데이터베이스를 삭제한 뒤 같은 이름으로 다시 만들어도 내부 identity는
재사용되지 않습니다.

### 7.2 읽기 전용으로 전환

```sql
ALTER DATABASE tenant1 READ ONLY;
```

READ ONLY 상태에서는 조회, metadata 확인, backup을 할 수 있습니다.
다음 쓰기 작업은 실패합니다.

- `INSERT`, `DELETE`, `UPDATE`
- append와 bulk 입력
- table, view, index, rollup 등의 생성·변경·삭제
- 대상 database와 table의 `GRANT`, `REVOKE`
- `TABLE_REFRESH`, rollup control, TAG index freeze/unfreeze와 같은 쓰기성 관리 작업

쓰기 작업이 진행 중이면 READ ONLY 전환은 기다리지 않고 실패합니다. 쓰기
transaction, append, DDL 작업을 종료한 뒤 다시 실행합니다.

다시 쓰기를 허용하려면 다음 SQL을 실행합니다.

```sql
ALTER DATABASE tenant1 READ WRITE;
```

Prepared SELECT는 READ ONLY에서도 실행할 수 있습니다. Prepared write는 execute
시점에 거부되며, 같은 handle은 READ WRITE 복귀 후 다시 실행할 수 있습니다.

### 7.3 안전하게 삭제

> `CASCADE`는 객체를 영구 삭제하고 `FORCE`는 사용 중인 연결과 작업을
> 중단합니다. 실행 전에 대상 이름과 backup을 확인합니다.

삭제 명령을 실행하는 연결이 대상 데이터베이스를 사용 중이면 삭제할 수
없습니다. 먼저 다른 데이터베이스로 이동합니다.

```sql
USE MACHBASEDB;
```

기본값과 명시적 `RESTRICT`는 빈 데이터베이스만 허용합니다.

```sql
DROP DATABASE tenant1;
DROP DATABASE tenant1 RESTRICT;
```

객체가 남아 있으면 `CASCADE`를 사용합니다.

```sql
DROP DATABASE tenant1 CASCADE;
```

연결, statement, cursor, append handle 등이 사용 중이면 `FORCE`가
필요합니다.

```sql
DROP DATABASE tenant1 FORCE;
```

객체와 사용 중인 참조가 모두 있으면 두 옵션을 함께 사용합니다.

```sql
DROP DATABASE tenant1 CASCADE FORCE;
```

| 옵션 | 정리 대상 |
| --- | --- |
| `CASCADE` | table, view, index, rollup, 권한과 관련 metadata |
| `FORCE` | 대상 데이터베이스를 사용하는 연결과 열린 handle |

> 객체와 live reference가 함께 있는 database에 `FORCE`만 실행하지 않습니다.
> FORCE가 연결을 먼저 종료한 뒤 RESTRICT 객체 검사에서 DROP이 실패할 수
> 있습니다. 이 경우 database와 객체는 남지만 대상 연결은 이미 끊어집니다.
> 두 종류가 모두 존재하면 처음부터 `CASCADE FORCE`를 사용합니다.

`IF EXISTS`는 database가 없는 경우만 오류를 생략합니다. 권한, current database,
객체 또는 live reference 오류를 무시하지 않습니다.

`MACHBASEDB`는 삭제할 수 없습니다. 또한 명령을 실행하는 session의 current
database는 `FORCE`를 포함한 어떤 조합으로도 삭제할 수 없습니다.

## 8. Backup, mount, restore

### 8.1 데이터베이스 백업

active database는 READ WRITE 상태에서도 online backup할 수 있습니다.
`SYS` 또는 대상 데이터베이스의 `BACKUP` 권한이 있는 사용자가 실행합니다.

```sql
BACKUP DATABASE factory_a
INTO DISK = '/backup/factory_a_20260730';

BACKUP DATABASE factory_a
FROM TO_DATE('2026-07-01', 'YYYY-MM-DD')
TO TO_DATE('2026-08-01', 'YYYY-MM-DD')
INTO DISK = '/backup/factory_a_202607';
```

시간 범위를 지정하면 `TO`가 `FROM`보다 커야 합니다. 경로에 기존 directory,
file 또는 symbolic link가 있으면 덮어쓰지 않고 실패합니다. Backup 전에 경로와
여유 공간을 확인합니다.

Backup snapshot에는 확정된 committed row만 포함됩니다. Snapshot 당시 미커밋인
TRANSACTION table row와 snapshot 완료 후 추가된 row는 포함되지 않습니다. 동시
commit과 snapshot 확정의 정밀 순서에 의존해야 하는 작업은 application에서 쓰기를
중지한 뒤 backup합니다. Source database는 backup 후에도 독립적으로 사용할 수
있습니다.

### 8.2 Backup을 읽기 전용으로 mount

backup을 복원하지 않고 바로 조회하려면 mount합니다.
`SYS` 또는 `MACHBASEDB`의 `MOUNT` 권한이 있는 사용자가 실행합니다.

```sql
MOUNT DATABASE '/backup/factory_a_20260730'
TO factory_a_backup;
```

일반 사용자에게 mounted database 권한을 부여합니다.

```sql
GRANT USAGE ON DATABASE factory_a_backup TO report_user;
GRANT SELECT ON TABLE factory_a_backup.sys.sensor_log TO report_user;
```

조회할 때는 세 부분 이름을 사용합니다.

```sql
SELECT COUNT(*)
FROM factory_a_backup.sys.sensor_log;
```

mounted database는 항상 다음 상태입니다.

- `KIND=MOUNTED`
- `ACCESS_MODE=READ_ONLY`
- `CAN_USE=0`

따라서 `USE factory_a_backup`과 모든 쓰기 작업은 실패합니다.

열린 statement나 cursor가 mounted table을 사용 중이면 umount가 실패합니다.
관련 handle을 닫고 다시 실행합니다.

```sql
UMOUNT DATABASE factory_a_backup;
```

umount하면 alias에 부여한 `USAGE`와 table 권한이 정리됩니다. 원본 backup
파일은 삭제되지 않습니다.

Mounted object의 owner identity는 backup image의 사용자 metadata를 기준으로
합니다. 현재 인스턴스에 같은 이름의 사용자가 있어도 원 owner로 자동 간주되지
않습니다. 접근 권한은 alias `USAGE`와 mounted table `SELECT`로 별도 부여합니다.

Mount할 수 있는 image에는 active catalog가 정확히 하나 있어야 합니다. 여러
active database를 포함한 full-instance backup, catalog metadata가 없거나 서로
맞지 않는 손상 image는 mount하지 않습니다.

### 8.3 새 데이터베이스로 restore

```sql
RESTORE DATABASE factory_a_restore
FROM DISK = '/backup/factory_a_20260730';
```

복원된 데이터베이스는 새로운 identity를 받습니다. backup 당시의 READ WRITE
또는 READ ONLY 상태를 유지합니다.

backup에 기록된 owner 사용자가 현재 인스턴스에 없으면 restore는 시작 전에
실패합니다. 사용자를 만들거나 owner remap을 사용합니다.

```sql
CREATE USER restored_app IDENTIFIED BY 'Restored#1234';

RESTORE DATABASE factory_a_migrated
FROM DISK = '/backup/factory_a_20260730'
REMAP OWNER app_a TO restored_app;
```

여러 owner를 remap할 수 있으며 모든 절은 `REPLACE`보다 앞에 둡니다.

```sql
RESTORE DATABASE factory_a_migrated
FROM DISK = '/backup/factory_a_20260730'
REMAP OWNER app_a TO restored_app
REMAP OWNER report_a TO restored_report;
```

새 owner는 restore 전에 존재해야 하고 같은 old owner를 두 번 지정할 수 없습니다.
RESTORE는 `SYS`만 실행합니다. 대상 이름이 이미 존재하거나 mounted alias와
충돌하면 신규 restore가 실패합니다.

> Logical backup은 database/table grant를 image에 보존하지 않습니다. Restore가
> 완료되면 새 database의 `CONNECT`와 필요한 table 권한을 다시 부여합니다.

### 8.4 기존 데이터베이스 교체

> `REPLACE`는 기존 데이터베이스의 내용을 backup image로 교체하는 비가역
> 작업입니다. 기존 데이터베이스를 별도로 백업한 뒤 실행합니다.

대상은 READ ONLY이고 사용 중인 연결이나 handle이 없어야 합니다.

```sql
ALTER DATABASE factory_a READ ONLY;

RESTORE DATABASE factory_a
FROM DISK = '/backup/factory_a_20260730'
REPLACE;
```

restore에는 `FORCE`가 없습니다. 사용 중인 연결과 handle은 직접 종료합니다.

성공한 REPLACE는 target의 기존 database/object identity와 권한을 유지하지
않습니다. Image의 schema, data와 access mode가 적용되므로 READ WRITE image로
교체하면 완료 직후 target도 READ WRITE가 됩니다. 교체 후 권한을 다시 부여하고
`CURRENT_DATABASE()`, object count와 data를 확인합니다.

Object, owner, index, view 검증처럼 target 사용 중지 전에 발생한 실패는 기존
target과 image를 변경하지 않습니다. Target 사용 중지가 시작된 뒤 실패하면 기존
target 복구를 시도합니다. 복구나 background worker 재시작에 실패하면 target이
`FAILED_NEEDS_ACTION` 상태가 되고 server restart가 필요할 수 있습니다. 교체 완료
후 이전 database 정리에 실패한 경우에는 새 target이 유지되고 이전 catalog가
`FAILED_NEEDS_ACTION`으로 남을 수 있습니다. 이 상태에서는 lifecycle 명령을 임의로
반복하지 말고 server log와 backup image를 보존한 뒤 기술 지원을 요청합니다.

### 8.5 Restore 제한사항

다음 객체와 정보는 복원됩니다.

- TRANSACTION, LOG, TAG, LOOKUP 테이블과 데이터
- 지원되는 LOG/TAG/RDB secondary index와 단일-column JSON path index
- 같은 database의 객체를 참조하는 view와 dependent view chain
- LOOKUP primary key와 `DEFAULT SYSDATE`
- VOLATILE 테이블 schema

VOLATILE 테이블의 메모리 row는 복원하지 않습니다.

다음 항목이 backup에 있으면 일부만 복원하지 않고 restore 전체가 사전
검증 단계에서 실패합니다.

- TAG 사용자 정의 metadata column
- 기본값이 아닌 TAG table property
- rollup 정의
- retention job 할당
- AUTO_INCREMENT 또는 LOOKUP sequence generator
- keyword, LIKE-normalized, composite JSON path 또는 알 수 없는 index 유형

Source database를 가리키는 view의 세 부분 이름은 restore target 이름으로
재작성됩니다. 다른 active database를 참조하는 view가 image에 있으면 restore
전체가 publish 전에 실패합니다.

Full-instance backup은 `RESTORE DATABASE`의 logical image로 사용할 수 없습니다.

| Image 종류 | MOUNT | RESTORE DATABASE |
| --- | --- | --- |
| 단일 active database logical backup | 가능 | 가능 |
| 여러 active database를 포함한 full-instance backup | 불가 | 불가 |
| `META_MAJOR < 16` legacy single-database image | 호환 검증을 통과하면 가능 | 불가 |
| 손상되거나 catalog metadata가 불일치한 image | 불가 | 불가 |

## 9. Client에서 데이터베이스 선택

| Client | 초기 database | 변경/확인 | 주의사항 |
| --- | --- | --- | --- |
| machsql | `-D`, `--database`, `DATABASE`/`DBNAME` | SQL `USE`, `CURRENT_DATABASE()` | 초기 옵션을 중복 지정하지 않습니다. |
| Native C/ODBC | connection string 또는 pre-connect catalog | catalog attribute와 SQL | Catalog는 database, schema는 owner입니다. |
| JDBC | URL path 또는 `database` property | `getCatalog()`, `setCatalog()`, SQL | URL/property 값이 다르면 실패합니다. |
| Python | `connect(database=...)` | SQL | 별도 catalog getter/setter가 없습니다. |
| Node.js | config 또는 URL의 database | SQL | 별도 catalog getter가 없습니다. |
| Go neo-client | native: `api.WithDatabase()`<br>SQL driver: DSN `database`/`db` 또는 URL path/query | SQL `USE`, `CURRENT_DATABASE()` | 설정된 초기 database가 있는 `database/sql` pool은 `ResetSession()`에서 해당 database로 복원합니다. |
| .NET 4.0 connector | `DATABASE`/`DB_NAME` | SQL | Initial database 선택만 사용합니다. |

### 9.1 machsql

```bash
machsql -s 127.0.0.1 -u app_a -p 'AppA#1234' \
    -D factory_a -f query.sql
```

connection string을 사용할 수도 있습니다.

```bash
machsql -s 127.0.0.1 -u app_a -p 'AppA#1234' \
    -c 'DATABASE=factory_a' -f query.sql
```

`DBNAME`은 `DATABASE`의 호환 이름입니다. 둘을 서로 다른 값으로 지정하면
연결이 실패합니다.

`-D`/`--database`와 `-c DATABASE=...`를 한 명령에 동시에 지정하는 우선순위는
공개 계약으로 사용하지 않습니다. 한 가지 방식만 선택합니다.

### 9.2 Native C와 ODBC

connection string에 `DATABASE`를 지정합니다.

```text
DSN=MACHBASE;UID=APP_A;PWD=AppA#1234;DATABASE=FACTORY_A
```

- `SQLGetConnectAttr(SQL_ATTR_CURRENT_CATALOG)`로 현재 데이터베이스를
  확인합니다.
- `SQLSetConnectAttr(SQL_ATTR_CURRENT_CATALOG, ...)`로 변경합니다.
- 연결하기 전에 disconnected connection handle에
  `SQL_ATTR_CURRENT_CATALOG`를 설정하면 initial database로 사용합니다.
- `SQLGetInfo(SQL_DATABASE_NAME)`도 현재 database 이름을 반환합니다.
- ODBC catalog는 Machbase database를 의미합니다.
- ODBC schema는 Machbase owner를 의미합니다.

`SQLTables`, `SQLColumns`, table/column privilege, primary key와 index metadata
API의 catalog 인자는 database를 선택합니다. NULL catalog는 current database,
명시적 catalog는 해당 database를 조회하며 호출 자체가 current database를
변경하지 않습니다. 접근 권한이 없는 catalog의 객체 metadata는 표시되지 않습니다.

Native appender는 open 시점 database에 고정됩니다. 다른 database를 직접 지정할
때는 세 부분 table 이름과 대상 database `CONNECT`, table `INSERT` 권한이 모두
필요합니다.

### 9.3 JDBC

URL path에 데이터베이스를 지정합니다.

```java
String url = "jdbc:machbase://127.0.0.1:5656/factory_a";
Connection conn = DriverManager.getConnection(url, "APP_A", password);

System.out.println(conn.getCatalog());
conn.setCatalog("FACTORY_A");
```

`setCatalog()`는 서버에서 `USE`와 같은 권한 검사를 수행합니다. 다른
데이터베이스로 변경하려면 해당 데이터베이스의 `CONNECT` 권한이 필요합니다.

URL path와 `database` property를 모두 지정하면 canonical 값이 같아야 하며,
다르면 연결이 실패합니다. JDBC metadata에서 catalog는 database, schema는 owner를
뜻합니다. `getCatalogs()`, `getSchemas()`, table/column/privilege/primary-key/index
metadata는 이 매핑을 사용합니다.

내장 `MachPooledConnection`은 logical connection을 반환할 때 열린 statement를
정리하고 URL의 initial catalog로 복원합니다. 복원에 실패한 physical connection은
재사용하지 않습니다. 외부 pool을 사용할 때도 반환 시 catalog reset을 보장하는지
확인합니다.

`MachStatement.executeAppendOpen/Data/Close`는 append-open 시점의 target
database에 고정됩니다. 다른 database의 table에는 세 부분 이름을 사용하고
`CONNECT`와 table `INSERT` 권한을 함께 부여합니다.

### 9.4 Python

```python
from machbaseAPI import connect

conn = connect(
    host="127.0.0.1",
    port=5656,
    user="APP_A",
    password="AppA#1234",
    database="FACTORY_A",
)

cur = conn.cursor()
cur.execute("SELECT CURRENT_DATABASE()")
print(cur.fetchall())

cur.close()
conn.close()
```

Python connector에는 별도 current-catalog getter/setter가 없습니다. SQL
`CURRENT_DATABASE()`와 `USE`를 사용합니다. Server prepared cursor가 필요하면
`cursor(prepared=True)`를 사용합니다. Python connector의 pooling option은
지원하지 않습니다. Legacy wrapper의 `machbase.open()`에는 database 인자가
없으므로 initial database가 필요하면 최신 `connect(database=...)` API를 사용합니다.

### 9.5 Node.js

```javascript
const { createConnection } = require('@machbase/ts-client');

async function main() {
  const conn = createConnection({
    host: '127.0.0.1',
    port: 5656,
    user: 'APP_A',
    password: 'AppA#1234',
    database: 'FACTORY_A',
  });

  try {
    await conn.connect();
    const [rows] = await conn.query('SELECT CURRENT_DATABASE()');
    console.table(rows);
  } finally {
    await conn.end();
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
```

Node.js connector에도 별도 catalog getter나 catalog metadata API는 없습니다.
SQL로 확인하고 변경합니다. Appender의 최종 성공/실패 건수가 필요하면 close
요약을 버리는 stream wrapper보다 `appendBatch()` 결과를 확인합니다. 문자열 URL을
사용하는 경우 path가 initial database가 됩니다.

### 9.6 Go

`neo-client`의 native 연결은 `api.WithDatabase()`로 접속 직후의 초기
database를 선택할 수 있습니다. 연결 후 `USE`를 실행해 current database를
변경하는 방식도 사용할 수 있습니다.

```go
ctx := context.Background()

db, err := machgo.NewDatabase(&machgo.Config{
    Host: "127.0.0.1",
    Port: 5656,
})
if err != nil {
    return err
}
defer db.Close()

conn, err := db.Connect(
    ctx,
    api.WithPassword("APP_A", "AppA#1234"),
    api.WithDatabase("FACTORY_A"),
)
if err != nil {
    return err
}
defer conn.Close()

var currentDatabase string
if err := conn.QueryRow(ctx, "SELECT CURRENT_DATABASE()").Scan(&currentDatabase); err != nil {
    return err
}
```

현재 데이터베이스의 테이블은 `SYS.SENSOR_LOG`처럼 사용하고, 다른
데이터베이스의 테이블은 `FACTORY_B.SYS.SENSOR_LOG`처럼 세 부분 이름으로
지정합니다.

세 부분 이름으로 Appender를 열어도 connection의 현재 데이터베이스는 바뀌지
않습니다. 다른 데이터베이스를 지정하려면 해당 데이터베이스의 `CONNECT`와
대상 테이블의 `INSERT` 권한이 필요합니다.

```go
appender, err := conn.Appender(ctx, "FACTORY_A.SYS.SENSOR_LOG")
if err != nil {
    return err
}

if err := appender.Append("pump-1", time.Now(), 12.5); err != nil {
    return err
}

success, failed, err := appender.Close()
if err != nil {
    return err
}
if failed != 0 {
    return fmt.Errorf("append result: success=%d, failed=%d", success, failed)
}
```

항상 `Close()`의 오류와 `success`, `failed` 건수를 확인합니다.

Go `database/sql` DSN에 초기 database를 지정하면 모든 새 physical connection에
해당 database가 적용됩니다.

```text
server=tcp://APP_A:AppA%231234@127.0.0.1:5656/FACTORY_A
server=tcp://APP_A:AppA%231234@127.0.0.1:5656;database=FACTORY_A
```

이후 애플리케이션이 `USE FACTORY_B`를 실행해도 pool에 connection을 반환할 때
`ResetSession()`이 설정된 `FACTORY_A`로 복원합니다. DSN에 초기 database를
설정하지 않은 경우에는 애플리케이션이 `USE`와 `CURRENT_DATABASE()`를 직접 관리해야
합니다. database/sql에서 Append가 필요하면 `sql.Conn.Raw()`와
`machbase.Conn.Appender()`를 사용할 수 있으며, 상세 예제는
[Go SDK 문서](/dbms/development-tools-integration/go/)를 참조하십시오.

### 9.7 .NET

.NET 4.0 connector는 connection string의 `DATABASE` 또는 `DB_NAME`으로 initial
database를 지정할 수 있습니다.

```text
SERVER=127.0.0.1;PORT_NO=5656;UID=APP_A;PWD=AppA#1234;DATABASE=FACTORY_A
```

현재 `.NET` provider의 표준 `Database` property와 `ChangeDatabase()`는
multi-database 전환 API로 보장하지 않습니다. 연결 후 전환과 확인은 SQL `USE`,
`CURRENT_DATABASE()`를 사용합니다. Pool 반환 시 catalog reset도 지원 계약으로
가정하지 않습니다. 따라서 .NET은 initial database 선택만 제한적으로 사용합니다.

### 9.8 열린 statement와 handle 주의사항

Prepared plan은 prepare 시점, cursor/result는 execute/open 시점, append session은
append-open 시점의 database에 고정됩니다. 일반 statement handle 자체가 항상
고정되는 것은 아닙니다.

```text
SQLPrepare(A) -> USE B -> SQLExecute       : A
A에서 연 cursor -> USE B -> 계속 fetch     : A
SQLAppendOpen(A) -> USE B -> append         : A
USE B 후 같은 handle의 SQLExecDirect        : B
USE B 후 새 SQLPrepare/Execute               : B
```

데이터베이스를 변경한 뒤에는 새 statement와 handle을 만드는 것을 권장합니다.

같은 connection에서 `CONNECT USER`로 실행 사용자를 바꾸는 경우에는 기존
prepared statement, cursor, append handle을 새 사용자 권한으로 사용할 수 없습니다.
기존 append handle은 `SQLAppendClose`로 정상 종료한 뒤, 새 사용자로 다시
`SQLAppendOpen`해야 합니다.

Database가 삭제된 뒤 같은 이름으로 재생성되어도 이전 prepared lifecycle
statement나 handle은 새 database에 적용되지 않습니다. Stale target 오류가 나면
기존 handle을 폐기하고 새로 prepare/open합니다.

## 10. 상태와 operation 이력 확인

### 10.1 데이터베이스 상태

```sql
SELECT
    database_id,
    tablespace_id,
    source_database_id,
    name,
    kind,
    access_mode,
    can_use,
    state,
    is_default
FROM V$DATABASES
ORDER BY database_id;
```

중요한 컬럼은 다음과 같습니다.

| 컬럼 | 의미 |
| --- | --- |
| `DATABASE_ID` | 논리 데이터베이스 식별자 |
| `TABLESPACE_ID` | 물리 tablespace 식별자 |
| `SOURCE_DATABASE_ID` | mount한 backup의 원본 데이터베이스 식별자 |
| `KIND` | `ACTIVE` 또는 `MOUNTED` |
| `ACCESS_MODE` | `READ_WRITE` 또는 `READ_ONLY` |
| `CAN_USE` | `USE`로 선택할 수 있는지 여부 |
| `STATE` | 현재 lifecycle 상태 |
| `IS_DEFAULT` | `MACHBASEDB`이면 `1` |

`DATABASE_ID`와 `TABLESPACE_ID`는 다른 값입니다. 논리 데이터베이스를 구분할
때 tablespace ID를 사용하지 않습니다.

Active database의 주요 lifecycle state는 `CREATING`, `NORMAL`, `RESTORING`,
`DROPPING`, `FAILED_NEEDS_ACTION`입니다. 일반 운영에서는 `NORMAL`인지 확인합니다.

### 10.2 현재 연결의 데이터베이스

```sql
SELECT
    id,
    auth_user_name,
    user_name,
    current_db_id,
    current_db_name
FROM V$SESSION
ORDER BY id;
```

현재 구현에서 `AUTH_USER_NAME`과 `USER_NAME`은 같은 연결 사용자 이름을
표시합니다. 다른 사용자의 session 정보는 `SYS` 운영 조회로 취급합니다.

### 10.3 Object metadata를 안전하게 조인

다른 database의 table/index ID가 같을 수 있으므로 object ID 하나만으로
`M$SYS_*` view를 조인하면 metadata가 섞일 수 있습니다. Child metadata는
`DATABASE_ID`와 parent object ID를 함께 조인합니다.

```sql
SELECT
    t.database_name,
    t.name AS table_name,
    c.name AS column_name
FROM M$SYS_TABLES t
JOIN M$SYS_COLUMNS c
  ON c.database_id = t.database_id
 AND c.tablespace_id = t.tablespace_id
 AND c.table_id = t.id
ORDER BY t.database_id, t.tablespace_id, t.id, c.id;
```

`M$SYS_TABLES`, `M$SYS_COLUMNS`, `M$SYS_INDEXES`는 사용자가 볼 수 있는 여러
database의 metadata를 반환할 수 있습니다. `M$SYS_USERS`는 인스턴스 전역이며,
`M$SYS_TABLE_PROPERTY`처럼 current database 범위인 view도 있으므로 각 view의
`DATABASE_ID`/`DATABASE_NAME` 컬럼을 확인합니다.

### 10.4 Standard operation 이력

`SYS`는 다음 작업의 local 이력을 조회할 수 있습니다.

- CREATE, ALTER, DROP DATABASE
- BACKUP, RESTORE DATABASE
- MOUNT, UMOUNT DATABASE

```sql
SELECT
    operation_id,
    operation_type,
    database_name,
    state,
    last_error,
    created_at,
    updated_at
FROM V$DATABASE_OPERATIONS
ORDER BY operation_id DESC;
```

특정 operation은 다음과 같이 확인합니다.

```sql
SHOW DATABASE OPERATION '<operation_id>';
```

정상 완료 상태는 `SUCCEEDED`입니다. 자동 복구하지 못한 작업은
`FAILED_NEEDS_ACTION`으로 표시될 수 있습니다.

`FAILED_NEEDS_ACTION`을 발견하면 같은 이름으로 DROP/RESTORE/REPLACE를 반복하지
않습니다. Server log, 해당 operation row와 backup image를 보존하고 기술 지원을
요청합니다.

`V$DATABASE_OPERATIONS`는 `SYS` 운영용입니다. Parser, 권한 또는 preflight에서
작업이 시작되기 전에 실패한 모든 요청이 반드시 row로 기록되는 것은 아닙니다.
BACKUP/MOUNT/UMOUNT의 이력 기록은 본 작업과 별도로 처리될 수 있으므로 실제
database 상태와 함께 확인합니다.

`SHOW DATABASE OPERATION`은 machsql 명령입니다. 다른 client에서는
`V$DATABASE_OPERATIONS`를 직접 조회합니다. 시작 시 남아 있는 RESTORING 작업은
rollback, DROPPING 작업은 roll-forward 복구를 시도하며 자동 복구할 수 없는
catalog는 `FAILED_NEEDS_ACTION`으로 격리됩니다.

## 11. 테이블 종류별 주의사항

- LOG와 TAG 테이블은 `SELECT`, `INSERT`, `DELETE`를 지원하며 `UPDATE`는
  지원하지 않습니다.
- VOLATILE과 LOOKUP 테이블은 전체 DML을 지원합니다.
- VOLATILE과 LOOKUP 테이블 조회는 `WHERE` 절에 primary key 조건을
  사용합니다.
- 각 데이터베이스에 이름이 같은 LOG, TAG, VOLATILE, LOOKUP,
  TRANSACTION 테이블을 따로 만들 수 있습니다.

## 12. 호환성과 제한

### 12.1 기존 동작 유지

- 기존 데이터와 객체는 `MACHBASEDB`에 속합니다.
- 기존 `owner.table` SQL의 의미는 바뀌지 않습니다.
- 데이터베이스를 지정하지 않는 client는 `MACHBASEDB`에 연결됩니다.
- 빈 database 값과 `data`는 `MACHBASEDB`로 해석됩니다.
- `machadmin` 명령은 계속 인스턴스 전체를 생성, 시작, 종료, 삭제합니다.

### 12.2 기존 인스턴스 업그레이드

서버를 처음 시작할 때 기존 metadata는 다중 database 형식으로 자동 변환됩니다.
기존 table, view, index와 권한은 `MACHBASEDB`에 귀속되고 기존 사용자에게
`MACHBASEDB` `CONNECT`가 추가됩니다.

이 변환은 구버전 binary가 새 metadata를 다시 읽을 수 있도록 되돌리는 작업이
아닙니다. 다음 절차로 업그레이드합니다.

1. 기존 server를 정상 종료합니다.
2. 기존 버전의 전체 인스턴스 backup과 설정 파일 사본을 만듭니다.
3. 새 binary로 시작해 metadata 변환을 완료합니다.
4. `SHOW DATABASES`에서 `MACHBASEDB`가 `ACTIVE/NORMAL`인지 확인합니다.
5. 기존 table/view/index와 주요 row count를 확인합니다.
6. 기존 사용자로 다시 연결하고 `M$SYS_USER_ACCESS`와 실제 DML을 확인합니다.
7. 문제가 있으면 구 binary를 새 metadata에 직접 적용하지 말고 업그레이드 전
   backup을 별도 data directory에 복원합니다.

이전 metadata 형식은 자동 변환되지만 모든 과거 8.5.x release와 client 조합을
포괄하는 호환 보장은 아닙니다. 8.5.2의 기본 `MACHBASEDB`와 legacy metadata
동작을 호환 기준으로 사용합니다.

### 12.3 Client/server 조합

다중 active database를 연결 시점에 선택하려면 Machbase 8.6.0 server와 같은
release의 client package를 사용합니다.

| Client → Server | `MACHBASEDB` | 비기본 active database |
| --- | --- | --- |
| 8.5.2 client → 8.6.0 server | 기존 방식으로 지원 | 구 client에 initial database 선택 API가 없음 |
| 8.6.0 client → 8.5.2 server | legacy fallback 지원 | Client에 따라 연결 거부 또는 `MACHBASEDB` fallback |
| 8.6.0 client → 8.6.0 server | 지원 | 지원 |

비기본 database를 요청한 경우 연결 직후 반드시 `CURRENT_DATABASE()`를 확인합니다.

- Native C/ODBC, Python, Node.js는 8.5.2 server가 비기본 database를 확인하지 못하면
  연결을 거부합니다.
- JDBC와 .NET은 8.5.2 server 호환 동작에서 요청한 비기본 이름 대신 `MACHBASEDB`를
  사용할 수 있으므로 확인 없이 요청이 적용됐다고 가정하면 안 됩니다.
- ODBC/JDBC의 8.5.2 server metadata는 current catalog의 legacy 조회만 보장하며
  다른 catalog를 인자로 지정하는 기능은 지원하지 않을 수 있습니다.
- Go neo-client의 8.5.2 server fallback은 `MACHBASEDB`와 기존 mounted metadata
  호환 범위입니다. 다중 active database에는 8.6.0 server가 필요합니다.

Server와 client package를 같은 release로 함께 배포합니다.

### 12.4 이번 범위에 포함되지 않는 기능

- Cluster edition의 분산 catalog 전파와 장애 복구
- 데이터베이스별 CPU, 메모리, 디스크 quota
- 데이터베이스별 물리 프로세스 또는 storage 격리
- 데이터베이스별 audit 저장·조회 기능
- mounted database의 쓰기와 `USE`
- Active session의 `CONNECT` 회수 시 이미 열린 prepared/cursor에 대한 즉시 적용 보장
- Quoted/Unicode database 이름의 모든 경계 조합
- RESTORE owner remap의 모든 다대일 object-name 충돌 조합
- .NET의 current-catalog API와 pool catalog reset

## 13. 문제 해결

| 증상 | 확인할 내용 | 해결 방법 |
| --- | --- | --- |
| 연결할 때 database 선택 실패 | 이름, `CONNECT` | database 생성과 권한을 확인합니다. |
| `USE` 실패 | transaction, `CONNECT`, database 종류 | transaction을 종료하고 active database를 선택합니다. |
| 다른 database 조회 실패 | `CONNECT`와 table 권한 | 두 권한을 모두 부여합니다. |
| mounted 조회 실패 | `USAGE`와 table `SELECT` | 두 권한을 모두 부여합니다. |
| READ ONLY 전환 실패 | 실행 중인 write, append, DDL | 쓰기 작업을 종료한 뒤 다시 실행합니다. |
| `DROP ... CASCADE` 실패 | 사용 중인 연결과 handle | 필요하면 `FORCE`를 함께 지정합니다. |
| `DROP ... FORCE` 실패 | 남아 있는 객체 | 필요하면 `CASCADE`를 함께 지정합니다. |
| FORCE 뒤 연결만 종료됨 | 객체가 있는 DB에 FORCE만 실행 | DB 상태를 확인하고 필요하면 `CASCADE FORCE`를 실행합니다. |
| 현재 database 삭제 실패 | 삭제 session의 current database | 먼저 `USE MACHBASEDB`를 실행합니다. |
| umount 실패 | mounted 객체를 사용하는 handle | statement와 cursor를 닫습니다. |
| restore 사용자 오류 | backup의 owner 사용자 | 사용자를 만들거나 owner remap을 지정합니다. |
| restore unsupported 오류 | rollup, retention, TAG 확장, generator, index 유형 | 제한 항목을 제거한 backup을 사용합니다. |
| full backup restore/mount 실패 | image에 active DB가 여러 개 있음 | 단일 database logical backup을 사용합니다. |
| `REPLACE` 실패 | READ ONLY와 사용 중 여부 | READ ONLY로 바꾸고 모든 참조를 종료합니다. |
| Restore 후 일반 사용자 접근 실패 | grant는 image/target에서 승계되지 않음 | `CONNECT`와 table 권한을 다시 부여합니다. |
| 재생성 DB에서 old handle 실패 | database identity가 변경됨 | statement, cursor와 appender를 새로 만듭니다. |
| Metadata join 결과 중복 | object ID만으로 child view 조인 | `DATABASE_ID`와 object ID를 함께 조인합니다. |
| 8.5.2 server에서 비기본 DB가 적용되지 않음 | client fallback | `CURRENT_DATABASE()`로 확인하고 같은 release client/server를 사용합니다. |
| Go pool에서 다른 DB가 조회됨 | current DB가 pool 반환 시 reset되지 않음 | physical connection을 고정하고 작업마다 `USE`를 실행합니다. |

## 14. 운영 점검표

### 기존 인스턴스를 업그레이드할 때

1. Server를 정상 종료합니다.
2. 전체 인스턴스 backup과 설정 사본을 확보합니다.
3. 새 binary로 시작해 metadata 변환을 완료합니다.
4. `V$DATABASES`에서 `MACHBASEDB` 상태를 확인합니다.
5. 기존 객체, 데이터, 사용자와 권한을 확인합니다.
6. Rollback이 필요하면 업그레이드 전 backup을 사용합니다.

### 새 데이터베이스를 서비스에 연결할 때

1. `CREATE DATABASE`로 생성합니다.
2. 애플리케이션 사용자를 생성합니다.
3. 데이터베이스 `CONNECT` 권한을 부여합니다.
4. 필요한 테이블 권한만 부여합니다.
5. `machsql -D` 또는 client `database` 옵션으로 연결합니다.
6. `CURRENT_DATABASE()`와 실제 테이블 조회 결과를 확인합니다.
7. Pool을 사용하면 connection 반환 시 current database reset 정책을 확인합니다.

### 데이터베이스를 backup/restore할 때

1. `V$DATABASES`에서 source가 `ACTIVE/NORMAL`인지 확인합니다.
2. 미커밋 transaction과 append를 정상 종료합니다.
3. 새 경로에 `BACKUP DATABASE`를 실행합니다.
4. Restore 제한 객체와 image 종류를 확인합니다.
5. 필요한 owner user를 만들거나 `REMAP OWNER`를 준비합니다.
6. REPLACE라면 target을 READ ONLY로 바꾸고 모든 참조를 종료합니다.
7. Restore 후 mode, object, row count를 확인합니다.
8. `CONNECT`, database DDL과 table 권한을 다시 부여합니다.

### 데이터베이스를 삭제할 때

1. 애플리케이션 쓰기를 중지합니다.
2. 필요한 경우 online backup을 생성합니다.
3. `ALTER DATABASE ... READ ONLY`로 전환합니다.
4. 연결, cursor, append handle을 정상 종료합니다.
5. 삭제를 실행하는 session에서 `USE MACHBASEDB`를 실행합니다.
6. 객체가 있으면 `CASCADE`, 사용 중인 참조가 있으면 `FORCE`를 지정합니다.
7. `SHOW DATABASES`와 `V$DATABASE_OPERATIONS`에서 완료를 확인합니다.
