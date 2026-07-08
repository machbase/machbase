---
type: docs
title: '12. 시나리오 가이드'
weight: 120
---

이 장은 실제 업무 시나리오를 단계별로 따라하며 Machbase의 주요 기능을 익히는 실습 중심의 안내서입니다. 데이터 수집부터 저장, 집계, 조회, 운영까지 산업 현장에서 자주 마주치는 패턴을 구체적인 SQL과 코드 예시와 함께 다룹니다.

각 시나리오는 독립적으로 따라할 수 있도록 완결성 있게 작성되었습니다. 처음 Machbase를 사용하는 경우 난이도 초급 시나리오부터 시작하는 것을 권장합니다.

## 시나리오 목록

| # | 시나리오 | 난이도 | 핵심 기능 |
|---|----------|--------|-----------|
| 1 | [센서 데이터 저장과 ROLLUP 분석](storage-sensor-data-rollup/) | 초급 | TAG 테이블, ROLLUP |
| 2 | [로그 데이터 저장과 텍스트 검색](storage-log-text-search-logs/) | 초급 | LOG 테이블, SEARCH |
| 3 | [장비 마스터 데이터와 알람 상태 관리](state-master-status-equipment-alarm/) | 중급 | LOOKUP 테이블, JOIN |
| 4 | [TAG + RDB + LOG 조인 대시보드](join-tag-rdb-log/) | 중급 | 복합 JOIN, 집계 |
| 5 | [실시간 상태판 만들기](state-status-real-time-dashboard/) | 중급 | STREAM, LOOKUP |
| 6 | [대량 데이터 적재 파이프라인](bulk-pipeline/) | 중급 | Append API, 배치 |
| 7 | [Collector로 파일/소켓 데이터 수집하기](file-ingestion-collector/) | 중급 | Collector |
| 8 | [Fluentd로 로그 파이프라인 연결하기](log-logs-pipeline-connection-fluentd/) | 중급 | Fluentd 플러그인 |
| 9 | [STREAM으로 LOG를 TAG로 자동 적재](stream-log-tag/) | 고급 | STREAM, 자동화 |
| 10 | [이상 데이터 정정 후 ROLLUP Rebuild](correction-abnormal-data-rollup-rebuild/) | 고급 | ROLLUP Rebuild |
| 11 | [백업 데이터 마운트 후 조회](backup-query-mount/) | 고급 | Backup, Mount |
| 12 | [Cluster 설치와 확장](cluster/) | 고급 | Cluster Edition |
| 13 | [애플리케이션 연동 예제](examples/) | 초급~중급 | SDK, REST API |

## 난이도 기준

- **초급**: Machbase를 처음 사용하는 분도 따라할 수 있습니다. 기본 SQL과 테이블 생성·조회에 집중합니다.
- **중급**: 테이블 유형별 특성과 기본 운영 방식을 이해한 상태에서 시작합니다. 여러 기능을 조합해 실용적인 패턴을 구성합니다.
- **고급**: 내부 동작 원리와 운영 경험을 갖춘 상태에서 시작합니다. 성능 최적화, 장애 대응, 클러스터 구성 등을 다룹니다.

## 시나리오 그룹

### 데이터 저장과 조회 (1~2번)

TAG 테이블과 LOG 테이블의 기본 사용 패턴입니다. 데이터를 수집·저장하고 ROLLUP 집계와 텍스트 검색으로 조회하는 흐름을 익힙니다.

### 마스터 데이터와 복합 조회 (3~4번)

LOOKUP 테이블로 장비 마스터를 관리하고, TAG·LOG·RDB 테이블을 조인해 대시보드용 데이터를 구성하는 패턴을 다룹니다.

### 실시간 처리와 파이프라인 (5~8번)

STREAM으로 실시간 상태판을 구성하고, Collector와 Fluentd로 외부 데이터를 수집하는 파이프라인을 구축합니다.

### 자동화와 고급 운영 (9~12번)

STREAM 기반 자동 적재, ROLLUP Rebuild, 백업 마운트, 클러스터 구성 등 운영 환경에서 필요한 고급 패턴을 다룹니다.

### 애플리케이션 연동 (13번)

Python, Go, REST API 등 다양한 언어와 인터페이스로 Machbase에 연결하는 예제를 제공합니다.
