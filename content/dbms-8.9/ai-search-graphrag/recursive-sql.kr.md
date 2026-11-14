---
type: docs
title: '11.4 재귀 SQL로 관계 탐색하기'
weight: 40
toc: true
---

재귀 CTE는 직전 반복 결과를 다음 반복의 입력으로 사용합니다. 첫 숫자 반복은 테이블 없이 실행할 수 있습니다. 관계 탐색 예제는 [그래프 실습 데이터](../knowledge-model/)를 준비한 뒤 실행합니다.

```sql
WITH RECURSIVE cte_name(col1, col2) AS (
    -- 첫 작업 집합: anchor
    SELECT ...
    UNION ALL
    -- 직전 작업 집합을 읽는 recursive term
    SELECT ... FROM cte_name ... WHERE ...
)
SELECT ... FROM cte_name;
```

위 블록의 `...`는 문법 설명용이며 그대로 실행하지 않습니다. 다음 숫자 예제부터 실행 가능한 SQL입니다.

1. anchor를 실행해 첫 작업 집합을 만듭니다.
2. 재귀 term이 직전 작업 집합을 읽어 다음 작업 집합을 만듭니다.
3. 다음 작업 집합이 비면 종료합니다.
4. 최종 SELECT가 누적 결과를 읽습니다. 표시 순서가 필요하면 최종 `ORDER BY`를 지정합니다.

| 연결 연산 | 동작 | 순환에서 주의할 점 |
|---|---|---|
| `UNION` | 이미 누적한 **전체 출력 튜플**과 같은 행은 다시 추가하지 않음 | node_id만 출력하면 같은 노드의 재방문이 제거됨 |
| `UNION ALL` | 중복을 그대로 추가 | 깊이·방문 경로·업무 조건으로 종료를 작성해야 함 |

`UNION`에 `(node_id,depth)`를 출력하면 `(2,0)`과 `(2,2)`는 다른 튜플입니다. 깊이가 계속 늘어나는 순환은 `UNION`이라고 자동 종료되지 않습니다. NULL도 집합 중복 제거의 대상이며, 미지정 타입의 NULL보다 `CAST(NULL AS LONG)`처럼 타입을 명시하는 편이 안전합니다.

anchor와 재귀 term의 열 수·순서를 맞추고 타입을 호환되게 작성합니다. 문자열 경로와 DECIMAL은 아래처럼 양쪽의 폭·정밀도를 명시합니다. 재귀 CTE를 같은 문장에서 여러 번 읽으면 그 producer의 결과를 공유합니다. 일반 비재귀 CTE까지 항상 한 번 물리화된다는 뜻은 아닙니다.

## 관계 탐색 실습

[관계 탐색 SQL 다운로드](/assets/dbms-8.9/89_recursive_queries.sql)

다음 블록은 설정 파일을 실행한 뒤 `89_recursive_queries.sql`로 실행합니다. 첫 숫자 반복은 테이블 없이도 실행할 수 있습니다. 다른 기본 순회 예제는 재귀 문법을 설명하는 것이며 서비스용 문서 권한·버전 필터는 11.6절의 전체 검색 SQL을 사용합니다.

[전체 코드 다운로드: example-4-1.sql](/assets/dbms-8.9/example-4-1.sql)

<details>
<summary>전체 코드 보기</summary>

```sql
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
```

</details>

### 결과 확인

| 예제 | 확인할 결과 |
|---|---|
| 숫자 반복 | 1,2,3,4,5 |
| 순방향 UNION | 노드1,2,3. 평행 edge와2↔3순환이 누적 중복으로 제거됨 |
| 깊이2의 UNION ALL | 깊이0/1/2의 행 수는1/3/1. 같은 노드의 여러 경로를 유지함 |
| 없는 시작점999 | COUNT=0 |
| 두 consumer | (1,1),(2,2),(3,3) |
| DECIMAL | 1,1.25,1.5. DECIMAL(12,2) 도메인 유지 |
| 양방향 경로 | 9개 경로, 서로 다른 노드는1·2·3·4. 한 경로 안의 노드 재방문 없음 |
| 역방향 PART_OF | 펌프1과 구성품2 |

NODE_PATH의 `|1|` 같은 구분자는1과11을 혼동하지 않게 합니다. `INSTR` 검사는 현재 경로의 재방문만 차단하며, 서로 다른 경로로 같은 노드에 도달하는 것은 유지합니다. EDGE_PATH에는 관계 ID와 원래 방향F/R을 남깁니다.

F는 저장된 source→target 방향, R은 반대 방향으로 **탐색했다는 표시**입니다. R로 이동했다고 원래 명제의 의미를 뒤집지 않습니다. 예를 들어 펌프에서 베어링으로 역방향 이동해도 원문 명제는 여전히 `베어링 PART_OF 펌프`입니다.

최단 경로를 하나만 보여 주려면 최종 결과에서 깊이와 안정된 경로 키로 대표를 선택합니다. 최단 노드 하나를 찾는 일과 모든 경로를 열거하는 일은 비용·결과가 다릅니다. 11.6절은 문서별 대표 경로를 선택합니다.

---

[이전: 내 문서로 검색과 RAG 만들기](../document-rag/) · [다음: 개념·관계·근거 모델 만들기](../knowledge-model/)
