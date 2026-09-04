---
title: '5.3 생성, 변경, 삭제'
weight: 30
toc: true
---
TAG 테이블은 태그 식별자와 하나의 축 컬럼을 필수로 가집니다. 이 페이지에서는 실행 가능한
기본 예제를 제공하고, 전체 옵션은 SQL 레퍼런스로 연결합니다.

<a id="original-85-creating-tag-tables"></a>

## TAG 테이블 생성

| 축 | 컬럼 정의 | 용도 |
| --- | --- | --- |
| 시간 | `DATETIME BASETIME` | 센서 측정 시각, 이벤트 발생 시각 |
| 거리 | `DOUBLE`, `LONG`, `ULONG` + `BASEDISTANCE` | 주행거리, 선로·배관 위치 |

한 테이블에는 축 컬럼을 하나만 정의합니다. 태그명 컬럼은 `PRIMARY KEY`이며, 시간축과
거리축 중 데이터의 실제 의미에 맞는 축을 선택합니다. 거리축 TAG에는 ROLLUP을 사용할 수
없습니다.

### 시간축 TAG

```sql
CREATE TAG TABLE tag_create_demo (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) METADATA (
    location VARCHAR(64)
);
```

`SUMMARIZED`는 ROLLUP 등 집계 기능을 사용할 숫자형 컬럼에 지정합니다. 위치·단위처럼
태그마다 한 번 저장하는 속성은 `METADATA`, 매 측정마다 달라지는 값은 일반 데이터 컬럼에
정의합니다.

### 거리축 TAG

```sql
CREATE TAG TABLE distance_create_demo (
    name     VARCHAR(32) PRIMARY KEY,
    distance DOUBLE BASEDISTANCE,
    value    DOUBLE
);
```

소수 거리값에는 `DOUBLE`, 정수 축에는 값 범위에 맞는 `LONG` 또는 `ULONG`을 사용합니다.

## TAG 테이블 변경

TAG 데이터 컬럼의 임의 변경은 제한됩니다. 스키마를 확장해야 한다면 새 테이블로 전환하는
방법을 먼저 검토하십시오. 메타데이터 컬럼은 지원 구문으로 추가하거나 삭제할 수 있습니다.

```sql
ALTER TABLE tag_create_demo
    METADATA ADD COLUMN (team VARCHAR(32));

ALTER TABLE tag_create_demo METADATA
    ADD COLUMN (limits DECIMAL(12,4)[2] DEFAULT [0.0000, NULL]);

ALTER TABLE tag_create_demo
    METADATA DROP COLUMN (team);

ALTER TABLE tag_create_demo METADATA
    DROP COLUMN (limits);
```

Standard Edition에서는 TAG METADATA에 고정 길이 숫자 ARRAY 컬럼을 추가할 수 있습니다.
ALTER 전에 존재한 metadata row에는 명시한 ARRAY DEFAULT를 적용합니다. ALTER 뒤 TAG DATA
입력으로 자동 등록되는 metadata row에는 DEFAULT를 다시 적용하지 않으며 새 ARRAY 컬럼은
whole NULL입니다.

TAG DATA의 일반 ARRAY 컬럼은 `CREATE TABLE`에서 선언할 수 있지만 ALTER로 추가할 수
없습니다. TAG METADATA ARRAY에는 자동 index를 만들지 않으며 명시적 index도 지원하지
않습니다. 자세한 규칙은 [TAG 메타데이터](../tag-metadata/)와
[숫자 ARRAY 타입](/dbms/reference/sql/type-data-types-dictionary/array/)을 참고하십시오.

데이터가 있는 운영 테이블에서는 변경 전에 의존 쿼리, SDK 컬럼 순서와 재입력 경로를
확인합니다.

## TAG 테이블 삭제

`DROP TABLE`은 원시 데이터와 메타데이터를 함께 제거합니다. ROLLUP 등 의존 객체가 있으면
먼저 의존 순서에 따라 정리해야 합니다.

```sql
DROP TABLE distance_create_demo;
DROP TABLE tag_create_demo;
```

정확한 속성, 허용 범위와 DDL은
[DDL 구문 사전](/dbms/reference/sql/syntax-dictionary-sql/ddl-syntax/)을 참고하십시오.

다음으로 읽을 내용:

- [TAG 테이블 구조와 스키마](../table-structure-schema/)
- [TAG 데이터 입력과 변경](../data-input-mutation/)
- [TAG 메타데이터](../tag-metadata/)
