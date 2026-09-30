---
title: 'machclusterctl YAML 작성 가이드'
type: docs
weight: 80
---

이 문서는 `machclusterctl`에서 사용하는 `cluster.yaml`의 작성 방법을 설명합니다. 명령 실행 절차는 [machclusterctl 사용자 가이드](../machclusterctl-user-guide/)를 참고하십시오.

YAML에는 클러스터의 목표 상태를 작성합니다. `machclusterctl`은 YAML을 읽은 뒤 `cluster.defaults`, `cluster.hosts`, 환경 변수 치환을 적용해 최종 설정값을 만듭니다.

## 1. 최소 설정

반복되는 값은 `cluster.defaults`와 `cluster.hosts`에 모으고, 각 노드에는 `alias`, `host`, 역할 필드만 남기는 방식입니다. 서로 다른 서버에 같은 타입의 노드를 1개씩 배치하는 일반적인 구성에서는 포트를 노드마다 반복해서 작성할 필요가 없습니다. 같은 host에 같은 타입의 노드를 2개 이상 올릴 때도 첫 번째 노드는 타입별 `defaults`를 그대로 사용하고, 두 번째 노드부터 충돌하는 포트와 보통 `home_path`만 override하면 됩니다.

다음 예시는 서버 2대에 coordinator 2개, deployer 2개, lookup master/monitor, broker 1개, warehouse group 1개를 구성합니다.

```yaml
version: "1"

cluster:
  name: mc-minimal

  hosts:
    node1:
      address: machbase@192.168.0.11
    node2:
      address: machbase@192.168.0.12

  package:
    name: machbase
    path: /machbase/packages/machbase-ent-release-lightweight.tgz

  ssh:
    key_file: /home/machbase/.ssh/id_rsa

  defaults:
    coordinator:
      home_path: /machbase/coordinator
      cluster_link_port: 5101
      http_admin_port: 5102
    deployer:
      home_path: /machbase/deployer
      cluster_link_port: 5201
      http_admin_port: 5202
    lookup:
      home_path: /machbase/lookup
      cluster_link_port: 5301
      http_admin_port: 5302
    broker:
      home_path: /machbase/broker
      cluster_link_port: 5401
      http_admin_port: 5402
      service_port: 5656
    warehouse:
      home_path: /machbase/warehouse
      cluster_link_port: 5501
      http_admin_port: 5502
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

  warehouse_groups:
    - name: group1
      nodes:
        - alias: warehouse-group1-1
          host: node1
          deployer: deployer-1

        - alias: warehouse-group1-2
          host: node2
          deployer: deployer-2
```

해석 결과:

- `node1`, `node2`는 `cluster.hosts`에 정의된 실제 `machbase@IP`로 변환됩니다.
- SSH user는 `address: machbase@...`에서 얻고, SSH key는 `cluster.ssh.key_file`을 공통으로 사용합니다.
- `home_path`, `cluster_link_port`, `http_admin_port`, `service_port`는 노드 타입별 `defaults`에서 상속됩니다.
- 서로 다른 host에서는 같은 default port를 사용해도 충돌하지 않습니다.
- 같은 host에 같은 타입의 노드를 2개 이상 배치하면 첫 번째 노드는 default port를 그대로 사용하고, 두 번째 노드부터 포트와 보통 `home_path`를 명시적으로 override합니다.

같은 host에 warehouse를 2개 올리는 예:

```yaml
defaults:
  warehouse:
    home_path: /machbase/warehouse
    cluster_link_port: 5501
    http_admin_port: 5502
    service_port: 5500

warehouse_groups:
  - name: group1
    nodes:
      - alias: warehouse-group1-1
        host: node1
        deployer: deployer-1

  - name: group2
    nodes:
      - alias: warehouse-group2-1
        host: node1
        deployer: deployer-1
        home_path: /machbase/warehouse-group2
        cluster_link_port: 5511
        http_admin_port: 5512
        service_port: 5510
```

## 2. 환경 변수, 공통 설정, 노드별 설정 함께 사용하기

환경마다 달라지는 값은 `${VAR}` 또는 `${VAR:-default}`로 작성할 수 있습니다. 공통값은 `defaults`에 두고, 특정 노드에서만 포트, 홈 경로, `dbs_path`를 override합니다.

사용할 수 있는 환경 변수 문법:

- `${VAR}`: 환경 변수가 없으면 오류가 발생합니다.
- `${VAR:-default}`: 환경 변수가 없거나 빈 문자열이면 `default`를 사용합니다.

환경 변수 예시:

```bash
export MC_PACKAGE_PATH=/machbase/packages/machbase-ent-release-lightweight.tgz
export MC_SSH_KEY=/home/machbase/.ssh/id_rsa
export MC_NODE1=machbase@192.168.0.11
export MC_NODE2=machbase@192.168.0.12
export MC_NODE3=machbase@192.168.0.13
export MC_HOME_BASE=/machbase
```

YAML 예시:

```yaml
version: "1"

cluster:
  name: "${MC_CLUSTER_NAME:-mc-mixed}"

  hosts:
    node1:
      address: "${MC_NODE1}"
    node2:
      address: "${MC_NODE2}"
    node3:
      address: "${MC_NODE3:-machbase@192.168.0.13}"

  package:
    name: "${MC_PACKAGE_NAME:-machbase}"
    path: "${MC_PACKAGE_PATH}"

  ssh:
    key_file: "${MC_SSH_KEY}"

  defaults:
    coordinator:
      home_path: "${MC_HOME_BASE:-/machbase}/coordinator"
      cluster_link_port: "${MC_COORD_PORT:-5101}"
      http_admin_port: "${MC_COORD_HTTP_PORT:-5102}"
    deployer:
      home_path: "${MC_HOME_BASE:-/machbase}/deployer"
      cluster_link_port: "${MC_DEPLOYER_PORT:-5201}"
      http_admin_port: "${MC_DEPLOYER_HTTP_PORT:-5202}"
    lookup:
      home_path: "${MC_HOME_BASE:-/machbase}/lookup"
      cluster_link_port: "${MC_LOOKUP_PORT:-5301}"
      http_admin_port: "${MC_LOOKUP_HTTP_PORT:-5302}"
    broker:
      home_path: "${MC_HOME_BASE:-/machbase}/broker"
      cluster_link_port: "${MC_BROKER_PORT:-5401}"
      http_admin_port: "${MC_BROKER_HTTP_PORT:-5402}"
      service_port: "${MC_BROKER_SERVICE_PORT:-5656}"
    warehouse:
      home_path: "${MC_HOME_BASE:-/machbase}/warehouse"
      cluster_link_port: "${MC_WAREHOUSE_PORT:-5501}"
      http_admin_port: "${MC_WAREHOUSE_HTTP_PORT:-5502}"
      service_port: "${MC_WAREHOUSE_SERVICE_PORT:-5500}"

  coordinators:
    - alias: coord-primary-1
      host: node1
      role: primary

    - alias: coord-secondary-1
      host: node2
      role: secondary
      # Only the coordinator on node2 uses a separate home path.
      home_path: "${MC_HOME_BASE:-/machbase}/coordinator-secondary"

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

    - alias: lookup-slave-1
      host: node3
      deployer: deployer-3
      type: slave
      # Override only the slave ports in case another lookup node is added on node3.
      cluster_link_port: "${MC_LOOKUP_SLAVE_PORT:-5311}"
      http_admin_port: "${MC_LOOKUP_SLAVE_HTTP_PORT:-5312}"

  brokers:
    - alias: broker-1
      host: node1
      deployer: deployer-1

    - alias: broker-2
      host: node2
      deployer: deployer-2
      # Override only broker-2's service port and dbs path.
      service_port: "${MC_BROKER2_SERVICE_PORT:-5666}"
      dbs_path: "${MC_HOME_BASE:-/machbase}/dbs/broker-2"

  warehouse_groups:
    - name: group1
      nodes:
        - alias: warehouse-group1-1
          host: node1
          deployer: deployer-1

        - alias: warehouse-group1-2
          host: node2
          deployer: deployer-2
          dbs_path: "${MC_HOME_BASE:-/machbase}/dbs/warehouse-group1-2"

    - name: group2
      nodes:
        - alias: warehouse-group2-1
          host: node2
          deployer: deployer-2
          # Because this is the second warehouse on node2, override ports and home_path.
          home_path: "${MC_HOME_BASE:-/machbase}/warehouse-group2"
          cluster_link_port: "${MC_WAREHOUSE_G2_PORT:-5511}"
          http_admin_port: "${MC_WAREHOUSE_G2_HTTP_PORT:-5512}"
          service_port: "${MC_WAREHOUSE_G2_SERVICE_PORT:-5510}"

        - alias: warehouse-group2-2
          host: node3
          deployer: deployer-3
```

운영 기준:

- 환경 변수 치환은 YAML을 decode하기 전에 수행됩니다. 숫자 필드에 들어가는 값은 치환 후 정수로 변환할 수 있어야 합니다.
- `cluster.hosts`의 `address`에 `user@host`를 작성하면 SSH user를 따로 반복해서 작성하지 않아도 됩니다.
- `cluster.ssh.key_file`은 공통 key를 한 번만 지정하는 용도입니다. host마다 key가 다르면 `cluster.hosts.<alias>.ssh.key_file`로 override합니다.
- `deployer`는 lookup/broker/warehouse가 사용할 deployer alias입니다. 같은 host에 deployer가 하나뿐이면 생략할 수 있지만, 명시하는 편이 안전합니다.
- `dbs_path`는 broker/warehouse 노드에만 사용할 수 있습니다. defaults에는 둘 수 없습니다.

## 3. 모든 설정 가능 필드

### 3-1. 최상위 구조

| YAML path | 타입 | 필수 | 설명 |
|-----------|------|------|------|
| `version` | string | 예 | YAML 스키마 버전입니다. 현재는 `"1"`을 사용합니다. |
| `cluster` | object | 예 | 클러스터 전체 정의입니다. |
| `cluster.name` | string | 예 | 클러스터 이름입니다. `validate`, `install`, `apply`, `destroy`의 확인 메시지와, 사람이 클러스터를 구분하는 용도로 사용됩니다. |

### 3-2. `cluster.hosts`

`cluster.hosts`는 IP/hostname을 한곳에 모아 두고, 노드 설정에서는 host alias만 사용하기 위한 섹션입니다.

| YAML path | 타입 | 필수 | fallback | 설명 |
|-----------|------|------|----------|------|
| `cluster.hosts` | map | 아니요 | 없음 | host alias 정의 목록입니다. |
| `cluster.hosts.<alias>.address` | string | host alias 사용 시 예 | 없음 | 실제 IP/DNS 또는 `user@ip`, `user@hostname` endpoint입니다. |
| `cluster.hosts.<alias>.ssh` | object | 아니요 | `cluster.ssh` | 해당 host alias를 사용하는 노드에 적용할 SSH override입니다. |
| `cluster.hosts.<alias>.ssh.user` | string | 아니요 | `address`의 user 또는 공통 SSH user | 호환성 유지나 예외 상황을 위한 SSH user입니다. 새 YAML에서는 `address: user@host`를 권장합니다. |
| `cluster.hosts.<alias>.ssh.port` | int | 아니요 | `cluster.ssh.port` 또는 22 | SSH 접속 포트입니다. |
| `cluster.hosts.<alias>.ssh.key_file` | string | 아니요 | `cluster.ssh.key_file` | 해당 host 전용 SSH private key 경로입니다. |

`host` 값이 `cluster.hosts`에 없는 단순 문자열이고 IP/DNS처럼 보이지 않으면 `undefined host alias` 오류가 발생합니다. `localhost`, IP, `.` 또는 `:`가 포함된 hostname은 host 값으로 직접 처리됩니다.

### 3-3. `cluster.defaults`

`defaults`는 노드 타입별로 반복되는 값을 줄이기 위한 `machclusterctl` 기능입니다.

| YAML path | 타입 | 필수 | 설명 |
|-----------|------|------|------|
| `cluster.defaults.common.ssh_user` | string | 아니요 | 기존 버전과의 호환성을 위한 공통 SSH user입니다. 새 YAML에서는 `user@host` 사용을 권장합니다. |
| `cluster.defaults.coordinator` | object | 아니요 | coordinator 기본값입니다. |
| `cluster.defaults.deployer` | object | 아니요 | deployer 기본값입니다. |
| `cluster.defaults.lookup` | object | 아니요 | lookup 기본값입니다. |
| `cluster.defaults.broker` | object | 아니요 | broker 기본값입니다. |
| `cluster.defaults.warehouse` | object | 아니요 | warehouse 기본값입니다. |

각 노드 타입의 defaults에서 사용할 수 있는 필드:

| 필드 | 적용 대상 | 설명 |
|------|-----------|------|
| `home_path` | 모든 노드 타입 | 노드 홈 경로입니다. 절대 경로만 허용합니다. |
| `cluster_link_port` | 모든 노드 타입 | cluster link 통신 포트입니다. |
| `http_admin_port` | 모든 노드 타입 | HTTP admin 포트입니다. coordinator/deployer에서는 필수입니다. lookup/broker/warehouse에서도 설정할 수 있으며, 기본값이나 노드별 값을 사용하는 것을 권장합니다. |
| `service_port` | broker, warehouse | broker의 client 접속 포트 또는 warehouse의 service 포트입니다. |

노드에 값이 있으면 노드 값이 우선하고, 없으면 해당 노드 타입의 `defaults`를 사용합니다.

### 3-4. `cluster.package`

| YAML path | 타입 | 필수 | 설명 |
|-----------|------|------|------|
| `cluster.package.name` | string | 예 | coordinator에 등록할 package 이름입니다. 업그레이드할 때는 새 package 이름을 권장합니다. |
| `cluster.package.path` | string | 조건부 | 운영자가 직접 작성하는 입력 archive 경로입니다. `origin_path`가 없으면 이 값을 사용합니다. |
| `cluster.package.origin_path` | string | 조건부 | 입력 archive 경로입니다. `path`와 함께 있으면 이 값이 우선합니다. export YAML은 이 필드를 출력합니다. |
| `cluster.package.registered_path` | string | 아니요 | coordinator가 package 저장소에 보관하고 있는 경로입니다. export YAML에 기록되는 current metadata 관찰값이며, 설치/업그레이드 입력으로 사용하지 않습니다. |

`path`와 `origin_path` 중 하나는 반드시 있어야 합니다. `install`, `upgrade`, 신규 노드 `apply`에서는 이 archive가 실제로 존재해야 하며, archive 안에 Machbase 실행 binary와 `bin/`, `lib/`, `conf/` 구성 요소가 있어야 합니다.

package 변경 여부는 실행 중인 broker/warehouse의 current package name과 YAML의 `cluster.package.name`을 비교해 판단합니다. 같은 `cluster.package.name`을 유지한 채 archive 내용이나 `cluster.package.path`/`cluster.package.origin_path`만 바꾸면 기존 broker/warehouse는 업그레이드 대상으로 감지되지 않습니다. 내용이 다른 archive를 적용하려면 새 `cluster.package.name`과 고유한 archive file name을 함께 사용합니다.

#### package 입력 경로와 coordinator package 저장소

운영자가 작성하는 desired YAML의 `cluster.package.path` 또는 `cluster.package.origin_path`에는 원칙적으로 coordinator home 밖에 보관한 **원본 archive 경로**를 작성합니다.

권장 예:

```yaml
cluster:
  package:
    name: machbase-v2
    path: /machbase/packages/machbase-v2.tgz
```

비권장 예:

```yaml
cluster:
  package:
    name: machbase-v2
    path: /machbase/coordinator/package/machbase-v2.tgz
```

coordinator의 `package/` 디렉터리는 `machcoordinatoradmin --add-package`가 package를 등록하면서 내부적으로 보관하는 저장소입니다. 이 경로의 파일을 다시 새 package 등록 source로 사용하면 다음과 같은 상황이 생길 수 있습니다.

- 같은 `package.name`과 같은 file name이 이미 등록되어 있으면 멱등 처리를 위해 no-op처럼 넘어갈 수 있습니다.
- 다른 `package.name`으로 같은 file name을 등록하려고 하면 coordinator가 file name 중복으로 거절할 수 있습니다.
- `destroy` 후에는 coordinator home과 함께 package 저장소가 삭제될 수 있습니다. export YAML의 package 경로만 믿고 재설치하면 archive가 없을 수 있습니다.

따라서 업그레이드용 새 archive는 다음 규칙으로 관리합니다.

- archive 내용이 바뀌면 `cluster.package.name`을 새 값으로 변경합니다.
- archive file name도 새 package 이름에 맞춰 고유하게 지정합니다. 예: `machbase-v2.tgz`, `machbase-v3.tgz`
- `cluster.package.path` 또는 `cluster.package.origin_path`에는 `/machbase/packages/...`처럼 coordinator home 밖에 보존할 수 있는 원본 경로를 지정합니다.
- `machclusterctl export`가 출력한 `registered_path`를 재설치나 새 업그레이드의 입력으로 사용하지 않습니다. 필요하면 `origin_path`를 원본 archive 경로로 수정하거나 `path`를 새로 작성합니다.

YAML에 정의되지 않은 필드가 있으면 로드 단계에서 오류가 발생합니다. 오타가 있는 필드는 조용히 무시되지 않으므로, 오류 메시지에 표시된 필드 이름을 확인해 수정합니다.

### 3-5. SSH 설정

SSH 설정은 `install`, 신규 노드 추가, `destroy`, `upgrade --full-stop`처럼 원격 서버에 직접 접근하는 명령에서 사용됩니다.

적용 우선순위(뒤에 있는 설정이 우선합니다):

```text
cluster.defaults.common.ssh_user
  -> cluster.ssh
  -> user from user@host or hosts.<alias>.address
  -> cluster.hosts.<alias>.ssh
  -> node.ssh
```

| YAML path | 타입 | 필수 | 설명 |
|-----------|------|------|------|
| `cluster.ssh.user` | string | 조건부 | 공통 SSH user입니다. 새 YAML에서는 `address: user@host`를 권장합니다. |
| `cluster.ssh.port` | int | 아니요 | 공통 SSH port입니다. 생략하면 SSH 기본 port인 22를 사용합니다. |
| `cluster.ssh.key_file` | string | 원격 작업 시 예 | 공통 SSH private key 경로입니다. |
| `node.ssh.user` | string | 아니요 | 특정 노드 전용 SSH user override입니다. |
| `node.ssh.port` | int | 아니요 | 특정 노드 전용 SSH port override입니다. |
| `node.ssh.key_file` | string | 아니요 | 특정 노드 전용 SSH key override입니다. |

YAML schema에는 SSH password 필드가 없습니다. `ssh.password`를 작성하면 설정 로드 단계에서 오류가 발생합니다.

### 3-6. 공통 노드 필드

다음 필드는 coordinator, deployer, lookup, broker, warehouse 노드에서 공통으로 사용됩니다. 단, `deployer`, `service_port`, `dbs_path`는 적용 대상이 제한됩니다.

| 필드 | 타입 | 필수 | fallback | 설명 |
|------|------|------|----------|------|
| `alias` | string | 아니요 | 자동 생성 | 노드의 논리 이름입니다. 운영 환경에서는 명시하는 것을 권장합니다. 명령의 `--node` 값에는 alias를 사용합니다. |
| `host` | string | 예 | 없음 | 실제 host, `user@host`, 또는 `cluster.hosts`에 정의한 host alias입니다. |
| `cluster_link_port` | int | defaults가 없으면 예 | `defaults.<type>.cluster_link_port` | 노드의 cluster link 포트입니다. 실제 identity는 `host:cluster_link_port`입니다. |
| `http_admin_port` | int | coordinator/deployer는 defaults가 없으면 예 | `defaults.<type>.http_admin_port` | HTTP admin 포트입니다. |
| `home_path` | string | defaults가 없으면 예 | `defaults.<type>.home_path` | 노드 홈 경로입니다. 절대 경로만 허용합니다. |
| `deployer` | string | lookup/broker/warehouse에서 권장 | 같은 host의 deployer | 사용할 deployer alias 또는 `host:cluster_link_port`입니다. 같은 host에 deployer가 여러 개 있으면 반드시 명시합니다. |
| `service_port` | int | broker/warehouse는 defaults가 없으면 예 | `defaults.broker.service_port`, `defaults.warehouse.service_port` | broker의 client 접속 포트 또는 warehouse의 service 포트입니다. |
| `dbs_path` | string | 아니요 | 없음 | broker/warehouse 데이터 경로입니다. 절대 경로 또는 `?`로 시작하는 경로만 허용합니다. |
| `dbs-path` | string | 아니요 | 없음 | `dbs_path`와 같은 호환용 alias입니다. broker/warehouse 노드에서만 허용합니다. |
| `ssh` | object | 아니요 | host/공통 SSH 설정 | 노드별 SSH override입니다. |

주의:

- `cluster_link_port`, `http_admin_port`, `service_port`와 노드가 내부적으로 사용하는 파생 포트가 같은 host 안에서 중복되면 validate 오류가 발생합니다.
- coordinator/deployer는 `cluster_link_port + 1`을 내부 `PORT_NO`로 사용합니다. 이 포트는 다른 노드의 포트와 겹치지 않아야 합니다.
- warehouse는 `service_port + 2`를 replication manager port로 사용합니다. 이 포트는 다른 노드의 `cluster_link_port`, `http_admin_port`, `service_port`와 겹치지 않아야 합니다.
- broker/warehouse가 아닌 곳에서 `dbs_path`를 사용하면 오류가 발생합니다.
- `dbs_path`는 defaults에 둘 수 없습니다.

### 3-7. coordinator

경로: `cluster.coordinators[]`

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `alias` | string | 아니요 | coordinator alias입니다. |
| `host` | string | 예 | host alias 또는 실제 host입니다. |
| `role` | string | 예 | `primary` 또는 `secondary`입니다. primary는 정확히 1개여야 합니다. |
| `cluster_link_port` | int | defaults가 없으면 예 | cluster link port입니다. |
| `http_admin_port` | int | defaults가 없으면 예 | HTTP admin port입니다. |
| `home_path` | string | defaults가 없으면 예 | coordinator home path입니다. |
| `ssh` | object | 아니요 | 노드별 SSH override입니다. |

### 3-8. deployer

경로: `cluster.deployers[]`

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `alias` | string | 아니요 | deployer alias입니다. |
| `host` | string | 예 | host alias 또는 실제 host입니다. |
| `cluster_link_port` | int | defaults가 없으면 예 | cluster link port입니다. |
| `http_admin_port` | int | defaults가 없으면 예 | HTTP admin port입니다. |
| `home_path` | string | defaults가 없으면 예 | deployer home path입니다. |
| `ssh` | object | 아니요 | 노드별 SSH override입니다. |

lookup/broker/warehouse의 `deployer` 필드는 이 deployer의 `alias` 또는 `host:cluster_link_port`를 참조합니다.

### 3-9. lookup

경로: `cluster.lookup[]`

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `alias` | string | 아니요 | lookup alias입니다. |
| `host` | string | 예 | host alias 또는 실제 host입니다. |
| `deployer` | string | 권장 | 설치에 사용할 deployer alias 또는 `host:cluster_link_port`입니다. |
| `type` | string | 예 | `master`, `monitor`, `slave` 중 하나입니다. master는 정확히 1개, monitor는 1개 이상 있어야 합니다. |
| `cluster_link_port` | int | defaults가 없으면 예 | cluster link port입니다. |
| `http_admin_port` | int | 아니요 | HTTP admin port입니다. |
| `home_path` | string | defaults가 없으면 예 | lookup home path입니다. |
| `ssh` | object | 아니요 | 노드별 SSH override입니다. |

### 3-10. broker

경로: `cluster.brokers[]`

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `alias` | string | 아니요 | broker alias입니다. |
| `host` | string | 예 | host alias 또는 실제 host입니다. |
| `deployer` | string | 권장 | 설치에 사용할 deployer alias 또는 `host:cluster_link_port`입니다. |
| `cluster_link_port` | int | defaults가 없으면 예 | cluster link port입니다. |
| `http_admin_port` | int | 아니요 | HTTP admin port입니다. |
| `service_port` | int | defaults가 없으면 예 | client/machsql 접속 port입니다. |
| `home_path` | string | defaults가 없으면 예 | broker home path입니다. |
| `dbs_path` 또는 `dbs-path` | string | 아니요 | broker의 `DBS_PATH` override입니다. |
| `ssh` | object | 아니요 | 노드별 SSH override입니다. |

### 3-11. warehouse group / warehouse node

경로:

- `cluster.warehouse_groups[]`
- `cluster.warehouse_groups[].nodes[]`

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `warehouse_groups[].name` | string | 예 | warehouse group 이름입니다. replication 단위입니다. |
| `warehouse_groups[].nodes[].alias` | string | 아니요 | warehouse alias입니다. |
| `warehouse_groups[].nodes[].host` | string | 예 | host alias 또는 실제 host입니다. |
| `warehouse_groups[].nodes[].deployer` | string | 권장 | 설치에 사용할 deployer alias 또는 `host:cluster_link_port`입니다. |
| `warehouse_groups[].nodes[].cluster_link_port` | int | defaults가 없으면 예 | cluster link port입니다. |
| `warehouse_groups[].nodes[].http_admin_port` | int | 아니요 | HTTP admin port입니다. |
| `warehouse_groups[].nodes[].service_port` | int | defaults가 없으면 예 | warehouse service port입니다. |
| `warehouse_groups[].nodes[].home_path` | string | defaults가 없으면 예 | warehouse home path입니다. |
| `warehouse_groups[].nodes[].dbs_path` 또는 `dbs-path` | string | 아니요 | warehouse의 `DBS_PATH` override입니다. |
| `warehouse_groups[].nodes[].ssh` | object | 아니요 | 노드별 SSH override입니다. |

warehouse를 추가할 때 `machclusterctl`은 해당 warehouse 자신의 `host:service_port+2`를 replication manager 주소로 계산합니다. 이 값은 peer 주소가 아니라 생성될 warehouse 설정의 `REPLICATION_MANAGER_PORT_NO`에 대응하는 값입니다. group의 첫 번째 warehouse처럼 `--no-replicate`가 필요한 경우에는 `--replication`을 함께 전달하지 않습니다.

### 3-12. export flat YAML과의 관계

`machclusterctl export`로 생성한 YAML은 운영 중인 클러스터의 최종 값을 보관하거나 diff로 비교하기 위한 출력입니다. `export`는 별도 옵션 없이 항상 flat YAML을 출력합니다.

flat YAML의 특징:

- `cluster.hosts`를 사용하지 않습니다.
- `cluster.defaults`를 사용하지 않습니다.
- 환경 변수 표현을 사용하지 않습니다.
- 모든 노드에 실제 `host`, `cluster_link_port`, `http_admin_port`, `service_port`, `home_path`, `dbs_path` 등을 가능한 한 명시합니다.
- diff를 안정적으로 비교할 수 있도록 출력 순서를 정렬합니다.

따라서 운영자가 직접 작성할 때는 1장이나 2장의 방식으로 간결하게 작성하고, 실제 running cluster 상태를 보관하거나 변경 이력을 비교할 때는 flat export를 사용하는 것을 권장합니다.

주의할 점:

- export YAML의 `cluster.package.origin_path`는 coordinator가 알고 있는 원본 archive 경로입니다. metadata에 원본 경로가 없으면 `registered_path` 값으로 채워질 수 있습니다.
- export YAML의 `cluster.package.registered_path`는 coordinator에 현재 등록되어 보관 중인 package 파일 경로입니다. 이 값은 원본 package archive의 보관 위치라기보다 current metadata snapshot에 가깝습니다.
- export는 package 목록 조회에 실패하거나 current package name에 대응하는 등록 package 경로를 absolute path로 찾지 못하면 실패합니다.
- export YAML은 같은 running cluster에 대한 `validate`, `apply --dry-run`, 구조 diff 용도로 사용할 수 있습니다.
- export YAML을 `destroy` 후 재설치하거나 새 package 업그레이드의 입력으로 사용할 때는 `cluster.package.origin_path` 또는 `cluster.package.path`를 coordinator home 밖의 원본 archive 경로로 수정합니다.
- 신규 노드 추가나 재설치에 필요한 SSH 설정은 coordinator metadata에서 복원할 수 없으므로 YAML에 다시 추가합니다.
