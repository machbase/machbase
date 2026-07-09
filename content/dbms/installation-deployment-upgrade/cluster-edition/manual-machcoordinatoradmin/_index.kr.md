---
type: docs
title: 'machcoordinatoradmin 기반 수동 배포'
weight: 40
toc: true
---

`machclusterctl`을 사용할 수 없거나 각 노드를 직접 제어해야 하는 경우 수동으로 클러스터를 구성합니다. 각 노드에 직접 SSH 접속하여 패키지 배포, 설정, 시작을 수행합니다.

## 수동 배포 순서

1. [Package 등록](/dbms/installation-deployment-upgrade/cluster-edition/manual-machcoordinatoradmin/package/) — 각 노드에 패키지 배포
2. [Coordinator / Deployer 설치](/dbms/installation-deployment-upgrade/cluster-edition/manual-machcoordinatoradmin/coordinator-deployer/) — 핵심 관리 노드 구동
3. [Lookup / Broker / Warehouse 설치](/dbms/installation-deployment-upgrade/cluster-edition/manual-machcoordinatoradmin/lookup-broker-warehouse/) — 데이터 처리 노드 등록 및 구동
4. [노드 상태 확인](/dbms/installation-deployment-upgrade/cluster-edition/manual-machcoordinatoradmin/status-check-node-state/) — 클러스터 정상 동작 검증

## machclusterctl 대비 차이점

| 항목 | machclusterctl | 수동 배포 |
|------|---------------|----------|
| 설정 방식 | cluster.yaml 단일 파일 | 각 노드 machbase.conf 직접 편집 |
| 패키지 배포 | 자동 원격 복사 | 수동 SCP/rsync |
| 노드 등록 | 자동 | `machcoordinatoradmin --add-node` 수동 실행 |
| 일괄 시작·종료 | `machclusterctl start/stop` | 노드별 개별 실행 |

수동 배포는 유연성이 높지만 실수 가능성도 높습니다. 신규 구축에는 `machclusterctl`을 권장합니다.

---

**다음 읽을 내용**
- [Package 등록](/dbms/installation-deployment-upgrade/cluster-edition/manual-machcoordinatoradmin/package/)
