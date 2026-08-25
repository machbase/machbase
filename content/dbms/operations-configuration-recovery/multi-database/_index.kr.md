---
type: docs
title: '14.5 다중 데이터베이스'
weight: 50
toc: true
---

Standard Edition에서는 하나의 server instance 안에 여러 logical database를 만들고
connection별 current database를 선택할 수 있습니다. 이 페이지는 공개 SQL과 client 선택
방법만 다루며 내부 identity·catalog 구현과 과거 metadata 형식은 설명하지 않습니다.

## 1. 이 기능으로 할 수 있는 일

- 같은 이름의 table을 database별로 분리
- 사용자에게 database 접속 권한과 table 권한 부여
- connection의 current database 변경
- `database.owner.object` 이름으로 다른 database 객체 조회
- database 단위 backup·mount·restore 수행

### 적용 범위

기본 database는 `MACHBASEDB`입니다. database를 지정하지 않는 기존 connection은 기본
database를 사용합니다. 생성·삭제·권한·backup 지원 여부는 edition과 현재 release를
확인합니다.

### 격리되는 것과 공유되는 것

table·view·index 같은 객체 namespace와 데이터는 database별로 분리됩니다. server process,
listener, 일부 전역 설정과 system account는 instance 범위입니다.

## 2. 먼저 알아둘 네 가지

### 2.1 기본 데이터베이스는 `MACHBASEDB`입니다

```sql
SELECT CURRENT_DATABASE();
SHOW DATABASES;
```

### 2.2 현재 데이터베이스는 연결마다 다릅니다

한 connection의 `USE`는 다른 connection에 영향을 주지 않습니다. pool에서는 다음 요청이
같은 physical connection을 받는다고 가정하지 않습니다.

### 2.3 객체 이름은 최대 세 부분입니다

`object`, `owner.object`, `database.owner.object` 형식을 사용합니다. 다른 database를
명시할 때 owner를 생략하지 않습니다.

### 2.4 Active database와 mounted database

active database는 일반 읽기·쓰기에 사용하고, mounted database는 backup 조회·선별 복구에
사용하는 읽기 전용 경로입니다. mount 이름과 active database 이름을 혼동하지 않습니다.

## 3. 5분 빠른 시작

다음 예제는 관리자 계정으로 database 격리와 세 부분 이름 조회를 확인한 뒤 모든 객체를
정리합니다.

### 3.1 관리자가 데이터베이스와 사용자를 만듭니다

```sql
CREATE DATABASE IF NOT EXISTS manual_multidb_a;
CREATE DATABASE IF NOT EXISTS manual_multidb_b;

USE manual_multidb_a;
CREATE LOG TABLE sensor_event (
    event_time DATETIME,
    message    VARCHAR(100)
);
INSERT INTO sensor_event VALUES (NOW, 'from-a');

USE manual_multidb_b;
CREATE LOG TABLE sensor_event (
    event_time DATETIME,
    message    VARCHAR(100)
);
INSERT INTO sensor_event VALUES (NOW, 'from-b');
```

### 3.2 애플리케이션 사용자가 데이터를 입력합니다

운영 사용자는 database `CONNECT`와 대상 객체의 필요한 권한만 받습니다. 사용자 생성과
권한 SQL은 [계정과 권한](/dbms/security-access-control/)을 참고합니다.

### 3.3 두 데이터베이스가 분리되었는지 확인합니다

```sql
SELECT message FROM manual_multidb_a.SYS.sensor_event;
SELECT message FROM manual_multidb_b.SYS.sensor_event;

USE MACHBASEDB;
DROP DATABASE manual_multidb_a CASCADE FORCE;
DROP DATABASE manual_multidb_b CASCADE FORCE;
```

## 4. 데이터베이스 선택과 조회

### 4.1 현재 데이터베이스 확인

`SELECT CURRENT_DATABASE()`를 connection 직후와 pool에서 빌린 직후에 확인할 수 있습니다.

### 4.2 현재 데이터베이스 변경

`USE database_name`은 해당 connection의 current database를 바꿉니다. 열린 statement,
cursor, Appender가 있다면 먼저 닫고 database 변경 뒤 새로 생성합니다.

### 4.3 다른 데이터베이스를 직접 조회

```text
SELECT * FROM FACTORY_A.APP_USER.SENSOR_DATA;
```

세 부분 이름은 object 권한을 우회하지 않습니다. 대상 database 접속과 object 접근 권한이
모두 필요합니다.

### 4.4 명시적 객체 이름과 statement 대상

statement를 준비한 시점과 실행 시점의 database가 다르지 않도록 합니다. 장기 실행
애플리케이션은 SQL에 세 부분 이름을 사용하거나 connection 초기화에서 current database를
명시적으로 설정합니다.

### 4.5 Transaction과 current database

transaction이 열린 상태에서 database를 바꾸지 않습니다. 먼저 commit 또는 rollback하고
statement를 닫은 뒤 전환합니다.

## 5. 데이터베이스와 객체 찾기

`SHOW DATABASES`와 `V$DATABASES`로 database 상태를 확인합니다. table metadata를
조인할 때는 이름만 사용하지 말고 database ID와 owner ID를 포함합니다.

## 6. 사용자와 권한

### 6.1 권한 종류

database `CONNECT`, 객체 `SELECT`·`INSERT`·`UPDATE`·`DELETE` 등 필요한 권한을
분리합니다.

### 6.2 권한 부여

관리자는 application 역할별 최소 권한을 부여하고, 실제 application 계정으로 연결·조회·입력
테스트를 수행합니다.

### 6.3 권한 회수

회수 전 사용 중인 connection과 batch job을 확인하고, 회수 후 신규 connection에서 차단을
검증합니다.

### 6.4 GRANT/REVOKE 기본 문법

전체 문법과 지원 조합은
[사용자·인증 SQL](/dbms/reference/sql/syntax-dictionary-sql/user-auth-syntax/)을 정본으로
사용합니다.

### 6.5 데이터베이스 권한 전체 조합

권한 조합을 이 운영 페이지에 복제하지 않습니다. 현재 release의 권한 레퍼런스를 확인합니다.

### 6.6 Active database의 테이블 권한 전체 조합

읽기 계정과 쓰기 계정을 분리하고 필요한 object에만 권한을 부여합니다.

### 6.7 Mounted database의 테이블 권한 조합

mounted database는 읽기 전용 복구·조사 목적에 한정합니다.

### 6.8 Active database 접근 조합

database `CONNECT`와 object 권한을 함께 검증합니다.

### 6.9 허용되지 않는 대표 조합

다른 database의 권한을 현재 database 권한으로 대체하거나, owner 이름만으로 database
접근을 우회할 수 없습니다.

### 6.10 기존 GRANT/REVOKE 문법과의 차이

기존 문법 호환성보다 현재 공개 `GRANT`·`REVOKE` 구문을 사용합니다.

### 6.11 권한의 수명과 정리

사용자·database·object를 삭제할 때 관련 grant와 운영 계정 의존성을 먼저 확인합니다.

## 7. 데이터베이스 운영

### 7.1 생성

이름 충돌과 기본 database 여부를 확인한 뒤 생성합니다. 완료 후 `SHOW DATABASES`에서
state를 확인합니다.

### 7.2 읽기 전용으로 전환

쓰기 차단 전 진행 중 transaction·Appender를 정리하고, 신규·기존 connection 모두에서
쓰기 실패와 읽기 성공을 검증합니다.

### 7.3 안전하게 삭제

database 삭제는 포함된 모든 객체와 데이터를 제거합니다. application 연결을 차단하고
backup·복원 테스트와 정확한 대상 이름을 확인한 뒤 실행합니다. `CASCADE FORCE`를
일상적인 정리 구문으로 사용하지 않습니다.

## 8. Backup, mount, restore

### 8.1 데이터베이스 백업

경로, 권한, free space, 완료 상태를 확인합니다.

### 8.2 Backup을 읽기 전용으로 mount

운영 database와 다른 mount 이름을 사용하고 필요한 query만 수행합니다.

### 8.3 새 데이터베이스로 restore

동일 이름을 덮어쓰기보다 새 이름으로 restore해 검증한 뒤 전환하는 방식을 우선 검토합니다.

### 8.4 기존 데이터베이스 교체

현재 데이터를 잃을 수 있으므로 service 중단, backup, rollback, connection 전환 계획이
필요합니다.

### 8.5 Restore 제한사항

구문, edition, backup 종류, mount·restore 제한은
[백업·복원·마운트](../backup-restore-mount/)를 정본으로 사용합니다.

## 9. Client에서 데이터베이스 선택

### 9.1 machsql

`machsql -D DATABASE_NAME`으로 초기 database를 지정하거나 연결 후 `USE`를 실행합니다.

### 9.2 Native C와 ODBC

지원 driver에서는 connection string의 `DATABASE` 또는 `DBNAME`을 사용하고
`SQL_DATABASE_NAME` 또는 `CURRENT_DATABASE()`로 확인합니다.

### 9.3 JDBC

JDBC URL path 또는 지원 property로 초기 database를 지정하고 `getCatalog()`로 확인합니다.

### 9.4 Python

DB-API `connect(database="FACTORY_A")`를 사용합니다. 호환 `machbase.open()`에는 database
인자가 없으므로 다중 database에는 DB-API connection을 사용합니다.

### 9.5 Node.js

connection config의 `database` 또는 URL path를 사용하고 `CURRENT_DATABASE()`로
확인합니다.

### 9.6 Go

neo-client v1.8.3 이상 native `machgo`는 연결 시 `api.WithDatabase("FACTORY_A")`로 초기
database를 선택합니다. 이미 열린 같은 connection에서 전환할 때는
`conn.Exec(ctx, "USE FACTORY_A")`를 실행합니다. `database/sql`은 DSN의 `database`/`db`
또는 URL path/query로 초기 database를 지정하면 pool에서 connection을 재사용할 때 설정된
database로 복원합니다. SDK 최소 버전과 `CURRENT_DATABASE()` 결과를 함께 검증하십시오.

### 9.7 .NET

connection string의 `DATABASE` 또는 `DB_NAME`을 사용합니다. `Database` property와
`ChangeDatabase()` 지원은 connector API에서 확인하고, SQL `CURRENT_DATABASE()`로
검증합니다.

### 9.8 열린 statement와 handle 주의사항

database를 바꾸기 전에 result set, prepared statement, Append handle을 닫습니다. pool은
반환·대여 시 database reset 정책을 테스트합니다.

## 10. 상태와 operation 이력 확인

### 10.1 데이터베이스 상태

`SHOW DATABASES`와 `V$DATABASES`에서 이름, state, access mode를 확인합니다.

### 10.2 현재 연결의 데이터베이스

`CURRENT_DATABASE()`를 사용합니다.

### 10.3 Object metadata를 안전하게 조인

table·column·index metadata는 database ID, owner ID, object ID를 포함해 조인합니다.
내부 예약 이름을 application 로직에 사용하지 않습니다.

### 10.4 Standard operation 이력

공개 operation view가 제공되면 시작·종료·성공·오류를 확인합니다. 컬럼은 현재 release에서
`DESC`로 확인합니다.

## 11. 테이블 종류별 주의사항

- TAG·LOG Append target은 database 전환 뒤 다시 엽니다.
- TRANSACTION transaction 중 database를 바꾸지 않습니다.
- LOOKUP refresh 범위와 cluster 동작은 edition 문서를 확인합니다.
- VOLATILE table은 server restart 때 정의와 데이터가 소멸합니다.

## 12. 호환성과 제한

### 12.1 기존 동작 유지

database를 지정하지 않는 기존 client는 `MACHBASEDB`를 사용합니다.

### 12.2 기존 인스턴스 업그레이드

지원되는 upgrade 경로와 backup 검증을 먼저 수행합니다.

### 12.3 Client/server 조합

같은 release의 server와 SDK를 우선 사용하고, 혼합 버전은 staging에서 초기 database,
metadata, prepared statement, Appender를 모두 검증합니다.

### 12.4 이번 범위에 포함되지 않는 기능

확인되지 않은 cross-database DDL·transaction·Appender 동작을 추정하지 않습니다.

## 13. 문제 해결

| 증상 | 확인 |
|------|------|
| 접속 직후 예상 database가 아님 | 연결 옵션과 `CURRENT_DATABASE()` |
| 세 부분 이름 query가 거부됨 | database `CONNECT`와 object 권한 |
| pool에서 간헐적으로 다른 database | connection reset·초기화 |
| prepared statement가 다른 object 사용 | database 변경 뒤 statement 재생성 |
| Appender open 실패 | target 이름, database, 권한, handle 재생성 |
| drop 실패 | active connection·operation과 access mode |

## 14. 운영 점검표

### 기존 인스턴스를 업그레이드할 때

backup·restore 테스트, client 호환성, default database를 확인합니다.

### 새 데이터베이스를 서비스에 연결할 때

최소 권한 계정으로 connect, current database, DDL·DML, metadata, pool reset을 검증합니다.

### 데이터베이스를 backup/restore할 때

경로·공간·권한, 완료 상태, mount query, 새 database restore 결과를 확인합니다.

### 데이터베이스를 삭제할 때

service 연결 차단, backup, 정확한 이름, 의존 job·grant, 삭제 후 client 동작을 확인합니다.
