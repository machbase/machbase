---
type: docs
title: 'Result Cache 운영'
weight: 10
---

Result Cache는 동일한 SELECT 쿼리가 반복 실행될 때 이전에 계산한 결과를 메모리에 저장해 두었다가 즉시 반환하는 기능입니다. 집계 연산이 많은 대시보드나 주기적으로 같은 조건을 조회하는 워크로드에서 응답 시간을 크게 줄일 수 있습니다.

## 동작 원리

1. 클라이언트가 SELECT 쿼리를 실행합니다.
2. 동일한 쿼리가 이미 캐시되어 있고 유효한 상태이면 저장된 결과를 즉시 반환합니다.
3. 캐시가 없거나 무효화된 경우 쿼리를 실제로 실행하고, 조건(`RS_CACHE_TIME_BOUND_MSEC`, `RS_CACHE_MAX_RECORD_PER_QUERY` 등)을 충족하면 결과를 캐시에 저장합니다.

쿼리 텍스트가 완전히 동일해야 캐시 히트가 발생합니다. 리터럴 값, 공백, 대소문자가 달라져 SQL 텍스트가 바뀌면 별도의 캐시 엔트리로 처리됩니다. 바인드 실행은 Result Cache 대상이 아니므로, 반복 조회를 캐시하려면 실제 실행되는 SELECT 텍스트가 동일한지 확인합니다.

## 적합한 워크로드

| 워크로드 유형 | Result Cache 효과 |
|------------|-----------------|
| 대시보드의 주기적 갱신 (30초~수 분 간격) | 높음 |
| 반복 실행되는 집계 쿼리 (COUNT, SUM, AVG 등) | 높음 |
| 배치 Append 후 조회 패턴 (적재 완료 후 일정 시간 조회) | 높음 |
| 실시간 센서 스트림 연속 조회 (매 초 새 데이터 Append) | 낮음 (Append마다 캐시 무효화) |
| 조건이 매번 바뀌는 임시 분석 쿼리 | 낮음 (캐시 히트 없음) |

## 주요 설정 항목

| 프로퍼티 | 기본값 | 설명 |
|--------|------|------|
| [`RS_CACHE_ENABLE`](rs-cache-enable/) | 1 | Result Cache 활성화 여부 |
| [`RS_CACHE_TIME_BOUND_MSEC`](rs-cache-time-bound-msec/) | 1000 ms | 이 시간보다 빠른 쿼리는 캐시하지 않음 |
| [`RS_CACHE_MAX_RECORD_PER_QUERY`](rs-cache-max-record-per-query/) | 기본값 10000, 표준 샘플 50000 | 결과 레코드 수 상한 (초과 시 캐시 안 함) |
| `RS_CACHE_MAX_MEMORY_PER_QUERY` | 16 MB | 쿼리당 최대 캐시 메모리 |
| `RS_CACHE_MAX_MEMORY_SIZE` | 512 MB | 전체 Result Cache 최대 메모리 |
| `RS_CACHE_APPROXIMATE_RESULT_ENABLE` | 0 | 근사 결과 허용 여부 (1이면 더 빠르지만 부정확할 수 있음) |

## 이 섹션의 구성

- [RS_CACHE_ENABLE](rs-cache-enable/) — Result Cache 전체 활성화/비활성화
- [RS_CACHE_TIME_BOUND_MSEC](rs-cache-time-bound-msec/) — 캐시 대상 쿼리의 최소 실행 시간 기준
- [RS_CACHE_MAX_RECORD_PER_QUERY](rs-cache-max-record-per-query/) — 결과 레코드 수 상한 설정
- [V$RS_CACHE_* 확인](vrs-cache/) — 캐시 상태 모니터링
- [LRU와 동시성](concurrency-lru/) — 교체 정책 및 고동시성 환경 고려 사항
- [Append invalidation](append-invalidation/) — 캐시 무효화 동작과 워크로드별 적합성
