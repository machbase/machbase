---
type: docs
title: '스토리지와 Cluster 튜닝'
weight: 70
---

Machbase의 성능 병목은 CPU보다 I/O에서 발생하는 경우가 훨씬 많습니다. TAG 테이블에 초당 수십만 건씩 Append되는 환경에서는 디스크 쓰기 속도가 전체 수집 처리량의 상한선이 되고, 대용량 범위 조회에서는 디스크 읽기 속도가 응답 시간을 결정합니다. 이 섹션에서는 스토리지 설정과 Cluster Edition 구성에서 성능을 높이는 방법을 설명합니다.

## I/O가 핵심 병목인 이유

Machbase는 컬럼형 스토리지 구조를 사용합니다. Append된 데이터는 메모리 버퍼에 먼저 쌓인 뒤 주기적으로 디스크 파티션 파일로 flush됩니다. 이 flush 경로에서 디스크 I/O 처리 능력이 부족하면 다음 현상이 나타납니다.

- 메모리 버퍼가 가득 차 Append 속도가 느려집니다 (`DISK_COLUMNAR_TABLESPACE_MEMORY_SLOWDOWN_*` 임계치 도달).
- 체크포인트가 밀리고 장애 발생 시 복구 시간이 길어집니다.
- 동시에 SELECT를 실행하면 I/O 경합으로 쿼리 응답 시간이 급격히 증가합니다.

## SSD vs HDD 선택 기준

| 구분 | SSD | HDD |
|------|-----|-----|
| Append 처리량 | 높음 (순차 쓰기 최적화) | 낮음 (회전 지연 발생) |
| 랜덤 읽기 | 빠름 | 매우 느림 |
| 비용 | 높음 | 낮음 |
| 권장 용도 | `DBS_PATH` 데이터 파일 | 콜드 데이터 아카이브 |

**SSD를 반드시 사용해야 하는 경우**

- 초당 10만 건 이상 Append가 발생하는 환경
- 여러 테이블을 동시에 쓰고 읽는 혼합 워크로드
- Cluster Edition에서 Warehouse 역할을 담당하는 호스트

이 빌드에서 사용자 설정으로 분리 가능한 별도 WAL/redo 경로는 확인되지 않습니다. 데이터베이스 파일이 저장되는 `DBS_PATH`를 빠른 스토리지에 배치하는 것을 우선 검토합니다.

## 이 섹션의 구성

| 항목 | 설명 |
|------|------|
| [스토리지와 체크포인트 튜닝](tuning-storage-checkpoint/) | 체크포인트 주기, flush 설정, Direct I/O, 파티션 정리 |
| [Cluster Edition 성능 고려사항](performance-considerations-cluster-edition/) | 노드 구조, 분산 처리, 네트워크 튜닝 |
