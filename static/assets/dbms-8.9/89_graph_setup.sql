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
