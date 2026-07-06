---
type: docs
title: 'ROLLUP vs STREAM'
weight: 10
---

ROLLUP과 STREAM은 모두 데이터를 자동으로 처리해 다른 형태로 변환한다는 점에서 비슷해 보입니다. 그러나 적용 대상, 동작 방식, 유연성이 근본적으로 다릅니다.

## 비교 표

| 항목 | ROLLUP | STREAM |
| --- | --- | --- |
| 적용 대상 | TAG 테이블 전용 | 임의 테이블 (LOG, TAG, LOOKUP 등) |
| 집계 단위 | SEC / MIN / HOUR 고정 | 사용자가 SQL로 자유롭게 정의 |
| 변환 로직 | 고정 (SUM, COUNT, MIN, MAX, FIRST, LAST) | 임의 SQL (조인, 조건 필터, 문자열 변환 등) |
| 결과 저장 위치 | `_TAG_ROLLUP_SEC`, `_TAG_ROLLUP_MIN`, `_TAG_ROLLUP_HOUR` | 사용자가 지정한 대상 테이블 |
| 설정 방법 | `WITH ROLLUP` 절로 테이블 생성 시 지정 | `CREATE STREAM` 문으로 별도 생성 |
| 트리거 방식 | 데이터 입력 시 자동 | 일정 주기(INTERVAL) 자동 실행 |
| Cluster Edition 지원 | 지원 | 제한적 지원 |
| 조회 방법 | `rollup()` 함수 사용 | 대상 테이블에 직접 SELECT |

## 어떤 상황에 ROLLUP을 선택하는가

- TAG 테이블에 수억 건 이상의 계측값이 있고, SEC/MIN/HOUR 단위 집계를 빠르게 조회해야 하는 경우
- 대시보드나 모니터링 화면에서 최솟값/최댓값/평균/합계를 실시간으로 표시해야 하는 경우
- 설정이 단순하고 추가 관리 부담 없이 자동 집계를 원하는 경우

```sql
-- ROLLUP 활성화
CREATE TAG TABLE sensor_values (
    name  VARCHAR(128) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) WITH ROLLUP (SEC);

-- 분 단위 평균 조회
SELECT rollup('MIN', avg, time, value), time
FROM sensor_values
WHERE name = 'temp_01';
```

## 어떤 상황에 STREAM을 선택하는가

- LOG 테이블의 이벤트를 특정 조건으로 필터링해 TAG 테이블에 계측값 형태로 변환해야 하는 경우
- SEC/MIN/HOUR가 아닌 사용자 정의 시간 구간(예: 15분, 30분)으로 집계해야 하는 경우
- 단순 집계가 아닌 조인이나 복잡한 변환 로직이 필요한 경우
- 특정 임계값 초과 시 알림용 파생 테이블을 자동으로 업데이트해야 하는 경우

```sql
-- LOG → TAG 변환 STREAM 예시
CREATE STREAM error_count_stream
ON SCHEDULE AT START + INTERVAL 1 MIN
INSERT INTO error_stats (name, time, value)
SELECT 'ERROR_PER_MIN', TO_DATE(TRUNC(_arrival_time, 'MI'), 'YYYY-MM-DD HH24:MI:SS'), COUNT(*)
FROM device_log
WHERE _arrival_time > RECENT 1 MIN
  AND severity = 'ERROR';

START STREAM error_count_stream;
```

## 두 기능을 함께 사용하는 패턴

STREAM으로 LOG 테이블의 이벤트를 TAG 테이블로 변환한 뒤, 해당 TAG 테이블에 ROLLUP을 활성화하는 것도 일반적인 패턴입니다. STREAM이 정제된 데이터를 TAG 테이블에 적재하고, ROLLUP이 해당 데이터를 시간 단위로 자동 집계합니다.

## 다음 읽을 내용

- [ROLLUP 통계의 역할](/dbms/core-concepts/features-concepts/role-statistics-rollup/) — ROLLUP 상세 개념
- [STREAM 처리 모델](/dbms/core-concepts/features-concepts/processing-model-stream/) — STREAM 상세 개념
