---
type: docs
title: '12. 성능 튜닝'
weight: 120
---

성능 문제는 대부분 몇 가지 공통 원인에서 비롯됩니다. 데이터 특성에 맞지 않는 테이블 타입, 인덱스 없는 대용량 컬럼 스캔, 배치 입력 대신 건별 INSERT, 과소 설정된 메모리 버퍼가 그것입니다.

**가장 큰 성능 이득은 올바른 테이블 타입 선택에서 옵니다.** 센서 계측값을 LOG 테이블로 저장하거나, 이벤트 로그를 TAG 테이블에 넣으면 인덱스를 아무리 추가해도 근본적인 한계를 넘지 못합니다. 쿼리 최적화나 캐시 튜닝보다 테이블 타입 재설계가 수십 배 더 큰 개선을 가져오는 경우가 흔합니다.

## 성능 튜닝 5대 영역

| 영역 | 핵심 질문 | 주요 수단 |
|------|-----------|-----------|
| **[모델링](performance-tuning-modeling/)** | 테이블 타입이 데이터 특성과 일치하는가? | TAG vs LOG 선택, 컬럼 설계, MINMAX 캐시 |
| **[입력](performance-tuning/)** | 데이터가 빠르게 적재되고 있는가? | Append API, 배치 크기, 병렬 스레드 |
| **[조회/분석](performance-query-tuning/)** | 쿼리 실행 계획이 인덱스를 활용하는가? | EXPLAIN, 인덱스 추가, 쿼리 재작성 |
| **[캐시/메모리](cache-tuning-memory/)** | 메모리 설정이 워크로드에 적합한가? | RS Cache, PVO Cache, 컬럼 버퍼 |
| **[스토리지/클러스터](tuning-storage-cluster/)** | 디스크 I/O와 체크포인트가 병목인가? | Direct I/O, 체크포인트 주기, 파티션 |

## 진단 순서

성능 문제를 만났을 때 무작정 프로퍼티부터 수정하면 효과를 확인하기 어렵습니다. 다음 순서를 따르면 원인을 빠르게 좁힐 수 있습니다.

1. **병목 지점 파악**: I/O, CPU, 메모리 중 어디가 포화 상태인가
2. **실행 계획 확인**: `EXPLAIN SELECT ...`로 FULL SCAN 여부 확인
3. **현재 세션 확인**: `V$STMT`, `V$SESSION`으로 실행 중인 쿼리 확인
4. **인덱스·캐시·프로퍼티 조정**: 대상이 명확해진 후 개별 튜닝
5. **모델 재설계**: 모든 튜닝이 효과 없을 때 최후 수단

자세한 접근 방법은 **[성능 문제 접근 순서](performance-approach/)** 를 참고하십시오.

## 하위 섹션

| 섹션 | 설명 |
|------|------|
| [성능 문제 접근 순서](performance-approach/) | 병목 진단, EXPLAIN 해석, V$ 뷰 활용 |
| [모델링 성능 튜닝](performance-tuning-modeling/) | 테이블 타입 선택, 스키마 설계 |
| [입력 성능 튜닝](performance-tuning/) | Append API, 대량 적재, Collector |
| [조회·분석 성능 튜닝](performance-query-tuning/) | SELECT 최적화, 인덱스, ROLLUP |
| [인덱스 튜닝](index-tuning/) | 테이블 타입별 인덱스 전략 |
| [캐시·메모리 튜닝](cache-tuning-memory/) | RS Cache, PVO Cache, 메모리 설정 |
| [스토리지·클러스터 튜닝](tuning-storage-cluster/) | 체크포인트, Direct I/O, Cluster Edition |
| [Collector 수집 성능 튜닝](/dbms/performance-tuning/performance-tuning/#ingestion-performance-tuning-collector) | 배치 크기, flush 주기, 병렬 스레드, 수집 모니터링 |
| [성능 진단 체크리스트](checklist-performance-diagnosis/) | 운영 환경 점검 항목 |
