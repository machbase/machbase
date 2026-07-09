---
type: docs
title: 'TAG data UPDATE SET 대상 컬럼 오류'
weight: 20
---

TAG data UPDATE의 SET 절은 실제 데이터 컬럼만 대상으로 합니다. PRIMARY KEY, BASETIME,
메타데이터 컬럼을 SET 대상으로 지정하면 오류가 발생합니다.

{{< callout type="warning" >}}
**SET 대상**

`value`와 사용자 데이터 컬럼은 UPDATE할 수 있습니다. `name`, `time`, METADATA 블록의 컬럼은
TAG data UPDATE의 SET 대상이 아닙니다.
{{< /callout >}}

## 증상

```sql
-- 오류: PRIMARY KEY 컬럼(name) 업데이트 시도
UPDATE sensor_tag
   SET name = 'new-sensor'
 WHERE name = 'old-sensor'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');

-- 오류: BASETIME 컬럼(time) 업데이트 시도
UPDATE sensor_tag
   SET time = NOW
 WHERE name = 'sensor-01'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');

-- 오류: 메타데이터 컬럼을 data UPDATE에서 수정
UPDATE sensor_tag
   SET location = 'zone-2'
 WHERE name = 'sensor-01'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');
```

## 컬럼 유형별 UPDATE 가능 여부

| 컬럼 유형 | 설명 | data UPDATE |
|-----------|------|:-----------:|
| PRIMARY KEY (`name`) | TAG를 식별하는 고유 키 | X |
| BASETIME (`time`) | 시계열 데이터의 타임스탬프 | X |
| 데이터 컬럼 (`value`, 보조 컬럼) | 실제 row 값 | O |
| `SUMMARIZED` 데이터 컬럼 | 통계 대상 데이터 컬럼 | O |
| 메타데이터 컬럼 | METADATA 블록의 태그 속성 | X |

## 해결 방법

데이터 값은 일반 UPDATE로 수정합니다.

```sql
UPDATE sensor_tag
   SET value = 99.9,
       status = 1
 WHERE name = 'sensor-01'
   AND time = TO_DATE('2026-07-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

메타데이터는 별도 구문을 사용합니다.

```sql
UPDATE sensor_tag METADATA
   SET location = 'zone-2'
 WHERE name = 'sensor-01';
```

태그 이름이나 시간 축을 변경해야 하는 경우에는 새 `name`/`time` 값으로 데이터를 삽입한 뒤
운영 정책에 따라 기존 데이터를 삭제합니다.
