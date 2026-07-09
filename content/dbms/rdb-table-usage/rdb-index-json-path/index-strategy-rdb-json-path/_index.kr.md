---
type: docs
title: 'JSON 경로 인덱스'
weight: 40
---

RDB 테이블에 `JSON` 타입 컬럼이 있는 경우, JSON 경로 인덱스 DDL과 카탈로그 등록을 사용할 수 있습니다. 단, 현재 JSON path 조건은 일반 컬럼 인덱스처럼 쿼리 경로에 푸시다운되지 않을 수 있으므로 실행 계획을 확인해야 합니다.

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

## JSON 경로 조건 쿼리

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

- JSON path 조건이 인덱스 경로로 처리되는지 실행 계획을 확인합니다.
- 중첩 구조가 복잡한 JSON 경로는 선택도가 낮을 수 있습니다.
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
