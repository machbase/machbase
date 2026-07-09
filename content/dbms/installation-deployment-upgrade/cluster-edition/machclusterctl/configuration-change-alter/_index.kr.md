---
type: docs
title: '구성 변경 적용'
weight: 40
toc: true
---

클러스터 구성(노드 추가, 포트 변경 등)을 변경하려면 `cluster.yaml`을 수정한 후 적용합니다.

## 구성 변경 절차

### 1. cluster.yaml 수정

필요한 변경사항을 `cluster.yaml`에 반영합니다. 예를 들어 새 Warehouse 그룹을 추가하려면 해당
항목을 추가합니다.

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

### 2. 유효성 검사

```bash
machclusterctl validate -f cluster.yaml
```

### 3. 실행 계획 확인

```bash
machclusterctl apply -f cluster.yaml --dry-run --verbose
```

### 4. 변경 적용

```bash
machclusterctl apply -f cluster.yaml --yes --verbose
machclusterctl status
```

`apply` 명령은 현재 클러스터 상태와 `cluster.yaml`의 차이를 계산하여 필요한 작업만 수행합니다.

## 노드 제거

`cluster.yaml`에서 해당 노드 항목을 삭제하고 `apply`를 실행합니다. 단, Warehouse 노드 제거 전에
해당 노드에 있는 데이터가 다른 노드에 충분히 복제되어 있는지 확인해야 합니다.

## 주의사항

- DDL 또는 DELETE가 실행 중인 상태에서 구성 변경을 수행하지 마십시오.
- 구성 변경 중에는 노드 추가·시작·종료·삭제 작업을 병행하지 마십시오.
- INSERT·APPEND·SELECT는 Coordinator 부재 시에도 계속 동작하지만, 구성 변경 작업은 Coordinator가 정상이어야 합니다.

---

**다음 읽을 내용**
- [상태 확인](/dbms/installation-deployment-upgrade/cluster-edition/machclusterctl/status-check-state/)
