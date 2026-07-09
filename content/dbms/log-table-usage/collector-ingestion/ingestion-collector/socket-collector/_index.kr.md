---
type: docs
title: 'socket Collector'
weight: 30
---

현재 확인된 Collector `COLLECT_TYPE`은 `FILE`과 `SFTP`입니다. TCP/UDP socket 수집
설정은 현재 브랜치의 Collector 타입 파서에서 확인되지 않았으므로 이 장에서는
설정 예제를 제공하지 않습니다.

네트워크를 통해 실시간 데이터를 입력해야 하는 경우에는 애플리케이션에서 REST API 또는
SDK Append API를 직접 호출하는 방식을 우선 검토합니다.

## 대안

| 요구 사항 | 권장 경로 |
|-----------|-----------|
| HTTP 기반 장비/게이트웨이 연동 | REST API |
| 애플리케이션 직접 연동 | SDK Append API |
| 파일로 저장된 로그 수집 | [파일 Collector](../file-collector/) |
| 원격 서버 파일 수집 | [SFTP Collector](../sftp-collector/) |
