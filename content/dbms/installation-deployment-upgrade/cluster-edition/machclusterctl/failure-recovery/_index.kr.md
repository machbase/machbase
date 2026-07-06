---
type: docs
title: '배포 실패 시 복구'
weight: 60
---

`machclusterctl install` 또는 `apply` 실행 중 오류가 발생한 경우 복구 방법을 설명합니다.

## 설치 실패 시 재시도

설치 도중 일부 노드에서 실패한 경우 원인을 해결한 후 동일한 명령을 다시 실행합니다. `machclusterctl`은 이미 완료된 노드는 건너뛰고 실패한 노드부터 재개합니다.

```bash
machclusterctl install -f cluster.yaml
```

## 클러스터 전체 초기화 후 재설치

오류 상태가 복잡하여 처음부터 다시 시작해야 하는 경우:

```bash
# 클러스터 전체 종료
machclusterctl stop -f cluster.yaml

# 클러스터 제거 (데이터 포함)
machclusterctl uninstall -f cluster.yaml

# 재설치
machclusterctl install -f cluster.yaml
machclusterctl start -f cluster.yaml
```

`uninstall`은 각 노드의 데이터 디렉터리를 포함하여 삭제합니다. **데이터 복구가 불가능하므로 주의하십시오.**

## Warehouse 노드 장애 복구

특정 Warehouse 노드에 장애가 발생하면 해당 노드의 상태가 `scrapped`로 전환됩니다. 복구 절차는 다음과 같습니다.

```bash
# 1. 그룹 상태를 readonly로 변경 (추가 데이터 유입 방지)
machcoordinatoradmin --set-group-state=readonly --group=group1

# 2. 장애 노드 재시작 또는 복구

# 3. 스냅샷 기반 복구 (Snapshot Failover)
machcoordinatoradmin --snapshot-recover=192.168.1.13:5401

# 4. 스냅샷 이후 데이터 복제 동기화
machcoordinatoradmin --exec-sync=192.168.1.13:5401

# 5. 그룹 상태를 normal로 복원
machcoordinatoradmin --set-group-state=normal --group=group1
```

## 로그 확인

각 노드의 `trc/machbase.trc` 파일에서 오류 원인을 확인합니다.

```bash
ssh machbase@<node-ip> 'tail -100 /home/machbase/coordinator/trc/machbase.trc'
```

---

**다음 읽을 내용**
- [노드 상태 확인](/dbms/installation-deployment-upgrade/cluster-edition/machclusterctl/status-check-state/)
- [설치 검증 체크리스트](/dbms/installation-deployment-upgrade/validation-checklist/)
