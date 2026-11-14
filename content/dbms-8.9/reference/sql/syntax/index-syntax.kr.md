---
type: docs
title: 'INDEX'
weight: 150
toc: true
---

인덱스 문법과 테이블 타입별 지원 범위를 설명합니다. 인덱스는 조회 비용을 줄이는 대신
입력과 변경 때 유지 비용이 발생하므로 실제 조건과 실행 계획을 확인한 뒤 추가하십시오.

<a id="create-index"></a>

## CREATE INDEX

일반 인덱스 문법은 다음과 같습니다. DBMS 8.9의 검색 인덱스 옵션은
[TRANSACTION 검색 인덱스](#transaction-검색-인덱스)를 참고합니다.

```sql
create_index_stmt ::=
    'CREATE' index_modifier? 'INDEX' [ 'IF NOT EXISTS' ] index_name
    'ON' index_target '(' index_column_list ')'
    [ 'INDEX_TYPE' ( 'LSM' | 'KEYWORD' | 'BITMAP' | 'REDBLACK' | 'TAG' ) ]
    [ 'TABLESPACE' tablespace_name ]
    [ index_property_list ]

index_modifier ::= 'UNIQUE' | 'PRIMARY KEY'

index_target ::= table_name | table_name 'METADATA'

index_column_list ::=
    column_name ( ',' column_name )*
  | column_name json_path

index_property_list ::=
    ( 'MAX_LEVEL'        '=' number
    | 'PAGE_SIZE'        '=' number
    | 'BITMAP_ENCODE'    '=' ( 'EQUAL' | 'RANGE' )
    | 'PART_VALUE_COUNT' '=' number )
    ( ',' index_property_list )*
```

<a id="create-index-if-not-exists"></a>

### IF NOT EXISTS

`IF NOT EXISTS`를 지정하면 같은 database와 owner에 동일한 index name이 있을 때 오류 없이
성공하고 기존 index를 유지합니다.

- 동일한 이름이 없으면 table, column, index type, property와 권한을 기존 CREATE INDEX와
  동일하게 검증한 뒤 생성합니다.
- 동일한 이름이 있으면 table, column, index type, JSON path와 property를 비교하거나
  변경하지 않습니다.
- 중복 판정 namespace는 `database + owner + index name`입니다. 다른 database나 owner의 같은
  이름은 별도 index입니다.
- 옵션을 생략한 CREATE INDEX는 기존 duplicate-name 오류를 그대로 반환합니다.

{{< callout type="warning" >}}
`IF NOT EXISTS`는 index 정의를 일치시키는 기능이 아닙니다. 같은 이름이 있으면 statement의
target table이나 column이 없거나 정의가 달라도 no-op으로 성공합니다. 반복 배포 뒤에는
`SHOW INDEX` 또는 system catalog에서 실제 table, column, type과 property를 확인하십시오.
{{< /callout >}}

```sql
CREATE LOG TABLE sensor_log_ifne (
    sensor_id INTEGER,
    value     DOUBLE
);

CREATE INDEX IF NOT EXISTS sensor_log_ifne_idx
    ON sensor_log_ifne(sensor_id);

-- 같은 이름이 있으므로 성공하고 기존 SENSOR_ID mapping을 유지합니다.
CREATE INDEX IF NOT EXISTS sensor_log_ifne_idx
    ON sensor_log_ifne(value);

SHOW INDEX sensor_log_ifne_idx;

DROP TABLE sensor_log_ifne;
```

### 조건부 생성 지원 형태

| 형식 | 지원 범위 |
|---|---|
| 일반 `CREATE INDEX IF NOT EXISTS` | 해당 table type에서 지원하는 일반 index |
| `CREATE UNIQUE INDEX IF NOT EXISTS` | Standard Edition TRANSACTION table |
| `CREATE PRIMARY KEY INDEX IF NOT EXISTS` | Standard Edition TRANSACTION table |
| TAG data JSON path / TAG METADATA index | Standard Edition, Cluster Edition |
| 일반 문법의 `INDEX_TYPE` 절 | 해당 table type과 index type의 기존 지원 범위 |

deprecated `CREATE BITMAP INDEX`, `CREATE KEYWORD INDEX`, `CREATE REDBLACK INDEX` 전용 문법에는
`IF NOT EXISTS`를 사용할 수 없습니다. 일반 문법을 사용합니다.

```sql
CREATE INDEX IF NOT EXISTS idx_message
    ON app_log(message) INDEX_TYPE KEYWORD;
```

## 테이블 타입별 지원 범위

| 테이블 타입 | 인덱스 | 주요 용도 |
|------------|--------|-----------|
| LOG | LSM, KEYWORD, BITMAP | 범위 조회, 텍스트 검색, 분석 조건 |
| TAG | TAG/KV secondary, JSON path | 값 컬럼과 JSON member 조건 |
| TAG METADATA | 자동 컬럼 인덱스, JSON path | 태그 속성 조건 |
| TRANSACTION | PRIMARY KEY, UNIQUE, BTREE, BM25, HNSW, IVF | 관계형 키·복합 조건과 텍스트·벡터 검색 |
| VOLATILE | REDBLACK | 메모리 테이블의 키·조건 조회 |
| LOOKUP | REDBLACK | 메모리 테이블의 키·조건 조회 |

타입을 생략했을 때 적용되는 내부 인덱스는 테이블 타입에 따라 다릅니다. 다른 테이블 타입의
인덱스 이름을 지정해도 같은 구조가 생성된다고 가정하지 마십시오.

## LOG 인덱스

```sql
CREATE INDEX idx_ts ON sensor_log (ts);
CREATE INDEX idx_msg ON app_log (message) INDEX_TYPE KEYWORD;
CREATE INDEX idx_status ON sensor_log (status)
    INDEX_TYPE BITMAP BITMAP_ENCODE = RANGE;
```

| 타입 | 대상과 특징 |
|------|-------------|
| LSM | LOG의 기본 범위 인덱스 |
| KEYWORD | VARCHAR/TEXT의 `SEARCH`, `ESEARCH` |
| BITMAP | 반복 값 분석. VARCHAR, TEXT, BINARY에는 사용하지 않음 |

LSM의 `MAX_LEVEL`, `PAGE_SIZE`, BITMAP의 `BITMAP_ENCODE` 같은 속성은 데이터 분포와
조회 조건으로 측정해 결정하십시오.

## TAG 인덱스

TAG 이름과 시간 축의 기본 접근 구조는 자동으로 관리됩니다. 값 컬럼을 단독 조건으로 자주
사용할 때 TAG/KV secondary index를 검토합니다.

```sql
CREATE INDEX idx_value ON sensor_tag (value) INDEX_TYPE TAG;
```

JSON 값 컬럼은 path별 인덱스를 만들 수 있습니다.

```sql
CREATE INDEX idx_sensor ON tag_json (value.sensor.name);
CREATE INDEX idx_metric ON tag_json (value->'$.metric');
CREATE INDEX idx_item ON tag_json (value.items[0]."product-id");
```

TAG METADATA 일반 컬럼에는 인덱스가 자동 생성됩니다. METADATA JSON 컬럼의 path를
추가할 때는 다음 형식을 사용합니다.

```sql
CREATE INDEX idx_ship_owner
ON ships METADATA (info->'$.owner');
```

지원 범위와 실행 계획 예시는
[TAG 인덱스와 성능](/dbms-8.9/tag-table-usage/index-performance/)을 참고하십시오.

## TRANSACTION 인덱스

TRANSACTION은 PRIMARY KEY, UNIQUE INDEX와 일반 단일·복합 인덱스를 지원합니다.

```sql
CREATE PRIMARY KEY INDEX idx_pk_order ON orders (order_id);
CREATE UNIQUE INDEX uidx_account_email ON account (email);
CREATE UNIQUE INDEX uidx_tenant_login ON account (tenant_id, login_name);
CREATE INDEX idx_category_name ON product (category, product_name);
```

PRIMARY KEY는 테이블당 하나이며 단일 컬럼입니다. `CREATE UNIQUE INDEX`는 복합 컬럼을
지원하고, NULL이 포함된 키는 다른 NULL 포함 키와 중복으로 판정하지 않습니다. 상세 동작은
[TRANSACTION 인덱스와 성능](/dbms-8.9/rdb-table-usage/index-performance/)을 참고하십시오.

## VOLATILE과 LOOKUP 인덱스

VOLATILE과 LOOKUP은 REDBLACK 메모리 인덱스를 사용합니다.

```sql
CREATE INDEX idx_status ON device_status (status) INDEX_TYPE REDBLACK;
```

타입별 기본 키와 추가 인덱스 설계는 다음 문서를 참고하십시오.

- [VOLATILE 인덱스와 성능](/dbms-8.9/volatile-table-usage/index-performance/)
- [LOOKUP 인덱스와 성능](/dbms-8.9/lookup-table-usage/index-performance/)

<a id="drop-index"></a>

## DROP INDEX

```sql
drop_index_stmt ::= 'DROP INDEX' index_name
```

```sql
DROP INDEX idx_status;
```

대상 인덱스를 사용하는 세션이 있으면 삭제가 실패할 수 있습니다. 삭제 전 실행 계획과
해당 인덱스를 사용하는 운영 쿼리를 확인하십시오.

## 관련 문서

- [SEARCH / ESEARCH / REGEXP](../search-esearch-regexp-syntax/)
- [쿼리 성능 튜닝](/dbms-8.9/performance-tuning/performance-query-tuning/)

## TRANSACTION 검색 인덱스

Standard Edition의 TRANSACTION 테이블에 다음 검색 인덱스를 생성합니다.
BM25는 텍스트 컬럼, HNSW와 IVF는 VECTOR 컬럼을 대상으로 합니다.
각 구문에서 대괄호는 선택 항목이며 실제 SQL에는 입력하지 않습니다.

```text
CREATE INDEX [IF NOT EXISTS] index_name ON table_name(text_column)
 INDEX_TYPE BM25 ANALYZER=analyzer;

CREATE INDEX [IF NOT EXISTS] index_name ON table_name(vector_column)
 INDEX_TYPE HNSW [hnsw_property [,hnsw_property] ...];

hnsw_property ::= DISTANCE=COSINE|L2|INNER_PRODUCT
 | M=integer | EF_CONSTRUCTION=integer | EF_SEARCH=integer
 | STORAGE_PRECISION=FLOAT32|FLOAT16

CREATE INDEX [IF NOT EXISTS] index_name ON table_name(vector_column)
 INDEX_TYPE IVF [ivf_property [,ivf_property] ...];

ivf_property ::= DISTANCE=COSINE|L2|INNER_PRODUCT | LISTS=integer | PROBES=integer
```

| 옵션 | 기본값과 허용 범위 | 의미 |
|---|---|---|
| ANALYZER | `CJK_EN` 또는 `KO_EN`을 지정 | 텍스트 분석기 |
| DISTANCE | COSINE | 벡터 검색 거리. 질의의 METRIC과 맞춥니다. |
| M | 16, 2~64 | HNSW 이웃 연결 수 |
| EF_CONSTRUCTION | 200, M~4096 | HNSW 구축 후보 폭 |
| EF_SEARCH | 100, 1~10000 | HNSW 검색 후보 폭 |
| STORAGE_PRECISION | FLOAT32 또는 FLOAT16, 기본 FLOAT32 | HNSW 인덱스 표현. 원본 VECTOR는 FLOAT32입니다. |
| LISTS | 자동 선택 | IVF 목록 수. 자동값은 `min(1024,ceil(sqrt(벡터 행 수)))`에서 메모리 예산에 맞춰 정합니다. |
| PROBES | `min(32,실제 LISTS)`, 1~실제 LISTS | IVF 검색에서 탐색할 목록 수 |

명시한 LISTS를 자원이 부족하다는 이유로 자동 축소하지 않습니다.
BM25는 키워드 검색과 Hybrid 검색의 텍스트 분기에 사용합니다. HNSW·IVF는 근사 검색
인덱스이며, MODE AUTO가 항상 근사 경로를 선택한다는 뜻은 아닙니다.

### 생성과 완료 확인

```sql
CREATE INDEX M89_DOCS_TEXT ON M89_DOCS(BODY)
 INDEX_TYPE BM25 ANALYZER='CJK_EN';
ALTER INDEX M89_DOCS_TEXT WAIT TIMEOUT 120;
CREATE INDEX M89_DOCS_VECTOR ON M89_DOCS(V)
 INDEX_TYPE IVF DISTANCE=COSINE,LISTS=2,PROBES=2;
ALTER INDEX M89_DOCS_VECTOR WAIT TIMEOUT 120;
```

이 예제의 M89_DOCS는 [첫 검색 실습](/kr/dbms-8.9/ai-search-graphrag/getting-started/)의
테이블입니다. 이미 같은 이름의 인덱스가 있으면 생성 명령을 반복하지 않습니다.
CREATE의 성공은 구축 완료와 다릅니다. WAIT와 상태 뷰에서 READY를 확인합니다.
`IF NOT EXISTS`는 기존 이름의 정의를 유지하므로 요청한 거리나 옵션으로 바뀌지 않습니다.

### 변경과 재구축

```text
ALTER INDEX index_name WAIT [TIMEOUT seconds];
ALTER INDEX index_name REBUILD;
ALTER INDEX index_name SET PROBES=integer;
```

WAIT의 기본 시간은 60초입니다. TIMEOUT 0은 즉시 상태를 확인합니다.
대기 시간 초과가 구축 취소를 의미하지는 않습니다. REBUILD는 재구축을 접수하므로
완료 여부는 WAIT와 상태 뷰에서 다시 확인합니다.

IVF의 PROBES 변경은 재구축 없이 적용합니다. LISTS, 분석기, 거리와 HNSW의 고정 옵션을
변경하려면 인덱스를 재생성합니다. HNSW의 M·EF 옵션을 ALTER SET으로 변경하지 않습니다.
재생성 중에는 해당 인덱스의 사용 가능 여부와 서비스 영향을 확인합니다.

- [검색 인덱스 상태 뷰](/kr/dbms-8.9/reference/system-catalog/search-indexes/)
- [검색 문법](../search-syntax/)
- [운영과 성능 관리](/kr/dbms-8.9/ai-search-graphrag/operations/)
