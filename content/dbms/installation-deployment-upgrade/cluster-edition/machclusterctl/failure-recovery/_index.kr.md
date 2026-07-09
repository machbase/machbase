---
type: docs
title: '3.3.3.6 배포 실패 시 복구'
weight: 60
toc: true
---

`machclusterctl install` 또는 `apply` 실행 중 오류가 발생한 경우 복구 방법을 설명합니다.

## 설치 실패 시 재시도

설치 도중 오류가 발생하면 `machclusterctl install`은 이미 수행한 bootstrap과 노드 등록 작업을
rollback합니다. 먼저 로그에서 원인을 해결한 뒤 동일한 명령을 다시 실행합니다.

`machclusterctl apply` 중 오류가 발생한 경우에는 현재 상태를 먼저 확인합니다. 일부 노드 추가나 시작이
진행된 뒤 실패했을 수 있으므로, 상태에 맞게 `apply`를 재실행하거나 필요한 노드를 수동으로 정리합니다.

```bash
machclusterctl install -f cluster.yaml --yes --verbose
```

## 클러스터 전체 초기화 후 재설치

오류 상태가 복잡하여 처음부터 다시 시작해야 하는 경우:

```bash
# 클러스터 전체 종료
machclusterctl stop

# 클러스터 제거 (데이터 포함)
machclusterctl destroy -f cluster.yaml --yes

# 재설치
machclusterctl install -f cluster.yaml --yes --verbose
```

`destroy`는 각 노드의 설치 흔적과 관리 대상 데이터 경로를 삭제할 수 있습니다. 외부 `dbs_path`
처리 범위는 버전에 따라 다를 수 있으므로, 데이터 보존 목적으로 `destroy`를 사용하지 마십시오.
**삭제된 데이터는 복구할 수 없으므로 주의하십시오.**

## Warehouse 노드 장애 복구

특정 Warehouse 노드에 장애가 발생하면 해당 노드의 상태가 `scrapped`로 전환됩니다. 복구 절차는 다음과 같습니다.

```bash
# 1. 그룹 상태를 readonly로 변경 (추가 데이터 유입 방지)
machcoordinatoradmin --set-group-state=readonly --group=group1

# 2. 장애 노드 재시작 또는 복구

# 3. 스냅샷 기반 복구 (Snapshot Failover)
machcoordinatoradmin --snapshot-recover=192.168.1.13:5501

# 4. 복구 대상 Warehouse 동기화 실행
machcoordinatoradmin --exec-sync=192.168.1.13:5501

# 5. Warehouse 상태가 sync-standby를 거쳐 normal로 전환되는지 확인한 뒤 그룹 상태 복원
machcoordinatoradmin --cluster-status-full --verbose
machcoordinatoradmin --set-group-state=normal --group=group1
```

스냅샷 복구는 대상 Warehouse가 `scrapped`, Warehouse 그룹이 `readonly` 상태일 때 수행합니다.
복구 명령 뒤에는 `--exec-sync`를 실행하고, Warehouse가 `sync-standby`를 거쳐 `normal` 상태가
되는지 확인합니다.

## 로그 확인

각 노드의 `trc/machbase.trc` 파일에서 오류 원인을 확인합니다.

```bash
ssh machbase@<node-ip> 'tail -100 /home/machbase/coordinator/trc/machbase.trc'
```

---

**다음 읽을 내용**
- [노드 상태 확인](/kr/dbms/installation-deployment-upgrade/cluster-edition/machclusterctl/status-check-state/)
- [설치 검증 체크리스트](/kr/dbms/installation-deployment-upgrade/validation-checklist/)
