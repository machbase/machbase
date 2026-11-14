---
type: docs
title: '11.9 운영과 성능 관리'
weight: 90
toc: true
---

검색과 관계 탐색을 서비스에 적용할 때 필요한 변경 반영, 읽기 일관성, 자원 관리와 복구 절차입니다.

- TRANSACTION 테이블의 INSERT/UPDATE/DELETE와 검색은 트랜잭션 수명을 따릅니다. 같은 세션의 미커밋 변경은 자신에게 보이고 다른 연결에는 COMMIT 후 새 읽기 snapshot에서 반영됩니다.
- READY BM25의 DML 변경은 원본과 같은 트랜잭션에 포함됩니다. 최초 구축/REBUILD는 백그라운드 작업입니다.
- HNSW/IVF 물리 파일 반영은 백그라운드이며, 검색은 같은 snapshot의 미반영 변경분과 현재 행을 확인합니다. COMMIT마다 REBUILD를 호출할 필요가 없습니다.
- 본문을 바꿔도 DB가 새 문장 벡터를 생성하지 않습니다. 새 본문과 같은 모델의 새 벡터를 함께 저장합니다.
- 문서 전체 교체는 새 청크 임베딩을 먼저 만든 뒤 BEGIN → tenant/doc_id 기존 청크 DELETE → 새 전체 청크 INSERT → COMMIT으로 처리합니다. 11.3절 replace 코드가 이 흐름입니다.
- `WAIT`/`REBUILD`는 사용자 트랜잭션 밖에서 호출합니다.

잠금 경합에 양수 대기 제한이 필요한 연결은 다음처럼 설정할 수 있습니다. 기본 `TRANSACTION_BUSY_TIMEOUT_MS=0`은 해제까지 기다리는 정책이며 로컬 conf의 명시적 양수가 이를 덮을 수 있습니다.

```sql
ALTER SESSION SET TRANSACTION_BUSY_TIMEOUT_MS=5000;
```

클라이언트 응답 timeout과 서버 transaction busy timeout은 다릅니다. 쓰기 응답을 못 받았다는 이유만으로 서버 rollback을 가정하지 말고 고유 ID/업무키로 실제 반영 여부를 확인한 뒤 재시도합니다.

## 검색 상태와 성능

### 상태를 먼저 확인

```sql
SELECT TABLE_NAME,INDEX_NAME,STATE,ERROR_CODE,LAST_ERROR
FROM V$TEXT_INDEXES WHERE TABLE_NAME='M89_DOCS';
SELECT TABLE_NAME,INDEX_NAME,INDEX_TYPE,STATE,BUILD_PHASE,
 PROCESSED_ROWS,PENDING_VECTOR_ROWS,LIST_COUNT,PROBE_COUNT,MEMORY_BYTES,PEAK_BYTES
FROM V$VECTOR_INDEXES WHERE TABLE_NAME='M89_DOCS';
SELECT POOL,LIMIT_BYTES,MEMORY_BYTES,PEAK_BYTES,OWNER_COUNT,ACTIVE_COUNT,
 RESERVED_BYTES,RETIRED_BYTES FROM V$VECTOR_IVF_MEMORY;
```

READY/BUILDING/REBUILDING/FAILED와 오류를 함께 봅니다. PENDING_VECTOR_ROWS는 물리 인덱스에 반영을 기다리는 벡터 행 수이며 파일 수가 아닙니다. READY 뒤에도 입력이 계속되면 pending이 생길 수 있습니다.

| 인덱스 | 생성 옵션과 기본값 | 변경 방법 |
|---|---|---|
| BM25 | ANALYZER='CJK_EN' 또는 'KO_EN' | analyzer 변경은 새 인덱스 생성 |
| HNSW | DISTANCE=COSINE, M=16(2~64), EF_CONSTRUCTION=200(M~4096), EF_SEARCH=100(1~10000), STORAGE_PRECISION=FLOAT32/FLOAT16 | 고정 옵션은 재생성 |
| IVF | DISTANCE=COSINE, LISTS 자동, PROBES=min(32,실제LISTS) | PROBES만 SET으로 동적 변경 |

```sql
ALTER INDEX M89_DOCS_VECTOR WAIT TIMEOUT 120;
ALTER INDEX M89_DOCS_VECTOR SET PROBES=2;
ALTER INDEX M89_DOCS_VECTOR REBUILD;
ALTER INDEX M89_DOCS_VECTOR WAIT TIMEOUT 120;
```

WAIT 기본은60초, TIMEOUT0은 즉시 상태 확인입니다. timeout은 구축 취소가 아닙니다. REBUILD 접수와 완료를 구분합니다. `CREATE INDEX IF NOT EXISTS`는 이름이 같으면 기존 정의를 유지할 뿐, 새 요청과 기존 거리/속성이 같은지 검증하지 않으므로 실제 관리 뷰를 확인하세요.

HNSW FLOAT16은 인덱스 표현이며 원본 VECTOR는 FLOAT32입니다. IVF LISTS 자동값은 `min(1024,ceil(sqrt(벡터 행 수)))`에서 예산에 맞게 정합니다. 명시 LISTS가1024 이하로 제한된다는 뜻은 아닙니다. 명시값을 자원 부족 때문에 조용히 낮추지 않습니다. PROBES는1~실제LISTS이며 변경에 REBUILD가 필요 없습니다. LISTS·HNSW M/EF를 ALTER SET으로 바꾸는 문법은 없습니다.

### 실제 경로와 비용

- `EXPLAIN`은 실행 전 계획입니다. `EXPLAIN FULL`은 실제 질의를 실행하므로 부하가 발생합니다.
- `BTREE_EXACT`는 조건 인덱스로 좁힌 행의 Exact 계산, `ANN_DIRECT`는 ANN 후보에서 시작하는 경로입니다. AUTO가 어느 경로였는지 먼저 확인합니다.
- `SOURCE_ROWS=0`은 해당 원본 전수 순회 카운터가0이라는 뜻입니다. 후보 원본 fetch·인덱스I/O·필터 검증이 없다는 뜻이 아닙니다.
- DELTA/EXACT_REFILL·IVF VISITS·FP64·BLOCK IO/CACHE는 변경분·보완·탐색량·캐시 영향을 보여 줍니다. BLOCK IO가 물리 SSD read와 같지는 않습니다.
- HNSW의 인덱스 가능한 FILTER는 B-tree Exact를 사용할 수 있습니다. IVF는 조건 선택도와 사전 탐색 예산을 보고 Exact/ANN을 결정합니다. 복잡한 FILTER에는 일반 평가 경로가 남습니다.
- `ORDER BY VECTOR_DISTANCE(...)` 일반 SQL이 ANN 사용을 자동 보장하지 않습니다. 검색 관계 VECTOR_SEARCH를 사용하세요.

### IVF 자원 예산

서버 시작 설정 `VECTOR_IVF_MEMORY_LIMIT=1073741824`의 기본은1GiB·최소1MiB입니다. 실행 중 ALTER SYSTEM으로 바꾸지 않습니다. 기본 BUILD512MiB/CACHE256MiB/SEARCH256MiB, 최대8개 active 검색과 기본 검색당32MiB 예산입니다.

이 값은 **IVF 전용 예산**이며 HNSW·원본 DB 버퍼·일반 SQL·OS 파일 캐시와 프로세스 RSS 전체 상한이 아닙니다. 학습 표본이 BUILD보다 크면 임시 디스크를 사용할 수 있고, 중심점/보조 배열의 최소 공간까지 부족하면 오류입니다. 큰 인덱스 구축에서는 정렬 stage와 새 검색 파일이 잠시 함께 존재하므로 최종 파일 크기 외에 디스크 여유를 확보합니다.

처음 검색의 파일 검증/로딩과 warm 반복 지연을 분리해서 측정합니다. 모델 추론 시간·DB execute+전체 fetch·rerank·LLM 생성 시간도 나눠 기록하세요.

## 백업과 호환성

### 도구 입출력

machsql은 VECTOR를 숫자 JSON으로 표시합니다. 다음은 client 측 format/CSV export입니다. 모델 없는11.1절 실습 뒤 실행할 수 있습니다.

```bash
machloader -s "$M89_HOST" -P "$M89_PORT" -u "$M89_USER" -p "$M89_PASSWORD" \
  -c -t M89_DOCS -f m89_docs.fmt -I
machloader -s "$M89_HOST" -P "$M89_PORT" -u "$M89_USER" -p "$M89_PASSWORD" \
  -o -f m89_docs.fmt -d m89_docs.csv -I
```

별도 새 실습 DB에 동일 schema/테이블을 준비했다면 같은 format으로 `-i -f m89_docs.fmt -d m89_docs.csv -I`를 사용합니다. CSV의 벡터 배열에는 쉼표가 있으므로 quoting을 유지하세요. format/CSV는 테이블 DDL·인덱스·SPACE 설정을 대신하지 않습니다. 값의 roundtrip은 출력 문자열 모양뿐 아니라 FLOAT32 값/NULL/차원을 확인합니다.

```sql
SAVE DATA INTO '/서버에서_쓰기_가능한_실습_절대경로/m89_docs.csv'
AS SELECT ID,TENANT,DOC_ID,BODY,V FROM M89_DOCS ORDER BY ID;
```

SAVE DATA 경로는 서버 측 파일시스템입니다. 원격 서버에 쓰인 파일을 클라이언트 현재 디렉터리에서 찾지 않습니다.

### 백업과 읽기 전용 MOUNT

새 백업 이름으로 실행합니다. 다음 경로는 서버가 해석하는 백업 경로입니다.

```sql
BACKUP DATABASE INTO DISK='m89_manual_backup';
MOUNT DATABASE 'm89_manual_backup' TO M89_BAK;
SELECT COUNT(*) AS BACKUP_ROWS FROM M89_BAK.SYS.M89_DOCS;
SELECT ID,BODY,VECTOR_DIM(V) AS DIM FROM M89_BAK.SYS.M89_DOCS ORDER BY ID;
UMOUNT DATABASE M89_BAK;
```

11.1절만 실행한 상태의 BACKUP_ROWS는6입니다. MOUNT는 읽기 전용이고 벡터 검색은 Exact 경로입니다. MOUNT에 REBUILD하지 않습니다. 물리 복원은 **같은 기능을 포함한 바이너리를 갖춘 새 독립 home**에 `machadmin -r 절대백업경로` 후 기동하는 흐름으로 진행하며, 복원할 DB를 미리 `-c`로 생성하거나 업무 DB를 덮지 않습니다. 복원 뒤 데이터와 색인 상태를 확인하고 WAIT합니다.

TRANSACTION 원본 데이터와 catalog의 백업을 확인하세요. BM25 자료는 원본 SQLite 파일에 포함됩니다. HNSW/IVF는 복원 후 원본에서 새 incarnation으로 재구축되므로 물리 파일을 live와 공유하지 않습니다. SQL catalog 논리 RESTORE를 검색 인덱스의 일반 물리 복원 대안으로 사용하지 않습니다.

### 호환성

| 항목 | 지원 내용 |
|---|---|
| DB 형식 | 7.0 |
| Standard metadata | 18. 검증된 기존17 DB의 기동 upgrade 지원 |
| native VECTOR | CMI4.0.5, VECTOR type173 |
| 신 SDK→검증된 구형4.0.4 서버 | 그 서버의 기존 SQL/ARRAY/DECIMAL 기능 유지, native VECTOR는 기능 부족 오류 |
| 구 SDK→신 서버 | VECTOR SQL 함수가 있는 서버라면 JSON 숫자 문자열/TO_VECTOR·VECTOR_TO_JSON 경로 사용 |

업그레이드는 원본 백업·복사본 확인 후 진행합니다. Meta18 DB를 구Meta17 실행 파일로 열거나, 구Meta17 backup을 MOUNT하는 일은 기동 자동 upgrade와 다릅니다. 새 SDK package를 설치해도 다른 경로의 구형 JAR/assembly/module을 읽을 수 있으므로 실제 import/classpath/assembly 위치를 확인하세요.

## 재귀 SQL 지원 범위

| 항목 | 현재 범위 |
|---|---|
| 재귀 구조 | anchor와직접 자기참조1개를 가진 recursive term, UNION/UNION ALL |
| 혼합 CTE | 같은 WITH RECURSIVE에 비재귀 CTE와 재귀 CTE를 함께 정의 가능 |
| 여러 consumer | 같은 재귀 producer의 누적 결과를 독립적으로 읽음 |
| 정수 | 반복 중 범위 축소를 피하도록 LONG/ULONG으로 승격;ID참조의 타입도 일치시킴 |
| DECIMAL | anchor의 precision/scale을 유지하고 재귀 값도 같은 도메인으로 CAST |
| 문자열 경로 | anchor/recursive term에 충분한 VARCHAR 폭을 명시. 긴 경로는 비용·잘림 여부 확인 |
| 재귀 UNION의 누적 중복 제거 | 정수·실수·DECIMAL·DATETIME·VARCHAR·BINARY·IP |
| 재귀 UNION의 제외 타입 | TEXT/CLOB/BLOB/JSON/ARRAY/VECTOR는 명시 오류 |
| UNION ALL payload | 누적 중복 제거 없음. 기존 행 운반이 지원하는 타입 범위이며 큰값/NULL/타입은 실제 쿼리로 확인 |

**지원하지 않는 범위:** 상호 재귀, producer의 외부 상관 참조, 재귀 term 안의 집계·윈도·정렬·LIMIT·서브쿼리, SEARCH/CYCLE, Cluster 전파. 최종 consumer나 비재귀 CTE의 기능까지 모두 금지한다는 뜻은 아닙니다. 예를 들어 최종 consumer의 GROUP BY/ORDER BY와 대표 경로 선택용 NOT EXISTS는 위 실습처럼 사용할 수 있습니다.

PostgreSQL의 모든 재귀 확장이나 SQL Server의 MAXRECURSION 옵션을 지원하는 것으로 해석하지 않습니다. 데모 CLI의 depth0~4 제한은 앱 정책이며 SQL 엔진의 전역 최대 반복 수가4라는 뜻이 아닙니다. parser의 CTE 전개 한도와 실행 중 재귀 반복·깊이도 다른 개념입니다.

## 읽기 일관성

재귀 문장에서 참조하는 TRANSACTION 파일들의 읽기 시점이 서로 섞이지 않도록 고정합니다. 읽기 상태를 잡지 못했을 때 부분 결과를 성공으로 반환하지 않습니다.

| 오류/상태 | 의미와 처리 |
|---|---|
| RECURSIVE_READ_CAPTURE | 읽기 상태 확보 경합. 변경 빈도·쿼리 범위·부하를 확인하고 앱 정책에 따라 재시도 |
| RECURSIVE_READ_CONTEXT | 이미 읽은 사용자 트랜잭션과 새 문장의 읽기 시점을 맞출 수 없음 |
| QUERY_TIMEOUT / 취소 | 쿼리를 실패로 처리하고 같은 요청의 일부 결과를 최종 답변에 쓰지 않음 |
| MAX_QPX_MEM 초과 | 범위·관계 유형·깊이·경로 폭을 줄이고 실행 메모리 확인 |
| 재귀 구문/타입 오류 | 실행하지 않은 branch나 빈 anchor라고 정적 오류를 무시하지 않음 |

`RECURSIVE_READ_CONTEXT`는 사용자의 미커밋 변경을 자동 rollback했다는 뜻이 아닙니다. 앱이 트랜잭션 종료/명시 ROLLBACK/재시도를 결정해야 합니다. 현재 일관성 epoch는 전역이어서 무관한 테이블 commit이나 실패한 commit 시도도 이미 시작한 사용자 트랜잭션과 보수적으로 충돌할 수 있습니다. BEGIN으로 묶었다는 이유만으로 경합이 사라진다고 가정하지 않습니다.

재귀 결과는 실행 메모리에 생성하며 디스크 spill을 지원하지 않습니다. 소비자의 LIMIT만으로 producer의 반복이 조기에 끝난다고 보장하지 않습니다. `UNION ALL`에는 종료 조건을 넣고, 순환뿐 아니라 분기·평행 관계 때문에 경로 수가 급증하는 경우도 고려합니다.

## 재귀 실행 계획

다음 두 문장을 별도로 실행합니다. FULL은 실제 쿼리를 실행하므로 계획 확인에도 부하가 발생할 수 있습니다.

```sql
EXPLAIN WITH RECURSIVE R(NODE_ID) AS (SELECT node_id FROM M89_G_NODE WHERE kb_id=1 AND node_id=2 UNION SELECT E.target_id FROM M89_G_EDGE E,R WHERE E.kb_id=1 AND E.state='APPROVED' AND E.source_id=R.node_id) SELECT NODE_ID FROM R ORDER BY NODE_ID;
EXPLAIN FULL WITH RECURSIVE R(NODE_ID) AS (SELECT node_id FROM M89_G_NODE WHERE kb_id=1 AND node_id=2 UNION SELECT E.target_id FROM M89_G_EDGE E,R WHERE E.kb_id=1 AND E.state='APPROVED' AND E.source_id=R.node_id) SELECT NODE_ID FROM R ORDER BY NODE_ID;
```

- 일반 EXPLAIN의 연산자 트리에서 `RECURSIVE CTE RESULT`/`WORK`, 실제 테이블의 INDEX/FULL SCAN과 key range를 확인합니다.
- FULL은 실행 통계를 제공합니다. 일부 경로는 프로파일만 반환하므로 FULL 출력에 FULL SCAN 문자열이 없다는 이유만으로 인덱스를 사용했다고 판단하지 않습니다.
- CTE 표시의 ITERATIONS/ROWS/DUPLICATES는 실제 실행 후의 값인지 확인합니다. 일반 EXPLAIN의0을 예상 cardinality로 해석하지 않습니다. UNION ALL의 DUPLICATES=0은 중복이 없다는 뜻이 아니라 그 중복을 집계하지 않는다는 뜻입니다.
- 같은 재귀 producer의 RESULT reader와 직전 작업 집합 WORK reader를 구분합니다. 일반 비재귀 CTE의 반복 인라인 전개 비용은 별도입니다.
- 관계의 정/역방향에 `(kb_id,source_id,predicate_id)`/`(kb_id,target_id,predicate_id)`, 근거에는 `(kb_id,target_kind,target_id,chunk_id)` 같은 인덱스가 유용합니다. 실제 key range가 ID까지 내려가는지 확인합니다.
- 인덱스 연산자가 보여도 전체 KB의 인덱스 범위를 반복 순회하면 느릴 수 있습니다. 접근 범위·SCAN open/fetch·전체 실행 시간을 함께 봅니다.
- EXACT 벡터 후보 점수화와 일반 구조 테이블의 FULL SCAN을 구분합니다. 입력 그래프·필터·문서량·질문을 고정하고 첫 실행과 warm 반복, execute부터전체fetch까지 측정합니다.
- EXPLAIN 공개 컬럼 폭은128바이트이며 표시 들여쓰기16을 넘는 깊이는 `[DEPTH=N]` 행으로 보존합니다. 계획 텍스트 파서는 이 표시를 고려합니다.

운영에서는 시작점 수·허용 관계·방향·깊이·방문 조건·선택 문서 수를 함께 제한합니다. 모든 경로를 출력한 뒤 줄이는 방식과, 필요한 후보/대표 경로만 남기는 방식은 비용이 다릅니다. 본 실습의 작은 그래프를 대규모 지연시간 보장으로 사용하지 않습니다.

---

[이전: 애플리케이션 연동](../application-integration/) · [다음: 문제 해결과 실습 정리](../troubleshooting/)
