---
type: docs
title: '13. 운영, 설정, 복구'
weight: 130
toc: true
---

Machbase 서버의 시작과 종료, 설정 변경, 관측, 백업과 복원, Cluster 운영 절차를
다룹니다. 일상 운영 절차를 먼저 정립하고, 변경·복구 작업은 계획에 따라 수행합니다.

## 이 장의 구성

| 순서 | 섹션 | 내용 |
|-----:|------|------|
| 13.1 | [서버와 데이터베이스 운영](./server-database/) | 서버 시작·종료, 데이터베이스 생성·삭제, 라이선스 |
| 13.2 | [다중 데이터베이스](./multi-database/) | 논리 데이터베이스, 권한, 백업·복원, 클라이언트 연동 |
| 13.3 | [설정 운영](./configuration/) | 설정 파일, 메모리, 네트워크, 스토리지, 타임존 |
| 13.4 | [ALTER SYSTEM 운영](./alter-system/) | 런타임 설정 변경과 시스템 제어 |
| 13.5 | [데이터 보존 정책](./policy-data-retention/) | Retention 생성, 적용, 점검, 해제 |
| 13.6 | [관측과 진단](./diagnosis-observability/) | 시스템 뷰, 로그, 세션, 용량과 장애 징후 |
| 13.7 | [스키마 변경 체크리스트](./checklist-schema-alter/) | DDL 전후 영향 분석과 검증 절차 |
| 13.8 | [백업, 복원, 마운트](./backup-restore-mount/) | 온라인 백업, 오프라인 복원, 읽기 전용 마운트 |
| 13.9 | [Cluster 운영](./cluster/) | 토폴로지, 노드 추가·제거, 상태 관리 |

일상 점검에는 [서버와 데이터베이스 운영](./server-database/), [설정 운영](./configuration/),
[관측과 진단](./diagnosis-observability/)을 사용합니다. 다중 데이터베이스를 도입할 때는
[다중 데이터베이스](./multi-database/)를 먼저 확인합니다. 스키마 또는 설정을 변경할 때는
[ALTER SYSTEM 운영](./alter-system/)과 [스키마 변경 체크리스트](./checklist-schema-alter/)를,
장애 복구와 백업 검증에는 [백업, 복원, 마운트](./backup-restore-mount/)를 확인합니다.
