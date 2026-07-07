---
type: docs
title: 'DDL / ALL 합성 권한'
weight: 60
---

`DDL`과 `ALL`은 여러 데이터베이스 권한을 묶어서 한 번에 부여하거나 취소하는 합성 권한입니다.

## DDL 합성 권한

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

## ALL 합성 권한

`ALL`은 데이터베이스 대상에서 사용할 수 있는 모든 권한을 일괄 부여합니다.  
`MACHBASEDB`에 대한 `ALL`은 `CREATE`, `DROP`, `ALTER`, `BACKUP`, `MOUNT`를 모두 포함합니다.

```sql
-- 모든 데이터베이스 권한 일괄 부여
GRANT ALL ON machbasedb TO admin_user;

-- 모든 데이터베이스 권한 일괄 취소
REVOKE ALL ON machbasedb FROM admin_user;
```

## ALL의 대상별 의미 차이

`ALL`은 대상에 따라 포함하는 권한이 다릅니다.

| 대상 | ALL의 의미 |
|---|---|
| `MACHBASEDB` | CREATE, DROP, ALTER, BACKUP, MOUNT (데이터베이스 관리 권한 전체) |
| 특정 테이블 | SELECT, INSERT, DELETE, UPDATE (DML 권한 전체) |

```sql
-- 데이터베이스 관리 권한 전체 부여
GRANT ALL ON machbasedb TO admin_user;

-- 특정 테이블의 DML 권한 전체 부여
GRANT ALL ON sys.sensor_log TO app_user;
```

## SYS 계정의 권한

SYS 계정은 모든 권한을 기본으로 보유합니다. GRANT 명령을 실행하지 않아도 모든 DDL, DML, 관리 작업을 수행할 수 있습니다.

```sql
-- SYS 계정에 권한을 부여할 필요가 없습니다.
-- GRANT ALL ON machbasedb TO SYS;  -- 불필요
```

## 실무 활용 예제

```sql
-- 배포 자동화 계정: DDL만 허용
GRANT DDL ON machbasedb TO ci_deploy_user;

-- DBA 계정: 모든 데이터베이스 권한 부여
GRANT ALL ON machbasedb TO dba_user;

-- 특정 프로젝트 종료 후 권한 회수
REVOKE ALL ON machbasedb FROM ci_deploy_user;
```
