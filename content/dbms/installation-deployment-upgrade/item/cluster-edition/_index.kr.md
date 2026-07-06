---
type: docs
title: 'Cluster Edition 업그레이드'
weight: 20
---

Cluster Edition 업그레이드는 서비스 중단 여부에 따라 두 가지 방식을 선택합니다.

| 방식 | 서비스 중단 | 적합한 상황 |
|------|-----------|------------|
| [온라인 업그레이드](/dbms/installation-deployment-upgrade/item/cluster-edition/online/) | 없음 (무중단) | 24/7 운영 환경 |
| [전체 중지 업그레이드](/dbms/installation-deployment-upgrade/item/cluster-edition/full-stop/) | 있음 | 유지보수 창이 허용되는 경우, Major 버전 변경 |

## 업그레이드 전 공통 주의사항

- 업그레이드 중에는 DDL 또는 DELETE를 실행하지 마십시오.
- 업그레이드 중 노드 추가·시작·종료·삭제 작업을 병행하지 마십시오.
- INSERT·APPEND·SELECT는 Coordinator 업그레이드 중에도 계속 동작합니다.
- 업그레이드 전 백업을 권장합니다.

---

**다음 읽을 내용**
- [온라인 업그레이드](/dbms/installation-deployment-upgrade/item/cluster-edition/online/)
- [전체 중지 업그레이드](/dbms/installation-deployment-upgrade/item/cluster-edition/full-stop/)
