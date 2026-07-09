---
type: docs
title: '13.7.1 Cluster 상태 확인'
weight: 10
---

클러스터 상태를 정기적으로 확인하여 모든 노드가 정상 동작 중인지 점검합니다.

## machcoordinatoradmin으로 상태 확인

### 기본 상태 출력

```bash
machcoordinatoradmin --cluster-status
```

출력 예:

```
+-------------+-------------------+-------------------+-------------------+--------------+
|  Node Type  |     Node Name     |    Group Name     |    Group State    |     State    |
+-------------+-------------------+-------------------+-------------------+--------------+
| coordinator | 192.168.0.32:5101 | Coordinator       | normal            | primary      |
| deployer    | 192.168.0.32:5201 | Deployer          | normal            | normal       |
| broker      | 192.168.0.32:5301 | Broker            | normal            | leader       |
| warehouse   | 192.168.0.32:5401 | Group1            | normal            | normal       |
+-------------+-------------------+-------------------+-------------------+--------------+
```

### 상세 상태 출력 (Desired vs Actual State)

```bash
machcoordinatoradmin --cluster-status-full
```

`Desired State`와 `Actual State`를 함께 표시합니다. 두 값이 다른 노드는 상태 전환 중이거나 문제가 있는 노드입니다.

### Deployer 상태 포함 출력

```bash
machcoordinatoradmin --cluster-status --verbose
```

### 클러스터 전체 정보 출력

```bash
machcoordinatoradmin --cluster-node
```

출력 예:

```
Token Pid      : 29245
Token Time     : 1553153902646178
Cluster Status : Service
Broker         : 192.168.0.32:5301
Warehouse      : 192.168.0.32:5401
```

`Cluster Status`가 `Service`이면 클러스터가 정상 서비스 중입니다.

## SQL로 노드 상태 확인

machsql 또는 애플리케이션에서 SQL로 노드 상태를 조회할 수 있습니다.

### 노드 상태 조회

```sql
-- 전체 클러스터 노드 상태
SELECT * FROM v$cluster_node_status;

-- Warehouse 노드 상태
SELECT * FROM v$warehouse_node_status;
```

## 노드 상태 값

| 상태 | 의미 |
|------|------|
| `normal` | 정상 동작 중 |
| `primary` | Coordinator Primary 상태 |
| `leader` | Broker Leader 상태 |
| `readonly` | 읽기 전용 상태 (그룹 상태) |
| `sync-standby` | 동기화 대기 상태 |
| `sync-active` | 동기화 진행 상태 |
| `scrapped` | 데이터 손상 또는 복구 필요 상태 |
| `inactive` | 비활성 상태 |
| `**unknown**` | 상태 미확인 또는 연결 불가 |
| `ddl-recovering` | DDL 복구 중 |

## 클러스터 상태 값 (Cluster Status)

| 상태 | 의미 |
|------|------|
| `Service` | 정상 서비스 중 |
| `Deactivate` | 비활성화 상태 |

## 호스트 리소스 모니터링

클러스터 노드가 위치한 호스트의 CPU·메모리·디스크·네트워크 사용량을 확인할 수 있습니다.

```bash
# 리소스 수집 활성화
machcoordinatoradmin --host-resource-enable

# 전체 호스트 리소스 확인
machcoordinatoradmin --get-host-resource

# 특정 메트릭만 확인
machcoordinatoradmin --get-host-resource --metric=cpu
machcoordinatoradmin --get-host-resource --metric=disk

# 특정 호스트만 확인
machcoordinatoradmin --get-host-resource --host=192.168.0.32

# 리소스 수집 비활성화
machcoordinatoradmin --host-resource-disable
```

## 정기 상태 확인 스크립트 예

```bash
#!/bin/bash
# 클러스터 상태 확인 후 비정상 노드 감지

OUTPUT=$(machcoordinatoradmin --cluster-status 2>&1)
echo "$OUTPUT"

# unknown 또는 scrapped 상태 노드 감지
if echo "$OUTPUT" | grep -qE '\\*\\*unknown\\*\\*|scrapped'; then
  echo "[경고] 비정상 노드가 감지되었습니다. 즉시 확인하십시오."
fi
```
