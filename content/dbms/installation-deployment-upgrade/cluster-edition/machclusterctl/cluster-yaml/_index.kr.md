---
type: docs
title: 'cluster.yaml 작성'
weight: 10
---

`cluster.yaml`은 machclusterctl이 클러스터를 배포하는 데 사용하는 선언적 설정 파일입니다. 노드 구성, 패키지 경로, 포트 등을 정의합니다.

## 파일 구조 예시

```yaml
# cluster.yaml 예시
package:
  path: /home/machbase/packages/machbase-cluster-8.6.0.official-LINUX-X86-64-release.tgz

coordinator:
  - host: 192.168.1.10
    user: machbase
    home: /home/machbase/coordinator
    cluster_link_port: 5101
    http_admin_port: 5102

deployer:
  - host: 192.168.1.10
    user: machbase
    home: /home/machbase/deployer
    cluster_link_port: 5201
    http_admin_port: 5202

broker:
  - host: 192.168.1.11
    user: machbase
    home: /home/machbase/broker
    port: 5656
    cluster_link_port: 5301

  - host: 192.168.1.12
    user: machbase
    home: /home/machbase/broker
    port: 5656
    cluster_link_port: 5301

warehouse:
  - group: group1
    nodes:
      - host: 192.168.1.13
        user: machbase
        home: /home/machbase/warehouse
        port: 5656
        cluster_link_port: 5401

      - host: 192.168.1.14
        user: machbase
        home: /home/machbase/warehouse
        port: 5656
        cluster_link_port: 5401

  - group: group2
    nodes:
      - host: 192.168.1.15
        user: machbase
        home: /home/machbase/warehouse
        port: 5656
        cluster_link_port: 5401

      - host: 192.168.1.16
        user: machbase
        home: /home/machbase/warehouse
        port: 5656
        cluster_link_port: 5401
```

## 주요 항목 설명

| 항목 | 설명 |
|------|------|
| `package.path` | 배포할 Machbase 패키지 파일 경로 (배포 서버 기준) |
| `coordinator[].host` | Coordinator 노드 IP 또는 호스트명 |
| `coordinator[].home` | Coordinator 설치 경로 |
| `coordinator[].cluster_link_port` | 클러스터 노드 간 통신 포트 |
| `broker[].port` | 클라이언트 SQL 접속 포트 (기본 5656) |
| `warehouse[].group` | 복제 그룹 이름 (같은 그룹 내 노드끼리 데이터 복제) |

## 권장 구성

- Coordinator: 2개 (Primary + Secondary HA)
- Deployer: 1개 이상
- Broker: 2개 이상 (부하 분산)
- Warehouse 그룹: 그룹당 2개 이상 (복제를 통한 고가용성)

작성이 완료되면 유효성을 검사합니다.

---

**다음 읽을 내용**
- [YAML 검증](/dbms/installation-deployment-upgrade/cluster-edition/machclusterctl/validation-yaml/)
