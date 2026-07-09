---
type: docs
title: 'Lookup / Broker / Warehouse 설치'
weight: 30
toc: true
---

Coordinator와 Deployer가 준비된 후 Lookup, Broker, Warehouse 노드를 Coordinator에 등록하고 시작합니다.
Broker와 Warehouse를 등록하기 전에 경량 패키지를 Coordinator에 `--add-package`로 등록해야 합니다.

## Broker 설치

### 1. machbase.conf 설정

각 Broker 노드의 `machbase.conf`를 편집합니다.

```
CLUSTER_LINK_HOST    = 192.168.1.11   # Broker 노드 IP
CLUSTER_LINK_PORT_NO = 5401
PORT_NO              = 5656           # 클라이언트 접속 포트
```

### 2. Coordinator에 노드 등록

Coordinator 노드에서 실행합니다.

```bash
machcoordinatoradmin --add-node="192.168.1.11:5401" \
  --node-type=broker \
  --deployer="192.168.1.10:5201" \
  --package-name=machbase \
  --home-path="/home/machbase/broker" \
  --port-no=5656 \
  --http-port-no=5402
```

| 파라미터 | 설명 |
|---------|------|
| `--add-node` | 등록할 노드의 IP:CLUSTER_LINK_PORT_NO |
| `--node-type` | `broker` / `warehouse` / `lookup` |
| `--deployer` | 해당 노드를 설치하고 제어할 Deployer의 IP:CLUSTER_LINK_PORT_NO |
| `--package-name` | Coordinator에 등록한 패키지 이름 |
| `--home-path` | 노드 홈 디렉터리 |
| `--port-no` | 클라이언트 또는 노드 서비스 포트 |
| `--http-port-no` | HTTP 관리 포트 |

### 3. 노드 시작

Coordinator에서 해당 노드를 시작합니다.

```bash
machcoordinatoradmin --startup-node="192.168.1.11:5401"
```

## Warehouse 설치

Warehouse 노드는 그룹 단위로 구성합니다. 같은 그룹의 노드끼리 데이터를 복제합니다.

### 1. machbase.conf 설정

```
CLUSTER_LINK_HOST    = 192.168.1.13
CLUSTER_LINK_PORT_NO = 5501
PORT_NO              = 5500
```

### 2. 노드 등록

```bash
machcoordinatoradmin --add-node="192.168.1.13:5501" \
  --node-type=warehouse \
  --deployer="192.168.1.10:5201" \
  --package-name=machbase \
  --home-path="/home/machbase/warehouse_g1_1" \
  --port-no=5500 \
  --http-port-no=5502 \
  --group=group1 \
  --no-replicate

machcoordinatoradmin --add-node="192.168.1.14:5501" \
  --node-type=warehouse \
  --deployer="192.168.1.10:5201" \
  --package-name=machbase \
  --home-path="/home/machbase/warehouse_g1_2" \
  --port-no=5500 \
  --http-port-no=5502 \
  --group=group1 \
  --no-replicate
```

별도 `--add-group` 명령은 사용하지 않습니다. Warehouse 그룹 이름은 각 Warehouse 노드를 등록할 때
`--group`으로 지정합니다.

### 3. 노드 시작

```bash
machcoordinatoradmin --startup-node="192.168.1.13:5501"
machcoordinatoradmin --startup-node="192.168.1.14:5501"
```

## Lookup 노드 (선택)

Lookup 노드는 참조 데이터를 위한 전용 노드입니다. 구성할 때는 `--lookup-type`을 함께 지정합니다.

```bash
machcoordinatoradmin --add-node="192.168.1.30:5301" \
  --node-type=lookup \
  --lookup-type=master \
  --deployer="192.168.1.10:5201" \
  --home-path="/home/machbase/lookup"
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
