---
title : 'Cluster Edition 업그레이드 및 복구'
type : docs
weight: 60
---

## Coordinator 업그레이드

Coordinator / Deployer 는 부득이하게 수동으로 업그레이드 해야 한다.

#### 주의사항

* DDL 또는 DELETE 수행 중이 아니어야 한다. (INSERT, APPEND, SELECT 는 상관없다.)
* 업그레이드 중 Node 추가/구동/종료/삭제 등의 명령을 내릴 수 없다.

#### Coordinator Shutdown

Coordinator / Deployer 는 종료되어도 Broker / Warehouse 의 INSERT, APPEND, SELECT 에 영향을 주지 않는다.
다만, 종료된 동안에는 Broker / Warehouse 가 도중에 죽는 것을 감지하지 못한다. (재시작 후에는 정상 감지된다.)

```bash
machcoordinatoradmin --shutdown
```

#### Coordinator 백업 (Optional)

$MACH_COORDINATOR_HOME 에 있는 dbs/, conf/ 디렉토리를 백업한다.

#### Coordinator 업그레이드

**lightweight package 가 아닌 full package 로 진행한다.**

Package 를 $MACH_COORDINATOR_HOME 에 압축을 풀어 덮어쓴다.

```bash
tar -zxvf machbase-ent-new.official-LINUX-X86-64-release.tgz -C $MACHBASE_COORDINATOR_HOME
```

#### Coordinator 시작

```bash
machcoordinatoradmin --startup
```


## Deployer 업그레이드

Coordinator 와 동일하다.

#### 주의사항
 
업그레이드 중 Node 추가/구동/종료/삭제 등의 명령을 내릴 수 없다.

#### Deployer 종료

```bash
machdeployeradmin --shutdown
```

#### Deployer 백업 (Optional)

$MACH_DEPLOYER_HOME 에 있는 dbs/, conf/ 디렉토리를 백업한다.

#### Deployer 업그레이드

Deployer 가 설치된 Host 에서 MWA 를 수행하거나 Collector 를 수행하지 않는다면, lightweight package 로 진행해도 무방하다.

Package 를 $MACH_DEPLOYER_HOME 에 압축을 풀어 덮어쓴다.

```bash
tar -zxvf machbase-ent-new.official-LINUX-X86-64-release.tgz -C $MACH_DEPLOYER_HOME
```

#### Deployer 시작

```bash
machdeployeradmin --startup
```


## Package 등록

Broker/Warehouse 업그레이드를 위한 작업으로, Package 를 Coordinator 에 등록해서 업그레이드를 진행한다.

{{<callout type="info">}}
lightweight package 로 등록하는 것이 좋다.
{{</callout>}}

먼저, Package 를 $MACH_COORDINATOR_HOME 이 위치한 host 에 옮긴다.

그 다음, 아래 명령으로 패키지를 추가한다. 

```bash
machcoordinatoradmin --add-package=new_package --file-name=./machbase-ent-new.official-LINUX-X86-64-release-lightweight.tgz
```

|옵션|설명|
|--|--|
|--add-package|추가할 패키지의 이름을 지정한다.|
|--file-name|추가할 패키지 파일의 경로를 지정한다.<br>**이미 같은 파일 이름의 package 가 추가되어 있다면 에러가 발생하므로, 파일 이름을 확인해야 한다.**|


#### Broker/Warehouse 업그레이드

Coordinator 에서 다음 명령을 수행한다.

## Node 종료 

```bash
machcoordinatoradmin --shutdown-node=localhost:5656
```

## Node 업그레이드 

```bash
machcoordinatoradmin --upgrade-node=localhost:5656 --package-name=new_package
```

|옵션|설명|
|--|--|
|--upgrade-node|업그레이드 대상 Node 이름을 입력한다.|
|--package-name|업그레이드할 Package 이름을 입력한다.|

Node 종료 없이 Node 업그레이드를 수행하면, 자동으로 Node 를 종료시키고 Node 업그레이드를 수행한다.
하지만, 안정성을 위해서 Node 종료를 명시적으로 수행하도록 한다.

## Node 구동

```bash
machcoordinatoradmin --startup-node=localhost:5656
```


## Snapshot Failover

Machbase 6.5 Cluster Edition에 Snapshot Failover 기능이 추가되었다.

Snapshot Failover는 DBMS가 정상적인 상황일 때 Snapshot 을 기록해두고 특정 Warehouse의 장애 발생 시 정상인 Snapshot은 제외하고 문제가 발생한 부분에 대해서만 Failover를 수행함으로써 빠른 복구를 제공하는 기능이다.

#### Snapshot 기본 개념

Cluster Edition의 각 Group별로 Group 내 존재하는 Warehouse들 사이의 정상 데이터의 위치를 기록하는 개념이다.

Group 내의 Warehouse 에 생성된 Snapshot 이전의 데이터는 모두 정상 상태의 Data임을 보장하며 각 Group 별로 각각의 Snapshot을 기록한다.

#### Snapshot Failover 동작 방식

특정 Warehouse에 문제가 발생했을 경우 이 Warehouse는 Scrapped 상태로 데이터 복구가 필요한 상황이 된다.

Snapshot Recovery를 수행하게 되면 문제가 발생한 Warehouse에서의 정상 Snapshot을 기준으로 Snapshot 이후의 Data는 Clear하고 같은 Group 내 정상 상태의 Warehouse의 기준 Snapshot 이후 Data를 문제가 발생한 Warehouse로 Replication해서 복구를 완료한다.

#### Snapshot 자동 수행

Default로 Snapshot 자동 수행이 Enable 되어 있으며 Snapshot을 수행하는 주기는 60초로 설정 되어 있으며 Clustser에 Warehouse Group이 여러 개일 경우 Snapshot 주기마다 하나의 Group만 순서대로 Snapshot을 수행한다.

수행 주기를 0으로 설정하면 Snapshot 자동 수행이 Disable된다.

Snapshot 주기 설정은 명령어를 실행하면 즉시 반영된다.

```bash
## Snapshot 주기 설정
machcoordinatoradmin --snapshot-interval=[sec]
  
## 현재 Snapshot 주기 확인
machcoordinatoradmin --configuration
```

#### Snapshot 수동 수행

machcoordinatoradmin tool을 이용해 group_name을 지정하고 수동으로 Snapshot을  수행한다.

group_name은 group1, group2와 같이 미리 설정되어 있다.

Cluster에 Group이 여러 개일 경우 전체 Snapshot을 찍기 위해서는 모든 각각의 Group에 Snapshot을 수행해줘야 한다.

```bash
## group_name에 대한 Snapshot 수동 수행
machcoordinatoradmin --exec-snapshot --group='group_name'
```

#### Scrapped node 를 Snapshot 기반으로 복구

Scrapped node 가 발생한 경우 아래와 같이 복구한다.

```bash
## 해당 group 을 readonly 로 변경
## 이후의 단계에서 group이 normal로 변경되는 것을 방지
machcoordinatoradmin --set-group-state=readonly --group=[groupname]
  
## snapshot 기반으로 복구
machcoordinatoradmin --snapshot-recover=[nodename]
  
## replication을 통해 snapshot 이후의 최신 data를 복제
## replication이 끝나면 warehouse 의 상태는 normal로 자동 변경
machcoordinatoradmin --exec-sync=[nodename]
  
## group 상태를 normal 로 변경
machcoordinatoradmin --set-group-state=normal --group=[groupname]
```

#### Scrapped node의 Snapshot 기반 복구 과정

Snapshot으로 Scrapped node를 복구시 아래와 같은 과정이 수행된다.

```bash
/*최초 cluster 상태*/
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
|  Node Type  |    Node Name    |   Group Name    |   Group State   |    Desired & Actual State     |  RP State   |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
| coordinator | localhost:30110 | Coordinator     | normal          | primary       | primary       | ----------- |
| coordinator | localhost:30120 | Coordinator     | normal          | normal        | normal        | ----------- |
| deployer    | localhost:30210 | Deployer        | normal          | normal        | normal        | ----------- |
| broker      | localhost:30310 | Broker          | normal          | leader        | leader        | ----------- |
| broker      | localhost:30320 | Broker          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30410 | group1          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30420 | group1          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30510 | group2          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30520 | group2          | normal          | normal        | normal        | ----------- |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
  
/*group1의 warehouse 0이 죽었을 때*/
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
|  Node Type  |    Node Name    |   Group Name    |   Group State   |    Desired & Actual State     |  RP State   |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
| coordinator | localhost:30110 | Coordinator     | normal          | primary       | primary       | ----------- |
| coordinator | localhost:30120 | Coordinator     | normal          | normal        | normal        | ----------- |
| deployer    | localhost:30210 | Deployer        | normal          | normal        | normal        | ----------- |
| broker      | localhost:30310 | Broker          | normal          | leader        | leader        | ----------- |
| broker      | localhost:30320 | Broker          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30410 | group1          | readonly        | scrapped      | **unknown**   | ----------- |
| warehouse   | localhost:30420 | group1          | readonly        | normal        | normal        | ----------- |
| warehouse   | localhost:30510 | group2          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30520 | group2          | normal          | normal        | normal        | ----------- |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
  
## 해당 group 을 readonly 로 변경
machcoordinatoradmin --set-group-state=readonly --group=[groupname]
  
kellen@kellen-ku:~$ machcoordinatoradmin --set-group-state=readonly --group=group1
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - 321a012d05.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Group Name: group1
Flag      : 1
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
|  Node Type  |    Node Name    |   Group Name    |   Group State   |    Desired & Actual State     |  RP State   |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
| coordinator | localhost:30110 | Coordinator     | normal          | primary       | primary       | ----------- |
| coordinator | localhost:30120 | Coordinator     | normal          | normal        | normal        | ----------- |
| deployer    | localhost:30210 | Deployer        | normal          | normal        | normal        | ----------- |
| broker      | localhost:30310 | Broker          | normal          | leader        | leader        | ----------- |
| broker      | localhost:30320 | Broker          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30410 | group1          | readonly         | scrapped      | **unknown**   | ----------- |
| warehouse   | localhost:30420 | group1          | readonly         | normal        | normal        | ----------- |
| warehouse   | localhost:30510 | group2          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30520 | group2          | normal          | normal        | normal        | ----------- |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
  
#죽은 Warehouse를 다시 startup 수행한다
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
|  Node Type  |    Node Name    |   Group Name    |   Group State   |    Desired & Actual State     |  RP State   |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
| coordinator | localhost:30110 | Coordinator     | normal          | primary       | primary       | ----------- |
| coordinator | localhost:30120 | Coordinator     | normal          | normal        | normal        | ----------- |
| deployer    | localhost:30210 | Deployer        | normal          | normal        | normal        | ----------- |
| broker      | localhost:30310 | Broker          | normal          | leader        | leader        | ----------- |
| broker      | localhost:30320 | Broker          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30410 | group1          | readonly         | scrapped      | scrapped      | ----------- |
| warehouse   | localhost:30420 | group1          | readonly         | normal        | normal        | ----------- |
| warehouse   | localhost:30510 | group2          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30520 | group2          | normal          | normal        | normal        | ----------- |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
  
## snapshot 기반으로 복구
machcoordinatoradmin --snapshot-recover=[nodename]
  
kellen@kellen-ku:~$ machcoordinatoradmin --snapshot-recover=localhost:30410
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - 321a012d05.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Node-Name: localhost:30410
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
|  Node Type  |    Node Name    |   Group Name    |   Group State   |    Desired & Actual State     |  RP State   |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
| coordinator | localhost:30110 | Coordinator     | normal          | primary       | primary       | ----------- |
| coordinator | localhost:30120 | Coordinator     | normal          | normal        | normal        | ----------- |
| deployer    | localhost:30210 | Deployer        | normal          | normal        | normal        | ----------- |
| broker      | localhost:30310 | Broker          | normal          | leader        | leader        | ----------- |
| broker      | localhost:30320 | Broker          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30410 | group1          | readonly         | scrapped      | scrapped      | ----------- |
| warehouse   | localhost:30420 | group1          | readonly         | normal        | normal        | ----------- |
| warehouse   | localhost:30510 | group2          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30520 | group2          | normal          | normal        | normal        | ----------- |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
  
## replication을 통해 snapshot 이후의 최신 data를 복제
machcoordinatoradmin --exec-sync=[nodename]
  
kellen@kellen-ku:~$ machcoordinatoradmin --exec-sync=localhost:30410
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - 321a012d05.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Node-Name: localhost:30410
Source:
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
|  Node Type  |    Node Name    |   Group Name    |   Group State   |    Desired & Actual State     |  RP State   |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
| coordinator | localhost:30110 | Coordinator     | normal          | primary       | primary       | ----------- |
| coordinator | localhost:30120 | Coordinator     | normal          | normal        | normal        | ----------- |
| deployer    | localhost:30210 | Deployer        | normal          | normal        | normal        | ----------- |
| broker      | localhost:30310 | Broker          | normal          | leader        | leader        | ----------- |
| broker      | localhost:30320 | Broker          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30410 | group1          | readonly         | scrapped      | scrapped      | stopped     |
| warehouse   | localhost:30420 | group1          | readonly         | normal        | normal        | stopped     |
| warehouse   | localhost:30510 | group2          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30520 | group2          | normal          | normal        | normal        | ----------- |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
|  Node Type  |    Node Name    |   Group Name    |   Group State   |    Desired & Actual State     |  RP State   |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
| coordinator | localhost:30110 | Coordinator     | normal          | primary       | primary       | ----------- |
| coordinator | localhost:30120 | Coordinator     | normal          | normal        | normal        | ----------- |
| deployer    | localhost:30210 | Deployer        | normal          | normal        | normal        | ----------- |
| broker      | localhost:30310 | Broker          | normal          | leader        | leader        | ----------- |
| broker      | localhost:30320 | Broker          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30410 | group1          | readonly         | sync-standby  | sync-standby  | running     |
| warehouse   | localhost:30420 | group1          | readonly         | sync-active   | sync-active   | running     |
| warehouse   | localhost:30510 | group2          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30520 | group2          | normal          | normal        | normal        | ----------- |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
|  Node Type  |    Node Name    |   Group Name    |   Group State   |    Desired & Actual State     |  RP State   |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
| coordinator | localhost:30110 | Coordinator     | normal          | primary       | primary       | ----------- |
| coordinator | localhost:30120 | Coordinator     | normal          | normal        | normal        | ----------- |
| deployer    | localhost:30210 | Deployer        | normal          | normal        | normal        | ----------- |
| broker      | localhost:30310 | Broker          | normal          | leader        | leader        | ----------- |
| broker      | localhost:30320 | Broker          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30410 | group1          | readonly         | normal        | normal        | stopped     |
| warehouse   | localhost:30420 | group1          | readonly         | normal        | normal        | stopped     |
| warehouse   | localhost:30510 | group2          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30520 | group2          | normal          | normal        | normal        | ----------- |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
  
## group 상태를 normal 로 변경
machcoordinatoradmin --set-group-state=normal --group=[groupname]
  
kellen@kellen-ku:~$ machcoordinatoradmin --set-group-state=normal --group=group1
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - 321a012d05.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Group Name: group1
Flag      : 0
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
|  Node Type  |    Node Name    |   Group Name    |   Group State   |    Desired & Actual State     |  RP State   |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
| coordinator | localhost:30110 | Coordinator     | normal          | primary       | primary       | ----------- |
| coordinator | localhost:30120 | Coordinator     | normal          | normal        | normal        | ----------- |
| deployer    | localhost:30210 | Deployer        | normal          | normal        | normal        | ----------- |
| broker      | localhost:30310 | Broker          | normal          | leader        | leader        | ----------- |
| broker      | localhost:30320 | Broker          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30410 | group1          | normal          | normal        | normal        | stopped     |
| warehouse   | localhost:30420 | group1          | normal          | normal        | normal        | stopped     |
| warehouse   | localhost:30510 | group2          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30520 | group2          | normal          | normal        | normal        | ----------- |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
```

#### Snapshot 관련 Property

|Property|설명|설정위치|
|--|--|--|
|GROUP_SNAPSHOT_TIMEOUT_SEC|Snapshot 실행 시의 timeout 시간을 결정<br>Default: 60 (초)<br>최소 값 : 0 (무한 대기)<br>최대 값 : uint32_max (초)|Coordinator, Broker, Warehouse 각각의 machbase.conf 파일 내 작성
|
