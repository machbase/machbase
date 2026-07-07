---
type: docs
title: 'ALTER SYSTEM 운영'
weight: 30
---

`ALTER SYSTEM`은 Machbase 서버의 전역 자원을 관리하는 SQL 구문입니다. 세션 제어, 라이선스 설치, 캐시 정리, 체크포인트, I/O 동결 등 DBA가 서버를 운영하면서 필요한 작업을 수행합니다.

> **권한**: `ALTER SYSTEM` 명령은 `SYS` 계정 또는 `GRANT ALTER ON MACHBASEDB TO user_name;`으로 권한을 부여받은 사용자만 실행할 수 있습니다.

## 명령어 목록

| 명령어 | 기능 | 서버 재시작 필요 |
|---|---|:---:|
| [`ALTER SYSTEM KILL SESSION`](./kill-cancel-session/) | 지정한 세션을 강제 종료 | 아니요 |
| [`ALTER SYSTEM CANCEL SESSION`](./kill-cancel-session/) | 세션의 현재 실행 중인 쿼리만 취소 (세션 유지) | 아니요 |
| [`ALTER SYSTEM CHECK DISK_USAGE`](./check-disk-usage/) | 디스크 사용량 정보를 파일 시스템에서 재계산 | 아니요 |
| [`ALTER SYSTEM INSTALL LICENSE`](./install-license/) | 라이선스 파일 설치 (기본 경로 또는 지정 경로) | 아니요 |
| [`ALTER SYSTEM CHECKPOINT`](./checkpoint/) | 메모리 버퍼를 디스크에 즉시 동기화 | 아니요 |
| [`ALTER SYSTEM FREEZE`](./freeze-unfreeze/) | 모든 DML을 일시 중단 (백업 준비용) | 아니요 |
| [`ALTER SYSTEM UNFREEZE`](./freeze-unfreeze/) | FREEZE로 중단된 DML을 재개 | 아니요 |
| [`ALTER SYSTEM FLUSH AGER`](./flush-ager/) | Ager 스레드를 즉시 실행하여 만료 데이터 정리 | 아니요 |
| [`ALTER SYSTEM FLUSH RESULT_CACHE`](./flush-result-cache/) | 쿼리 결과 캐시 전체 초기화 | 아니요 |
| [`ALTER SYSTEM FLUSH SYS_STAT`](./flush-sys-stat/) | 쿼리 최적화기용 시스템 통계 정보 갱신 | 아니요 |
| [`ALTER SYSTEM FLUSH PVO_CACHE`](./flush-pvo-cache/) | PVO(Partition Value Object) Statement 캐시 초기화 | 아니요 |
| [`ALTER SYSTEM FLUSH PAGE_CACHE`](./flush-page-cache/) | OS 페이지 캐시를 Machbase 레벨에서 강제 해제 | 아니요 |
| [`ALTER SYSTEM FLUSH TAG_CACHE`](./flush-tag-cache/) | TAG 테이블 메타데이터 캐시 초기화 | 아니요 |

## 관련 뷰

| 뷰 | 설명 |
|---|---|
| `v$session` | 현재 접속 세션 목록 및 실행 중인 쿼리 확인 |
| `v$storage` | 디스크 사용량 정보 (`DC_TABLE_FILE_SIZE` 등) |
| `v$license_info` | 설치된 라이선스 정보 확인 |
| `v$property` | 시스템 속성 및 현재 값 확인 |
