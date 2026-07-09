---
type: docs
title: '15.7 Cluster 설치와 확장'
weight: 120
---

Machbase Cluster Edition은 대용량 시계열 데이터를 여러 노드에 분산 저장·처리합니다. 이 시나리오는 Cluster를 처음 구성하고 운영 중에 Warehouse 노드를 추가해 수평 확장하는 절차를 설명합니다.

## Cluster 구성 요소

| 노드 유형 | 역할 | 최소 구성 |
|-----------|------|:---:|
| **Coordinator** | 클러스터 메타데이터·토폴로지 관리, 노드 상태 감시 | 1개 |
| **Deployer** | 패키지 배포, 노드 설치·업그레이드 자동화 | 호스트당 1개 |
| **Broker** | 클라이언트 연결 수신, 쿼리 라우팅 | 1개 이상 |
| **Warehouse** | 실제 데이터 저장·처리 | 1개 이상 |

최소 구성 예시 (개발용):
```
호스트 A: Coordinator + Deployer + Broker
호스트 B: Deployer + Warehouse
```

## 사전 준비

1. 모든 노드에 Machbase Cluster Edition 패키지 설치
2. 노드 간 SSH 키 인증 설정 (Deployer가 원격 명령 실행에 사용)
3. 방화벽: 기본 포트 허용 (Coordinator 5301, Broker 5656, Warehouse 5300+)
4. `$MACHBASE_HOME/conf/machbase.conf` 각 노드 역할에 맞게 설정

## 클러스터 초기화

`machclusterctl`로 클러스터 전체를 관리합니다.

```bash
# 설정 검증
machclusterctl validate -f cluster.yaml

# 클러스터 설치
machclusterctl install -f cluster.yaml --yes

# 클러스터 전체 시작
machclusterctl start -f cluster.yaml

# 전체 상태 확인
machclusterctl status
```

상태 출력 예시:
```
Cluster Status: RUNNING
  Coordinator  [host-a:5301]  RUNNING
  Broker       [host-a:5656]  RUNNING
  Warehouse[0] [host-b:5300]  RUNNING
```

## 클러스터 접속

Broker 주소로 접속합니다. Standard Edition과 동일한 연결 방식을 사용합니다.

```bash
# machsql로 접속
machsql -s host-a -P 5656 -u SYS -p MANAGER

# 클러스터 토폴로지 확인
SELECT host, nodetype, state, coord_host, coord_http_admin_port
  FROM v$node_status;
```

## Warehouse 노드 추가 (수평 확장)

데이터 처리량이 증가할 때 Warehouse 노드를 추가해 수평 확장합니다.

### 1단계: 새 노드 패키지 설치

새 호스트(host-c)에 Machbase 패키지를 설치하고 Deployer를 기동합니다.

```bash
# host-c에서 Deployer 시작
machadmin -u
```

### 2단계: 클러스터에 Warehouse 노드 등록

```bash
# Coordinator가 실행 중인 노드에서
machcoordinatoradmin --add-node=host-c:5300 --node-type=warehouse \
  --deployer=<deployer> --package-name=<package> --home-path=<path> \
  --port-no=<service-port> --replication=<replication-port> --group=<group>
```

### 3단계: 노드 상태 확인

```bash
machclusterctl status

# 또는 SQL로 확인
SELECT host, nodetype, state FROM v$node_status;
```

새 Warehouse 노드가 `RUNNING` 상태가 되면 자동으로 데이터 분산이 시작됩니다.

## 노드 제거 절차

운영 중 특정 Warehouse 노드를 제거할 때는 데이터 재배치 후 제거합니다.

```bash
# 상태 확인 후 제거
machcoordinatoradmin --remove-node=<warehouse-node-name-or-host:cluster-port>
```

> **주의:** 노드 제거 전에 해당 노드의 데이터 복사본이 다른 노드에 있는지 확인하세요. 단일 복제본인 경우 데이터 손실이 발생할 수 있습니다.

## 장애 복구

Warehouse 노드가 예기치 않게 중단된 경우:

```bash
# 1. 장애 노드 상태 확인
machclusterctl status

# 2. 해당 노드에서 Warehouse 재시작
machadmin -u  # 장애 노드에서 실행

# 3. 클러스터 합류 확인
machclusterctl status
```

자세한 Warehouse 장애 복구 절차는 [Warehouse 상태 복구](../../operations-configuration-recovery/cluster/recovery-state-status-warehouse/)를 참고하세요.

## Cluster Edition 제약사항

Cluster Edition에서는 다음 기능이 지원되지 않습니다.

| 기능 | 지원 여부 |
|------|:---:|
| RDB 테이블 | X |
| Custom ROLLUP | X |
| ROLLUP_REBUILD | X |
| MOUNT / UNMOUNT | X |
| STREAM / CQL | X |

전체 제한사항 목록은 [Cluster 운영 제한사항](../../operations-configuration-recovery/cluster/limitations-cluster/)을 참고하세요.
