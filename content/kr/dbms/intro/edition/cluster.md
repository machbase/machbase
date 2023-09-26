---
title : "Cluster Edition"
type: docs
weight: 20
---

Cluster Edition은, 빠른 입력 속도와 표준 SQL로 조회가 가능한 Machbase Standard Edition 으로도 처리할 수 없는 초대용량의 데이터 입력/조회를 분산 환경에서 처리할 수 있는 제품이다.

## 왜 Cluster Edition을 써야 하는가?

Machbase 초고속으로 시계열 데이터를 입력받을 수 있는 Standard Edition 을 서비스하고 있다. 그러나, 다음의 단점이 존재한다.

* 하나의 프로세스로 구성되어 있기 때문에, 가용성이 떨어진다.
* 데이터를 분석할 때 하나의 프로세스가 전담하므로, 대용량 데이터 분석 성능을 늘리는 데 한계가 있다.

위의 단점을 극복하기 위해, 즉 가용성을 확보하고 대용량 데이터를 저장하고 분석하는데 확장성을 확보할 수 있는 새로운 제품군이 필요하다. 이런 요구사항을 만족할 수 있는 것이 Machbase Cluster Edition 이다.

## 용어

Host

물리적인 서버 1대, 또는 클라우드/VM 에서의 OS 인스턴스 1대를 나타낸다.

Node

서버에 상주하는 Machbase Process 를 나타낸다.

Process 타입은 아래의 Node Type 과 동일하다.

* Coordinator
* Deployer
* Lookup
* Broker
* Warehouse

## 구조

Machbase Cluster Edition 은, Host 에 상주하는 여러 Node 가 하나의 클러스터를 구성한다.

![clusteredition](../clusteredition.png)

고가용성

내부의 모든 Node 중 하나가 중단되어도 서비스가 지속될 수 있도록 한다

고확장성

데이터 저장을 분산할 수 있고, 분산된 데이터에서 병렬 분석이 가능하므로 클러스터를 확장할수록 성능이 증가한다.

#### Node의 분류

각 Node는 다음과 같이 분류할 수 있다.

| 분류 | 설명 | 프로세스 이름|
| -- | -- | -- |
| Coordinator | 모든 범용 서버와 Node를 관리하는 프로세스 | machcoordinatord |
| Deployer | Host 마다 하나씩 상주하는 프로세스<br> Broker/Warehouse 의 설치와 업그레이드, 상태 관찰을 담당한다.| machdeployerd |
| Lookup | Lookup 테이블 데이터를 가지고 있는 프로세스 | machlookupd |
| Broker | 실제 클라이언트 프로그램을 맞이하는 프로세스<br> 클라이언트의 데이터 입력/데이터 조회 쿼리를 Warehouse 에 분산 수행시키는 역할을 한다.| machbased |
| Warehouse | 실제 데이터를 저장하고 있는 프로세스<br> 전체 클러스터 데이터 중 일부를 저장하고 있으며, Broker 로부터 전달받은 명령을 수행한다.| machbased|

#### Coordinator

Coordinator는 모든 Node의 상태를 관리하는 Process로, 최대 2개를 가질 수 있다.

먼저 생성된 Coordinator를 Primary Coordinator, 그 다음을 Secondary Coordinator라 하고 Primary Coordinator만이 모든 Node의 상태를 관리한다.

Primary Coordinator가 종료하면 Secondary Coordinator가 Primary Coordinator로 격상된다.

#### Deployer

Coordinator에 의해 관리되지만, 단순히 Broker/Warehouse/Lookup Node의 설치/제거를 담당하는 Process 이다.

보통은 Node 를 설치할 Host 에 1대씩 추가하지만, 설치 성능을 위해 여러 Deployer를 추가할 수도 있다.

![deployer](../deployer.png)

![deployer2](../deployer2.png)


서버에서 설치 예제

아래 그림(a)는, 범용 서버 4대에 2개의 Coordinator, 2개의 Broker, 4개의 Warehouse Active, 4개의 Warehouse Standby Node를 설치한 것을 나타낸 것이다.
그림 처럼, 범용 서버의 호스트 이름과 할당된 포트 번호가 이어진 **'hostname:port'** 로 각 Node를 구분할 수 있다.

![deploynode](../deploynode.png)

#### Lookup

Lookup은 Lokkup Table 데이터 관리를 위해 존재한다.


#### Broker

Broker는 말 그대로 Client의 명령을 Warehouse에게 전달하고, Warehouse의 결과를 Client에 모아서 전달하는 역할을 한다.

* 데이터 입력 시, Broker는 Warehouse에게 데이터 입력을 골고루 가도록 한다.
* 이터 조회 시, Broker는 Warehouse에게 데이터를 가져오도록 한 뒤에 모든 결과를 모아서 전달한다.

Broker는 Log Table의 데이터를 가지고 있지 않지만, Volatile Table의 데이터는 가지고 있는다.


#### Warehouse

Warehouse 는 Log Table 데이터를 직접 저장하게 되고, Broker가 전달한 명령을 실제로 수행하는 역할을 한다.

Broker 처럼 Warehouse 에도 직접 클라이언트 접속이 가능하지만, 데이터 입력/갱신/삭제는 할 수 없고 오로지 해당 Warehouse 데이터 조회만 가능하다.

Warehouse Group

Warehouse 는, 자신이 속할 Group 을 지정할 수 있다.

* Broker 가 데이터를 입력할 때, 같은 Group 에 있는 모든 Warehouse는 동일한 레코드를 입력받는다.
* Group 의 특정 Warehouse 가 탈락하더라도, 데이터 조회는 이상 없다.
* Group 에 새로운 Warehouse 가 추가되면, 이중화 (Replication) 를 통해 동일한 레코드를 유지한다.

Warehouse Group 의 상태

|상태|INSERT/APPEND|SELECT|
|--|--|--|
|Normal| O | O |
|Readonly| X | O |

Readonly 상태로 변하는 조건은 다음과 같다.

* INSERT/APPEND 도중, Group 의 일부 Warehouse 가 입력에 실패하는 경우
  * 실패한 Warehouse 와 성공한 Warehouse 간의 데이터 불일치가 발생했기 때문에,
    실패한 Warehouse 는 Scrapped 상태로 만들고 해당 Group 은 더 이상의 입력을 받지 않기 위해 Readonly 상태로 전환된다. (warning)
* 새로운 Warehouse 가 추가된 경우
  * 이중화 과정이 진행되는 동안에도 입력을 받게 되면, 이중화 끝을 알 수 없기 때문에 Readonly 상태로 전환된다. (warning)


#### Node의 Port 관리

![nodeport](../node_port.png)

|Port 구분| 설명 | 필요한 Node |
|--|--|--|
|Cluster Port | Node 간 통신을 위한 Port | 모든 Node|
|Service Port | Client 가 직접 접속하는 Port | Broker/Warehouse|
|Admin Port | 관리 목적으로 통신하는 Port | Coordinator/Deployer|
|Replication Port| Warehouse 간에 Replication 용 통신을 위한 Port | Warehouse|

직접 접속 후, 수행 가능한 명령

다음은 각 Node에 직접 접속해서, 명령 수행이 가능한 것과 불가능한 것을 표로 나타낸 것이다.
모든 Node는 Client 를 통한 접속이 가능하지만, Node 종류에 따라 불가능한 쿼리가 존재한다

| | Broker (Leader) | Broker (non-leader) | Warehouse Standby|
|--|--|--|--|
|Client 접속| O | O | O |
|DDL | O | X | X |
|DELETE | O | O | X |
|INSERT| O | O | X |
|APPEND| O | O | X |
|SELECT| O | O | O |

## 데이터 저장/조회

Machbase Cluster Edition 은 데이터를 분산 저장하고, 분산 쿼리 수행으로 계산되는 결과를 수집할 수 있다. 여기서는 테이블 종류에 따라 어떻게 저장되고 조회되는지 설명한다.

#### 데이터 저장

###### Log Table

Broker를 통해 Log Table에 데이터를 입력하는 경우, 모든 Warehouse에 분산 저장된다. (입력을 수행하는 Broker에는 데이터가 저장되지 않는다.) Coordinator가 각 Warehouse의 데이터베이스 크기를 판단, 그 기준으로 Broker가 분산 저장한다.

Warehouse를 통해 직접 Log Table에 데이터를 입력하는 경우, 해당 Warehouse에만 저장된다. 분산 알고리즘, 네트워크 병목으로 인한 성능 저하를 피하고자 하는 경우에 선택할 수 있다.

###### Volatile Table

Broker를 통해 Volatile Table에 데이터를 입력하는 경우, 해당 Broker에 저장된다. 즉, 다른 Broker에는 해당 데이터가 입력되지 않고 동기화되지도 않는다.

Volatile Table에 대한 이중화를 지원하지 않는 이유는, DELETE가 가능한 Volatile Table의 특성에 맞추면 이중화 성능에 영향을 미치기 때문이다.

Volatile Table은 Broker에서만 생성되므로, Warehouse에서 입력할 수 없다.

###### Lookup Table

Broker를 통해 Lookup 테이블에 데이터를 입력하는 경우, 입력한 데이터는 Lookup 노드에에 저장되며, Replication을 통해 다른 Broker들에게 복제된다.

###### Tag Table

Log 테이블의 저장 방식과 동일하다. 단, 신규 TagID를 포함하는 데이터를 입력할 경우 Leader Broker를 통해서만 입력할 수 있다.


#### 데이터 조회

###### Log Table

Broker를 통해 Log Table에 데이터를 조회하는 경우, 모든 Warehouse에 쿼리가 분산된다. 각 Warehouse는 쿼리를 실제로 수행하는데, 필요한 경우엔 Warehouse 간 중간 결과를 교환한다. 이렇게 생성된 부분 결과를 Broker가 수집, 최종 결과를 반환한다.

Warehouse를 통해 Log Table에 데이터를 조회하는 경우, 해당 Warehouse에서만 쿼리가 수행된다. 이 과정은 Fog Edition 에서의 쿼리 수행과 동일하다.

###### Lookup / Volatile Table

Broker를 통해 Volatile Table에 데이터를 조회하는 경우, Broker에서만 쿼리가 수행된다. 이 과정은 Fog Edition 에서의 쿼리 수행과 동일하다.

Warehouse를 통해서는 JOIN을 할 수 없는데, Volatile Table이 생성되지 않기 때문이다.

###### 두 테이블 간 JOIN

Broker를 통해서 Log Table과 Volatile Table 간 JOIN을 하는 경우, 접속한 Broker와 나머지 Warehouse 가 동시에 쿼리를 수행한다. Broker는 Volatile Table 결과를 Warehouse에게 나눠주며, Warehouse는 Broker가 전달한 데이터를 JOIN 해서 결과를 반환한다. 이렇게 생성된 부분 결과를 Broker가 수집, 최종 결과를 반환한다.

Warehouse를 통해서는 JOIN을 할 수 없는데, Volatile Table이 생성되지 않기 때문이다.


## 이중화

이중화란, 기존에 설치된 Node 의 실패를 대비해 똑같은 Node 를 복제하는 과정 또는 그 상태를 의미한다.

#### Coordinator Replication

Cluster Edition 에서 Coordinator는 최대 2개까지 생성이 가능하다.

두 Coordinator는 지속적으로 Cluster Node 정보를 계속 유지한다.
어느 한 쪽이 비정상적으로 종료되더라도, 나머지 Coordinator가 Cluster Node 관리를 계속 할 수 있다.

**Primary Coordinator가 재시작되면 기존의 secondary coordinator가 primary로 격상되고, 재시작하는 coordinator는 secondary가 된다.**

#### Lookup Replication

기본적으로 Lookup Master가 Lookup Table 데이터를 관리하지만, Lookup Slave를 추가하여 데이터를 복제하도록 할 수 있다.

#### Broker Replication

**Broker는 Replication 대상이 아니다.**

따라서 Broker A에 들어있는 Volatile Table의 데이터 레코드는 Broker B에 똑같이 유지되지 않는다. (not synchronized)
다만, Cluster 전체의 테이블/인덱스 스키마는 모두 동일하므로, Broker A에 Volatile Table VOL_TBL1 이 존재하면 Broker B에도 Volatile Table VOL_TBL1 이 존재한다.

#### Warehouse Replication

Group 에 새로운 Warehouse 가 추가되는 경우, 다음 과정을 통해서 Warehouse 가 이중화된다.

* Coordinator 가, 새로운 Warehouse 에게 DDL 이중화를 시작한다.
* Group 이 Readonly 상태로 전환된다.
* Group 중 1개의 Warehouse 가, 새로운 Warehouse 에게 데이터 이중화를 시작한다.
* 데이터 이중화가 끝나면 Group 은 Normal 상태로 전환된다.
* 데이터 입력의 경우, Broker 가 같은 Group 에는 같은 데이터를 전송함으로써 이중화를 보장한다.

## 복구 방법

Node가 비정상적으로 종료되어도, 아래와 같은 방법으로 서비스를 계속할 수 있다.

자세한 내용은 운영 가이드를 참고한다.

|종류|Fail-over 방법|
|--|--|
|Coordinator| Primary Coordinator가 비정상 종료되어도, Secondary Coordinator 가 Primary Coordinator가 되면서 클러스터 관리를 계속 할 수 있다.<br> 최악의 상황으로 Coordinator가 모두 종료되어도, 클러스터 관리를 할 수 없을 뿐 전체 서비스 (데이터 입력/조회) 는 계속 할 수 있다. <br> (물론, 이 때 Broker나 Warehouse가 종료되면 클러스터 관리를 할 수 없다.) |
|Deployer| 해당 Host 로 Node Operation (ADD, REMOVE..) 을 할 수 없고, 해당 Host 의 통계 정보를 수집할 수 없다.|
|Lookup| Lookup Master에세 장애가 발생하면 Lookup Monitor가 자동으로 감지하여 Lookup Slave 중 하나를 Lookup Master로 변경하여 계속적인 서비스 이용이 가능하게 한다.<br> 기존에 Lookup Slave가 존재하지 않았다면 데이터 복제가 되지 않는 상태이기에 안정적인 HA를 위해 Lookup Slave는 하나 이상 존재하는 것을 권장한다.|
|Broker| Broker가 종료되어도, 다른 Broker가 존재한다면 계속 서비스를 지속할 수 있다.<br>단, 종료된 Broker와 연결된 클라이언트의 접속은 끊어지기 때문에 다른 Broker로 재접속해야 한다.|
|Warehouse| Group 에 다른 Warehouse(s) 가 존재하면, 해당 Warehouse(s) 가 SELECT 와 APPEND 를 그대로 참여한다.|

## 지원되지 않는 기능

#### Query Statement

###### TABLESPACE

현재 Cluster Edition 에서는 테이블 스페이스 구분을 하지 않는다.

###### BACKUP / MOUNT

현재 Cluster Edition 에서는 데이터베이스 구분을 하지 않는다.

###### LOAD IN FILE

CSV 파일을 읽어 분산하는 기능은 현재 구현되어 있지 않다.

###### ALTER TABLE FORGERY CHECK

고객의 데이터가 변경되었는지 검증하기 위한 구문인데, Result File을 한 곳에 모을 수 없다.

#### Clause / Function

###### UNION ALL

실행 단위가 복잡하게 생성되므로, 현재 지원되지 않는다.

###### GROUP_CONCAT() function

각 Warehouse 에서 수집한 부분 그룹에 대한 CONCAT 내용 전체를, 단순 누적으로 처리할 수 없다.
(GROUP CONCAT에서 ORDER BY를 하는 경우)

###### TS_CHANGE_COUNT() function

각 Warehouse 에서 수집한 부분 그룹에 대한 TS_CHANGE_COUNT 결과를 단순 누적으로 처리할 수 없다.

게다가 TS_CHANGE_COUNT() 는 전체 결과가 정렬되어 있어야 의미가 있는데, Warehouse에 분산된 결과를 대상으로 하면 의미가 없다.

## 지원 하드웨어 및 운영체제

| CPU | Intel Core i Series (Nehalem~) 이상 권장 |
| -- | -- |
| Memory | 설치될 Node 1개 당 2GB 이상 권장 |
|운영체제 | Linux (Any distribution) |
