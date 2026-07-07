---
type: docs
title: 'JOIN'
weight: 30
---

JOIN은 두 개 이상의 테이블을 연결하여 하나의 결과 집합으로 조회하는 SQL 연산입니다. Machbase에서는 대용량 시계열 테이블(TAG/LOG)과 소규모 참조 테이블(LOOKUP/VOLATILE)을 결합하는 패턴이 가장 일반적입니다.

## 지원 JOIN 유형

| 유형 | 설명 |
|------|------|
| INNER JOIN | 두 테이블에서 조인 조건을 만족하는 행만 반환 |
| LEFT OUTER JOIN | 왼쪽 테이블의 모든 행과 오른쪽 테이블의 일치 행 반환, 일치하지 않으면 NULL |
| 암묵적 JOIN | FROM 절에 쉼표로 테이블을 나열하고 WHERE에서 조인 조건 지정 |

## 기본 문법

### INNER JOIN (명시적)

```sql
SELECT a.컬럼, b.컬럼
FROM 테이블A a
INNER JOIN 테이블B b ON a.키 = b.키
WHERE 조건;
```

### 암묵적 JOIN (쉼표 구문)

```sql
SELECT a.컬럼, b.컬럼
FROM 테이블A a, 테이블B b
WHERE a.키 = b.키
  AND 추가조건;
```

## TAG 테이블과 메타데이터 조인

TAG 테이블은 센서 값을 저장하고, 별도 메타데이터 테이블은 센서의 위치·단위·설명 등 부가 정보를 보관합니다. JOIN을 통해 두 정보를 결합합니다.

```sql
-- 센서 값과 위치 정보를 함께 조회
SELECT
    t.time,
    t.name,
    t.value,
    m.location,
    m.unit
FROM tag t
INNER JOIN tag_meta m ON t.name = m.name
WHERE t.time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02')
  AND m.location = '1공장'
ORDER BY t.time;
```

## LOOKUP 테이블을 활용한 참조 값 조인

LOOKUP 테이블은 자주 조인하는 소규모 참조 데이터를 메모리에 유지하므로 조인 성능이 우수합니다.

```sql
-- 센서 측정값에 허용 임계값 정보를 함께 조회
SELECT
    t.time,
    t.name,
    t.value,
    r.threshold_high,
    r.threshold_low,
    CASE
        WHEN t.value > r.threshold_high THEN 'HIGH'
        WHEN t.value < r.threshold_low  THEN 'LOW'
        ELSE 'NORMAL'
    END AS status
FROM tag t
INNER JOIN ref_threshold r ON t.name = r.sensor_name
WHERE t.time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02');
```

## LEFT OUTER JOIN

오른쪽 테이블에 일치하는 행이 없어도 왼쪽 테이블의 행을 모두 유지합니다. 메타 정보가 없는 센서도 누락 없이 조회해야 할 때 사용합니다.

```sql
-- 메타 정보가 없는 센서도 포함하여 조회 (미등록 센서는 NULL로 표시)
SELECT
    t.time,
    t.name,
    t.value,
    m.location,
    m.description
FROM tag t
LEFT OUTER JOIN tag_meta m ON t.name = m.name
WHERE t.time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02');
```

## 서브쿼리를 FROM 절에서 사용

집계 결과나 필터링된 데이터를 인라인 뷰로 활용하여 JOIN할 수 있습니다.

```sql
-- 센서별 일 평균과 메타 정보를 함께 조회
SELECT avg_t.name, avg_t.avg_value, m.location
FROM (
    SELECT name, AVG(value) AS avg_value
    FROM tag
    WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02')
    GROUP BY name
) avg_t
INNER JOIN tag_meta m ON avg_t.name = m.name
ORDER BY avg_t.avg_value DESC;
```

## 성능 권장 사항

> **팁**: JOIN에서 큰 테이블(TAG/LOG)을 왼쪽에, 작은 참조 테이블(LOOKUP/VOLATILE/메타)을 오른쪽에 배치하십시오. Machbase는 오른쪽 테이블을 기준으로 해시 또는 인덱스 조인을 수행하므로, 참조 테이블이 작을수록 성능이 향상됩니다.

> **주의**: TAG 테이블끼리의 대용량 JOIN은 성능에 큰 부담을 줄 수 있습니다. TAG-TAG JOIN이 필요한 경우 반드시 시간 범위 조건을 지정하고, 결과 크기를 LIMIT로 제한하는 것을 권장합니다.

## 제한 사항

- CROSS JOIN은 대용량 테이블에서 지원되지 않습니다.
- TAG 테이블 간 JOIN 시 양쪽 모두 시간 조건을 명시하는 것이 필수입니다.
- OUTER JOIN에서 집계 함수를 사용할 경우 NULL 값 처리에 주의가 필요합니다.

## 관련 항목

- [PIVOT](../pivot/): JOIN 결과를 열 방향으로 변환
- [집계 함수와 GROUP BY](../aggregation-group/): JOIN 후 그룹별 집계
- [조건 검색 - TAG 메타데이터 조회](../../condition-conditional-search/metadata-query-tag/): FROM TAG METADATA 구문
