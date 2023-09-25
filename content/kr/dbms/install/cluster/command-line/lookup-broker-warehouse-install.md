---
title : "Lookup / Broker / Warehouse 설치"
type: docs
weight: 30
---

## Lookup 설치

Coordinator 노드에서 lookup 노드를 추가한다.  여러 개의 lookup 노드 등록이 가능하다.

해당 서버에 deployer 노드가 미리 설치되어 있어야 한다.

Deployer 노드가 설치되면, 모든 작업은 coordinator 노드에서 수행하게 되며 해당 서버에 접속해서 설정하는 것은 없다.

```bash
## lookup master 노드를 추가한다.                                
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-node="192.168.0.84:5301"  \
        --node-type=lookup --lookup-type=master --deployer="192.168.0.84:5201"      \
        --home-path="/home/machbase/lookup1"
 
 
## lookup monitor 노드를 추가한다.                                
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-node="192.168.0.84:5302"  \
        --node-type=lookup --lookup-type=monitor --deployer="192.168.0.84:5201"         \
        --home-path="/home/machbase/lookupm1"
 
 
## lookup slave 노드를 추가한다.                                
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-node="192.168.0.84:5303"  \
        --node-type=lookup --lookup-type=slave --deployer="192.168.0.84:5201"       \
        --home-path="/home/machbase/lookup3"
 
  
## lookup 노드를 실행한다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --startup-node="192.168.0.84:5301"
 
## lookup 노드를 일괄적으로 실행할 수 있다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --startup-lookup
```

|옵션 항목|설명|예시|
|--|--|--|
|--add-node|추가할 노드명으로, “IP:PORT” 형식으로 지정한다.|192.168.0.84:5301|
|--node-type|노드 종류를 지정한다.<br> coordinator, deployer, broker, lookup, warehouse 5종류가 있다.|lookup|
|--deployer|설치할 서버의 deployer node 정보를 등록한다. |192.168.0.84:5201|
|--lookup-type|lookup 노드 종류를 지정한다.<br>  master,slave,monitor 3종류가 있다.|master|
|--home-path|설치할 경로를 지정한다.<br> machbase 계정에서 /home/machabse/lookup1 로 지정한다 |/home/machabse/lookup|

### 설치 조건

Lookup 노드는 Master, Slave, Monitor 3 종류가 존재하는데 아래 조건에 맞게 설치해야 한다.

    1. Lookup Master 노드
        a. 반드시 1개가 존재해야 하는 Lookup 노드이다.
        b. Monitor, Slave 노드보다 먼저 설치되어야 한다.
    2. Lookup Monitor 노드 
        a. 반드시 존재해야 하는 Lookup 노드이다.
        b. 안정적인 HA를 위해 각 서버에 1개씩 존재해야 한다.
    3. Lookup Slave 노드
        a. HA를 위해 1개 이상 존재하는 것을 권장한다.(없을경우 HA를 보장할 수 없다)


## Lookup 삭제

Coordinator 노드에서 lookup 노드를 삭제한다.


```bash
## Delete 노드를 삭제한다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --remove-node="192.168.0.84:5301"
```


## Lookup 종료/중단

Coordinator 노드에서 lookup 노드를 종료/중단하는 방법이 있다.


```bash
## lookup 노드를 종료한다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --shutdown-node="192.168.0.84:5301"
 
## lookup 노드를 일괄적으로 종료할 수 있다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --shutdown-lookup
```


## Lookup Master 변경

Coordinator 노드에서 lookup master 노드를 변경하는 방법이 있다.

lookup slave에 한해서 lookup master로 변경 가능하며, 기존에 lookup master는 lookup slave가 된다.

```bash
## lookup master를 변경한다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --set-lookup-master="192.168.0.84:5301"```
```


## Broker 설치

Coordinator 노드에서 broker 노드를 추가한다.  여러 개의 broker 노드 등록이 가능하다.

해당 서버에 deployer 노드가 미리 설치되어 있어야 한다.

Deployer 노드가 설치되면, 모든 작업은 coordinator 노드에서 수행하게 되며 해당 서버에 접속해서 설정하는 것은 없다.

최초에 등록되는 노드가 leader broker가 되고 이후에 추가적으로 등록되는 노드는 follower broker가 된다.

```bash
## broker 노드를 추가한다.                                
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-node="192.168.0.84:5301"  \
        --node-type=broker --deployer="192.168.0.84:5201" --port-no="5656"          \
        --home-path="/home/machbase/broker" --package-name=machbase
  
## broker 노드를 실행한다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --startup-node="192.168.0.84:5301"
```

|옵션 항목|설명|예시|
|--|--|--|
|--add-node|추가할 노드명으로, “IP:PORT” 형식으로 지정한다.<br>  PORT 값은 CLUSTER_LINK_PORT_NO 값으로 설정된다.|192.168.0.84:5301|
|--node-type|노드 종류를 지정한다.<br>  coordinator, deployer, broker, lookup,warehouse 5종류가 있다.|broker|
|--deployer|설치할 서버의 deployer node 정보를 등록한다.  |192.168.0.84:5201|
|--port-no|machbased 구동 포트를 지정한다.<br>  Broker는 디폴트값인 5656을 지정한다.<br> client와 machsql이 접속할 때 이 포트를 이용한다.|5656|
|--home-path|설치할 경로를 지정한다.<br>  machbase 계정에서 /home/machabse/broker 로 지정한다|/home/machbase/broker|
|--package-name|패키지 추가할 때 지정한 package 명을 설정한다.  |machbase|


## Broker 삭제

Coordinator 노드에서 broker 노드를 삭제한다.

```bash
## broker 노드를 삭제한다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --remove-node="192.168.0.84:5301"
```


## Broker 종료/중단

Coordinator 노드에서 broker 노드를 종료/중단하는 방법이 있다.

```bash
## broker 노드를 종료한다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --shutdown-node="192.168.0.84:5301"
  
## broker 노드를 중단한다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --kill-node="192.168.0.84:5301"
```

또는, broker가 설치된 서버에서 직접 그 프로세스를 종료/중단하는 방법도 있다.


```bash
## broker 노드를 종료한다.
$MACHBASE_HOME/bin/machadmin -s
  
## broker 노드를 종료한다.
$MACHBASE_HOME/bin/machadmin -k
```


## Warehouse 설치 

Coordinator 노드에서 active 노드와 standby 노드를 설치한다.

사전에 설치된 deployer 를 통해서 설치된다.

### Group1 설치 

첫번째 Warehouse 그룹인 Group1 노드를 설치한다.

```bash
## group1 warehouse를 설치한다.                         
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-node="192.168.0.83:5401"  \
        --node-type=warehouse --deployer="192.168.0.83:5201" --port-no="5400"       \
        --home-path="/home/machbase/warehouse_g1" --package-name=machbase           \
        --replication="192.168.0.83:5402"  --group="group1" --no-replicate
  
## 설치된 노드를 구동한다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --startup-node="192.168.0.84:5401"
```

|옵션 항목|설명|예시|
|--|--|--|
|--add-node|추가할 노드명으로 “IP:PORT” 형식으로 지정한다.<br>  PORT값은 CLUSTER_LINK_PORT_NO 값으로 설정된다.|192.168.0.84:5401|
|--node-type|노드 종류를 지정한다.<br>  coordinator, deployer, broker, warehouse, lookup 5종류가 있다.|warehouse|
|--deployer|설치할 서버의 deployer node 정보를 등록한다.  |192.168.0.84:5201|
|--port-no|machbased 구동 포트를 지정한다.<br>  Broker에서 5656값을 설정하였으므로 동일 서버에 설치되는 경우 다른 포트를 지정해야 한다. 따라서 warehouse 사용 포트 대역인 5400 을 지정한다.<br> client와 machsql 접속할 때 이 포트를 이용한다.|5400|
|--home-path|설치할 경로를 지정한다. 그룹을 구분하기 위해서 warehouse_g1, g2, g3 순으로 설정한다. |/home/machbase/warehouse_g1|
|--package-name|패키지 추가할 때 지정한 package 명을 설정한다.  |machbase|
|--replication|	Replication을 담당할 노드를 “IP:PORT” 형식으로 지정한다.<br> PORT값은 해당 warehouse 사용 포트대역인 5402로 지정한다.|192.168.0.84:5402|
|--group| Group명을 지정한다.| group1|
|--no-replicate| Group내의 warehouse데이터가 있는 경우, 노드추가 시, 데이터를 복제할 것 인지 지정한다.| |

### Group1에 노드 추가 설치

Warehouse Group1에 노드를 한 개 더 추가 설치한다.


```bash
## group1에 warehouse node를 추가 설치한다.              
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-node="192.168.0.84:5401"  \
        --node-type=warehouse --deployer="192.168.0.84:5201" --port-no="5400"       \
        --home-path="/home/machbase/warehouse_g1" --package-name=machbase           \
        --replication="192.168.0.84:5402" --group="group1" --no-replicate
  
## 설치된 노드를 구동한다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --startup-node="192.168.0.84:5401"
```

|옵션 항목|설명|예시|
|--|--|--|
|--add-node|추가할 노드명으로 “IP:PORT” 형식으로 지정한다.<br>  PORT값은 CLUSTER_LINK_PORT_NO 값으로 설정된다.|192.168.0.84:5401|
|--node-type|노드 종류를 지정한다.<br>  coordinator, deployer, broker, warehouse, lookup 5종류가 있다.|warehouse|
|--deployer|설치할 서버의 deployer node 정보를 등록한다.  |192.168.0.84:5201|
|--port-no|machbased 구동 포트를 지정한다.<br>  Broker에서 5656값을 설정하였으므로 동일 서버에 설치되는 경우 다른 포트를 지정해야 한다. 따라서 warehouse 사용 포트 대역인 5400 을 지정한다.<br> client와 machsql 접속할 때 이 포트를 이용한다.|5400|
|--home-path|설치할 경로를 지정한다. 그룹을 구분하기 위해서 warehouse_g1, g2, g3 순으로 설정한다. |/home/machbase/warehouse_g1|
|--package-name|패키지 추가할 때 지정한 package 명을 설정한다.  |machbase|
|--replication|	Replication을 담당할 노드를 “IP:PORT” 형식으로 지정한다.<br> PORT값은 해당 warehouse 사용 포트대역인 5402로 지정한다.|192.168.0.84:5402|
|--group| Group명을 지정한다.| group1|
|--no-replicate| Group내의 warehouse데이터가 있는 경우, 노드추가 시, 데이터를 복제할 것 인지 지정한다.| |

## Group2 설치

두 번째 Warehouse 그룹인 Group2 노드를 설치한다.

```bash
## group1 warehouse를 설치한다.                         
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-node="192.168.0.84:5411"  \
        --node-type=warehouse --deployer="192.168.0.84:5201" --port-no="5410"       \
        --home-path="/home/machbase/warehouse_g2" --package-name=machbase           \
        --replication="192.168.0.84:5412"  --group="group2" --no-replicate
  
## 설치된 노드를 구동한다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --startup-node="192.168.0.84:5411"
```

|옵션 항목|설명|예시|
|--|--|--|
|--add-node|추가할 노드명으로 “IP:PORT” 형식으로 지정한다.<br>  PORT값은 CLUSTER_LINK_PORT_NO 값으로 설정된다.|192.168.0.84:5411|
|--node-type|노드 종류를 지정한다.<br>  coordinator, deployer, broker, warehouse, lookup 5종류가 있다.|warehouse|
|--deployer|설치할 서버의 deployer node 정보를 등록한다.  |192.168.0.84:5201|
|--port-no|machbased 구동 포트를 지정한다.<br>  Broker에서 5656값을 설정하였으므로 동일 서버에 설치되는 경우 다른 포트를 지정해야 한다. 따라서 warehouse 사용 포트 대역인 5410 을 지정한다.<br> client와 machsql 접속할 때 이 포트를 이용한다.|5410|
|--home-path|설치할 경로를 지정한다. 그룹을 구분하기 위해서 warehouse_g1, g2, g3 순으로 설정한다. |/home/machbase/warehouse_g2|
|--package-name|패키지 추가할 때 지정한 package 명을 설정한다.  |machbase|
|--replication|	Replication을 담당할 노드를 “IP:PORT” 형식으로 지정한다.<br> PORT값은 해당 warehouse 사용 포트대역인 5412로 지정한다.|192.168.0.84:5412|
|--group| Group명을 지정한다.| group2|
|--no-replicate| Group내의 warehouse데이터가 있는 경우, 노드추가 시, 데이터를 복제할 것 인지 지정한다.| |

### Group2에 노드 추가 설치

Warehouse Group2에 노드를 한 개 더 추가 설치한다.


```bash
## group1에 warehouse node를 추가 설치한다.              
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-node="192.168.0.83:5411"  \
        --node-type=warehouse --deployer="192.168.0.83:5201" --port-no="5410"       \
        --home-path="/home/machbase/warehouse_g2" --package-name=machbase           \
        --replication="192.168.0.83:5412" --group="group2" --no-replicate
  
## 설치된 노드를 구동한다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --startup-node="192.168.0.83:5411"
```

|옵션 항목|설명|예시|
|--|--|--|
|--add-node|추가할 노드명으로 “IP:PORT” 형식으로 지정한다.<br>  PORT값은 CLUSTER_LINK_PORT_NO 값으로 설정된다.|192.168.0.84:5411|
|--node-type|노드 종류를 지정한다.<br>  coordinator, deployer, broker, warehouse, lookup 5종류가 있다.|warehouse|
|--deployer|설치할 서버의 deployer node 정보를 등록한다.  |192.168.0.84:5201|
|--port-no|machbased 구동 포트를 지정한다.<br>  Broker에서 5656값을 설정하였으므로 동일 서버에 설치되는 경우 다른 포트를 지정해야 한다. 따라서 warehouse 사용 포트 대역인 5410 을 지정한다.<br> client와 machsql 접속할 때 이 포트를 이용한다.|5410|
|--home-path|설치할 경로를 지정한다. 그룹을 구분하기 위해서 warehouse_g1, g2, g3 순으로 설정한다. |/home/machbase/warehouse_g2|
|--package-name|패키지 추가할 때 지정한 package 명을 설정한다.  |machbase|
|--replication|	Replication을 담당할 노드를 “IP:PORT” 형식으로 지정한다.<br> PORT값은 해당 warehouse 사용 포트대역인 5412로 지정한다.|192.168.0.84:5412|
|--group| Group명을 지정한다.| group2|
|--no-replicate| Group내의 warehouse데이터가 있는 경우, 노드추가 시, 데이터를 복제할 것 인지 지정한다.| |


## Warehouse 삭제

Coordinator 노드에서 warehouse 노드를 삭제한다.

```bash
## warehouse 노드를 삭제한다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --remove-node="192.168.0.83:5401"
```


## Warehouse 종료/중단

Coordinator 노드에서 warehouse 노드를 종료/중단하는 방법이 있다.

```bash
## warehouse 노드를 종료한다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --shutdown-node="192.168.0.83:5401"
  
## warehouse 노드를 중단한다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --kill-node="192.168.0.83:5401"
```

또는 warehouse가 설치된 서버에서 직접 그 프로세스를 종료/중단하는 방법이 있다.

```bash
## warehouse 노드를 종료한다.
$MACHBASE_HOME/bin/machadmin -s
  
## warehouse 노드를 종료한다.
$MACHBASE_HOME/bin/machadmin -k
```
