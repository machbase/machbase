---
type: docs
title: 'Cluster 노드 상태가 비정상일 때'
weight: 10
---

Cluster Edition에서 특정 노드가 비정상 상태로 전환되면 데이터 입력, 쿼리, 또는 클러스터 전체 기능에 영향을 미칠 수 있습니다. 노드 상태를 확인하고 복구하는 방법을 설명합니다.

## 노드 상태 확인

클러스터 전체 상태를 확인합니다.

```bash
# 클러스터 상태 전체 확인
machclusterctl status
```

또는 Coordinator를 통해 상세 상태를 조회합니다.

```bash
machcoordinatoradmin --cluster-status-full
```

SQL로도 노드 상태를 조회할 수 있습니다.

```sql
SELECT host, nodetype, state, coord_host, coord_http_admin_port
  FROM v$node_status;
```

## 비정상 상태 유형과 조치

| 상태 | 의미 | 조치 |
|------|------|------|
| `STOPPED` | 프로세스가 종료된 상태 | 해당 노드에서 `machadmin -u` 실행 |
| `DISCONNECTED` | 네트워크 단절 | 네트워크 상태 확인 후 재연결 대기 |
| `ERROR` | 내부 오류 발생 | 해당 노드 트레이스 로그 확인 |
| `scrapped` | 데이터 손상 또는 복구 불가 상태 | Snapshot 복구 또는 강제 복구 |

## Warehouse 노드 재기동

Warehouse 노드가 `STOPPED` 상태인 경우 해당 노드에서 직접 재기동합니다.

```bash
# 1. 장애 노드 확인
machcoordinatoradmin --cluster-status-full

# 2. Coordinator에서 노드 시작 (Coordinator가 접근 가능한 경우)
machcoordinatoradmin --startup-node=warehouse-a1

# 3. 또는 해당 호스트에 직접 접속하여 시작
export MACHBASE_HOME=/home/machbase/warehouse_a1
machadmin -u

# 4. 상태 복귀 확인
machcoordinatoradmin --cluster-status-full
```

## Broker 노드 확인

Broker 노드에 이상이 있으면 클라이언트 연결 전체가 영향을 받습니다.

```bash
# Broker 상태 확인
machcoordinatoradmin --cluster-status-full | grep -i broker
```

Broker가 응답하지 않으면 해당 Broker 호스트에서 프로세스를 확인하고 재기동합니다.

## Coordinator 상태 확인

Coordinator가 비정상이면 클러스터 메타 변경 및 장애 조치가 불가합니다.

```bash
# Coordinator 상태 확인
machcoordinatoradmin --cluster-status-full
```

Primary Coordinator에 장애가 발생했고 Secondary Coordinator가 구성되어 있다면, Secondary가 자동으로 Primary로 승격됩니다. Secondary가 없다면 Primary를 수동으로 재기동해야 합니다.

## 노드 트레이스 로그 확인

오류 원인을 상세히 파악하려면 해당 노드의 트레이스 로그를 확인합니다.

```bash
# 해당 노드 로그 확인
grep -i "error\|fatal\|assert" $MACHBASE_HOME/trc/machbase.trc | tail -50
```

## 상세 복구 절차

Warehouse 노드의 데이터 손상(`scrapped` 상태) 복구, Snapshot 활용, 강제 복구 방법에 대한 상세 내용은 다음을 참고하십시오.

- [Warehouse 상태 복구](../../../operations-configuration-recovery/cluster/recovery-state-status-warehouse/)
- [Cluster 노드 상태와 전환](../../../operations-configuration-recovery/cluster/state-alter-status-cluster/)
