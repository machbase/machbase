---
type: docs
title: '11.1 시작하기'
weight: 10
toc: true
---

이 절에서는 숫자 벡터로 검색 SQL을 익힙니다. 임베딩 모델과 LLM은 필요하지 않습니다.

| 방식 | 적합한 시작점 | 필요한 준비 | 결과 해석 |
|---|---|---|---|
| BM25 | 제품명·오류 코드·정확한 용어·키워드 | BODY의 BM25 인덱스 | 텍스트 점수가 클수록 앞 |
| Exact vector | 소규모 문서, 좁은 업무 조건, ANN 정확도 비교 | 저장 벡터와 질문 벡터 | 거리가 작을수록 앞 |
| HNSW | 이웃 그래프를 이용한 ANN | VECTOR의 HNSW 인덱스 | 근사 검색, 그래프 자원 고려 |
| 디스크 IVF | 인덱스 전체를 메모리에 두기 어려운 규모 | VECTOR의 IVF 인덱스와 학습 | 일부 목록을 검색, PROBES로 탐색량 조절 |
| Hybrid | 키워드와 의미를 함께 반영 | BM25와 질문/문서 벡터 | 두 분기의 순위를 RRF로 결합 |

- **Standard TRANSACTION 테이블 대상**입니다. LOG/TAG의 벡터 검색이나 Cluster 지원으로 해석하지 않습니다.
- VECTOR 지원 플랫폼은 Linux x86-64, Darwin arm64, Windows x86-64 MinGW UCRT64입니다. 플랫폼별 패키지에 VECTOR 기능이 포함됐는지도 확인합니다.
- `VECTOR(n)`은 유한 FLOAT32 숫자 1~65,536개를 저장합니다. SQL ARRAY의 1,024 요소 상한과 다릅니다.
- 문서를 문단/절/표/절차 단위의 **청크**로 나누고 출처를 보존하는 일, 임베딩 모델 실행, 최종 LLM 호출은 애플리케이션이 담당합니다.
- `TO_VECTOR('문장',1024)`는 임베딩 API가 아닙니다. 이 함수는 **숫자 배열 텍스트**를 VECTOR로 바꿉니다.
- HNSW·IVF는 ANN 방식입니다. `MODE AUTO`는 ANN 강제가 아니며, 인덱스 상태·거리·필터에 따라 Exact 경로를 선택할 수 있습니다.

## 접속 준비

아래 Bash 명령에서 실제 설치 home과 **실습 서버** 주소·포트를 지정합니다. 이미 기동된 실습 서버가 있으면 DB 생성 명령은 필요 없습니다.

```bash
export MACHBASE_HOME=/opt/machbase89-lab
export PATH="$MACHBASE_HOME/bin:$PATH"
export M89_HOST=127.0.0.1 M89_PORT=5656 M89_USER=SYS
read -rsp '실습 DB 비밀번호: ' M89_PASSWORD
export M89_PASSWORD
printf '\n'
```

관리자가 새 전용 설치 home을 준비했고 아직 DB가 없는 경우에만 그 home에서 `machadmin -c`, `machadmin -u`로 생성·기동합니다. `M89_PORT`는 실제 `conf/machbase.conf`의 `PORT_NO`와 맞춰야 합니다. 기존 `MACHBASE_PORT_NO` 환경변수도 다른 포트로 설정돼 있지 않은지 확인하세요.

이후 SQL 블록을 예를 들어 `m89.sql`로 저장하고 다음 형식으로 실행합니다.

```bash
machsql -s "$M89_HOST" -P "$M89_PORT" -u "$M89_USER" \
  -p "$M89_PASSWORD" -f m89.sql
```

| 실습 | 런타임 준비 |
|---|---|
| SQL | DBMS 8.9 Standard 서버, machsql |
| Python RAG | Python3.10 이상, 해당 Python SDK, 아래 고정 임베딩 패키지 |
| JDBC | Java8 호환 예제, 최신 machbase.jar |
| Node | Node18 이상, VECTOR가 반영된 ts-client |
| Go | Go1.22 이상, VECTOR가 반영된 neo-client/v2 |
| .NET | 이 예제는 net8.0, 최신 4.0/full 또는 Universal provider |

SQL만 실습할 때는 Python 모델·ONNX·LLM이 필요 없습니다. native VECTOR SDK 실습에는 서버와 SDK 양쪽의 CMI 4.0.5 지원이 필요합니다. 설치된 오래된 wheel/JAR/npm/NuGet 파일을 현재 SDK로 가정하지 마세요.

## 첫 검색 실습

다음 전체 블록을 `89_quickstart.sql`로 저장해 위의 `machsql ... -f 89_quickstart.sql`로 실행합니다. 같은 이름의 객체가 이미 있으면 중단합니다. 테이블은 추가 실습을 위해 마지막에 남깁니다.

첫 세 숫자는 문장 의미를 표현한 실제 임베딩이 아니라 SQL 동작을 확인하기 위한 가상 벡터입니다.

[전체 코드 다운로드: 89_quickstart.sql](/assets/dbms-8.9/89_quickstart.sql)

<details>
<summary>전체 코드 보기</summary>

```sql
-- 8.9 검색 실습: 새 전용 DB에서 한 번 실행한다. M89_DOCS는 마지막에 남긴다.
CREATE TRANSACTION TABLE M89_DOCS (
 ID INTEGER PRIMARY KEY, TENANT INTEGER, DOC_ID INTEGER, BODY TEXT,
 V VECTOR(3) PROPERTY(EMBEDDING_SPACE='m89-numeric-v1')
);
INSERT INTO M89_DOCS VALUES(1,1,10,'펌프 밸브 점검과 누수 확인','[1,0,0]');
INSERT INTO M89_DOCS VALUES(2,1,10,'펌프 진동과 소음 점검',TO_VECTOR('[0.8,0.2,0]',3));
INSERT INTO M89_DOCS VALUES(3,1,20,'모터 베어링 교체',TO_VECTOR('[0,1,0]',3));
INSERT INTO M89_DOCS VALUES(4,2,30,'다른 사업장의 펌프 점검','[1,0,0]');
INSERT INTO M89_DOCS VALUES(5,1,40,'데이터베이스 백업 복원','[0,0,1]');
INSERT INTO M89_DOCS VALUES(6,1,50,'펌프 점검 임베딩 대기',NULL);
SELECT ID,TENANT,VECTOR_TO_JSON(V) AS VJSON FROM M89_DOCS ORDER BY ID;
CREATE INDEX M89_DOCS_TEXT ON M89_DOCS(BODY) INDEX_TYPE BM25 ANALYZER='CJK_EN';
ALTER INDEX M89_DOCS_TEXT WAIT TIMEOUT 60;
SELECT R.ID,R.BODY,R.__SEARCH_TEXT_SCORE FROM TEXT_SEARCH(
 TABLE M89_DOCS,TEXT BODY,QUERY_TEXT '펌프',FILTER(TENANT=1),TOP_K 3) R
 ORDER BY R.__SEARCH_TEXT_SCORE DESC,R.ID;
SELECT R.ID,R.__SEARCH_VECTOR_DISTANCE FROM VECTOR_SEARCH(
 TABLE M89_DOCS,VECTOR V,QUERY_VECTOR TO_VECTOR('[1,0,0]',3),
 SPACE 'm89-numeric-v1',METRIC COSINE,MODE EXACT,FILTER(TENANT=1),TOP_K 3) R
 ORDER BY R.__SEARCH_VECTOR_DISTANCE,R.ID;
CREATE INDEX M89_DOCS_TENANT ON M89_DOCS(TENANT) INDEX_TYPE BTREE;
CREATE INDEX M89_DOCS_VECTOR ON M89_DOCS(V) INDEX_TYPE HNSW DISTANCE=COSINE;
ALTER INDEX M89_DOCS_VECTOR WAIT TIMEOUT 60;
EXPLAIN FULL SELECT R.ID FROM VECTOR_SEARCH(TABLE M89_DOCS,VECTOR V,
 QUERY_VECTOR TO_VECTOR('[1,0,0]',3),SPACE 'm89-numeric-v1',
 MODE AUTO,FILTER(TENANT=1),TOP_K 3) R;
DROP INDEX M89_DOCS_VECTOR;
CREATE INDEX M89_DOCS_VECTOR ON M89_DOCS(V)
 INDEX_TYPE IVF DISTANCE=COSINE,LISTS=2,PROBES=2;
ALTER INDEX M89_DOCS_VECTOR WAIT TIMEOUT 60;
SELECT R.ID,R.BODY,R.__SEARCH_SCORE,R.__SEARCH_VECTOR_DISTANCE,R.__SEARCH_TEXT_SCORE
 FROM HYBRID_SEARCH(TABLE M89_DOCS,VECTOR V,TEXT BODY,
 QUERY_VECTOR TO_VECTOR('[1,0,0]',3),QUERY_TEXT '펌프',SPACE 'm89-numeric-v1',
 MODE AUTO,VECTOR_WEIGHT 0.5,VECTOR_CANDIDATES 10,TEXT_CANDIDATES 10,
 FILTER(TENANT=1),TOP_K 3) R ORDER BY R.__SEARCH_SCORE DESC,R.ID;
ALTER INDEX M89_DOCS_VECTOR SET PROBES=1;
ALTER INDEX M89_DOCS_VECTOR REBUILD;
ALTER INDEX M89_DOCS_VECTOR WAIT TIMEOUT 60;
CREATE TRANSACTION TABLE M89_ACL(USER_ID INTEGER,DOC_ID INTEGER);
INSERT INTO M89_ACL VALUES(7,10);
INSERT INTO M89_ACL VALUES(7,10);
SELECT R.ID,R.BODY FROM TEXT_SEARCH(TABLE M89_DOCS AS D,TEXT D.BODY,
 QUERY_TEXT '펌프',FILTER(D.TENANT=1 AND EXISTS(
 SELECT 1 FROM M89_ACL A WHERE A.USER_ID=7 AND A.DOC_ID=D.DOC_ID)),TOP_K 10) R
 ORDER BY R.ID;
DROP TABLE M89_ACL;
SELECT R.ID,R.V_VECTOR_DISTANCE FROM VECTOR_SEARCH(TABLE M89_DOCS,VECTOR V,
 QUERY_VECTOR TO_VECTOR('[1,0,0]',3),SPACE 'm89-numeric-v1',MODE EXACT,
 RESULT_PREFIX 'V_',FILTER(TENANT=1),TOP_K 3) R ORDER BY R.V_VECTOR_DISTANCE,R.ID;
BEGIN;
UPDATE M89_DOCS SET BODY='펌프 밸브 점검 절차 개정',V=TO_VECTOR('[0.9,0.1,0]',3) WHERE ID=1;
SELECT ID,BODY,VECTOR_TO_JSON(V) AS VJSON FROM M89_DOCS WHERE ID=1;
ROLLBACK;
SELECT ID,BODY,VECTOR_TO_JSON(V) AS VJSON FROM M89_DOCS WHERE ID=1;
SELECT TABLE_NAME,INDEX_NAME,STATE,ERROR_CODE,LAST_ERROR FROM V$TEXT_INDEXES WHERE TABLE_NAME='M89_DOCS';
SELECT TABLE_NAME,INDEX_NAME,STATE,BUILD_PHASE,PENDING_VECTOR_ROWS,LIST_COUNT,PROBE_COUNT
 FROM V$VECTOR_INDEXES WHERE TABLE_NAME='M89_DOCS';
SELECT VECTOR_TO_JSON(TO_VECTOR('[1,null]',4)) AS PADDED;
SELECT VECTOR_DIM(TO_VECTOR('[3,4]',2)) AS DIM,VECTOR_NORM(TO_VECTOR('[3,4]',2)) AS NORM;
SELECT VECTOR_TO_JSON(VECTOR_NORMALIZE(TO_VECTOR('[3,4]',2))) AS UNIT_VECTOR;
SELECT VECTOR_DISTANCE(TO_VECTOR('[3,0]',2),TO_VECTOR('[0,4]',2),'L2') AS D;
SELECT CAST(TO_VECTOR('[1,2,3]',3) AS FLOAT[3]);
-- 정리는 별도 실행: DROP TABLE M89_DOCS;
```

</details>

### 결과 읽기

1. 첫 조회는 6행입니다. ID6의 벡터 전체는 SQL NULL입니다.
2. `TEXT_SEARCH`는 tenant=1에서 펌프가 포함된 ID1·2·6을 반환합니다. ID4는 tenant=2라 제외됩니다. 텍스트 점수와 그 순서는 색인 통계에 따라 달라질 수 있습니다.
3. COSINE Exact 검색의 ID1 거리는 0, ID2는 약 0.0298575입니다. ID3·5는 같은 거리 1이며, 명시한 `ORDER BY distance,ID`로 결과 표시 순서를 정합니다. 현재 실습의 Top-3은 ID1·2·3입니다. ID6은 벡터 검색에서 제외됩니다.
4. HNSW가 있어도 작은 tenant 필터는 `BTREE_EXACT`로 실행될 수 있습니다. 작은 예제의 `AUTO` 성공을 대규모 ANN Recall 증거로 사용하지 않습니다.
5. 같은 VECTOR 인덱스를 DROP한 뒤 IVF로 재생성했습니다. HNSW/IVF를 계속 비교하려면 별도 테이블에 같은 데이터를 적재합니다.
6. ACL 조회는 사용자7이 읽을 수 있는 문서10의 ID1·2를 반환합니다. 중복 ACL 행이 있어도 EXISTS이므로 원본 청크가 복제되지 않습니다.
7. UPDATE 직후에는 새 값이 보이지만 ROLLBACK 후 ID1의 원문과 벡터가 복구됩니다.

### 독립적으로 다시 실행하는 검색 예

테이블·BM25가 남아 있으므로 다음 블록은 따로 실행할 수 있습니다.

```sql
-- 키워드만 검색
SELECT R.ID,R.BODY,R.__SEARCH_TEXT_SCORE
FROM TEXT_SEARCH(TABLE M89_DOCS,TEXT BODY,QUERY_TEXT '펌프',
 FILTER(TENANT=1),TOP_K 3) R ORDER BY R.__SEARCH_TEXT_SCORE DESC,R.ID;

-- 벡터만 검색: SQL 문자열 METRIC과 scalar 함수의 metric 인자를 구분한다.
SELECT R.ID,R.__SEARCH_VECTOR_DISTANCE
FROM VECTOR_SEARCH(TABLE M89_DOCS,VECTOR V,
 QUERY_VECTOR TO_VECTOR('[1,0,0]',3),SPACE 'm89-numeric-v1',
 METRIC COSINE,MODE EXACT,FILTER(TENANT=1),TOP_K 3) R
ORDER BY R.__SEARCH_VECTOR_DISTANCE,R.ID;

-- 무필터 계획은 경로 확인용 진단이다. 서비스의 tenant/ACL 필터를 제거하지 않는다.
EXPLAIN FULL SELECT R.ID FROM VECTOR_SEARCH(TABLE M89_DOCS,VECTOR V,
 QUERY_VECTOR TO_VECTOR('[1,0,0]',3),SPACE 'm89-numeric-v1',MODE AUTO,TOP_K 3) R;
```

BM25의 기본 analyzer는 `CJK_EN`입니다. 영문·숫자·밑줄 연속열과 한글/한자/히라가나/가타카나를 처리하며, CJK에는 한 글자·겹치는 두 글자 토큰을 사용합니다. 형태소 분석·번역·간체/번체 변환은 수행하지 않습니다. 공백으로 나뉜 검색어는 OR로 결합합니다. `QUERY_TEXT`는 일반 텍스트이며 FTS MATCH 식을 직접 실행하는 인터페이스가 아닙니다. 기존 `KO_EN` 인덱스는 유지되며 REBUILD로 analyzer가 바뀌지 않습니다. analyzer를 바꾸려면 새 인덱스를 만들고 WAIT 후 전환합니다.

---

[다음: 검색 방식과 인덱스 선택](../search-indexes/)
