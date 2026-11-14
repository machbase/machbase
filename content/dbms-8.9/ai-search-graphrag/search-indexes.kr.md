---
type: docs
title: '11.2 검색 방식과 인덱스 선택'
weight: 20
toc: true
---

첫 검색 실습을 마친 뒤 검색 방식과 인덱스를 선택합니다. 의미 검색은 가까운 벡터를, BM25는 키워드 관련도를 이용하며 Hybrid 검색은 두 결과를 결합합니다.

아래 `[ ]`는 선택 항목 표시이며 실제 SQL에는 입력하지 않습니다.

```text
TEXT_SEARCH(TABLE table [AS alias],TEXT column,QUERY_TEXT expression,TOP_K integer
 [,FILTER(predicate)] [,RESULT_PREFIX 'prefix'])

VECTOR_SEARCH(TABLE table [AS alias],VECTOR column,QUERY_VECTOR expression,TOP_K integer
 [,SPACE 'space'] [,METRIC COSINE|L2|INNER_PRODUCT] [,MODE AUTO|EXACT]
 [,FILTER(predicate)] [,RESULT_PREFIX 'prefix'])

HYBRID_SEARCH(TABLE table [AS alias],VECTOR column,TEXT column,TOP_K integer
 [,QUERY_VECTOR expression] [,QUERY_TEXT expression] [,SPACE 'space']
 [,METRIC COSINE|L2|INNER_PRODUCT] [,MODE AUTO|EXACT] [,VECTOR_WEIGHT number]
 [,VECTOR_CANDIDATES integer] [,TEXT_CANDIDATES integer]
 [,FILTER(predicate)] [,RESULT_PREFIX 'prefix'])
```

| 항목 | 사용 규칙 |
|---|---|
| TABLE·VECTOR·TEXT | 테이블/컬럼 식별자. 값 bind `?`로 테이블명을 바꾸지 않음 |
| QUERY_VECTOR | VECTOR 식, JSON 변환 식 또는 목표 타입이 알려진 native bind |
| QUERY_TEXT | 일반 문자열 식 또는 bind |
| TOP_K | 필수 정수, 1~1000. 값 bind 가능 |
| MODE | AUTO 기본, EXACT는 벡터 인덱스 없이 동작. Hybrid에서는 벡터 분기에 적용 |
| METRIC | COSINE 기본. 검색 옵션은 `METRIC COSINE`처럼 식별자로 씀 |
| SPACE | 컬럼에 EMBEDDING_SPACE가 선언됐으면 같은 문자열 literal 필수. 미선언 컬럼에는 생략 |
| FILTER | Top-K 후보 선정 전에 적용. 일반 SQL 조건과 상관 EXISTS 사용 가능 |
| RESULT_PREFIX | 기본 `__SEARCH_`. 원본 컬럼과 반환 이름 충돌 시 바꿈. 결과 이름은 대문자로 정규화 |
| VECTOR_WEIGHT | Hybrid 0~1, 기본0.5. 0은 텍스트만, 1은 벡터만 활성화 |
| VECTOR_CANDIDATES·TEXT_CANDIDATES | Hybrid 분기별 후보 상한. TOP_K 이상~10000, 기본 max(100,10×TOP_K) |

검색 함수는 FROM 절의 관계로 호출합니다. `SELECT VECTOR_SEARCH(...)` 같은 scalar 호출은 지원 문법이 아닙니다. 옵션은 중복하거나 알 수 없는 이름을 넣으면 오류입니다. 활성 텍스트 분기에는 준비된 BM25 인덱스가 필요합니다. 가중치0이면 QUERY_VECTOR를, 가중치1이면 QUERY_TEXT를 생략할 수 있지만 컬럼/SPACE 등 정적 검사는 유지됩니다.

반환 원본 행에 `__SEARCH_TEXT_SCORE`, `__SEARCH_VECTOR_DISTANCE`, Hybrid의 `__SEARCH_SCORE`가 추가됩니다. Hybrid의 한 분기에 없는 행은 해당 거리/텍스트 점수가 NULL일 수 있습니다. 최종 표시 순서는 ORDER BY로 지정하세요.

Hybrid는 거리와 BM25 점수를 단순 합산하지 않습니다. 각 분기의 rank를 다음 식으로 합칩니다.

```text
score = w/(60 + vector_rank) + (1-w)/(60 + text_rank)
```

없는 분기의 기여는 0이며, score가 클수록 앞입니다. 후보 수와 최종 TOP_K는 별개입니다. 예를 들어 분기100개씩을 결합해 최종5개를 반환할 수 있습니다.

### VECTOR 값과 거리

| 표현식 | 결과·규칙 |
|---|---|
| `TO_VECTOR(value,n)` | 숫자 JSON VARCHAR/TEXT/CLOB 또는 FLOAT ARRAY → VECTOR(n) |
| `VECTOR_DIM(v)` | 차원 INTEGER |
| `VECTOR_NORM(v)` | L2 norm DOUBLE |
| `VECTOR_NORMALIZE(v)` | 같은 차원의 단위 벡터. 영벡터는 오류 |
| `VECTOR_DISTANCE(a,b,'COSINE')` | 1−cosine similarity. 영벡터 거부 |
| `VECTOR_DISTANCE(a,b,'L2')` | 제곱하지 않은 Euclidean 거리 |
| `VECTOR_DISTANCE(a,b,'INNER_PRODUCT')` | 내적의 음수 |
| `VECTOR_TO_JSON(v)` | 숫자 JSON TEXT |
| `CAST(v AS FLOAT[n])` / `DOUBLE[n]` | 같은 차원의 SQL ARRAY. ARRAY 쪽 n<=1024 |

모든 거리에서 작은 값이 앞입니다. 거리 함수의 세 번째 인자는 `'L2'`처럼 문자열입니다. 입력 차원은 맞아야 하고 NaN/Infinity·잘못된 숫자 JSON·범위 초과를 거부합니다. JSON 또는 고정 VECTOR 컬럼의 짧은 입력은 뒤에0을 채우지만 차원 초과는 오류입니다. JSON의 NULL 요소는0으로 보정하며, 컬럼 전체 SQL NULL과 영벡터는 구분합니다. SDK의 요소 NULL 정책은 언어별로 다릅니다.

`TO_VECTOR`가 자동 정규화를 하지는 않습니다. 같은 모델·revision·전처리·정규화 정책을 문서와 질문에 적용하세요. SPACE는 이 계약에 붙이는 이름이며 모델 실행/검증 기능이 아닙니다. 같은1024차원이어도 서로 다른 모델의 벡터를 섞으면 의미 검색이 깨집니다.

VECTOR(4096)은 저장할 수 있어도 SQL DOUBLE[4096]으로 CAST할 수는 없습니다. 큰 벡터는 native SDK 결과 또는 `VECTOR_TO_JSON(V)`의 TEXT로 읽습니다. 함수의 전체 SQL NULL 입력은 해당 계약대로 NULL을 전파하며, 잘못된 타입을 허용한다는 뜻은 아닙니다.

## 권한과 업무 필터

`FILTER(TENANT=1)`은 후보 중 tenant1의 Top-K를 구합니다. 검색 바깥의 `WHERE R.TENANT=1`은 이미 뽑힌 Top-K를 나중에 줄이므로 결과와 건수가 다를 수 있습니다. 업무 권한은 애플리케이션이 검색 함수 안에 반영해야 합니다.

11.1절의 ACL 예제에서 `D`는 검색 대상 행의 별칭, `R`은 반환 관계의 별칭입니다. `FILTER` 안에서는 `D`를 사용합니다. 사용자/tenant 값은 인증된 세션의 업무 권한에서 얻고 bind하세요. 화면에서 받은 tenant 번호만 신뢰하는 API로 만들지 않습니다.

Python prepared cursor가 이미 있다면 다음처럼 문서 권한을 함께 bind할 수 있습니다. 먼저 `M89_ACL(USER_ID INTEGER,DOC_ID INTEGER)`와 해당 권한 행을 준비해야 합니다.

```python
query = """SELECT R.ID,R.BODY FROM VECTOR_SEARCH(TABLE M89_DOCS AS D,VECTOR D.V,
 QUERY_VECTOR TO_VECTOR(?,3),SPACE 'm89-numeric-v1',MODE EXACT,
 FILTER(D.TENANT=? AND EXISTS(SELECT 1 FROM M89_ACL A
 WHERE A.USER_ID=? AND A.DOC_ID=D.DOC_ID)),TOP_K ?) R
 ORDER BY R.__SEARCH_VECTOR_DISTANCE,R.ID"""
cur.execute(query, ['[1,0,0]', 1, 7, 3])
print(cur.fetchall())
```

간단한 tenant/범위 조건에 B-tree를 함께 두면 선행 필터 최적화에 도움이 됩니다. OR·함수식·상관 EXISTS 등이 있다고 SQL 자체가 미지원인 것은 아니지만, 단순 B-tree 선행 경로 대신 일반 FILTER 평가가 선택될 수 있습니다. ACL 중복으로 원본 청크를 복제하지 않으려면 단순 JOIN 대신 EXISTS가 적합한 경우가 있습니다.

현재 공개 함수는 TEXT_SEARCH·VECTOR_SEARCH·HYBRID_SEARCH입니다. 내부 후보 실행기 이름을 SQL `SEARCH_CANDIDATES` 함수로 호출하거나, `CANDIDATES(SELECT...)`·GRAPH_TRAVERSE·MODE ANN·VECTOR_TO_STR를 지원 문법으로 가정하지 않습니다.

---

[이전: 시작하기](../getting-started/) · [다음: 내 문서로 검색과 RAG 만들기](../document-rag/)


## 문법 레퍼런스

- [VECTOR 타입](/kr/dbms-8.9/reference/sql/types/vector/)
- [검색 문법과 함수](/kr/dbms-8.9/reference/sql/syntax/search-syntax/)
