---
type: docs
title: '11.5 개념·관계·근거 모델 만들기'
weight: 50
toc: true
---

문서에서 추출한 개념과 관계를 원문 근거에 연결합니다. 전용 GRAPH 테이블이 아니라 일반 TRANSACTION 테이블을 사용합니다.

`WITH RECURSIVE`는 이전 반복에서 찾은 행을 다음 반복의 입력으로 사용합니다. 조직·부품 계층, 관계망의 도달 가능 노드, 경로를 SQL로 구할 수 있습니다. 온톨로지 RAG에서는 질문과 연결되는 개념에서 관계를 따라가 관련 원문 후보를 정합니다.

```text
사용자 질문
 → 이름·별칭 확인 / 개념 설명의 의미 검색 ()
 → 시작 개념의 실제 ID 결정
 → 관계·방향·깊이·순환 조건으로 탐색 ()
 → 노드·관계의 근거 청크 집합
 → 후보 집합 안에서 Hybrid 문서 검색 ()
 → 문서·연결 경로·관계 원문
 → 외부 LLM의 답변과 인용
```

- 대상은 **Standard TRANSACTION SELECT**입니다. Cluster, LOG/TAG의 재귀 실행까지 지원한다는 뜻이 아닙니다.
- 그래프는 일반 사용자 테이블에 저장합니다. 전용 GRAPH 테이블 생성이나 그래프 등록이 필요하지 않습니다.
- 관계 코드·개념 분류·별칭·근거는 사용자 데이터입니다. SQL 엔진이 `PART_OF` 같은 관계 코드의 의미를 이해하거나 OWL 규칙을 자동 추론하는 기능은 아닙니다.
- 아래 5개 테이블은 실습용 스키마입니다. 기존 문서·청크 저장소가 있다면 노드·관계·근거를 연결해 재사용할 수 있습니다.

## 실습 준비

DBMS 8.9 Standard **전용 실습 서버**를 준비합니다. 이미 실행 중이면 DB 생성·서버 시작을 반복할 필요 없습니다. 기존 업무 객체와 이름이 충돌하지 않는지 확인합니다. 아래 SQL은 파일로 저장한 뒤 반드시 `machsql -f`로 실행합니다.

```bash
export MACHBASE_HOME=/opt/machbase89-lab
export PATH="$MACHBASE_HOME/bin:$PATH"
export M89_HOST=127.0.0.1 M89_PORT=5656 M89_USER=SYS
read -rsp '실습 DB 비밀번호: ' M89_PASSWORD
export M89_PASSWORD
printf '\n'

machsql -s "$M89_HOST" -P "$M89_PORT" -u "$M89_USER" \
  -p "$M89_PASSWORD" -f 89_graph_setup.sql
```

예제의 `M89_G_` 객체는 모두 이 장에서 새로 만드는 실습용입니다. 임의 업무 테이블을 삭제해 이름 충돌을 해결하지 않습니다. 벡터3개 숫자는 SQL 동작을 확인하는 **합성값**이며 문장 의미 임베딩이나 검색 정확도 인증 자료가 아닙니다.

### 실습의 5개 테이블

| 테이블 | 역할 | 입력 행 수 |
|---|---|---:|
| M89_G_DOCUMENT | 문서 제목·출처·현재 버전·공개 상태 | 4 |
| M89_G_CHUNK | 원문·위치·문서 버전·VECTOR(3) | 5 |
| M89_G_NODE | 개념·별칭·관계 유형 | 9 |
| M89_G_EDGE | source/predicate/target와 승인 상태·범위 | 5 |
| M89_G_EVIDENCE | NODE/EDGE와 원문 청크·정확 인용 연결 | 13 |

내부 ID·참조·kb_id는 LONG(INT64)입니다. NODE의9행은 ENTITY5개, RELATION_TYPE3개, ALIAS1개입니다. ALIAS의 canonical_id가 정규 개념을 가리키므로 별칭마다 개념을 복제하지 않습니다. predicate_id도 NODE의 RELATION_TYPE 행을 가리킵니다. 이름·코드·URI는 문자열로 보존합니다.

```text
베어링2 ── PART_OF ──→ 펌프1
베어링2 ── RELATED_TO ──→ 진동3
진동3   ── RELATED_TO ──→ 베어링2       (순환)
점검절차4 ── APPLIES_TO ──→ 베어링2
모터5                                     (연결 없음)
```

PART_OF 관계101과105는 일부러 같은 두 노드를 연결한 평행 관계입니다. 문서30은 미공개이고, 문서40의 청크는 현재 버전2보다 오래된 버전1입니다. 아래 데이터는 실제 설비를 판정하는 지식이 아닌 학습용 가상 그래프입니다.


[전체 코드 다운로드: 89_graph_setup.sql](/assets/dbms-8.9/89_graph_setup.sql)

<details>
<summary>전체 코드 보기</summary>

```sql
-- 새 전용 실습 DB에서 한번 실행한다. 기존 M89_G_ 객체가 있으면 중단한다.
CREATE TRANSACTION TABLE M89_G_DOCUMENT (
    document_id LONG PRIMARY KEY,
    kb_id LONG NOT NULL,
    title VARCHAR(256) NOT NULL,
    source_uri VARCHAR(1024) NOT NULL,
    current_version LONG NOT NULL,
    state VARCHAR(16) NOT NULL,
    external_key VARCHAR(256)
);

CREATE TRANSACTION TABLE M89_G_CHUNK (
    chunk_id LONG PRIMARY KEY,
    kb_id LONG NOT NULL,
    document_id LONG NOT NULL,
    document_version LONG NOT NULL,
    ordinal INTEGER NOT NULL,
    locator VARCHAR(256) NOT NULL,
    body TEXT NOT NULL,
    embedding VECTOR(3) PROPERTY(EMBEDDING_SPACE='m89-g-chunk-v1'),
    analysis_state VARCHAR(16) NOT NULL,
    extractor_version VARCHAR(128),
    fact_count INTEGER
);

CREATE TRANSACTION TABLE M89_G_NODE (
    node_id LONG PRIMARY KEY,
    kb_id LONG NOT NULL,
    node_kind VARCHAR(16) NOT NULL,
    label VARCHAR(256) NOT NULL,
    code VARCHAR(64),
    description VARCHAR(2048),
    search_text TEXT,
    state VARCHAR(16) NOT NULL,
    embedding VECTOR(3) PROPERTY(EMBEDDING_SPACE='m89-g-node-v1'),
    canonical_id LONG,
    label_key VARCHAR(256),
    source_kind VARCHAR(16),
    target_kind VARCHAR(16)
);

CREATE TRANSACTION TABLE M89_G_EDGE (
    edge_id LONG PRIMARY KEY,
    kb_id LONG NOT NULL,
    source_id LONG,
    predicate_id LONG,
    target_id LONG,
    state VARCHAR(16) NOT NULL,
    subject_text VARCHAR(256),
    predicate_text VARCHAR(128),
    object_text VARCHAR(256),
    extractor_version VARCHAR(128),
    canonical_edge_id LONG,
    scope_json TEXT
);

CREATE TRANSACTION TABLE M89_G_EVIDENCE (
    evidence_id LONG PRIMARY KEY,
    kb_id LONG NOT NULL,
    target_kind VARCHAR(8) NOT NULL,
    target_id LONG NOT NULL,
    chunk_id LONG NOT NULL,
    quote VARCHAR(2048) NOT NULL
);

CREATE INDEX M89_G_NODE_ALIAS_LOOKUP ON M89_G_NODE(kb_id,node_kind,label_key) INDEX_TYPE BTREE;
CREATE INDEX M89_G_NODE_KIND ON M89_G_NODE(kb_id,node_kind) INDEX_TYPE BTREE;
CREATE INDEX M89_G_NODE_CODE ON M89_G_NODE(kb_id,node_kind,code) INDEX_TYPE BTREE;
CREATE INDEX M89_G_EDGE_OUT ON M89_G_EDGE(kb_id,source_id,predicate_id) INDEX_TYPE BTREE;
CREATE INDEX M89_G_EDGE_IN ON M89_G_EDGE(kb_id,target_id,predicate_id) INDEX_TYPE BTREE;
CREATE INDEX M89_G_EVIDENCE_TARGET ON M89_G_EVIDENCE(kb_id,target_kind,target_id,chunk_id) INDEX_TYPE BTREE;
CREATE INDEX M89_G_EVIDENCE_CHUNK ON M89_G_EVIDENCE(kb_id,chunk_id,target_kind,target_id) INDEX_TYPE BTREE;
CREATE INDEX M89_G_CHUNK_DOCUMENT ON M89_G_CHUNK(kb_id,document_id,document_version) INDEX_TYPE BTREE;

CREATE INDEX M89_G_NODE_BM25 ON M89_G_NODE(search_text) INDEX_TYPE BM25 ANALYZER='CJK_EN';
CREATE INDEX M89_G_CHUNK_BM25 ON M89_G_CHUNK(body) INDEX_TYPE BM25 ANALYZER='CJK_EN';
ALTER INDEX M89_G_NODE_BM25 WAIT TIMEOUT 60;
ALTER INDEX M89_G_CHUNK_BM25 WAIT TIMEOUT 60;

INSERT INTO M89_G_DOCUMENT VALUES(10,1,'펌프 점검','lab:pump',1,'PUBLISHED','pump');
INSERT INTO M89_G_DOCUMENT VALUES(20,1,'모터 점검','lab:motor',1,'PUBLISHED','motor');
INSERT INTO M89_G_DOCUMENT VALUES(30,1,'미공개 초안','lab:draft',1,'DRAFT','draft');
INSERT INTO M89_G_DOCUMENT VALUES(40,1,'개정 문서','lab:version',2,'PUBLISHED','version');
INSERT INTO M89_G_CHUNK(chunk_id,kb_id,document_id,document_version,ordinal,locator,body,embedding,analysis_state)
VALUES(201,1,10,1,1,'paragraph-201','펌프 P-101은 베어링을 포함한다. 베어링은 펌프의 일부이다.',TO_VECTOR('[1,0,0]',3),'COMPLETE');
INSERT INTO M89_G_CHUNK(chunk_id,kb_id,document_id,document_version,ordinal,locator,body,embedding,analysis_state)
VALUES(202,1,10,1,2,'paragraph-202','베어링 진동은 베어링과 관련된다. 진동 점검 절차는 베어링에 적용된다.',TO_VECTOR('[0.8,0.2,0]',3),'COMPLETE');
INSERT INTO M89_G_CHUNK(chunk_id,kb_id,document_id,document_version,ordinal,locator,body,embedding,analysis_state)
VALUES(203,1,20,1,1,'paragraph-203','모터 절연 점검 절차.',TO_VECTOR('[0,1,0]',3),'COMPLETE');
INSERT INTO M89_G_CHUNK(chunk_id,kb_id,document_id,document_version,ordinal,locator,body,embedding,analysis_state)
VALUES(204,1,30,1,1,'paragraph-204','펌프 진동 미공개 초안.',TO_VECTOR('[1,0,0]',3),'COMPLETE');
INSERT INTO M89_G_CHUNK(chunk_id,kb_id,document_id,document_version,ordinal,locator,body,embedding,analysis_state)
VALUES(205,1,40,1,1,'paragraph-205','펌프 진동 이전 버전.',TO_VECTOR('[1,0,0]',3),'COMPLETE');
INSERT INTO M89_G_NODE(node_id,kb_id,node_kind,label,code,description,search_text,state,embedding,label_key)
VALUES(1,1,'ENTITY','펌프 P-101','P101','펌프 P-101','펌프 P-101','PUBLISHED',TO_VECTOR('[1,0,0]',3),'펌프 p-101');
INSERT INTO M89_G_NODE(node_id,kb_id,node_kind,label,code,description,search_text,state,embedding,label_key)
VALUES(2,1,'ENTITY','베어링','BEARING','베어링','베어링','PUBLISHED',TO_VECTOR('[0.8,0.2,0]',3),'베어링');
INSERT INTO M89_G_NODE(node_id,kb_id,node_kind,label,code,description,search_text,state,embedding,label_key)
VALUES(3,1,'ENTITY','베어링 진동','VIBRATION','베어링 진동','베어링 진동','PUBLISHED',TO_VECTOR('[0.7,0.3,0]',3),'베어링 진동');
INSERT INTO M89_G_NODE(node_id,kb_id,node_kind,label,code,description,search_text,state,embedding,label_key)
VALUES(4,1,'ENTITY','진동 점검 절차','CHECK','진동 점검 절차','진동 점검 절차','PUBLISHED',TO_VECTOR('[0.6,0.4,0]',3),'진동 점검 절차');
INSERT INTO M89_G_NODE(node_id,kb_id,node_kind,label,code,description,search_text,state,embedding,label_key)
VALUES(5,1,'ENTITY','모터','MOTOR','모터','모터','PUBLISHED',TO_VECTOR('[0,1,0]',3),'모터');
INSERT INTO M89_G_NODE(node_id,kb_id,node_kind,label,code,state,source_kind,target_kind)
VALUES(1001,1,'RELATION_TYPE','PART_OF','PART_OF','PUBLISHED','ENTITY','ENTITY');
INSERT INTO M89_G_NODE(node_id,kb_id,node_kind,label,code,state,source_kind,target_kind)
VALUES(1002,1,'RELATION_TYPE','RELATED_TO','RELATED_TO','PUBLISHED','ENTITY','ENTITY');
INSERT INTO M89_G_NODE(node_id,kb_id,node_kind,label,code,state,source_kind,target_kind)
VALUES(1003,1,'RELATION_TYPE','APPLIES_TO','APPLIES_TO','PUBLISHED','ENTITY','ENTITY');
INSERT INTO M89_G_NODE(node_id,kb_id,node_kind,label,state,canonical_id,label_key)
VALUES(2001,1,'ALIAS','P101','PUBLISHED',1,'p101');
INSERT INTO M89_G_EDGE(edge_id,kb_id,source_id,predicate_id,target_id,state,scope_json)
VALUES(101,1,2,1001,1,'APPROVED','{"assertion":"펌프 P-101은 베어링을 포함한다. 베어링은 펌프의 일부이다.","conditions":[],"polarity":"affirmative"}');
INSERT INTO M89_G_EDGE(edge_id,kb_id,source_id,predicate_id,target_id,state,scope_json)
VALUES(102,1,2,1002,3,'APPROVED','{"assertion":"베어링 진동은 베어링과 관련된다. 진동 점검 절차는 베어링에 적용된다.","conditions":[],"polarity":"affirmative"}');
INSERT INTO M89_G_EDGE(edge_id,kb_id,source_id,predicate_id,target_id,state,scope_json)
VALUES(103,1,3,1002,2,'APPROVED','{"assertion":"베어링 진동은 베어링과 관련된다. 진동 점검 절차는 베어링에 적용된다.","conditions":[],"polarity":"affirmative"}');
INSERT INTO M89_G_EDGE(edge_id,kb_id,source_id,predicate_id,target_id,state,scope_json)
VALUES(104,1,4,1003,2,'APPROVED','{"assertion":"베어링 진동은 베어링과 관련된다. 진동 점검 절차는 베어링에 적용된다.","conditions":[],"polarity":"affirmative"}');
INSERT INTO M89_G_EDGE(edge_id,kb_id,source_id,predicate_id,target_id,state,scope_json)
VALUES(105,1,2,1001,1,'APPROVED','{"assertion":"펌프 P-101은 베어링을 포함한다. 베어링은 펌프의 일부이다.","conditions":[],"polarity":"affirmative"}');
INSERT INTO M89_G_EVIDENCE VALUES(401,1,'NODE',1,201,'펌프 P-101은 베어링을 포함한다. 베어링은 펌프의 일부이다.');
INSERT INTO M89_G_EVIDENCE VALUES(402,1,'NODE',2,201,'펌프 P-101은 베어링을 포함한다. 베어링은 펌프의 일부이다.');
INSERT INTO M89_G_EVIDENCE VALUES(403,1,'NODE',3,202,'베어링 진동은 베어링과 관련된다. 진동 점검 절차는 베어링에 적용된다.');
INSERT INTO M89_G_EVIDENCE VALUES(404,1,'NODE',4,202,'베어링 진동은 베어링과 관련된다. 진동 점검 절차는 베어링에 적용된다.');
INSERT INTO M89_G_EVIDENCE VALUES(405,1,'NODE',5,203,'모터 절연 점검 절차.');
INSERT INTO M89_G_EVIDENCE VALUES(406,1,'NODE',2001,201,'펌프 P-101은 베어링을 포함한다. 베어링은 펌프의 일부이다.');
INSERT INTO M89_G_EVIDENCE VALUES(407,1,'NODE',1,204,'펌프 진동 미공개 초안.');
INSERT INTO M89_G_EVIDENCE VALUES(408,1,'NODE',1,205,'펌프 진동 이전 버전.');
INSERT INTO M89_G_EVIDENCE VALUES(501,1,'EDGE',101,201,'펌프 P-101은 베어링을 포함한다. 베어링은 펌프의 일부이다.');
INSERT INTO M89_G_EVIDENCE VALUES(502,1,'EDGE',102,202,'베어링 진동은 베어링과 관련된다. 진동 점검 절차는 베어링에 적용된다.');
INSERT INTO M89_G_EVIDENCE VALUES(503,1,'EDGE',103,202,'베어링 진동은 베어링과 관련된다. 진동 점검 절차는 베어링에 적용된다.');
INSERT INTO M89_G_EVIDENCE VALUES(504,1,'EDGE',104,202,'베어링 진동은 베어링과 관련된다. 진동 점검 절차는 베어링에 적용된다.');
INSERT INTO M89_G_EVIDENCE VALUES(505,1,'EDGE',105,201,'펌프 P-101은 베어링을 포함한다. 베어링은 펌프의 일부이다.');
ALTER INDEX M89_G_NODE_BM25 WAIT TIMEOUT 60;
ALTER INDEX M89_G_CHUNK_BM25 WAIT TIMEOUT 60;
```

</details>


스키마의 PK/NOT NULL과 인덱스가 모든 온톨로지 의미 제약을 강제하지는 않습니다. 노드·관계의 KB 일치, 술어의 source_kind/target_kind, 근거 인용, 승인·문서 버전은 적재기와 검색 SQL에서 검사해야 합니다. 문서·관계별 근거를 빼고 유사한 단어만 연결하는 것으로 온톨로지 검증을 대신하지 않습니다.

---

[이전: 재귀 SQL로 관계 탐색하기](../recursive-sql/) · [다음: 관계를 활용한 GraphRAG 검색](../graph-search/)
