---
type: docs
title: '13.7.7 Warehouse 상태 복구'
weight: 70
---

Warehouse 노드에 장애가 발생하면 해당 노드의 상태가 `scrapped`, `inactive`, `**unknown**` 등으로 전환될 수 있습니다. 장애 유형에 따라 자동 복구 또는 수동 복구를 수행합니다.

## 장애 유형과 복구 방법

| 장애 유형 | 증상 | 복구 방법 |
|-----------|------|-----------|
| 일시적 네트워크 단절 | `**unknown**` 또는 `inactive` | 네트워크 복구 후 자동 재연결 |
| 프로세스 비정상 종료 | `**unknown**` 또는 `inactive` | 노드 재시작 |
| 데이터 손상 | scrapped | Snapshot 복구 또는 강제 복구 |
| 디스크 장애 | scrapped | 디스크 교체 후 데이터 복구 |

## 자동 복구

네트워크 단절이나 일시적 프로세스 오류의 경우, Coordinator가 자동으로 노드 재연결을 시도합니다. `CLUSTER_LINK_CONNECT_RETRY_TIMEOUT` 설정 내에 연결이 복구되면 자동으로 `normal` 상태로 전환됩니다.

```bash
# 복구 진행 확인
machcoordinatoradmin --cluster-status
```

`sync-standby`, `sync-active`, `ddl-recovering` 등의 전환 상태가 `normal` 상태로 돌아올 때까지 대기합니다.

## 수동 복구: 노드 재시작

프로세스가 종료된 경우 해당 노드를 재시작합니다.

```bash
# 1. 장애 노드 상태 확인
machcoordinatoradmin --cluster-status

# 2. 노드 시작 (Coordinator가 접근 가능한 경우)
machcoordinatoradmin --startup-node=warehouse-a1

# 3. 또는 해당 호스트에 직접 접속하여 시작
export MACHBASE_HOME=/home/machbase/warehouse_a1
machadmin -u

# 4. 상태 복귀 확인
machcoordinatoradmin --cluster-status
```

## Snapshot 복구

데이터 손상으로 노드가 `scrapped` 상태인 경우 Snapshot 기능으로 복구합니다.

### Snapshot 실행 (사전 준비)

정기적으로 Snapshot을 실행해 복구 포인트를 만들어 두어야 합니다.

```bash
# Snapshot 주기 설정 (초 단위)
machcoordinatoradmin --snapshot-interval=3600

# 즉시 Snapshot 실행
machcoordinatoradmin --exec-snapshot --group=Group1
```

### Snapshot으로 복구

```bash
# scrapped 노드를 Snapshot 기반으로 복구
machcoordinatoradmin --snapshot-recover=warehouse-a1
```

### Snapshot 정리

오래된 Snapshot을 정리하여 디스크 공간을 확보합니다.

```bash
machcoordinatoradmin --snapshot-clean
```

## Sync 복구

다른 노드와 데이터를 동기화하여 복구합니다.

```bash
# 지정 노드에 Sync 실행 (다른 노드로부터 데이터 동기화)
machcoordinatoradmin --exec-sync=warehouse-a1
```

## 강제 복구

Snapshot이 없거나 Sync가 불가능한 경우, `scrapped` 상태의 노드를 강제로 복구합니다. 단, 강제 복구 후 해당 노드의 데이터 일관성은 보장되지 않습니다.

```bash
# scrapped 노드 강제 복구
machcoordinatoradmin --force-restore-warehouse=warehouse-a1
```

강제 복구 후 반드시 데이터 일관성을 검증합니다.

## 복구 후 확인

```bash
# 전체 클러스터 상태 확인
machcoordinatoradmin --cluster-status

# 특정 노드 상세 정보
machcoordinatoradmin --list-node=warehouse-a1
```

복구된 노드의 `Actual State`가 `normal`로 표시되고 `Desired State`와 일치하면 복구가 완료된 것입니다.

## 복구 불가 시 조치

복구가 불가능한 경우 해당 노드를 클러스터에서 제거하고 새 노드로 교체합니다.

```bash
# 1. 노드 제거
machcoordinatoradmin --remove-node=warehouse-a1

# 2. 새 노드 추가
machcoordinatoradmin \
  --add-node=192.168.0.32:5401 \
  --node-type=warehouse \
  --deployer=192.168.0.32:5201 \
  --package-name=machbase \
  --home-path=/home/machbase/warehouse_a1 \
  --port-no=5400 \
  --group=Group1 \
  --alias=warehouse-a1

# 3. 노드 시작
machcoordinatoradmin --startup-node=warehouse-a1
```

노드 교체 이후 데이터 재분산이 필요한지 확인하고, 필요하다면 `--exec-sync`로 동기화합니다.
