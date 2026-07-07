---
type: docs
title: 'ROLLUP 통계의 역할'
weight: 10
---

TAG 테이블에 수억 건의 계측값이 쌓인 상황에서 "지난 한 달의 시간별 평균 온도"를 조회한다고 가정합니다. 이 쿼리를 매번 원시 데이터 전체를 스캔해서 계산한다면, 조회할 때마다 수억 건을 집계하는 오버헤드가 발생합니다. ROLLUP은 이 문제를 해결하기 위한 Machbase의 자동 사전 집계 메커니즘입니다.

## ROLLUP이란

ROLLUP은 TAG 테이블에 새로운 데이터가 입력될 때, 배경 스레드가 자동으로 초·분·시간 단위의 집계 통계를 미리 계산해 내부 테이블에 저장하는 기능입니다. 집계가 이미 계산된 상태이므로, 조회 시 원시 데이터를 다시 스캔할 필요가 없습니다.

## 3단계 자동 집계

ROLLUP은 세 가지 시간 단위로 집계를 관리합니다.

| 단계 | 집계 단위 | 내부 테이블 |
| --- | --- | --- |
| 1단계 | 초(SEC) | `_TAG_ROLLUP_SEC` |
| 2단계 | 분(MIN) | `_TAG_ROLLUP_MIN` |
| 3단계 | 시(HOUR) | `_TAG_ROLLUP_HOUR` |

SEC 집계가 축적되면 MIN으로, MIN이 축적되면 HOUR로 순차적으로 합산됩니다. 각 집계 테이블에는 합계(SUM), 건수(COUNT), 최솟값(MIN), 최댓값(MAX), 첫 번째 값(FIRST), 마지막 값(LAST)이 저장됩니다.

## ROLLUP 테이블 생성

TAG 테이블 생성 시 `WITH ROLLUP` 절을 추가하면 ROLLUP이 활성화됩니다.

```sql
CREATE TAG TABLE rollup_sensor_values (
    name  VARCHAR(128) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) WITH ROLLUP (SEC);
```

`SUMMARIZED` 속성이 붙은 컬럼이 집계 대상이 됩니다. `WITH ROLLUP (SEC)` 은 SEC → MIN → HOUR 세 단계 모두를 활성화합니다. 특정 단계까지만 필요하다면 `WITH ROLLUP (MIN)` 또는 `WITH ROLLUP (HOUR)` 를 지정할 수 있습니다.

## rollup() 함수로 조회

ROLLUP 집계 데이터를 조회할 때는 `rollup()` 함수를 사용합니다.

```sql
-- 분 단위 평균값 조회
SELECT rollup('min', 1, time) AS mtime, AVG(value) AS avg_value
FROM rollup_sensor_values
WHERE name = 'temp_sensor_01'
  AND time BETWEEN TO_DATE('2026-07-01', 'YYYY-MM-DD')
               AND TO_DATE('2026-07-03', 'YYYY-MM-DD')
GROUP BY mtime
ORDER BY mtime;
```

`rollup()` 함수는 내부적으로 `_TAG_ROLLUP_MIN` 테이블에서 이미 계산된 집계를 읽어 반환합니다. 원시 데이터를 스캔하지 않으므로 조회 성능이 수십 배에서 수백 배까지 향상될 수 있습니다.

## ROLLUP이 필요한 경우와 불필요한 경우

**ROLLUP이 유용한 경우**

- 수억 건 이상의 TAG 계측값이 있고, 시간 단위 집계 조회가 반복적으로 필요한 경우
- 대시보드나 모니터링 화면에서 분·시간 단위 트렌드를 실시간으로 표시해야 하는 경우
- 최근 데이터뿐 아니라 장기 이력(수개월~수년)의 집계도 빠르게 조회해야 하는 경우

**ROLLUP 없이도 충분한 경우**

- 데이터 건수가 수천만 건 이하로 원시 데이터 집계가 빠른 경우
- 집계 조회보다 개별 값의 조회(포인트 쿼리)가 주된 패턴인 경우
- 집계 주기가 SEC/MIN/HOUR와 맞지 않는 사용자 정의 구간이 필요한 경우 (이 경우 STREAM을 검토)

## 다음 읽을 내용

- [STREAM 처리 모델](../processing-model-stream/) — 임의 SQL 기반의 자동 변환/집계 처리
- [ROLLUP vs STREAM](/dbms/core-concepts/terminology-distinction/rollup-vs-stream/) — 두 기능의 차이와 선택 기준
- [TAG 테이블 설계](/dbms/data-modeling-table-design/table-types-design-type/design-tag/) — ROLLUP 활성화를 포함한 TAG 테이블 상세 설계
