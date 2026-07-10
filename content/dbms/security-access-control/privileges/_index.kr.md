---
type: docs
title: '14.3 권한 관리'
weight: 30
toc: true
---
각 사용자가 수행할 수 있는 작업을 제어하는 핵심 보안 기능입니다.

## 권한의 두 가지 종류

Machbase 권한은 적용 범위에 따라 두 가지로 나뉩니다.

| 종류 | 설명 | 예시 |
|---|---|---|
| 데이터베이스 권한 | DB 전체 범위에서 DDL 및 관리 작업 허용 | 테이블 생성, 백업 실행 |
| 테이블 권한 | 특정 테이블에 대한 DML 작업 허용 | 특정 테이블 조회·삽입 |

데이터베이스 권한은 `GRANT ... ON MACHBASEDB TO user` 구문으로 부여하고,
테이블 권한은 `GRANT ... ON schema.table TO user` 구문으로 부여합니다.

## GRANT / REVOKE 명령어 개요

```sql
-- 데이터베이스 권한 부여
GRANT CREATE ON machbasedb TO app_user;

-- 테이블 권한 부여
GRANT SELECT ON sys.sensor_log TO reader_user;

-- 권한 취소
REVOKE SELECT ON sys.sensor_log FROM reader_user;
```

자세한 문법과 예제는 다음 하위 섹션을 참고하십시오.

- [권한 모델](/dbms/security-access-control/privileges/#privileges) — 권한 계층 구조와 전체 권한 목록
- [GRANT / REVOKE](/dbms/security-access-control/privileges/#grant-revoke) — 권한 부여·취소 구문 상세
- [데이터베이스 권한](/dbms/security-access-control/privileges/#database-privileges) — 데이터베이스 범위 권한 각각의 설명
- [테이블 권한](/dbms/security-access-control/privileges/#privileges-2) — 특정 테이블 대상 세밀한 권한 제어
- [기본 부여 권한과 제외 권한](/dbms/security-access-control/privileges/#privileges-grant-exclude) — 신규 사용자의 초기 권한 범위
- [LOOKUP UPDATE/DELETE 권한 모델](/dbms/lookup-table-usage/privilege-predicate-performance/#privileges-lookup-update-delete-target-select) — Primary key 기반 DML 권한 동작
- [권한 진단 체크리스트](/dbms/security-access-control/privileges/#checklist-diagnosis-privileges) — 권한 현황 조회 및 감사 방법


<a id="privileges"></a>

## 권한 모델

### 권한 계층 구조

Machbase의 권한 모델은 다음과 같은 구조를 가집니다.

```
SYS 계정 (슈퍼유저)
  └─ 모든 권한 보유, 별도 GRANT 불필요
  └─ 다른 사용자에게 권한 부여 가능

일반 사용자
  ├─ 데이터베이스 권한 (DB 전체 범위)
  │    SELECT, INSERT, DELETE, UPDATE, CREATE, DROP, ALTER, BACKUP, MOUNT, DDL, ALL
  └─ 테이블 권한 (특정 테이블 범위)
       SELECT, INSERT, DELETE, UPDATE, ALL
```

SYS 계정은 모든 권한을 기본으로 보유하므로 별도로 GRANT를 실행할 필요가 없습니다.
일반 사용자는 SYS 계정 또는 충분한 권한을 가진 관리자로부터 권한을 부여받아야 합니다.

### 데이터베이스 권한 목록

`MACHBASEDB`를 대상으로 부여하는 DB 전체 범위 권한입니다.

| 권한 | 허용하는 작업 |
|---|---|
| `CREATE` | 테이블, 뷰, 인덱스, 롤업, 테이블스페이스, 리텐션 생성 |
| `DROP` | 테이블, 뷰, 인덱스, 롤업, 테이블스페이스, 리텐션 삭제 |
| `ALTER` | 테이블 구조 변경, `ALTER SYSTEM` 실행 |
| `BACKUP` | `BACKUP DATABASE` 실행 |
| `MOUNT` | `MOUNT DATABASE` / `UMOUNT DATABASE` 실행 |
| `DDL` | CREATE + DROP 묶음 (두 권한 동시 부여) |
| `ALL` | SELECT, INSERT, DELETE, UPDATE, CREATE, DROP, ALTER, BACKUP, MOUNT 일괄 부여 |

`GRANT ALL ON MACHBASEDB`는 DML 권한 비트도 함께 부여하지만,
`GRANT SELECT ON MACHBASEDB`처럼 DML 권한만 개별로 DB 대상에 부여하는 구문은
지원되지 않습니다. 다른 사용자 소유 테이블에 접근하려면 테이블 대상 GRANT가 필요합니다.

### 테이블 권한 목록

특정 테이블을 대상으로 부여하는 DML 범위 권한입니다.

| 권한 | 허용하는 작업 | 비고 |
|---|---|---|
| `SELECT` | 해당 테이블 조회 | 모든 테이블 유형 지원 |
| `INSERT` | 해당 테이블에 행 삽입 | 모든 테이블 유형 지원 |
| `DELETE` | 해당 테이블에서 행 삭제 | 모든 테이블 유형 지원 |
| `UPDATE` | 해당 테이블의 행 수정 | TAG는 태그/시간 조건 필요. LOG 미지원 |
| `ALL` | SELECT + INSERT + DELETE + UPDATE 일괄 부여 | |

### ALL의 의미

`ALL`은 대상에 따라 의미가 다릅니다.

```sql
-- 데이터베이스 ALL 권한
GRANT ALL ON machbasedb TO admin_user;

-- 테이블 DML 권한 전체 (SELECT, INSERT, DELETE, UPDATE)
GRANT ALL ON sys.sensor_log TO app_user;
```

대상이 `MACHBASEDB`이면 SELECT, INSERT, DELETE, UPDATE, CREATE, DROP, MOUNT,
BACKUP, ALTER 권한 비트를 일괄 부여하고, 특정 테이블이면 해당 테이블의 DML 권한
전체를 의미합니다.

### 신규 사용자의 기본 권한

`CREATE USER`로 생성된 사용자는 다음 권한을 기본으로 가집니다.

| 기본 보유 | 기본 미보유 (명시적 부여 필요) |
|---|---|
| SELECT, INSERT, DELETE, UPDATE, CREATE, DROP | ALTER, BACKUP, MOUNT |

자신이 생성한 객체(테이블, 뷰 등)에 대해서는 소유자로서 모든 작업이 허용됩니다.
다른 사용자 소유의 객체에 접근하려면 SYS 계정이 명시적으로 GRANT를 실행해야 합니다.

### 권한과 테이블 유형 제약

권한이 있어도 테이블 유형이 지원하지 않는 DML은 실행할 수 없습니다.

- `LOG` 테이블은 `UPDATE`를 지원하지 않습니다.
- `TAG` 테이블의 data UPDATE는 태그 선택 조건과 BASETIME 조건이 필요합니다.
- `VOLATILE`, `LOOKUP` 테이블의 `DELETE`/`UPDATE`는 기본키 기반 `WHERE` 조건이 필요합니다.

권한을 부여한다고 해서 지원하지 않는 DML이 허용되는 것은 아닙니다.

<a id="grant-revoke"></a>

## GRANT / REVOKE

`GRANT` 문으로 사용자에게 권한을 부여하고, `REVOKE` 문으로 이미 부여된 권한을 취소합니다.
두 명령 모두 SYS 계정에서 실행합니다.

### 문법

```sql
-- 권한 부여
GRANT privilege_list ON target TO user_name;

-- 권한 취소
REVOKE privilege_list ON target FROM user_name;
```

- `privilege_list`: 쉼표로 구분된 하나 이상의 권한명
- `target`: `MACHBASEDB` (데이터베이스 권한) 또는 `[schema.]table_name` (테이블 권한)
- `user_name`: 대상 사용자명 (대소문자 무관, 내부적으로 대문자 처리)

### 데이터베이스 권한 부여

`MACHBASEDB`를 대상으로 DDL 및 관리 권한을 부여합니다.

```sql
-- 테이블·뷰·인덱스 생성 권한
GRANT CREATE ON machbasedb TO app_user;

-- 테이블·뷰·인덱스 삭제 권한
GRANT DROP ON machbasedb TO app_user;

-- CREATE + DROP 묶음 (DDL 권한)
GRANT DDL ON machbasedb TO deploy_user;

-- 테이블 구조 변경 및 ALTER SYSTEM 권한
GRANT ALTER ON machbasedb TO ops_user;

-- 백업 실행 권한
GRANT BACKUP ON machbasedb TO backup_user;

-- 마운트/언마운트 권한
GRANT MOUNT ON machbasedb TO mount_user;

-- 모든 데이터베이스 권한 일괄 부여
GRANT ALL ON machbasedb TO admin_user;
```

### 테이블 권한 부여

특정 테이블에 대한 DML 권한을 부여합니다.

```sql
-- 단일 권한 부여
GRANT SELECT ON sensor_log TO app_user;
GRANT INSERT ON sensor_log TO writer_user;

-- 여러 권한 동시 부여
GRANT SELECT, INSERT ON sensor_tag TO iot_user;

-- 스키마 지정
GRANT SELECT ON sys.sensor_log TO reader_user;

-- DB명·스키마명·테이블명 모두 지정
GRANT SELECT ON machbasedb.sys.sensor_log TO reader_user;

-- 테이블의 모든 DML 권한 부여
GRANT ALL ON sensor_log TO app_user;
```

### 권한 취소

```sql
-- 테이블 권한 일부 취소
REVOKE SELECT ON sensor_log FROM app_user;
REVOKE INSERT ON sensor_log FROM writer_user;

-- 테이블 권한 전체 취소
REVOKE ALL ON sensor_log FROM app_user;

-- 데이터베이스 권한 취소
REVOKE BACKUP ON machbasedb FROM backup_user;
REVOKE ALL ON machbasedb FROM admin_user;
```

### 주의 사항

- `GRANT SELECT ON machbasedb TO user` 형식으로 DML 권한을 데이터베이스 전체에 부여하는 것은 지원하지 않습니다. DML 권한은 반드시 특정 테이블을 지정해야 합니다.
- 데이터베이스 권한 대상 이름은 반드시 `MACHBASEDB`를 사용합니다. 다른 이름을 지정하면 `[ERR-02186: Invalid database name.]` 오류가 발생합니다.
- SYS 계정은 모든 권한을 기본으로 보유하므로 별도 GRANT가 필요 없습니다.

### 현재 권한 확인

```sql
-- 데이터베이스 권한 확인
SELECT * FROM m$sys_privileges;

-- 특정 사용자의 데이터베이스 권한 확인
SELECT * FROM m$sys_privileges WHERE grantee = 'APP_USER';

-- 테이블 권한 확인
SELECT * FROM m$obj_privileges;

-- 특정 테이블의 권한 부여 현황 확인
SELECT * FROM m$obj_privileges WHERE obj_name = 'SENSOR_LOG';
```

<a id="database-privileges"></a>

## 데이터베이스 권한

데이터베이스 권한은 `MACHBASEDB` 전체 범위에 적용되는 권한입니다. 개별 DML 권한은
테이블 대상으로 부여하지만, `ALL ON MACHBASEDB`는 DML 권한 비트까지 함께 포함합니다.

### 데이터베이스 권한 목록

| 권한 | 허용하는 작업 | 기본 보유 |
|---|---|---|
| `CREATE` | 테이블, 뷰, 인덱스, 롤업, 테이블스페이스, 리텐션 생성 | 예 |
| `DROP` | 테이블, 뷰, 인덱스, 롤업, 테이블스페이스, 리텐션 삭제 | 예 |
| `ALTER` | 테이블 구조 변경, `ALTER SYSTEM` 실행 | 아니오 |
| `BACKUP` | `BACKUP DATABASE` 실행 | 아니오 |
| `MOUNT` | `MOUNT DATABASE` / `UMOUNT DATABASE` 실행 | 아니오 |
| `DDL` | CREATE + DROP 묶음 | — |
| `ALL` | SELECT, INSERT, DELETE, UPDATE, CREATE, DROP, ALTER, BACKUP, MOUNT 일괄 부여 | — |

"기본 보유"가 "예"인 권한은 `CREATE USER`로 생성된 사용자가 별도 GRANT 없이 보유합니다.
나머지 권한은 SYS 계정이 명시적으로 부여해야 합니다.

### 권한이 필요한 주요 작업

다음 작업은 테이블 권한이 아닌 데이터베이스 권한이 필요합니다.

| 작업 | 필요한 권한 |
|---|---|
| `CREATE TABLE` / `DROP TABLE` | CREATE / DROP |
| `CREATE VIEW` / `DROP VIEW` | CREATE / DROP |
| `CREATE INDEX` / `DROP INDEX` | CREATE / DROP |
| `CREATE ROLLUP` / `DROP ROLLUP` | CREATE / DROP |
| `CREATE TABLESPACE` / `DROP TABLESPACE` | CREATE / DROP |
| `CREATE RETENTION` / `DROP RETENTION` | CREATE / DROP |
| `ALTER TABLE` (컬럼 추가/삭제 등) | ALTER |
| `ALTER SYSTEM` | ALTER |
| `BACKUP DATABASE` | BACKUP |
| `MOUNT DATABASE` / `UMOUNT DATABASE` | MOUNT |

### 부여 예제

```sql
-- deploy_user에게 DDL 권한 부여
GRANT DDL ON machbasedb TO deploy_user;

-- ops_user에게 ALTER 권한 부여
GRANT ALTER ON machbasedb TO ops_user;

-- backup_user에게 BACKUP 권한 부여
GRANT BACKUP ON machbasedb TO backup_user;

-- admin_user에게 모든 데이터베이스 권한 부여
GRANT ALL ON machbasedb TO admin_user;
```

### 하위 섹션

각 권한의 상세 설명과 사용 예제는 다음 페이지를 참고하십시오.

- [SELECT / INSERT / DELETE / UPDATE](/dbms/security-access-control/privileges/#select-insert-delete-update)
- [CREATE / DROP](/dbms/security-access-control/privileges/#create-drop)
- [ALTER](/dbms/security-access-control/privileges/#alter)
- [BACKUP](/dbms/security-access-control/privileges/#backup)
- [MOUNT](/dbms/security-access-control/privileges/#mount)
- [DDL / ALL 합성 권한](/dbms/security-access-control/privileges/#privileges-ddl-all)

<a id="select-insert-delete-update"></a>
<a id="database-privileges-select-insert-delete-update"></a>

### SELECT / INSERT / DELETE / UPDATE

`SELECT`, `INSERT`, `DELETE`, `UPDATE`는 데이터 조작 언어(DML) 권한입니다.
신규 사용자는 이 네 가지 권한을 기본으로 보유합니다.

#### 데이터베이스 권한으로서의 DML

Machbase에서는 DML 권한을 데이터베이스 전체 범위(`MACHBASEDB`)로 부여할 수 없습니다.
DML 권한은 반드시 특정 테이블을 대상으로 부여해야 합니다.

```sql
-- 올바른 방법: 특정 테이블에 SELECT 부여
GRANT SELECT ON sys.sensor_log TO reader_user;

-- 지원하지 않는 방법: MACHBASEDB에 SELECT 부여 (오류 발생)
GRANT SELECT ON machbasedb TO reader_user;
-- [ERR-02186: Invalid database name.]
```

테이블별로 세밀하게 권한을 제어하려면 [테이블 권한](/dbms/security-access-control/privileges/#privileges-2)을 참고하십시오.

#### 각 DML 권한 설명

##### SELECT

데이터를 조회하는 권한입니다. 모든 테이블 유형에서 지원합니다.

```sql
-- 특정 테이블 조회 권한 부여
GRANT SELECT ON sys.sensor_log TO reader_user;

-- 권한 취소
REVOKE SELECT ON sys.sensor_log FROM reader_user;
```

##### INSERT

테이블에 새 행을 삽입하는 권한입니다. 모든 테이블 유형에서 지원합니다.

```sql
-- 특정 테이블 삽입 권한 부여
GRANT INSERT ON sys.sensor_log TO writer_user;

-- 권한 취소
REVOKE INSERT ON sys.sensor_log FROM writer_user;
```

##### DELETE

테이블에서 행을 삭제하는 권한입니다. 모든 테이블 유형에서 지원합니다.

```sql
-- 특정 테이블 삭제 권한 부여
GRANT DELETE ON sys.sensor_log TO manager_user;

-- 권한 취소
REVOKE DELETE ON sys.sensor_log FROM manager_user;
```

##### UPDATE

테이블의 행을 수정하는 권한입니다.

```sql
-- VOLATILE/LOOKUP 테이블에 UPDATE 권한 부여
GRANT UPDATE ON sys.device_config TO ops_user;

-- 권한 취소
REVOKE UPDATE ON sys.device_config FROM ops_user;
```

**UPDATE 권한과 테이블 유형 제약:**

| 테이블 유형 | UPDATE 지원 여부 |
|---|---|
| LOG | 미지원 |
| TAG | 지원 (태그/시간 조건 필요) |
| VOLATILE | 지원 (기본키 기반 WHERE 조건 필요) |
| LOOKUP | 지원 (기본키 기반 WHERE 조건 필요) |

UPDATE 권한을 부여하더라도 LOG 테이블에서는 UPDATE를 실행할 수 없습니다. TAG 테이블의
data UPDATE는 태그 선택 조건과 시간 조건을 만족해야 하며, `name`, `time`, 메타데이터 컬럼은
data UPDATE의 SET 대상이 아닙니다.

#### 복합 DML 권한 부여

여러 DML 권한을 한 번에 부여하려면 테이블 권한을 사용합니다.

```sql
-- 조회와 삽입을 함께 허용
GRANT SELECT, INSERT ON sys.sensor_log TO iot_user;

-- 조회, 삽입, 삭제를 함께 허용
GRANT SELECT, INSERT, DELETE ON sys.sensor_log TO app_user;

-- 해당 테이블의 모든 DML 권한 부여
GRANT ALL ON sys.sensor_log TO app_user;
```

<a id="create-drop"></a>
<a id="database-privileges-create-drop"></a>

### CREATE / DROP

`CREATE` 권한과 `DROP` 권한은 데이터베이스 객체(테이블, 뷰, 인덱스 등)를 생성하고 삭제하는 권한입니다.
`CREATE USER`로 생성된 사용자는 이 두 권한을 기본으로 보유합니다.

#### CREATE 권한

`CREATE` 권한이 있는 사용자는 다음 객체를 생성할 수 있습니다.

- 테이블 (`CREATE TABLE`)
- 뷰 (`CREATE VIEW`)
- 인덱스 (`CREATE INDEX`)
- 롤업 (`CREATE ROLLUP`)
- 테이블스페이스 (`CREATE TABLESPACE`)
- 리텐션 (`CREATE RETENTION`)

```sql
-- app_user에게 CREATE 권한 부여
GRANT CREATE ON machbasedb TO app_user;

-- CREATE 권한 취소
REVOKE CREATE ON machbasedb FROM app_user;
```

#### DROP 권한

`DROP` 권한이 있는 사용자는 다음 객체를 삭제할 수 있습니다.

- 테이블 (`DROP TABLE`)
- 뷰 (`DROP VIEW`)
- 인덱스 (`DROP INDEX`)
- 롤업 (`DROP ROLLUP`)
- 테이블스페이스 (`DROP TABLESPACE`)
- 리텐션 (`DROP RETENTION`)

```sql
-- app_user에게 DROP 권한 부여
GRANT DROP ON machbasedb TO app_user;

-- DROP 권한 취소
REVOKE DROP ON machbasedb FROM app_user;
```

#### 소유자의 DROP 권한

자신이 생성한 객체는 별도의 `DROP` 권한 없이도 삭제할 수 있습니다.
단, 다른 사용자가 소유한 객체를 삭제하려면 반드시 `DROP` 권한이 필요합니다.

```sql
-- app_user가 자신의 테이블을 삭제하는 경우 (DROP 권한 불필요)
-- app_user 세션에서 실행
DROP TABLE my_table;

-- ops_user가 다른 사용자 소유 테이블을 삭제하려면 DROP 권한 필요
-- SYS 계정에서 권한 부여
GRANT DROP ON machbasedb TO ops_user;
```

#### CREATE + DROP 동시 부여

두 권한을 함께 부여하려면 `DDL` 권한을 사용합니다.

```sql
-- CREATE + DROP을 한 번에 부여
GRANT DDL ON machbasedb TO deploy_user;

-- 개별 부여와 동일한 효과
GRANT CREATE ON machbasedb TO deploy_user;
GRANT DROP ON machbasedb TO deploy_user;
```

`DDL` 합성 권한에 대한 자세한 내용은 [DDL / ALL 합성 권한](/dbms/security-access-control/privileges/#database-privileges-privileges-ddl-all)을 참고하십시오.

<a id="database-privileges-alter"></a>

### ALTER

`ALTER` 권한은 테이블 구조 변경과 시스템 수준의 설정 변경을 허용하는 권한입니다.
신규 사용자 생성 시 기본으로 부여되지 않으므로 필요할 때 명시적으로 GRANT해야 합니다.

#### 허용하는 작업

`ALTER` 권한이 있는 사용자는 다음을 실행할 수 있습니다.

- `ALTER TABLE` — 테이블 구조 변경 (컬럼 추가, 컬럼 삭제, 데이터 타입 변경 등)
- `ALTER SYSTEM` — 시스템 설정 변경 및 관리 명령

#### 권한 부여 예제

```sql
-- ops_user에게 ALTER 권한 부여
GRANT ALTER ON machbasedb TO ops_user;

-- ALTER 권한 취소
REVOKE ALTER ON machbasedb FROM ops_user;
```

#### ALTER TABLE 사용 예

```sql
-- ops_user 세션에서 컬럼 추가 (ALTER 권한 필요)
ALTER TABLE sensor_log ADD COLUMN (location VARCHAR(64));

-- 컬럼 삭제
ALTER TABLE sensor_log DROP COLUMN (location);
```

#### SYS 전용 작업

다음 작업은 `ALTER` 권한이 있어도 SYS 계정에서만 실행할 수 있습니다.

- `ALTER ROLLUP` — 롤업 정책 변경
- 일부 `ALTER SYSTEM` 하위 명령 중 SYS 전용 항목

운영 환경에서는 `ALTER` 권한을 DBA나 운영 담당자에게만 부여하고, 일반 애플리케이션 계정에는 부여하지 않도록 권장합니다.

<a id="database-privileges-backup"></a>

### BACKUP

`BACKUP` 권한은 `BACKUP DATABASE` 명령을 실행하는 권한입니다.
신규 사용자 생성 시 기본으로 부여되지 않으므로 필요할 때 명시적으로 GRANT해야 합니다.

#### 허용하는 작업

`BACKUP` 권한이 있는 사용자는 다음 명령을 실행할 수 있습니다.

- `BACKUP DATABASE` — 데이터베이스 전체 또는 증분 백업

SYS 계정은 별도 권한 없이 백업을 실행할 수 있습니다.

#### 권한 부여 예제

```sql
-- backup_user에게 BACKUP 권한 부여
GRANT BACKUP ON machbasedb TO backup_user;

-- BACKUP 권한 취소
REVOKE BACKUP ON machbasedb FROM backup_user;
```

#### BACKUP DATABASE 실행 예

```sql
-- backup_user 세션에서 실행
BACKUP DATABASE INTO DISK = '/backup/machbase_backup';

-- 증분 백업
BACKUP DATABASE LEVEL 1 INTO DISK = '/backup/machbase_inc_backup';
```

#### 권한 없을 때의 오류

`BACKUP` 권한이 없는 사용자가 `BACKUP DATABASE`를 실행하면 권한 오류가 발생합니다.

```sql
-- 권한 없는 사용자가 실행할 경우
BACKUP DATABASE INTO DISK = '/backup/test';
-- [ERR-02xxx: Not enough privilege to execute BACKUP DATABASE.]
```

#### 운영 지침

- 백업 전용 계정을 별도로 생성하고 `BACKUP` 권한만 부여하는 것을 권장합니다.
- 백업 계정은 필요한 파일 시스템 경로에 대한 OS 수준 쓰기 권한도 함께 필요합니다.
- 정기 백업 스크립트는 전용 백업 계정으로 실행하여 SYS 계정 자격증명 노출을 최소화합니다.

<a id="database-privileges-mount"></a>

### MOUNT

`MOUNT` 권한은 `MOUNT DATABASE` 및 `UMOUNT DATABASE` 명령을 실행하는 권한입니다.
신규 사용자 생성 시 기본으로 부여되지 않으므로 필요할 때 명시적으로 GRANT해야 합니다.

#### 허용하는 작업

`MOUNT` 권한이 있는 사용자는 다음 명령을 실행할 수 있습니다.

- `MOUNT DATABASE` — 백업 또는 외부 데이터베이스를 읽기 전용으로 마운트
- `UMOUNT DATABASE` — 마운트된 데이터베이스를 해제

SYS 계정은 별도 권한 없이 마운트/언마운트를 실행할 수 있습니다.

#### 권한 부여 예제

```sql
-- mount_user에게 MOUNT 권한 부여
GRANT MOUNT ON machbasedb TO mount_user;

-- MOUNT 권한 취소
REVOKE MOUNT ON machbasedb FROM mount_user;
```

#### MOUNT DATABASE 실행 예

```sql
-- mount_user 세션에서 실행
MOUNT DATABASE '/backup/machbase_backup' TO 'backup_db';

-- 마운트 해제
UMOUNT DATABASE 'backup_db';
```

#### 마운트된 DB 데이터 조회 권한

`MOUNT` 권한은 마운트/언마운트 명령 실행만 허용합니다.
마운트된 데이터베이스의 테이블에서 데이터를 조회하려면 해당 테이블에 대한 `SELECT` 권한이 별도로 필요합니다.

```sql
-- mount_user가 마운트된 DB 테이블을 조회하려면 SELECT도 필요
GRANT SELECT ON backup_db.sys.sensor_log TO mount_user;
```

#### 운영 지침

- 마운트 작업은 백업 검증이나 히스토리 데이터 조회 목적으로 주로 사용됩니다.
- 마운트 전용 계정을 별도로 생성하고 `MOUNT` 권한만 부여하는 것을 권장합니다.
- 마운트된 데이터베이스는 읽기 전용이므로 데이터 변경 위험 없이 안전하게 조회할 수 있습니다.

<a id="privileges-ddl-all"></a>
<a id="database-privileges-privileges-ddl-all"></a>

### DDL / ALL 합성 권한

`DDL`과 `ALL`은 여러 데이터베이스 권한을 묶어서 한 번에 부여하거나 취소하는 합성 권한입니다.

#### DDL 합성 권한

`DDL`은 `CREATE`와 `DROP`을 묶은 합성 권한입니다. 두 권한을 개별로 부여하는 것과 동일한 효과를 가집니다.

```sql
-- DDL 권한 부여 (CREATE + DROP 동시 부여)
GRANT DDL ON machbasedb TO deploy_user;

-- 개별 부여와 동일
GRANT CREATE ON machbasedb TO deploy_user;
GRANT DROP ON machbasedb TO deploy_user;
```

`DDL` 권한을 취소하면 `CREATE`와 `DROP`이 함께 취소됩니다.

```sql
-- DDL 권한 취소
REVOKE DDL ON machbasedb FROM deploy_user;
```

#### ALL 합성 권한

`ALL`은 데이터베이스 대상에서 사용할 수 있는 권한 비트를 일괄 부여합니다.
`MACHBASEDB`에 대한 `ALL`은 `SELECT`, `INSERT`, `DELETE`, `UPDATE`, `CREATE`,
`DROP`, `MOUNT`, `ALTER`, `BACKUP`을 모두 포함합니다.

```sql
-- 모든 데이터베이스 권한 일괄 부여
GRANT ALL ON machbasedb TO admin_user;

-- 모든 데이터베이스 권한 일괄 취소
REVOKE ALL ON machbasedb FROM admin_user;
```

#### ALL의 대상별 의미 차이

`ALL`은 대상에 따라 포함하는 권한이 다릅니다.

| 대상 | ALL의 의미 |
|---|---|
| `MACHBASEDB` | SELECT, INSERT, DELETE, UPDATE, CREATE, DROP, MOUNT, ALTER, BACKUP |
| 특정 테이블 | SELECT, INSERT, DELETE, UPDATE (DML 권한 전체) |

```sql
-- 데이터베이스 관리 권한 전체 부여
GRANT ALL ON machbasedb TO admin_user;

-- 특정 테이블의 DML 권한 전체 부여
GRANT ALL ON sys.sensor_log TO app_user;
```

`GRANT ALL ON MACHBASEDB`가 DML 권한 비트를 포함하더라도,
`GRANT SELECT ON MACHBASEDB`처럼 DML 권한을 개별로 DB 대상에 부여하는 구문은
지원되지 않습니다. 다른 사용자 소유 테이블 접근은 테이블 대상 `GRANT`로 제어합니다.

#### SYS 계정의 권한

SYS 계정은 모든 권한을 기본으로 보유합니다. GRANT 명령을 실행하지 않아도 모든 DDL, DML, 관리 작업을 수행할 수 있습니다.

```sql
-- SYS 계정에 권한을 부여할 필요가 없습니다.
-- GRANT ALL ON machbasedb TO SYS;  -- 불필요
```

#### 실무 활용 예제

```sql
-- 배포 자동화 계정: DDL만 허용
GRANT DDL ON machbasedb TO ci_deploy_user;

-- DBA 계정: 모든 데이터베이스 권한 부여
GRANT ALL ON machbasedb TO dba_user;

-- 특정 프로젝트 종료 후 권한 회수
REVOKE ALL ON machbasedb FROM ci_deploy_user;
```

<a id="privileges-grant-exclude"></a>

## 기본 부여 권한과 제외 권한

`CREATE USER`로 사용자를 생성하면 일부 권한이 자동으로 부여되고, 일부는 명시적으로 부여해야 합니다.

### 기본 보유 권한

신규 생성된 사용자가 별도 GRANT 없이 보유하는 권한입니다.

| 권한 | 허용 작업 |
|---|---|
| `SELECT` | 자신이 소유한 테이블 조회 |
| `INSERT` | 자신이 소유한 테이블 삽입 |
| `DELETE` | 자신이 소유한 테이블 삭제 |
| `UPDATE` | 자신이 소유한 테이블 수정 |
| `CREATE` | 테이블, 뷰, 인덱스 등 객체 생성 |
| `DROP` | 자신이 소유한 객체 삭제 |

### 기본 제외 권한 (명시적 부여 필요)

다음 권한은 기본 보유 권한에 포함되지 않습니다.

| 권한 | 부여 구문 |
|---|---|
| `ALTER` | `GRANT ALTER ON machbasedb TO user;` |
| `BACKUP` | `GRANT BACKUP ON machbasedb TO user;` |
| `MOUNT` | `GRANT MOUNT ON machbasedb TO user;` |

```sql
-- 기본 제외 권한 부여 예시
GRANT ALTER ON machbasedb TO ops_user;
GRANT BACKUP ON machbasedb TO backup_user;
GRANT MOUNT ON machbasedb TO mount_user;
```

### 객체 소유권과 권한

사용자가 직접 생성한 객체에 대해서는 해당 사용자가 소유자가 됩니다.
소유자는 별도 권한 없이 자신의 객체에 대한 모든 DML 및 DROP을 실행할 수 있습니다.

```sql
-- app_user가 생성한 테이블은 app_user가 소유자
-- app_user 세션에서 아래 작업 모두 가능 (별도 GRANT 불필요)
CREATE TABLE my_data (id INTEGER, val DOUBLE);
INSERT INTO my_data VALUES (1, 3.14);
SELECT * FROM my_data;
DROP TABLE my_data;
```

### 다른 사용자 소유 객체 접근

SYS 계정이 생성한 테이블이나 다른 사용자 소유 테이블에 접근하려면 명시적 GRANT가 필요합니다.

```sql
-- SYS 소유의 sensor_log를 app_user가 조회하려면
-- SYS 계정에서 권한 부여
GRANT SELECT ON sys.sensor_log TO app_user;

-- app_user1 소유의 테이블을 app_user2가 접근하려면
GRANT SELECT ON app_user1.shared_table TO app_user2;
```

권한 부여 없이 다른 사용자 소유 테이블에 접근하면 권한 오류가 발생합니다.

### 최소 권한 원칙 적용

실무에서는 업무에 필요한 최소한의 권한만 부여하는 것을 권장합니다.

```sql
-- 읽기 전용 계정: SELECT만 부여
CREATE USER reader_user IDENTIFIED BY 'Reader!Pass1';
-- CREATE, DROP, INSERT, DELETE, UPDATE 기본 권한은 제거하지 않음에 주의
-- 다른 사용자 테이블에 대한 접근은 별도 GRANT로 제어

-- 데이터 수집 전용 계정: INSERT만 필요한 테이블에 부여
CREATE USER collector_user IDENTIFIED BY 'Collect!Pass1';
GRANT INSERT ON sys.sensor_log TO collector_user;
GRANT INSERT ON sys.sensor_tag TO collector_user;
```

신규 사용자의 기본 권한(SELECT, INSERT, DELETE, UPDATE, CREATE, DROP)은 자신의 소유 객체에만 적용됩니다. 다른 사용자 소유 객체에 대한 접근은 항상 명시적 GRANT가 필요합니다.

<a id="privileges-2"></a>

## 테이블 권한

테이블 권한은 특정 테이블에 대한 DML 작업을 세밀하게 제어하는 권한입니다.
`GRANT ... ON table TO user` 구문으로 부여하며, 테이블 단위로 개별 관리할 수 있습니다.

### 테이블 권한 종류

| 권한 | 허용하는 작업 | 비고 |
|---|---|---|
| `SELECT` | 해당 테이블 데이터 조회 | 모든 테이블 유형 지원 |
| `INSERT` | 해당 테이블에 행 삽입 | 모든 테이블 유형 지원 |
| `DELETE` | 해당 테이블에서 행 삭제 | 모든 테이블 유형 지원 |
| `UPDATE` | 해당 테이블의 행 수정 | VOLATILE, LOOKUP 전용 |
| `ALL` | SELECT + INSERT + DELETE + UPDATE 일괄 부여 | |

### 테이블 지정 방법

테이블 권한 부여 시 테이블을 지정하는 방법은 세 가지입니다.

| 형식 | 예시 |
|---|---|
| 테이블명만 | `GRANT SELECT ON sensor_log TO user1` |
| 스키마.테이블명 | `GRANT SELECT ON sys.sensor_log TO user1` |
| DB명.스키마명.테이블명 | `GRANT SELECT ON machbasedb.sys.sensor_log TO user1` |

### 권한 부여 예제

```sql
-- 단일 테이블 조회 권한
GRANT SELECT ON sys.sensor_log TO reader_user;

-- 단일 테이블 삽입 권한
GRANT INSERT ON sensor_tag TO writer_user;

-- 여러 DML 권한 동시 부여
GRANT SELECT, INSERT ON sys.sensor_log TO app_user;
GRANT SELECT, INSERT, DELETE ON sys.sensor_log TO manager_user;

-- 테이블의 모든 DML 권한 부여
GRANT ALL ON sys.sensor_log TO admin_user;
```

### 권한 취소 예제

```sql
-- 특정 권한 취소
REVOKE DELETE ON sys.sensor_log FROM manager_user;

-- 모든 테이블 권한 취소
REVOKE ALL ON sys.sensor_log FROM admin_user;
```

### 테이블 권한 조회

```sql
-- 모든 테이블 권한 현황 조회
SELECT * FROM m$obj_privileges;

-- 특정 테이블의 권한 부여 현황
SELECT * FROM m$obj_privileges WHERE obj_name = 'SENSOR_LOG';

-- 특정 사용자의 테이블 권한 목록
SELECT * FROM m$obj_privileges WHERE grantee = 'APP_USER';
```

### 주의 사항

- 테이블 소유자는 별도 GRANT 없이 자신의 테이블에 대한 모든 DML을 실행할 수 있습니다.
- 다른 사용자 소유의 테이블에 접근하려면 반드시 해당 테이블에 대한 권한이 필요합니다.
- LOG, TAG 테이블에 `UPDATE` 권한을 부여하더라도 테이블 유형 제약으로 인해 UPDATE를 실행할 수 없습니다.
- VOLATILE, LOOKUP 테이블의 `DELETE`/`UPDATE`는 기본키 기반 `WHERE` 조건이 필요합니다.

<a id="checklist-diagnosis-privileges"></a>

## 권한 진단 체크리스트

권한 현황을 정기적으로 점검하고 불필요한 권한을 제거하는 것이 데이터베이스 보안의 기본입니다.

### 권한 조회 쿼리

#### 데이터베이스 권한 확인

```sql
-- 모든 데이터베이스 권한 현황
SELECT * FROM m$sys_privileges;

-- 특정 사용자의 데이터베이스 권한 확인
SELECT * FROM m$sys_privileges WHERE grantee = 'APP_USER';
```

#### 테이블 권한 확인

```sql
-- 모든 테이블 권한 현황
SELECT * FROM m$obj_privileges;

-- 특정 테이블의 권한 부여 현황
SELECT * FROM m$obj_privileges WHERE obj_name = 'SENSOR_LOG';

-- 특정 사용자의 테이블 권한 목록
SELECT * FROM m$obj_privileges WHERE grantee = 'APP_USER';
```

#### 사용자와 권한 전체 현황

```sql
-- 모든 사용자와 데이터베이스 권한 현황
SELECT u.user_name, p.privilege_type
  FROM m$user u
  LEFT JOIN m$sys_privileges p ON u.user_id = p.grantee_id
 ORDER BY u.user_name, p.privilege_type;

-- 모든 사용자와 테이블 권한 현황
SELECT u.user_name, op.obj_name, op.privilege_type
  FROM m$user u
  LEFT JOIN m$obj_privileges op ON u.user_id = op.grantee_id
 ORDER BY u.user_name, op.obj_name, op.privilege_type;
```

### 진단 체크리스트

#### 일상 점검

- [ ] 신규 사용자 생성 후 최소 권한 원칙 적용 여부 확인
- [ ] 애플리케이션 계정에 불필요한 관리 권한(ALTER, BACKUP, MOUNT) 부여 여부 확인
- [ ] 읽기 전용 계정에 INSERT, DELETE, UPDATE 권한이 부여되어 있지 않은지 확인

#### 정기 감사 (분기별 권장)

- [ ] 전체 사용자 목록과 권한 현황 검토
- [ ] 퇴직·이직한 직원 계정의 비활성화 또는 삭제 여부 확인
- [ ] 임시로 부여한 권한(테스트, 마이그레이션 등)이 회수되었는지 확인
- [ ] SYS 계정 비밀번호 변경 이력 확인
- [ ] 권한이 과도하게 부여된 계정 식별 및 조정

```sql
-- 분기 감사용: 각 사용자별 보유 권한 요약
SELECT
    u.user_name,
    COUNT(DISTINCT p.privilege_type) AS db_priv_count,
    COUNT(DISTINCT op.obj_name)      AS table_access_count
  FROM m$user u
  LEFT JOIN m$sys_privileges p  ON u.user_id = p.grantee_id
  LEFT JOIN m$obj_privileges op ON u.user_id = op.grantee_id
 GROUP BY u.user_name
 ORDER BY db_priv_count DESC, table_access_count DESC;
```

### 계정 비활성화 처리

퇴직·이직 시 계정을 즉시 처리합니다.

```sql
-- 비밀번호를 알 수 없는 값으로 변경하여 접속 차단
ALTER USER old_employee IDENTIFIED BY '!DISABLED!ACCOUNT!';

-- 테이블 권한 전체 취소
REVOKE ALL ON sys.sensor_log FROM old_employee;

-- 데이터베이스 권한 전체 취소
REVOKE ALL ON machbasedb FROM old_employee;

-- 해당 사용자가 소유한 객체를 다른 사용자에게 이관 후 계정 삭제
-- (소유 테이블이 있는 경우 먼저 DROP TABLE 또는 소유권 이전 필요)
DROP USER old_employee;
```

> **주의**: 사용자가 소유한 테이블이 있으면 `DROP USER`가 실패합니다. 먼저 해당 사용자의 테이블을 삭제하거나 SYS 계정으로 이관한 후 사용자를 삭제하십시오.

### 권장 계정 구성 예시

| 계정 유형 | 필요 권한 | 설명 |
|---|---|---|
| 읽기 전용 | `SELECT ON target_table` | 데이터 조회 전용 |
| 데이터 수집 | `INSERT ON target_table` | 센서·IoT 데이터 적재 |
| 애플리케이션 | `SELECT, INSERT ON target_table` | 일반 CRUD 애플리케이션 |
| 배포 자동화 | `DDL ON machbasedb` | 스키마 변경 자동화 |
| 운영 DBA | `ALL ON machbasedb` | 데이터베이스 전반 관리 |
| 백업 에이전트 | `BACKUP ON machbasedb` | 정기 백업 전용 |

각 계정에는 업무에 필요한 최소한의 권한만 부여하고, 정기적으로 권한 현황을 검토하십시오.
