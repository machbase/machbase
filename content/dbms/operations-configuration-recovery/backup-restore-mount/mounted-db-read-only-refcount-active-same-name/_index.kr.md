---
type: docs
title: 'mounted DB read-only/refcount/active same-name isolation'
weight: 100
---

마운트된 데이터베이스의 동작 특성인 읽기 전용 속성, refcount, 동일 이름 충돌 방지에 대해 설명합니다.

## 읽기 전용 (Read-Only)

마운트된 데이터베이스는 반드시 읽기 전용으로만 접근할 수 있습니다. 이는 백업 데이터의 무결성을 보장하기 위한 설계입니다.

- 마운트 DB에 `INSERT`, `UPDATE`, `DELETE`를 실행하면 오류가 발생합니다.
- `CREATE TABLE`, `DROP TABLE`, `CREATE INDEX` 등 DDL도 실행할 수 없습니다.
- 마운트 DB의 내용은 마운트된 이후 변경되지 않으므로 특정 시점의 데이터를 신뢰할 수 있습니다.

```sql
-- 읽기 전용 확인 예제
MOUNT DATABASE '/backup/machbase_20240101' TO backup_db;

-- 아래 명령은 오류 발생
INSERT INTO backup_db.sys.sensor_log VALUES (...);  -- 오류: 읽기 전용
UPDATE backup_db.sys.sensor_log SET value = 0;      -- 오류: 읽기 전용
```

## refcount (참조 카운트)

refcount는 특정 마운트 데이터베이스를 현재 활성 세션에서 참조하고 있는 수를 나타냅니다.

```sql
-- 현재 마운트 목록과 refcount 확인
SELECT name, path, refcount FROM v$storage_mount_databases;
```

**refcount의 역할:**

- 마운트 DB를 사용 중인 세션이 있을 때 강제 언마운트를 방지합니다.
- `UNMOUNT DATABASE` 명령은 `refcount = 0`일 때 즉시 실행됩니다.
- `refcount > 0`인 상태에서 `UNMOUNT DATABASE`를 실행하면, 모든 참조 세션이 종료될 때까지 언마운트가 지연되거나 오류가 반환될 수 있습니다.

```sql
-- refcount가 0이 될 때까지 대기 후 언마운트
-- (활성 쿼리가 완료된 후 실행)
UNMOUNT DATABASE backup_db;
```

## 동일 이름 충돌 방지 (Same-Name Isolation)

같은 이름으로 두 개의 마운트 데이터베이스를 동시에 생성할 수 없습니다.

```sql
-- 첫 번째 마운트 성공
MOUNT DATABASE '/backup/machbase_20240101' TO archive_db;

-- 동일 이름으로 다시 마운트 시도 - 오류 발생
MOUNT DATABASE '/backup/machbase_20240201' TO archive_db;  -- 오류: 이미 존재하는 이름
```

다른 백업을 같은 이름으로 마운트하려면 기존 마운트를 먼저 해제해야 합니다.

```sql
-- 기존 마운트 해제 후 새 마운트
UNMOUNT DATABASE archive_db;
MOUNT DATABASE '/backup/machbase_20240201' TO archive_db;
```

## 동시 마운트

서버 한 대에 여러 개의 백업 데이터베이스를 동시에 마운트할 수 있습니다. 단, 각각 다른 이름을 사용해야 합니다.

```sql
-- 여러 백업을 동시에 마운트
MOUNT DATABASE '/backup/machbase_202401' TO archive_202401;
MOUNT DATABASE '/backup/machbase_202402' TO archive_202402;
MOUNT DATABASE '/backup/machbase_202403' TO archive_202403;

-- 각 마운트 DB에서 독립적으로 조회
SELECT COUNT(*) FROM archive_202401.sys.sensor_log;
SELECT COUNT(*) FROM archive_202402.sys.sensor_log;
SELECT COUNT(*) FROM archive_202403.sys.sensor_log;

-- 정리
UNMOUNT DATABASE archive_202401;
UNMOUNT DATABASE archive_202402;
UNMOUNT DATABASE archive_202403;
```

## 마운트 상태 요약

| 상태 | 설명 |
|------|------|
| 마운트 직후 | refcount = 0, 읽기 전용 |
| 쿼리 실행 중 | refcount > 0, 읽기 전용 |
| 쿼리 완료 후 | refcount = 0, 언마운트 가능 |
| 언마운트 후 | 목록에서 제거됨 |
