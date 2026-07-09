---
type: docs
title: '14.3.3.5 MOUNT'
weight: 50
---

`MOUNT` 권한은 `MOUNT DATABASE` 및 `UNMOUNT DATABASE` 명령을 실행하는 권한입니다.  
신규 사용자 생성 시 기본으로 부여되지 않으므로 필요할 때 명시적으로 GRANT해야 합니다.

## 허용하는 작업

`MOUNT` 권한이 있는 사용자는 다음 명령을 실행할 수 있습니다.

- `MOUNT DATABASE` — 백업 또는 외부 데이터베이스를 읽기 전용으로 마운트
- `UNMOUNT DATABASE` — 마운트된 데이터베이스를 해제

SYS 계정은 별도 권한 없이 마운트/언마운트를 실행할 수 있습니다.

## 권한 부여 예제

```sql
-- mount_user에게 MOUNT 권한 부여
GRANT MOUNT ON machbasedb TO mount_user;

-- MOUNT 권한 취소
REVOKE MOUNT ON machbasedb FROM mount_user;
```

## MOUNT DATABASE 실행 예

```sql
-- mount_user 세션에서 실행
MOUNT DATABASE '/backup/machbase_backup' TO 'backup_db';

-- 마운트 해제
UNMOUNT DATABASE 'backup_db';
```

## 마운트된 DB 데이터 조회 권한

`MOUNT` 권한은 마운트/언마운트 명령 실행만 허용합니다.  
마운트된 데이터베이스의 테이블에서 데이터를 조회하려면 해당 테이블에 대한 `SELECT` 권한이 별도로 필요합니다.

```sql
-- mount_user가 마운트된 DB 테이블을 조회하려면 SELECT도 필요
GRANT SELECT ON backup_db.sys.sensor_log TO mount_user;
```

## 운영 지침

- 마운트 작업은 백업 검증이나 히스토리 데이터 조회 목적으로 주로 사용됩니다.
- 마운트 전용 계정을 별도로 생성하고 `MOUNT` 권한만 부여하는 것을 권장합니다.
- 마운트된 데이터베이스는 읽기 전용이므로 데이터 변경 위험 없이 안전하게 조회할 수 있습니다.
