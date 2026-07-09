---
type: docs
title: '6.1.1 ROLLUP 개념'
weight: 10
---

ROLLUP 테이블은 TAG 테이블의 특정 숫자형 컬럼을 시간 단위로 집계한 결과를 저장하는 내부 테이블입니다.

## 집계 저장 구조

ROLLUP 테이블 하나는 한 컬럼의 시간 단위 통계를 저장합니다. 각 행은 하나의 (태그명, 시간 구간) 조합에 대해 다음 값을 보유합니다.

| 집계 값 | 설명 |
|---------|------|
| MIN | 구간 내 최솟값 |
| MAX | 구간 내 최댓값 |
| SUM | 구간 내 합계 |
| COUNT | 구간 내 데이터 개수 |
| AVG | 구간 내 평균 (SUM/COUNT) |
| SUMSQ | 제곱합 (표준편차 계산용) |

확장 ROLLUP(EXTENSION)에는 FIRST(구간 첫 값), LAST(구간 마지막 값)도 추가됩니다.

## 계층 구조

여러 ROLLUP을 연결해 다단계 집계 계층을 만들 수 있습니다.

```
TAG 테이블 (원시 데이터)
  └── ROLLUP 1초  (ON tag(value) INTERVAL 1 SEC)
        └── ROLLUP 1분  (FROM rollup_1sec INTERVAL 1 MIN)
              └── ROLLUP 1시간  (FROM rollup_1min INTERVAL 1 HOUR)
```

상위 롤업은 하위 롤업을 소스로 집계하므로, 원시 데이터를 반복 스캔하지 않습니다.

## 자동 집계 시점

ROLLUP은 백그라운드 스레드로 동작합니다. wakeup 주기(기본값 = ROLLUP 주기)마다 깨어나 새로 입력된 데이터를 처리합니다.

- 실시간성이 필요하면 wakeup 주기를 ROLLUP 주기의 약수로 짧게 설정합니다.
- 즉시 집계가 필요하면 `ALTER ROLLUP name FORCE` 또는 `EXEC ROLLUP_FORCE(name)`를 사용합니다.

## 조회 원리

`rollup()` 함수를 SELECT에서 사용하면 Machbase 엔진이 요청한 시간 단위와 일치하는 ROLLUP 테이블을 자동으로 선택합니다.

```sql
-- 1분 단위 집계 조회 → ROLLUP 1분 테이블에서 읽음
SELECT rollup('min', 1, time) AS rt, AVG(value)
FROM   tag
WHERE  name = 'SENSOR-01'
  AND  time BETWEEN '2024-01-01' AND '2024-01-02'
GROUP BY rt
ORDER BY rt;
```

ROLLUP 테이블이 없으면 원시 TAG 데이터를 직접 스캔합니다(성능 저하).
