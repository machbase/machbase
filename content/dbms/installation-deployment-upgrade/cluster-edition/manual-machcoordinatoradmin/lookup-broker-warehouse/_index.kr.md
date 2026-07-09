---
type: docs
title: 'Lookup / Broker / Warehouse 설치'
weight: 30
toc: true
---

Coordinator와 Deployer가 준비된 후 Lookup, Broker, Warehouse 노드를 Coordinator에 등록하고 시작합니다.
Broker와 Warehouse를 등록하기 전에 경량 패키지를 Coordinator에 `--add-package`로 등록해야 합니다.

## Broker 설치

### 1. 등록 파라미터 확인

Broker 설정 파일은 `--add-node` 실행 때 생성되어 Deployer를 통해 대상 노드에 배포됩니다. 등록 전에
사용할 cluster link 포트, 서비스 포트, HTTP 포트를 확정합니다.

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
  --dbs-path="/data/machbase/broker_dbs" \
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
| `--dbs-path` | Broker/Warehouse의 데이터 파일 경로. 생략하면 기본 `DBS_PATH`를 사용 |
| `--port-no` | 클라이언트 또는 노드 서비스 포트 |
| `--http-port-no` | Broker HTTP 포트입니다. Warehouse HTTP 포트를 사용하는 버전에서는 Warehouse에도 지정합니다. |
| `--replication` | Warehouse replication manager 주소입니다. `host:port` 형식을 사용합니다. |

### 3. 노드 시작

Coordinator에서 해당 노드를 시작합니다.

```bash
machcoordinatoradmin --startup-node="192.168.1.11:5401"
```

## Warehouse 설치

Warehouse 노드는 그룹 단위로 구성합니다. 같은 그룹의 노드끼리 데이터를 복제합니다.

### 1. 등록 파라미터 확인

Warehouse 설정 파일은 `--add-node` 실행 때 생성되어 Deployer를 통해 대상 노드에 배포됩니다. 등록
전에 cluster link 포트, 서비스 포트, replication manager 주소를 확정합니다.

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
  --dbs-path="/data/machbase/warehouse_g1_1_dbs" \
  --port-no=5500 \
  --replication=192.168.1.13:5502 \
  --group=group1 \
  --no-replicate

machcoordinatoradmin --add-node="192.168.1.14:5501" \
  --node-type=warehouse \
  --deployer="192.168.1.10:5201" \
  --package-name=machbase \
  --home-path="/home/machbase/warehouse_g1_2" \
  --dbs-path="/data/machbase/warehouse_g1_2_dbs" \
  --port-no=5500 \
  --replication=192.168.1.14:5502 \
  --group=group1
```

별도 `--add-group` 명령은 사용하지 않습니다. Warehouse 그룹 이름은 각 Warehouse 노드를 등록할 때
`--group`으로 지정합니다.

Tag update가 반영된 빌드에서 Warehouse HTTP 포트를 별도로 지정해야 하는 경우에는 Warehouse
`--add-node`에 `--http-port-no`를 추가합니다. `main` 또는 RDB 구현 브랜치 기반 빌드에서는
Warehouse 설정 생성 시 `HTTP_PORT_NO`를 기록하지 않습니다.

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

Coordinator, Lookup, Broker, Warehouse가 각 역할에 맞는 정상 상태로 표시되면 클러스터가 정상
구동 중입니다. Coordinator는 `primary`, Broker는 `leader`, Warehouse는 `normal`,
`sync-active`, `sync-standby` 등으로 표시될 수 있습니다.

---

**다음 읽을 내용**
- [노드 상태 확인](/kr/dbms/installation-deployment-upgrade/cluster-edition/manual-machcoordinatoradmin/status-check-node-state/)
