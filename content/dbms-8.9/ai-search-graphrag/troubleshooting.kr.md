---
type: docs
title: '11.10 문제 해결과 실습 정리'
weight: 100
toc: true
---

실습 결과가 예상과 다를 때 아래 표에서 증상을 찾습니다. 정리 명령은 해당 실습으로 직접 만든 객체에만 실행합니다.

| 증상 | 먼저 확인할 것 |
|---|---|
| VECTOR/검색 문법 자체 오류 | 기능 포함 서버인지, Standard TRANSACTION인지, 실제 접속 host/port인지 |
| TO_VECTOR에 문장을 넣어 오류 | 먼저 외부 모델로 문장을 숫자 배열로 임베딩 |
| 차원·SPACE 오류 | 모델 출력 차원, column dimension, SPACE literal, 동일 revision/정규화 |
| NORMALIZE/COSINE 영벡터 오류 | 빈/실패 임베딩과 전처리, zero padding만으로 된 벡터 검사 |
| INDEX_NOT_READY | BM25 상태·LAST_ERROR 확인. WAIT timeout은 취소가 아님 |
| AUTO가 Exact 또는 PROBES 변화 효과 없음 | 실제 B-tree Exact 경로인지 EXPLAIN FULL로 확인 |
| 입력 후 CPU·disk 사용이 증가 | BUILD_PHASE·PENDING·학습·REBUILD·남은 공간 점검 |
| 다른 사업장 문서가 반환 | 검색 함수 내부 FILTER에 tenant·ACL을 넣었는지 |
| 결과는 나오지만 질문에 답할 근거가 없음 | Top-K는 답변 가능성 보장이 아님. evidence와 적절한 abstention 정책 확인 |
| Vector is not a constructor / enum 없음 | 실제 최신 SDK 경로·로컬 package 확인 |
| VECTOR(4096)을 DOUBLE[4096]으로 못 읽음 | SQL ARRAY는1024 상한. native VECTOR 또는 JSON TEXT로 조회 |
| 질문마다 모델 로딩이 오래 걸림 | CLI의 새 프로세스 특성. 서비스에서는 모델 인스턴스 재사용 |
| 재실행 시 테이블/PK 충돌 | 앞선 실습 상태 확인. 본인이 만든 M89_ 객체만 명시 정리 |

### 검색 품질을 측정하는 두 방법

ANN Recall@K는 **동일 모델·질문 벡터·필터·snapshot**의 Exact Top-K와 AUTO 결과를 비교합니다. Exact 결과 ID 집합이 E, AUTO가 A라면 `|A∩E|/|E|`로 계산하고 E가 비었으면 N/A로 처리합니다. latency는 execute부터 모든 결과 fetch까지 같은 조건으로 측정합니다.

문서 의미 품질은 별도로 측정합니다. 검색 전에 질문별 정답 근거/출처를 고정하고 Hit@K·누락 근거·정답 없는 질문을 확인하세요. Exact와 ANN 결과가 일치해도 임베딩/청킹/정답 정의가 잘못되면 업무 질문을 해결하지 못합니다. 개발 질문으로 설정을 고른 뒤 별도 평가 질문으로 확인합니다. 검색 결과를 본 뒤 정답 근거를 추가한 점수를 미노출 평가로 사용하지 않습니다.

### 정리

실행한 예제의 객체만 선택해서 삭제합니다. Python load가 만든 M89_RAG는 다음 CLI로 정리합니다.

```bash
python 89_rag.py cleanup --yes
```

SQL/SDK 실습 객체는 다음 SQL을 파일로 저장해 실행합니다.

```sql
DROP TABLE IF EXISTS M89_ACL;
DROP TABLE IF EXISTS M89_DOCS;
DROP TABLE IF EXISTS M89_SDK;
```

실습을 위해 직접 시작한 전용 서버만 `machadmin -s`로 종료합니다.

---



## 그래프 검색 문제 해결

| 증상 | 확인할 내용 |
|---|---|
| WITH RECURSIVE 자체가 거부됨 | 를 지원하는 DBMS 8.9 서버인지, 실제 접속 host/port와 Standard판인지 |
| 순환에서 끝나지 않음 | UNION의전체튜플에depth/path를넣었는지, UNION ALL에깊이/방문조건이있는지 |
| 같은 노드가 여러 번 나옴 | 평행edge·서로다른경로·UNION ALL의의도된결과인지 |
| 문자열 경로가 잘리거나 타입 오류 | anchor/recursive term의CAST와길이,정수ID의LONG타입 |
| 빈 anchor인데도 오류 | 정적검증은생략되지않음.재귀term컬럼·참조·타입확인 |
| Top-K보다 결과 행이 많음 | HIT와PATH/STEP/EDGE_SOURCE를구분.원문근거행을문서수로세지않음 |
| 오래된/미공개 원문이 검색됨 | DOCUMENT.state/current_version과CHUNK.document_version,모든근거JOIN의kb_id |
| EXPLAIN을 prepared로 실행해 오류 | 일반cursor로계획실행;업무SELECT prepared와분리 |
| FULL만 보고 인덱스 사용을 판정할 수 없음 | 일반EXPLAIN의트리/KEY RANGE와FULL의실행통계를함께확인 |
| SQL은 성공했지만 답변 근거가 없음 | 그래프/검색점수는업무정답보장이아님.원문과abstention정책확인 |

### 의도한 거부 예제

다음은 정상 실습과 분리합니다. 두 쿼리는 각각 열 수 불일치와 재귀 UNION의 TEXT 중복 제거 미지원 때문에 거부되어야 합니다. 오류 뒤에는 같은 연결에서 `SELECT 1 AS N`을 실행해 정상 재사용을 확인할 수 있습니다.

```sql
-- 두SQL모두거부되는것이정상이다. 정상예제실행과분리한다.
WITH RECURSIVE R(N) AS (SELECT 1 UNION ALL SELECT N,2 FROM R) SELECT * FROM R;
WITH RECURSIVE R(T) AS (SELECT CAST('seed' AS TEXT) UNION SELECT T FROM R) SELECT T FROM R;
```

### 실습 정리

아래는 **이 장으로 직접 만든 M89_G_객체임을 확인한 뒤** 실행합니다. 해당 테이블의 인덱스도 함께 정리됩니다. 다른 실습의 M89_DOCS나 GRRAG_자료까지 삭제하지 않습니다.

```sql
-- 본인이그래프 실습으로만든객체임을확인한뒤실행한다.
DROP TABLE M89_G_EVIDENCE;
DROP TABLE M89_G_EDGE;
DROP TABLE M89_G_NODE;
DROP TABLE M89_G_CHUNK;
DROP TABLE M89_G_DOCUMENT;
```

직접 시작한 실습 서버만 정상 종료합니다. 이미 기동되어 있던 업무 서버를 실습 정리 명령으로 중지하지 않습니다.

---

[이전: 운영과 성능 관리](../operations/)
