-- 1. 모델/테이블 없이 숫자 반복
WITH RECURSIVE R(N) AS (
 SELECT CAST(1 AS LONG)
 UNION ALL SELECT N+1 FROM R WHERE N<5
) SELECT N FROM R ORDER BY N;

-- 2. 베어링2에서 순방향: 1,2,3. 중복 edge와2↔3순환을 UNION이 제거한다.
WITH RECURSIVE R(NODE_ID) AS (
 SELECT node_id FROM M89_G_NODE WHERE kb_id=1 AND node_id=2
 UNION
 SELECT E.target_id FROM M89_G_EDGE E,R
 WHERE E.kb_id=1 AND E.state='APPROVED' AND E.source_id=R.node_id
) SELECT NODE_ID FROM R ORDER BY NODE_ID;

-- 3. UNION ALL의 깊이 제한: 깊이0/1/2에1/3/1행
WITH RECURSIVE R(NODE_ID,DEPTH) AS (
 SELECT node_id,CAST(0 AS LONG) FROM M89_G_NODE WHERE kb_id=1 AND node_id=2
 UNION ALL
 SELECT E.target_id,R.depth+1 FROM M89_G_EDGE E,R
 WHERE E.kb_id=1 AND E.state='APPROVED' AND E.source_id=R.node_id AND R.depth<2
) SELECT DEPTH,COUNT(*) AS ROWS_AT_DEPTH FROM R GROUP BY DEPTH ORDER BY DEPTH;

-- 4. 빈 anchor: 0행
WITH RECURSIVE R(NODE_ID) AS (
 SELECT node_id FROM M89_G_NODE WHERE kb_id=1 AND node_id=999
 UNION SELECT E.target_id FROM M89_G_EDGE E,R
 WHERE E.kb_id=1 AND E.state='APPROVED' AND E.source_id=R.node_id
) SELECT COUNT(*) AS REACHABLE FROM R;

-- 5. 같은 재귀 결과를 두 consumer에서 사용
WITH RECURSIVE R(N) AS (
 SELECT CAST(1 AS LONG) UNION ALL SELECT N+1 FROM R WHERE N<3
) SELECT A.N AS A,B.N AS B FROM R A,R B WHERE A.N=B.N ORDER BY A.N;

-- 6. DECIMAL의 precision/scale을 명시
WITH RECURSIVE R(N) AS (
 SELECT CAST(1 AS DECIMAL(12,2))
 UNION ALL SELECT CAST(N+0.25 AS DECIMAL(12,2)) FROM R WHERE N<1.50
) SELECT N FROM R ORDER BY N;

-- 7. 양방향 탐색: node 재방문 차단 + 원래 edge 방향F/R 보존
WITH RECURSIVE
ARCS AS (
 SELECT edge_id,source_id AS from_id,target_id AS to_id,'F' AS direction
 FROM M89_G_EDGE WHERE kb_id=1 AND state='APPROVED'
 UNION ALL
 SELECT edge_id,target_id AS from_id,source_id AS to_id,'R' AS direction
 FROM M89_G_EDGE WHERE kb_id=1 AND state='APPROVED'
),
W(NODE_ID,DEPTH,NODE_PATH,EDGE_PATH) AS (
 SELECT node_id,CAST(0 AS LONG),
        CAST('|' || CAST(node_id AS VARCHAR(20)) || '|' AS VARCHAR(1024)),
        CAST('@' AS VARCHAR(1024))
 FROM M89_G_NODE WHERE kb_id=1 AND node_id=1
 UNION ALL
 SELECT A.to_id,W.depth+1,
        CAST(W.node_path || CAST(A.to_id AS VARCHAR(20)) || '|' AS VARCHAR(1024)),
        CAST(W.edge_path || '/' || CAST(A.edge_id AS VARCHAR(20)) || A.direction AS VARCHAR(1024))
 FROM W,ARCS A
 WHERE A.from_id=W.node_id AND W.depth<2
   AND INSTR(W.node_path,'|' || CAST(A.to_id AS VARCHAR(20)) || '|')=0
)
SELECT NODE_ID,DEPTH,NODE_PATH,EDGE_PATH FROM W ORDER BY DEPTH,NODE_ID,EDGE_PATH;

-- 8. 역방향 PART_OF만 조회: 펌프1과 그 구성품2
WITH RECURSIVE R(NODE_ID) AS (
 SELECT node_id FROM M89_G_NODE WHERE kb_id=1 AND node_id=1
 UNION
 SELECT E.source_id FROM R,M89_G_EDGE E
 WHERE E.kb_id=1 AND E.state='APPROVED' AND E.predicate_id=1001 AND E.target_id=R.node_id
) SELECT NODE_ID FROM R ORDER BY NODE_ID;
