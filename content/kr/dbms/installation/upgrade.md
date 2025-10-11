---
type: docs
title : 'Cluster Edition 업그레이드'
type : docs
weight: 60
---

## Coordinator 업그레이드

Coordinator / Deployer는 수동으로 업그레이드해야 합니다.

#### 주의 사항

* 업그레이드 중에는 노드 추가 / 시작 / 종료 / 삭제와 같은 명령을 실행할 수 없습니다.
* DDL 또는 DELETE가 사용 중이어서는 안 됩니다. (INSERT, APPEND, SELECT는 상관없습니다.)

#### Coordinator 종료


Coordinator / Deployer는 종료되더라도 Broker / Warehouse의 INSERT, APPEND, SELECT에 영향을 주지 않습니다.

그러나 종료되는 동안 Broker / Warehouse도 종료되는 것을 감지하지 못합니다. (일반적으로 재시작 후 감지됩니다)

```bash
machcoordinatoradmin --shutdown
```

#### Coordinator 백업 (선택 사항)

$MACH_COORDINATOR_HOME에 있는 dbs/ 및 conf/ 디렉토리를 백업합니다.

#### Coordinator 업그레이드

* 경량 패키지 대신 전체 패키지로 진행합니다.

패키지를 $MACH_COORDINATOR_HOME에 압축 해제하여 덮어씁니다.

```bash
tar zxvf machbase-ent-new.official-LINUX-X86-64-release.tgz -C $MACHBASE_COORDINATOR_HOME
```

#### Coordinator 시작

```bash
machcoordinatoradmin --startup
```


## Deployer 업그레이드

Coordinator와 동일한 프로세스입니다.

#### 주의 사항

* 업그레이드 중에는 노드 추가 / 시작 / 종료 / 삭제와 같은 명령을 실행할 수 없습니다.

#### Deployer 종료

```bash
machdeployeradmin --shutdown
```

#### Deployer 백업 (선택 사항)

$MACH_DEPLOYER_HOME에 있는 dbs/ 및 conf/ 디렉토리를 백업합니다.

#### Deployer 업그레이드

* Deployer가 설치된 호스트에서 MWA를 실행하거나 Collector를 실행하지 않는 경우 경량 패키지로 진행할 수 있습니다.

패키지를 $MACH_DEPLOYER_HOME에 압축 해제하여 덮어씁니다.

```bash
tar zxvf machbase-ent-new.official-LINUX-X86-64-release.tgz -C $MACH_DEPLOYER_HOME
```

#### Deployer 시작

```bash
machdeployeradmin --startup
```


## 패키지 등록

Broker / Warehouse를 업그레이드하려면 Coordinator에 패키지를 등록하고 업그레이드를 진행합니다.

{{< callout type="info" >}}
경량 패키지를 등록하는 것이 좋습니다.
{{< /callout >}}

먼저 $MACH_COORDINATOR_HOME이 있는 호스트로 패키지를 이동합니다.

다음으로 다음 명령을 사용하여 패키지를 추가합니다.

```bash
machcoordinatoradmin --add-package=new_package --file-name=./machbase-ent-new.official-LINUX-X86-64-release-lightweight.tgz
```

|옵션|설명|
|--|--|
|--add-package|추가할 패키지 이름을 지정합니다.|
|--file-name|추가할 패키지 파일의 경로를 지정합니다.<br>**동일한 파일 이름을 가진 패키지가 추가되면 오류가 발생하므로 파일 이름을 확인하십시오.**|


#### Broker/Warehouse 업그레이드

Coordinator에서 다음 명령을 실행합니다.

## 노드 종료

```bash
machcoordinatoradmin --shutdown-node=localhost:5656
```

## 노드 업그레이드

```bash
machcoordinatoradmin --upgrade-node=localhost:5656 --package-name=new_package
```

|옵션|설명|
|--|--|
|--upgrade-node|업그레이드 대상 노드의 이름을 입력합니다.|
|--package-name|업그레이드할 패키지의 이름을 입력합니다.|

* 노드를 종료하지 않고 노드를 업그레이드하면 자동으로 노드를 종료하고 노드 업그레이드를 수행합니다.
  그러나 안정성을 위해 업그레이드하기 전에 명시적으로 노드를 종료해야 합니다.

## 노드 시작

```bash
machcoordinatoradmin --startup-node=localhost:5656
```


## Snapshot Failover

Machbase 6.5 Cluster Edition부터 Snapshot Failover 기능이 추가되었습니다.

Snapshot failover는 DBMS가 정상 상태일 때 스냅샷을 기록하고 특정 warehouse에 장애가 발생하면 정상 스냅샷을 제외한 문제가 발생한 부분에 대해서만 failover를 수행하여 빠른 복구를 제공하는 기능입니다.

#### Snapshot 기본 개념

Cluster Edition의 그룹별로 그룹 내 warehouse 간의 정상 데이터 위치를 기록하는 개념입니다.

그룹 내 warehouse에서 생성된 스냅샷 이전의 모든 데이터는 정상 상태의 데이터이며, 각 스냅샷은 그룹별로 기록됩니다.

#### Snapshot Failover 작동 방식

특정 warehouse에 문제가 발생하면 warehouse가 scrapped 상태로 전환되고 데이터 복구가 필요합니다.

Snapshot Recovery를 수행할 때 문제가 발생한 warehouse의 정상 스냅샷을 기준으로 스냅샷 이후의 데이터가 지워지고, 동일한 그룹 내 정상 상태의 warehouse의 기준 스냅샷 이후 데이터가 문제가 발생한 warehouse로 복제되어 복구가 완료됩니다.

#### 자동 스냅샷 실행

기본적으로 자동 스냅샷 실행이 활성화되어 있으며, 스냅샷 실행 간격은 60초로 설정됩니다. 클러스터에 여러 warehouse 그룹이 있는 경우 스냅샷 간격마다 한 그룹만 순차적으로 스냅샷을 수행합니다.

실행 간격이 0으로 설정되면 자동 스냅샷 실행이 비활성화됩니다.

스냅샷 간격 설정은 명령이 실행될 때 즉시 반영됩니다.

```bash
## 스냅샷 간격 설정
machcoordinatoradmin --snapshot-interval=[sec]

## 현재 스냅샷 간격 확인
machcoordinatoradmin --configuration
```

#### 수동으로 스냅샷 생성

machcoordinatoradmin 도구를 사용하여 **group_name**을 지정하고 수동으로 스냅샷을 수행합니다.

**group_name**은 group1, group2와 같이 사전 설정됩니다.

클러스터에 여러 그룹이 있는 경우 전체 스냅샷을 생성하려면 각 그룹에 대해 스냅샷을 수행해야 합니다.

```bash
## group_name에 대해 수동으로 스냅샷 생성
machcoordinatoradmin --exec-snapshot --group='group_name'
```

#### 스냅샷을 기반으로 scrapped 노드 복구

scrapped 노드가 발생하면 다음과 같이 복구됩니다.

```bash
## 그룹 상태를 readonly로 변경
## 이후 단계에서 그룹이 normal 상태로 변경되는 것을 방지
machcoordinatoradmin --set-group-state=readonly --group=[groupname]

## 스냅샷을 기반으로 복구
machcoordinatoradmin --snapshot-recover=[nodename]

## 복제를 통해 스냅샷 이후의 최신 데이터 복제
## 복제가 완료되면 warehouse의 상태가 자동으로 normal로 변경됩니다.
machcoordinatoradmin --exec-sync=[nodename]

## 그룹 상태를 normal로 변경
machcoordinatoradmin --set-group-state=normal --group=[groupname]
```

#### Snapshot-based recovery process of scrapped nodes

When recovering a scrapped node with a snapshot, the following process is performed.

```bash
/* Initial cluster state */
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
  
/* warehouse 0 of group1 dies */
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
  
## Change the group state to readonly
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
| warehouse   | localhost:30410 | group1          | readonly        | scrapped      | **unknown**   | ----------- |
| warehouse   | localhost:30420 | group1          | readonly        | normal        | normal        | ----------- |
| warehouse   | localhost:30510 | group2          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30520 | group2          | normal          | normal        | normal        | ----------- |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
  
## Restart the dead warehouse
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
|  Node Type  |    Node Name    |   Group Name    |   Group State   |    Desired & Actual State     |  RP State   |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
| coordinator | localhost:30110 | Coordinator     | normal          | primary       | primary       | ----------- |
| coordinator | localhost:30120 | Coordinator     | normal          | normal        | normal        | ----------- |
| deployer    | localhost:30210 | Deployer        | normal          | normal        | normal        | ----------- |
| broker      | localhost:30310 | Broker          | normal          | leader        | leader        | ----------- |
| broker      | localhost:30320 | Broker          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30410 | group1          | readonly        | scrapped      | scrapped      | ----------- |
| warehouse   | localhost:30420 | group1          | readonly        | normal        | normal        | ----------- |
| warehouse   | localhost:30510 | group2          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30520 | group2          | normal          | normal        | normal        | ----------- |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
  
## Recovery based on snapshot
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
| warehouse   | localhost:30410 | group1          | readonly        | scrapped      | scrapped      | ----------- |
| warehouse   | localhost:30420 | group1          | readonly        | normal        | normal        | ----------- |
| warehouse   | localhost:30510 | group2          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30520 | group2          | normal          | normal        | normal        | ----------- |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
  
## Replicate the latest data after snapshot through replication
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
| warehouse   | localhost:30410 | group1          | readonly        | scrapped      | scrapped      | stopped     |
| warehouse   | localhost:30420 | group1          | readonly        | normal        | normal        | stopped     |
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
| warehouse   | localhost:30410 | group1          | readonly        | sync-standby  | sync-standby  | running     |
| warehouse   | localhost:30420 | group1          | readonly        | sync-active   | sync-active   | running     |
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
| warehouse   | localhost:30410 | group1          | readonly        | normal        | normal        | stopped     |
| warehouse   | localhost:30420 | group1          | readonly        | normal        | normal        | stopped     |
| warehouse   | localhost:30510 | group2          | normal          | normal        | normal        | ----------- |
| warehouse   | localhost:30520 | group2          | normal          | normal        | normal        | ----------- |
+-------------+-----------------+-----------------+-----------------+-------------------------------+-------------+
  
## Change the group state to readonly
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

#### Snapshot related properties

|Property|Description|Applies to|
|--|--|--|
|GROUP_SNAPSHOT_TIMEOUT_SEC|Determines the timeout time when executing Snapshot<br>Default : 60 (sec)<br>Minimum : 0 (wait infinitely)<br>Maximum : uint32_max (sec)|Write in each node's machbase.conf file|
