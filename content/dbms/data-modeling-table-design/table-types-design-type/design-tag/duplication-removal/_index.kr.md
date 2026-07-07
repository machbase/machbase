---
type: docs
title: '자동 중복 제거'
weight: 90
---

TAG 테이블은 동일한 태그·시간 조합의 데이터가 반복 입력될 때 설정된 시간 창 내에서 중복을 자동으로 제거하는 기능을 제공합니다.

## 설정: TAG_DUPLICATE_CHECK_DURATION

테이블 생성 시 `TAG_DUPLICATE_CHECK_DURATION` 속성으로 중복 제거 기간(분 단위)을 지정합니다.

```sql
-- 1440분(24시간) 이내 중복 자동 제거
CREATE TAG TABLE tag (
    name  VARCHAR(20) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) TAG_DUPLICATE_CHECK_DURATION = 1440;
```

새로 삽입된 데이터의 시간이 현재 서버 시각으로부터 설정된 기간 내에 이미 존재하는 데이터와 동일하면, 해당 행은 삽입되지 않습니다.

## 동작 예시

```sql
-- 동일 시각 데이터를 두 번 삽입
INSERT INTO tag VALUES ('tag1', DATE_TRUNC('day', NOW), 0);
INSERT INTO tag VALUES ('tag1', DATE_TRUNC('day', NOW), 0);  -- 중복 → 무시됨

EXEC TABLE_FLUSH(tag);

-- 결과: 1건만 저장됨
SELECT * FROM tag WHERE name = 'tag1';
```

`INSERT` 직후 같은 세션에서 태그 이름 조건으로 결과를 확인할 때는 `EXEC TABLE_FLUSH`를 먼저 실행합니다. Flush 전에는 전체 조회에서는 보이더라도 태그 이름 조건 조회가 아직 인덱스에 반영되지 않을 수 있습니다.

## 설정 변경

생성 후에도 변경할 수 있습니다.

```sql
ALTER TABLE tag SET TAG_DUPLICATE_CHECK_DURATION = 2880;  -- 48시간으로 변경
```

현재 설정값 확인:

```sql
SELECT * FROM m$sys_table_property
WHERE name = 'TAG_DUPLICATE_CHECK_DURATION';
```

## 제약 사항

| 항목 | 내용 |
|------|------|
| 최대 기간 | 43,200분 (30일) |
| 단위 | 분(minute) |
| 기본값 | 0 (중복 제거 비활성) |

- 기간이 0이면 중복 제거가 동작하지 않습니다.
- 중복 제거로 무시된 데이터가 이후 삭제되어 빈 자리가 생겨도, 그 자리에 동일 데이터를 재입력할 때는 중복으로 간주하지 않습니다.

## TRACE 로그로 중복 제거 확인

`TRACE_LOG_LEVEL`에 32(SM_2)를 추가하면 중복 제거 시 로그가 출력됩니다.

```sql
-- 현재 레벨 확인
SELECT name, value FROM v$property WHERE name = 'TRACE_LOG_LEVEL';

-- 32 추가 (예: 기존 277이면 277 + 32 = 309)
ALTER SYSTEM SET TRACE_LOG_LEVEL = 309;
```

로그 위치: `$MACHBASE_HOME/trc/machbase.trc`

```bash
tail -f $MACHBASE_HOME/trc/machbase.trc | grep DUP_DROP
```

로그 포맷: `DUP_DROP Table=<테이블명> TAG=<tag id> TIME=<시간> COL<n>=<값>`

```
[SM-INFO] DUP_DROP Table=TAG TAG=1 TIME=1998-12-24 09:00:00 000:000:012 COL3=12.000000
```
