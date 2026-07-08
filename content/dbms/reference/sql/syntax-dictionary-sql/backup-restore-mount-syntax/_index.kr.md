---
type: docs
title: 'BACKUP / RESTORE / MOUNT syntax'
weight: 150
---

Machbase의 백업·복원·마운트 구문은 데이터를 안전하게 보호하고 필요 시 복구하거나 과거 데이터를 조회할 때 사용합니다.

> **권한**: 일반 사용자가 백업·마운트를 실행하려면 별도 권한이 필요합니다.
> ```sql
> GRANT BACKUP ON machbasedb TO user_name;
> GRANT MOUNT  ON machbasedb TO user_name;
> ```

---

## BACKUP

### 전체 백업

```sql
backup_database_stmt ::=
    'BACKUP DATABASE INTO DISK' '=' 'backup_path'
    [ 'IMPORT MODE' ]
```

현재 데이터베이스 전체를 지정한 경로에 저장합니다. 서버를 중단하지 않고 실행하는 온라인 백업입니다.

```sql
-- 절대 경로로 전체 백업
BACKUP DATABASE INTO DISK = '/backup/machbase_20240101';

-- 상대 경로 ($MACHBASE_HOME/dbs 기준)
BACKUP DATABASE INTO DISK = 'backup_20240101';
```

- `backup_path`가 이미 존재하면 오류가 발생합니다. 날짜 등을 포함한 고유한 이름을 사용하세요.
- 백업이 완료될 때까지 명령이 블로킹됩니다.

### 증분 백업

```sql
backup_incremental_stmt ::=
    'BACKUP DATABASE INTO DISK' '=' 'backup_path'
    'AFTER' 'backup_path_or_lsn'
```

마지막 전체(또는 증분) 백업 이후에 변경된 데이터만 백업합니다.

```sql
-- 전체 백업 이후 변경분 증분 백업
BACKUP DATABASE INTO DISK = '/backup/incr_20240102'
AFTER '/backup/machbase_20240101';
```

### 기간 백업

```sql
backup_period_stmt ::=
    'BACKUP DATABASE INTO DISK' '=' 'backup_path'
    'FROM' datetime_expr 'TO' datetime_expr
```

지정한 시간 범위에 해당하는 데이터만 백업합니다.

```sql
BACKUP DATABASE INTO DISK = '/backup/period_jan'
FROM TO_DATE('2024-01-01','YYYY-MM-DD')
TO   TO_DATE('2024-02-01','YYYY-MM-DD');
```

### 테이블 백업

```sql
backup_table_stmt ::=
    'BACKUP TABLE' table_name 'INTO DISK' '=' 'backup_path'
```

전체 데이터베이스가 아닌 특정 테이블만 선택적으로 백업합니다.

```sql
BACKUP TABLE sensor_log INTO DISK = '/backup/sensor_log_20240101';
```

---

## RESTORE

복원은 서버를 중단한 상태(오프라인)에서만 수행합니다. `machadmin -r` 명령을 사용합니다.

```bash
# 1. (권장) 복원 전 현재 데이터 백업
machsql -u sys -p manager -e "BACKUP DATABASE INTO DISK = '/backup/before_restore';"

# 2. 서버 종료
machadmin -s

# 3. 현재 데이터베이스 삭제
machadmin -d

# 4. 백업 데이터로 복원
machadmin -r /backup/machbase_20240101

# 5. 서버 시작
machadmin -u
```

복원을 실행하면 현재 데이터베이스가 백업 시점으로 완전히 교체됩니다.

### 증분 백업 복원

복원할 최종 증분 백업 경로를 한 번 지정합니다. 증분 백업은 체인 정보를 포함하므로 전체 백업부터 반복 적용하지 않아도 됩니다.

```bash
machadmin -s
machadmin -d
machadmin -r /backup/incr_20240103
machadmin -u
```

### machadmin 주요 옵션

| 옵션 | 설명 |
|------|------|
| `-s` (`--shutdown`) | 서버 정상 종료 |
| `-k` (`--kill`) | 서버 강제 종료 |
| `-u` (`--startup`) | 서버 시작 |
| `-d` (`--destroydb`) | 현재 데이터베이스 삭제 |
| `-r path` (`--restore`) | 지정한 백업 경로로 복원 |

---

## MOUNT DATABASE

```sql
mount_database_stmt ::=
    'MOUNT DATABASE' 'backup_database_path' 'TO' mount_name
```

서버를 중단하거나 데이터를 교체하지 않고, 백업 데이터베이스를 현재 서버에 읽기 전용으로 연결합니다.

- `backup_database_path`: DISK 방식으로 생성된 백업 디렉터리 경로
- `mount_name`: 마운트된 DB에 접근할 때 사용할 이름(스키마)

```sql
-- 절대 경로로 마운트
MOUNT DATABASE '/backup/machbase_20240101' TO backup_db;

-- 상대 경로 ($MACHBASE_HOME/dbs 기준)
MOUNT DATABASE 'machbase_20240101' TO backup_db;
```

### 마운트된 DB 조회

마운트된 데이터베이스의 테이블은 `mount_name.user_name.table_name` 형식으로 접근합니다.

```sql
-- 마운트 DB의 테이블 조회
SELECT * FROM backup_db.sys.sensor_log
 WHERE _arrival_time > TO_DATE('2024-01-01','YYYY-MM-DD');

-- 현재 DB와 마운트 DB를 함께 조회 (JOIN)
SELECT a.name, a.value AS current_val, b.value AS backup_val
  FROM sensor_log a
  JOIN backup_db.sys.sensor_log b ON a.name = b.name;
```

---

## UNMOUNT DATABASE

```sql
unmount_database_stmt ::=
    'UNMOUNT DATABASE' mount_name
```

마운트된 데이터베이스를 해제합니다.

```sql
UNMOUNT DATABASE backup_db;
```

마운트 DB를 참조 중인 열린 커서나 실행 중인 쿼리가 있으면 언마운트가 실패합니다. 해당 세션을 종료한 뒤 다시 실행하세요.

---

## 제약 및 주의 사항

| 항목 | 설명 |
|------|------|
| 마운트 DB 쓰기 | 불가 (읽기 전용) |
| IBFILE 방식 백업 마운트 | 불가 (DISK 방식만 마운트 가능) |
| 버전 호환성 | 백업 DB와 현재 서버의 메타 버전이 호환되어야 함 |
| TAG 테이블 기간 복원 | 미지원 (전체 백업 또는 증분 백업으로만 복원 가능) |
| Cluster Edition | MOUNT/UNMOUNT 제한될 수 있음 |

---

## 관련 문서

- [백업, 복원, 마운트 운영 가이드](../../../../operations-configuration-recovery/backup-restore-mount/) - 상세 운영 절차 및 자동화 예시
- [GRANT/REVOKE](../user-auth-syntax/#grant-revoke) - 백업·마운트 권한 부여
