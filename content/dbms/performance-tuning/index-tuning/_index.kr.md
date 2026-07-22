---
type: docs
title: '12.3 인덱스 튜닝'
weight: 30
toc: true
---

테이블 유형마다 인덱스 구조가 다르며, 조회 성능과 삽입 오버헤드 사이에서 균형을 잡는 것이 핵심입니다.

## Machbase 인덱스 종류 요약

| 테이블 유형 | 기본 인덱스 | 추가 생성 가능 | 주요 용도 |
|------------|------------|--------------|---------|
| TAG | 태그명·시간 파티션·METADATA 인덱스 (자동) | 값 컬럼에 TAG/KV 인덱스 가능 | 태그명 + 시간 범위 고속 조회, 값 조건 보조 |
| LOG | 없음 (시간 기반 파티션 pruning) | LSM, BITMAP, KEYWORD | 특정 컬럼 조건 조회 |
| LOOKUP | Red-Black 트리 (PK 자동) | Red-Black 보조 인덱스 | PK 기반 기준 정보 조회 |
| VOLATILE | Red-Black 트리 (PK 자동) | Red-Black 보조 인덱스 | 인메모리 상태 테이블 |
| TRANSACTION | B-Tree (PK 자동) | 단일/복합 B-Tree 인덱스 | RDBMS 방식 관계형 데이터 |

## 인덱스가 성능에 미치는 양면

### 조회 가속

인덱스가 있으면 특정 컬럼 조건에서 전체 파티션 스캔을 줄이고 대상 행에 접근할 수 있습니다.
카디널리티와 조건 선택도를 확인하고 `EXPLAIN`으로 인덱스 사용 여부를 검증합니다.

```sql
-- 인덱스 없이: 파티션 전체 순차 스캔
SELECT * FROM device_log WHERE device_id = 'DEV-1234' DURATION 1 DAY;

-- 인덱스 있음: 인덱스 경유 직접 접근
CREATE INDEX idx_device ON device_log (device_id);
SELECT * FROM device_log WHERE device_id = 'DEV-1234' DURATION 1 DAY;
```

### 삽입 오버헤드

인덱스는 데이터 삽입 시마다 함께 갱신되므로 Append 비용을 증가시킵니다. 인덱스 수에 따른
영향은 데이터 분포와 입력 동시성에 따라 달라지므로 운영 워크로드로 측정합니다.

```
인덱스 없음:  Append 100만 건/초 (기준)
LSM 인덱스 1개:  Append ~90~95만 건/초
LSM 인덱스 3개:  Append ~75~85만 건/초
```

따라서 인덱스는 실제로 WHERE 조건에 자주 등장하는 컬럼에만 선별적으로 생성해야 합니다.

## 현재 인덱스 확인

```sql
-- 전체 인덱스 목록
SHOW INDEXES;

-- 인덱스 구축 진행 상황 (백그라운드 빌드 중일 때)
SHOW INDEXGAP;
```

## 다음 읽을 내용

- [TAG 인덱스 튜닝](/dbms/tag-table-usage/index-performance/#index-tuning-tag) — 자동 파티션 인덱스와 METADATA 컬럼 최적화
- [LOG 인덱스 튜닝](/dbms/log-table-usage/index-performance/#index-tuning-log) — LSM, BITMAP, KEYWORD 인덱스 활용 전략
- [LOOKUP/VOLATILE 인덱스 튜닝](/dbms/lookup-table-usage/index-performance/#index-tuning-lookup-volatile) — PK 기반 인덱스 특성과 한계
- [TRANSACTION 인덱스 튜닝](/dbms/rdb-table-usage/index-performance/#index-tuning-rdb) — B-Tree 인덱스와 PK 설계 패턴
