---
type: docs
title: '17.8.11 error-resolution-map'
weight: 110
toc: true
---

오류 번호나 원인을 추측하지 않고 전체 오류와 실행 문맥을 보존합니다.

## 진단 순서

1. 전체 `ERR-XXXXX` 메시지, SQL·명령, 발생 시각을 수집합니다.
2. 서버와 SDK 버전, Edition, 대상 database·owner·table과 연결 option을 기록합니다.
3. [오류 코드 사전](/dbms/reference/error-dictionary-codes/)에서 메시지를 확인합니다.
4. [문제 해결](/dbms/troubleshooting/)에서 증상별 진단 절차를 적용합니다.
5. 조치 뒤 같은 입력과 확인 쿼리로 복구 여부를 검증합니다.

| 증상 | 정본 |
|------|------|
| 서버·인증·연결 | [서버와 연결 문제](/dbms/troubleshooting/server-connection/) |
| 입력·Append·파일 | [입력과 적재 문제](/dbms/troubleshooting/item/) |
| 쿼리·성능·메모리 | [쿼리와 성능 문제](/dbms/troubleshooting/performance/) |
| 백업·복구 | [백업과 복구 문제](/dbms/troubleshooting/recovery-backup/) |
| Cluster | [Cluster 문제](/dbms/troubleshooting/cluster/) |

오류 문자열 일부만으로 임의의 오류 코드를 붙이거나, 재현 없이 destructive workaround를
권장하지 않습니다.
