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
