---
type: docs
title: '7.12.1.1 REGEXP / NOT REGEXP'
weight: 10
---

`REGEXP`는 정규 표현식 패턴으로 컬럼 값을 필터링합니다.

## 구문

```text
column REGEXP 'pattern'
column NOT REGEXP 'pattern'
```

## 예시

```sql
-- 'time'을 포함하는 값
SELECT * FROM sensor_log WHERE sensor_id REGEXP 'time';

-- 숫자로 끝나는 sensor_id
SELECT * FROM sensor_log WHERE sensor_id REGEXP 'TEMP[0-9]+';

-- 특정 패턴 NOT REGEXP
SELECT * FROM sensor_log WHERE sensor_id NOT REGEXP 'TEMP[12]';

-- 정확한 패턴 매칭
SELECT 'abcde' REGEXP 'a[bcd]{1,10}e';  -- → 1 (true)

-- 복수 조건 조합
SELECT * FROM event_log
WHERE message REGEXP 'error|timeout'
  AND source REGEXP '^app\\.';
```

## 성능 주의사항

REGEXP는 인덱스를 사용할 수 없습니다. 전체 스캔이 발생하므로 다음 전략을 사용하세요.

1. **SEARCH/ESEARCH로 1차 필터링** 후 REGEXP로 정밀 검색:

```sql
-- 1단계: KEYWORD 인덱스로 범위 축소
-- 2단계: 범위가 줄어든 상태에서 REGEXP 적용
SELECT * FROM event_log
WHERE message SEARCH 'error'    -- 인덱스 사용
  AND message REGEXP 'ERR-[0-9]{4}';  -- 정밀 필터
```

2. **시간 범위 먼저 지정**:
```sql
SELECT * FROM event_log
WHERE ts >= NOW - 3600000000000    -- 시간 조건으로 범위 축소
  AND message REGEXP 'CRITICAL.*timeout';
```

## 지원 정규식 문법

Machbase는 POSIX 확장 정규 표현식(ERE)을 지원합니다.

| 패턴 | 의미 |
|------|------|
| `.` | 임의의 한 문자 |
| `*` | 0회 이상 반복 |
| `+` | 1회 이상 반복 |
| `?` | 0 또는 1회 |
| `[abc]` | a, b, c 중 하나 |
| `[^abc]` | a, b, c가 아닌 문자 |
| `^` | 문자열 시작 |
| `$` | 문자열 끝 |
| `{m,n}` | m~n회 반복 |
| `(abc)` | 그룹 |
| `a\|b` | a 또는 b |
