---
type: docs
title: '17.3.5 V$STORAGE_MOUNT_* 사전'
weight: 50
---

`V$STORAGE_MOUNT_DATABASES`는 백업 데이터를 현재 서버에 읽기 전용으로 마운트한 상태를 표시합니다. 마운트된 백업 데이터베이스에서 데이터를 SELECT로 직접 조회할 수 있습니다.

## V$STORAGE_MOUNT_DATABASES

| 컬럼 이름 | 타입 | 설명 |
|----------|------|------|
| `MOUNT_NAME` | VARCHAR | 마운트에 부여된 이름 |
| `PATH` | VARCHAR | 마운트된 백업 데이터의 경로 |
| `MOUNT_TIME` | DATETIME | 마운트가 수행된 시각 |
| `STATUS` | VARCHAR | 마운트 상태 (`MOUNTED` / `ERROR`) |

## SQL 예제

```sql
-- 현재 마운트된 백업 데이터베이스 목록 전체 조회
SELECT * FROM v$storage_mount_databases;

-- 마운트 이름과 경로, 마운트 시각 확인
SELECT mount_name, path, mount_time, status
  FROM v$storage_mount_databases
 ORDER BY mount_time DESC;

-- 마운트 상태가 정상인 항목만 확인
SELECT mount_name, path, mount_time
  FROM v$storage_mount_databases
 WHERE status = 'MOUNTED';
```

## 마운트 명령 참고

백업 데이터베이스를 마운트하고 해제하는 명령은 다음과 같습니다.

```sql
-- 백업 데이터베이스 마운트
MOUNT DATABASE 'backup_20240101' TO '/data/backup/20240101';

-- 마운트 해제
UNMOUNT DATABASE 'backup_20240101';
```

마운트 후 마운트 이름을 접두사로 사용하여 데이터를 조회합니다.

```sql
-- 마운트된 백업에서 데이터 조회
SELECT * FROM backup_20240101:sensor_tag
 WHERE time >= TO_DATE('2024-01-01') AND time < TO_DATE('2024-01-02')
 ORDER BY time;
```

> 마운트 기능 상세와 운영 절차는 [백업과 복구](../../../operations-configuration-recovery/) 섹션을 참고하십시오.
