---
type: docs
title: '16. 시나리오 가이드'
weight: 160
toc: true
---

이 장은 앞 장의 기능을 실제 운영 흐름으로 조합합니다. SQL 실습은 각 페이지의 고유한
`SC16_` 객체를 사용하며 생성, 입력, 검증, 정리 순서로 구성합니다.

| 절 | 시나리오 | 정본으로 연결되는 내용 |
|---|---|---|
| 16.1 | [실시간 상태 대시보드](./state-status-real-time-dashboard/) | TAG 최신값과 상태 판정 |
| 16.2 | [장비 마스터와 알람](./state-master-status-equipment-alarm/) | LOOKUP, TAG, LOG |
| 16.3 | [TAG·TRANSACTION·LOG 조인](./join-tag-rdb-log/) | 이기종 테이블 조인 |
| 16.4 | [대량 적재 파이프라인](./bulk-pipeline/) | loader와 Append 선택 |
| 16.5 | [백업 데이터 조회](./backup-query-mount/) | BACKUP, MOUNT, UMOUNT |
| 16.6 | [클러스터 작업 계획](./cluster/) | 설치·운영 정본을 이용한 변경 계획 |
| 16.7 | [Collector 파일 적재](./file-ingestion-collector/) | 템플릿 등록과 결과 검증 |
| 16.8 | [SDK 선택](./examples/) | 11장의 검증된 언어별 quickstart |

공유 서버에서 실습할 때는 별도 논리 database를 사용하고, 완료 후 만든 객체와 database를
삭제하십시오. 백업·MOUNT, Collector, Cluster 예제는 서비스와 파일 시스템에 영향을 주므로
격리된 검증 환경에서만 실행합니다.
