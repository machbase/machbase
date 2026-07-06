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
