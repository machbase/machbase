---
type: docs
title: '13. 문제 해결'
weight: 130
---

이 장은 Machbase 운영 중 발생하는 일반적인 오류와 문제 상황을 **증상 → 원인 → 해결** 순서로 안내합니다. 먼저 증상을 확인하고 진단 명령으로 원인을 좁힌 후, 해당 섹션의 해결 방법을 적용하는 절차를 따르면 대부분의 문제를 빠르게 해결할 수 있습니다.

{{< callout type="info" >}}
**먼저 확인할 것**

1. **서버 상태**: `machadmin -c` 명령으로 프로세스가 실행 중인지 확인합니다.
2. **로그 파일**: `$MACHBASE_HOME/trc/machbase.trc`에서 최근 오류 메시지를 확인합니다.
3. **오류 코드**: 오류 메시지의 `ERR-XXXXX` 코드로 원인과 해결 방법을 찾습니다.
{{< /callout >}}

## 이 장의 구성

| 섹션 | 내용 |
|------|------|
| [문제 해결 접근법](./troubleshooting/) | 체계적인 5단계 진단 절차, 증상 확인, 진단 명령, 로그 분석, 오류 코드 조회 |
| [서버와 연결 문제](./server-connection/) | 서버 시작 실패, 원격 접속 불가, 인증 오류 |
| [입력과 적재 문제](./item/) | 데이터 입력 실패, CSV 임포트 오류, Collector 연동 문제 |
| [쿼리와 성능 문제](./performance/) | 느린 쿼리, 검색 결과 없음, 메모리 부족, 트랜잭션 충돌 |
| [UPDATE/DELETE 문제](./update-delete/) | 태그 데이터 수정 제한, WHERE 조건 오류, JSON 경로 오류 |
| [자동 처리 문제](./automation/) | ROLLUP 실행 이상, STREAM 쿼리 오류 |
| [백업과 복구 문제](./recovery-backup/) | 백업 실패, MOUNT/UNMOUNT 오류, RDB Sidecar 연동 오류 |
| [Cluster 문제](./cluster/) | 노드 상태 이상, Cluster Edition 오류 |
