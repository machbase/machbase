---
type: docs
title: '18.8.11 error-resolution-map'
weight: 110
toc: true
---

오류 코드를 요약 페이지에 복제하면 제품 변경과 함께 의미가 어긋날 수 있습니다. AI는 전체
오류 코드와 메시지를 보존하고 [오류 코드 사전](/dbms/reference/error-dictionary-codes/)에서
정확한 의미를 찾습니다.

## 오류 해결 맵

| 증상 | 첫 확인 | 정본 |
|---|---|---|
| 서버 접속 불가 | `machadmin -e`, 주소·포트·리스너·방화벽 | [서버와 연결 문제](/dbms/troubleshooting/server-connection/) |
| 인증 실패 | 사용자 만료, 선택한 AUTH_MODE, 키 활성 상태 | [인증 문제](/dbms/troubleshooting/server-connection/#failure-authentication) |
| 권한 오류 | 대상 database·owner·table과 `M$SYS_USER_ACCESS` | [권한 관리](/dbms/security-access-control/privileges/) |
| 객체 오류 | 현재 database와 `M$SYS_TABLES`, `M$SYS_COLUMNS` | [시스템 카탈로그](/dbms/reference/log-logs-system-catalog/) |
| loader 입력 실패 | `machloader -h`, bad/log 파일, schema | [입력 문제](/dbms/troubleshooting/item/#failure-csv-import) |
| 디스크·메모리 경고 | `V$STORAGE_USAGE`, `V$SYSMEM`, OS 상태 | [성능 문제](/dbms/troubleshooting/performance/) |
| Cluster 노드 이상 | 전체 토폴로지와 최초 오류 노드 | [Cluster 문제](/dbms/troubleshooting/cluster/) |

## SDK 오류

SDK 이름과 버전, 서버 빌드, 연결 옵션, 전체 오류와 최소 재현 코드를 함께 수집합니다. 동일한
기능이라도 SDK마다 marker, 시간 타입, Append 반환값과 database 선택 방법이 다르므로
[개발 도구 연동](/dbms/development-tools-integration/)의 해당 언어 정본을 사용합니다.

오류 메시지의 일부 문자열만 보고 임의의 `ERR-` 번호를 붙이지 않습니다. 사전에 없는 코드는
서버 빌드와 로그 위치를 포함해 지원 요청 자료로 남깁니다.
