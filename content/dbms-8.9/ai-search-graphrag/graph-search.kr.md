---
type: docs
title: '11.6 관계를 활용한 GraphRAG 검색'
weight: 60
toc: true
---

[그래프 실습 데이터](../knowledge-model/)를 먼저 준비합니다. 관계로 문서 후보를 좁힌 다음 Hybrid 검색으로 순위를 결정합니다.

실제 사용자 질문은 node_id를 포함하지 않습니다. 앱이 LLM/식별자 추출로 용어 후보를 만들고 DB의 정규 이름·별칭과 확인합니다. 정확한 표현이 없으면 개념 설명의 벡터·BM25 검색으로 후보를 보충합니다. 검색 점수를 정답 확률로 해석하지 않습니다.

다음 세 SQL은 각각 별칭 확인, 개념 Hybrid 검색, 그래프 제한 없는 문서 Hybrid 검색입니다. 예제의 질문 벡터는 합성 `[1,0,0]`입니다.

[전체 코드 다운로드: 89_graph_seeds.sql](/assets/dbms-8.9/89_graph_seeds.sql)

<details>
<summary>전체 코드 보기</summary>

```sql
-- 정규 이름/별칭 확인
SELECT * FROM (
SELECT N.node_id,N.node_kind,N.label,N.description,
       N.label_key AS matched_alias,CAST(1 AS DOUBLE) AS seed_score,
       'EXACT_NAME' AS match_method
FROM M89_G_NODE N
WHERE N.kb_id=1 AND N.state='PUBLISHED' AND N.label_key IN ('p101')
  AND (N.node_kind='ENTITY' OR ('context'='taxonomy' AND N.node_kind='CLASS'))
  AND EXISTS(SELECT 1 FROM M89_G_EVIDENCE NS,M89_G_CHUNK C,M89_G_DOCUMENT D
      WHERE NS.kb_id=N.kb_id AND NS.target_kind='NODE' AND NS.target_id=N.node_id
        AND C.chunk_id=NS.chunk_id AND C.kb_id=NS.kb_id
        AND D.document_id=C.document_id AND D.kb_id=C.kb_id
        AND D.state='PUBLISHED' AND D.current_version=C.document_version)
UNION ALL
--  사용. 먼저 정확한 코드/별칭을 조회한다.
-- alias_key는 앱이 적재 때와 같은 NFC/대소문자 정책으로 정규화한 값이다.
SELECT N.node_id,N.node_kind,N.label,N.description,
       A.label_key AS matched_alias,CAST(1 AS DOUBLE) AS seed_score,
       'EXACT_ALIAS' AS match_method
FROM M89_G_NODE A,
     M89_G_NODE N
WHERE (A.node_kind='ALIAS' AND A.state='PUBLISHED' AND A.kb_id=1 AND A.label_key IN ('p101')
  AND N.state='PUBLISHED'
  AND (N.node_kind='ENTITY' OR ('context'='taxonomy' AND N.node_kind='CLASS'))
  AND EXISTS(
      SELECT 1 FROM M89_G_EVIDENCE AE,
     M89_G_CHUNK C,
     M89_G_DOCUMENT D
WHERE (AE.kb_id=A.kb_id AND AE.target_kind='NODE' AND AE.target_id=A.node_id
        AND D.state='PUBLISHED' AND D.current_version=C.document_version)
  AND (C.chunk_id=AE.chunk_id AND C.kb_id=AE.kb_id)
  AND (D.document_id=C.document_id AND D.kb_id=C.kb_id)
)
  AND EXISTS(
      SELECT 1 FROM M89_G_EVIDENCE NS,
     M89_G_CHUNK C,
     M89_G_DOCUMENT D
WHERE (NS.target_kind='NODE' AND NS.kb_id=N.kb_id AND NS.target_id=N.node_id
        AND D.state='PUBLISHED' AND D.current_version=C.document_version)
  AND (C.chunk_id=NS.chunk_id AND C.kb_id=NS.kb_id)
  AND (D.document_id=C.document_id AND D.kb_id=C.kb_id)
))
  AND (N.node_id=A.canonical_id AND N.kb_id=A.kb_id)
) MATCHES
ORDER BY matched_alias,node_id;

-- 질문 벡터/텍스트로 개념 검색
-- 이름이 질문에 없어도 질문 전체로 개념·개체 설명을 검색한다.
SELECT R.node_id,R.node_kind,R.label,R.description,
       R.__SEARCH_VECTOR_DISTANCE,R.__SEARCH_TEXT_SCORE,
       R.__SEARCH_SCORE AS seed_score,'HYBRID' AS match_method
FROM HYBRID_SEARCH(
    TABLE M89_G_NODE AS N,
    VECTOR N.embedding,TEXT N.search_text,
    QUERY_VECTOR TO_VECTOR('[1,0,0]',3),
    QUERY_TEXT '펌프 진동',
    SPACE 'm89-g-node-v1',METRIC COSINE,MODE EXACT,
    VECTOR_CANDIDATES 100,TEXT_CANDIDATES 100,
    FILTER(
        N.kb_id=1 AND N.state='PUBLISHED'
        AND (N.node_kind='ENTITY' OR ('context'='taxonomy' AND N.node_kind='CLASS'))
        AND EXISTS(
            SELECT 1 FROM M89_G_EVIDENCE NS,
     M89_G_CHUNK C,
     M89_G_DOCUMENT D
WHERE (NS.target_kind='NODE' AND NS.kb_id=N.kb_id AND NS.target_id=N.node_id
              AND D.state='PUBLISHED' AND D.current_version=C.document_version)
  AND (C.chunk_id=NS.chunk_id AND C.kb_id=NS.kb_id)
  AND (D.document_id=C.document_id AND D.kb_id=C.kb_id)
)
    ),
    TOP_K 3
) R
ORDER BY R.__SEARCH_SCORE DESC,R.node_id;

-- 그래프 제한 없이 직접 문서 검색
--  직접 문서 검색. 그래프 제한과 관계없는 검색 결과임을 별도 표시한다.
SELECT R.chunk_id,R.body,R.document_id,R.document_version,R.locator,
       D.title,D.source_uri,R.__SEARCH_SCORE AS document_score
FROM HYBRID_SEARCH(
    TABLE M89_G_CHUNK AS C,VECTOR C.embedding,TEXT C.body,
    QUERY_VECTOR TO_VECTOR('[1,0,0]',3),QUERY_TEXT '펌프 진동',
    SPACE 'm89-g-chunk-v1',METRIC COSINE,MODE EXACT,
    VECTOR_CANDIDATES 100,TEXT_CANDIDATES 100,
    FILTER(
        C.kb_id=1
        AND EXISTS(
            SELECT 1 FROM M89_G_DOCUMENT D
            WHERE D.document_id=C.document_id AND D.kb_id=C.kb_id
              AND D.state='PUBLISHED' AND D.current_version=C.document_version
        )
    ),
    TOP_K 3
) R,M89_G_DOCUMENT D
WHERE D.document_id=R.document_id AND D.kb_id=1
  AND D.state='PUBLISHED' AND D.current_version=R.document_version
ORDER BY R.__SEARCH_SCORE DESC,R.chunk_id;
```

</details>

- 별칭 `p101`은 정규 ENTITY 노드1을 가리키고 match_method는 `EXACT_ALIAS`입니다.
- 개념 검색은 ENTITY만 후보로 삼습니다. ALIAS/RELATION_TYPE 행 자체가 일반 업무 개념처럼 순위에 섞이지 않습니다.
- 직접 문서 검색은 공개·현재 버전 조건을 만족하는201·202·203을 반환합니다. 그래프 연결이 없는 모터 청크203도 검색 범위에 들어갑니다.
- 미공개204와 이전 버전205는 직접 검색에서도 제외됩니다.

같은 모델·revision·전처리·정규화와 SPACE의 벡터를 저장과 질문에 사용합니다. 이 장의3차원 벡터를 실제 BGE-M3의1024차원 벡터와 섞지 않습니다. `TO_VECTOR`는 숫자 배열 텍스트를 변환할 뿐 문장을 임베딩하지 않습니다.

## 관계 후보와 Hybrid 검색

그래프를 따라 찾은 원문 ID를 `HYBRID_SEARCH`의 FILTER에 전달하면 **두 검색 분기의 Top-N 전에 후보가 제한**됩니다. 이 예제는 시작점을 펌프1, 최대 깊이를2, 문서 Top-K를3으로 고정했습니다. 실제 앱은 검증한 시작점·업무 범위·깊이·질문 벡터를 바인딩합니다.

| CTE | 하는 일 |
|---|---|
| readable_chunks | 공개 문서의 현재 버전 청크 |
| readable_nodes / readable_edges | 현재 원문 근거가 있는 게시 노드·승인 관계와 술어 타입 확인 |
| seeds / arcs / walk | 시작점, 양방향 관계, 깊이·경로·순환 조건 |
| best_nodes | 시작점별 도달 노드의 대표 경로 |
| candidate_routes / candidate_keys | 연결 이유와 구분되는 문서 후보 집합 |
| hits | 후보 안에서  Hybrid Top-K |
| picked_routes / path_steps | 최종 문서의 대표 경로·단계 |
| result_rows | HIT/PATH/STEP/EDGE_SOURCE를 같은 결과 집합으로 반환 |

다음은 그래프 탐색부터 문서 검색과 근거 반환까지 수행하는 전체 SQL입니다. 본문이 길어도 일부를 생략하지 않았으므로 `89_graph_rag.sql`로 저장해 실행할 수 있습니다.


[전체 코드 다운로드: 89_graph_rag.sql](/assets/dbms-8.9/89_graph_rag.sql)

<details>
<summary>전체 코드 보기</summary>

```sql
-- 양방향 문맥 탐색이며 F/R은 원래 관계 방향을 보존한다.
-- 기본 context는 6개 도메인 관계만 탐색한다. 분류 확장은 명시적 taxonomy 정책에서 허용한다.
-- seed 자리표시는 검증된 ID 개수에 맞춰 named bind로만 확장한다.
-- Standard TRANSACTION:  재귀 탐색과  원문 검색을 연결한다.
-- 2는 앱에서 0..4로 검사한다. seed_id 중복은 앱에서 제거한다.
-- 내부 키는 LONG. 경로에서만 명시적 CAST와 19자리 LPAD로 직렬화한다.
WITH RECURSIVE
readable_chunks AS (
    SELECT C.chunk_id,C.kb_id,C.document_id,C.document_version,
           C.locator,C.body,D.title,D.source_uri
    FROM M89_G_CHUNK C,
     M89_G_DOCUMENT D
WHERE (C.kb_id=1 AND D.state='PUBLISHED'
      AND C.document_version=D.current_version)
  AND (D.document_id=C.document_id AND D.kb_id=C.kb_id)
),
readable_nodes AS (
    SELECT N.node_id,N.node_kind,N.label
    FROM M89_G_NODE N
    WHERE N.kb_id=1 AND N.state='PUBLISHED'
      AND (N.node_kind='ENTITY' OR ('context'='taxonomy' AND N.node_kind='CLASS'))
      AND EXISTS(
          SELECT 1 FROM M89_G_EVIDENCE NS,
     M89_G_CHUNK C,M89_G_DOCUMENT D
WHERE (NS.target_kind='NODE' AND NS.kb_id=1 AND NS.target_id=N.node_id)
  AND (C.chunk_id=NS.chunk_id AND C.kb_id=NS.kb_id)
  AND (D.document_id=C.document_id AND D.kb_id=C.kb_id
       AND D.state='PUBLISHED' AND D.current_version=C.document_version)
)
),
readable_edges AS (
    SELECT E.edge_id,E.source_id,E.predicate_id,E.target_id,P.code AS predicate_code
    FROM M89_G_EDGE E,
     readable_nodes S,
     readable_nodes T,
     M89_G_NODE P
WHERE (E.kb_id=1 AND E.state='APPROVED'
      AND EXISTS(
          SELECT 1 FROM M89_G_EVIDENCE ES,
     M89_G_CHUNK C,M89_G_DOCUMENT D
WHERE (ES.target_kind='EDGE' AND ES.kb_id=1 AND ES.target_id=E.edge_id)
  AND (C.chunk_id=ES.chunk_id AND C.kb_id=ES.kb_id)
  AND (D.document_id=C.document_id AND D.kb_id=C.kb_id
       AND D.state='PUBLISHED' AND D.current_version=C.document_version)
))
  AND (S.node_id=E.source_id)
  AND (T.node_id=E.target_id)
  AND (P.node_id=E.predicate_id AND P.kb_id=E.kb_id
      AND P.node_kind='RELATION_TYPE' AND P.state='PUBLISHED'
      AND P.source_kind=S.node_kind AND P.target_kind=T.node_kind)
),
seeds AS (
    SELECT N.node_id AS seed_id,CAST(1.0 AS DOUBLE) AS seed_score
    FROM readable_nodes N WHERE N.node_id IN (1)
),
arcs AS (
    SELECT E.edge_id,E.source_id AS from_id,E.target_id AS to_id,
           E.predicate_id,E.predicate_code,'F' AS direction
    FROM readable_edges E
    WHERE E.predicate_code IN ('PART_OF','REQUIRES','APPLIES_TO','SUPPORTS','LIMITED_BY','RELATED_TO')
       OR ('context'='taxonomy' AND E.predicate_code IN ('INSTANCE_OF','SUBCLASS_OF'))
    UNION ALL
    SELECT E.edge_id,E.target_id AS from_id,E.source_id AS to_id,
           E.predicate_id,E.predicate_code,'R' AS direction
    FROM readable_edges E
    WHERE E.predicate_code IN ('PART_OF','REQUIRES','APPLIES_TO','SUPPORTS','LIMITED_BY','RELATED_TO')
       OR ('context'='taxonomy' AND E.predicate_code IN ('INSTANCE_OF','SUBCLASS_OF'))
),
walk(seed_id,node_id,depth,from_id,edge_id,predicate_id,predicate_code,direction,route_key,node_path) AS (
    SELECT S.seed_id,S.seed_id,0,
           CAST(NULL AS LONG),CAST(NULL AS LONG),CAST(NULL AS LONG),
           CAST(NULL AS VARCHAR(64)),CAST(NULL AS VARCHAR(4)),
           CAST('@' AS VARCHAR(1024)),
           CAST('|' || CAST(S.seed_id AS VARCHAR(20)) || '|' AS VARCHAR(1024))
    FROM seeds S

    UNION ALL

    SELECT W.seed_id,A.to_id,W.depth+1,W.node_id,A.edge_id,
           A.predicate_id,A.predicate_code,A.direction,
           CAST(W.route_key || '/' || LPAD(CAST(A.edge_id AS VARCHAR(20)),19,'0')
                || A.direction AS VARCHAR(1024)),
           CAST(W.node_path || CAST(A.to_id AS VARCHAR(20)) || '|' AS VARCHAR(1024))
    FROM walk W,
     arcs A
WHERE (W.depth<2
      AND INSTR(W.node_path,'|' || CAST(A.to_id AS VARCHAR(20)) || '|')=0)
  AND (A.from_id=W.node_id)
),
best_nodes AS (
    SELECT W.*
    FROM walk W
    WHERE NOT EXISTS(
        SELECT 1 FROM walk B
        WHERE B.seed_id=W.seed_id AND B.node_id=W.node_id
          AND (B.depth<W.depth OR
               (B.depth=W.depth AND B.route_key<W.route_key))
    )
),
candidate_routes AS (
    SELECT W.seed_id,W.node_id,W.depth,W.route_key,
           NS.chunk_id,'NODE' AS attachment_kind,
           W.node_id AS attachment_id,NS.evidence_id AS source_ref,NS.quote
    FROM best_nodes W,
     M89_G_EVIDENCE NS,
     readable_chunks C
WHERE (NS.target_id=W.node_id AND NS.target_kind='NODE' AND NS.kb_id=1)
  AND (C.chunk_id=NS.chunk_id)
UNION ALL

    SELECT W.seed_id,W.node_id,W.depth,W.route_key,
           ES.chunk_id,'EDGE' AS attachment_kind,
           W.edge_id AS attachment_id,ES.evidence_id AS source_ref,ES.quote
    FROM walk W,
     M89_G_EVIDENCE ES,
     readable_chunks C
WHERE (ES.target_id=W.edge_id AND ES.target_kind='EDGE' AND ES.kb_id=1)
  AND (C.chunk_id=ES.chunk_id)
),
candidate_keys AS (
    SELECT DISTINCT chunk_id FROM candidate_routes
),
hits AS (
    SELECT R.chunk_id,R.__SEARCH_SCORE AS document_score
    FROM HYBRID_SEARCH(
        TABLE M89_G_CHUNK AS C,
        VECTOR C.embedding,TEXT C.body,
        QUERY_VECTOR TO_VECTOR('[1,0,0]',3),
        QUERY_TEXT '펌프 진동',
        SPACE 'm89-g-chunk-v1',METRIC COSINE,MODE EXACT,
        VECTOR_CANDIDATES 100,TEXT_CANDIDATES 100,
        FILTER(C.kb_id=1 AND C.chunk_id IN (
            SELECT chunk_id FROM candidate_keys
        )),
        TOP_K 3
    ) R
),
picked_routes AS (
    SELECT P.*
    FROM candidate_routes P,
     hits H
WHERE (NOT EXISTS(
        SELECT 1 FROM candidate_routes B
        WHERE B.seed_id=P.seed_id AND B.chunk_id=P.chunk_id
          AND (
              B.depth<P.depth OR
              (B.depth=P.depth AND B.route_key<P.route_key) OR
              (B.depth=P.depth AND B.route_key=P.route_key
               AND B.attachment_kind<P.attachment_kind) OR
              (B.depth=P.depth AND B.route_key=P.route_key
               AND B.attachment_kind=P.attachment_kind AND B.source_ref<P.source_ref)
          )
    ))
  AND (H.chunk_id=P.chunk_id)
),
path_steps AS (
    SELECT P.chunk_id,P.seed_id,P.route_key,
           W.depth AS step_no,W.from_id,W.edge_id,W.predicate_id,W.predicate_code,
           W.node_id AS to_id,W.direction
    FROM picked_routes P,
     walk W
WHERE (W.seed_id=P.seed_id AND W.depth>0
      AND SUBSTR(P.route_key,1,LENGTH(W.route_key))=W.route_key)
),
result_rows AS (
    SELECT 'HIT' AS record_type,H.chunk_id AS hit_chunk_id,H.document_score,
           CAST(NULL AS LONG) AS seed_id,CAST(NULL AS DOUBLE) AS seed_score,
           CAST(NULL AS VARCHAR(1024)) AS path_key,CAST(NULL AS INTEGER) AS step_no,
           CAST(NULL AS LONG) AS from_id,CAST(NULL AS LONG) AS predicate_id,
           CAST(NULL AS VARCHAR(64)) AS predicate_code,CAST(NULL AS LONG) AS to_id,
           CAST(NULL AS VARCHAR(4)) AS direction,CAST(NULL AS LONG) AS edge_id,
           C.chunk_id AS source_chunk_id,C.title,C.source_uri,C.locator,C.body,
           CAST(NULL AS VARCHAR(2048)) AS quote,
           CAST(NULL AS VARCHAR(16)) AS attachment_kind,
           CAST(NULL AS LONG) AS attachment_id,CAST(NULL AS TEXT) AS scope_json
    FROM hits H,
     readable_chunks C
WHERE (C.chunk_id=H.chunk_id)
UNION ALL

    SELECT 'PATH',P.chunk_id,H.document_score,P.seed_id,S.seed_score,
           P.route_key,P.depth,CAST(NULL AS LONG),CAST(NULL AS LONG),
           CAST(NULL AS VARCHAR(64)),P.node_id,CAST(NULL AS VARCHAR(4)),CAST(NULL AS LONG),
           C.chunk_id,C.title,C.source_uri,C.locator,CAST(NULL AS TEXT),
           P.quote,P.attachment_kind,P.attachment_id,CAST(NULL AS TEXT)
    FROM picked_routes P,
     seeds S,
     hits H,
     readable_chunks C
WHERE (S.seed_id=P.seed_id)
  AND (H.chunk_id=P.chunk_id)
  AND (C.chunk_id=P.chunk_id)
UNION ALL

    SELECT 'STEP',P.chunk_id,H.document_score,P.seed_id,S.seed_score,
           P.route_key,P.step_no,P.from_id,P.predicate_id,P.predicate_code,P.to_id,
           P.direction,P.edge_id,CAST(NULL AS LONG),CAST(NULL AS VARCHAR(256)),
           CAST(NULL AS VARCHAR(1024)),CAST(NULL AS VARCHAR(256)),CAST(NULL AS TEXT),
           CAST(NULL AS VARCHAR(2048)),CAST(NULL AS VARCHAR(16)),CAST(NULL AS LONG),E.scope_json
    FROM path_steps P,
     seeds S,
     hits H,M89_G_EDGE E
WHERE (S.seed_id=P.seed_id)
  AND (H.chunk_id=P.chunk_id)
  AND (E.edge_id=P.edge_id AND E.kb_id=1)
UNION ALL

    SELECT 'EDGE_SOURCE',P.chunk_id,H.document_score,P.seed_id,S.seed_score,
           P.route_key,P.step_no,P.from_id,P.predicate_id,P.predicate_code,P.to_id,
           P.direction,P.edge_id,C.chunk_id,C.title,C.source_uri,C.locator,C.body,ES.quote,
           CAST(NULL AS VARCHAR(16)),CAST(NULL AS LONG),E.scope_json
    FROM path_steps P,
     seeds S,
     hits H,
     M89_G_EVIDENCE ES,M89_G_EDGE E,
     readable_chunks C
WHERE (S.seed_id=P.seed_id)
  AND (H.chunk_id=P.chunk_id)
  AND (ES.target_id=P.edge_id AND ES.target_kind='EDGE' AND ES.kb_id=1)
  AND (C.chunk_id=ES.chunk_id)
  AND (E.edge_id=P.edge_id AND E.kb_id=1)
)
SELECT *
FROM result_rows
ORDER BY document_score DESC,hit_chunk_id,seed_id,path_key,record_type,step_no,source_chunk_id;
```

</details>


### 결과를 읽는 방법

| record_type | 의미 |
|---|---|
| HIT | 검색된 문서 청크와 점수 |
| PATH | 해당 문서를 선택한 연결 이유와 원문 인용 |
| STEP | 대표 경로의 관계 ID·양 끝점·술어·F/R·scope_json |
| EDGE_SOURCE | 각 관계를 뒷받침하는 정확 인용과 원문 위치 |

이 fixture에서는 **HIT가201·202 두 개**입니다. 공개됐지만 연결되지 않은203은 그래프 후보에서 제외되고,204·205는 상태/버전 조건으로 제외됩니다. 현재 실행 결과 전체는8행(HIT2/PATH2/STEP2/EDGE_SOURCE2)입니다. `TOP_K=3`이 결과 집합 전체 행 수를3으로 제한한다는 뜻이 아닙니다.

후보 키의 중복 제거와 관계 근거 보존은 별개입니다. 문서 Top-K를 경로/근거 JOIN 이후에 적용하면 같은 문서의 여러 근거가 상위를 차지해 다른 문서가 빠질 수 있습니다. 이 SQL은 문서를 먼저 선택하고 그 문서의 대표 경로와 관계 근거를 연결합니다.

scope_json은 명제의 범위·조건·극성·대조 원문 등을 저장할 수 있는 앱 필드입니다. 저장만으로 조건의 논리 판정이 자동 수행되지는 않습니다. 이 실습은 같은 KB만 읽고 업무 ACL 테이블은 생략했습니다. 실제 서비스는 tenant/ACL도 그래프·원문·검색 후보의 허용 조건에 함께 적용합니다.

한 SQL 안의 재귀·원문 후보·검색은 문장 내 읽기 일관성의 대상입니다. 시작 개념 발견 SQL, 본 검색 SQL, 추가 명제 SQL처럼 **앱이 나눠 실행한 여러 문장을 하나의 snapshot으로 간주하지 않습니다.** 실제 예제의 빈 그래프 결과를 전체 문서 검색으로 보완할 때도 같은 권한 조건을 유지하고 GRAPH/DIRECT 출처를 구분합니다.

---

[이전: 개념·관계·근거 모델 만들기](../knowledge-model/) · [다음: Ollama로 근거 있는 답변 만들기](../ollama/)
