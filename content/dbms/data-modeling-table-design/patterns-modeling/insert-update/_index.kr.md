---
type: docs
title: '4.3.7 INSERT·UPDATE 패턴'
weight: 70
---

Machbase 테이블 타입별로 데이터를 삽입·수정하는 패턴을 정리합니다.

## 테이블 타입별 쓰기 패턴

| 테이블 타입 | INSERT | UPDATE | DELETE | UPSERT |
|-----------|--------|--------|--------|--------|
| TAG | INSERT / Append API | O (태그/시간 조건) | O | X |
| LOG | INSERT / Append API | X | O (BEFORE/OLDEST/EXCEPT) | X |
| RDB | INSERT / SDK Append API | O (WHERE 유무 모두) | O | DELETE+INSERT |
| LOOKUP | INSERT / Append API | O (by PK) | O (by PK) | DELETE+INSERT |
| VOLATILE | INSERT | O (by PK) | O | ON DUPLICATE KEY UPDATE |

## TAG/LOG: Append API 패턴 (고속 입력)

```go
// Go SDK - Append API (초고속 대량 입력)
appender, _ := conn.Appender(ctx, "sensor_data")
for _, row := range rows {
    appender.Append(row.Name, row.Time, row.Value)
}
appender.Close()
```

## TAG: UPDATE 패턴

TAG data UPDATE는 태그 선택 조건과 BASETIME 조건을 함께 사용합니다.

```sql
UPDATE sensor_data
   SET value = value + 1
 WHERE name = 'sensor-01'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');
```

## RDB: UPDATE 패턴

RDB 테이블은 일반 SQL UPDATE를 지원합니다.

```sql
-- WHERE 조건 UPDATE
UPDATE orders SET status = 'SHIPPED' WHERE order_id = 1001;

-- 자기 참조 UPDATE
UPDATE inventory SET qty = qty - 5 WHERE item_id = 42;

-- 전체 행 UPDATE (WHERE 없음)
UPDATE product_catalog SET discount = 0;
```

## VOLATILE: UPDATE 패턴

VOLATILE 테이블은 일반 UPDATE와 ON DUPLICATE KEY UPDATE를 모두 지원합니다.

```sql
-- 일반 UPDATE (WHERE 조건)
UPDATE device_status SET status = 'NORMAL', value = 23.5 WHERE device_id = 'DEV-01';

-- UPSERT: ON DUPLICATE KEY UPDATE (PK 중복 시 자동 UPDATE)
INSERT INTO device_status VALUES ('DEV-01', 'ALARM', 95.3, NOW)
ON DUPLICATE KEY UPDATE SET status = 'ALARM', value = 95.3, updated_at = NOW;
```

## LOOKUP: UPDATE 패턴

```sql
-- PRIMARY KEY 기준 직접 UPDATE
UPDATE alarm_threshold SET high_limit = 90.0, updated_at = NOW
WHERE sensor_id = 'TEMP-01';
```

## 대량 초기 로드 패턴

```bash
# machloader로 CSV 파일 대량 로드
machloader -i -d table_name -f data.csv
```
