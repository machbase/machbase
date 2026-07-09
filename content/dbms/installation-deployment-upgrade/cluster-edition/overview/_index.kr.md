---
type: docs
title: '3.3.1 Cluster Edition 구성 개요'
weight: 10
toc: true
---

Cluster Edition은 역할이 분리된 Coordinator, Deployer, Lookup, Broker, Warehouse 노드로 구성됩니다.
각 노드의 역할과 상호 관계를 이해한 후 배포 계획을 세우십시오.

## 노드 역할 상세

### Coordinator

클러스터 전체의 메타 정보를 관리합니다. 노드 등록, 상태 감시, 장애 감지를 담당합니다. Primary/Secondary 이중화를 권장합니다. Coordinator가 다운되어도 이미 실행 중인 Broker·Warehouse의 INSERT·SELECT는 중단되지 않습니다.

- 설정 파일: `$MACHBASE_COORDINATOR_HOME/conf/machbase.conf`
- 관리 도구: `machcoordinatoradmin`
- 주요 포트: `CLUSTER_LINK_PORT_NO`, `HTTP_ADMIN_PORT`

설정하지 않았을 때의 기본값은 `CLUSTER_LINK_PORT_NO=3868`, `HTTP_ADMIN_PORT=5779`입니다. 이 장의
예제에서는 운영 중 포트 충돌을 피하기 위해 Coordinator link/admin 포트로 `5101`/`5102`를
명시합니다.

### Deployer

Coordinator의 지시에 따라 각 노드에 패키지를 배포하고 초기화를 중계합니다. 각 노드 호스트에 하나씩 배치하거나, 별도 배포 서버로 운영할 수 있습니다.

- 관리 도구: `machdeployeradmin`

### Lookup

참조 데이터와 조회 처리를 위한 노드입니다. 구성에 따라 master, monitor, slave 역할을 지정합니다.

### Broker

클라이언트의 SQL 요청을 받아 파싱하고 적절한 Warehouse로 분배합니다. 애플리케이션은 Broker 주소로만 연결하며, Warehouse와 직접 통신하지 않습니다. Broker도 이중화를 권장합니다.

- 클라이언트 접속 포트: 기본 5656

### Warehouse

실제 데이터를 저장하고 쿼리를 실행합니다. 같은 그룹의 Warehouse끼리 데이터를 복제하여 고가용성을 제공합니다. 그룹당 2개 이상을 권장합니다.

## 구성 예시

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

## 에디션 비교

Standard Edition과의 상세 비교는 [에디션 차이점](/dbms/core-concepts/concepts-edition/differences-standard-edition-cluster/)을 참고하십시오.

---

**다음 읽을 내용**
- [Cluster Edition 설치 환경 준비](/kr/dbms/installation-deployment-upgrade/cluster-edition/preparation-environment-cluster-edition/)
