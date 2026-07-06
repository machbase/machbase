---
type: docs
title: 'Lookup / Broker / Warehouse 설치'
weight: 30
---

Coordinator와 Deployer가 준비된 후 Broker와 Warehouse 노드를 Coordinator에 등록하고 시작합니다.

## Broker 설치

### 1. machbase.conf 설정

각 Broker 노드의 `machbase.conf`를 편집합니다.

```
CLUSTER_LINK_HOST    = 192.168.1.11   # Broker 노드 IP
CLUSTER_LINK_PORT_NO = 5301
PORT_NO              = 5656           # 클라이언트 접속 포트
```

### 2. Coordinator에 노드 등록

Coordinator 노드에서 실행합니다.

```bash
machcoordinatoradmin --add-node="192.168.1.11:5301" --node-type=broker
```

| 파라미터 | 설명 |
|---------|------|
| `--add-node` | 등록할 노드의 IP:CLUSTER_LINK_PORT_NO |
| `--node-type` | `coordinator` / `deployer` / `broker` / `warehouse` |

### 3. 노드 시작

Coordinator에서 해당 노드를 시작합니다.

```bash
machcoordinatoradmin --startup-node="192.168.1.11:5301"
```

## Warehouse 설치

Warehouse 노드는 그룹 단위로 구성합니다. 같은 그룹의 노드끼리 데이터를 복제합니다.

### 1. machbase.conf 설정

```
CLUSTER_LINK_HOST    = 192.168.1.13
CLUSTER_LINK_PORT_NO = 5401
PORT_NO              = 5656
```

### 2. 그룹 생성 및 노드 등록

```bash
# 그룹 생성
machcoordinatoradmin --add-group=group1

# 노드를 그룹에 등록
machcoordinatoradmin --add-node="192.168.1.13:5401" --node-type=warehouse --group=group1
machcoordinatoradmin --add-node="192.168.1.14:5401" --node-type=warehouse --group=group1
```

### 3. 노드 시작

```bash
machcoordinatoradmin --startup-node="192.168.1.13:5401"
machcoordinatoradmin --startup-node="192.168.1.14:5401"
```

## Lookup 노드 (선택)

Lookup 노드는 참조 데이터를 위한 전용 노드입니다. 구성이 필요한 경우 동일한 방식으로 등록합니다.

```bash
machcoordinatoradmin --add-node="192.168.1.30:5501" --node-type=lookup
```

## 전체 상태 확인

모든 노드 등록 후 상태를 확인합니다.

```bash
machcoordinatoradmin --cluster-status
```

모든 노드가 `normal` 상태이면 클러스터가 정상 구동 중입니다.

---

**다음 읽을 내용**
- [노드 상태 확인](/dbms/installation-deployment-upgrade/cluster-edition/manual-machcoordinatoradmin/status-check-node-state/)
