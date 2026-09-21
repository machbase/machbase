---
title: '조건부 롤업으로 이상치 제외 집계'
type: docs
weight: 61
---

## 개요

시계열 데이터에는 정상값과 이상치가 섞여 들어오는 경우가 많습니다. 이때 **조건부 롤업**(필터 롤업)을 사용하면
특정 조건을 만족하는 데이터만 집계해 일관되고 “정제된 통계”를 얻을 수 있습니다.  
이 문서에서는 실제 회귀 테스트 시나리오를 바탕으로 **조건부 롤업 생성 → 데이터 적재 → 결과 검증 → 운영 적용** 흐름을 설명합니다.

> 이 문서의 SQL 예제는 회귀 테스트에 사용하는 `extension.tc`의 내용을 그대로 사용합니다.  
> 전체 SQL은 [extension.tc 샘플 SQL](../rollup-conditional-extension.tc/)에서 확인할 수 있습니다.

## 언제 조건부 롤업을 쓰면 좋은가요?

- 센서 오류, 통신 오류 등으로 생긴 **이상치가 집계값(MAX, AVG 등)을 왜곡**하는 경우
- 특정 상태(예: 정상을 뜻하는 `value2=0`)의 행만 **보고서 집계 대상**으로 삼고 싶은 경우
- 모니터링용 집계와 보고서용 집계를 **분리**해 관리하고 싶은 경우

조건부 롤업은 조회 시점에 `WHERE` 조건을 거는 방식보다 안정적입니다.  
조건을 미리 적용한 집계 테이블을 만들어 두므로 **항상 같은 품질의 통계를 빠르게 제공**할 수 있습니다.

---

## 1) 예제 테이블과 컬럼 의미

아래 예제에서 `value`는 집계 대상 값이고, `value2`는 정상값과 이상치를 구분하는 플래그입니다.

- `value2=0`: 정상
- `value2=1`: 이상치

```sql
CREATE TAG TABLE tag (
    name   VARCHAR(20) PRIMARY KEY,
    time   DATETIME BASETIME,
    value  DOUBLE SUMMARIZED,
    value2 DOUBLE
);
```

---

## 2) 롤업 체인과 조건부 롤업 정의

초 단위와 분 단위 롤업을 만들고, 분 단위에 **조건부 롤업**을 추가합니다.

```sql
CREATE ROLLUP _tag_rollup_custom_1 ON tag(value) INTERVAL 1 SEC  EXTENSION;
CREATE ROLLUP _tag_rollup_custom_2 FROM _tag_rollup_custom_1 INTERVAL 1 MIN EXTENSION;
CREATE ROLLUP _tag_rollup_custom_3 ON tag(value) INTERVAL 1 MIN EXTENSION WHERE value2 = 0;
```

- `_tag_rollup_custom_3`은 **정상 데이터만 반영한 1분 롤업**입니다.
- `WHERE` 조건은 집계 전에 원본 행에 적용됩니다.
- 조건에 사용한 컬럼(`value2` 등)은 롤업 테이블에 **저장되지 않습니다**.

> `FIRST()`/`LAST()`를 사용하려면 **EXTENSION 롤업**이 필요합니다.

---

## 3) 샘플 데이터(이상치 포함)

조건부 롤업의 효과를 확인할 수 있도록 `value2=1`인 행을 섞어 두었습니다. 아래는 `extension.tc`의 입력 데이터를 그대로 사용한 예입니다.

```sql
INSERT INTO tag VALUES('APPL', '2020-01-01 00:00:00', 100,  0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:00:10', 101,  0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:00:11', 130,  0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:00:20', 120,  0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:00:30', 110,  0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:00:40', 9900, 1);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:00:50', 99,   0);

INSERT INTO tag VALUES('APPL', '2020-01-01 00:01:00', 98,  0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:01:10', 94,  0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:01:20', 2990, 1);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:01:30', 92,  0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:01:40', 99,  0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:01:50', 102, 0);

INSERT INTO tag VALUES('APPL', '2020-01-01 00:02:00', 110, 0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:02:10', 120, 0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:02:20', 140, 0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:02:30', 66160, 1);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:02:40', 170, 0);
INSERT INTO tag VALUES('APPL', '2020-01-01 00:02:50', 180, 0);
```

이상치 값은 정상 범위를 크게 벗어나므로 집계 결과에 큰 영향을 줍니다.

---

## 4) 롤업 강제 수행(테스트 시점 고정)

테스트 환경에서는 타이밍을 확실히 맞추기 위해 롤업을 강제로 수행합니다.

```sql
EXEC ROLLUP_FORCE(_tag_rollup_custom_1);
EXEC ROLLUP_FORCE(_tag_rollup_custom_2);
EXEC ROLLUP_FORCE(_tag_rollup_custom_3);
```

---

## 5) 결과 비교 쿼리

### 5-1. 일반 집계(원본 기준)

```sql
SELECT rollup('min', 1, time) AS rt,
       COUNT(value), MIN(value), MAX(value),
       FIRST(time, value), LAST(time, value)
  FROM tag
 GROUP BY rt
 ORDER BY rt;
```

### 5-2. 조건부 롤업을 강제로 선택(힌트 사용)

```sql
SELECT /*+ ROLLUP_TABLE(_tag_rollup_custom_3) */
       rollup('min', 1, time) AS rt,
       COUNT(value), MIN(value), MAX(value),
       FIRST(time, value), LAST(time, value)
  FROM tag
 GROUP BY rt
 ORDER BY rt;
```

---

## 6) 왜 힌트를 반드시 써야 하나요?

조건부 롤업이 있더라도 후보가 여러 개이면 **옵티마이저는 조건 없는 롤업을 자동으로 우선 선택**합니다.  
즉, 힌트 없이 실행하면 **조건부 롤업이 무시될 수 있습니다.**

따라서 다음과 같은 경우에는 힌트를 사용해야 합니다.

- 조건부 집계 결과를 **정확히 검증**해야 할 때
- 주기와 값 컬럼이 같은 롤업이 여러 개여서 **특정 롤업을 선택해야** 할 때
- `FIRST()`/`LAST()`를 사용하느라 **EXTENSION 롤업을 지정해야** 할 때

힌트는 **의도한 롤업이 실제로 사용되도록 보장하는 안전장치**입니다.

---

## 7) 예시 결과 요약(이상치 포함 vs 조건부)

아래 표는 `extension.tc` 데이터를 기준으로 분 단위 집계 결과 중 **핵심 통계만 요약**한 예시입니다.

**건수와 최솟값/최댓값:**

| 분(rollup) | 원본 COUNT | 원본 MIN | 원본 MAX | 조건부 COUNT | 조건부 MIN | 조건부 MAX |
|---|---:|---:|---:|---:|---:|---:|
| 00:00 | 7 | 99 | 9900 | 6 | 99 | 130 |
| 00:01 | 6 | 92 | 2990 | 5 | 92 | 102 |
| 00:02 | 6 | 110 | 66160 | 5 | 110 | 180 |

핵심은 다음과 같습니다.

- **원본 집계는 이상치 때문에 MAX 값이 크게 증가**합니다.
- **조건부 롤업은 정상 데이터만 반영**하므로 안정적인 통계를 제공합니다.

### FIRST/LAST 값까지 확인하기

`FIRST()`와 `LAST()`는 각 구간의 시작 값과 종료 값을 돌려주는 함수이며, **EXTENSION 롤업이 필요**합니다.  
아래는 분 단위로 실제 FIRST/LAST 결과를 정리한 예시입니다. 표에는 해당 시각과 값을 함께 적었지만, 함수가 돌려주는 것은 값뿐입니다.

| 분(rollup) | 원본 FIRST(time, value) | 원본 LAST(time, value) | 조건부 FIRST(time, value) | 조건부 LAST(time, value) |
|---|---|---|---|---|
| 00:00 | 00:00:00, 100 | 00:00:50, 99 | 00:00:00, 100 | 00:00:50, 99 |
| 00:01 | 00:01:00, 98 | 00:01:50, 102 | 00:01:00, 98 | 00:01:50, 102 |
| 00:02 | 00:02:00, 110 | 00:02:50, 180 | 00:02:00, 110 | 00:02:50, 180 |

이 샘플에서는 이상치가 구간의 시작이나 끝에 있지 않아 FIRST/LAST 값이 같습니다.  
하지만 실제 운영에서는 이상치가 구간 경계에 올 수 있으므로 **조건부 롤업이 FIRST/LAST 값에도 영향을 줄 수 있습니다.**

---

## 8) 운영 시나리오(실무 적용 흐름)

현장에서는 다음과 같은 흐름으로 조건부 롤업을 적용합니다.

1. **데이터 적재 단계**: 센서나 로그 데이터를 입력할 때 품질 플래그(`value2`)를 함께 기록합니다.
2. **롤업 체인 구성**: 일반 롤업(전체 통계)과 조건부 롤업(정상 통계)을 **함께 유지**합니다.
3. **일반 대시보드**: 일반 롤업으로 전체 데이터를 빠르게 모니터링합니다.
4. **정상 데이터 분석**: 리포트나 KPI 계산에는 **조건부 롤업을 힌트로 고정**해 사용합니다.
5. **문제 분석 시 원본 조회**: 이상치의 원인을 분석할 때는 원본 데이터를 직접 조회합니다.

이 구조를 유지하면 세부 데이터를 잃지 않으면서 **빠른 조회와 정확한 통계를 함께 확보**할 수 있습니다.

---

## 정리

- 조건부 롤업은 **이상치가 섞이는 환경에서 통계를 안정화**하는 실용적인 방법입니다.
- 힌트는 **조건부 롤업을 확실히 선택하기 위해 반드시 필요**합니다.
- 운영 환경에서는 일반 롤업과 조건부 롤업을 함께 사용해 **모니터링과 분석을 분리**하는 것이 효과적입니다.

---

## 관련 문서

- [롤업 테이블](../rollup-tables/)
- [SELECT 힌트: ROLLUP_TABLE](../../../sql-reference/select-hint/)
