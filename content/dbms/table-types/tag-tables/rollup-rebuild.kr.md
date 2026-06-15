---
title: 'Rollup Rebuild 사용자 가이드'
type: docs
weight: 63
toc: true
---

## 개요

이상 데이터가 수집되면 원본 데이터는 삭제 후 정상 데이터로 다시 넣을 수 있지만, 이미 생성된 rollup 통계는 자동으로 되감기지 않습니다.
이 경우 영향 버킷의 rollup 데이터를 다시 만들어야 합니다.

Machbase 환경에서는 서버 내장 Procedure `EXEC ROLLUP_REBUILD(...)`로 rollup을 재구성합니다.

- built-in rollup + rollup extension + custom rollup 대상
- SQL에서 직접 호출 가능
- custom rollup dependency tree를 따라 stop/rebuild/start 수행

## 제약사항

`EXEC ROLLUP_REBUILD(...)`에는 아래 제약이 있습니다.

1. standard edition에서 지원하며, **cluster edition에서는 지원하지 않습니다.**
2. `table_name`, `tag_name`, `begin_time`, `end_time` 기준의 단일 tag rebuild만 지원합니다.
3. rebuild 대상 구간은 부분 시간이 아니라 영향 버킷 전체를 기준으로 delete 후 insert 해야 합니다.

## Rollup Rebuild 프로시저 사용법

### 호출 문법

```sql
EXEC ROLLUP_REBUILD(table_name, tag_name, begin_time, end_time);
```

예:

```sql
EXEC ROLLUP_REBUILD(tag,
                    'tag-00045',
                    TO_DATE('2025-09-02 01:00:00'),
                    TO_DATE('2025-09-02 01:00:00'));

EXEC ROLLUP_REBUILD(sys.tag,
                    'tag-00045',
                    TO_DATE('2025-09-02 01:00:00'),
                    TO_DATE('2025-09-02 01:00:00'));
```

### 매개변수 의미

1. `table_name`
   - 대상 source TAG 테이블 이름
   - 필요 시 `schema.table` 형태 사용
2. `tag_name`
   - 재구성 대상 tag key 값
3. `begin_time`
   - 이상 데이터 보정 시작 시각
4. `end_time`
   - 이상 데이터 보정 종료 시각

### 적용 범위

- built-in rollup
- rollup extension
- custom rollup
- rollup-on-rollup dependency 환경

## Custom Rollup Rebuild 원리

### 왜 built-in처럼 고정 SQL로 처리할 수 없는가

custom rollup은 아래가 모두 사용자 정의입니다.

- destination table 이름
- destination 컬럼 수와 타입
- 집계 함수
- source가 root table인지, 다른 rollup destination인지

따라서 범용 rebuild는 "고정 스키마 재삽입"이 아니라 "원래 custom SELECT를 다시 실행하되, tag/time 버킷만 좁혀서 다시 넣는 방식"이어야 합니다.

### 버킷 경계 확장

예를 들어 1분 custom rollup에서 원본 이상 구간이 아래와 같다고 가정합니다.

- 원본 오류 시간: `2026-01-27 09:30:12` ~ `2026-01-27 09:31:07`

실제 rebuild 대상은 아래처럼 버킷 전체입니다.

- 시작 버킷: `2026-01-27 09:30:00`
- 종료 버킷: `2026-01-27 09:31:59.999999999`

부분 집계 row가 destination table에 이미 있을 수 있으므로, 삭제 없이 다시 insert만 하면 중복 집계가 발생합니다.
항상 대상 버킷을 먼저 삭제한 뒤 다시 insert 해야 합니다.

### 수동 rebuild 절차

프로시저를 사용하지 않고 수동으로 하려면 아래 절차를 따라야 합니다.

1. 영향 받는 모든 custom rollup stop
2. source 이상 데이터 수정 또는 재적재
3. 버킷 경계 계산
4. destination delete
5. 원래 `CREATE ROLLUP ... AS (SELECT ...)`와 같은 집계식으로 재insert
6. destination flush
7. 상위 custom rollup이 있으면 하위부터 차례대로 반복
8. rollup start

## Custom Rollup 수동 Rebuild 예제

### 1분 custom rollup

아래는 `stock_tick -> stock_rollup_1m`에 대해 `09:30` ~ `09:31` 버킷을 다시 만드는 예제입니다.

```sql
STOP ROLLUP rollup_stock_1m;

DELETE FROM stock_rollup_1m
WHERE time BETWEEN TO_DATE('2026-01-27 09:30:00')
               AND TO_DATE('2026-01-27 09:31:59');

INSERT INTO stock_rollup_1m
SELECT code,
       DATE_TRUNC('minute', time) AS time,
       SUM(price)                 AS sum_price,
       SUM(volume)                AS sum_volume,
       COUNT(*)                   AS cnt
FROM stock_tick
WHERE time BETWEEN TO_DATE('2026-01-27 09:30:00')
               AND TO_DATE('2026-01-27 09:31:59')
GROUP BY code, time;

EXEC TABLE_FLUSH('stock_rollup_1m');
START ROLLUP rollup_stock_1m;
```

### FIRST/LAST 가 있는 custom rollup

`FIRST/LAST`를 쓰는 custom rollup은 보조 시간 컬럼도 같이 다시 계산해야 합니다.

```sql
STOP ROLLUP rollup_stock_candle_1m;

DELETE FROM stock_candle_1m
WHERE time = TO_DATE('2026-01-27 09:30:00');

INSERT INTO stock_candle_1m
SELECT code,
       DATE_TRUNC('minute', time) AS time,
       MIN(time)                  AS firsttime,
       MAX(time)                  AS lasttime,
       FIRST(time, price)         AS open,
       MAX(price)                 AS high,
       MIN(price)                 AS low,
       LAST(time, price)          AS close,
       SUM(volume)                AS volume,
       COUNT(*)                   AS cnt
FROM stock_tick
WHERE time BETWEEN TO_DATE('2026-01-27 09:30:00')
               AND TO_DATE('2026-01-27 09:30:59')
GROUP BY code, time;

EXEC TABLE_FLUSH('stock_candle_1m');
START ROLLUP rollup_stock_candle_1m;
```

최종 조회는 기존과 동일하게 `FIRST(firsttime, open)`, `LAST(lasttime, close)`로 재병합해야 합니다.

### rollup-on-rollup 순서

예:

- 1차: `stock_tick -> stock_rollup_1m`
- 2차: `stock_rollup_1m -> stock_rollup_1h`

rebuild 순서는 반드시 하위부터입니다.

1. `stock_rollup_1h` stop
2. `stock_rollup_1m` stop
3. `stock_rollup_1m` rebuild
4. `stock_rollup_1h` delete / rebuild
5. `stock_rollup_1m` start
6. `stock_rollup_1h` start

상위를 먼저 재구성하면 아직 복원되지 않은 하위 결과를 읽게 되어 다시 잘못된 집계가 들어갑니다.

## 운영 권장사항

1. custom rollup rebuild 전에는 먼저 영향 버킷 범위를 확인합니다.
2. 운영 적용 전후에 `v$rollup`으로 dependency를 확인합니다.
3. custom rollup destination table은 append-only 결과가 누적되므로 rebuild 시 반드시 delete 후 insert 합니다.
4. rollup-on-rollup 구조에서는 반드시 하위부터 rebuild 하고, 이후 상위를 재구성합니다.
5. 오류 구간이 여러 버킷에 걸치면 전체 범위를 지정해서 `EXEC ROLLUP_REBUILD(...)`를 호출합니다.

## 최신 데이터를 포함한 효율적인 Rollup 질의 정리

앞서 설명한 최신 데이터 조회 원칙은 built-in rollup과 custom rollup 모두 동일합니다.

핵심 규칙:

1. 안정 구간은 rollup table 사용
2. 최근 구간은 source table 직접 집계
3. 두 결과를 `UNION ALL`
4. 필요하면 바깥에서 한 번 더 최종 집계

### 일반 1분 rollup 예

```sql
SELECT ROLLUP('minute', 1, time) AS mtime, AVG(value)
FROM tag
WHERE name = 'TAG_0001'
  AND time < DATE_TRUNC('minute', SYSDATE) - 2m
GROUP BY mtime

UNION ALL

SELECT DATE_TRUNC('minute', time) AS mtime, AVG(value)
FROM tag
WHERE name = 'TAG_0001'
  AND time >= DATE_TRUNC('minute', SYSDATE) - 2m
GROUP BY mtime;
```

### 일반 20분 집계 예

```sql
SELECT ROLLUP('minute', 20, time) AS mtime, AVG(value)
FROM tag
WHERE name = 'TAG_0001'
  AND time < DATE_BIN('minute', 20, SYSDATE, 0) - 20m
GROUP BY mtime

UNION ALL

SELECT DATE_BIN('minute', 20, time, 0) AS mtime, AVG(value)
FROM tag
WHERE name = 'TAG_0001'
  AND time >= DATE_BIN('minute', 20, SYSDATE, 0) - 20m
GROUP BY mtime;
```

### custom rollup 예

custom rollup도 동일합니다. 단, rollup 쪽은 destination table을 읽고, 최근 구간은 source를 직접 다시 집계합니다.

```sql
SELECT code, time,
       SUM(sum_price) / SUM(cnt) AS avg_price
FROM (
      SELECT code, time,
             SUM(sum_price) AS sum_price,
             SUM(cnt)       AS cnt
      FROM stock_rollup_1m
      WHERE time < DATE_TRUNC('minute', SYSDATE) - 2m
      GROUP BY code, time

      UNION ALL

      SELECT code,
             DATE_TRUNC('minute', time) AS time,
             SUM(price)                 AS sum_price,
             COUNT(*)                   AS cnt
      FROM stock_tick
      WHERE time >= DATE_TRUNC('minute', SYSDATE) - 2m
      GROUP BY code, time
     )
GROUP BY code, time
ORDER BY code, time;
```
