---
type: docs
title: '백업 검증'
weight: 50
---

백업이 완료된 후 해당 백업 파일이 실제로 복구 가능한 상태인지 검증하는 절차를 설명합니다. 백업 파일이 존재하더라도 손상된 경우 복구에 실패할 수 있으므로, 정기적인 검증이 필요합니다.

## 백업 완료 확인

백업 실행 후 서버 로그에서 완료 여부를 확인합니다.

```bash
# 백업 완료 로그 확인
grep 'Backup completed\|Backup failed' $MACHBASE_HOME/trc/machbase.trc | tail -10
```

정상 완료 시:
```
[2024-01-15 03:00:15.001] [INFO] [BACKUP] Backup completed. path=/backup/20240115, elapsed=125s
```

백업 실패 시:
```
[2024-01-15 03:00:15.001] [ERROR] [BACKUP] Backup failed. path=/backup/20240115, reason=Disk full
```

## 백업 파일 존재 여부 확인

```bash
# 백업 디렉터리 크기 확인
du -sh /backup/20240115/

# 백업 파일 목록 확인
ls -lh /backup/20240115/

# 최소한의 필수 파일 존재 여부
ls /backup/20240115/backup.dat /backup/20240115/meta.dbs-* 2>/dev/null
```

## Mount를 이용한 백업 검증

가장 확실한 검증 방법은 백업 데이터베이스를 마운트하여 실제 데이터를 조회하는 것입니다. 마운트는 운영 데이터베이스에 영향을 주지 않습니다.

### 1단계: 백업 데이터베이스 마운트

```sql
-- 백업을 testdb라는 이름으로 마운트
MOUNT DATABASE '/backup/20240115' TO testdb;
```

### 2단계: 마운트 상태 확인

```sql
-- 마운트된 데이터베이스 목록 확인
SELECT name, path, backup_begin_time, backup_end_time,
       db_begin_time, db_end_time
  FROM v$storage_mount_databases;
```

### 3단계: 마운트된 데이터 조회

```sql
-- 마운트된 테이블 조회 (testdb 접두어 사용)
SELECT count(*) FROM testdb.sys.sensor_log;

-- 데이터 범위 확인
SELECT min(_arrival_time) AS earliest,
       max(_arrival_time) AS latest,
       count(*)           AS total_rows
  FROM testdb.sys.sensor_log;

-- 일부 레코드 샘플 확인
SELECT * FROM testdb.sys.sensor_log LIMIT 10;
```

### 4단계: 마운트 해제

검증 완료 후 마운트를 해제합니다.

```sql
UNMOUNT DATABASE testdb;
```

## 백업 파일 무결성 체크섬 확인

파일 수준의 무결성을 확인합니다.

```bash
# 백업 직후 체크섬 생성 및 저장
find /backup/20240115/ -type f | sort | xargs md5sum > /backup/20240115.md5

# 이후 검증 시 체크섬 비교
md5sum -c /backup/20240115.md5
```

체크섬 불일치가 발생하면 해당 파일이 손상된 것이며, 그 백업 세트는 복구에 사용할 수 없습니다.

## 백업 검증 자동화

정기 백업 스크립트에 검증 단계를 포함합니다.

```bash
#!/bin/bash
# backup_and_verify.sh

BACKUP_PATH="/backup/$(date +%Y%m%d)"
DB_USER="sys"
DB_PASS="manager"
DB_HOST="127.0.0.1"

# 1. 백업 실행
cat > /tmp/backup.sql <<SQL
BACKUP DATABASE INTO DISK = '${BACKUP_PATH}';
SQL
machsql -u $DB_USER -p $DB_PASS -s $DB_HOST -f /tmp/backup.sql > /tmp/backup.log 2>&1

if [ $? -eq 0 ]; then
    echo "[OK] Backup completed: $BACKUP_PATH"
else
    echo "[FAIL] Backup failed. Check /tmp/backup.log"
    exit 1
fi

# 2. 체크섬 생성
find $BACKUP_PATH -type f | sort | xargs md5sum > ${BACKUP_PATH}.md5
echo "[OK] Checksum created: ${BACKUP_PATH}.md5"

# 3. 마운트 검증
cat > /tmp/verify_backup.sql <<SQL
MOUNT DATABASE '${BACKUP_PATH}' TO verify_db;
SELECT count(*) FROM verify_db.sys.sensor_log;
UNMOUNT DATABASE verify_db;
SQL
ROW_COUNT=$(machsql -u $DB_USER -p $DB_PASS -s $DB_HOST -f /tmp/verify_backup.sql \
  2>/dev/null | awk '/^[[:space:]]*[0-9]+[[:space:]]*$/ {print $1; exit}')

if [ -n "$ROW_COUNT" ] && [ "$ROW_COUNT" -gt 0 ]; then
    echo "[OK] Backup verified. Row count: $ROW_COUNT"
else
    echo "[WARN] Backup mount verification may have failed. Check manually."
fi
```

## 백업 보관 정책

| 백업 유형 | 보관 기간 | 검증 주기 |
|---------|---------|---------|
| 일별 백업 | 7일 | 매 백업 후 |
| 주별 백업 | 4주 | 주 1회 |
| 월별 백업 | 12개월 | 월 1회 |

오래된 백업 파일은 정기적으로 삭제하여 디스크 공간을 확보합니다.

```bash
# 7일 이상 된 일별 백업 삭제
find /backup/ -maxdepth 1 -type d -name "20*" -mtime +7 -exec rm -rf {} \;
```

> **중요**: 백업 검증은 백업 완료 직후뿐 아니라 정기적으로(최소 월 1회) 수행해야 합니다. 장애 발생 시 검증되지 않은 백업은 복구 실패로 이어질 수 있습니다.
