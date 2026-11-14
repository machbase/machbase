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
