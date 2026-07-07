---
type: docs
title: '테이블 백업'
weight: 30
---

테이블 백업은 전체 데이터베이스가 아닌 특정 테이블 하나만 백업합니다. 중요도가 높은 테이블을 더 자주 백업하거나, 특정 테이블만 별도로 이전해야 할 때 사용합니다.

## 문법

```sql
BACKUP TABLE table_name INTO DISK = 'backup_path';
```

기간 조건을 함께 사용할 수 있습니다.

```sql
BACKUP TABLE table_name
  [ FROM start_time TO end_time ]
  INTO DISK = 'backup_path';
```

## 예제

```sql
-- 특정 테이블 전체 백업
BACKUP TABLE sensor_log INTO DISK = '/backup/sensor_log_20240101';

-- 특정 테이블 기간 백업
BACKUP TABLE sensor_log
  FROM TO_DATE('20240101','YYYYMMDD')
  TO   TO_DATE('20240131','YYYYMMDD')
  INTO DISK = '/backup/sensor_log_202401';

-- IBFILE 방식으로 테이블 백업
BACKUP TABLE sensor_log INTO IBFILE = '/backup/sensor_log_20240101.ibf';
```

## 지원 테이블 타입

| 테이블 타입 | BACKUP TABLE 지원 |
|------------|:-----------------:|
| LOG 테이블 | O |
| TAG 테이블 | O |
| LOOKUP 테이블 | O |
| VOLATILE 테이블 | X (메모리 기반) |
| RDB 테이블 | △ (Standard Edition 전용) |

VOLATILE 테이블은 메모리에만 존재하므로 백업이 지원되지 않습니다.

## 마운트를 통한 테이블 복구

테이블 백업 파일을 마운트하여 특정 테이블의 과거 데이터를 조회하거나, 필요한 데이터를 선별하여 현재 데이터베이스에 복사할 수 있습니다.

```sql
-- 테이블 백업 마운트
MOUNT DATABASE '/backup/sensor_log_20240101' TO tbl_backup;

-- 마운트된 테이블에서 데이터 확인
SELECT COUNT(*) FROM tbl_backup.sys.sensor_log;

-- 필요한 데이터만 현재 DB로 복사
INSERT INTO sensor_log
  SELECT * FROM tbl_backup.sys.sensor_log
   WHERE _arrival_time > TO_DATE('20240115','YYYYMMDD');

-- 언마운트
UNMOUNT DATABASE tbl_backup;
```

## 주의 사항

- 테이블 백업으로 생성된 디렉터리에는 해당 테이블의 데이터만 포함됩니다.
- 전체 데이터베이스를 복원하는 용도로는 사용할 수 없습니다.
- 백업 경로가 이미 존재하면 오류가 발생합니다. 고유한 디렉터리 이름을 지정하세요.
