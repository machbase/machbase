---
type: docs
title: 'VIEW 조회'
weight: 60
---

저장 VIEW는 `CREATE VIEW`로 정의한 논리 객체로, SELECT 문에서 테이블처럼 사용합니다. 자주 쓰는 복잡한 조인이나 조건을 VIEW로 정의하면 쿼리를 단순화하고 재사용성을 높일 수 있습니다.

## VIEW 조회

```sql
-- 저장 VIEW 조회
SELECT * FROM active_alarms;

SELECT sensor_id, location, value
FROM enriched_sensor_data
WHERE value > 80.0;
```

## 저장 VIEW 목록 확인

```sql
SELECT VIEW_NAME, VIEW_TEXT FROM M$SYS_VIEWS;
```

## DESC로 VIEW 구조 확인

```sql
DESC active_alarms;
```

## VIEW 활용 예시

```sql
-- VIEW 정의: TAG + LOOKUP JOIN
CREATE VIEW sensor_with_meta AS
    SELECT t.name, t.time, t.value, l.location, l.dept
    FROM tag t
    LEFT JOIN device_meta l ON t.name = l.sensor_id;

-- VIEW 조회
SELECT name, time, value, location
FROM sensor_with_meta
WHERE time >= DATEADD('h', -1, NOW)
  AND location = 'zone-1';

-- VIEW에 집계 적용
SELECT location, AVG(value) AS avg_temp
FROM sensor_with_meta
WHERE time >= DATEADD('h', -24, NOW)
GROUP BY location
ORDER BY avg_temp DESC;
```

## VIEW의 특성과 제한

- VIEW는 데이터를 물리적으로 저장하지 않습니다. 조회 시마다 정의된 쿼리를 실행합니다.
- INSERT/UPDATE/DELETE를 지원하지 않습니다. 읽기 전용입니다.
- VIEW는 다른 VIEW를 참조할 수 있습니다.
- TAG, LOG, RDB, VOLATILE, LOOKUP 모든 테이블 타입을 VIEW 정의에 포함할 수 있습니다.

> VIEW 생성·삭제 방법은 [5장 스키마·데이터 생명주기](/dbms/schema-data-lifecycle/schema-objects-definition/create-view/)를 참고하세요.
