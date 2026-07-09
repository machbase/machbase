---
type: docs
title: '13. 운영, 설정, 복구'
weight: 130
---

이 장에서는 Machbase 서버를 실제 환경에서 운영할 때 필요한 작업 전반을 다룹니다. 서버 기동과 종료처럼 일상적인 운영부터 설정 변경, 백업과 복구, 장애 진단, 그리고 클러스터 환경 운영까지 6개의 영역으로 구성됩니다.

## 운영 6대 영역

| 영역 | 내용 | 섹션 |
|------|------|------|
| 서버/DB 운영 | 서버 시작·종료, 데이터베이스 생성·삭제, 라이선스 관리 | [서버와 데이터베이스 운영](./server-database/) |
| ALTER SYSTEM | 런타임 파라미터 변경, 시스템 제어 명령 | [ALTER SYSTEM](./alter-system/) |
| 설정 운영 | 설정 파일, 주요 파라미터, 메모리·네트워크·스토리지 설정, 타임존 | [설정 운영](./configuration/) |
| 백업/복구 | 온라인·오프라인 백업, 복구 절차, 마운트 | [백업, 복구, 마운트](./backup-restore-mount/) |
| 관측/진단 | 모니터링, 시스템 뷰, 로그 분석, 성능 진단 | [관측과 진단](./diagnosis-observability/) |
| Cluster/Collector | 클러스터 토폴로지 관리, Collector 운영 | [클러스터](./cluster/) · [Collector](./collector/) |

## 이 장의 구성

### 10.1 서버와 데이터베이스 운영

서버 프로세스의 생명 주기를 관리합니다. `machadmin` 명령어로 서버를 시작하고 종료하며, 데이터베이스를 생성하거나 삭제합니다. 라이선스 설치와 갱신 절차도 여기에서 설명합니다.

- [서버 시작과 종료](./server-database/start-server/)
- [데이터베이스 생성과 삭제](./server-database/create-delete-database/)
- [라이선스 설치와 확인](./server-database/license/)

### 10.2 설정 운영

`$MACHBASE_HOME/conf/machbase.conf` 파일의 구조와 각 파라미터의 의미를 설명합니다. 재시작 없이 즉시 적용할 수 있는 런타임 설정과 재시작이 필요한 정적 설정을 구분하고, 메모리·네트워크·스토리지 튜닝 지침과 타임존 설정 방법을 다룹니다.

- [설정 파일 위치와 적용 절차](./configuration/file-config-configuration/)
- [Runtime 변경 가능 설정과 재시작 필요 설정](./configuration/alter-start-restart-configuration-runtime/)
- [주요 설정 파라미터](./configuration/parameters-configuration/)
- [메모리 설정](./configuration/memory-configuration/)
- [세션과 네트워크 설정](./configuration/network-session-configuration/)
- [스토리지와 체크포인트 설정](./configuration/storage-checkpoint-configuration/)
- [타임존](./configuration/timezone/)
