---
type: docs
title: '17.3 권한 관리'
weight: 160
toc: true
---

Machbase는 데이터베이스 연결·관리, 테이블 DML, DFQ 파일 읽기에 필요한 권한을 작업
대상별로 부여합니다. 사용자는 데이터베이스에 연결할 `CONNECT` 권한과 수행할 작업에
필요한 권한을 함께 가져야 합니다.

```sql
GRANT CONNECT ON DATABASE factory_a TO app_user;
GRANT SELECT, INSERT ON TABLE factory_a.sys.sensor_log TO app_user;
```

<a id="privileges"></a>

## 권한 모델

| 범위 | 권한 | 용도 |
|---|---|---|
| 활성 데이터베이스 | `CONNECT` | 연결 및 `USE` |
| 활성 데이터베이스 | `CREATE`, `DROP`, `ALTER` | 객체 생성·삭제·변경 |
| 활성 데이터베이스 | `BACKUP` | 데이터베이스 백업 |
| 활성 데이터베이스 | `DDL` | `CREATE`와 `DROP` 묶음 |
| 활성 데이터베이스 | `ALL` | `CONNECT`, `CREATE`, `DROP`, `ALTER`, `BACKUP` |
| 마운트된 데이터베이스 | `USAGE` | 마운트된 데이터베이스 탐색 |
| 관리 데이터베이스 | `MOUNT` | `MOUNT DATABASE`, `UMOUNT DATABASE` |
| 테이블 | `SELECT`, `INSERT`, `DELETE`, `UPDATE` | 특정 테이블 DML |
| 테이블 | `ALL` | 네 가지 테이블 DML 권한 |
| 서버 디렉터리 | [`READ ON DIRECTORY`](#dfq-파일-읽기) | DFQ로 해당 디렉터리와 하위 디렉터리의 로컬 파일 읽기 |
| 원격 엔드포인트 | [`READ ON ENDPOINT`](#dfq-파일-읽기) | 허용된 접속 주소와 인증 출처로 DFQ 원격 파일 읽기 |

데이터베이스의 `ALL`은 테이블 DML이나 `MOUNT`를 포함하지 않습니다. 테이블의 `ALL`도 데이터베이스
관리 권한을 포함하지 않습니다. 권한이 있어도 해당 테이블 타입이 지원하지 않는 DML은 실행할
수 없습니다. 예를 들어 LOG 테이블은 `UPDATE`를 지원하지 않습니다. DFQ의 `READ` 권한은
`ALL`에 포함되지 않으며 디렉터리나 엔드포인트별로 부여합니다.

<a id="grant-revoke"></a>

## GRANT / REVOKE

```sql
GRANT privilege_list ON target TO user_name;
REVOKE privilege_list ON target FROM user_name;
```

다음 예제는 사용자에게 데이터베이스 연결과 한 테이블의 읽기·쓰기를 허용합니다.

```sql
GRANT CONNECT ON DATABASE factory_a TO app_user;
GRANT SELECT, INSERT ON TABLE factory_a.sys.sensor_log TO app_user;

REVOKE INSERT ON TABLE factory_a.sys.sensor_log FROM app_user;
REVOKE CONNECT ON DATABASE factory_a FROM app_user;
```

테이블은 현재 데이터베이스의 `owner.table` 또는 `database.owner.table`로 지정할 수 있습니다.
데이터베이스 전체에 `SELECT` 같은 DML 권한을 주는 구문은 지원하지 않습니다.

데이터베이스와 테이블의 권한 기록은 `M$SYS_USER_ACCESS`에서 확인합니다.
DFQ 권한의 부여와 회수는 [DFQ 파일 읽기](#dfq-파일-읽기)를 참고합니다.

```sql
SELECT DB_NAME, USER_NAME, OWNER_NAME, TABLE_NAME, PRIV
  FROM M$SYS_USER_ACCESS
 WHERE USER_NAME = 'APP_USER'
 ORDER BY DB_NAME, OWNER_NAME, TABLE_NAME;
```

`OWNER_NAME`과 `TABLE_NAME`이 `NULL`이면 데이터베이스 범위, 값이 있으면 테이블 범위의
기록입니다. `PRIV`는 복수 권한을 표현하는 비트 마스크이므로 화면에 나온 숫자 하나를 권한명
하나로 해석하거나 운영 스크립트에 고정하지 마십시오.

<a id="database-privileges"></a>

## 데이터베이스 권한

논리 데이터베이스는 사용자를 만든 것만으로 연결할 수 없습니다. 대상 데이터베이스에 `CONNECT`를
명시적으로 부여하고 필요한 관리 권한을 최소 단위로 추가합니다.

```sql
GRANT CONNECT ON DATABASE factory_a TO deploy_user;
GRANT DDL ON DATABASE factory_a TO deploy_user;
GRANT ALTER ON DATABASE factory_a TO deploy_user;
```

새 사용자에게 기본으로 기록되는 호환 권한은 기본 데이터베이스인 `MACHBASEDB` 범위입니다.
다른 논리 데이터베이스까지 자동으로 확장되지 않습니다.

<a id="select-insert-delete-update"></a>
<a id="database-privileges-select-insert-delete-update"></a>

### SELECT / INSERT / DELETE / UPDATE

DML 권한은 특정 테이블을 대상으로 부여합니다.

```sql
GRANT SELECT ON sys.sensor_log TO reader_user;
GRANT INSERT ON sys.sensor_log TO writer_user;
GRANT DELETE ON sys.device_config TO maint_user;
GRANT UPDATE ON sys.device_config TO maint_user;
```

`DELETE`와 `UPDATE`를 부여하기 전에는 대상 테이블 타입의 조건 제약을 함께 검토합니다.
TAG 데이터 변경은 태그와 시간 조건이 필요하고, VOLATILE 변경은 기본 키 조건이 필요합니다.

<a id="create-drop"></a>
<a id="database-privileges-create-drop"></a>

### CREATE / DROP

```sql
GRANT CREATE ON DATABASE factory_a TO deploy_user;
GRANT DROP ON DATABASE factory_a TO deploy_user;
```

`DROP`은 복구하기 어려운 변경을 허용하므로, 단순 적재·조회 계정에는 부여하지 마십시오.
객체 소유권만으로 다른 데이터베이스에 접속할 수 있는 것은 아닙니다.

<a id="database-privileges-alter"></a>

### ALTER

```sql
GRANT ALTER ON DATABASE factory_a TO deploy_user;
```

`ALTER`는 테이블 구조와 운영 설정 변경에 영향을 줄 수 있습니다. 애플리케이션 계정과 분리한
배포·운영 계정에만 부여하고, 변경 후 현재 설정과 스키마를 다시 조회하십시오.

<a id="database-privileges-backup"></a>

### BACKUP

```sql
GRANT BACKUP ON DATABASE factory_a TO backup_user;
```

백업 경로에 대한 Machbase 서버 프로세스 OS 계정의 쓰기 권한과 여유 공간은 SQL 권한과
별도로 필요합니다. 백업용 DB 사용자에는 DML이나 DDL 권한을 함께 주지 않는 구성을 권장합니다.

<a id="database-privileges-mount"></a>

### MOUNT

```sql
GRANT MOUNT ON DATABASE MACHBASEDB TO recovery_user;
```

MOUNT/UMOUNT는 관리 작업입니다. 마운트된 데이터베이스를 탐색할 `USAGE`와 그 안의 테이블을
읽을 `SELECT`는 별도 권한입니다. 실제 복구 절차는
[백업, 복구, 마운트](/dbms-8.9/operations-configuration-recovery/backup-restore-mount/)를 따르십시오.

<a id="privileges-ddl-all"></a>
<a id="database-privileges-privileges-ddl-all"></a>

### DDL / ALL 합성 권한

```sql
-- CREATE + DROP
GRANT DDL ON DATABASE factory_a TO deploy_user;

-- active database의 CONNECT, CREATE, DROP, ALTER, BACKUP
GRANT ALL ON DATABASE factory_a TO database_admin;

-- 한 테이블의 SELECT, INSERT, DELETE, UPDATE
GRANT ALL ON TABLE factory_a.sys.sensor_log TO table_admin;
```

합성 권한은 편리하지만 최소 권한 검토를 어렵게 할 수 있습니다. 자동화 계정에는 가능한 한
개별 권한을 부여하십시오.

<a id="privileges-grant-exclude"></a>

## 기본 부여 권한과 제외 권한

새 사용자는 기본 데이터베이스 `MACHBASEDB`에서 `CONNECT`, `CREATE`, `DROP`을 기본
보유합니다. 읽기 전용 계정에는 SYS가 `REVOKE DDL ON DATABASE MACHBASEDB FROM app_user;`로
기본 생성·삭제 권한을 회수합니다. 다른 사용자의 테이블에 접근하려면 테이블 권한을
별도로 부여합니다. 다른 논리 데이터베이스에는 다음처럼 필요한 범위를 지정합니다.

```sql
GRANT CONNECT ON DATABASE factory_a TO app_user;
GRANT SELECT, INSERT ON TABLE factory_a.sys.sensor_log TO app_user;
```

`ALTER`, `BACKUP`, `MOUNT`, `USAGE`와 DFQ의 `READ`는 업무에 필요한 범위를 지정해
별도로 부여합니다.

<a id="privileges-2"></a>

## 테이블 권한

테이블 권한은 반드시 대상 객체와 함께 관리합니다.

```sql
GRANT SELECT ON TABLE factory_a.sys.sensor_log TO reader_user;
GRANT SELECT, INSERT ON TABLE factory_a.sys.sensor_log TO ingest_user;

REVOKE INSERT ON TABLE factory_a.sys.sensor_log FROM ingest_user;
```

테이블을 삭제할 때 기존 테이블 grant도 정리되며, 같은 이름으로 만든 새 객체에 승계되지
않습니다. 필요한 권한을 다시 부여한 뒤 `M$SYS_USER_ACCESS`에서 확인하십시오.

<a id="checklist-diagnosis-privileges"></a>

## 권한 진단 체크리스트

사용자와 권한 현황을 다음 순서로 검토합니다.

```sql
SELECT USER_ID, NAME, PWD_POLICY_LEVEL, VALID_BEFORE
  FROM M$SYS_USERS
 ORDER BY USER_ID;

SELECT DB_NAME, USER_NAME, OWNER_NAME, TABLE_NAME, PRIV
  FROM M$SYS_USER_ACCESS
 ORDER BY USER_NAME, DB_NAME, OWNER_NAME, TABLE_NAME;
```

- 사용하지 않는 계정이 남아 있지 않은지 확인합니다.
- 읽기 계정에 쓰기·DDL·관리 권한이 없는지 확인합니다.
- 임시 권한은 승인된 기간이 끝나면 `REVOKE`하고 결과를 다시 조회합니다.
- 사용자를 삭제하기 전 소유 객체와 실행 중인 세션을 확인합니다.
- 숫자 `PRIV`를 해석해야 하는 감사 도구는 사용 중인 버전의 권한 정의와 함께 검증합니다.
- DFQ 권한은 [실행 계정으로 읽기 결과](#dfq-권한-확인)를 확인합니다.

## DFQ 파일 읽기

Standard Edition에서 SYS가 현재 데이터베이스의 사용자에게 DFQ 권한을 부여합니다.
조회할 데이터베이스에서 사용자의 `CONNECT` 권한과 읽을 위치의 `READ` 권한을 확인합니다.
같은 사용자에게 다른 데이터베이스에서 조회를 허용하려면 그 데이터베이스에서도 부여합니다.

### 대상을 선택하고 권한을 부여합니다

| 읽을 대상 | 필요한 권한 | 함께 확인할 항목 |
|---|---|---|
| 서버 로컬 경로 또는 `file://` URI | `READ ON DIRECTORY` | 파일을 포함하는 실제 서버 절대 디렉터리와 서버 OS 계정의 읽기 권한 |
| 공개·익명 원격 파일 또는 사전 서명 HTTPS URL | 인증 절을 생략한 `READ ON ENDPOINT` | 실제 스킴·호스트·포트 |
| AWS 공유 파일 프로필로 서명하는 S3 객체 | `READ ON ENDPOINT … PROFILE '이름'` | 변환된 HTTP(S) 주소와 사용한 프로필 |
| 서버 환경변수 키로 서명하는 S3 객체 | `READ ON ENDPOINT … USING ENVIRONMENT` | 변환된 HTTP(S) 주소와 환경 키 사용 여부 |
| 서버 .netrc 계정으로 읽는 FTP(S) | `READ ON ENDPOINT … USING NETRC` | 실제 FTP(S) 주소와 호스트에 대응하는 계정 |

[12.12 실습](/kr/dbms-8.9/dfq/remote-read/)의 파일과 `DFQ_REMOTE_LAB` 계정이
준비된 경우, SYS는 다음처럼 로컬 파일과 공개 HTTP 파일을 허용합니다.

```sql
GRANT READ ON DIRECTORY '/tmp/dfq-read-lab/files' TO DFQ_REMOTE_LAB;
GRANT READ ON ENDPOINT 'http://127.0.0.1:18080' TO DFQ_REMOTE_LAB;
```

S3에는 `s3://` 문자열을 변환한 접속 주소를 사용합니다. 버킷이 호스트에 붙는
virtual 방식에서는 버킷이 포함된 호스트가 권한 대상입니다. 같은 endpoint의
`PROFILE`과 `USING ENVIRONMENT`는 별도 권한입니다. 경로·와일드카드를 붙여
endpoint 권한의 범위를 좁힐 수 없으므로 공개할 파일 범위는 원격 서버에서도 설정합니다.
[인증 출처별 GRANT·REVOKE 예제](/kr/dbms-8.9/dfq/operations/#endpoint-read-permissions)를 참고합니다.

### VIEW 사용과 권한 회수

일반 사용자가 DFQ를 포함한 VIEW를 조회하려면 VIEW의 `SELECT`와 원본의 `READ`를 모두
부여합니다. 중첩 VIEW에서도 원본 파일 권한은 실제 실행 사용자로 검사합니다.
redirect가 있으면 최종 주소뿐 아니라 접속하는 각 주소에 대한 권한이 필요합니다.

위 실습의 공개 HTTP 권한은 다음과 같이 회수합니다.

```sql
REVOKE READ ON ENDPOINT 'http://127.0.0.1:18080' FROM DFQ_REMOTE_LAB;
```

인증 절을 써서 부여한 권한은 회수할 때도 같은 절과 프로필을 지정합니다. 다음 실행부터
회수한 권한을 적용하며, 이미 준비한 SQL을 다시 실행할 때도 권한을 검사합니다.
실행 중인 조회를 중지하려면 [세션 취소](/kr/dbms-8.9/dfq/operations/#remote-read-spool)를 사용합니다.

### DFQ 권한 확인 {#dfq-권한-확인}

`M$SYS_USER_ACCESS`는 데이터베이스·테이블 권한을 표시합니다. DFQ는 권한을 부여한
데이터베이스에 대상 사용자로 접속해 같은 READ를 실행하여 확인합니다.

1. 허용한 경로 또는 URI에서 예상 행을 조회하는지 확인합니다. VIEW를 사용하는 경우
   같은 실행 계정으로 VIEW도 조회합니다.
2. 권한을 회수한 뒤 같은 SQL을 다시 실행해 `ACCESS_DENIED`를 확인합니다.
3. 승인한 주소에서 거부되면 현재 데이터베이스, URI 변환 후의 호스트·포트, 실제 인증
   출처, redirect 목적지 순서로 대조합니다. 로컬 경로는 서버 OS 권한도 확인합니다.

[DIRECTORY 권한 문법](/kr/dbms-8.9/reference/sql/syntax/user-auth-syntax/#서버-디렉터리-read-권한)과
[ENDPOINT 권한 문법](/kr/dbms-8.9/reference/sql/syntax/user-auth-syntax/#read-on-endpoint)을 참고합니다.
