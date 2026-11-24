---
type: docs
title: '19.6.7 권한별 기능 지원표'
weight: 70
toc: true
---

Machbase는 데이터베이스, 테이블과 DFQ 파일 원본의 범위에 따라 권한을 부여합니다.

## 데이터베이스 권한

데이터베이스 권한은 지정한 active database 범위에 적용됩니다. `MOUNT`는
`MACHBASEDB`에 부여하고, mounted database 접근에는 `USAGE`와 table `SELECT`를
별도로 부여합니다.

| 권한 | 허용하는 작업 | 기본 보유 |
|------|-------------|:--------:|
| `CONNECT` | active database 연결, `USE`, 객체 탐색 | O(MACHBASEDB 호환) |
| `CREATE` | 테이블, 뷰, 인덱스, 롤업, 테이블스페이스, 리텐션 생성 | O |
| `DROP` | 테이블, 뷰, 인덱스, 롤업, 테이블스페이스, 리텐션 삭제 | O |
| `ALTER` | 테이블 구조 변경, `ALTER SYSTEM` 실행 | X |
| `BACKUP` | `BACKUP DATABASE` 실행 | X |
| `MOUNT` | `MOUNT DATABASE` / `UMOUNT DATABASE` 실행 | X |
| `USAGE` | mounted database 탐색 | X |
| `DDL` | CREATE + DROP 묶음 (합성 권한) | — |
| `ALL` | CONNECT, CREATE, DROP, ALTER, BACKUP 일괄 부여 | — |

> "기본 보유 O"는 `CREATE USER`로 생성된 사용자의 `MACHBASEDB` 호환 기본 권한을 뜻합니다.
> 다른 논리 데이터베이스의 권한은 별도로 부여합니다.

## 테이블 권한

테이블 권한은 특정 테이블에 대한 DML 작업을 제어합니다.

| 권한 | 허용하는 작업 |
|------|-------------|
| `SELECT` | 특정 테이블 SELECT 조회 |
| `INSERT` | 특정 테이블 INSERT |
| `DELETE` | 특정 테이블 DELETE |
| `UPDATE` | 특정 테이블 UPDATE |
| `ALL` | `SELECT`, `INSERT`, `DELETE`, `UPDATE` 묶음 |

## DFQ 읽기 권한

| 권한 | 허용하는 작업 |
|---|---|
| `READ ON DIRECTORY` | 해당 서버 디렉터리와 하위 디렉터리의 로컬 파일 읽기 |
| `READ ON ENDPOINT` | 실제 접속 주소와 인증 출처 조합에 해당하는 원격 파일 읽기 |

Standard Edition에서 현재 데이터베이스와 사용자별로 권한을 부여합니다. VIEW에서
읽을 때도 실행 사용자의 READ 권한을 적용합니다. 권한 부여·회수와 검증 절차는
[DFQ 파일 읽기](/kr/dbms-8.9/security-access-control/privileges/#dfq-파일-읽기)를 참고합니다.

## GRANT / REVOKE 문법

```sql
-- 데이터베이스 권한 부여
GRANT CONNECT ON DATABASE factory_a TO app_user;
GRANT CREATE ON DATABASE factory_a TO app_user;
GRANT BACKUP ON DATABASE factory_a TO backup_user;
GRANT ALL ON DATABASE factory_a TO admin_user;

-- 테이블 권한 부여
GRANT SELECT ON sys.sensor_data TO reader_user;
GRANT INSERT ON sys.sensor_data TO writer_user;

-- 권한 취소
REVOKE SELECT ON sys.sensor_data FROM reader_user;
REVOKE BACKUP ON DATABASE factory_a FROM backup_user;
```

## 권한이 필요한 주요 작업

| 작업 | 필요 권한 종류 | 필요 권한 |
|------|-------------|---------|
| `CREATE TABLE` | 데이터베이스 | CREATE |
| `DROP TABLE` | 데이터베이스 | DROP |
| `ALTER TABLE` | 데이터베이스 | ALTER |
| `BACKUP DATABASE` | 데이터베이스 | BACKUP |
| `MOUNT DATABASE` | 데이터베이스 | MOUNT |
| 테이블 SELECT | 테이블 | SELECT |
| 테이블 INSERT | 테이블 | INSERT |
| 테이블 UPDATE | 테이블 | UPDATE |
| 테이블 DELETE | 테이블 | DELETE |
| 로컬 파일 READ | 서버 디렉터리 | READ ON DIRECTORY 및 서버 OS 읽기 권한 |
| 원격 파일 READ | 원격 엔드포인트 | READ ON ENDPOINT 및 해당 인증 출처 |

## 권한 현황 조회

```sql
SELECT NAME, USER_ID FROM M$SYS_USERS ORDER BY USER_ID;

-- 데이터베이스와 테이블의 권한 기록
SELECT DB_NAME, USER_NAME, OWNER_NAME, TABLE_NAME, PRIV
  FROM M$SYS_USER_ACCESS
 WHERE USER_NAME = 'APP_USER'
 ORDER BY DB_NAME, OWNER_NAME, TABLE_NAME;
```

SYS는 전체 권한 기록을, 일반 사용자는 자신의 기록을 조회합니다. DFQ의 파일 권한은
[대상 계정으로 READ를 실행](/kr/dbms-8.9/security-access-control/privileges/#dfq-권한-확인)해 확인합니다.

## 상세 레퍼런스

권한 모델 전체 설명과 예제는 [권한 관리](/dbms-8.9/security-access-control/privileges/) 섹션을 참고하십시오.
