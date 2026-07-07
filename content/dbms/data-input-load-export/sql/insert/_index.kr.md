---
type: docs
title: 'INSERT 구문'
weight: 10
---

SQL INSERT는 Machbase의 모든 테이블 타입에서 사용할 수 있는 기본 입력 방법입니다.

## 기본 INSERT

```sql
INSERT INTO table_name VALUES (val1, val2, ...);
INSERT INTO table_name (col1, col2) VALUES (val1, val2);
```

지정하지 않은 컬럼은 NULL로 채워집니다.

```sql
-- LOG 테이블 단건 삽입
INSERT INTO sensor_log (sensor_id, ts, value) VALUES ('TEMP-01', NOW, 25.3);

-- TAG 테이블 데이터 삽입
INSERT INTO tag VALUES ('TEMP-01', NOW, 25.3);

-- TAG 메타데이터 삽입
INSERT INTO tag METADATA VALUES ('TEMP-01', 'zone-1', 'R&D');

-- RDB 테이블 삽입
INSERT INTO orders (product, qty, status) VALUES ('Widget', 10, 'PENDING');

-- VOLATILE 테이블 삽입
INSERT INTO device_status VALUES ('DEV-01', 'NORMAL', 23.5, NOW);

-- LOOKUP 테이블 삽입
INSERT INTO alarm_threshold VALUES ('TEMP-01', 85.0, 5.0);
```

## NOW 키워드

`NOW`는 현재 서버 시각을 나타냅니다. DATETIME 타입 컬럼에 사용합니다.

```sql
INSERT INTO sensor_log VALUES ('TEMP-01', NOW, 25.3);
```

## INSERT SELECT

다른 테이블이나 쿼리 결과를 삽입합니다.

```sql
-- 테이블 간 데이터 복사
INSERT INTO archive_log SELECT * FROM sensor_log;

-- 조건부 복사
INSERT INTO error_log
SELECT sensor_id, ts, value FROM sensor_log WHERE value > 100.0;

-- _ARRIVAL_TIME을 보존하여 복사
INSERT INTO archive_log (_arrival_time, sensor_id, ts, value)
SELECT _arrival_time, sensor_id, ts, value FROM sensor_log;
```

### INSERT SELECT 주의사항

- `_ARRIVAL_TIME` 컬럼을 명시하지 않으면 INSERT 실행 시점의 시각이 자동 부여됩니다.
- `_ARRIVAL_TIME`을 명시한 경우, 지정값이 테이블에 이미 존재하는 가장 최신 `_ARRIVAL_TIME`보다 이전이면 해당 행은 입력되지 않습니다.
- 수행 중 오류가 발생해도 ROLLBACK되지 않습니다 (부분 성공 가능).
- VARCHAR 컬럼의 최대 길이를 초과하는 값은 자동으로 잘립니다.
- 형 변환이 필요한 경우 묵시적 변환이 적용됩니다. 변환 불가 시 해당 행은 건너뜁니다.

## INSERT ON DUPLICATE KEY UPDATE (UPSERT)

PRIMARY KEY가 지정된 VOLATILE 테이블에서 PK 중복 시 자동 UPDATE되는 구문입니다.

```sql
-- PK 중복 없으면 INSERT, 있으면 UPDATE
INSERT INTO device_status VALUES ('DEV-01', 'ALARM', 95.3, NOW)
ON DUPLICATE KEY UPDATE status = 'ALARM', value = 95.3, updated_at = NOW;

-- SET 절로 삽입값과 다른 값 업데이트
INSERT INTO device_status VALUES ('DEV-02', 'NORMAL', 23.5, NOW)
ON DUPLICATE KEY UPDATE SET value = value + 1;
```

## 다건 INSERT (일부 방언)

```sql
-- 다건 한 번에 삽입 (Machbase 지원)
INSERT INTO sensor_log VALUES
    ('TEMP-01', NOW, 25.3),
    ('TEMP-02', NOW, 27.1),
    ('TEMP-03', NOW, 22.8);
```

## machsql에서 사용

```bash
machsql -s 127.0.0.1 -u SYS -p MANAGER
Mach> INSERT INTO sensor_log VALUES ('TEMP-01', NOW, 25.3);
1 row(s) inserted.
```
