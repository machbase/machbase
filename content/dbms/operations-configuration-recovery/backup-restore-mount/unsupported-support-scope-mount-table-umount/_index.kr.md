---
type: docs
title: 'MOUNT TABLE / UMOUNT TABLE 비공개 또는 미지원 범위 (TODO(verify))'
weight: 120
---

`MOUNT DATABASE`는 데이터베이스 전체를 단위로 마운트하는 공식 지원 기능입니다. 테이블 단위 마운트(`MOUNT TABLE`)는 현재 공개적으로 지원되지 않습니다.

## 테이블 단위 마운트 미지원

Machbase는 테이블 단위의 마운트(`MOUNT TABLE`) 명령을 공개 API로 제공하지 않습니다. 따라서 특정 테이블만 선택적으로 마운트하는 기능은 사용할 수 없습니다.

- `MOUNT TABLE table_name ...` 문법은 지원되지 않거나 공개되지 않은 상태입니다.
- `UMOUNT TABLE table_name` 역시 동일하게 공개되지 않은 상태입니다.

## 권장 대안: MOUNT DATABASE

특정 테이블의 데이터에만 접근하더라도 데이터베이스 전체 마운트를 사용하세요. 마운트된 데이터베이스에서 원하는 테이블만 선택적으로 조회하면 됩니다.

```sql
-- 전체 DB 마운트
MOUNT DATABASE '/backup/machbase_20240101' TO backup_db;

-- 특정 테이블만 조회
SELECT * FROM backup_db.sys.sensor_log
 WHERE _arrival_time > TO_DATE('2024-01-15','YYYY-MM-DD');

SELECT * FROM backup_db.sys.device_info
 WHERE device_id = 'DEV_001';

-- 사용 완료 후 언마운트
UNMOUNT DATABASE backup_db;
```

## 테이블 백업과의 조합

특정 테이블만 백업한 경우에도 마운트는 `MOUNT DATABASE` 명령으로 수행합니다.

```sql
-- 테이블 단위 백업
BACKUP TABLE sensor_log INTO DISK = '/backup/sensor_log_20240101';

-- 테이블 백업 파일도 MOUNT DATABASE로 마운트
MOUNT DATABASE '/backup/sensor_log_20240101' TO tbl_backup;
SELECT * FROM tbl_backup.sys.sensor_log;
UNMOUNT DATABASE tbl_backup;
```

## 요약

| 기능 | 지원 여부 |
|------|:---------:|
| `MOUNT DATABASE` | O (공식 지원) |
| `UNMOUNT DATABASE` | O (공식 지원) |
| `MOUNT TABLE` | X (미공개/미지원) |
| `UMOUNT TABLE` | X (미공개/미지원) |

테이블 단위 마운트가 필요한 경우, 데이터베이스 전체를 마운트한 뒤 해당 테이블만 조회하는 방식을 사용하세요. 마운트는 읽기 전용이므로 다른 테이블에 영향을 주지 않습니다.
