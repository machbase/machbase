---
type: docs
title: 'JSON 경로 인덱스'
weight: 40
---

RDB 테이블에 `JSON` 타입 컬럼이 있는 경우, JSON 경로에 대해 인덱스를 생성하여 JSON 필드 기반 조회 성능을 향상시킬 수 있습니다.

## JSON 컬럼 스키마

```sql
CREATE RDB TABLE device_state (
    device_id VARCHAR(64),
    ts        DATETIME,
    state     JSON,
    region    VARCHAR(32)
);
```

## JSON 경로 인덱스 생성

```sql
-- JSON 경로 인덱스: state.status 필드
CREATE INDEX idx_state_status ON device_state(state->'$.status');

-- JSON 경로 인덱스: state.code 필드
CREATE INDEX idx_state_code ON device_state(state->'$.code');
```

## JSON 경로 인덱스를 활용하는 쿼리

```sql
-- state.status 값이 'ALARM'인 디바이스 조회
SELECT device_id, ts, state
FROM device_state
WHERE state->'$.status' = 'ALARM';

-- 복합 조건
SELECT device_id, ts
FROM device_state
WHERE region = 'KR'
  AND state->'$.code' = '500';
```

## 주의사항

- JSON 경로 인덱스는 해당 경로의 값이 문자열 또는 숫자인 경우에 효과적입니다.
- 중첩 구조가 복잡한 JSON 경로는 인덱스 선택도가 낮을 수 있습니다.
- 자주 조회하는 JSON 필드는 별도 컬럼으로 추출하여 일반 인덱스를 사용하는 것이 더 효율적인 경우가 많습니다.

```sql
-- 더 효율적인 패턴: JSON 필드를 컬럼으로 분리
CREATE RDB TABLE device_state_v2 (
    device_id VARCHAR(64),
    ts        DATETIME,
    status    VARCHAR(16),   -- JSON에서 추출한 필드
    code      INTEGER,       -- JSON에서 추출한 필드
    region    VARCHAR(32),
    extra     JSON           -- 나머지 속성
);

CREATE INDEX idx_ds_status ON device_state_v2(status);
```
