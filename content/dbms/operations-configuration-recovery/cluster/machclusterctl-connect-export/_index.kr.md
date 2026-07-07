---
type: docs
title: 'machclusterctl connect/export'
weight: 20
---

`machclusterctl`은 클러스터 전체 기동·종료 외에 클러스터 접속과 설정 내보내기 기능을 제공합니다.

## 클러스터 접속

```bash
machclusterctl connect broker-1
```

지정한 Broker 또는 Warehouse alias를 통해 machsql 클라이언트로 클러스터에 접속합니다. alias는 클러스터 YAML 또는 Coordinator 메타에 등록된 이름을 사용합니다.

접속 후 일반 machsql과 동일하게 SQL을 실행할 수 있습니다.

```sql
Mach> SELECT COUNT(*) FROM my_table;
Mach> SELECT * FROM v$cluster_node_status;
Mach> EXIT
```

특정 Broker로 직접 접속하려면 해당 Broker alias를 지정하거나 machsql을 직접 사용합니다.

```bash
# 특정 Broker alias로 접속
machclusterctl connect broker-2

# 호스트와 포트를 직접 지정해 접속
machsql -s <broker_host> -P <broker_port> -u SYS -p MANAGER
```

## 클러스터 설정 내보내기

```bash
machclusterctl export -o cluster_config.yaml
```

현재 클러스터 구성 정보를 YAML 파일로 내보냅니다. 내보낸 파일에는 다음 정보가 포함됩니다.

- 각 노드의 호스트·포트 정보
- 노드 유형 (coordinator, deployer, broker, warehouse, lookup)
- 그룹 구성
- 패키지·홈 경로 정보

### 활용 예

- **문서화**: 현재 클러스터 구성을 기록으로 남길 때
- **재구성 참조**: 클러스터를 재구성하거나 유사한 환경을 구성할 때 참조 파일로 활용
- **백업**: 클러스터 메타 정보 변경 전 현재 상태를 저장

출력 파일 예:

```yaml
coordinators:
  - alias: coordinator-1
    host: 192.168.0.32
    port: 5101
deployers:
  - alias: deployer-1
    host: 192.168.0.32
    port: 5201
brokers:
  - alias: broker-1
    host: 192.168.0.32
    port: 5301
    service_port: 5757
warehouse_groups:
  - name: Group1
    warehouses:
      - alias: warehouse-group1-1
        host: 192.168.0.32
        port: 5401
```

> YAML 기반 구성 변경은 `machclusterctl apply -f <파일>` 흐름을 사용합니다. 개별 노드의 세부 운영이 필요한 경우에만 `machcoordinatoradmin`을 사용합니다.
