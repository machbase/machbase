---
type: docs
title: '캐시와 메모리 튜닝'
weight: 60
---

Machbase는 반복적인 쿼리 처리 비용을 줄이고 메모리를 효율적으로 활용하기 위해 여러 종류의 캐시를 제공합니다. 캐시와 메모리 설정을 올바르게 구성하면 조회 응답 시간을 단축하고 서버 전체의 처리량을 높일 수 있습니다.

## Machbase의 주요 캐시

| 캐시 종류 | 설명 | 관련 프로퍼티 |
|---------|------|------------|
| **Result Cache** | 동일한 SELECT 쿼리의 결과를 메모리에 저장하여 재사용 | `RS_CACHE_*` |
| **PVO Cache** | SQL 실행 계획(Plan)을 캐시하여 파싱/최적화 비용 절감 (Standard Edition) | `PVO_CACHE_*` |
| **Min-Max Cache** | 컬럼별 최솟값/최댓값 정보를 캐시하여 파티션 프루닝 가속 | `DISK_COLUMNAR_TABLE_COLUMN_MINMAX_CACHE_SIZE` |

## 메모리 예산 배분 원칙

Machbase 서버의 메모리 예산을 배분할 때는 다음 원칙을 참고하십시오.

```
전체 물리 메모리
  ├── OS 및 기타 프로세스: 약 20%
  ├── 캐시 (Result Cache + PVO Cache 합산): 30~40%
  └── Machbase 처리 공간 (정렬, 집계, 인덱스 빌드 등): 나머지
```

- **Result Cache**(`RS_CACHE_MAX_MEMORY_SIZE`)와 **PVO Cache**(`PVO_CACHE_MAX_MEMORY_SIZE`)의 합이 전체 메모리의 40%를 넘지 않도록 설정합니다.
- Min-Max Cache는 파티션 수에 비례하여 메모리를 사용하므로, 대규모 LOG 테이블 환경에서는 `_ARRIVAL_TIME` 기본값과 필요한 LOG 일반 컬럼의 `MINMAX_CACHE_SIZE`를 함께 검토합니다.
- 메모리 부족(OOM killer 발생, swap 급증)이 감지되면 캐시 상한을 낮추고 `PROCESS_MAX_SIZE`로 프로세스 최대 메모리를 제한하십시오.

## 이 섹션의 구성

- [Result Cache 운영](result-cache/) — 반복 집계 쿼리의 결과를 캐시하는 방법과 무효화 동작
- [PVO Cache 운영](pvo-cache/) — SQL 실행 계획 캐시 (Standard Edition)
- [메모리 설정 튜닝](tuning-memory-configuration/) — 전체 메모리 배분 및 Min-Max Cache 조정
