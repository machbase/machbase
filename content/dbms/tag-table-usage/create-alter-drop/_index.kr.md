---
title: '5.3 생성, 변경, 삭제'
weight: 30
toc: true
---
TAG 테이블은 태그 식별자와 하나의 축 컬럼을 필수로 가집니다. 이 페이지에서는 실행 가능한
기본 예제를 제공하고, 전체 옵션은 SQL 레퍼런스로 연결합니다.

<a id="original-85-creating-tag-tables"></a>

## TAG 테이블 생성

TAG 테이블을 만들 때는 컬럼 순서에 따라 특별한 의미가 정해집니다.

| 컬럼 위치 | 용도와 특성 |
| --- | --- |
| 첫 번째 | 센서·설비·검사 회차처럼 반복해서 관측할 대상을 식별합니다. 같은 태그 이름으로 여러 DATA 행을 입력할 수 있으므로 관계형 테이블의 행별 고유 키와 다르게 이해합니다. |
| 두 번째 | 관측값을 시간 또는 거리·위치 기준으로 정렬·조회합니다. 한 TAG 테이블에는 시간축 또는 거리축 중 하나만 정의할 수 있습니다. |
| 세 번째 이후 | 온도, 압력, 상태, 품질 코드처럼 관측마다 달라지는 DATA 컬럼들입니다. 숫자형, 문자형, JSON, 숫자 ARRAY, BINARY 같은 값을 저장할 수 있습니다. 대표 통계·집계가 필요할 경우 세 번째 컬럼에 `SUMMARIZED`를 지정해서 기준 값으로 사용합니다. |

다음 두 테이블은 이 페이지의 독립 실습용입니다. 기존 객체가 없는지 확인한 뒤 순서대로
실행합니다. 시간축과 거리축 중 데이터의 실제 의미에 맞는 축을 선택합니다. 거리축 TAG에는
ROLLUP을 사용할 수 없습니다.

### 시간축 TAG

```sql
CREATE TAG TABLE ch5_tag_ddl (
    name  VARCHAR(32) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
) METADATA (
    location VARCHAR(64)
);
```

`SUMMARIZED`는 지원 숫자 타입이나 JSON에 지정할 수 있으며 ARRAY에는 지정할 수 없습니다.
이 컬럼이 있으면 TAG별 STAT 뷰의 `MIN_VALUE`, `MAX_VALUE` 같은 값 통계가 해당 컬럼을
기준으로 저장됩니다. 일반 숫자 ROLLUP은 `CREATE ROLLUP ... ON table(column)`에서 지정한
숫자 컬럼으로 만들 수 있으므로 `SUMMARIZED`가 필수는 아닙니다. 다만 `WITH ROLLUP` 자동
생성과 JSON 문서 전체 ROLLUP은 `SUMMARIZED` 컬럼을 사용합니다. ROLLUP 생성 조건은
[6장](../../tag-rollup-usage/)을 참고합니다. 위치·단위처럼 태그마다 한 번 저장하는 속성은
`METADATA`, 매 측정마다 달라지는 값은 일반 데이터 컬럼에 정의합니다.

### 거리축 TAG

```sql
CREATE TAG TABLE ch5_distance_ddl (
    name     VARCHAR(32) PRIMARY KEY,
    distance DOUBLE BASEDISTANCE,
    value    DOUBLE
);
```

소수 거리값에는 `DOUBLE`, 정수 축에는 값 범위에 맞는 `LONG` 또는 `ULONG`을 사용합니다.

## TAG 테이블 변경

이 절의 METADATA ADD/DROP 실습은 Standard Edition을 전제로 합니다.
TAG 데이터 컬럼의 임의 변경은 제한됩니다. 스키마를 확장해야 한다면 새 테이블로 전환하는
방법을 먼저 검토하십시오. 메타데이터 컬럼은 지원 구문으로 추가하거나 삭제할 수 있습니다.

```sql
ALTER TABLE ch5_tag_ddl
    METADATA ADD COLUMN (team VARCHAR(32));

ALTER TABLE ch5_tag_ddl METADATA
    ADD COLUMN (limits DECIMAL(12,4)[2] DEFAULT [0.0000, NULL]);

ALTER TABLE ch5_tag_ddl
    METADATA DROP COLUMN (team);

ALTER TABLE ch5_tag_ddl METADATA
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
확인합니다. ALTER 후 `DESC ch5_tag_ddl;`과 METADATA 조회로 변경 결과를 확인합니다.

## TAG 테이블 삭제

`DROP TABLE`은 원시 데이터와 메타데이터를 함께 제거합니다. ROLLUP 등 의존 객체가 있으면
먼저 의존 순서에 따라 정리해야 합니다. TAG의 `DROP TABLE ... CASCADE`는 연결된
ROLLUP도 제거할 수 있으므로 단순 정리의 기본 명령으로 사용하지 않습니다.
Custom ROLLUP의 대상 테이블은 별도 의존 제약도 확인합니다.

```sql
DROP TABLE ch5_distance_ddl;
DROP TABLE ch5_tag_ddl;
```

정확한 속성, 허용 범위와 DDL은
[DDL 구문 사전](/dbms/reference/sql/syntax-dictionary-sql/ddl-syntax/)을 참고하십시오.

다음으로 읽을 내용:

- [TAG 테이블 구조와 스키마](../table-structure-schema/)
- [TAG 데이터 입력과 변경](../data-input-mutation/)
- [TAG 메타데이터](../tag-metadata/)
