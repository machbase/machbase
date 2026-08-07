---
type: docs
title: '17. 문제 해결'
weight: 170
toc: true
---

Machbase 운영 중 발생하는 문제를 증상 확인, 원인 진단, 해결, 재발 방지 순서로 다룹니다.

{{< callout type="info" >}}
문제를 분류하기 전에 `machadmin -e`로 서버 상태를 확인하고,
`$MACHBASE_HOME/trc/machbase.trc`의 최근 오류와 클라이언트의 `ERR-XXXXX` 코드를 기록합니다.
{{< /callout >}}

## 이 장의 구성

| 순서 | 섹션 | 내용 |
|-----:|------|------|
| 17.1 | [문제 해결 접근법](./troubleshooting/) | 증상 수집, 진단 명령, 로그와 오류 코드 분석 |
| 17.2 | [서버와 연결 문제](./server-connection/) | 서버 시작, 원격 접속, 인증 오류 |
| 17.3 | [UPDATE/DELETE 문제](./update-delete/) | 테이블 타입별 변경 조건과 JSON 경로 오류 |
| 17.4 | [입력과 적재 문제](./item/) | Append, CSV 가져오기, Collector 오류 |
| 17.5 | [쿼리와 성능 문제](./performance/) | 느린 쿼리, 빈 결과, 메모리, 트랜잭션 충돌 |
| 17.6 | [자동 처리 문제](./automation/) | ROLLUP과 STREAM 실행 오류 |
| 17.7 | [백업과 복구 문제](./recovery-backup/) | BACKUP, RESTORE, MOUNT, UMOUNT 오류 |
| 17.8 | [Cluster 문제](./cluster/) | 노드 상태와 Cluster Edition 오류 |

문제를 해결한 뒤에는 원인, 조치, 확인 쿼리와 재발 방지 항목을 운영 기록에 남깁니다.
