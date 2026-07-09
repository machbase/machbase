---
type: docs
title: '3.4.2 Cluster Edition 업그레이드'
weight: 20
toc: true
---

Cluster Edition 업그레이드는 서비스 중단 여부에 따라 두 가지 방식을 선택합니다.

| 방식 | 서비스 중단 | 적합한 상황 |
|------|-----------|------------|
| [온라인 업그레이드](/kr/dbms/installation-deployment-upgrade/upgrade/cluster-edition/online/) | Broker/Warehouse 순차 재기동 | Broker와 Warehouse만 교체하는 운영 환경 |
| [전체 중지 업그레이드](/kr/dbms/installation-deployment-upgrade/upgrade/cluster-edition/full-stop/) | 있음 | 유지보수 창이 허용되는 경우, Major 버전 변경 |

## 업그레이드 전 공통 주의사항

- 업그레이드 중에는 DDL 또는 DELETE를 실행하지 마십시오.
- 업그레이드 중 노드 추가·시작·종료·삭제 작업을 병행하지 마십시오.
- 온라인 업그레이드는 Broker와 Warehouse를 대상으로 합니다. Coordinator, Deployer, Lookup까지 교체하려면 전체 중지 업그레이드를 사용합니다.
- 업그레이드 전 백업을 권장합니다.

---

**다음 읽을 내용**
- [온라인 업그레이드](/kr/dbms/installation-deployment-upgrade/upgrade/cluster-edition/online/)
- [전체 중지 업그레이드](/kr/dbms/installation-deployment-upgrade/upgrade/cluster-edition/full-stop/)
