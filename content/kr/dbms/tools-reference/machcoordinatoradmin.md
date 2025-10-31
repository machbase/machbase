---
title : 'machcoordinatoradmin'
type : docs
weight: 50
---

Coordinator는 클러스터 전체 관리 도구입니다.

클러스터 에디션 패키지에만 존재합니다.

## 옵션 및 기능

machcoordinatoradmin의 옵션은 다음과 같습니다. 이전 섹션에서 설명한 기능은 생략되었습니다.

```
mach@localhost:~$ machcoordinatoradmin -h
```


|옵션| 설명|
|--|--|
|-u, --startup | Coordinator 프로세스 실행|
|-s, --shutdown | Coordinator 프로세스 종료|
|-k, --kill| Coordinator 프로세스 중지|
|-c, --createdb | Coordinator 메타 생성|
|-d, --destroydb| Coordinator 메타 제거, $MACHBASE_COORDINATOR_HOME/package의 패키지 파일 삭제|
|-e, --check | Coordinator 프로세스 실행 여부 확인|
|-i, --silence | 출력 없이 실행|
|--configuration[=name] | 설정의 키와 값 출력 (특정 키만 출력 가능)|
|--configure | 시스템 속성 목록 출력 |
|--activate | 클러스터 상태를 Service로 전환|
|--deactivate | 클러스터 상태를 Deactivate로 전환|
|--list-package[=package] | 등록된 패키지 정보 목록 출력 (특정 패키지만 출력 가능)|
|--add-package=package | 패키지 추가|
|--remove-package=package | 패키지 삭제|
|--list-node[=node] | 노드 정보 목록 출력 (특정 노드만 출력 가능)|
|--add-node=node | 노드 추가|
|--remove-node=node | 노드 삭제|
|--upgrade-node=node | 노드 업그레이드|
|--startup-node=node | 노드 실행|
|--shutdown-node=node | 노드 종료|
|--kill-node=node | 노드 중지|
|--cluster-status | 클러스터의 각 노드 상태 출력|
|--cluster-status-full | 클러스터의 각 노드 상태를 상세히 출력|
|--cluster-node | 클러스터 정보 출력|
|--set-group-state=`[normal | readonly]` | 특정 웨어하우스 그룹의 상태 변경
|--get-host-resource | 각 노드가 위치한 호스트 리소스 정보 출력|
|--host-resource-enable | 각 노드의 호스트 리소스 정보 수집 시작|
|--host-resource-disable | 각 노드의 호스트 리소스 정보 수집 중지|

|추가 옵션|설명|필수 옵션|
|--|--|--|
--file-name=filename | 파일 이름| --add-package|
|--port-no=portno | 포트 번호| --add-node|
|--deployer=node | Deployer 노드 이름| --add-node|
|--package-name=packagename | 설치 소스가 될 패키지 이름| --add-package|
|--home-path=path | Deployer 서버 기준, 현재 노드의 설치 경로| --add-node|
|--node-type=`[broker | warehouse]` | 설치할 노드 유형 (broker/warehouse 중 선택)| --add-node |
|--group=groupname | 설치할 노드의 그룹 이름| --add-node |
|--replication=host:port | 복제를 교환할 host:port| --add-node |
|--no-replicate |설치할 노드에서 복제를 사용하지 않음 |--add-node|
|--primary=host:port | Secondary Coordinator 설치 시 Primary Coordinator의 노드 이름 지정 |-u, --startup|
|--host=host | 호스트 리소스 정보를 출력할 특정 호스트 지정| --get-host-resource|
|--metric=`[cpu|memory|disk|network]` | 호스트 리소스 정보를 출력할 특정 메트릭 지정| --get-host-resource|

## 실행 상태 확인

예제:

```
mach@localhost:~$ machcoordinatoradmin -e
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Machbase Coordinator is running with pid(29245)!
```

## 메타 생성 / 삭제

예제:

```
mach@localhost:~$ machcoordinatoradmin -c
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Coordinator metadata created successfully.
  
mach@localhost:~$ machcoordinatoradmin -d
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Coordinator metadata destroyed successfully.
```

## 설정 출력

구문:

```
machcoordinatoradmin --configuration[=name]
```

예제:

```
mach@localhost:~$ machcoordinatoradmin --configuration
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Name  : CLUSTER
Value : 3
 
Name  : DECISION
Value : ON
 
Name  : HOST-RESOURCE
Value : OFF
  
mach@localhost:~$ machcoordinatoradmin --configuration=decision
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
              Name : DECISION
             Value : ON
            Format : text/plain
```

## 시스템 속성 목록 출력

구문

```
machcoordinatoradmin --configure
```

예제

```
mach@localhost:~$ machcoordinatoradmin --configure

CLUSTER_LINK_HOST=192.168.0.30
CLUSTER_LINK_PORT_NO=36110
CLUSTER_LINK_THREAD_COUNT=16
CLUSTER_LINK_MAX_LISTEN=512
CLUSTER_LINK_MAX_POLL=4096
CLUSTER_LINK_ACCEPT_TIMEOUT=5000000
CLUSTER_LINK_CHECK_INTERVAL=1000000
CLUSTER_LINK_CONNECT_RETRY_TIMEOUT=60000000
CLUSTER_LINK_CONNECT_TIMEOUT=5000000
CLUSTER_LINK_HANDSHAKE_TIMEOUT=5000000
CLUSTER_LINK_LONG_TERM_CALLBACK_INTERVAL=1000000
CLUSTER_LINK_LONG_WAIT_INTERVAL=1000000
CLUSTER_LINK_RECEIVE_TIMEOUT=5000000
CLUSTER_LINK_REQUEST_TIMEOUT=60000000
CLUSTER_LINK_SEND_TIMEOUT=5000000
CLUSTER_LINK_SESSION_TIMEOUT=3600000000
CLUSTER_LINK_ERROR_ADD_ORIGIN_HOST=0
CLUSTER_LINK_BUFFER_SIZE=33554432
..
..
```


## 클러스터 상태 변경

예제:

```
mach@localhost:~$ machcoordinatoradmin --activate
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
              Name : CLUSTER
             Value : 3
            Format : text/plain
 
 
mach@localhost:~$ machcoordinatoradmin --deactivate
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
              Name : CLUSTER
             Value : 0
            Format : text/plain 
```

## 패키지 정보 목록 출력

구문:

```
machcoordinatoradmin --list-package[=package]
```

예제:

```
mach@localhost:~$ machcoordinatoradmin --list-package
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Package Name : machbase
File Name    : machbase-cluster-6bab497c9.develop-LINUX-X86-64-release-lightweight.tgz
File Size    : 64630670 bytes
 
Package Name : machbase2
File Name    : machbase-cluster-e3c0717.develop-LINUX-X86-64-release-lightweight.tgz
File Size    : 64677030 bytes
 
 
mach@localhost:~$ machcoordinatoradmin --list-package=machbase
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Package Name : machbase
File Name    : machbase-cluster-6bab497c9.develop-LINUX-X86-64-release-lightweight.tgz
File Size    : 64630670 bytes
```


## 노드 정보 목록 출력

구문:

```
machcoordinatoradmin --list-node[=node]
```

예제:

```
mach@localhost:~$  machcoordinatoradmin --list-node
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Node Name             : 192.168.0.32:5101
Node Type             : coordinator
HTTP Admin Port       : 5102
Group Name            : Coordinator
Desired State         : primary
Actual State          : primary
Coordinator Host      : 192.168.0.32:5101
Last Response Time    : 497590
Last Modify Time      : 421020408
Last Response Elapsed : 1006148
 
Node Name             : 192.168.0.32:5201
Node Type             : deployer
Group Name            : Deployer
Desired State         : normal
Actual State          : normal
Coordinator Host      : 192.168.0.32:5101
Last Response Time    : 497594
Last Modify Time      : 404915419
Last Response Elapsed : 1006128
 
Node Name             : 192.168.0.32:5301
Node Type             : broker
Port Number           : 5757
Deployer              : 192.168.0.32:5201
Package Name          : machbase
Home Path             : /home/machbase/broker1
Group Name            : Broker
Desired State         : leader
Actual State          : leader
Coordinator Host      : 192.168.0.32:5101
Last Response Time    : 497544
Last Modify Time      : 353606480
Last Response Elapsed : 1006157
 
Node Name             : 192.168.0.32:5401
Node Type             : warehouse
Port Number           : 5400
Deployer              : 192.168.0.32:5201
Package Name          : machbase
Home Path             : /home/machbase/warehouse_a1
Group Name            : Group1
Desired State         : normal
Actual State          : normal
Coordinator Host      : 192.168.0.32:5101
Last Response Time    : 497556
Last Modify Time      : 332480933
Last Response Elapsed : 1006160
  
mach@localhost:~$  machcoordinatoradmin --list-node=192.168.0.32:5401
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Node Name             : 192.168.0.32:5401
Node Type             : warehouse
Port Number           : 5400
Deployer              : 192.168.0.32:5201
Package Name          : machbase
Home Path             : /home/cumulus/warehouse_a1
Group Name            : Group1
Desired State         : normal
Actual State          : normal
Coordinator Host      : 192.168.0.32:5101
Last Response Time    : 648879
Last Modify Time      : 419153148
Last Response Elapsed : 1005962
```


## 클러스터 노드 상태 출력

예제:

```
mach@localhost:~$ machcoordinatoradmin --cluster-status
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
+-------------+-------------------+-------------------+-------------------+--------------+
|  Node Type  |     Node Name     |    Group Name     |    Group State    |     State    |
+-------------+-------------------+-------------------+-------------------+--------------+
| coordinator | 192.168.0.32:5101 | Coordinator       | normal            | primary      |
| deployer    | 192.168.0.32:5201 | Deployer          | normal            | normal       |
| broker      | 192.168.0.32:5301 | Broker            | normal            | leader       |
| warehouse   | 192.168.0.32:5401 | Group1            | normal            | normal       |
+-------------+-------------------+-------------------+-------------------+--------------+
 
mach@localhost:~$ machcoordinatoradmin --cluster-status-full
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
+-------------+-------------------+-------------------+-------------------+-------------------------------+-------------+
|  Node Type  |     Node Name     |    Group Name     |    Group State    |    Desired & Actual State     |  RP State   |
+-------------+-------------------+-------------------+-------------------+-------------------------------+-------------+
| coordinator | 192.168.0.32:5101 | Coordinator       | normal            | primary       | primary       | ----------- |
| deployer    | 192.168.0.32:5201 | Deployer          | normal            | normal        | normal        | ----------- |
| broker      | 192.168.0.32:5301 | Broker            | normal            | leader        | leader        | ----------- |
| warehouse   | 192.168.0.32:5401 | Group1            | normal            | normal        | normal        | ----------- |
+-------------+-------------------+-------------------+-------------------+-------------------------------
```


## 클러스터 정보 출력

예제:

```
mach@localhost:~$ machcoordinatoradmin --cluster-node
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Token Pid      : 29245
Token Time     : 1553153902646178
Modify Time    : 1553154010296715
Modify Count   : 8
Cluster Status : Service
Broker         : 192.168.0.32:5301
Warehouse      : 192.168.0.32:5401
```


## 그룹 상태 변경

구문:

```
machcoordinatoradmin --set-group-state=[ normal | readonly ] --group=group
```

예제:

```
mach@localhost:~$ machcoordinatoradmin --set-group-state=readonly --group=Group1
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Group Name: Group1
Flag      : 1
  
mach@localhost:~$ machcoordinatoradmin --cluster-status
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
+-------------+-------------------+-------------------+-------------------+--------------+
|  Node Type  |     Node Name     |    Group Name     |    Group State    |     State    |
+-------------+-------------------+-------------------+-------------------+--------------+
| coordinator | 192.168.0.32:5101 | Coordinator       | normal            | primary      |
| deployer    | 192.168.0.32:5201 | Deployer          | normal            | normal       |
| broker      | 192.168.0.32:5301 | Broker            | normal            | leader       |
| warehouse   | 192.168.0.32:5401 | Group1            | readonly          | normal       |
+-------------+-------------------+-------------------+-------------------+--------------+
```

## 호스트 리소스 출력

구문:

```
machcoordinatoradmin --host-resource-enable [--metric=metric] [host=host]
```

예제:

```
mach@localhost:~$ machcoordinatoradmin --host-resource-enable
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
              Name : HOST-RESOURCE
             Value : ON
            Format : text/plain
  
mach@localhost:~$ machcoordinatoradmin --get-host-resource
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Host Name : 192.168.0.32
   CPU Info :
      Model Name          : Intel(R) Xeon(R) CPU E3-1231 v3 @ 3.40GHz
      Number of CPUs      : 8
      Number of CPU Cores : 4
      CPU Utilization     : 14.0%
      CPU IOWait Ratio    : 0.0%
   Memory Info :
      Physical Memory Utilization : 99.1%
      Virtual Memory Utilization  : 98.6%
   Network Info :
      Receive Bytes(per second)    : 42809
      Receive Packets(per second)  : 337
      Transmit Bytes(per second)   : 42885
      Transmit Packets(per second) : 332
   Disk Info :
      /dev/sda1 : 87.4%
         |-> 192.168.0.32:5101   /home/cumulus/coordinator1
         |-> 192.168.0.32:5301   /home/cumulus/broker1
         |-> 192.168.0.32:5401   /home/cumulus/warehouse_a1
Host Name : 192.168.0.33
   CPU Info :
      Model Name          : Intel(R) Xeon(R) CPU E3-1231 v3 @ 3.40GHz
      Number of CPUs      : 8
      Number of CPU Cores : 4
      CPU Utilization     : 2.0%
      CPU IOWait Ratio    : 0.0%
   Memory Info :
      Physical Memory Utilization : 46.9%
      Virtual Memory Utilization  : 22.8%
   Network Info :
      Receive Bytes(per second)    : 12336
      Receive Packets(per second)  : 103
      Transmit Bytes(per second)   : 13500
      Transmit Packets(per second) : 103
   Disk Info :
      /dev/sda1 : 64.2%
         |-> 192.168.0.33:5101   /home/cumulus/coordinator2
         |-> 192.168.0.33:5401   /home/cumulus/warehouse_a2
  
mach@localhost:~$ machcoordinatoradmin --get-host-resource --metric=cpu
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Host Name : 192.168.0.32
   CPU Info :
      Model Name          : Intel(R) Xeon(R) CPU E3-1231 v3 @ 3.40GHz
      Number of CPUs      : 8
      Number of CPU Cores : 4
      CPU Utilization     : 13.9%
      CPU IOWait Ratio    : 0.0%
Host Name : 192.168.0.33
   CPU Info :
      Model Name          : Intel(R) Xeon(R) CPU E3-1231 v3 @ 3.40GHz
      Number of CPUs      : 8
      Number of CPU Cores : 4
      CPU Utilization     : 1.9%
      CPU IOWait Ratio    : 0.0%
  
mach@localhost:~$ machcoordinatoradmin --get-host-resource --host=192.168.0.33
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
Host Name : 192.168.0.33
   CPU Info :
      Model Name          : Intel(R) Xeon(R) CPU E3-1231 v3 @ 3.40GHz
      Number of CPUs      : 8
      Number of CPU Cores : 4
      CPU Utilization     : 2.0%
      CPU IOWait Ratio    : 0.0%
   Memory Info :
      Physical Memory Utilization : 46.9%
      Virtual Memory Utilization  : 22.8%
   Network Info :
      Receive Bytes(per second)    : 12588
      Receive Packets(per second)  : 106
      Transmit Bytes(per second)   : 13330
      Transmit Packets(per second) : 100
   Disk Info :
      /dev/sda1 : 64.2%
         |-> 192.168.0.33:5101   /home/cumulus/coordinator2
         |-> 192.168.0.33:5401   /home/cumulus/warehouse_a2
  
mach@localhost:~$ machcoordinatoradmin --host-resource-disable
-------------------------------------------------------------------------
     Machbase Coordinator Administration Tool
     Release Version - e3c0717.develop
     Copyright 2014, MACHBASE Corp. or its subsidiaries
     All Rights Reserved
-------------------------------------------------------------------------
              Name : HOST-RESOURCE
             Value : OFF
            Format : text/plain
```
