---
type: docs
title: '7.11.1.3 LIKE / NOT LIKE'
weight: 30
---

`LIKE`는 SQL 표준 패턴 매칭 연산자입니다. 인덱스를 사용하지 않으므로 대용량 테이블에서는 성능에 주의가 필요합니다.

## 패턴 문자

| 문자 | 의미 |
|------|------|
| `%` | 0개 이상의 임의 문자 |
| `_` | 정확히 1개의 임의 문자 |

## 예시

```sql
-- 'TEMP'로 시작하는 sensor_id
SELECT * FROM sensor_log WHERE sensor_id LIKE 'TEMP%';

-- '-01'로 끝나는 sensor_id
SELECT * FROM sensor_log WHERE sensor_id LIKE '%-01';

-- 중간에 'ERR' 포함
SELECT * FROM event_log WHERE message LIKE '%ERR%';

-- 4자리 코드 패턴 (___)
SELECT * FROM sensor_log WHERE code LIKE 'T___';
```

## NOT LIKE

```sql
-- 'TEMP'로 시작하지 않는 센서
SELECT * FROM sensor_log WHERE sensor_id NOT LIKE 'TEMP%';
```

## 성능 고려사항

- `LIKE '%pattern'` 또는 `LIKE '%pattern%'`처럼 앞에 `%`가 오면 인덱스를 사용할 수 없어 전체 스캔이 발생합니다.
- 대용량 LOG/TAG 테이블의 VARCHAR 컬럼에 자주 검색한다면 KEYWORD 인덱스를 생성하고 `SEARCH` 또는 `ESEARCH`를 사용하는 것이 성능상 유리합니다.
- 앞쪽이 고정된 패턴(`LIKE 'prefix%'`)이라면 인덱스가 있을 경우 활용될 수 있습니다.
