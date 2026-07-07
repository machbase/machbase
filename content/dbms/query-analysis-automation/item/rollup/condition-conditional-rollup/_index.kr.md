---
type: docs
title: '조건 ROLLUP'
weight: 80
---

조건 ROLLUP은 원본 데이터에 WHERE 필터를 적용해, 특정 조건을 만족하는 행만 집계합니다. 정상 데이터, 알람 데이터 등 카테고리별 사전 집계에 유용합니다.

## 생성 구문

```sql
CREATE ROLLUP rollup_name
  ( ON source_table(column_name)
  | FROM source_rollup_table )
  INTERVAL n (SEC|MIN|HOUR)
  WHERE predicate;
```

## 생성 예시

```sql
-- value >= 0 인 데이터만 집계
CREATE ROLLUP _tag_ru_valid_1m ON tag(value) INTERVAL 1 MIN
  WHERE value >= 0;

-- status = 'NORMAL' 인 경우만 집계 (status 컬럼이 TAG 테이블에 있을 때)
CREATE ROLLUP _tag_ru_normal_1m ON tag(value) INTERVAL 1 MIN
  WHERE status = 1;

-- 복합 조건
CREATE ROLLUP _tag_ru_alarm_1s ON tag(value) INTERVAL 1 SEC
  WHERE value > 90.0 AND quality >= 2;

-- 분 롤업을 소스로 조건 시간 롤업
CREATE ROLLUP _tag_ru_cond_1h FROM _tag_ru_valid_1m INTERVAL 1 HOUR;
```

## WHERE 조건 제약

- 허용: 비교 연산자, BETWEEN, IN, LIKE, AND/OR/NOT, CASE, 비집계 스칼라 함수
- 금지: 서브쿼리, 집계 함수(SUM, AVG 등), 존재하지 않는 컬럼
- 태그명(PRIMARY KEY) 컬럼 조건은 지원하지 않습니다 (내부적으로 숫자 ID로 관리)

## 자동 선택과 힌트

조건 없는 ROLLUP과 조건 ROLLUP이 같은 주기·컬럼으로 있을 때, 엔진은 기본적으로 **조건 없는 ROLLUP**을 선택합니다. 조건 ROLLUP이 필요할 때는 힌트를 사용합니다.

```sql
-- 기본: 조건 없는 롤업 자동 선택
SELECT rollup('min', 1, time) AS rt, AVG(value)
FROM   tag
WHERE  name = 'SENSOR-01'
GROUP BY rt;

-- 조건 롤업 강제 지정
SELECT /*+ ROLLUP_TABLE(_tag_ru_valid_1m) */
       rollup('min', 1, time) AS rt, AVG(value)
FROM   tag
WHERE  name = 'SENSOR-01'
GROUP BY rt;
```

## V$ROLLUP에서 조건 확인

```sql
SELECT ROLLUP_TABLE, PREDICATE
FROM   V$ROLLUP
WHERE  PREDICATE IS NOT NULL;
```
