---
type: docs
title: 'VECTOR'
weight: 95
toc: true
---

`VECTOR(n)`은 1~65,536개의 유한 FLOAT32 요소를 저장합니다.
Standard Edition의 TRANSACTION 테이블에서 사용합니다.

## 선언과 입력

```sql
CREATE TRANSACTION TABLE VECTOR_DOCS (
 ID LONG PRIMARY KEY,
 EMBEDDING VECTOR(3) PROPERTY(EMBEDDING_SPACE='documents-v1')
);
INSERT INTO VECTOR_DOCS VALUES(1,TO_VECTOR('[1,0,0]',3));
SELECT VECTOR_TO_JSON(EMBEDDING) FROM VECTOR_DOCS WHERE ID=1;
```

`EMBEDDING_SPACE`는 문서와 질문에 사용하는 임베딩 계약을 식별합니다.

## 값 변환과 거리 함수


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


[검색 실습과 인덱스 선택](/kr/dbms-8.9/ai-search-graphrag/search-indexes/)

## 큰 벡터의 JSON 출력

`VECTOR_TO_JSON`은 입력 차원에 맞춰 출력 버퍼를 확보합니다. JSON 표현이 32 KiB를
넘는 큰 벡터도 전체 값을 TEXT로 반환합니다. 차원과 숫자 표현에 따라 출력 길이가 달라지므로
애플리케이션에서 작은 고정 길이 문자열로 받지 않습니다.

SQL ARRAY의 요소 수 제한과 VECTOR의 차원 제한은 별개입니다. 큰 벡터는 native VECTOR
API 또는 `VECTOR_TO_JSON`으로 읽습니다. CLI 화면이나 애플리케이션이 출력을 줄여 표시할
경우 서버 반환값의 길이와 클라이언트의 표시·버퍼 제한을 구분해 확인합니다.
