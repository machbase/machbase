---
type: docs
title: '13.5 조회와 분석 성능 튜닝'
weight: 50
toc: true
---
SELECT 쿼리와 집계 분석의 응답 시간을 단축하기 위한 실무 튜닝 기법을 다룹니다.

## 핵심 원칙

조회 성능을 결정하는 핵심 요소는 네 가지입니다.

### 1. 인덱스 활용

LOG 테이블은 생성된 인덱스를 동등·범위 조건과 JOIN 키에 사용할 수 있습니다. TAG 테이블은
태그 이름과 `BASETIME` 범위를 위한 전용 접근 경로를 제공합니다. WHERE 절의 조건 순서는
실행 계획을 강제하지 않으므로 `EXPLAIN`에서 실제 스캔과 `KEY RANGE`를 확인합니다.

### 2. 파티션 Pruning

LOG 테이블은 `_arrival_time`, TAG 테이블은 `time` 컬럼을 기준으로 데이터를 파티션에 분산
저장합니다. WHERE 절에 시간 범위를 명시하면 불필요한 파티션을 건너뜁니다. 시간 조건의
효과는 `EXPLAIN`과 실행 시간으로 확인합니다.

### 3. ROLLUP 사전 집계

원시 데이터를 매번 집계하는 대신 ROLLUP으로 미리 계산된 통계(MIN, MAX, AVG, COUNT 등)를
활용하면 반복 집계 비용을 줄일 수 있습니다. 분·시간·일 단위 추세 분석에 적합합니다.

### 4. 힌트 사용

`/*+ 힌트 */` 구문으로 병렬 처리 계수, 인덱스 사용 여부, ROLLUP 테이블 선택 등을
조정할 수 있습니다. 일반적인 JOIN 순서나 JOIN 알고리즘을 직접 고정하는 힌트는 제공하지
않습니다. 힌트는 실행 계획을 확인한 뒤 필요한 경우에만 사용합니다.

## 이 섹션의 구성

| 주제 | 설명 |
|------|------|
| [SELECT/JOIN 옵티마이저](/dbms/performance-tuning/performance-query-tuning/#select-join-optimizer) | JOIN 순서, 인덱스 선택, TAG pruning, EXPLAIN 해석 |
| [CTE 성능 고려사항](/dbms/performance-tuning/performance-query-tuning/#performance-cte) | 인라인 전개, 반복 참조와 필터 배치 |
| [검색 연산자 성능 튜닝](/dbms/performance-tuning/performance-query-tuning/#performance-operators-tuning) | 인덱스 활용 가능·불가 연산자, BITMAP vs LSM 선택 |
| [윈도우 함수와 PIVOT 성능 고려사항](/dbms/performance-tuning/performance-query-tuning/#performance-window-functions-considerations-pivot) | 메모리 주의사항, 서브쿼리 선처리 패턴 |
| [ROLLUP 활용 튜닝](/dbms/tag-rollup-usage/performance-tuning-rollup/#tuning-rollup) | ROLLUP 조회 패턴, 계층 설계, WAKEUP INTERVAL |
| [TAG 데이터 대량 정정 성능 고려사항](/dbms/tag-table-usage/tag-data-update-correction/#correction-performance-bulk-considerations-tag-data-update) | TAG data UPDATE 대상 범위와 롤업 재구성 |
| [LOOKUP DML 성능 고려사항](/dbms/lookup-table-usage/privilege-predicate-performance/#performance-considerations-lookup-predicate-dml) | PK fast path, 일반 predicate 대상 수집과 JSON SET 비용 |


<a id="performance-tuning-select"></a>
<a id="select-join-optimizer"></a>

## SELECT/JOIN 옵티마이저

<span class="badge-since">Machbase 8.7.0 기준</span>

이 절은 Standard Edition에서 사용자가 관찰할 수 있는 SELECT/JOIN 계획 선택 동작을
Machbase 8.7.0 기준으로 설명합니다. 옵티마이저와 `EXPLAIN` 자체가 8.7.0에서 처음
제공됐다는 의미는 아닙니다.

Machbase는 `SELECT` 문을 실행하기 전에 테이블을 읽는 순서와 접근 방법을 결정합니다.
JOIN에서는 `FROM` 절의 순서를 그대로 따르지 않고, 반복 작업을 줄이고 인덱스를 활용할
수 있는 실행 계획을 선택합니다.

JOIN 성능을 처음 점검할 때는 다음 세 가지를 먼저 확인합니다.

1. 어느 테이블을 먼저 읽는지 확인합니다.
2. 다음 테이블을 `FULL SCAN`하는지 인덱스로 검색하는지 확인합니다.
3. 인덱스로 처리하지 못한 조건이 `FILTER`에서 검사되는지 확인합니다.

계획은 테이블 종류, 인덱스, 조건식과 데이터 상태에 따라 달라질 수 있으므로 최종 판단은
현재 환경의 `EXPLAIN` 결과를 기준으로 합니다.

### 기본 조회 작성 원칙

- LOG와 TAG 조회에는 필요한 시간 범위를 명시합니다.
- TAG 조회 대상을 알면 태그 이름 조건도 함께 지정합니다.
- `SELECT *` 대신 필요한 컬럼만 조회합니다.
- `LIMIT`은 반환할 행 수를 제한하지만 전체 스캔 방지나 결과 순서를 보장하지 않습니다.
  출력 순서가 필요하면 `ORDER BY`를 사용합니다.

### 5분 빠른 시작

#### 계획 확인

실행하지 않고 계획만 확인하려면 `EXPLAIN`을 사용합니다.

```sql
EXPLAIN
SELECT E.CODE, C.NAME
FROM EVENT E, CODE C
WHERE E.CODE = C.CODE;
```

다음 순서로 읽습니다.

1. 처음 나타나는 스캔에서 먼저 읽는 테이블을 확인합니다.
2. 그 다음 스캔에 `INDEX SCAN`이 있는지 확인합니다.
3. `KEY RANGE`에 기대한 JOIN 컬럼이 있는지 확인합니다.
4. 큰 테이블이 두 번째 이후의 `FULL SCAN`으로 놓였는지 확인합니다.
5. 실제 `SELECT` 결과의 행 수와 주요 값을 함께 확인합니다.

대표적인 좋은 형태는 다음과 같습니다.

```text
FULL SCAN (EVENT)
VOLATILE INDEX SCAN (CODE)
  KEY RANGE: CODE = ...
```

`EVENT`를 한 번 읽고 각 행의 `CODE`로 `CODE` 테이블을 검색합니다. 내부 번호나 전체
들여쓰기보다 스캔 종류, 테이블 이름과 `KEY RANGE` 컬럼을 보는 것이 중요합니다.

#### 주의해서 볼 형태

```text
FULL SCAN (SMALL_TABLE)
FULL SCAN (LARGE_TABLE)
```

두 번째의 큰 테이블은 첫 테이블의 각 행마다 반복해서 읽을 수 있습니다. 다만 `FULL SCAN`
자체가 항상 문제인 것은 아닙니다. 한 번만 수행되는 스캔이나 매우 작은 테이블의 스캔은
정상일 수 있습니다. 주의할 대상은 큰 inner 테이블의 반복 `FULL SCAN`입니다.

#### 태그 테이블 빠른 조회의 기본 형태

태그 테이블은 일반 테이블처럼 `TIME` 인덱스를 별도로 만드는 방식이 아닙니다.
`BASETIME`으로 선언한 시간 컬럼의 전용 접근 경로를 자동으로 사용합니다. 대량
시계열을 조회할 때는 먼저 시간 범위를 명시하고, 대상 태그를 알면 태그 이름 조건도
함께 제공하는 것이 가장 중요한 기본 형태입니다.

```sql
WHERE NAME = 'sensor-a'
  AND TIME >= TO_DATE('2026-08-17 10:00:00')
  AND TIME <  TO_DATE('2026-08-17 11:00:00')
```

시간 범위는 필요 없는 시간 구간을 제외하고, 태그 이름은 다른 시계열까지 제외합니다.
별도의 `CREATE INDEX ... (TIME)`은 필요하지 않습니다.

#### 결과 순서

실행 계획이 달라지면 결과 행의 반환 순서도 달라질 수 있습니다. `LIMIT`만으로 순서가
고정되지는 않습니다. 출력 순서가 필요하면 반드시 `ORDER BY`를 사용합니다.

### 기본 용어

| 용어 | 의미 |
| --- | --- |
| outer 테이블 | JOIN에서 먼저 읽는 테이블입니다. 읽은 각 행의 값이 다음 테이블의 검색 조건으로 사용됩니다. |
| inner 테이블 | outer 행마다 조건에 맞는 행을 찾는 테이블입니다. 적절한 인덱스가 있으면 반복 검색 비용을 줄일 수 있습니다. |
| access path | `FULL SCAN`, `INDEX SCAN`처럼 테이블을 읽는 방법입니다. |
| JOIN 조건 | 서로 다른 테이블의 행을 연결하는 조건입니다. 예: `A.ID = B.ID` |
| 해당 테이블만의 조건 | 다른 테이블 값 없이 한 테이블만으로 계산할 수 있는 조건입니다. 예: `A.ID = 1` |
| 키 범위 | 인덱스 탐색에 직접 사용하는 `=`, `<`, `<=`, `>`, `>=` 조건입니다. |
| 최종 필터 | 인덱스로 후보를 줄인 뒤 원래 SQL 조건을 최종 확인하는 조건입니다. 계획에는 `FILTER`로 표시됩니다. |
| 복합 인덱스의 선두 컬럼 | 인덱스 정의에서 가장 먼저 나오는 컬럼입니다. `(A, B)` 인덱스에서는 `A`입니다. |

### 테이블 종류별 실무 특성

Machbase는 준비 시점에 즉시 알 수 있는 행 수 정보와 인덱스 사용 가능 여부를 활용해
계획을 선택합니다.

| 테이블 종류 | 행 수 정보 | 주요 접근 특성 |
| --- | --- | --- |
| LOG | 현재 행 수를 빠르게 얻을 수 있습니다. | 생성된 인덱스가 있으면 동등·범위 조건과 JOIN key에 사용할 수 있습니다. |
| VOLATILE | 현재 행 수를 빠르게 얻을 수 있습니다. | 기본 키 동등 검색을 우선 활용합니다. |
| LOOKUP | 현재 행 수를 빠르게 얻을 수 있습니다. | 기본 키 동등 검색이 빠르며 계획에는 `VOLATILE INDEX SCAN`으로 표시될 수 있습니다. |
| 태그 | 현재 행 수를 빠르게 얻을 수 있습니다. | 태그 이름으로 대상 시계열을 고르고 `BASETIME` 범위로 필요한 시간 구간만 읽을 수 있습니다. 시간 접근 경로는 자동 제공됩니다. |
| TRANSACTION | 계획 준비를 위해 전체 테이블을 세지 않습니다. | 기본 키, UNIQUE 및 일반 TRANSACTION 인덱스를 활용합니다. |
| FIXED | 일반적인 행 수를 알 수 없는 대상으로 취급합니다. | 대상이 제공하는 스캔 방식에 따라 실행합니다. |
| 단순 VIEW | 원본 테이블의 행 수가 상한으로 전달될 수 있습니다. | VIEW 필터가 행을 줄이므로 base 행 수를 실제 결과 행 수로 보지 않습니다. |

#### 태그 이름과 시간 범위로 읽기 범위 줄이기(pruning)

태그에서 `PRIMARY KEY`로 선언한 `NAME`은 개별 측정 행이 아니라 시계열을 식별합니다.
따라서 같은 `NAME`에 서로 다른 `TIME`의 측정값을 여러 건 저장할 수 있습니다.

pruning은 모든 데이터를 읽은 뒤 결과를 버리는 후처리가 아닙니다. 읽기 전에 필요 없는
태그와 시간 구간을 제외해 스캔 후보 자체를 줄이는 것입니다.

```text
전체 TAG 데이터
  → NAME 조건으로 대상 시계열 선택(조건이 있는 경우)
  → TIME 범위와 교차해 필요한 시간 구간 선택
  → VALUE 등 나머지 조건을 최종 확인
```

| 조건 | 읽기 범위 |
| --- | --- |
| `NAME = ... AND TIME >= ... AND TIME < ...` | 선택한 태그의 지정 시간 구간만 대상으로 삼습니다. 가장 권장하는 일반 형태입니다. |
| `TIME >= ... AND TIME < ...` | 시간 구간은 줄지만 그 구간에 포함된 여러 태그를 확인할 수 있습니다. |
| `NAME = ...` | 한 태그만 고르지만 그 태그의 전체 이력이 후보가 될 수 있습니다. |
| `VALUE ...`만 사용 | 태그와 시간으로 먼저 줄이지 못해 많은 후보를 읽고 최종 필터로 검사할 수 있습니다. |

정확한 단일 태그 이름과 유효한 시간 범위를 함께 제공하면 대상 시계열을 좁힌 뒤
그 안에서 필요한 시간 구간을 탐색할 수 있습니다. 실제 효과는 선택한 태그 수, 시간 폭과
데이터 상태에 따라 달라지므로 `EXPLAIN`으로 확인합니다.

행 수는 계획을 준비한 시점의 정보입니다. prepared statement를 재사용하는 동안 데이터가 크게
변하면 같은 계획이 계속 사용될 수 있습니다. 데이터나 인덱스가 크게 변한 뒤에는 중요한
질의를 다시 준비하고 `EXPLAIN`으로 확인하는 것이 좋습니다.

작은 테이블이 항상 먼저 실행되는 것은 아닙니다. 작은 테이블을 먼저 읽은 뒤 큰 테이블을
반복 `FULL SCAN`해야 한다면, 큰 테이블을 한 번 읽고 작은 테이블을 인덱스로 반복
검색하는 편이 더 유리할 수 있습니다. 행 수와 inner 인덱스의 사용 가능 여부를 함께 확인합니다.

### JOIN 순서와 인덱스 선택

#### JOIN 순서

옵티마이저는 다음 정보를 함께 고려합니다.

1. 한 테이블의 조건만으로 기본 키 또는 UNIQUE key가 완전히 정해져 최대 한 행인가
2. 이미 읽은 테이블의 값으로 다음 테이블의 인덱스를 검색할 수 있는가
3. inner `FULL SCAN`을 반복하는 계획을 피할 수 있는가
4. 준비 시점에 비교할 수 있는 행 수 또는 안전한 상한이 있는가
5. 같은 품질의 계획이라면 일관된 순서를 선택할 수 있는가

따라서 `FROM A, B`로 작성해도 계획은 `B`를 먼저 읽을 수 있습니다. `FROM` 절의 순서를
바꾸는 것은 계획을 강제하는 방법이 아닙니다.

Standard Edition에서는 JOIN에 참여하는 모든 테이블이 동등, 범위 또는 함수 조건의
연결 사슬에 포함되어야 합니다. 연결 조건이 전혀 없는 테이블이 있으면 의도하지 않은
Cartesian JOIN을 막기 위해 질의 준비가 거부될 수 있습니다.

#### 인덱스를 사용하기 쉬운 조건

양쪽이 직접적인 컬럼 참조인 다음 조건은 JOIN 인덱스 검색 후보가 될 수 있습니다.

```sql
A.ID = B.ID
A.TIME >= B.START_TIME
A.VALUE < B.LIMIT_VALUE
```

피연산자의 좌우 순서는 중요하지 않습니다. `A.ID = B.ID`와 `B.ID = A.ID`는 같은
인덱스 후보를 만들 수 있습니다.

반면 인덱스 컬럼을 함수나 산술식으로 감싸면 저장된 인덱스 key와 직접 비교하기
어렵습니다.

```sql
A.ID + 0 = B.ID
SUBSTR(A.CODE, 1, 3) = B.PREFIX
```

이 조건들은 보통 후보 행을 읽은 뒤 `FILTER`에서 평가됩니다. 업무 의미상 가능하면
별도의 직접 JOIN key를 함께 제공합니다.

#### 복합 인덱스

다음 복합 UNIQUE 인덱스를 예로 듭니다.

```sql
CREATE UNIQUE INDEX IDX_ACCOUNT_UQ
ON ACCOUNT(TENANT_ID, ACCOUNT_ID);
```

| 제공된 조건 | 사용 가능성 |
| --- | --- |
| `TENANT_ID = ... AND ACCOUNT_ID = ...` | 두 key를 모두 사용하며 최대 한 행을 찾을 수 있습니다. |
| `TENANT_ID = ...` | 선두 prefix 검색은 가능하지만 여러 행일 수 있습니다. |
| `ACCOUNT_ID = ...` | 선두 컬럼이 없어 이 복합 인덱스로 키 범위를 만들기 어렵습니다. |

TRANSACTION 테이블에 여러 인덱스가 있으면 primary/UNIQUE의 모든 key가 동등 조건으로
정해진 인덱스, 더 긴 선두 동등 prefix를 가진 인덱스, 그 다음 범위 조건까지 사용할
수 있는 인덱스가 유리합니다.

### 함수, VIEW, OUTER JOIN과 정확성을 위한 안전 경로

#### 함수 조건

여러 테이블을 참조하는 함수 조건은 필요한 모든 테이블이 준비된 단계에서 최종
필터로 평가할 수 있습니다. 함수 조건만으로 직접 인덱스 검색을 기대해서는 안 됩니다.

```sql
WHERE E.CODE = C.CODE
  AND SUBSTR(E.MESSAGE, C.POS, 1) <> '_'
```

위 SQL에서는 `E.CODE = C.CODE`가 인덱스 검색에 쓰이고 `SUBSTR` 조건은 최종
결과를 확인합니다.

#### VIEW

단일 원본 테이블의 컬럼을 직접 투영하는 단순 inline view는 안전한 경우 외부 JOIN
조건이 base 스캔으로 전달될 수 있습니다. VIEW 필터가 있으면 원본 테이블의 행 수는
실제 VIEW 결과 행 수가 아니라 상한입니다.

저장 VIEW 또는 집계, `DISTINCT`, `ORDER BY`, `LIMIT` 등이 포함된 복잡한 VIEW가
같은 방식으로 최적화된다고 단정할 수 없습니다. 실제 원본 테이블 접근과 인덱스 사용
여부를 `EXPLAIN`으로 확인합니다.

#### OUTER JOIN

OUTER JOIN에서는 조건의 위치가 결과 자체를 바꿀 수 있습니다.

```sql
-- B가 없어도 A 행을 유지합니다. B.STATUS는 매치 조건입니다.
SELECT A.ID, B.STATUS
FROM A LEFT JOIN B
  ON A.ID = B.ID
 AND B.STATUS = 'ACTIVE';

-- B가 없는 행은 WHERE에서 제거될 수 있습니다.
SELECT A.ID, B.STATUS
FROM A LEFT JOIN B
  ON A.ID = B.ID
WHERE B.STATUS = 'ACTIVE';
```

오른쪽 테이블의 조건으로 매치 여부를 결정하려면 `ON`에 둡니다. NULL로 채워진 결과를
그 이후에 걸러내려는 의도일 때만 `WHERE`에 둡니다. 성능을 이유로 조건을 옮기기 전에
결과 행 수와 NULL 행이 같은지 반드시 확인합니다.

#### 정확성을 위한 안전한 전체 스캔 전환

JOIN 값을 TRANSACTION 인덱스의 key로 바꿀 때 비교 의미가 달라질 수 있으면 Machbase는
결과 누락을 막기 위해 인덱스 대신 `FULL SCAN`과 최종 필터를 선택할 수 있습니다.

대표적인 경우는 다음과 같습니다.

- 서로 다른 크기나 signed/unsigned 정수 타입
- 정밀도를 잃을 수 있는 `FLOAT`, `DOUBLE`, `DECIMAL` 범위 비교
- 짧은 `VARCHAR` 인덱스와 더 긴 문자열의 범위 비교

IPV4 wildcard처럼 실제 값에 따라 안전성이 달라지는 경우에는 `EXPLAIN`에 인덱스
스캔이 표시되더라도 해당 outer 행을 처리할 때 안전한 전체 스캔으로 전환할 수
있습니다. 따라서 계획 텍스트만으로 모든 실행 시점의 안전 경로 전환을 판단하지 않습니다.

`INDEX SCAN`과 `FILTER`가 함께 표시되는 것도 정상입니다. 인덱스는 후보를 줄이고,
`FILTER`는 원래 SQL 조건을 최종 확인해 정확성을 지킵니다.

성능이 중요하면 JOIN 컬럼의 타입, 정수 범위와 문자열 길이를 같게 설계하는 것이
가장 안전합니다. 임의의 `CAST`를 추가하기 전에 결과와 계획을 다시 확인합니다.

### EXPLAIN과 EXPLAIN FULL 읽기

#### 기본 사용법

```sql
EXPLAIN
SELECT ...
FROM ...
WHERE ...;
```

질의를 실제로 실행하면서 내부 작업량도 확인하려면 다음을 사용합니다.

```sql
EXPLAIN FULL
SELECT ...
FROM ...
WHERE ...;
```

`EXPLAIN FULL`은 결과를 끝까지 읽으며 statement 동안 누적된 내부 작업 count와
timebox profile을 보여줍니다. 일반적인 operator별 actual rows, loops, time과는
다릅니다. 같은 데이터와 환경에서 두 SQL의 상대 작업량을 비교하는 보조 자료로
사용합니다. 운영 환경에서는 부하와 결과 건수를 먼저 고려합니다.

#### 주요 출력

| 출력 | 해석 |
| --- | --- |
| `FULL SCAN (T)` / `VOLATILE FULL SCAN (T)` | 테이블 `T` 전체를 읽습니다. inner라면 반복될 수 있습니다. |
| `INDEX SCAN (T)` | LOG 등의 인덱스 범위를 사용합니다. |
| `VOLATILE INDEX SCAN (T)` | VOLATILE 또는 LOOKUP의 key 인덱스를 사용합니다. 테이블 이름도 함께 확인합니다. |
| `TRANSACTION INDEX SCAN (T)` | TRANSACTION 테이블의 인덱스를 사용합니다. |
| `TAG READ (RAW)` | 태그 테이블 전용 raw read 노드입니다. 이 문구만으로 전체 스캔이라고 판단하지 않고 하위 접근을 함께 확인합니다. |
| `KEYVALUE INDEX SCAN (...)` | 태그 raw 데이터의 key/인덱스 접근입니다. 실제로 사용한 시간·태그·일반 인덱스 조건은 하위 `KEY RANGE`에서 확인합니다. |
| `KEY RANGE` | 인덱스 탐색에 실제로 사용된 조건입니다. |
| `FILTER` | 후보 행에 원래 SQL 조건을 최종 적용합니다. |

계획은 다음 순서로 점검합니다.

1. 실제 SELECT 결과와 행 수를 기록합니다.
2. outer와 inner 순서를 확인합니다.
3. 큰 inner 테이블의 반복 `FULL SCAN`을 찾습니다.
4. `KEY RANGE`에 기대한 JOIN 컬럼이 있는지 확인합니다.
5. 복합 인덱스의 선두 컬럼이 조건에 포함됐는지 확인합니다.
6. JOIN 컬럼의 타입과 길이를 비교합니다.
7. 함수나 산술식이 인덱스 컬럼을 감쌌는지 확인합니다.
8. SQL 또는 인덱스를 한 가지씩 변경합니다.
9. 결과 행 수와 주요 값이 같은지 먼저 비교합니다.
10. 필요하면 같은 데이터에서 `EXPLAIN FULL`의 상대 작업량을 비교합니다.

### 실전 예제

첫 번째 태그 예제는 독립적으로 실행합니다. 이후 예제는 LOG와 LOOKUP 예제의 공통
테이블을 재사용합니다. 같은 이름의 객체가 있으면 아래 예제 정리 SQL을 먼저 실행합니다.

#### 태그 이름과 `BASETIME` 범위로 pruning

다음은 별도 `TIME` 인덱스를 만들지 않고 한 sensor의 10분 구간만 읽는 예제입니다.

```sql
CREATE TAG TABLE OPT_SENSOR (
    NAME VARCHAR(32) PRIMARY KEY,
    TIME DATETIME BASETIME,
    VALUE DOUBLE SUMMARIZED
);

INSERT INTO OPT_SENSOR VALUES
    ('sensor-a', TO_DATE('2026-08-17 09:55:00'), 10);
INSERT INTO OPT_SENSOR VALUES
    ('sensor-a', TO_DATE('2026-08-17 10:05:00'), 11);
INSERT INTO OPT_SENSOR VALUES
    ('sensor-a', TO_DATE('2026-08-17 10:15:00'), 12);
INSERT INTO OPT_SENSOR VALUES
    ('sensor-b', TO_DATE('2026-08-17 10:05:00'), 21);

-- 이 예제에서는 방금 입력한 TAG 데이터를 즉시 확인할 수 있도록 flush합니다.
EXEC TABLE_FLUSH(OPT_SENSOR);

EXPLAIN
SELECT NAME, TIME, VALUE
FROM OPT_SENSOR
WHERE NAME = 'sensor-a'
  AND TIME >= TO_DATE('2026-08-17 10:00:00')
  AND TIME <  TO_DATE('2026-08-17 10:10:00')
ORDER BY TIME;

SELECT NAME, TIME, VALUE
FROM OPT_SENSOR
WHERE NAME = 'sensor-a'
  AND TIME >= TO_DATE('2026-08-17 10:00:00')
  AND TIME <  TO_DATE('2026-08-17 10:10:00')
ORDER BY TIME;
```

결과는 `sensor-a`, `10:05`, 값 `11`인 한 행입니다. `NAME`은 `sensor-b` 전체를
제외하고, 시간 조건은 `sensor-a`의 10시 이전과 10시 10분 이후 이력을 제외합니다.
`[시작, 종료)` 형태는 연속된 시간 창에서 경계 행의 중복을 피하기 좋습니다.

대표적인 계획은 다음 형태입니다.

```text
TAG READ (RAW)
  KEYVALUE INDEX SCAN (...)
    KEY RANGE: TIME 범위
  VOLATILE INDEX SCAN (...)
    KEY RANGE: NAME = 'sensor-a'
```

괄호 안의 내부 테이블 이름은 버전에 따라 달라질 수 있으므로 검사 대상으로 고정하지
않습니다. 중요한 것은 다음 세 가지입니다.

1. `TAG READ (RAW)` 아래 `KEYVALUE INDEX SCAN`이 있는가
2. 이 단일-테이블 예제의 시간 범위가 `KEY RANGE`에 있는가
3. 태그 이름이 별도의 인덱스 `KEY RANGE`로 사용됐는가

시간 조건만 사용해도 시간 pruning은 동작합니다. 태그 이름까지 알면 다른 시계열을
추가로 제외할 수 있어 일반적으로 더 유리합니다. 반대로 `VALUE` 조건은 태그와 시간으로
후보를 줄인 뒤 `FILTER`에서 검사될 수 있습니다.

다른 테이블이 태그 이름과 조회 시간창을 제공하는 JOIN도 같은 장점을 활용할 수 있습니다.

```sql
CREATE LOOKUP TABLE OPT_SENSOR_WINDOW (
    NAME VARCHAR(32) PRIMARY KEY,
    START_TIME DATETIME,
    END_TIME DATETIME
);

INSERT INTO OPT_SENSOR_WINDOW VALUES (
    'sensor-a',
    TO_DATE('2026-08-17 10:00:00'),
    TO_DATE('2026-08-17 10:10:00')
);

EXPLAIN
SELECT T.NAME, T.TIME, T.VALUE
FROM OPT_SENSOR_WINDOW W, OPT_SENSOR T
WHERE T.NAME = W.NAME
  AND T.TIME >= W.START_TIME
  AND T.TIME < W.END_TIME
ORDER BY T.TIME;

SELECT T.NAME, T.TIME, T.VALUE
FROM OPT_SENSOR_WINDOW W, OPT_SENSOR T
WHERE T.NAME = W.NAME
  AND T.TIME >= W.START_TIME
  AND T.TIME < W.END_TIME
ORDER BY T.TIME;
```

이 JOIN도 결과는 한 행입니다. LOOKUP의 한 행이 태그 이름과 시간창을 제공하면 태그는
사용 가능한 시간 경계로 후보 범위를 줄이고 나머지 경계를 `FILTER`로 최종 확인할
수 있습니다. 시간 pruning을 확인하려면 적어도 하나의 `TIME` 경계가 `KEY RANGE`에
있는지 확인합니다. 모든 시간 조건이 `FILTER`에만 있다면 해당 시간 조건 자체로 읽기
범위가 줄었다고 판단하지 않습니다.

#### LOG에서 LOOKUP 기본 키 검색

```sql
CREATE LOOKUP TABLE OPT_CODE (
    CODE INTEGER PRIMARY KEY,
    NAME VARCHAR(20),
    POS INTEGER
);

CREATE LOG TABLE OPT_EVENT (
    CODE INTEGER,
    MESSAGE VARCHAR(40),
    VALUE DOUBLE
);

INSERT INTO OPT_CODE VALUES (1, 'NORMAL', 1);
INSERT INTO OPT_CODE VALUES (2, 'WARN', 1);
INSERT INTO OPT_EVENT VALUES (1, 'started', 10.5);
INSERT INTO OPT_EVENT VALUES (2, 'warning', 20.5);
INSERT INTO OPT_EVENT VALUES (2, 'retry', 21.0);

EXPLAIN
SELECT E.CODE, C.NAME, E.MESSAGE
FROM OPT_EVENT E, OPT_CODE C
WHERE E.CODE = C.CODE
ORDER BY E.CODE, E.MESSAGE;

SELECT E.CODE, C.NAME, E.MESSAGE
FROM OPT_EVENT E, OPT_CODE C
WHERE E.CODE = C.CODE
ORDER BY E.CODE, E.MESSAGE;
```

결과는 3행입니다. 핵심 계획은 다음과 같습니다.

```text
FULL SCAN (OPT_EVENT)
VOLATILE INDEX SCAN (OPT_CODE)
  KEY RANGE: CODE = ...
```

각 event마다 LOOKUP 전체를 읽지 않고 `CODE` 기본 키로 필요한 행만 찾습니다.

#### 직접 JOIN key와 함수 최종 필터

```sql
EXPLAIN
SELECT E.CODE, C.NAME, E.MESSAGE
FROM OPT_EVENT E, OPT_CODE C
WHERE E.CODE = C.CODE
  AND SUBSTR(E.MESSAGE, C.POS, 1) <> '_'
ORDER BY E.CODE, E.MESSAGE;

SELECT COUNT(*)
FROM OPT_EVENT E, OPT_CODE C
WHERE E.CODE = C.CODE
  AND SUBSTR(E.MESSAGE, C.POS, 1) <> '_';
```

현재 데이터의 결과는 3입니다. `E.CODE = C.CODE`는 LOOKUP 키 범위를 유지하고,
`SUBSTR`은 두 테이블의 값이 준비된 뒤 `FILTER`에서 평가됩니다.

#### LOG, LOOKUP, VOLATILE의 3-테이블 JOIN

```sql
CREATE VOLATILE TABLE OPT_STATE (
    CODE INTEGER PRIMARY KEY,
    STATE VARCHAR(20)
);

INSERT INTO OPT_STATE VALUES (1, 'ACTIVE');
INSERT INTO OPT_STATE VALUES (2, 'PAUSED');

EXPLAIN
SELECT E.CODE, C.NAME, S.STATE, E.MESSAGE
FROM OPT_EVENT E, OPT_CODE C, OPT_STATE S
WHERE E.CODE = C.CODE
  AND C.CODE = S.CODE
ORDER BY E.CODE, E.MESSAGE;

SELECT COUNT(*)
FROM OPT_EVENT E, OPT_CODE C, OPT_STATE S
WHERE E.CODE = C.CODE
  AND C.CODE = S.CODE;
```

결과는 3입니다. `OPT_EVENT`를 읽은 뒤 `OPT_CODE`와 `OPT_STATE`를 각각 기본 키로
검색하는지 확인합니다. LOOKUP과 VOLATILE 모두 `VOLATILE INDEX SCAN`으로 표시될 수
있으므로 테이블 이름을 함께 확인합니다.

#### TRANSACTION 복합 UNIQUE 인덱스

```sql
CREATE TRANSACTION TABLE OPT_ACCOUNT (
    ID INTEGER PRIMARY KEY,
    TENANT_ID INTEGER,
    ACCOUNT_ID INTEGER,
    ACCOUNT_NAME VARCHAR(30)
);

CREATE UNIQUE INDEX OPT_ACCOUNT_UQ
ON OPT_ACCOUNT(TENANT_ID, ACCOUNT_ID);

CREATE LOOKUP TABLE OPT_REQUEST (
    REQUEST_ID INTEGER PRIMARY KEY,
    TENANT_ID INTEGER,
    ACCOUNT_ID INTEGER
);

INSERT INTO OPT_ACCOUNT VALUES (1, 10, 100, 'alpha');
INSERT INTO OPT_ACCOUNT VALUES (2, 10, 200, 'beta');
INSERT INTO OPT_ACCOUNT VALUES (3, 20, 100, 'gamma');
INSERT INTO OPT_REQUEST VALUES (1, 10, 100);
INSERT INTO OPT_REQUEST VALUES (2, 10, 200);

EXPLAIN
SELECT R.REQUEST_ID, A.ACCOUNT_NAME
FROM OPT_REQUEST R, OPT_ACCOUNT A
WHERE A.TENANT_ID = R.TENANT_ID
  AND A.ACCOUNT_ID = R.ACCOUNT_ID
ORDER BY R.REQUEST_ID;
```

결과는 2행입니다. `TRANSACTION INDEX SCAN (OPT_ACCOUNT)`과 `TENANT_ID`,
`ACCOUNT_ID` 두 `KEY RANGE`를 확인합니다.

다음 세 계획을 비교하면 복합 인덱스의 선두 규칙을 확인할 수 있습니다.

```sql
-- 두 key: 두 컬럼을 모두 사용하며 최대 한 행
EXPLAIN SELECT COUNT(*)
FROM OPT_REQUEST R, OPT_ACCOUNT A
WHERE A.TENANT_ID = R.TENANT_ID
  AND A.ACCOUNT_ID = R.ACCOUNT_ID;

-- 선두 key: prefix 검색 가능, 여러 행일 수 있음
EXPLAIN SELECT COUNT(*)
FROM OPT_REQUEST R, OPT_ACCOUNT A
WHERE A.TENANT_ID = R.TENANT_ID;

-- 두 번째 key만 사용: 이 복합 index의 선두 범위를 만들기 어려움
EXPLAIN SELECT COUNT(*)
FROM OPT_REQUEST R, OPT_ACCOUNT A
WHERE A.ACCOUNT_ID = R.ACCOUNT_ID;
```

#### 인덱스 컬럼을 가공한 경우

```sql
-- 권장 형태
EXPLAIN SELECT COUNT(*)
FROM OPT_REQUEST R, OPT_ACCOUNT A
WHERE A.TENANT_ID = R.TENANT_ID
  AND A.ACCOUNT_ID = R.ACCOUNT_ID;

-- 결과는 같지만 복합 index의 선두 key를 직접 사용하기 어려운 형태
EXPLAIN SELECT COUNT(*)
FROM OPT_REQUEST R, OPT_ACCOUNT A
WHERE A.TENANT_ID + 0 = R.TENANT_ID
  AND A.ACCOUNT_ID = R.ACCOUNT_ID;
```

두 SELECT의 결과는 모두 2입니다. 두 번째 SQL에서는 `TENANT_ID`가 직접적인 key가
아니므로 TRANSACTION `FULL SCAN`이 선택될 수 있습니다. 함수 자체가 항상 느린 것이
아니라, 인덱스 컬럼을 가공해 저장된 key와 직접 비교하기 어려워진 것이 핵심입니다.

#### 단순 VIEW의 base 접근 확인

```sql
CREATE VIEW OPT_ACTIVE_EVENT AS
SELECT CODE, MESSAGE, VALUE
FROM OPT_EVENT
WHERE VALUE >= 20;

EXPLAIN
SELECT V.CODE, C.NAME, V.MESSAGE
FROM OPT_ACTIVE_EVENT V, OPT_CODE C
WHERE V.CODE = C.CODE
ORDER BY V.CODE, V.MESSAGE;

SELECT V.CODE, C.NAME, V.MESSAGE
FROM OPT_ACTIVE_EVENT V, OPT_CODE C
WHERE V.CODE = C.CODE
ORDER BY V.CODE, V.MESSAGE;
```

결과는 `retry`, `warning` 두 행입니다. VIEW 이름만 찾지 말고 실제 base인
`OPT_EVENT`, `VALUE >= 20` 조건, `OPT_CODE`의 key 접근을 함께 확인합니다.

#### 세 테이블을 함께 참조하는 함수 조건

```sql
CREATE LOOKUP TABLE OPT_TEXT (ID INTEGER PRIMARY KEY, CODE VARCHAR(8));
CREATE LOOKUP TABLE OPT_POSITION (ID INTEGER PRIMARY KEY, POS INTEGER);
CREATE LOOKUP TABLE OPT_EXPECTED (ID INTEGER PRIMARY KEY, EXPECTED VARCHAR(2));

INSERT INTO OPT_TEXT VALUES (1, 'AX');
INSERT INTO OPT_TEXT VALUES (2, 'BY');
INSERT INTO OPT_POSITION VALUES (1, 1);
INSERT INTO OPT_POSITION VALUES (2, 2);
INSERT INTO OPT_EXPECTED VALUES (1, 'A');
INSERT INTO OPT_EXPECTED VALUES (2, 'Y');
INSERT INTO OPT_EXPECTED VALUES (3, 'Z');

EXPLAIN
SELECT COUNT(*)
FROM OPT_TEXT A, OPT_POSITION B, OPT_EXPECTED C
WHERE SUBSTR(A.CODE, B.POS, 1) = C.EXPECTED;

SELECT COUNT(*)
FROM OPT_TEXT A, OPT_POSITION B, OPT_EXPECTED C
WHERE SUBSTR(A.CODE, B.POS, 1) = C.EXPECTED;
```

결과는 2입니다. 이 함수는 세 테이블의 값이 모두 있어야 판정할 수 있으므로 직접적인 PK
검색 조건처럼 동작하지 않습니다. 중간 후보 조합이 많아질 수 있으므로 업무 의미상
가능하면 직접적인 JOIN key를 함께 제공합니다.

#### 정확성을 위한 문자열 범위의 안전한 전체 스캔 전환

```sql
CREATE LOG TABLE OPT_LONG_KEY (K VARCHAR(10));
CREATE TRANSACTION TABLE OPT_SHORT_KEY (K VARCHAR(5));
CREATE INDEX OPT_SHORT_KEY_IDX ON OPT_SHORT_KEY(K);

INSERT INTO OPT_LONG_KEY VALUES ('abcdeZ');
INSERT INTO OPT_SHORT_KEY VALUES ('abcde');
INSERT INTO OPT_SHORT_KEY VALUES ('abcdf');

EXPLAIN
SELECT COUNT(*)
FROM OPT_LONG_KEY L, OPT_SHORT_KEY T
WHERE T.K < L.K;

SELECT COUNT(*)
FROM OPT_LONG_KEY L, OPT_SHORT_KEY T
WHERE T.K < L.K;
```

결과는 1입니다. 긴 outer 값을 `VARCHAR(5)` key로 잘라 범위를 만들면 정상 후보를
잃을 수 있으므로 `OPT_SHORT_KEY`의 `FULL SCAN`은 올바른 선택입니다.

반대로 동등 비교는 안전한 후보 범위를 만들 수 있습니다.

```sql
INSERT INTO OPT_LONG_KEY VALUES ('abcde');

EXPLAIN
SELECT COUNT(*)
FROM OPT_LONG_KEY L, OPT_SHORT_KEY T
WHERE T.K = L.K;
```

이 경우 `TRANSACTION INDEX SCAN (OPT_SHORT_KEY)`과 `KEY RANGE`를 기대할 수 있습니다.
같은 두 타입도 비교 연산자에 따라 안전한 접근 방법이 달라질 수 있습니다.

### 자주 발생하는 안티패턴

| 형태 | 왜 불리한가 | 권장 방향 |
| --- | --- | --- |
| `A.ID + 0 = B.ID` | 직접적인 인덱스 key로 사용하기 어렵습니다. | 의미가 같다면 `A.ID = B.ID`로 작성합니다. |
| 함수 조건만으로 JOIN | 함수 계산 뒤 최종 비교가 필요합니다. | 저장된 직접 JOIN key를 함께 제공합니다. |
| `(A, B)` 인덱스에 `B` 조건만 제공 | 선두 컬럼이 준비되지 않습니다. | `A` 조건을 제공하거나 목적에 맞는 인덱스를 설계합니다. |
| 큰 테이블이 inner `FULL SCAN` | outer 행마다 반복될 수 있습니다. | inner JOIN 컬럼의 인덱스와 전체 JOIN 방향을 검토합니다. |
| 서로 다른 숫자·문자열 타입 JOIN | 안전한 인덱스 범위를 만들지 못할 수 있습니다. | 스키마의 타입, 범위와 문자열 길이를 맞춥니다. |
| `LIMIT`만 사용하고 `ORDER BY` 생략 | 반환 순서가 계획에 따라 달라질 수 있습니다. | 필요한 정렬 기준을 `ORDER BY`에 명시합니다. |

### 자주 묻는 질문

#### 인덱스가 있는데 왜 FULL 스캔인가?

현재 JOIN 단계에서 인덱스의 선두 key 값을 만들 수 없거나, 컬럼이 함수로 감싸졌거나,
타입 변환이 정상 후보를 누락시킬 수 있기 때문입니다. `KEY RANGE`, 복합 인덱스 순서와
양쪽 컬럼 타입을 확인합니다.

#### 태그의 TIME 컬럼에 인덱스를 만들어야 하나?

아닙니다. `BASETIME`으로 선언한 시간 컬럼은 태그 테이블이 제공하는 전용 시간 접근
경로를 자동으로 사용합니다. SQL에 명확한 시간 범위를 주고 `EXPLAIN`에서 `TAG READ`
아래 `KEYVALUE INDEX SCAN`의 `KEY RANGE`에 시간 조건이 있는지 확인합니다.

#### 태그 조회에 시간 범위만 있으면 충분한가?

시간 pruning은 되지만 해당 구간의 여러 태그를 함께 확인할 수 있습니다. 조회 대상 태그를
알면 정확한 `NAME = ...` 조건이나 작은 `NAME IN (...)` 목록도 함께 제공하는 편이
보통 더 유리합니다.

#### `TAG READ (RAW)`는 FULL 스캔을 뜻하나?

아닙니다. 태그 전용 읽기 노드의 이름입니다. 그 아래가 `KEYVALUE INDEX SCAN`인지
`KEYVALUE FULL SCAN`인지, 태그 이름과 시간 조건이 `KEY RANGE`에 있는지를 함께 확인합니다.

#### 작은 테이블이 왜 먼저 실행되지 않았나?

행 수만으로 정하지 않기 때문입니다. 큰 테이블을 한 번 읽고 작은 테이블의 key 인덱스를
반복 검색하는 계획이 반대 방향의 반복 full 스캔보다 나을 수 있습니다.

#### FROM 절의 순서를 바꾸면 계획을 강제할 수 있나?

아닙니다. JOIN 컬럼에 적절한 인덱스를 만들고 직접 컬럼 비교와 호환되는 타입을 사용한
뒤 `EXPLAIN`으로 확인합니다.

#### 인덱스 스캔인데 필터도 표시되는 이유는 무엇인가?

인덱스가 후보를 줄인 뒤 원래 SQL 조건을 최종 확인하기 때문입니다. 정확성을 위한 정상
계획일 수 있습니다.

#### FULL 스캔은 항상 나쁜가?

아닙니다. 한 번만 읽는 outer 스캔, 작은 테이블 또는 안전하지 않은 인덱스 변환을 피하기
위한 스캔은 정상일 수 있습니다. 큰 inner 테이블에서 반복되는지를 확인합니다.

#### EXPLAIN과 EXPLAIN FULL은 언제 구분해 쓰나?

먼저 `EXPLAIN`으로 접근 순서와 인덱스를 확인합니다. 같은 데이터에서 두 SQL의 실제
내부 작업량을 비교해야 할 때 제한된 환경에서 `EXPLAIN FULL`을 사용합니다.

#### 버전 업그레이드 후 계획 순서가 달라도 괜찮나?

계획 개선으로 스캔 순서와 결과 반환 순서는 달라질 수 있습니다. SQL 의미는 같아야 하므로
결과 행 수와 주요 값을 먼저 비교하고, 출력 순서가 필요하면 `ORDER BY`를 사용합니다.

#### optimizer hint를 사용할 수 있나?

`INDEX`, `NO_INDEX`, `FULL`, `PARALLEL` 등 일부 스캔·인덱스 관련 hint를 지원합니다.
일반적인 JOIN 순서나 JOIN 알고리즘을 직접 고정하는 hint는 제공하지 않습니다. hint를
사용하더라도 버전과 데이터가 달라진 뒤 결과와 계획을 다시 검증합니다.

### SQL 작성 체크리스트

- 태그 조회는 `TIME` 범위를 명시하고, 대상 태그를 알면 `NAME` 조건도 함께 제공합니다.
- JOIN key를 가능하면 함수나 산술식 없이 직접 컬럼 비교로 작성합니다.
- 자주 사용하는 복합 JOIN key는 동등 조건 컬럼을 인덱스 선두에 배치합니다.
- 복합 UNIQUE 단일 key 검색을 기대하면 모든 key 컬럼에 동등 조건을 제공합니다.
- 큰 테이블이 inner `FULL SCAN`으로 반복되지 않는지 확인합니다.
- 양쪽 JOIN 컬럼의 타입, 정수 범위와 문자열 길이를 맞춥니다.
- 인덱스 스캔에 `FILTER`가 함께 있어도 즉시 오류로 판단하지 않습니다.
- 결과 순서가 중요하면 반드시 `ORDER BY`를 사용합니다.
- SQL이나 인덱스를 변경한 뒤 성능보다 먼저 결과 행 수와 주요 값이 같은지 확인합니다.
- `EXPLAIN FULL`은 같은 데이터와 세션 조건에서 상대 비교합니다.

### 예제 정리 SQL

의존하는 VIEW를 먼저 삭제한 뒤 테이블을 삭제합니다.

```sql
DROP VIEW OPT_ACTIVE_EVENT;
DROP TABLE OPT_SENSOR_WINDOW;
DROP TABLE OPT_SENSOR;
DROP TABLE OPT_EXPECTED;
DROP TABLE OPT_POSITION;
DROP TABLE OPT_TEXT;
DROP TABLE OPT_SHORT_KEY;
DROP TABLE OPT_LONG_KEY;
DROP TABLE OPT_REQUEST;
DROP TABLE OPT_ACCOUNT;
DROP TABLE OPT_STATE;
DROP TABLE OPT_EVENT;
DROP TABLE OPT_CODE;
```

### 범위와 제한

- 이 문서는 Standard Edition의 SELECT/JOIN 계획을 기준으로 합니다.
- Cluster Edition의 분산 JOIN 계획과 제약은 이 문서의 범위가 아닙니다.
- 일반적인 histogram, NDV와 같은 통계 기반 cost 정보는 사용하지 않습니다.
- 일부 스캔·인덱스 hint는 지원하지만 일반적인 JOIN 순서·알고리즘 hint는 제공하지 않습니다.
- 데이터 상태와 optimizer 개선에 따라 실행 계획은 달라질 수 있습니다. 계획을 비교할 때
  성능뿐 아니라 결과 행 수와 주요 결과값도 함께 확인합니다.
- 계획을 자동 검사할 때는 내부 ID나 전체 문자열보다 스캔 종류, 테이블 이름과
  `KEY RANGE`처럼 의미가 안정적인 항목을 사용합니다.

<a id="performance-cte"></a>

## CTE 성능 고려사항

Standard Edition의 CTE는 각 참조를 인라인 뷰 형태로 전개하여 계획합니다. CTE 결과가 임시
테이블에 구체화되거나 한 번만 평가된다고 보장하지 않습니다. 같은 CTE를 여러 번 참조하면
원본 테이블의 스캔, 집계 또는 JOIN이 참조마다 실행될 수 있습니다.

```sql
WITH recent_data AS (
    SELECT device_id, time, value
    FROM sensor_data
    WHERE time >= NOW - 1h
      AND device_id IN ('device-01', 'device-02')
)
SELECT a.device_id, a.value, b.value
FROM recent_data a
JOIN recent_data b
  ON a.device_id = b.device_id
 AND a.time = b.time;
```

다음 기준으로 CTE 쿼리를 튜닝합니다.

- 시간 범위, TAG 이름과 키 조건을 CTE 본문에 가능한 한 일찍 적용합니다.
- 대량 테이블을 읽거나 비용이 큰 집계를 수행하는 CTE는 반복 참조를 피합니다.
- 반복 사용이 필요하면 실제 테이블이나 VIEW로 분리하는 방안을 검토합니다.
- `EXPLAIN`, `EXPLAIN FULL`, `EXPLAIN TRACE`로 전개된 각 참조의 계획을 확인합니다.
- 전개된 `SELECT` 단위가 1,024개를 넘지 않도록 긴 연쇄 참조와 다중 참조를 줄입니다.

`MATERIALIZED`와 `NOT MATERIALIZED`는 지원하지 않습니다. 자세한 문법과 제한은
[WITH / CTE syntax](/dbms/reference/sql/syntax-dictionary-sql/cte-syntax/)를 참고하십시오.

<a id="performance-operators-tuning"></a>

## 검색 연산자 성능 튜닝

WHERE 절에서 어떤 연산자를 사용하느냐에 따라 인덱스 활용 여부가 결정됩니다.

### 인덱스 사용 가능 연산자

다음 연산자는 BITMAP 또는 LSM 인덱스를 활용해 스캔 범위를 줄입니다.

| 연산자 | 설명 | 예시 |
|--------|------|------|
| `=` | 동등 비교 | `severity = 'ERROR'` |
| `<` | 미만 | `value < 100.0` |
| `<=` | 이하 | `value <= 100.0` |
| `>` | 초과 | `value > 50.0` |
| `>=` | 이상 | `value >= 50.0` |
| `BETWEEN` | 범위 | `value BETWEEN 10.0 AND 90.0` |
| 전방 LIKE | 접두어 일치 | `host LIKE 'server%'` |

```sql
-- 인덱스 활용: BETWEEN (내부적으로 >= AND <= 로 처리)
EXPLAIN SELECT * FROM machine_log
WHERE  response_code BETWEEN 400 AND 499
  AND  _arrival_time >= '2025-06-01' AND _arrival_time < '2025-06-02';

PLAN
------------------------------------------------------------------------------------
 PROJECT
  INDEX SCAN
   *BITMAP RANGE (table id:3, column id:4, index id:5)
   [KEY RANGE]
    * response_code >= 400
    * response_code <= 499
   [FILTER]
    * _arrival_time >= '2025-06-01 00:00:00'
    * _arrival_time < '2025-06-02 00:00:00'
```

### 인덱스 사용 불가 연산자

다음 패턴은 인덱스를 사용하지 못해 FULL SCAN이 발생합니다.

#### 중간/후방 LIKE

와일드카드가 앞에 오는 LIKE 패턴은 인덱스를 사용할 수 없습니다.

```sql
-- 인덱스 미사용: '%xxx%' 또는 '%xxx' 패턴
SELECT * FROM machine_log WHERE message LIKE '%timeout%';  -- FULL SCAN

-- 인덱스 사용 가능: 전방 LIKE (접두어 일치)
SELECT * FROM machine_log WHERE host LIKE 'server%';       -- INDEX SCAN
```

#### 컬럼에 함수 적용

WHERE 절에서 컬럼을 함수로 감싸면 옵티마이저가 인덱스를 사용하지 못합니다.

```sql
-- 인덱스 미사용: 함수 내부 컬럼
SELECT * FROM system_log WHERE UPPER(severity) = 'ERROR';   -- FULL SCAN
SELECT * FROM system_log WHERE LENGTH(message) > 100;       -- FULL SCAN

-- 권장: 비교 값을 변환
SELECT * FROM system_log WHERE severity = 'ERROR';           -- INDEX SCAN
```

#### OR 조건과 인덱스 결합

OR 조건에서 하나라도 인덱스가 없는 컬럼이 포함되면 전체 FULL SCAN으로 전환될 수 있습니다.

```sql
-- 인덱스 있는 컬럼끼리 OR: INDEX(OR) 사용
EXPLAIN SELECT * FROM machine_log WHERE code = 400 OR code = 500;

PLAN
------------------------------------------------------------------------------------
 PROJECT
  INDEX SCAN
   INDEX (OR)
    *BITMAP RANGE (table id:3, column id:4, index id:5)
    *BITMAP RANGE (table id:3, column id:4, index id:5)
   [KEY RANGE]
    * code = 400 or code = 500

-- 인덱스 없는 컬럼이 OR에 포함: FULL SCAN 전환
SELECT * FROM machine_log WHERE code = 400 OR message = 'ok'; -- FULL SCAN
```

OR 조건 대신 UNION ALL로 분리하면 각 쿼리에서 INDEX SCAN을 활용할 수 있습니다.

```sql
-- UNION ALL로 분리 (각각 INDEX SCAN 적용)
SELECT * FROM machine_log WHERE code = 400
UNION ALL
SELECT * FROM machine_log WHERE code = 500;
```

### BITMAP 인덱스 효과 (LOG 테이블)

LOG 테이블에서 기본으로 생성되는 BITMAP 인덱스는 카디널리티(서로 다른 값의 수)가 낮은 컬럼에 특히 효과적입니다.

| 컬럼 특성 | BITMAP 인덱스 효과 |
|-----------|-------------------|
| 카디널리티 낮음 (예: severity, status_code) | 매우 효과적 — 값당 비트 벡터로 빠른 RID 계산 |
| 카디널리티 높음 (예: session_id, message) | 효과 제한적 — 비트 벡터 밀도가 높아 이점 감소 |

```sql
-- 카디널리티 낮은 컬럼 (severity: ERROR/WARN/INFO) → BITMAP 효과적
CREATE INDEX idx_severity ON machine_log (severity);

-- 복합 조건에서 BITMAP 인덱스 AND 연산
EXPLAIN SELECT * FROM machine_log
WHERE  severity = 'ERROR' AND response_code = 500;

PLAN
------------------------------------------------------------------------------------
 PROJECT
  INDEX SCAN
   *BITMAP RANGE (table id:3, column id:2, index id:4)  -- severity 인덱스
   *BITMAP RANGE (table id:3, column id:5, index id:6)  -- response_code 인덱스
   [KEY RANGE]
    * severity = 'ERROR'
    * response_code = 500
```

두 인덱스의 비트 벡터를 AND 연산해 교집합 RID만 읽으므로 단일 인덱스보다 빠릅니다.

### LSM vs BITMAP 인덱스 선택 기준

LOG 테이블에는 두 가지 인덱스 유형을 사용할 수 있습니다.

| 구분 | LSM 인덱스 | BITMAP 인덱스 |
|------|-----------|--------------|
| 구조 | 정렬된 키 목록 | 값별 비트 벡터 |
| 적합 대상 | 숫자형, 날짜형, 고카디널리티 컬럼 | 문자열, 저카디널리티 컬럼 |
| 범위 검색 | 우수 | 보통 |
| 동등 검색 | 우수 | 우수 |
| 복합 AND | 제한적 | 비트 AND 연산으로 매우 빠름 |
| 생성 구문 | `CREATE INDEX ... INDEX_TYPE LSM` | `CREATE BITMAP INDEX ...` 또는 `CREATE INDEX ... INDEX_TYPE BITMAP` |

```sql
-- BITMAP 인덱스 생성 (문자열·저카디널리티 컬럼에 적합)
CREATE BITMAP INDEX idx_severity ON machine_log (severity);

-- LSM 인덱스 생성 (숫자형 범위 검색에 적합)
CREATE INDEX idx_ts ON machine_log (event_time) INDEX_TYPE LSM;
```

**선택 기준 요약:**
- 값의 종류가 수십~수백 개 이하(저카디널리티): BITMAP
- 숫자·날짜 컬럼의 범위 검색: LSM
- 복합 AND 조건으로 여러 컬럼 동시 필터링: BITMAP 조합이 효과적

### IP 타입 BETWEEN 조회 성능

IP 타입 컬럼은 내부적으로 정수로 저장되므로, BETWEEN 조건에서 인덱스 범위 검색이 효율적으로 동작합니다.

```sql
-- IP 범위 조회: BETWEEN으로 서브넷 필터링
SELECT _arrival_time, src_ip, dst_ip, bytes
FROM   network_log
WHERE  src_ip BETWEEN '192.168.1.0' AND '192.168.1.255'
  AND  _arrival_time >= '2025-06-01' AND _arrival_time < '2025-06-02';
```

IP 컬럼에 인덱스를 생성하면 BETWEEN 조건에 대해 INDEX SCAN이 적용됩니다.

```sql
CREATE INDEX idx_src_ip ON network_log (src_ip);
```

### 특정 인덱스 비활성화

옵티마이저가 선택한 인덱스보다 다른 인덱스가 더 효율적일 때 `NO_INDEX` 힌트로 특정 인덱스를 제외할 수 있습니다.

```sql
-- idx_code 인덱스를 제외하고 idx_severity 인덱스만 사용
SELECT /*+ NO_INDEX(machine_log, idx_code) */ *
FROM   machine_log
WHERE  code = 400 AND severity = 'ERROR';

PLAN
------------------------------------------------------------------------------------
 PROJECT
  INDEX SCAN
   *BITMAP RANGE (table id:3, column id:2, index id:4)  -- severity 인덱스만 사용
   [KEY RANGE]
    * severity = 'ERROR'
   [FILTER]
    * code = 400
```

### 요약: 연산자별 인덱스 활용 가능 여부

| 패턴 | 인덱스 활용 |
|------|-------------|
| `col = value` | O |
| `col < value`, `col <= value` | O |
| `col > value`, `col >= value` | O |
| `col BETWEEN v1 AND v2` | O |
| `col LIKE 'prefix%'` | O (전방 LIKE) |
| `col LIKE '%suffix'` | X |
| `col LIKE '%middle%'` | X |
| `FUNC(col) = value` | X |
| `col1 = v1 OR col2 = v2` (col2 인덱스 없음) | X (FULL SCAN) |
| `col1 = v1 OR col1 = v2` (같은 컬럼) | O (INDEX OR) |

<a id="performance-window-functions-considerations-pivot"></a>

## 윈도우 함수와 PIVOT 성능 고려사항

윈도우 함수와 PIVOT은 강력한 분석 도구이지만, 처리 방식에 따라 메모리와 응답 시간에 큰 영향을 줄 수 있습니다. 대용량 데이터 환경에서 안전하게 사용하려면 몇 가지 주의가 필요합니다.

### 윈도우 함수 성능 고려사항

#### 전체 결과셋 메모리 적재

윈도우 함수(`ROW_NUMBER`, `RANK`, `LAG`, `LEAD`, `SUM OVER` 등)는 정렬·분할할 결과가 많을수록
메모리 사용량과 응답 시간이 증가할 수 있습니다.

```sql
-- 주의: 넓은 시간 범위에 직접 윈도우 함수를 적용하면 메모리 사용량이 증가합니다
SELECT name, time, value,
       LAG(value, 1) OVER (PARTITION BY name ORDER BY time) AS prev_value
FROM   sensor_tag
WHERE  time BETWEEN '2025-01-01' AND '2025-06-30';  -- 6개월 전체 데이터
```

`MAX_QPX_MEM` 프로퍼티로 단일 쿼리의 메모리 상한을 설정해 시스템 전체 영향을 제한할 수 있습니다. 표준 샘플 설정의 기본값은 1073741824 bytes(1 GB)입니다.

```
# machbase.conf
MAX_QPX_MEM = 2147483648   # 2 GB
```

#### 서브쿼리로 결과셋을 줄인 후 윈도우 함수 적용

윈도우 함수를 적용하기 전에 서브쿼리에서 집계 또는 범위 제한을 수행해 처리 대상 행 수를 줄입니다.

```sql
-- 권장: 서브쿼리에서 1시간 단위로 집계 후 윈도우 함수 적용
SELECT name, bucket,
       avg_val,
       LAG(avg_val, 1) OVER (PARTITION BY name ORDER BY bucket) AS prev_avg,
       avg_val - LAG(avg_val, 1) OVER (PARTITION BY name ORDER BY bucket) AS delta
FROM (
    -- 서브쿼리에서 대용량 → 소용량으로 집계
    SELECT name,
           rollup('hour', 1, time) AS bucket,
           AVG(value)              AS avg_val
    FROM   sensor_tag
    WHERE  time BETWEEN '2025-01-01' AND '2025-06-30'
    GROUP BY name, bucket
) t
ORDER BY name, bucket;
```

서브쿼리에서 집계·필터링한 뒤 윈도우 함수를 적용하면 처리할 결과 수를 줄일 수 있습니다.

#### 윈도우 함수 적용 전 필터링

윈도우 함수는 정렬과 파티션별 상태를 유지해야 하므로 입력 행 수가 성능에 직접 영향을 줍니다. `PARTITION BY` 자체가 특별한 인덱스 최적화를 보장하는 것은 아니므로, 인덱스가 있는 컬럼과 시간 범위 조건으로 대상 행을 먼저 줄인 뒤 윈도우 함수를 적용합니다.

```sql
-- TAG 테이블: name/time 조건으로 대상 행을 줄인 뒤 윈도우 함수 적용
SELECT name, time, value,
       ROW_NUMBER() OVER (PARTITION BY name ORDER BY time) AS rn
FROM   sensor_tag
WHERE  name IN ('TEMP-01', 'TEMP-02')
  AND  time BETWEEN '2025-06-01' AND '2025-06-02';
```

### PIVOT 성능 고려사항

#### IN 목록 값 수와 컬럼 수

PIVOT의 IN 목록에 포함된 값 수만큼 결과 컬럼이 생성됩니다. 값 수가 많을수록 와이드 테이블이 되어 메모리 사용량과 처리 시간이 증가합니다.

```sql
-- 주의: IN 목록이 길면 결과 컬럼 수가 많아져 성능 저하
SELECT *
FROM (
    SELECT bucket, name, avg_val FROM agg_result
)
PIVOT (
    AVG(avg_val)
    FOR name IN (
        'SENSOR-001', 'SENSOR-002', 'SENSOR-003', ..., 'SENSOR-200'  -- 200개 컬럼
    )
);
```

**권장 사항:**
- IN 목록은 실제로 필요한 태그/값으로만 제한합니다. 불필요한 항목은 제거합니다.
- 태그 수가 수십 개를 초과하는 경우 PIVOT 대신 애플리케이션에서 행렬 변환을 수행하는 것을 검토합니다.

#### 서브쿼리로 집계 후 PIVOT 적용

원시 데이터에 직접 PIVOT을 적용하면 처리 대상 행과 결과 컬럼 수가 커질 수 있습니다. 먼저 일반 집계 서브쿼리나 별도 집계 테이블로 대상 행 수를 줄인 뒤 PIVOT을 적용하면 메모리 사용량을 줄일 수 있습니다.

```sql
-- 권장: 서브쿼리에서 집계 후 PIVOT
SELECT *
FROM (
    SELECT DATE_TRUNC('hour', time) AS bucket,
           name,
           AVG(value)              AS avg_val
    FROM   sensor_tag
    WHERE  name IN ('TEMP-01', 'TEMP-02', 'PRESS-01')
      AND  time BETWEEN '2025-06-01' AND '2025-06-02'
    GROUP BY bucket, name
)
PIVOT (
    AVG(avg_val)
    FOR name IN ('TEMP-01', 'TEMP-02', 'PRESS-01')
)
ORDER BY bucket;
```

이 빌드에서는 `rollup(...)`을 사용하는 ROLLUP 쿼리 위에 바로 PIVOT을 적용할 수 없습니다. ROLLUP 결과를 행렬 형태로 바꾸려면 애플리케이션에서 변환하거나, 필요한 집계 결과를 일반 테이블에 적재한 뒤 그 테이블을 PIVOT 입력으로 사용합니다.

#### PIVOT과 사전 집계 테이블 조합

반복 조회가 많은 경우에는 집계 결과를 별도 테이블에 저장한 뒤 PIVOT 입력으로 사용할 수 있습니다.

```sql
-- 일반 집계 테이블을 PIVOT 입력으로 사용
SELECT *
FROM (
    SELECT bucket,
           name,
           avg_val
    FROM   sensor_hourly_agg
    WHERE  name IN ('TEMP-01', 'TEMP-02')
      AND  bucket BETWEEN '2025-06-01 00:00:00' AND '2025-06-01 06:00:00'
)
PIVOT (
    AVG(avg_val)
    FOR name IN ('TEMP-01', 'TEMP-02')
)
ORDER BY bucket;
```

### 요약: 패턴별 권장 접근법

| 상황 | 권장 접근법 |
|------|-------------|
| 넓은 범위에 윈도우 함수 적용 | 서브쿼리에서 집계·필터링 후 윈도우 함수 적용 |
| PIVOT IN 목록이 수십 개 초과 | 필요한 항목만 선택, 또는 애플리케이션에서 처리 |
| 윈도우 함수 + 대용량 기간 | ROLLUP 또는 일반 집계로 입력 행 수를 줄인 뒤 적용 |
| 메모리 부족 오류 | `MAX_QPX_MEM` 설정 검토, 기간 범위 축소 |
