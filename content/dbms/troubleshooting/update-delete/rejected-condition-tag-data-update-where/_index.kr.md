---
type: docs
title: 'TAG data UPDATE WHERE 조건 오류'
weight: 10
---

TAG data UPDATE는 지원되지만 WHERE 절에 태그 선택 조건과 BASETIME 조건이 모두 있어야 합니다.
조건이 모호하거나 허용되지 않는 형태이면 UPDATE가 거부됩니다.

{{< callout type="warning" >}}
**필수 조건**

`WHERE name ...` 형태의 태그 선택 조건과 `time ...` 형태의 BASETIME 조건을 함께 지정합니다.
조건 없는 전체 UPDATE, 태그 조건만 있는 UPDATE, 시간 조건만 있는 UPDATE는 허용되지 않습니다.
{{< /callout >}}

## 증상

다음과 같은 UPDATE가 오류로 거부됩니다.

```sql
-- 시간 조건 없음
UPDATE sensor_tag SET value = 99.9
WHERE name = 'sensor-01';

-- 태그 선택 조건 없음
UPDATE sensor_tag SET value = 99.9
WHERE time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');

-- OR 조건 사용
UPDATE sensor_tag SET value = 99.9
WHERE name = 'sensor-01'
   OR name = 'sensor-02';
```

## 원인

TAG data UPDATE는 내부적으로 대상 태그와 시간 범위를 먼저 결정합니다. 대상 범위를 안정적으로
결정할 수 없는 조건은 거부됩니다.

| 조건 형태 | 지원 여부 |
|-----------|:--------:|
| `name = 'sensor-01' AND time >= ...` | O |
| `name IN ('sensor-01', 'sensor-02') AND time BETWEEN ...` | O |
| `name LIKE 'sensor-%' AND time < ...` | O |
| `value > 10`만 사용 | X |
| `name = 'sensor-01'`만 사용 | X |
| `time >= ...`만 사용 | X |
| `OR`, 서브쿼리, 집계 조건 | X |

## 해결 방법

태그 선택 조건과 시간 조건을 함께 명시합니다.

```sql
UPDATE sensor_tag
   SET value = 99.9
 WHERE name = 'sensor-01'
   AND time = TO_DATE('2026-07-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS');

UPDATE sensor_tag
   SET status = 1
 WHERE name IN ('sensor-01', 'sensor-02')
   AND time >= TO_DATE('2026-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND time <  TO_DATE('2026-07-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

대량 UPDATE 전에는 같은 WHERE 조건으로 `SELECT COUNT(*)`를 실행해 수정 대상 row 수를
확인합니다.
