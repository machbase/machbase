---
type: docs
title: 'INSERT·UPDATE 패턴'
weight: 70
---

Machbase 테이블 타입별로 데이터를 삽입·수정하는 패턴을 정리합니다.

## 테이블 타입별 쓰기 패턴

| 테이블 타입 | INSERT | UPDATE | DELETE | UPSERT |
|-----------|--------|--------|--------|--------|
| TAG | INSERT / Append API | X | X | X |
| LOG | INSERT / Append API | X | X | X |
| RDB | INSERT | X | O | DELETE+INSERT |
| LOOKUP | INSERT | O (by PK) | O (by PK) | DELETE+INSERT |
| VOLATILE | INSERT | X | O | ON DUPLICATE KEY UPDATE |

## TAG/LOG: Append API 패턴

```go
// Go SDK - Append API (고속 대량 입력)
appender, _ := conn.Appender(ctx, "sensor_data")
for _, row := range rows {
    appender.Append(row.Name, row.Time, row.Value)
}
appender.Close()
```

## RDB: DELETE + INSERT 패턴

```sql
-- UPDATE 미지원이므로 DELETE + INSERT
BEGIN;
DELETE FROM order_history WHERE order_id = 1001;
INSERT INTO order_history VALUES (1001, 'CUST-001', 5, 59.99, NOW, 'UPDATED');
COMMIT;
```

## VOLATILE: ON DUPLICATE KEY UPDATE 패턴

```sql
INSERT INTO device_status VALUES ('DEV-01', 'ALARM', 95.3, NOW)
ON DUPLICATE KEY UPDATE status = 'ALARM', value = 95.3, updated_at = NOW;
```

## LOOKUP: UPDATE 패턴

```sql
-- PRIMARY KEY 기준 직접 UPDATE
UPDATE alarm_threshold SET high_limit = 90.0, updated_at = NOW
WHERE sensor_id = 'TEMP-01';
```

## 대량 초기 로드 패턴

```sql
-- machloader로 CSV 파일 대량 로드
-- bash: machloader -i -d table_name -f data.csv
```
