---
type: docs
title: '벡터·텍스트·Hybrid 검색'
weight: 95
toc: true
---


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



## 관련 문서

- [VECTOR 값과 거리 함수](../../types/vector/)
- [검색 실습과 인덱스 선택](/kr/dbms-8.9/ai-search-graphrag/search-indexes/)
