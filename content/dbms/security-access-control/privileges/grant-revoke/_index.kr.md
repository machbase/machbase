---
type: docs
title: 'GRANT / REVOKE'
weight: 20
---

`GRANT` 문으로 사용자에게 권한을 부여하고, `REVOKE` 문으로 이미 부여된 권한을 취소합니다.  
두 명령 모두 SYS 계정에서 실행합니다.

## 문법

```sql
-- 권한 부여
GRANT privilege_list ON target TO user_name;

-- 권한 취소
REVOKE privilege_list ON target FROM user_name;
```

- `privilege_list`: 쉼표로 구분된 하나 이상의 권한명
- `target`: `MACHBASEDB` (데이터베이스 권한) 또는 `[schema.]table_name` (테이블 권한)
- `user_name`: 대상 사용자명 (대소문자 무관, 내부적으로 대문자 처리)

## 데이터베이스 권한 부여

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

## 테이블 권한 부여

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

## 권한 취소

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

## 주의 사항

- `GRANT SELECT ON machbasedb TO user` 형식으로 DML 권한을 데이터베이스 전체에 부여하는 것은 지원하지 않습니다. DML 권한은 반드시 특정 테이블을 지정해야 합니다.
- 데이터베이스 권한 대상 이름은 반드시 `MACHBASEDB`를 사용합니다. 다른 이름을 지정하면 `[ERR-02186: Invalid database name.]` 오류가 발생합니다.
- SYS 계정은 모든 권한을 기본으로 보유하므로 별도 GRANT가 필요 없습니다.

## 현재 권한 확인

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
