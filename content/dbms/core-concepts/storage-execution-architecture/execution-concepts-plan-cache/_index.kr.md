---
type: docs
title: 'Cache와 실행 계획 개념'
weight: 40
---

Machbase는 반복적인 SQL 처리 비용을 줄이기 위해 여러 레벨의 캐시를 운용합니다. 각 캐시가 어떤 역할을 하는지 이해하면 시스템 설정을 조정하고 성능 문제를 진단하는 데 도움이 됩니다.

## SQL 실행 과정

SQL 문장이 Machbase에 도달해 결과가 반환되기까지 다음 단계를 거칩니다.

```
클라이언트 SQL
      │
      ▼
  1. 파싱 (Parsing)
     SQL 문장을 파스 트리로 변환
      │
      ▼
  2. 최적화 (Optimization)
     파스 트리를 분석해 최적 실행 경로 결정
     (인덱스 사용 여부, 파티션 pruning 범위 등)
      │
      ▼
  3. 실행 계획 생성 (Plan Generation)
     최적화 결과를 실행 가능한 계획으로 변환
      │
      ▼
  4. 실행 (Execution)
     저장 관리자(SM)에 데이터 읽기/쓰기 요청
      │
      ▼
  결과 반환
```

파싱과 최적화는 동일한 SQL이 반복 실행될 때마다 중복 수행될 수 있습니다. 캐시는 이 중복 비용을 제거하기 위해 존재합니다.

## Plan Cache

Plan Cache는 SQL 문장의 실행 계획을 메모리에 저장해 두고, 같은 SQL이 다시 들어오면 파싱과 최적화 단계를 생략하고 저장된 계획을 재사용하는 캐시입니다.

실시간 수집 환경에서는 동일한 INSERT나 SELECT 패턴이 반복되는 경우가 많습니다. Plan Cache가 있으면 파싱 CPU 비용을 크게 줄일 수 있습니다. Plan Cache는 서버가 기동된 이후 자동으로 운용되며, 별도 설정 없이 동작합니다.

## Result Cache (RS Cache)

RS Cache는 SELECT 쿼리의 결과 자체를 캐시하는 기능입니다. 동일한 쿼리가 짧은 시간 내에 반복 실행될 때, 저장소에서 데이터를 다시 읽지 않고 캐시된 결과를 즉시 반환합니다.

RS Cache는 기본적으로 비활성화되어 있으며, 설정 파일 또는 SQL로 활성화합니다.

```sql
-- RS Cache 활성화 여부 확인
SELECT * FROM M$SYS_CACHE;

-- 세션 수준에서 RS Cache 활성화
SET RS_CACHE_ENABLE = 1;
```

RS Cache는 대시보드처럼 동일 쿼리를 짧은 주기로 반복하는 환경에서 유용합니다. 단, 데이터가 자주 변하는 테이블에 적용하면 오래된 결과가 반환될 수 있으므로, 정책적으로 허용 가능한 경우에만 활성화합니다.

## PVO Cache (파티션 메타데이터 캐시)

PVO Cache는 TAG 테이블의 파티션 메타데이터를 메모리에 보관하는 캐시입니다. TAG 테이블 조회 시 어떤 파티션을 읽어야 하는지 결정하는 데 필요한 메타데이터를 매번 디스크에서 읽지 않고 메모리에서 즉시 참조합니다.

PVO Cache는 서버가 기동될 때 자동으로 로드되며, TAG 테이블 조회가 많은 환경에서 특히 효과적입니다.

## EXPLAIN으로 실행 계획 확인

`EXPLAIN` 문을 사용하면 쿼리가 실제로 어떤 실행 계획을 사용하는지 확인할 수 있습니다.

```sql
EXPLAIN SELECT AVG(value)
FROM sensor_values
WHERE name = 'temp_sensor_01'
  AND time BETWEEN TO_DATE('2026-07-01', 'YYYY-MM-DD')
               AND TO_DATE('2026-07-03', 'YYYY-MM-DD');
```

실행 계획 출력에서 파티션 pruning이 적용되었는지, 인덱스가 사용되었는지, RS Cache 히트 여부를 확인할 수 있습니다. 성능이 기대에 못 미칠 때 `EXPLAIN`을 먼저 실행해 실행 경로를 검토하십시오.

## 다음 읽을 내용

- [인덱싱 기본 원리](../indexing-basics/) — 실행 계획에서 인덱스가 사용되는 원리
- [Machbase 아키텍처 개요](../architecture-machbase/) — 쿼리 프로세서(QP)의 역할
- [컬럼형 저장과 압축](../storage-columnar-compression-column/) — 실행 계획이 읽는 저장 구조
