---
title : 'Lookup / Broker / Warehouse 설치'
type: docs
weight: 30
---

## Lookup 설치

Coordinator 노드에서 lookup 노드를 추가합니다. 여러 개의 lookup 노드를 등록할 수 있습니다.

서버에 deployer 노드가 사전에 설치되어 있어야 합니다.

deployer 노드가 설치되면 모든 작업은 coordinator 노드에서 수행되며, 서버에 접속하여 설정할 것은 없습니다.

```bash
# lookup master 노드 추가
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-node="192.168.0.84:5301"  \
        --node-type=lookup --lookup-type=master --deployer="192.168.0.84:5201"      \
        --home-path="/home/machbase/lookup1"


# lookup monitor 노드 추가
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-node="192.168.0.84:5302"  \
        --node-type=lookup --lookup-type=monitor --deployer="192.168.0.84:5201"         \
        --home-path="/home/machbase/lookupm1"


# lookup slave 노드 추가
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-node="192.168.0.84:5303"  \
        --node-type=lookup --lookup-type=slave --deployer="192.168.0.84:5201"       \
        --home-path="/home/machbase/lookup3"


# lookup 노드 실행
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --startup-node="192.168.0.84:5301"

# lookup 노드들을 일괄 실행할 수 있습니다
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --startup-lookup
```

|옵션|설명|예시|
|--|--|--|
|--add-node|추가할 노드 이름을 "IP:PORT"로 지정합니다.|192.168.0.84:5301|
|--node-type|노드 타입을 지정합니다.<br>coordinator, deployer, lookup, broker, warehouse 다섯 가지가 있습니다.|lookup|
|--deployer|설치할 서버의 deployer 노드 정보를 등록합니다.|192.168.0.84:5201|
|--lookup-type|lookup 타입을 지정합니다.<br>master, slave, monitor 세 가지가 있습니다.|master|
|--home-path|설치할 경로를 지정합니다.<br>machbase 계정에서 /home/machbase/lookup을 지정합니다.|/home/machabse/lookup|

### 설치 조건

Lookup 노드는 Master, Slave, Monitor 3가지 타입이 있으며, 아래 조건에 따라 설치해야 합니다.

    1. Lookup Master 노드
        a. 반드시 하나만 존재해야 하는 Lookup 노드입니다.
        b. Monitor 및 Slave 노드보다 먼저 설치해야 합니다.
    2. Lookup Monitor 노드
        a. 최소 하나 이상 존재해야 하는 Lookup 노드입니다.
        b. 안정적인 HA를 위해 각 서버마다 하나씩 있어야 합니다.
    3. Lookup Slave 노드
        a. HA를 위해 하나 이상 있는 것을 권장합니다. (없으면 HA를 보장할 수 없습니다)


## Lookup 삭제

Coordinator 노드에서 broker 노드를 제거합니다.

```bash
# lookup 노드 삭제
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --remove-node="192.168.0.84:5301"
```


## Lookup 종료/중지

Coordinator 노드에서 lookup 노드를 종료/중지합니다.

```bash

# lookup 노드 종료
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --shutdown-node="192.168.0.84:5301"

# lookup 노드들을 일괄 종료할 수 있습니다
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --shutdown-lookup
```


## Lookup Master 변경

coordinator 노드에서 lookup master 노드를 변경할 수 있습니다.

lookup slave만 lookup master로 변경할 수 있으며, 기존 lookup master는 lookup slave가 됩니다.

```bash
# lookup master 변경
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --set-lookup-master="192.168.0.84:5301"
```


## Broker 설치

coordinator 노드에서 broker 노드를 추가합니다. 여러 개의 broker 노드 등록이 가능합니다.

서버에 deployer 노드가 사전에 설치되어 있어야 합니다.

deployer 노드가 설치되면 coordinator 노드에서 모든 작업이 가능하므로 서버에 접속하여 설정할 것은 없습니다.

처음 등록되는 노드가 leader broker가 되고, 추가로 등록되는 노드는 follower broker가 됩니다.

```bash
# broker 노드 추가
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-node="192.168.0.84:5301"  \
        --node-type=broker --deployer="192.168.0.84:5201" --port-no="5656"          \
        --home-path="/home/machbase/broker" --package-name=machbase

# broker 노드 실행
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --startup-node="192.168.0.84:5301"
```

|옵션|설명|예시|
|--|--|--|
|--add-node|추가할 노드 이름을 "IP:PORT"로 지정합니다.<br>PORT 값은 CLUSTER_LINK_PORT_NO 값으로 설정됩니다.|192.168.0.84:5301|
|--node-type|노드 타입을 지정합니다.<br>coordinator, deployer, lookup, broker, warehouse 다섯 가지가 있습니다.|broker|
|--deployer|설치할 서버의 deployer 노드 정보를 등록합니다.|192.168.0.84:5201|
|--port-no|'machbased' 포트를 지정합니다.<br>Broker는 기본값 5656을 지정합니다.<br>이 포트는 클라이언트 및 machsql 연결 시 사용됩니다.|5656|
|--home-path|설치할 경로를 지정합니다.<br>machbase 계정에서 /home/machbase/broker를 지정합니다.|/home/machbase/broker|
|--package-name|패키지 추가 시 지정한 패키지 이름을 설정합니다.|machbase|


## Broker 삭제

Coordinator 노드에서 broker 노드를 제거합니다.

```bash
# broker 노드 삭제
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --remove-node="192.168.0.84:5301"
```


## Broker 종료/중지

Coordinator 노드에서 broker 노드를 종료/중지하는 방법이 있습니다.

```bash
# broker 노드 종료
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --shutdown-node="192.168.0.84:5301"

# broker 노드 중지
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --kill-node="192.168.0.84:5301"
```

또는 broker가 설치된 서버에서 직접 프로세스를 종료/중지할 수 있습니다.

```bash
# broker 노드 종료
$MACHBASE_HOME/bin/machadmin -s

# broker 노드 중지
$MACHBASE_HOME/bin/machadmin -k
```


## Warehouse 설치

Coordinator 노드에서 active 노드와 standby 노드를 설치합니다.

사전에 설치된 deployer를 통해 설치됩니다.

### Group 1 설치

첫 번째 Warehouse Group1 노드를 설치합니다.

```bash
# group1 warehouse 설치
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-node="192.168.0.83:5401"  \
        --node-type=warehouse --deployer="192.168.0.83:5201" --port-no="5400"       \
        --home-path="/home/machbase/warehouse_g1" --package-name=machbase           \
        --replication="192.168.0.83:5402"  --group="group1" --no-replicate

# 설치된 노드 실행
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --startup-node="192.168.0.84:5401"
```

|옵션|설명|예시|
|--|--|--|
|--add-node|추가할 노드 이름을 "IP:PORT"로 지정합니다.<br>PORT 값은 CLUSTER_LINK_PORT_NO 값으로 설정됩니다.|192.168.0.84:5401|
|--node-type|노드 타입을 지정합니다.<br>coordinator, deployer, lookup, broker, warehouse 다섯 가지가 있습니다.|warehouse|
|--deployer|설치할 서버의 deployer 노드 정보를 등록합니다.|192.168.0.84:5201|
|--port-no|'machbased'의 작업 포트를 지정합니다.<br>Broker에서 5656으로 설정했으므로 같은 서버에 설치하는 경우 다른 포트를 지정해야 합니다. warehouse 포트 번호는 5400으로 설정합니다.<br>이 포트는 클라이언트 및 machsql 연결 시 사용됩니다.|5400|
|--home-path|설치할 경로를 지정합니다. 그룹을 구분하기 위해 warehouse_g1, g2, g3 순으로 설정합니다.|/home/machbase/warehouse_g1|
|--package-name|패키지 추가 시 지정한 패키지 이름을 설정합니다.|machbase|
|--replication|복제를 담당할 노드를 "IP:PORT"로 지정합니다.<br>포트 값은 warehouse 포트 번호 5402로 설정합니다.|192.168.0.84:5402|
|--no-replicate|그룹에 warehouse 데이터가 있는 경우 노드 추가 시 데이터를 복제할지 여부를 지정합니다.| |
|--set-group-state|그룹의 상태를 normal과 readonly로 지정합니다.<br>Normal은 읽기, 쓰기 / readonly는 읽기만 가능합니다.| |

### Group 1에 노드 추가

Warehouse Group1에 다른 노드를 추가합니다.

```bash
# group1에 warehouse 노드 추가
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-node="192.168.0.84:5401"  \
        --node-type=warehouse --deployer="192.168.0.84:5201" --port-no="5400"       \
        --home-path="/home/machbase/warehouse_g1" --package-name=machbase           \
        --replication="192.168.0.84:5402" --group="group1" --no-replicate

# 설치된 노드 실행
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --startup-node="192.168.0.84:5401"
```

|옵션|설명|예시|
|--|--|--|
|--add-node|추가할 노드 이름을 "IP:PORT"로 지정합니다.<br>PORT 값은 CLUSTER_LINK_PORT_NO 값으로 설정됩니다.|192.168.0.84:5401|
|--node-type|노드 타입을 지정합니다.<br>coordinator, deployer, lookup, broker, warehouse 다섯 가지가 있습니다.|warehouse|
|--deployer|설치할 서버의 deployer 노드 정보를 등록합니다.|192.168.0.84:5201|
|--port-no|'machbased'의 작업 포트를 지정합니다.<br>Broker에서 5656으로 설정했으므로 같은 서버에 설치하는 경우 다른 포트를 지정해야 합니다. warehouse 포트 번호는 5400으로 설정합니다.<br>이 포트는 클라이언트 및 machsql 연결 시 사용됩니다.|5400|
|--home-path|설치할 경로를 지정합니다. 그룹을 구분하기 위해 warehouse_g1, g2, g3 순으로 설정합니다.|/home/machabse/warehouse_g1|
|--package-name|패키지 추가 시 지정한 패키지 이름을 설정합니다.|machbase|
|--replication|복제를 담당할 노드를 "IP:PORT"로 지정합니다.<br>포트 값은 warehouse 포트 번호 5402로 설정합니다.|192.168.0.84:5402|
|--group|그룹 이름을 지정합니다.|group1|
|--no-replicate|그룹에 warehouse 데이터가 있는 경우 노드 추가 시 데이터를 복제할지 여부를 지정합니다.| |
|--set-group-state|그룹의 상태를 normal과 readonly로 지정합니다.<br>Normal은 읽기, 쓰기 / readonly는 읽기만 가능합니다.| |

## Group 2 설치

두 번째 Warehouse Group2 노드를 설치합니다.

```bash
# group2 warehouse 설치
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-node="192.168.0.84:5411"  \
        --node-type=warehouse --deployer="192.168.0.84:5201" --port-no="5410"       \
        --home-path="/home/machbase/warehouse_g2" --package-name=machbase           \
        --replication="192.168.0.84:5412"  --group="group2" --no-replicate

# 설치된 노드 실행
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --startup-node="192.168.0.84:5411"
```

|옵션|설명|예시|
|--|--|--|
|--add-node|추가할 노드 이름을 "IP:PORT"로 지정합니다.<br>PORT 값은 CLUSTER_LINK_PORT_NO 값으로 설정됩니다.|192.168.0.84:5411|
|--node-type|노드 타입을 지정합니다.<br>coordinator, deployer, lookup, broker, warehouse 다섯 가지가 있습니다.|warehouse|
|--deployer|설치할 서버의 deployer 노드 정보를 등록합니다.|192.168.0.84:5201|
|--port-no|'machbased'의 작업 포트를 지정합니다.<br>Broker에서 5656으로 설정했으므로 같은 서버에 설치하는 경우 다른 포트를 지정해야 합니다. warehouse 포트 번호는 5410으로 설정합니다.<br>이 포트는 클라이언트 및 machsql 연결 시 사용됩니다.|5410|
|--home-path|설치할 경로를 지정합니다. 그룹을 구분하기 위해 warehouse_g1, g2, g3 순으로 설정합니다.|/home/machbase/warehouse_g2|
|--package-name|패키지 추가 시 지정한 패키지 이름을 설정합니다.|machbase|
|--replication|복제를 담당할 노드를 "IP:PORT"로 지정합니다.<br>포트 값은 warehouse 포트 번호 5412로 설정합니다.|192.168.0.84:5412|
|--group|그룹 이름을 지정합니다.|group2|
|--no-replicate|그룹에 warehouse 데이터가 있는 경우 노드 추가 시 데이터를 복제할지 여부를 지정합니다.| |
|--set-group-state|그룹의 상태를 normal과 readonly로 지정합니다.<br>Normal은 읽기, 쓰기 / readonly는 읽기만 가능합니다.| |

### Group 2에 노드 추가

Warehouse Group2에 다른 노드를 추가합니다.

```bash
# group2에 warehouse 노드 추가
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-node="192.168.0.83:5411"  \
        --node-type=warehouse --deployer="192.168.0.83:5201" --port-no="5410"       \
        --home-path="/home/machbase/warehouse_g2" --package-name=machbase           \
        --replication="192.168.0.83:5412" --group="group2" --no-replicate

# 설치된 노드 실행
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --startup-node="192.168.0.83:5411"
```

|옵션|설명|예시|
|--|--|--|
|--add-node|추가할 노드 이름을 "IP:PORT"로 지정합니다.<br>PORT 값은 CLUSTER_LINK_PORT_NO 값으로 설정됩니다.|192.168.0.83:5411|
|--node-type|노드 타입을 지정합니다.<br>coordinator, deployer, lookup, broker, warehouse 다섯 가지가 있습니다.|warehouse|
|--deployer|설치할 서버의 deployer 노드 정보를 등록합니다.|192.168.0.83:5201|
|--port-no|'machbased'의 작업 포트를 지정합니다.<br>Broker에서 5656으로 설정했으므로 같은 서버에 설치하는 경우 다른 포트를 지정해야 합니다. warehouse 포트 번호는 5410으로 설정합니다.<br>이 포트는 클라이언트 및 machsql 연결 시 사용됩니다.|5410|
|--home-path|설치할 경로를 지정합니다. 그룹을 구분하기 위해 warehouse_g1, g2, g3 순으로 설정합니다.|/home/machbase/warehouse_g2|
|--package-name|패키지 추가 시 지정한 패키지 이름을 설정합니다.|machbase|
|--replication|복제를 담당할 노드를 "IP:PORT"로 지정합니다.<br>포트 값은 warehouse 포트 번호 5412로 설정합니다.|192.168.0.83:5412|
|--group|그룹 이름을 지정합니다.|group2|
|--no-replicate|그룹에 warehouse 데이터가 있는 경우 노드 추가 시 데이터를 복제할지 여부를 지정합니다.| |
|--set-group-state|그룹의 상태를 normal과 readonly로 지정합니다.<br>Normal은 읽기, 쓰기 / readonly는 읽기만 가능합니다.| |


## Warehouse 삭제

Coordinator 노드에서 warehouse 노드를 삭제합니다.

```bash
# warehouse 노드 삭제
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --remove-node="192.168.0.83:5401"
```


## Warehouse 종료/중지

Coordinator 노드에서 warehouse 노드를 종료/중지하는 방법이 있습니다.

```bash
# warehouse 노드 종료
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --shutdown-node="192.168.0.83:5401"

# warehouse 노드 중지
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --kill-node="192.168.0.83:5401"
```

또는 warehouse가 설치된 서버에서 직접 프로세스를 종료/중지할 수 있습니다.

```bash
# warehouse 노드 종료
$MACHBASE_HOME/bin/machadmin -s

# warehouse 노드 중지
$MACHBASE_HOME/bin/machadmin -k
```
