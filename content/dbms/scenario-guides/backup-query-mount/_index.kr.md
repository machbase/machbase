---
type: docs
title: '백업 데이터 마운트 후 조회'
weight: 110
---

## 시나리오 개요

과거 백업 데이터를 현재 운영 서버에 MOUNT해 현재 데이터와 함께 분석하는 패턴입니다.

데이터베이스를 중단하거나 복원 작업 없이 과거 백업 스냅샷을 읽기 전용으로 접근할 수 있습니다. 감사(audit), 과거 이슈 재현, 아카이브 데이터 추출 등 다양한 상황에서 활용합니다.

**적합한 상황:**

- 운영 서버를 중단하지 않고 특정 시점의 과거 데이터를 확인해야 할 때
- 장애 발생 전후 데이터를 현재 데이터와 비교 분석할 때
- 아카이브된 오래된 데이터에서 일부 레코드를 추출해야 할 때
- 백업 데이터를 복원하지 않고 신속하게 조회가 필요할 때

> **에디션 참고**: MOUNT/UNMOUNT는 Standard Edition 전용 기능입니다. Cluster Edition에서는 지원되지 않습니다.

> **권한 요구사항**: 일반 사용자가 MOUNT를 실행하려면 `GRANT MOUNT ON machbasedb TO user_name;` 권한이 필요합니다.

## 1단계: 백업 수행

마운트에 사용할 백업을 생성합니다. 운영 중인 서버를 중단하지 않고 실행할 수 있습니다.

```sql
-- 전체 데이터베이스 백업
BACKUP DATABASE INTO DISK = '/backup/machbase_20240101';

-- 특정 기간 데이터 백업
BACKUP DATABASE
    FROM TO_DATE('2024-01-01', 'YYYY-MM-DD')
    TO   TO_DATE('2024-01-02', 'YYYY-MM-DD')
    INTO DISK = '/backup/machbase_period_20240101';

-- 특정 테이블만 백업
BACKUP TABLE sensor_tag INTO DISK = '/backup/sensor_tag_20240101';
```

> 백업 경로는 절대 경로(`/`로 시작) 또는 `$MACHBASE_HOME/dbs` 기준 상대 경로를 사용할 수 있습니다.

## 2단계: 백업 데이터 MOUNT

`MOUNT DATABASE` 명령으로 백업 디렉터리를 현재 서버에 연결합니다.

```sql
-- 절대 경로로 마운트
MOUNT DATABASE '/backup/machbase_20240101' TO backup_20240101;

-- 상대 경로 ($MACHBASE_HOME/dbs 기준)
MOUNT DATABASE 'machbase_20240101' TO backup_20240101;
```

- `'/backup/machbase_20240101'`: BACKUP 명령으로 생성된 디렉터리 경로
- `backup_20240101`: 마운트된 DB에 접근할 때 사용할 이름 (SQL에서 스키마처럼 사용)

마운트 성공 후 마운트된 DB 목록을 확인합니다.

```sql
SELECT * FROM v$storage_mount_databases;
```

## 3단계: 마운트된 DB 조회

마운트된 데이터베이스의 테이블에 접근할 때는 `mount_name.user_name.table_name` 형식을 사용합니다.

```sql
-- 마운트된 테이블의 특정 기간 데이터 조회
SELECT name, time, value
  FROM backup_20240101.sys.sensor_tag
 WHERE time > TO_DATE('2024-01-01', 'YYYY-MM-DD')
 ORDER BY time
 LIMIT 100;
```

```sql
-- 마운트된 DB의 집계 조회
SELECT
    name,
    COUNT(*)    AS cnt,
    MIN(value)  AS min_val,
    MAX(value)  AS max_val,
    AVG(value)  AS avg_val
  FROM backup_20240101.sys.sensor_tag
 WHERE name = 'sensor-01'
   AND time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02')
 GROUP BY name;
```

## 4단계: 현재 DB와 백업 DB 비교 분석

MOUNT의 가장 강력한 기능은 현재 운영 데이터와 과거 백업 데이터를 하나의 쿼리에서 함께 조회하는 것입니다.

### 레코드 수 비교

```sql
-- 현재 DB vs 백업 DB 레코드 수 비교
SELECT 'current' AS src, COUNT(*) AS cnt FROM sensor_tag
UNION ALL
SELECT 'backup',          COUNT(*) AS cnt FROM backup_20240101.sys.sensor_tag;
```

### 특정 센서 값 비교

```sql
-- 동일 시간대의 현재 값과 백업 값 비교
SELECT
    a.name,
    a.time,
    a.value       AS current_value,
    b.value       AS backup_value,
    a.value - b.value AS diff
  FROM sensor_tag a
  JOIN backup_20240101.sys.sensor_tag b
    ON a.name = b.name AND a.time = b.time
 WHERE a.name = 'sensor-01'
   AND a.time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-01 01:00:00')
 ORDER BY a.time;
```

### 현재 DB에 없는 과거 데이터 추출

```sql
-- 백업에만 있고 현재 DB에 없는 레코드 확인
SELECT b.name, b.time, b.value
  FROM backup_20240101.sys.sensor_tag b
 WHERE NOT EXISTS (
     SELECT 1 FROM sensor_tag a
      WHERE a.name = b.name AND a.time = b.time
 )
   AND b.time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02')
 LIMIT 100;
```

### 기간별 집계 비교

```sql
-- 시간대별 평균 비교 (현재 vs 백업)
SELECT
    'current'                         AS src,
    DATE_TRUNC('hour', time)          AS hour_bucket,
    AVG(value)                        AS avg_val
  FROM sensor_tag
 WHERE name = 'sensor-01'
   AND time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02')
 GROUP BY hour_bucket
UNION ALL
SELECT
    'backup',
    DATE_TRUNC('hour', time),
    AVG(value)
  FROM backup_20240101.sys.sensor_tag
 WHERE name = 'sensor-01'
   AND time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02')
 GROUP BY DATE_TRUNC('hour', time)
 ORDER BY src, hour_bucket;
```

## 5단계: UNMOUNT

조회가 완료되면 마운트를 해제합니다.

```sql
UNMOUNT DATABASE backup_20240101;
```

마운트 해제 후 해당 이름으로는 더 이상 접근할 수 없습니다. 언마운트는 해당 마운트 DB를 참조 중인 활성 세션이 없을 때 즉시 실행됩니다.

## 주의사항

### 동시 MOUNT 제한

한 서버에 여러 백업 DB를 동시에 마운트할 수 있지만, 마운트 수가 많아질수록 메모리와 파일 핸들 사용량이 증가합니다. 현재 마운트 상태는 다음으로 확인합니다.

```sql
SELECT * FROM v$storage_mount_databases;
```

### 디스크 공간 확인

마운트는 백업 데이터를 복사하지 않고 원본 디렉터리를 직접 참조합니다. 원본 백업 파일이 삭제되거나 이동되면 마운트된 DB 접근이 실패합니다. 마운트 중에는 백업 디렉터리를 변경하지 마십시오.

### 읽기 전용 제한

마운트된 데이터베이스에서는 다음 작업이 불가능합니다.

- 테이블 생성 및 삭제
- 인덱스 생성 및 삭제
- 데이터 삽입, 수정, 삭제

### 버전 호환성

백업 데이터베이스의 버전과 현재 서버의 메타데이터 버전이 호환되어야 합니다. 버전 차이가 큰 경우 마운트가 실패할 수 있습니다.

## 요약

| 단계 | 명령 |
|------|------|
| 백업 생성 | `BACKUP DATABASE INTO DISK = '경로'` |
| 마운트 | `MOUNT DATABASE '경로' TO 이름` |
| 마운트 DB 조회 | `SELECT ... FROM 이름.sys.테이블` |
| 현재 vs 백업 비교 | `UNION ALL`로 두 쿼리 결합 |
| 마운트 목록 확인 | `SELECT * FROM v$storage_mount_databases` |
| 언마운트 | `UNMOUNT DATABASE 이름` |

## 관련 문서

- [백업, 복원, 마운트](../../operations-configuration-recovery/backup-restore-mount/)
- [데이터베이스 마운트](../../operations-configuration-recovery/backup-restore-mount/database-mount/)
- [마운트된 데이터베이스 조회](../../operations-configuration-recovery/backup-restore-mount/query-database-mount/)
- [이상 데이터 정정 후 ROLLUP Rebuild](../correction-abnormal-data-rollup-rebuild/)
