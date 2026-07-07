---
type: docs
title: '마운트된 데이터베이스 조회'
weight: 90
---

마운트된 데이터베이스는 마운트 이름을 스키마처럼 사용하여 기존 SQL 문법으로 데이터를 조회합니다.

## 테이블 접근 방식

마운트된 DB의 테이블을 참조할 때는 마운트 이름과 소유자 이름을 점(`.`)으로 연결합니다.

```sql
SELECT column_name FROM mount_name.user_name.table_name;
```

예제:

```sql
-- SYS 사용자의 테이블 조회
SELECT * FROM backup_db.sys.sensor_log;

-- 조건 필터링
SELECT * FROM backup_db.sys.sensor_log
 WHERE _arrival_time > TO_DATE('2024-01-15','YYYY-MM-DD')
   AND name = 'sensor_01';

-- 집계
SELECT name, AVG(value) AS avg_val
  FROM backup_db.sys.sensor_log
 WHERE _arrival_time BETWEEN TO_DATE('20240101','YYYYMMDD')
                         AND TO_DATE('20240131','YYYYMMDD')
 GROUP BY name
 ORDER BY name;
```

## 마운트 목록 확인

현재 서버에 마운트된 데이터베이스 목록은 `V$STORAGE_MOUNT_DATABASES` 시스템 뷰에서 확인합니다.

```sql
SELECT * FROM v$storage_mount_databases;
```

| 컬럼 | 설명 |
|------|------|
| `NAME` | 마운트 이름 |
| `PATH` | 백업 디렉터리 경로 |
| `REFCOUNT` | 현재 마운트를 참조 중인 세션 수 |
| `STATE` | 마운트 상태 |

## 조회 시 제약사항

마운트된 데이터베이스는 읽기 전용입니다. 다음 작업은 모두 오류가 발생합니다.

| 불가 작업 | 오류 사유 |
|-----------|-----------|
| `INSERT INTO backup_db.sys.t1 ...` | 마운트 DB는 읽기 전용 |
| `UPDATE backup_db.sys.t1 SET ...` | 마운트 DB는 읽기 전용 |
| `DELETE FROM backup_db.sys.t1 ...` | 마운트 DB는 읽기 전용 |
| `CREATE TABLE backup_db.sys.t2 ...` | 마운트 DB는 읽기 전용 |
| `CREATE INDEX ON backup_db.sys.t1 ...` | 마운트 DB는 읽기 전용 |

## 현재 DB로 데이터 복사

마운트 DB에서 선택한 데이터를 현재 운영 DB로 가져올 수 있습니다.

```sql
-- 마운트 DB의 특정 레코드를 현재 DB에 삽입
INSERT INTO sensor_log (name, time, value)
  SELECT name, time, value
    FROM backup_db.sys.sensor_log
   WHERE _arrival_time BETWEEN TO_DATE('20240115','YYYYMMDD')
                           AND TO_DATE('20240116','YYYYMMDD');
```

## 접근 권한

기본적으로 SYS 사용자만 마운트된 데이터를 읽을 수 있습니다. 일반 사용자에게는 `GRANT MOUNT` 권한을 부여해야 합니다.

```sql
GRANT MOUNT ON machbasedb TO analyst_user;
```
