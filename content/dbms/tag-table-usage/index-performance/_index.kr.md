---
title: '5.6 인덱스와 성능'
weight: 60
toc: true
---
TAG 조회는 태그명과 축 범위를 먼저 제한하는 것이 기본입니다. 추가 인덱스는 실제 조회 조건과
실행 계획을 측정한 뒤 선택합니다.

<a id="index-tuning-tag"></a>
<a id="original-85-tag-indexes"></a>

## 기본 조회 경로

TAG 테이블은 `PRIMARY KEY` 태그명과 `BASETIME` 또는 `BASEDISTANCE` 축을 기준으로 조회할 수
있도록 필요한 구조를 자동 관리합니다. 애플리케이션은 생성되는 시스템 객체의 이름이나
저장 단계에 의존하지 마십시오.

| 조회 조건 | 조정 방향 |
| --- | --- |
| 한 태그의 축 범위 | 태그명과 축 범위를 모두 명시 |
| 여러 태그의 같은 시간 범위 | 시간 범위를 먼저 제한하고 대상 태그 수를 관리 |
| 메타데이터 속성 | TAG `METADATA` 컬럼으로 정의 |
| 반복적인 시간 집계 | ROLLUP 검토 |
| 값 조건 중심 조회 | 값 컬럼 secondary index를 실행 계획으로 검증 |

태그명이나 축 범위 없이 넓은 데이터를 조회하면 읽어야 할 범위가 커집니다. “항상 빠르다”는
가정 대신 실제 데이터량으로 `EXPLAIN` 결과와 실행 시간을 확인하십시오.

## METADATA 컬럼

설치 위치, 장치 유형처럼 태그마다 한 번 정의하는 속성은 `METADATA` 컬럼으로 설계합니다.
METADATA 컬럼에는 검색을 위한 인덱스가 자동으로 제공되므로 같은 컬럼에 인덱스를 다시 만들지
않습니다.

시계열 값과 자주 바뀌는 상태를 METADATA에 넣으면 갱신 경로와 의미가 불명확해집니다. 값의
성격에 따라 TAG 데이터 컬럼, LOOKUP 또는 VOLATILE 테이블을 검토하십시오.

## 값 컬럼 secondary index

값 조건을 자주 사용하는 경우 `INDEX_TYPE TAG` secondary index를 검토할 수 있습니다. 추가
인덱스는 입력·저장 비용을 늘리므로 생성 전후의 대표 쿼리를 비교합니다.

다음 예제는 격리된 이름을 사용해 값 및 JSON path 인덱스를 만들고, 실행 계획을 확인한 뒤
모든 객체를 정리합니다.

```sql
CREATE TAG TABLE index_tag (
    name    VARCHAR(32) PRIMARY KEY,
    time    DATETIME BASETIME,
    value   DOUBLE,
    payload JSON
) METADATA (
    location VARCHAR(64)
);

CREATE INDEX idx_index_tag_value
    ON index_tag (value) INDEX_TYPE TAG;
CREATE INDEX idx_index_tag_json
    ON index_tag (payload->'$.state');

EXPLAIN SELECT name, time, value
  FROM index_tag
 WHERE name = 'TEMP-01'
   AND time BETWEEN TO_DATE('2026-01-01', 'YYYY-MM-DD')
                AND TO_DATE('2026-01-02', 'YYYY-MM-DD')
   AND value > 80.0;

DROP INDEX idx_index_tag_json;
DROP INDEX idx_index_tag_value;
DROP TABLE index_tag;
```

JSON path 연산자의 반환 타입과 비교 값의 타입을 맞추고, 원하는 경로가 실제로 인덱스를
사용하는지 `EXPLAIN`으로 확인합니다.

## 사용하지 않는 조정

- TAG의 축 컬럼에는 별도 인덱스를 만들지 않습니다.
- LOG용 `MINMAX_CACHE_SIZE` 설정을 TAG 값 컬럼에 적용하지 않습니다.
- 넓은 기간의 반복 집계를 secondary index만으로 해결하려 하지 말고 ROLLUP을 검토합니다.

정확한 인덱스 구문은 [SQL 문법 사전](/dbms/reference/sql/syntax-dictionary-sql/)을,
측정과 튜닝 절차는 [쿼리 튜닝](/dbms/performance-tuning/performance-query-tuning/)을 참고하십시오.
