---
type: docs
title: '13.2 설정 운영'
weight: 20
---

이 섹션에서는 Machbase의 설정 파일 구조와 주요 파라미터를 설명합니다. 설정값을 올바르게 이해하고 환경에 맞게 조정하면 성능과 안정성을 크게 향상시킬 수 있습니다.

## 설정 파일 개요

Machbase의 모든 설정은 `$MACHBASE_HOME/conf/machbase.conf` 파일에서 관리합니다. 이 파일은 키-값 쌍으로 구성되며, 서버 시작 시 읽혀 적용됩니다.

일부 설정은 서버를 재시작해야만 적용되고, 일부는 `ALTER SYSTEM SET` 명령어로 서버 실행 중에 즉시 변경할 수 있습니다. 변경 가능 여부는 각 파라미터 설명에서 확인합니다.

## 이 섹션의 구성

| 페이지 | 내용 |
|--------|------|
| [설정 파일 위치와 적용 절차](./file-config-configuration/) | machbase.conf 구조, 변경 후 재시작 절차, 백업 방법 |
| [Runtime 변경 가능 설정과 재시작 필요 설정](./alter-start-restart-configuration-runtime/) | ALTER SYSTEM SET 사용법, 런타임 변경 가능 파라미터 목록 |
| [주요 설정 파라미터](./parameters-configuration/) | 파라미터 전체 요약표 (기본값, 재시작 필요 여부, 설명) |
| [메모리 설정](./memory-configuration/) | PROCESS_MAX_SIZE, RS_CACHE 메모리 튜닝 |
| [세션과 네트워크 설정](./network-session-configuration/) | PORT_NO, MAX_SESSION_COUNT, 타임아웃 설정 |
| [스토리지와 체크포인트 설정](./storage-checkpoint-configuration/) | 데이터 경로, 체크포인트 주기, Direct I/O |
| [타임존](./timezone/) | 서버·클라이언트 타임존, machsql/machloader/REST API 설정 |
