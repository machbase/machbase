---
type: docs
title: '13.4.4.3 디스크 사용량 확인'
weight: 30
---

Machbase 데이터 파일이 저장된 디스크의 사용량을 SQL과 OS 명령으로 확인하는 방법을 설명합니다. 디스크가 가득 차면 데이터 적재와 인덱스 구축이 자동으로 중단되므로 정기적인 모니터링이 필수입니다.

## 스토리지 사용량 개요

`V$STORAGE_USAGE`는 Machbase 데이터 디렉터리가 위치한 스토리지의 전체 사용 현황을 보여줍니다.

```sql
-- 스토리지 사용량 확인
SELECT total_space,
       used_space,
       used_ratio,
       ratio_cap
  FROM v$storage_usage;
```

| 컬럼 | 설명 |
|------|------|
| TOTAL_SPACE | 스토리지 전체 용량 (MiB) |
| USED_SPACE | 사용 중인 용량 (MiB) |
| USED_RATIO | 사용률 (%) |
| RATIO_CAP | 허용 최대 사용률 (%). 이 값 초과 시 데이터 입력 중단 |

`USED_RATIO`가 `RATIO_CAP`에 근접하면 즉시 조치가 필요합니다.

## 테이블별 디스크 사용량

`V$STORAGE_TABLES`에서 각 테이블이 스토리지에서 점유한 용량을 확인합니다.

```sql
-- 테이블별 스토리지 사용량 (큰 순서대로)
SELECT id, type, status, storage_usage
  FROM v$storage_tables
 ORDER BY storage_usage DESC;
```

테이블 이름을 함께 조회하려면 메타 테이블과 JOIN합니다.

```sql
-- 테이블 이름과 스토리지 사용량
SELECT t.name          AS table_name,
       t.type          AS table_type,
       vs.storage_usage AS used_bytes,
       round(vs.storage_usage / 1073741824.0, 2) AS used_gb
  FROM v$storage_tables vs
  JOIN m$sys_tables t ON vs.id = t.id
 ORDER BY vs.storage_usage DESC;
```

## 컬럼별 디스크 사용량

특정 테이블에서 용량을 많이 차지하는 컬럼을 파악합니다.

```sql
-- 특정 테이블의 컬럼별 파일 크기 확인
SELECT dc.id           AS column_id,
       mc.name         AS column_name,
       dc.disk_file_size AS disk_bytes,
       round(dc.disk_file_size / 1073741824.0, 2) AS disk_gb
  FROM v$storage_dc_table_columns dc
  JOIN m$sys_tables  mt ON dc.table_id = mt.id
  JOIN m$sys_columns mc ON dc.id = mc.id AND mc.table_id = mt.id
 WHERE mt.name = 'SENSOR_LOG'
 ORDER BY dc.disk_file_size DESC;
```

## 인덱스 파일 크기 확인

```sql
-- 인덱스 파일 크기 확인
SELECT di.id           AS index_id,
       mi.name         AS index_name,
       di.disk_file_size AS disk_bytes
  FROM v$storage_dc_table_indexes di
  JOIN m$sys_tables  mt ON di.table_id = mt.id
  JOIN m$sys_indexes mi ON di.id = mi.id
 WHERE mt.name = 'SENSOR_LOG'
 ORDER BY di.disk_file_size DESC;
```

## 테이블스페이스 정보 확인

```sql
-- 테이블스페이스와 디스크 경로 확인
SELECT ts.name AS tablespace_name,
       d.path,
       d.io_thread_count
  FROM v$storage_dc_tablespace_disks d
  JOIN v$storage_dc_tablespaces ts ON d.tablespace_id = ts.id;
```

## OS 레벨 디스크 확인

SQL 조회와 함께 OS 명령으로 디스크 여유 공간을 확인합니다.

```bash
# 전체 파티션 디스크 사용량
df -h

# Machbase 데이터 디렉터리 사용량
df -h $MACHBASE_HOME/dbs/

# 데이터 디렉터리 내 파일 크기 합계
du -sh $MACHBASE_HOME/dbs/

# 큰 파일 상위 20개 확인
du -sh $MACHBASE_HOME/dbs/*/ | sort -rh | head -20
```

## 디스크 풀 임박 시 조치

`USED_RATIO`가 `RATIO_CAP`의 90% 이상에 도달하면 아래 조치를 취합니다.

### 1. 불필요한 파일 제거

```bash
# 오래된 트레이스 로그 압축
gzip $MACHBASE_HOME/trc/machbase.trc.2024*

# 30일 이상 된 로그 파일 삭제
find $MACHBASE_HOME/trc/ -name "*.trc.*" -mtime +30 -delete
```

### 2. Retention Policy로 오래된 데이터 삭제

```sql
-- 특정 시점 이전 데이터 삭제 (Log 테이블)
DELETE FROM sensor_log BEFORE TO_DATE('2023-01-01', 'YYYY-MM-DD');

-- 삭제 후 테이블 통계 확인
SELECT id, storage_usage FROM v$storage_tables
 ORDER BY storage_usage DESC;
```

### 3. RATIO_CAP 조정

`DISK_USED_RATIO_CAP`은 설정 파일에서 관리합니다. 실제 디스크 공간 확보 없이 이 설정만 높이면 OS 레벨에서 실제 디스크가 가득 찰 수 있으므로 주의합니다.

```sql
-- 현재 DISK_USED_RATIO_CAP 설정 확인
SELECT name, value FROM v$property WHERE name = 'DISK_USED_RATIO_CAP';
```

## 주기적 모니터링 스크립트 예시

```bash
#!/bin/bash
# check_disk.sh — 디스크 사용량 경보 스크립트

THRESHOLD=80

cat > /tmp/check_disk.sql <<'SQL'
SELECT used_ratio FROM v$storage_usage;
SQL

USED=$(machsql -u sys -p manager -s 127.0.0.1 -f /tmp/check_disk.sql \
  2>/dev/null | awk '/^[[:space:]]*[0-9]+(\\.[0-9]+)?[[:space:]]*$/ {print int($1); exit}')

if [ "$USED" -gt "$THRESHOLD" ]; then
    echo "[WARN] Machbase disk usage: ${USED}% (threshold: ${THRESHOLD}%)"
    df -h $MACHBASE_HOME/dbs/
fi
```
