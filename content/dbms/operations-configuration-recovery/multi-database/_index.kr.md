---
type: docs
title: '13.2 다중 데이터베이스'
weight: 20
toc: true
---

Standard Edition에서는 한 서버 안에 여러 논리 데이터베이스를 만들고 객체와 접근 권한을
분리할 수 있습니다. 이 페이지는 도입과 운영 흐름만 설명합니다. SQL 문법, 권한, SDK 옵션과
백업 절차는 연결된 정본을 사용합니다.

## 적용 범위

- 다중 데이터베이스는 Standard Edition 기능입니다.
- 논리 데이터베이스는 별도 서버 프로세스나 자원 quota를 만들지 않습니다.
- 객체 이름은 `object`, `owner.object`, `database.owner.object`의 최대 세 부분입니다.
- 다른 데이터베이스를 지정할 때 owner를 생략하지 않습니다.
- mounted database는 active database와 다른 읽기 전용 백업 조회 경로입니다.

## 도입 전 결정 사항

1. 데이터베이스별 owner와 애플리케이션 사용자를 정합니다.
2. `CONNECT`와 객체별 최소 권한을 정의합니다.
3. connection pool이 current database를 어떻게 초기화·복원하는지 확인합니다.
4. 백업 단위, 복구 순서와 mounted database 이름 규칙을 정합니다.
5. 데이터베이스별 사용량과 장애를 구분할 모니터링 기준을 마련합니다.

## 빠른 검증

다음 예제는 두 데이터베이스가 분리되는지 확인한 뒤 모두 정리합니다.

```sql
CREATE DATABASE IF NOT EXISTS manual_multidb_a;
CREATE DATABASE IF NOT EXISTS manual_multidb_b;

USE manual_multidb_a;
CREATE LOG TABLE sensor_event (
    event_time DATETIME,
    message    VARCHAR(100)
);
INSERT INTO sensor_event VALUES (SYSDATE, 'from-a');

USE manual_multidb_b;
CREATE LOG TABLE sensor_event (
    event_time DATETIME,
    message    VARCHAR(100)
);
INSERT INTO sensor_event VALUES (SYSDATE, 'from-b');

SELECT message FROM manual_multidb_a.SYS.sensor_event;
SELECT message FROM manual_multidb_b.SYS.sensor_event;

USE MACHBASEDB;
DROP DATABASE manual_multidb_a CASCADE FORCE;
DROP DATABASE manual_multidb_b CASCADE FORCE;
```

`USE database_name`은 현재 connection의 database를 변경합니다. transaction, 열린 cursor,
prepared statement와 Appender가 있는 상태에서 전환하지 마십시오. 다른 database의 객체는
`database.owner.object`로 명시합니다.

## 권한 경계

사용자는 대상 database의 `CONNECT` 권한과 실제 객체 작업에 필요한 권한을 모두 가져야
합니다. database 생성·삭제·권한 SQL은
[계정과 권한](/dbms/security-access-control/privileges/)을 정본으로 사용합니다. 운영 계정에
관리자 권한을 일괄 부여하지 않습니다.

## 애플리케이션 연결

SDK마다 초기 database를 지정하는 option 이름과 pool reset 동작이 다릅니다. 각 SDK의
connection 문서에서 지원 여부를 확인하고, connection을 빌린 직후 다음 값을 검증합니다.

```sql
SELECT CURRENT_DATABASE();
```

언어별 설정은 [개발 및 애플리케이션 연동](/dbms/development-tools-integration/)을,
서버·SDK 호환성은
[서버와 SDK 호환성](/dbms/reference/support-scope-constraints/compatibility-xma-protocol/)을
참고하십시오.

## 백업과 복구

백업 전에 포함할 active database와 복구 순서를 기록합니다. mounted database는 `USE`할 수
없으며, `USAGE`와 대상 테이블의 `SELECT` 권한으로 세 부분 이름을 조회합니다. 정확한 명령과
검증 절차는 [백업, 복원, 마운트](../backup-restore-mount/)를 사용하십시오.

## 운영 체크리스트

- connection 직후와 pool 재사용 직후 `CURRENT_DATABASE()`가 기대값인가
- SQL과 모니터링이 동일 이름의 다른 database 객체를 혼동하지 않는가
- 사용자에게 대상 database와 객체의 최소 권한만 부여했는가
- 백업·복구 훈련에서 모든 대상 database를 확인했는가
- database 삭제 전에 열린 connection, 객체와 백업 보존 조건을 확인했는가

정확한 `CREATE/DROP/USE DATABASE` 문법은
[DATABASE 문법](/dbms/reference/sql/syntax-dictionary-sql/database-syntax/)을 참고하십시오.
