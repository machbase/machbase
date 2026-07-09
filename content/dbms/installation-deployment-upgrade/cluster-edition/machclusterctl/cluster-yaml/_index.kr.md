---
type: docs
title: 'cluster.yaml 작성'
weight: 10
toc: true
---

`cluster.yaml`은 `machclusterctl`이 클러스터를 배포하는 데 사용하는 선언적 설정 파일입니다.
클러스터 이름, 호스트 별칭, 패키지 입력 경로, 노드별 포트와 홈 경로를 정의합니다.

## 파일 구조 예시

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

    - alias: broker-2
      host: node2
      deployer: deployer-2

  warehouse_groups:
    - name: group1
      nodes:
        - alias: warehouse-group1-1
          host: node2
          deployer: deployer-2

        - alias: warehouse-group1-2
          host: node3
          deployer: deployer-3
```

## 주요 항목 설명

| 항목 | 설명 |
|------|------|
| `version` | YAML 스키마 버전입니다. 현재 `"1"`을 사용합니다. |
| `cluster.name` | 클러스터 이름입니다. `destroy` 확인 등에서 사용됩니다. |
| `cluster.hosts` | 노드에서 참조할 호스트 별칭과 SSH 접속 주소입니다. `address`는 `user@host` 형식을 사용합니다. |
| `cluster.package.name` | Coordinator에 등록할 패키지 이름입니다. |
| `cluster.package.origin_path` | `install`, `apply`, `upgrade` 실행 때 입력으로 사용할 패키지 archive 경로입니다. |
| `cluster.package.registered_path` | `export`가 기록하는 Coordinator package repository의 관찰 경로입니다. 실행 입력으로 사용하지 않습니다. |
| `cluster.ssh.key_file` | 대상 서버 접속에 사용할 private key 경로입니다. 비밀번호 필드는 사용하지 않습니다. |
| `cluster.defaults` | 노드 타입별 `home_path`, `cluster_link_port`, `service_port` 기본값입니다. Coordinator와 Deployer는 `http_admin_port`, Broker는 `http_port_no`를 사용합니다. |
| `cluster.coordinators` | Coordinator 노드 목록입니다. `role`은 `primary` 또는 `secondary`를 사용합니다. |
| `cluster.deployers` | Deployer 노드 목록입니다. |
| `cluster.lookup` | Lookup 노드 목록입니다. `type`은 `master`, `monitor`, `slave`를 사용합니다. |
| `cluster.brokers` | Broker 노드 목록입니다. 클라이언트 SQL 접속 포트는 `service_port`입니다. |
| `cluster.warehouse_groups` | Warehouse 그룹과 그룹별 노드 목록입니다. |

## 권장 구성

- Coordinator: 2개 (Primary + Secondary HA)
- Deployer: 1개 이상
- Lookup: master 1개, monitor 1개 이상
- Broker: 2개 이상 (부하 분산)
- Warehouse 그룹: 그룹당 2개 이상 (복제를 통한 고가용성)

같은 서버에 같은 타입의 노드를 2개 이상 배치할 때는 두 번째 노드부터 `home_path`와 포트를
명시적으로 지정하여 충돌을 피합니다.

기존 `cluster.package.path`는 하위 호환 입력으로 사용할 수 있지만, 새로 작성하는 YAML에서는
`origin_path`를 사용합니다.

작성이 완료되면 유효성을 검사합니다.

---

**다음 읽을 내용**
- [YAML 검증](/dbms/installation-deployment-upgrade/cluster-edition/machclusterctl/validation-yaml/)
