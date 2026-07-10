---
type: docs
title: '3.3 Cluster Edition 설치와 배포'
weight: 30
toc: true
---
Cluster Edition은 여러 노드에 분산 배포하는 구성으로, 대용량 시계열 데이터 수집이 필요한 산업 IoT·금융 tick 환경에 적합합니다.

## 노드 역할

| 노드 | 역할 |
|------|------|
| **Coordinator** | 클러스터 메타 정보 관리, 노드 상태 감시 |
| **Deployer** | 패키지 배포 및 노드 초기화 중계 |
| **Lookup** | 참조 데이터와 조회 처리 |
| **Broker** | SQL 파싱 및 쿼리 분배, 클라이언트 접점 |
| **Warehouse** | 실제 데이터 저장 및 쿼리 실행 |

최소 구성은 Coordinator 1, Deployer 1, Lookup 2(master 1, monitor 1), Broker 1,
Warehouse 2(그룹당 2노드로 복제) 입니다.

## 배포 방식

| 방식 | 설명 | 적합한 경우 |
|------|------|------------|
| [machclusterctl](/dbms/installation-deployment-upgrade/cluster-edition/#machclusterctl) | cluster.yaml 기반 자동 배포 | 권장. 신규 구축 |
| [수동 (machcoordinatoradmin)](/dbms/installation-deployment-upgrade/cluster-edition/#manual-machcoordinatoradmin) | Coordinator 명령 기반 노드 등록·배포 | 세밀한 제어가 필요한 경우 |

## 설치 순서

1. [Cluster Edition 구성 개요](/dbms/installation-deployment-upgrade/cluster-edition/#overview) 숙지
2. [환경 준비](/dbms/installation-deployment-upgrade/cluster-edition/#preparation-environment-cluster-edition) (SSH 키, 커널 파라미터, NTP)
3. 배포 방식 선택 후 설치 진행
4. [라이선스 설치](/dbms/installation-deployment-upgrade/pre-install-preparation/#license)
5. [설치 검증](/dbms/installation-deployment-upgrade/validation-checklist/)

---

<a id="overview"></a>

## Cluster Edition 구성 개요

역할이 분리된 Coordinator, Deployer, Lookup, Broker, Warehouse 노드로 구성됩니다. 각 노드의 역할과 상호 관계를 이해한 후 배포 계획을 세우십시오.

### 노드 역할 상세

#### Coordinator

클러스터 전체의 메타 정보를 관리하며, 노드 등록, 상태 감시, 장애 감지를 담당합니다. Primary/Secondary 이중화를 권장합니다. Coordinator가 다운되어도 이미 실행 중인 Broker·Warehouse의 INSERT·SELECT는 중단되지 않습니다.

- 설정 파일: `$MACHBASE_COORDINATOR_HOME/conf/machbase.conf`
- 관리 도구: `machcoordinatoradmin`
- 주요 포트: `CLUSTER_LINK_PORT_NO`, `HTTP_ADMIN_PORT`

기본값은 `CLUSTER_LINK_PORT_NO=3868`, `HTTP_ADMIN_PORT=5779`입니다. 이 장의 예제에서는 운영 중 포트 충돌을 피하기 위해 Coordinator link/admin 포트로 `5101`/`5102`를 명시합니다.

#### Deployer

Coordinator의 지시에 따라 각 노드에 패키지를 배포하고 초기화를 중계합니다. 각 노드 호스트에 하나씩 배치하거나, 별도 배포 서버로 운영합니다.

- 관리 도구: `machdeployeradmin`

#### Lookup

참조 데이터와 조회 처리를 위한 노드입니다. 구성에 따라 master, monitor, slave 역할을 지정합니다.

#### Broker

클라이언트의 SQL 요청을 받아 파싱하고 적절한 Warehouse로 분배합니다. 애플리케이션은 Broker 주소로만 연결하며, Warehouse와 직접 통신하지 않습니다. 이중화를 권장합니다.

- 클라이언트 접속 포트: 기본 5656

#### Warehouse

실제 데이터를 저장하고 쿼리를 실행합니다. 같은 그룹의 Warehouse끼리 데이터를 복제하여 고가용성을 제공합니다. 그룹당 2개 이상을 권장합니다.

### 구성 예시

```
[클라이언트]
     │ (SQL, 5656)
     ▼
[Broker ×2]  ──────────────────────────────────────────
     │ (쿼리 분배)
     ├─► [Warehouse group1-node1] ◄──복제──► [Warehouse group1-node2]
     └─► [Warehouse group2-node1] ◄──복제──► [Warehouse group2-node2]

[Coordinator Primary] ◄──HA──► [Coordinator Secondary]
     │ (메타 관리, 노드 감시)
[Deployer]
     │
[Lookup master / monitor]
```

### 에디션 비교

Standard Edition과의 상세 비교는 [에디션 차이점](/dbms/core-concepts/concepts-edition/#differences-standard-edition-cluster)을 참고하십시오.

---

<a id="preparation-environment-cluster-edition"></a>

## Cluster Edition 설치 환경 준비

배포 전에 모든 노드에 다음 환경을 준비합니다.

### 파일 디스크립터 한도

모든 노드에서 아래 설정을 적용합니다.

```bash
sudo vi /etc/security/limits.conf
```

```
*  hard  nofile  65535
*  soft  nofile  65535
```

재부팅 후 확인합니다.

```bash
ulimit -Sn
# 65535
```

### OS 사용자 생성

모든 노드에 `machbase` 계정을 생성합니다.

```bash
sudo useradd machbase --home-dir /home/machbase
sudo passwd machbase
```

### SSH 키 기반 인증

`machclusterctl`을 사용하는 경우, 배포 서버에서 모든 노드로 비밀번호 없이 SSH 접속이 가능해야 합니다.

```bash
# 배포 서버에서 SSH 키 생성 (이미 있으면 생략)
ssh-keygen -t rsa -b 4096

# 각 노드에 공개 키 등록
ssh-copy-id machbase@<node-ip>
```

등록 후 비밀번호 없이 접속이 되는지 확인합니다.

```bash
ssh machbase@<node-ip> 'hostname'
```

### 네트워크 커널 파라미터

대용량 데이터 전송 성능을 위해 네트워크 버퍼를 늘립니다. 64 GB 메모리 기준 권장값입니다.

```bash
sudo sysctl -w net.core.rmem_default=33554432
sudo sysctl -w net.core.wmem_default=33554432
sudo sysctl -w net.core.rmem_max=268435456
sudo sysctl -w net.core.wmem_max=268435456
sudo sysctl -w 'net.ipv4.tcp_rmem=262144 33554432 268435456'
sudo sysctl -w 'net.ipv4.tcp_wmem=262144 33554432 268435456'
sudo sysctl -w 'net.ipv4.tcp_mem=8388608 8388608 8388608'
```

영구 적용은 `/etc/sysctl.conf`에 추가합니다.

### 시간 동기화 (NTP)

모든 노드의 시스템 시간이 일치해야 합니다. NTP 또는 `chrony`로 동기화하십시오.

```bash
# chrony 사용 예
sudo systemctl enable chronyd
sudo systemctl start chronyd
chronyc tracking
```

타임 서버를 사용할 수 없는 경우 직접 설정합니다.

```bash
sudo date -s "2025-01-02 12:34:56"
```

### 포트 예약

각 노드에서 Machbase가 사용할 포트를 예약합니다.

```bash
current=$(cat /proc/sys/net/ipv4/ip_local_reserved_ports)
ports=5101-5110,5201-5202,5301-5302,5401-5402,5500-5503,5656-5657
sudo sysctl -w net.ipv4.ip_local_reserved_ports="${current:+$current,}$ports"
```

기존 예약 포트가 있으면 덮어쓰지 말고 쉼표로 구분해 병합합니다. 클러스터 구성에 따라 포트 범위를 조정하십시오. Cluster link, admin, service, Broker/Warehouse HTTP 관리 포트, Warehouse replication manager 포트 등을 모두 포함해야 합니다.

---

<a id="machclusterctl"></a>

## machclusterctl 기반 배포

`machclusterctl`은 `cluster.yaml` 파일 하나로 전체 클러스터를 자동으로 배포하고 관리하는 도구입니다. SSH를 통해 각 노드에 원격 접속하여 패키지 배포, 초기화, 시작·종료를 일괄 처리합니다.

### 사전 조건

- 배포 서버에서 모든 노드로 SSH 키 기반 인증이 설정되어 있어야 합니다.
- [Cluster Edition 설치 환경 준비](/dbms/installation-deployment-upgrade/cluster-edition/#preparation-environment-cluster-edition) 완료

### 작업 순서

| 단계 | 문서 |
|------|------|
| 1. cluster.yaml 작성 | [cluster.yaml 작성](/dbms/installation-deployment-upgrade/cluster-edition/#machclusterctl-cluster-yaml) |
| 2. YAML 유효성 검사 | [YAML 검증](/dbms/installation-deployment-upgrade/cluster-edition/#machclusterctl-validation-yaml) |
| 3. 최초 설치 및 시작 | [최초 설치](/dbms/installation-deployment-upgrade/cluster-edition/#machclusterctl-initial) |
| 4. 상태 확인 | [상태 확인](/dbms/installation-deployment-upgrade/cluster-edition/#machclusterctl-status-check-state) |
| 5. (이후) 구성 변경 | [구성 변경 적용](/dbms/installation-deployment-upgrade/cluster-edition/#machclusterctl-configuration-change-alter) |
| 6. (장애 시) 복구 | [배포 실패 시 복구](/dbms/installation-deployment-upgrade/cluster-edition/#machclusterctl-failure-recovery) |

---

<a id="machclusterctl-cluster-yaml"></a>

### cluster.yaml 작성

`cluster.yaml`은 `machclusterctl`이 클러스터를 배포할 때 사용하는 선언적 설정 파일입니다. 클러스터 이름, 호스트 별칭, 패키지 경로, 노드별 포트와 홈 경로를 정의합니다.

#### 파일 구조 예시

```yaml
version: "1"

cluster:
  name: mc-prod

  hosts:
    node1:
      address: machbase@192.168.1.10
    node2:
      address: machbase@192.168.1.11
    node3:
      address: machbase@192.168.1.12

  package:
    name: machbase
    origin_path: /home/machbase/packages/machbase-cluster-8.6.0.official-LINUX-X86-64-release.tgz

  ssh:
    key_file: /home/machbase/.ssh/id_rsa

  defaults:
    coordinator:
      home_path: /home/machbase/coordinator
      cluster_link_port: 5101
      http_admin_port: 5102
    deployer:
      home_path: /home/machbase/deployer
      cluster_link_port: 5201
      http_admin_port: 5202
    lookup:
      home_path: /home/machbase/lookup
      cluster_link_port: 5301
    broker:
      home_path: /home/machbase/broker
      cluster_link_port: 5401
      http_port_no: 5402
      service_port: 5656
    warehouse:
      home_path: /home/machbase/warehouse
      cluster_link_port: 5501
      service_port: 5500

  coordinators:
    - alias: coord-primary-1
      host: node1
      role: primary

    - alias: coord-secondary-1
      host: node2
      role: secondary

  deployers:
    - alias: deployer-1
      host: node1

    - alias: deployer-2
      host: node2

    - alias: deployer-3
      host: node3

  lookup:
    - alias: lookup-master-1
      host: node1
      deployer: deployer-1
      type: master

    - alias: lookup-monitor-1
      host: node2
      deployer: deployer-2
      type: monitor

  brokers:
    - alias: broker-1
      host: node1
      deployer: deployer-1
      dbs_path: /data/machbase/broker-1/dbs

    - alias: broker-2
      host: node2
      deployer: deployer-2

  warehouse_groups:
    - name: group1
      nodes:
        - alias: warehouse-group1-1
          host: node2
          deployer: deployer-2
          dbs_path: /data/machbase/warehouse-group1-1/dbs

        - alias: warehouse-group1-2
          host: node3
          deployer: deployer-3
          dbs_path: /data/machbase/warehouse-group1-2/dbs
```

#### 주요 항목 설명

| 항목 | 설명 |
|------|------|
| `version` | YAML 스키마 버전입니다. 현재 `"1"`을 사용합니다. |
| `cluster.name` | 클러스터 이름입니다. `destroy` 확인 등에서 사용됩니다. |
| `cluster.hosts` | 노드에서 참조할 호스트 별칭과 SSH 접속 주소입니다. `address`는 `user@host` 형식을 사용합니다. |
| `cluster.package.name` | Coordinator에 등록할 패키지 이름입니다. |
| `cluster.package.origin_path` | `install`, `apply`, `upgrade` 실행 때 입력으로 사용할 패키지 archive 경로입니다. |
| `cluster.package.registered_path` | `export`가 기록하는 Coordinator package repository의 관찰 경로입니다. 실행 입력으로 사용하지 않습니다. |
| `cluster.ssh.key_file` | 대상 서버 접속에 사용할 private key 경로입니다. 비밀번호 필드는 사용하지 않습니다. |
| `cluster.defaults` | 노드 타입별 `home_path`, `cluster_link_port`, `service_port` 기본값입니다. |
| `cluster.coordinators` | Coordinator 노드 목록입니다. `role`은 `primary` 또는 `secondary`를 사용합니다. |
| `cluster.deployers` | Deployer 노드 목록입니다. |
| `cluster.lookup` | Lookup 노드 목록입니다. `type`은 `master`, `monitor`, `slave`를 사용합니다. |
| `cluster.brokers` | Broker 노드 목록입니다. 클라이언트 SQL 접속 포트는 `service_port`입니다. |
| `cluster.warehouse_groups` | Warehouse 그룹과 그룹별 노드 목록입니다. |

#### 권장 구성

- Coordinator: 2개 (Primary + Secondary HA)
- Deployer: 1개 이상
- Lookup: master 1개, monitor 1개 이상
- Broker: 2개 이상 (부하 분산)
- Warehouse 그룹: 그룹당 2개 (복제를 통한 고가용성)

같은 서버에 같은 타입의 노드를 2개 이상 배치할 때는 두 번째 노드부터 `home_path`와 포트를 명시적으로 지정하여 충돌을 피합니다.

Coordinator와 Deployer의 HTTP 관리 포트는 `http_admin_port`, Broker의 HTTP 포트는 `http_port_no`를 사용합니다.

Broker와 Warehouse 노드에는 선택적으로 `dbs_path`를 지정합니다. `dbs_path`는 노드가 설치되는 서버 기준의 데이터 파일 경로이며, 생략하면 `machcoordinatoradmin --add-node`의 기본 `DBS_PATH` 동작을 따릅니다.

기존 `cluster.package.path`는 하위 호환 입력으로 사용할 수 있지만, 새로 작성하는 YAML에서는 `origin_path`를 사용합니다.

Tag update가 반영된 빌드에서는 Lookup, Broker, Warehouse의 HTTP 관리 포트도 `http_admin_port`로 작성할 수 있습니다. `main` 또는 RDB 구현 브랜치 기반 빌드에서는 Broker HTTP 포트가 `http_port_no`로 기록되고, Lookup과 Warehouse의 `http_admin_port` 입력을 지원하지 않습니다.

작성이 완료되면 유효성을 검사합니다.

---

<a id="machclusterctl-validation-yaml"></a>

### YAML 검증

`cluster.yaml`을 실제 설치에 사용하기 전에 유효성 검사를 수행합니다. `validate`는 YAML 문법과 필수 값, 별칭, 포트 충돌, 토폴로지 관계를 정적으로 검사합니다.

#### 검증 명령

```bash
machclusterctl validate -f cluster.yaml
```

#### 검증 항목

| 항목 | 설명 |
|------|------|
| YAML 문법 | 파일 파싱 오류 여부 |
| 환경변수 치환 | `${VAR}` 또는 `${VAR:-default}` 표현식 해석 가능 여부 |
| 필수 필드 | 클러스터 이름, 호스트, 패키지, 노드별 필수 값 누락 여부 |
| 별칭 | 노드 alias 중복 여부 |
| 포트 충돌 | 같은 host 안에서 선언된 포트 충돌 여부 |
| 토폴로지 | Primary Coordinator, Lookup master/monitor, Deployer 참조 관계 |

#### 출력 예시

```text
Validation passed.
```

오류가 있으면 메시지에 표시된 항목을 수정한 뒤 재검증합니다.

#### 설치 전 실행 계획 확인

신규 설치 전에 SSH 접속, 패키지 파일 존재 여부, 원격 디렉터리 권한까지 확인하려면 `install --dry-run --verbose`를 사용합니다.

```bash
machclusterctl install -f cluster.yaml --dry-run --verbose
```

설치 후 구성 변경을 검증할 때는 `apply --dry-run`을 사용합니다. 현재 클러스터 상태와 YAML의 차이를 계산해 실행 계획을 보여주며, 실제 원격 변경 작업은 수행하지 않습니다.

```bash
machclusterctl apply -f cluster.yaml --dry-run --verbose
```

#### 일반적인 오류와 해결

| 오류 | 원인 | 해결 |
|------|------|------|
| `field ... not found` | 지원하지 않는 YAML 키 사용 | 현행 스키마의 `cluster.*` 항목으로 수정 |
| `required field ...` | 필수 값 누락 | 메시지에 표시된 필드를 추가 |
| `duplicate alias` | 노드 alias 중복 | 모든 노드 alias를 고유하게 변경 |
| `port conflict` | 같은 host에서 동일 포트 사용 | 해당 노드의 포트 또는 `home_path`를 명시적으로 분리 |
| `deployer ... not found` | Lookup/Broker/Warehouse가 존재하지 않는 Deployer를 참조 | `deployer` 값을 Deployer alias 또는 host:port로 수정 |

---

<a id="machclusterctl-initial"></a>

### 최초 설치

`cluster.yaml` 작성과 유효성 검사가 완료되면 설치 계획을 확인한 뒤 클러스터를 설치합니다.

#### 1. 클러스터 설치

패키지를 각 노드에 배포하고 초기화하기 전에 실행 계획과 사전 점검 결과를 확인합니다.

```bash
machclusterctl install -f cluster.yaml --dry-run --verbose
```

문제가 없으면 실제 설치를 실행합니다.

```bash
machclusterctl install -f cluster.yaml --yes --verbose
```

이 명령은 다음을 자동으로 처리합니다.

1. 패키지를 각 노드에 복사하고 압축 해제
2. 각 노드의 `machbase.conf` 생성 및 포트 설정
3. Coordinator 데이터베이스 초기화
4. 노드 등록 (Coordinator에 각 노드 추가)

#### 2. 클러스터 시작

`install`은 Coordinator, Deployer, Lookup, Broker, Warehouse를 준비하고 기동합니다. 설치 후 전체 클러스터를 다시 시작해야 할 때만 다음 명령을 사용합니다.

```bash
machclusterctl start
```

#### 3. 상태 확인

```bash
export MACHBASE_COORDINATOR_HOME=/home/machbase/coordinator
machclusterctl status
```

한 서버에서 여러 Coordinator 홈을 번갈아 확인할 때는 직접 지정합니다.

```bash
machclusterctl status --coordinator /home/machbase/coordinator
```

출력은 `machcoordinatoradmin --cluster-status-full --verbose` 형식입니다. Coordinator와 Broker는 `primary`, `leader` 같은 역할 상태가 표시될 수 있으며, Desired/Actual state가 서로 맞는지 확인합니다.

```
+-------------+--------------------------------+--------------------------------+--------------------------------+-------------------------------+-------------+-----------------+----------+
|  Node Type  |           Node Name            |           Group Name           |           Group State          |    Desired & Actual State     |  RP State   | Disk(%) (00/00) | Ping(μs) |
+-------------+--------------------------------+--------------------------------+--------------------------------+-------------------------------+-------------+-----------------+----------+
| coordinator | coord-1(192.168.1.10:5101)     | Coordinator                    | normal                         | primary       | primary       | ----------- | --------------- |      214 |
| deployer    | deployer-1(192.168.1.10:5201)  | Deployer                       | normal                         | running       | running       | ----------- | --------------- |      100 |
| broker      | broker-1(192.168.1.11:5401)    | Broker                         | normal                         | leader        | leader        | ----------- | --------------- |      100 |
| warehouse   | wh-g1-1(192.168.1.13:5501)     | group1                         | normal                         | normal        | normal        | running     | 26.9            |      100 |
+-------------+--------------------------------+--------------------------------+--------------------------------+-------------------------------+-------------+-----------------+----------+
```

#### 4. 클라이언트 접속 테스트

Broker 노드의 IP와 포트로 접속합니다.

```bash
machsql -s 192.168.1.11 -u SYS -p MANAGER
# Mach>
```

#### 클러스터 종료

```bash
machclusterctl stop
```

---

<a id="machclusterctl-status-check-state"></a>

### 상태 확인

클러스터 전체 노드의 상태를 한 번에 조회합니다.

#### 상태 조회

```bash
machclusterctl status
```

`MACHBASE_COORDINATOR_HOME`을 사용하지 않는 환경에서는 Primary Coordinator 홈을 직접 지정합니다.

```bash
machclusterctl status --coordinator /home/machbase/coordinator
```

또는 Coordinator 관리 도구로 직접 조회합니다.

```bash
machcoordinatoradmin --cluster-status-full --verbose
```

#### 출력 해석

```
+-------------+--------------------------------+--------------------------------+--------------------------------+-------------------------------+-------------+-----------------+----------+
|  Node Type  |           Node Name            |           Group Name           |           Group State          |    Desired & Actual State     |  RP State   | Disk(%) (00/00) | Ping(μs) |
+-------------+--------------------------------+--------------------------------+--------------------------------+-------------------------------+-------------+-----------------+----------+
| coordinator | coord-1(192.168.1.10:5101)     | Coordinator                    | normal                         | primary       | primary       | ----------- | --------------- |      214 |
| deployer    | deployer-1(192.168.1.10:5201)  | Deployer                       | normal                         | running       | running       | ----------- | --------------- |      100 |
| broker      | broker-1(192.168.1.11:5401)    | Broker                         | normal                         | leader        | leader        | ----------- | --------------- |      100 |
| warehouse   | wh-g1-1(192.168.1.13:5501)     | group1                         | normal                         | normal        | normal        | running     | 26.9            |      100 |
+-------------+--------------------------------+--------------------------------+--------------------------------+-------------------------------+-------------+-----------------+----------+
```

| 값 | 의미 |
|----|------|
| `normal` | 정상 동작 |
| `primary` | Coordinator Primary |
| `sync-active` | 복제 송신 역할 |
| `sync-standby` | 복제 수신 역할 |
| `inactive` | 비활성 상태 |
| `scrapped` | 장애 감지, 복구 필요 |
| `ddl-incompl` | DDL 처리 미완료 상태 |
| `ddl-recov` | DDL 복구 진행 상태 |
| `**unknown**` | 통신 불가, 노드 다운 의심 |

`leader`처럼 Broker 역할을 나타내는 값은 Desired/Actual state나 그룹 상태 영역에 표시될 수 있습니다.

#### Desired vs Actual State

- **Desired State**: Coordinator가 기대하는 상태
- **Actual State**: 노드의 실제 상태

두 값이 다르면 노드가 전환 중이거나 이상 상태입니다. 오랫동안 차이가 유지되면 로그를 확인하십시오.

#### 서버 로그 확인

각 노드의 로그는 해당 노드의 홈 디렉터리 아래 `trc/`에 있습니다.

```bash
tail -f $MACHBASE_HOME/trc/machbase.trc
```

---

<a id="machclusterctl-configuration-change-alter"></a>

### 구성 변경 적용

클러스터 구성(노드 추가, 일반 노드 포트 변경 등)을 변경하려면 `cluster.yaml`을 수정한 후 적용합니다. Primary Coordinator 교체, 제거, identity 또는 포트 변경은 `apply`에서 지원하지 않습니다.

#### 구성 변경 절차

##### 1. cluster.yaml 수정

필요한 변경사항을 `cluster.yaml`에 반영합니다. 예를 들어 새 Warehouse 그룹을 추가하려면 해당 항목을 추가합니다.

```yaml
cluster:
  warehouse_groups:
    - name: group1
      nodes:
        - alias: warehouse-group1-1
          host: node2
          deployer: deployer-2
          ...
        - alias: warehouse-group1-2
          host: node3
          deployer: deployer-3
          ...
    - name: group2
      nodes:
        - alias: warehouse-group2-1
          host: node4
          deployer: deployer-4
          home_path: /home/machbase/warehouse-group2-1
          cluster_link_port: 5511
          service_port: 5510
        - alias: warehouse-group2-2
          host: node5
          deployer: deployer-5
          home_path: /home/machbase/warehouse-group2-2
          cluster_link_port: 5521
          service_port: 5520
```

##### 2. 유효성 검사

```bash
machclusterctl validate -f cluster.yaml
```

##### 3. 실행 계획 확인

```bash
machclusterctl apply -f cluster.yaml --dry-run --verbose
```

##### 4. 변경 적용

```bash
machclusterctl apply -f cluster.yaml --yes --verbose
machclusterctl status
```

`apply` 명령은 현재 클러스터 상태와 `cluster.yaml`의 차이를 계산하여 필요한 작업만 수행합니다.

#### 노드 제거

`cluster.yaml`에서 해당 노드 항목을 삭제하고 `apply`를 실행합니다. 단, Coordinator 제거와 Primary Coordinator 변경은 지원하지 않습니다. Warehouse 노드를 제거하기 전에는 해당 노드에 있는 데이터가 다른 노드에 충분히 복제되어 있는지 확인해야 합니다.

#### 주의사항

- DDL 또는 DELETE가 실행 중인 상태에서 구성 변경을 수행하지 마십시오.
- 구성 변경 중에는 노드 추가·시작·종료·삭제 작업을 병행하지 마십시오.
- INSERT·APPEND·SELECT는 Coordinator 부재 시에도 계속 동작하지만, 구성 변경 작업은 Coordinator가 정상이어야 합니다.

---

<a id="machclusterctl-failure-recovery"></a>

### 배포 실패 시 복구

`machclusterctl install` 또는 `apply` 실행 중 오류가 발생한 경우의 복구 방법입니다.

#### 설치 실패 시 재시도

설치 도중 오류가 발생하면 `machclusterctl install`은 이미 수행한 bootstrap과 노드 등록 작업을 rollback합니다. 로그에서 원인을 해결한 뒤 동일한 명령을 다시 실행합니다.

`machclusterctl apply` 중 오류가 발생한 경우에는 현재 상태를 먼저 확인합니다. 일부 노드 추가나 시작이 진행된 뒤 실패했을 수 있으므로, 상태에 맞게 `apply`를 재실행하거나 필요한 노드를 수동으로 정리합니다.

```bash
machclusterctl install -f cluster.yaml --yes --verbose
```

#### 클러스터 전체 초기화 후 재설치

오류 상태가 복잡하여 처음부터 다시 시작해야 하는 경우:

```bash
# 클러스터 전체 종료
machclusterctl stop

# 클러스터 제거 (데이터 포함)
machclusterctl destroy -f cluster.yaml --yes

# 재설치
machclusterctl install -f cluster.yaml --yes --verbose
```

`destroy`는 각 노드의 설치 흔적과 관리 대상 데이터 경로를 삭제합니다. 외부 `dbs_path` 처리 범위는 버전에 따라 다를 수 있으므로, 데이터 보존 목적으로 `destroy`를 사용하지 마십시오. **삭제된 데이터는 복구할 수 없습니다.**

#### Warehouse 노드 장애 복구

특정 Warehouse 노드에 장애가 발생하면 해당 노드의 상태가 `scrapped`로 전환됩니다.

```bash
# 1. 그룹 상태를 readonly로 변경 (추가 데이터 유입 방지)
machcoordinatoradmin --set-group-state=readonly --group=group1

# 2. 장애 노드 재시작 또는 복구

# 3. 스냅샷 기반 복구 (Snapshot Failover)
machcoordinatoradmin --snapshot-recover=192.168.1.13:5501

# 4. 복구 대상 Warehouse 동기화 실행
machcoordinatoradmin --exec-sync=192.168.1.13:5501

# 5. Warehouse 상태가 sync-standby를 거쳐 normal로 전환되는지 확인한 뒤 그룹 상태 복원
machcoordinatoradmin --cluster-status-full --verbose
machcoordinatoradmin --set-group-state=normal --group=group1
```

스냅샷 복구는 대상 Warehouse가 `scrapped`, Warehouse 그룹이 `readonly` 상태일 때 수행합니다. 복구 명령 뒤에는 `--exec-sync`를 실행하고, Warehouse가 `sync-standby`를 거쳐 `normal` 상태가 되는지 확인합니다.

#### 로그 확인

각 노드의 `trc/machbase.trc` 파일에서 오류 원인을 확인합니다.

```bash
ssh machbase@<node-ip> 'tail -100 /home/machbase/coordinator/trc/machbase.trc'
```

---

<a id="manual-machcoordinatoradmin"></a>

## machcoordinatoradmin 기반 수동 배포

`machclusterctl`을 사용할 수 없거나 각 단계를 직접 제어해야 하는 경우의 수동 클러스터 구성 방법입니다. Coordinator와 Deployer를 직접 준비한 뒤, `machcoordinatoradmin` 명령으로 패키지 등록, 노드 등록, 시작을 수행합니다.

### 수동 배포 순서

1. [Package 준비와 등록](/dbms/installation-deployment-upgrade/cluster-edition/#manual-machcoordinatoradmin-package) — 전체 패키지 설치와 경량 패키지 등록 준비
2. [Coordinator / Deployer 설치](/dbms/installation-deployment-upgrade/cluster-edition/#manual-machcoordinatoradmin-coordinator-deployer) — 핵심 관리 노드 구동
3. [Package 등록](/dbms/installation-deployment-upgrade/cluster-edition/#manual-machcoordinatoradmin-package) — 실행 중인 Coordinator에 경량 패키지 등록
4. [Lookup / Broker / Warehouse 설치](/dbms/installation-deployment-upgrade/cluster-edition/#manual-machcoordinatoradmin-lookup-broker-warehouse) — 데이터 처리 노드 등록 및 구동
5. [노드 상태 확인](/dbms/installation-deployment-upgrade/cluster-edition/#manual-machcoordinatoradmin-status-check-node-state) — 클러스터 정상 동작 검증

### machclusterctl 대비 차이점

| 항목 | machclusterctl | 수동 배포 |
|------|---------------|----------|
| 설정 방식 | cluster.yaml 단일 파일 | 각 노드 machbase.conf 직접 편집 |
| 패키지 배포 | 자동 원격 복사 | Coordinator/Deployer는 직접 설치, Broker/Warehouse는 Deployer가 배포 |
| 노드 등록 | 자동 | `machcoordinatoradmin --add-node` 수동 실행 |
| 일괄 시작·종료 | `machclusterctl start/stop` | 노드별 개별 실행 |

수동 배포는 유연성이 높지만 실수 가능성도 높습니다. 신규 구축에는 `machclusterctl`을 권장합니다.

---

<a id="manual-machcoordinatoradmin-package"></a>

### Package 준비와 등록

Cluster Edition 수동 배포의 패키지 준비와 등록 절차입니다. Coordinator와 Deployer에는 전체 패키지를 설치하고 환경 변수를 설정합니다. Broker와 Warehouse 배포에 사용할 경량 패키지는 Coordinator가 기동된 후에 등록합니다.

#### 패키지 종류

Cluster Edition에는 두 가지 패키지가 있습니다.

| 패키지 | 대상 노드 | 특징 |
|--------|-----------|------|
| 전체 패키지 | Coordinator, Deployer | 모든 실행 파일 포함 |
| 경량 패키지 (lightweight) | Broker, Warehouse | 데이터 처리에 필요한 파일만 포함, 크기 작음 |

파일명 예시:
- 전체: `machbase-cluster-8.6.0.official-LINUX-X86-64-release.tgz`
- 경량: `machbase-cluster-8.6.0.official-LINUX-X86-64-release-lightweight.tgz`

#### Coordinator와 Deployer에 패키지 배포

전체 패키지 파일을 Coordinator와 Deployer 노드에 복사하고 압축 해제합니다.

##### Coordinator 노드

```bash
# Coordinator 노드에서 실행
mkdir -p ~/coordinator
scp machbase@배포서버:/path/to/machbase-cluster-8.6.0.official-LINUX-X86-64-release.tgz ~/
tar zxf machbase-cluster-8.6.0.official-LINUX-X86-64-release.tgz -C ~/coordinator
```

##### Deployer 노드

```bash
mkdir -p ~/deployer
scp machbase@배포서버:/path/to/machbase-cluster-8.6.0.official-LINUX-X86-64-release.tgz ~/
tar zxf machbase-cluster-8.6.0.official-LINUX-X86-64-release.tgz -C ~/deployer
```

Broker와 Warehouse 노드에는 이 단계에서 경량 패키지를 직접 압축 해제하지 않습니다. 경량 패키지를 Coordinator에 등록하면, 이후 `--add-node`로 지정한 Deployer가 대상 노드의 `--home-path`에 패키지를 배포합니다.

#### Coordinator에 패키지 등록

Broker와 Warehouse를 Coordinator에서 기동하려면 경량 패키지를 Coordinator에 등록해야 합니다. Coordinator와 Deployer를 설치하고 Coordinator가 실행 중인 상태에서 다음 명령을 실행합니다.

```bash
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-package=machbase \
  --file-name="/home/machbase/machbase-cluster-8.6.0.official-LINUX-X86-64-release-lightweight.tgz"
```

등록된 패키지는 이후 Broker와 Warehouse를 `--add-node`로 등록할 때 `--package-name=machbase`로 참조합니다.

#### 환경 변수 설정

Coordinator와 Deployer 운영 계정의 `~/.bashrc`에 해당 역할에 맞는 HOME 경로를 설정합니다.

```bash
# Coordinator 노드
export MACHBASE_COORDINATOR_HOME=~/coordinator
export MACHBASE_HOME=$MACHBASE_COORDINATOR_HOME
export PATH=$MACHBASE_HOME/bin:$PATH
export LD_LIBRARY_PATH=$MACHBASE_HOME/lib:$LD_LIBRARY_PATH
source ~/.bashrc

# Deployer 노드
export MACHBASE_DEPLOYER_HOME=~/deployer
export MACHBASE_HOME=$MACHBASE_DEPLOYER_HOME
...
```

---

<a id="manual-machcoordinatoradmin-coordinator-deployer"></a>

### Coordinator / Deployer 설치

패키지 배포가 완료되면 Coordinator를 먼저 설치·시작한 후 Deployer를 등록합니다.

#### Coordinator 설치

##### 1. machbase.conf 설정

`$MACHBASE_COORDINATOR_HOME/conf/machbase.conf`를 편집합니다.

```bash
vi $MACHBASE_COORDINATOR_HOME/conf/machbase.conf
```

주요 설정:

```
CLUSTER_LINK_HOST    = 192.168.1.10   # 이 노드의 IP
CLUSTER_LINK_PORT_NO = 5101
HTTP_ADMIN_PORT      = 5102
```

##### 2. 메타 데이터베이스 생성 및 서비스 시작

```bash
machcoordinatoradmin -c
machcoordinatoradmin -u
```

##### 3. 자기 자신을 Coordinator 노드로 등록

```bash
machcoordinatoradmin --add-node="192.168.1.10:5101" \
  --node-type=coordinator \
  --http-port-no=5102
```

##### 4. 등록 확인

```bash
machcoordinatoradmin --cluster-status
```

#### Secondary Coordinator 설치 (선택)

고가용성을 위해 Secondary Coordinator를 추가합니다.

Secondary 노드에서 패키지를 배포하고 `machbase.conf`를 설정한 후, **Primary Coordinator에서** 먼저 노드를 등록합니다.

```bash
# Primary Coordinator에서 먼저 등록
machcoordinatoradmin --add-node="192.168.1.20:5101" \
  --node-type=coordinator \
  --http-port-no=5102

# 그 다음 Secondary 노드에서 시작 (--primary 옵션으로 Primary 지정)
machcoordinatoradmin -u --primary=192.168.1.10:5101
```

Secondary를 시작하기 전에 반드시 Primary에서 노드 등록을 완료해야 합니다.

#### Deployer 설치

##### 1. machbase.conf 설정

```
CLUSTER_LINK_HOST    = 192.168.1.10   # Deployer 노드 IP
CLUSTER_LINK_PORT_NO = 5201
HTTP_ADMIN_PORT      = 5202
```

##### 2. 시작

```bash
machdeployeradmin -c
machdeployeradmin -u
```

##### 3. Coordinator에 Deployer 노드 등록

```bash
machcoordinatoradmin --add-node="192.168.1.10:5201" \
  --node-type=deployer \
  --http-port-no=5202
```

---

<a id="manual-machcoordinatoradmin-lookup-broker-warehouse"></a>

### Lookup / Broker / Warehouse 설치

Coordinator와 Deployer가 준비된 후 Lookup, Broker, Warehouse 노드를 Coordinator에 등록하고 시작합니다. Broker와 Warehouse를 등록하기 전에 경량 패키지를 Coordinator에 `--add-package`로 등록해야 합니다.

#### Broker 설치

##### 1. 등록 파라미터 확인

Broker 설정 파일은 `--add-node` 실행 때 생성되어 Deployer를 통해 대상 노드에 배포됩니다. 등록 전에 cluster link 포트, 서비스 포트, HTTP 포트를 확정합니다.

```
CLUSTER_LINK_HOST    = 192.168.1.11   # Broker 노드 IP
CLUSTER_LINK_PORT_NO = 5401
PORT_NO              = 5656           # 클라이언트 접속 포트
```

##### 2. Coordinator에 노드 등록

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

##### 3. 노드 시작

Coordinator에서 해당 노드를 시작합니다.

```bash
machcoordinatoradmin --startup-node="192.168.1.11:5401"
```

#### Warehouse 설치

Warehouse 노드는 그룹 단위로 구성합니다. 같은 그룹의 노드끼리 데이터를 복제합니다.

##### 1. 등록 파라미터 확인

Warehouse 설정 파일은 `--add-node` 실행 때 생성되어 Deployer를 통해 대상 노드에 배포됩니다. 등록 전에 cluster link 포트, 서비스 포트, replication manager 주소를 확정합니다.

```
CLUSTER_LINK_HOST    = 192.168.1.13
CLUSTER_LINK_PORT_NO = 5501
PORT_NO              = 5500
```

##### 2. 노드 등록

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

별도 `--add-group` 명령은 사용하지 않습니다. Warehouse 그룹 이름은 각 Warehouse 노드를 등록할 때 `--group`으로 지정합니다.

Tag update가 반영된 빌드에서 Warehouse HTTP 포트를 별도로 지정해야 하는 경우에는 Warehouse `--add-node`에 `--http-port-no`를 추가합니다. `main` 또는 RDB 구현 브랜치 기반 빌드에서는 Warehouse 설정 생성 시 `HTTP_PORT_NO`를 기록하지 않습니다.

##### 3. 노드 시작

```bash
machcoordinatoradmin --startup-node="192.168.1.13:5501"
machcoordinatoradmin --startup-node="192.168.1.14:5501"
```

#### Lookup 노드 (선택)

Lookup 노드는 참조 데이터를 위한 전용 노드입니다. 구성할 때는 `--lookup-type`을 함께 지정합니다.

```bash
machcoordinatoradmin --add-node="192.168.1.30:5301" \
  --node-type=lookup \
  --lookup-type=master \
  --deployer="192.168.1.10:5201" \
  --home-path="/home/machbase/lookup"
```

#### 전체 상태 확인

모든 노드 등록 후 상태를 확인합니다.

```bash
machcoordinatoradmin --cluster-status
```

Coordinator, Lookup, Broker, Warehouse가 각 역할에 맞는 정상 상태로 표시되면 클러스터가 정상 구동 중입니다. Coordinator는 `primary`, Broker는 `leader`, Warehouse는 `normal`, `sync-active`, `sync-standby` 등으로 표시됩니다.

---

<a id="manual-machcoordinatoradmin-status-check-node-state"></a>

### 노드 상태 확인

클러스터 구성 완료 후 모든 노드의 상태를 확인합니다.

#### 전체 클러스터 상태 조회

```bash
machcoordinatoradmin --cluster-status
```

정상 클러스터 출력 예시:

```
+-------------+-------------------+-------------------+-------------------+--------------+
|  Node Type  |     Node Name     |    Group Name     |    Group State    |     State    |
+-------------+-------------------+-------------------+-------------------+--------------+
| coordinator | 192.168.1.10:5101 | Coordinator       | normal            | primary      |
| broker      | 192.168.1.11:5401 | Broker            | normal            | normal       |
| warehouse   | 192.168.1.13:5501 | group1            | normal            | normal       |
| warehouse   | 192.168.1.14:5501 | group1            | normal            | normal       |
+-------------+-------------------+-------------------+-------------------+--------------+
```

Deployer 상태까지 함께 보려면 `--cluster-status --verbose`를 사용합니다. Desired/Actual state, RP state, 디스크 사용률, ping 값은 `--cluster-status-full`에서 확인합니다.

#### 개별 노드 관리 명령

| 명령 | 설명 |
|------|------|
| `machcoordinatoradmin --startup-node=IP:PORT` | Lookup/Broker/Warehouse 노드 시작 |
| `machcoordinatoradmin --shutdown-node=IP:PORT` | Lookup/Broker/Warehouse 노드 종료 |
| `machcoordinatoradmin --cluster-status` | 전체 상태 조회 |
| `machcoordinatoradmin --configuration` | Coordinator 설정 조회 |

Coordinator와 Deployer 프로세스는 각 노드에서 `machcoordinatoradmin -u/-s`, `machdeployeradmin -u/-s` 같은 서비스 명령으로 시작하거나 종료합니다.

#### 상태값 설명

| 값 | 의미 |
|----|------|
| `normal` | 정상 동작 |
| `primary` | Coordinator Primary |
| `sync-active` | 복제 송신 역할 |
| `sync-standby` | 복제 수신 역할 |
| `inactive` | 비활성 상태 |
| `scrapped` | 장애 감지, 복구 필요 |
| `ddl-incompl` | DDL 처리 미완료 상태 |
| `ddl-recov` | DDL 복구 진행 상태 |
| `**unknown**` | 통신 불가, 노드 다운 의심 |

`leader`처럼 Broker 역할을 나타내는 값은 상태 출력의 Desired/Actual state나 그룹 상태 영역에 표시될 수 있습니다.

#### 클라이언트 접속 테스트

Broker 포트로 접속하여 쿼리를 실행합니다.

```bash
machsql -s 192.168.1.11 -u SYS -p MANAGER
Mach> SELECT * FROM V$NODE_STATUS;
```

`V$NODE_STATUS` 뷰는 접속한 노드의 타입, 상태, 호스트, Coordinator 연결 정보 등을 반환합니다. 등록된 전체 노드 목록은 `machcoordinatoradmin --cluster-status` 출력에서 확인합니다.
