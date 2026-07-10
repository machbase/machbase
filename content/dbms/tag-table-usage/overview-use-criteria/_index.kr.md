---
title: '5.1 개요와 사용 기준'
weight: 10
toc: true
---

TAG 테이블은 센서, 설비, 장치처럼 이름으로 식별되는 대상의 시계열 데이터를 저장하는 테이블이다. 하나의 태그 이름과 시간축 또는 거리축 값을 기준으로 데이터를 축적하며, 대량 입력과 시간 범위 조회, 태그별 집계에 맞춰 설계한다.

<a id="overview-tag-characteristics"></a>

## TAG 테이블의 특성

TAG 테이블은 `PRIMARY KEY`로 지정한 이름 컬럼을 태그 식별자로 사용한다. 시간축 테이블은 `DATETIME BASETIME` 컬럼을, 거리축 테이블은 `BASEDISTANCE` 컬럼을 축으로 사용한다.

```sql
CREATE TAG TABLE sensor_data (
    name  VARCHAR(64) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);
```

태그 이름은 센서 또는 측정 지점을 식별하고, 축 컬럼은 값이 발생한 시각이나 위치를 표현한다. 값 컬럼에는 계측값, 상태값, 품질 코드 등을 저장한다.

TAG 테이블의 주요 특성은 다음과 같다.

| 항목 | 내용 |
|------|------|
| 주요 용도 | 센서 데이터, 설비 계측값, 위치 기반 측정값 |
| 기본 식별자 | 태그 이름 (`PRIMARY KEY`) |
| 축 컬럼 | `BASETIME` 또는 `BASEDISTANCE` |
| 입력 패턴 | 지속적인 append 중심 입력 |
| 조회 패턴 | 태그 이름과 시간/거리 범위 조건 |
| 부가 기능 | 메타데이터, 통계 요약, ROLLUP, TAG 캐시 |

<a id="overview-tag-use-criteria"></a>

## 사용 기준

다음 조건에 해당하면 TAG 테이블을 우선 검토한다.

- 같은 구조의 계측 데이터가 여러 태그에서 지속적으로 발생한다.
- 조회 조건이 `name`과 시간 또는 거리 범위 중심이다.
- 최근값, 구간 집계, 다운샘플링, ROLLUP 같은 시계열 처리가 필요하다.
- 태그별 위치, 단위, 상태 같은 메타데이터를 함께 관리해야 한다.
- 입력 후 원본 데이터를 자주 수정하기보다, 보정 이력 또는 정정 절차로 관리한다.

예를 들어 온도 센서, 압력 센서, 전력 계측기, 차량 주행 거리별 측정값은 TAG 테이블에 적합하다.

```sql
SELECT name, time, value
FROM sensor_data
WHERE name = 'TEMP-01'
  AND time BETWEEN '2026-01-01 00:00:00' AND '2026-01-01 01:00:00';
```

<a id="overview-tag-not-use"></a>

## 다른 테이블을 검토할 경우

다음 경우에는 다른 테이블 타입이 더 적합할 수 있다.

| 요구사항 | 권장 테이블 |
|----------|-------------|
| 이벤트 로그, 패킷, 웹 로그처럼 태그 식별자 없이 append 데이터만 저장 | LOG |
| 기준 코드, 장비 마스터, 임계값처럼 작은 참조 데이터를 조회·갱신 | LOOKUP |
| INSERT, UPDATE, DELETE, JOIN을 모두 사용하는 관계형 업무 데이터 | RDB |
| 서버 재시작 후 없어져도 되는 최신 상태 캐시 또는 임시 집계 | VOLATILE |

TAG 테이블은 대량 시계열 저장에는 적합하지만, 일반 업무 테이블처럼 임의 조건으로 행을 자주 수정하는 모델에는 맞지 않는다. 관계형 갱신이 중심이면 RDB 테이블을 사용한다.

<a id="overview-tag-design-flow"></a>

## 설계 순서

TAG 테이블을 설계할 때는 다음 순서로 결정한다.

1. 태그 이름 규칙을 정한다.
2. 시간축(`BASETIME`) 또는 거리축(`BASEDISTANCE`) 중 하나를 선택한다.
3. 값 컬럼의 타입과 개수를 정한다.
4. 태그 메타데이터 컬럼을 분리할지 결정한다.
5. 조회 패턴에 따라 TAG 인덱스, TAG 캐시, ROLLUP 필요 여부를 판단한다.

스키마 세부 설계는 [테이블 구조와 스키마](/dbms/tag-table-usage/table-structure-schema/)에서 다루고, 데이터 입력과 보정은 [데이터 입력과 변경](/dbms/tag-table-usage/data-input-mutation/) 및 [TAG 데이터 업데이트와 보정](/dbms/tag-table-usage/tag-data-update-correction/)을 참고한다.
