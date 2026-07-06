---
type: docs
title: 'Red-Black 트리 인덱스'
weight: 50
---

VOLATILE 테이블의 인덱스는 메모리 내 Red-Black 트리를 사용합니다. 디스크 기반 인덱스와 달리 순수 메모리 연산으로 빠른 조회를 지원합니다.

## 인덱스 특성

| 항목 | Red-Black 트리 인덱스 |
|------|----------------------|
| 저장 위치 | 메모리 |
| 자료구조 | 자기 균형 이진 탐색 트리 |
| 시간 복잡도 | O(log n) |
| 범위 조회 | 지원 |
| 서버 재시작 후 유지 | X |

## PRIMARY KEY 자동 인덱스

PRIMARY KEY 컬럼에는 자동으로 Red-Black 트리 인덱스가 생성됩니다.

```sql
CREATE VOLATILE TABLE sensor_cache (
    sensor_id VARCHAR(64) PRIMARY KEY,  -- 자동 인덱스
    value     DOUBLE,
    ts        DATETIME
);

-- PK 기반 빠른 조회 (Red-Black 트리 인덱스 사용)
SELECT value FROM sensor_cache WHERE sensor_id = 'TEMP-01';
```

## 보조 인덱스

PRIMARY KEY 외 컬럼에도 인덱스를 생성할 수 있습니다.

```sql
-- 보조 인덱스 생성
CREATE INDEX idx_cache_ts ON sensor_cache(ts);

-- 범위 조회 (인덱스 활용)
SELECT sensor_id, value FROM sensor_cache
WHERE ts >= '2024-01-01 10:00:00' AND ts < '2024-01-01 11:00:00';
```

## 주의사항

- 모든 인덱스는 메모리에 저장됩니다. 데이터량이 많을수록 메모리 사용량이 증가합니다.
- 서버 재시작 시 인덱스도 함께 소멸됩니다.
