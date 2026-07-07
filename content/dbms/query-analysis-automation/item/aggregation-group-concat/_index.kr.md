---
type: docs
title: 'GROUP_CONCAT'
weight: 20
---

`GROUP_CONCAT`은 그룹 내 여러 행의 값을 하나의 문자열로 이어 붙이는 집계 함수입니다. 쿼리 결과를 쉼표로 구분된 목록으로 가공하거나, 센서 이름·상태 값 등을 한 셀에 요약할 때 유용합니다.

## 기본 문법

```sql
GROUP_CONCAT(column [SEPARATOR 'sep'])
```

- `column`: 이어 붙일 값이 있는 컬럼
- `SEPARATOR 'sep'`: 구분자를 지정합니다. 생략하면 기본값 `,`(쉼표)가 사용됩니다.

## 기본 사용 예시

### 위치별 센서 이름 목록 만들기

```sql
-- 각 위치에 설치된 센서 이름을 쉼표로 나열
SELECT location, GROUP_CONCAT(sensor_name) AS sensors
FROM sensor_meta
GROUP BY location;
```

결과 예시:

| location | sensors |
|----------|---------|
| 1공장 | temp_01,temp_02,pressure_01 |
| 2공장 | temp_03,flow_01 |

### 구분자 변경

```sql
-- 세미콜론으로 구분
SELECT location, GROUP_CONCAT(sensor_name SEPARATOR '; ') AS sensors
FROM sensor_meta
GROUP BY location;
```

## TAG 테이블 활용 예시

TAG 테이블의 메타데이터나 LOOKUP 테이블과 조합하면 특정 조건에 해당하는 태그명 목록을 한 번에 조회할 수 있습니다.

```sql
-- 상태가 'ACTIVE'인 센서 이름을 그룹별로 나열
SELECT factory, GROUP_CONCAT(tag_name SEPARATOR ', ') AS active_sensors
FROM tag_metadata
WHERE status = 'ACTIVE'
GROUP BY factory;
```

```sql
-- 특정 시간대에 이상값이 발생한 센서 목록
SELECT GROUP_CONCAT(DISTINCT name SEPARATOR ', ') AS alert_sensors
FROM tag
WHERE time BETWEEN TO_DATE('2024-01-01') AND TO_DATE('2024-01-02')
  AND value > 100;
```

## 결과 길이 제한

> **주의**: `GROUP_CONCAT`의 결과 문자열 길이에는 내부 제한이 있습니다. 그룹 내 행 수가 매우 많을 경우 문자열이 잘릴 수 있으므로, 대량 데이터보다는 메타 정보나 코드 목록처럼 항목 수가 적은 경우에 사용하는 것이 적합합니다.

## 활용 패턴

| 패턴 | 설명 |
|------|------|
| 코드 목록 조회 | 그룹별 코드·이름 값을 단일 행으로 반환 |
| 태그 이름 집합 | 공장/라인별 센서 이름을 하나의 컬럼으로 요약 |
| 상태 값 나열 | 시간대별 발생한 이벤트 코드를 순서대로 연결 |
| 동적 IN 목록 | 애플리케이션에서 후속 쿼리의 IN 조건에 사용할 목록 생성 |

## 관련 항목

- [집계 함수와 GROUP BY](../aggregation-group/): COUNT, AVG 등 일반 집계 함수
- [JOIN](../join/): 메타데이터 테이블과의 조인으로 풍부한 정보 조회
