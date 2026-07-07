---
type: docs
title: '인덱싱 기본 원리'
weight: 30
---

Machbase는 테이블 유형에 따라 서로 다른 인덱스 구조를 사용합니다. 어떤 인덱스가 어떤 조회 패턴에 적합한지 이해하면, 불필요한 인덱스 생성을 피하고 최적의 조회 성능을 달성할 수 있습니다.

## TAG 테이블: 자동 3단계 파티션 인덱스

TAG 테이블은 별도의 `CREATE INDEX` 없이도 자동으로 3단계 인덱스를 구성합니다.

```
태그명 (PRIMARY KEY)
  └──► 시간 파티션 범위
          └──► 파티션 내 컬럼 값
```

"sensor_A의 2026-07-03 데이터"를 조회하면 먼저 태그명으로 해당 태그의 파티션 목록을 찾고, 시간 범위로 대상 파티션을 좁힌 뒤, 그 파티션에서 컬럼 값을 읽습니다. 대규모 TAG 테이블에서 태그명과 시간 범위가 명시된 조회는 항상 이 경로를 통해 최소한의 I/O로 처리됩니다.

## LOG 테이블: LSM 인덱스 (선택적 생성)

LOG 테이블은 기본적으로 `_arrival_time` 기준의 순차 저장 구조를 사용합니다. `_arrival_time`을 조건으로 사용하면 파티션 pruning으로 해당 시간 범위만 스캔합니다.

특정 컬럼에 빠른 조회가 필요하면 LSM(Log-Structured Merge-tree) 인덱스를 명시적으로 생성합니다.

```sql
-- LOG 테이블의 device_id 컬럼에 인덱스 생성
CREATE INDEX idx_device ON device_log (device_id);
```

LSM 인덱스는 삽입 시 메모리 내 구조에 먼저 기록되고, 배경 스레드가 주기적으로 디스크의 정렬된 파일로 병합합니다. 순차 삽입이 많은 환경에서 B-Tree보다 삽입 성능이 우수합니다. 단, 데이터 병합 중에 I/O 부하가 일시 증가할 수 있습니다.

**KEYWORD 인덱스**: 긴 텍스트 컬럼에서 단어 검색이 필요한 경우 사용합니다.

```sql
CREATE INDEX idx_msg ON device_log (message) INDEX_TYPE KEYWORD;
```

## LOOKUP 테이블: B-Tree 인덱스

LOOKUP 테이블은 RDBMS와 유사하게 PRIMARY KEY에 B-Tree 인덱스가 자동으로 생성됩니다. 소규모 기준 정보를 키로 빠르게 조회하는 패턴에 최적화되어 있습니다.

## VOLATILE 테이블: Red-Black 트리 인덱스

VOLATILE 테이블은 메모리 기반 테이블로, PRIMARY KEY 컬럼에 자동으로 Red-Black 트리 인덱스가 생성됩니다. 메모리에서 동작하므로 삽입과 조회 모두 매우 빠르지만, 서버 재시작 시 데이터가 사라집니다.

## 인덱스를 만들어야 할 때와 만들지 말아야 할 때

**인덱스가 유용한 경우**

- LOG 테이블에서 `_arrival_time` 이외의 컬럼(예: 장치 ID, 이벤트 유형)으로 자주 필터링하는 경우
- 텍스트 컬럼에서 특정 단어를 포함하는 행을 검색하는 경우 (KEYWORD 인덱스)

**인덱스 생성을 피해야 하는 경우**

- 입력 속도가 최우선이고 조회 빈도가 낮은 경우 (인덱스 유지 오버헤드 발생)
- 카디널리티가 낮은 컬럼 (예: TRUE/FALSE 구분값) — 인덱스 효과가 없음
- TAG 테이블 — 이미 자동 파티션 인덱스가 있으므로 추가 인덱스는 불필요

## 다음 읽을 내용

- [컬럼형 저장과 압축](../storage-columnar-compression-column/) — 인덱스가 동작하는 저장 구조
- [Cache와 실행 계획 개념](../execution-concepts-plan-cache/) — 인덱스를 활용하는 실행 계획 최적화
- [Machbase 아키텍처 개요](../architecture-machbase/) — 인덱스와 저장 관리자의 관계

## Min-Max Cache

### 개념

Machbase는 시계열 데이터를 시간순으로 파티션된 구조로 저장합니다. 특정 값을 인덱스로 검색할 때, 이 파티션 파일들을 순차적으로 열어 검색해야 합니다. 파티션이 1,000개라면 최악의 경우 1,000번의 파일 I/O가 발생합니다.

**Min-Max Cache**는 이 문제를 해결하는 메모리 구조입니다. 각 파티션의 특정 컬럼에 대해 최솟값·최댓값을 메모리에 유지하여, 검색 대상 값이 해당 파티션의 범위를 벗어나면 파티션 자체를 건너뜁니다.

```
[파티션 1] MIN=10, MAX=50  →  검색값 85 → 건너뜀
[파티션 2] MIN=60, MAX=80  →  검색값 85 → 건너뜀
[파티션 3] MIN=80, MAX=95  →  검색값 85 → 스캔 ✓
[파티션 4] MIN=20, MAX=40  →  검색값 85 → 건너뜀
[파티션 5] MIN=75, MAX=90  →  검색값 85 → 스캔 ✓
```

### 설정

컬럼별 Min-Max Cache 크기는 `PROPERTY(MINMAX_CACHE_SIZE = n)` 옵션으로 지정합니다.

```sql
-- id 컬럼에 Min-Max Cache 적용 (20KB)
CREATE TABLE ctest (
    id   INTEGER PROPERTY(MINMAX_CACHE_SIZE = 20480),
    name VARCHAR(100) PROPERTY(MINMAX_CACHE_SIZE = 0)  -- VARCHAR는 0만 허용
);
```

### 기본값과 규칙

| 항목 | 기본값 |
|------|--------|
| 일반 컬럼 MINMAX_CACHE_SIZE | 10KB (10240 bytes) |
| `_ARRIVAL_TIME` (숨김 컬럼) | 100MB (자동 적용) |
| VARCHAR 컬럼 | 0 고정 (캐시 미지원) |

- Min-Max Cache는 명시적으로 인덱스를 생성하지 않아도 동작합니다.
- `ALTER TABLE ... MODIFY COLUMN ... SET MINMAX_CACHE_SIZE = n`으로 생성 후 변경 가능합니다.
- 레코드가 없는 테이블은 Min-Max Cache 메모리를 할당하지 않습니다.
- 파티션 수가 증가할수록 설정된 크기만큼 메모리가 점진적으로 증가합니다.
- VARCHAR 타입에 MINMAX_CACHE_SIZE를 0 이외의 값으로 설정하면 오류가 발생합니다.

```sql
-- 생성 후 캐시 크기 변경
ALTER TABLE ctest MODIFY COLUMN id SET MINMAX_CACHE_SIZE = 20480;
```
