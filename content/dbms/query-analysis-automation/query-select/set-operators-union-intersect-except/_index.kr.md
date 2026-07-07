---
type: docs
title: '집합 연산: UNION ALL'
weight: 70
---

Machbase는 복수 SELECT 결과를 결합하는 집합 연산으로 `UNION ALL`만 지원합니다.

## UNION ALL

두 SELECT 결과를 중복 포함하여 합칩니다.

```sql
SELECT i1, i2 FROM table_1
UNION ALL
SELECT c1, c2 FROM table_2;
```

### 사용 조건

- 좌측과 우측 SELECT의 **컬럼 수가 동일**해야 합니다.
- 대응하는 컬럼의 **타입이 호환 가능**해야 합니다.
  - 부호 있는 정수 ↔ 부호 없는 정수: 호환 불가
  - 정수 ↔ 실수: 호환 (결과는 실수 타입)
  - 문자열: 길이가 달라도 호환
  - IPv4 ↔ IPv6: 호환 불가
- 결과의 **컬럼명은 좌측 SELECT**의 컬럼명을 사용합니다.

### 예시

```sql
-- 두 날짜 범위의 데이터 합치기
SELECT name, time, value FROM tag
WHERE time BETWEEN '2024-01-01' AND '2024-01-15'
UNION ALL
SELECT name, time, value FROM tag
WHERE time BETWEEN '2024-02-01' AND '2024-02-15';

-- 두 테이블의 데이터 통합
SELECT sensor_id AS id, ts AS time, value FROM sensor_log_2023
UNION ALL
SELECT sensor_id AS id, ts AS time, value FROM sensor_log_2024;

-- 두 집계 결과 합치기
SELECT 'zone-1' AS zone, AVG(value) FROM tag WHERE name LIKE 'ZONE1%' DURATION 1 DAY
UNION ALL
SELECT 'zone-2' AS zone, AVG(value) FROM tag WHERE name LIKE 'ZONE2%' DURATION 1 DAY;
```

## UNION (DISTINCT) 미지원

Machbase는 `UNION ALL`만 지원하며, 중복 제거가 필요한 `UNION` (DISTINCT)은 지원하지 않습니다. 중복 제거가 필요하면 서브쿼리나 애플리케이션 레이어에서 처리하세요.

```sql
-- 미지원
SELECT i1 FROM t1 UNION SELECT i1 FROM t2;
-- → 오류 발생

-- 대안: UNION ALL 후 애플리케이션에서 중복 제거
SELECT DISTINCT * FROM (
    SELECT i1 FROM t1
    UNION ALL
    SELECT i1 FROM t2
);
```

> INTERSECT, EXCEPT(MINUS)도 지원하지 않습니다.
