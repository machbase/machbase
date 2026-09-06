---
title: '6.5 조건 ROLLUP'
weight: 50
toc: true
---

<a id="original-85-rollup-conditional"></a>

## 조건부 롤업으로 이상치 제외 집계


### 개요

시계열 데이터에는 정상값과 이상치가 섞이기 마련입니다. **조건부 롤업**(필터 롤업)을 사용하면 특정 조건을 만족하는 데이터만 집계해 정제된 통계를 얻을 수 있습니다.
아래에서는 조건부 롤업 생성부터 데이터 적재, 결과 검증, 운영 적용까지의 흐름을 설명합니다.
아래 예제를 순서대로 읽고, 마지막의 [문법과 제약](#rollup-conditional-extension-tc)에서
허용 조건을 확인합니다.

### 언제 조건부 롤업이 유용한가

- 센서 오류, 통신 오류 등 **이상치가 집계값을 왜곡**하는 경우
- 특정 상태(예: `value2=0` 정상)만 **보고서 집계 대상**으로 삼고 싶은 경우
- 운영 대시보드와 품질 검증용 통계를 **분리**해 관리하고 싶은 경우

집계 전에 품질 조건을 적용해 두면 같은 조건의 통계를 반복해서 조회할 수 있습니다.
일반 롤업에는 품질 플래그가 보존되지 않으므로 이미 집계된 결과에서 이상치만 다시 빼는
방식과는 구분해야 합니다.

---

### 1) 예제 테이블과 컬럼 의미

아래 예제에서 `value`는 집계 대상 값이고, `value2`는 정상/이상치를 구분하는 플래그입니다.
`value2=0`이면 정상, `value2=1`이면 이상치로 사용합니다.

```sql
CREATE TAG TABLE tag (
    name   VARCHAR(20) PRIMARY KEY,
    time   DATETIME BASETIME,
    value  DOUBLE SUMMARIZED,
    value2 DOUBLE
);
```

---

### 2) 롤업 체인과 조건부 롤업 정의

전체 데이터를 집계하는 초→분 롤업 계층과, 원본 TAG에서 정상 데이터만 집계하는
별도의 1분 롤업을 만듭니다. 조건부 롤업은 앞의 일반 롤업을 소스로 사용하지 않습니다.

```sql
CREATE ROLLUP _tag_rollup_custom_1 ON tag(value) INTERVAL 1 SEC  EXTENSION;
CREATE ROLLUP _tag_rollup_custom_2 FROM _tag_rollup_custom_1 INTERVAL 1 MIN EXTENSION;
CREATE ROLLUP _tag_rollup_custom_3 ON tag(value) INTERVAL 1 MIN EXTENSION WHERE value2 = 0;
```

- `_tag_rollup_custom_3`는 **정상 데이터만 반영된 1분 롤업**입니다.
- `WHERE` 조건은 원본 행에 적용됩니다.
  조건에 사용한 컬럼(`value2`) 자체는 롤업 테이블에 저장되지 않습니다.

> `FIRST()`/`LAST()`를 사용하려면 **EXTENSION 롤업**이 필요합니다.

---

### 3) 샘플 데이터(이상치 포함)

`value2=1`인 행을 섞어 두어 조건부 롤업 효과를 확인합니다.

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

`value2=1`로 표시한 9900, 2990, 66160은 다른 표본보다 크게 설정하여 집계 차이를
확인하기 위한 값입니다. 실제 품질 판정 규칙은 업무에 맞게 정합니다.

---

### 4) 롤업 강제 수행

데이터 적재 직후 결과를 확인하려면 롤업을 강제로 수행합니다.

```sql
EXEC ROLLUP_FORCE(_tag_rollup_custom_1);
EXEC ROLLUP_FORCE(_tag_rollup_custom_2);
EXEC ROLLUP_FORCE(_tag_rollup_custom_3);
```

---

### 5) 결과 비교 쿼리

#### 5-1. 일반 집계(원본 기준)

다음 쿼리는 원본 전체를 반영한 조건 없는 롤업을 사용합니다. 원시 행을 직접 스캔하는
쿼리는 아닙니다.
```sql
SELECT rollup('min', 1, time) AS rt,
       COUNT(value), MIN(value), MAX(value),
       FIRST(time, value), LAST(time, value)
  FROM tag
 GROUP BY rt
 ORDER BY rt;
```

#### 5-2. 조건부 롤업을 강제로 선택(힌트 사용)
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

### 6) 힌트가 필수인 이유

조건부 롤업이 존재해도 옵티마이저는 조건 없는 롤업을 우선 선택합니다. 힌트 없이 실행하면 조건부 롤업이 무시될 수 있습니다.

다음 경우에는 힌트를 사용해야 합니다.

- 조건부 집계를 **정확히 검증**하고 싶을 때
- 여러 롤업 중 **특정 롤업을 선택해야** 할 때
- `FIRST()`/`LAST()`를 사용할 때 **EXTENSION 롤업을 지정해야** 할 때

---

### 7) 예시 결과 요약(이상치 포함 vs 조건부)

위 예제 데이터의 분 단위 집계 결과입니다.

| 분(rollup) | 원본 COUNT | 원본 MIN | 원본 MAX | 조건부 COUNT | 조건부 MIN | 조건부 MAX |
|---|---:|---:|---:|---:|---:|---:|
| 00:00 | 7 | 99 | 9900 | 6 | 99 | 130 |
| 00:01 | 6 | 92 | 2990 | 5 | 92 | 102 |
| 00:02 | 6 | 110 | 66160 | 5 | 110 | 180 |

- 원본 집계는 이상치 때문에 MAX 값이 크게 증가합니다.
- 조건부 롤업은 정상 데이터만 반영되어 안정적인 통계를 제공합니다.

#### FIRST/LAST 값까지 확인하기

`FIRST()`와 `LAST()`는 구간의 시작/종료 값을 반환하며 EXTENSION 롤업이 필요합니다.
분 단위 기준 FIRST/LAST 결과 예시입니다.

아래 표의 시각은 선택된 원본 행을 설명하기 위한 보조 정보입니다. `FIRST(time, value)`와
`LAST(time, value)` 자체는 시각·값 쌍이 아니라 선택된 `value`를 반환합니다.

| 분(rollup) | 원본 FIRST(time, value) | 원본 LAST(time, value) | 조건부 FIRST(time, value) | 조건부 LAST(time, value) |
|---|---|---|---|---|
| 00:00 | 00:00:00, 100 | 00:00:50, 99 | 00:00:00, 100 | 00:00:50, 99 |
| 00:01 | 00:01:00, 98 | 00:01:50, 102 | 00:01:00, 98 | 00:01:50, 102 |
| 00:02 | 00:02:00, 110 | 00:02:50, 180 | 00:02:00, 110 | 00:02:50, 180 |

이 샘플에서는 이상치가 구간의 시작/끝에 위치하지 않아 FIRST/LAST 값이 동일합니다. 실제 운영에서는 이상치가 경계에 위치할 수 있으므로 조건부 롤업이 FIRST/LAST에도 영향을 줍니다.

---

### 8) 운영 시나리오(실무 적용 흐름)

현장에서 조건부 롤업을 적용하는 일반적인 흐름입니다.

1. **데이터 적재 단계**
   센서나 로그가 들어올 때, 품질 플래그(`value2`)를 함께 기록합니다.

2. **롤업 체인 구성**
   일반 롤업(전체 통계)과 조건부 롤업(정상 통계)을 **병렬로 유지**합니다.

3. **일반 대시보드**
   전체 데이터를 기반으로 빠른 모니터링을 수행합니다.

4. **정상 데이터 분석**
   리포트나 KPI 계산은 **조건부 롤업을 힌트로 고정**해 사용합니다.

5. **문제 분석 시 원본 조회**
   이상치 발생 원인을 분석할 때는 원본 데이터를 직접 조회합니다.

이 구조를 유지하면 빠른 조회와 정확한 통계를 동시에 확보할 수 있습니다.

---

### 정리

- 조건부 롤업은 이상치가 섞이는 환경에서 통계를 안정화하는 실용적인 방법입니다.
- 힌트는 조건부 롤업을 확실히 선택하기 위한 필수 수단입니다.
- 일반 롤업과 조건부 롤업을 병행해 모니터링과 분석을 분리하는 구성이 효과적입니다.

---

### 관련 문서

- [롤업 테이블](/dbms/tag-rollup-usage/overview-use-criteria/#original-85-rollup-tables)
- [SELECT 힌트: ROLLUP_TABLE](/dbms/reference/sql/syntax-dictionary-sql/select-hint-syntax/)

<a id="rollup-conditional-extension-tc"></a>
<a id="original-85-rollup-conditional-extension"></a>
<a id="condition-conditional-rollup"></a>

## 문법과 제약

```sql
CREATE ROLLUP rollup_name
  ON source_table(column_name)
  INTERVAL n (SEC|MIN|HOUR)
  WHERE predicate;
```

WHERE에는 비교, BETWEEN, IN, LIKE, 논리 연산과 비집계 scalar 함수를 사용할 수 있습니다.
subquery와 집계 함수는 사용할 수 없으며 tag-name PRIMARY KEY 조건도 지원하지 않습니다.
조건 없는 후보가 함께 있으면 자동 선택이 달라질 수 있으므로 필요한 경우 `ROLLUP_TABLE` hint를
사용합니다. 조건과 상태는 `V$ROLLUP.PREDICATE` 및
[ROLLUP 제어와 상태 확인](../ingestion-control-rollup/)에서 확인합니다.
