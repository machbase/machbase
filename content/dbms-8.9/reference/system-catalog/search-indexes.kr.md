---
type: docs
title: '검색 인덱스 상태와 IVF 메모리'
weight: 60
toc: true
---

Standard Edition의 검색 인덱스와 IVF 자원을 조회하는 읽기 전용 뷰입니다.

## V$TEXT_INDEXES

BM25 인덱스의 상태를 반환합니다. 일반 B-tree는 포함하지 않습니다.

| 컬럼 | 타입 | 의미 |
|---|---|---|
| DATABASE_ID / TABLE_ID / INDEX_ID | LONG | 데이터베이스·테이블·인덱스 ID |
| USER_ID | INTEGER | 소유자 ID |
| DATABASE_NAME / TABLE_NAME / COLUMN_NAME / INDEX_NAME | VARCHAR | 객체 이름 |
| STATE | VARCHAR | BUILDING/READY/REBUILDING/FAILED |
| ANALYZER | VARCHAR | 텍스트 분석기 |
| ACTIVE_GENERATION | LONG | 공개된 검색 세대. 0이면 아직 공개한 세대 없음 |
| BUILD_GENERATION | LONG | 구축 중인 세대 |
| ERROR_CODE | INTEGER | 구축 오류 코드. 0이면 오류 없음 |
| LAST_ERROR | VARCHAR | 오류 메시지, 최대 1024바이트 |

```sql
SELECT TABLE_NAME,INDEX_NAME,STATE,ANALYZER,ACTIVE_GENERATION,
 BUILD_GENERATION,ERROR_CODE,LAST_ERROR FROM V$TEXT_INDEXES;
```

## V$VECTOR_INDEXES

HNSW·IVF 인덱스의 상태를 반환합니다. BM25와 B-tree는 포함하지 않습니다.

| 컬럼 | 타입 | 의미 |
|---|---|---|
| DATABASE_ID | LONG | 데이터베이스 ID |
| DATABASE_NAME | VARCHAR | 데이터베이스 이름 |
| USER_ID | INT | 소유자 ID |
| TABLE_ID | LONG | 테이블 ID |
| TABLE_NAME | VARCHAR | 테이블 이름 |
| COLUMN_NAME | VARCHAR | 대상 컬럼 |
| INDEX_ID | LONG | 인덱스 ID |
| INDEX_NAME | VARCHAR | 인덱스 이름 |
| STATE | VARCHAR | BUILDING/READY/REBUILDING/FAILED 상태 |
| METRIC | VARCHAR | 거리 방식 |
| DIMENSIONS | INT | 벡터 차원 |
| PRECISION | VARCHAR | 인덱스 저장 정밀도 |
| COMMITTED_SEQ | LONG | 커밋된 변경 순번 |
| INDEXED_SEQ | LONG | 인덱스가 반영한 변경 순번 |
| PENDING_VECTOR_ROWS | LONG | 현재 존재하는 non-NULL 미반영 벡터 행 수 |
| PENDING_VECTOR_BYTES | LONG | 미반영 벡터의 FLOAT32 원본 바이트 수 |
| SEGMENT_COUNT | LONG | 세그먼트 수 |
| REGISTERED_FILE_BYTES | LONG | manifest 등록 파일의 논리 크기 합계(바이트) |
| MEMORY_BYTES | LONG | 인덱스에 귀속된 현재 계측 메모리(바이트) |
| DISK_BYTES | LONG | 소유 파일 길이 합계(바이트). 귀속 불명으로 계산할 수 없으면 NULL |
| ACTIVE_GENERATION | LONG | 검색에 공개한 세대 |
| BUILD_GENERATION | LONG | 구축 중인 세대 |
| ERROR_CODE | INT | 구축 오류 코드. 0은 오류 없음 |
| LAST_ERROR | VARCHAR | 최근 구축 오류 정보, 최대 1024바이트 |
| INDEX_TYPE | VARCHAR | HNSW 또는 IVF |
| LIST_COUNT | INT | IVF 목록 수 |
| PROBE_COUNT | INT | IVF 탐색 목록 수 |
| BUILD_PHASE | VARCHAR | IVF 구축 단계 |
| PROCESSED_ROWS | LONG | IVF의 현재 원본 순회 처리 행 수 |
| PEAK_BYTES | LONG | IVF 귀속 메모리의 최고 동시 사용량(바이트). HNSW는 0 |

```sql
SELECT TABLE_NAME,INDEX_NAME,INDEX_TYPE,STATE,BUILD_PHASE,PROCESSED_ROWS,
 COMMITTED_SEQ,INDEXED_SEQ,PENDING_VECTOR_ROWS,MEMORY_BYTES,PEAK_BYTES
FROM V$VECTOR_INDEXES;
```

### 상태 해석

- READY라도 이후 변경으로 미반영 행이 생길 수 있습니다. 순번 차이는 미반영 행 수가 아닙니다.
- IVF BUILD_PHASE는 WAITING/PREPARE/SAMPLE/TRAIN/CREATE/WRITE/SEAL/VERIFY/PUBLISH,
  구축이 없으면 IDLE, 실패하면 FAILED, MOUNT에서는 DISABLED입니다.
- PROCESSED_ROWS는 전체 누적 진행률이 아닙니다. TRAIN은 SAMPLE의 값을 유지하고,
  WRITE 시작 전에 0으로 초기화합니다. WAITING/IDLE/FAILED/DISABLED에서는 0입니다.
  HNSW에는 IVF 진행 단계를 적용하지 않습니다.
- REGISTERED_FILE_BYTES는 등록 파일을 한 번씩 합산합니다. DISK_BYTES는 임시·잔존 파일도
  포함할 수 있습니다. 둘 다 디스크 할당 블록 수나 장치 전체 사용량은 아닙니다.
- MEMORY_BYTES는 RSS가 아닙니다. IVF의 PEAK_BYTES는 작업별 최고값의 합이 아니라
  인덱스 귀속 메모리의 최고 동시 사용량입니다. 같은 인덱스의 REBUILD로 초기화하지 않습니다.
- MOUNT는 백업 원본을 수정하지 않습니다. 인덱스 파일을 사용할 수 없으면 진단 상태와
  Exact 경로의 사용 이유를 확인하고, MOUNT에 REBUILD를 실행하지 않습니다.

<a id="ivf-memory"></a>

## V$VECTOR_IVF_MEMORY

TOTAL·BUILD·CACHE·SEARCH 풀별 메모리 상태를 반환합니다.

| 컬럼 | 타입 | 의미 |
|---|---|---|
| POOL | VARCHAR | 풀 이름 |
| LIMIT_BYTES | LONG | 풀의 예산(바이트) |
| MEMORY_BYTES | LONG | 현재 실제 계측 메모리(바이트) |
| PEAK_BYTES | LONG | 실제 계측 메모리의 최고값(바이트) |
| OWNER_COUNT | LONG | 잔존 할당을 포함한 메모리 소유 객체 수 |
| ACTIVE_COUNT | LONG | SEARCH의 활성 예약 수. BUILD/CACHE는 retire 전 소유 객체 수 |
| RESERVED_BYTES | LONG | 접수 예약과 종료 작업의 잔존 메모리(바이트) |
| RETIRED_BYTES | LONG | 작업 종료 뒤에도 남아 있는 메모리(바이트) |

```sql
SELECT POOL,LIMIT_BYTES,MEMORY_BYTES,PEAK_BYTES,OWNER_COUNT,ACTIVE_COUNT,
 RESERVED_BYTES,RETIRED_BYTES FROM V$VECTOR_IVF_MEMORY;
```

OWNER_COUNT는 SEARCH 동시 접수 한도 8을 넘을 수 있습니다. 종료된 작업의 할당이 남기
때문입니다. 예약량과 실제 사용량을 같은 값으로 해석하지 않습니다.
인덱스별 계측에 귀속하지 않는 공용 비용이 있어 인덱스별 합과 전역 합도 다를 수 있습니다.

## 조회 권한과 관측 시점

인덱스 상태 뷰는 조회 권한이 있는 객체를 표시하며, SYS는 전체 목록을 확인합니다.
사용자 트랜잭션의 과거 snapshot이나 미커밋 상태가 아니라 조회 시점의 커밋된 진단 상태를
읽습니다. 여러 파일의 단일 시점 snapshot을 보장하지 않으며 DROP·배타 DDL 중인 항목은
조회에서 제외될 수 있습니다. 진단 조회가 인덱스 설정을 변경하지는 않습니다.

- [IVF 메모리 설정](../../configuration/configuration/#vector_ivf_memory_limit)
- [검색 인덱스 생성과 변경](../../sql/syntax/index-syntax/#transaction-검색-인덱스)
