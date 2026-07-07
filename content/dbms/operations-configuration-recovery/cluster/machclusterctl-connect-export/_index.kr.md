---
type: docs
title: 'machclusterctl connect/export'
weight: 20
---

`machclusterctl`은 클러스터 전체 기동·종료 외에 클러스터 접속과 설정 내보내기 기능을 제공합니다.

## 클러스터 접속

```bash
machclusterctl connect
```

Broker를 통해 machsql 클라이언트로 클러스터에 접속합니다. Broker 노드의 접속 정보(호스트·포트·사용자)를 자동으로 사용하므로 별도로 접속 정보를 입력하지 않아도 됩니다.

접속 후 일반 machsql과 동일하게 SQL을 실행할 수 있습니다.

```sql
Mach> SELECT COUNT(*) FROM my_table;
Mach> SELECT * FROM v$cluster_node_status;
Mach> EXIT
```

Broker가 여러 개인 경우 설정 파일에 등록된 첫 번째 활성 Broker에 접속합니다. 특정 Broker로 직접 접속하려면 machsql을 직접 사용합니다.

```bash
# 특정 Broker로 직접 접속
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
cluster:
  coordinator:
    - host: 192.168.0.32
      port: 5101
  deployer:
    - host: 192.168.0.32
      port: 5201
  broker:
    - host: 192.168.0.32
      port: 5301
      service-port: 5757
  warehouse:
    - group: Group1
      nodes:
        - host: 192.168.0.32
          port: 5401
```

> 내보낸 YAML 파일을 그대로 import하는 명령은 별도로 없습니다. 클러스터 재구성 시에는 `machcoordinatoradmin`의 `--add-node` 명령을 사용합니다.
