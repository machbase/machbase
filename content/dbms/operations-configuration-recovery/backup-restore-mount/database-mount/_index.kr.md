---
type: docs
title: '데이터베이스 마운트'
weight: 80
---

데이터베이스 마운트는 서버를 중단하거나 데이터를 복원하지 않고 백업 데이터베이스를 현재 서버에 연결하여 읽기 전용으로 접근하는 기능입니다.

## 마운트가 필요한 상황

- 운영 서버를 중단하지 않고 특정 시점의 과거 데이터를 확인해야 할 때
- 아카이브된 오래된 데이터에서 일부 레코드를 추출해야 할 때
- 백업 데이터를 복원 없이 빠르게 조회해야 할 때

## MOUNT DATABASE

```sql
MOUNT DATABASE 'backup_database_path' TO mount_name;
```

- `backup_database_path`: DISK 방식으로 생성된 백업 디렉터리 경로 (절대/상대 경로 모두 가능)
- `mount_name`: 마운트된 DB에 접근할 때 사용할 이름

```sql
-- 절대 경로로 마운트
MOUNT DATABASE '/backup/machbase_20240101' TO backup_db;

-- 상대 경로 (MACHBASE_HOME/dbs 기준)
MOUNT DATABASE 'machbase_20240101' TO backup_db;
```

## 마운트된 DB에서 데이터 조회

마운트된 데이터베이스의 테이블에 접근할 때는 `mount_name.user_name.table_name` 형식을 사용합니다.

```sql
-- 마운트 DB의 특정 테이블 조회
SELECT * FROM backup_db.sys.sensor_log
 WHERE _arrival_time > TO_DATE('2024-01-01','YYYY-MM-DD');

-- 집계 쿼리
SELECT name, COUNT(*), MIN(value), MAX(value)
  FROM backup_db.sys.sensor_log
 WHERE _arrival_time BETWEEN TO_DATE('20240101','YYYYMMDD')
                         AND TO_DATE('20240131','YYYYMMDD')
 GROUP BY name;

-- 현재 DB와 마운트 DB를 함께 조회
SELECT a.name, a.value AS current_value, b.value AS backup_value
  FROM sensor_log a
  JOIN backup_db.sys.sensor_log b ON a.name = b.name
 WHERE a._arrival_time > TO_DATE('20240201','YYYYMMDD');
```

## UNMOUNT DATABASE

마운트된 데이터베이스가 더 이상 필요 없으면 언마운트합니다.

```sql
UNMOUNT DATABASE mount_name;
```

```sql
-- 예제
UNMOUNT DATABASE backup_db;
```

언마운트는 해당 마운트 DB를 참조 중인 열린 커서나 실행 중인 문장이 없을 때 즉시 실행됩니다. 마운트 DB를 참조 중이면 언마운트가 실패할 수 있으므로, 해당 문장과 세션을 종료한 뒤 다시 실행합니다.

## 마운트 조건

마운트 명령을 실행하려면 다음 조건을 충족해야 합니다.

- 백업 데이터베이스의 버전과 현재 서버의 메타데이터 버전이 호환되어야 합니다.
- DISK 방식으로 생성된 백업만 마운트할 수 있습니다 (IBFILE 방식 불가).
- 마운트된 DB에서는 테이블 생성, 인덱스 생성/삭제, 데이터 추가/삭제가 불가능합니다 (읽기 전용).

## 마운트 권한

일반 사용자가 `MOUNT DATABASE` 또는 `UNMOUNT DATABASE`를 실행하려면 권한이 필요합니다.

```sql
-- SYS 사용자가 권한 부여
GRANT MOUNT ON machbasedb TO user_name;
```

## 에디션 참고

Cluster Edition에서는 `MOUNT` 및 `UNMOUNT` 문이 거부될 수 있습니다. 마운트 기능은 주로 Standard Edition 환경에서 사용합니다.
