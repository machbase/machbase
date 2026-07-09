---
type: docs
title: '13.7.4 machclusterctl start/stop/destroy'
weight: 40
---

`machclusterctl`은 Machbase Cluster Edition 전용 통합 CLI입니다. 클러스터 전체를 대상으로 시작·종료·삭제를 한 번에 처리합니다.

## 클러스터 전체 시작

```bash
machclusterctl start
```

클러스터에 등록된 모든 노드를 미리 정의된 시작 순서에 따라 기동합니다.

**내부 시작 순서:**

1. Coordinator
2. Deployer
3. Broker
4. Warehouse (Active/Lookup)

각 단계에서 이전 노드 유형이 정상 상태(normal/leader)로 전환된 것을 확인한 후 다음 단계로 넘어갑니다. 노드 시작에 실패하면 오류를 출력하고 중단합니다.

## 클러스터 전체 종료

```bash
machclusterctl stop
```

시작의 역순으로 모든 노드를 안전하게 종료합니다.

**내부 종료 순서:**

1. Warehouse (Active/Lookup)
2. Broker
3. Deployer
4. Coordinator

각 노드가 처리 중인 트랜잭션을 완료한 후 종료되므로, 데이터 유실 없이 안전하게 클러스터를 내릴 수 있습니다.

## 클러스터 완전 삭제

```bash
machclusterctl destroy
```

> **주의:** 이 명령은 클러스터 메타데이터와 데이터베이스 파일을 **영구적으로 삭제**합니다. 실행 전 반드시 데이터 백업 여부를 확인하십시오.

클러스터에 등록된 모든 노드의 프로세스를 종료하고 데이터베이스 파일, 설정 파일, 메타 정보를 삭제합니다. 클러스터를 완전히 초기화하고 새로 구성할 때 사용합니다.

## 시작/종료 시 주의사항

- **개별 노드가 이미 실행 중인 경우**: `machclusterctl start`는 이미 실행 중인 노드를 건너뜁니다.
- **네트워크 단절 상태에서 시작**: 특정 노드에 도달할 수 없는 경우 해당 노드 시작이 실패하고 전체 시작이 중단될 수 있습니다.
- **대규모 클러스터**: 노드 수가 많을수록 `start`/`stop` 완료까지 시간이 걸립니다. 완료 메시지가 출력될 때까지 기다립니다.

## 개별 노드 제어

클러스터 전체가 아닌 특정 노드만 시작·종료하려면 `machclusterctl`의 `--node` 옵션에 노드 alias를 지정합니다. `machcoordinatoradmin`은 저수준 수동 운영이 필요한 경우에만 사용합니다.

```bash
# 특정 노드 시작
machclusterctl start --node=warehouse-group1-1

# 특정 노드 종료
machclusterctl stop --node=warehouse-group1-1
```

자세한 내용은 [Cluster 노드 시작과 종료](../node-start-cluster/)를 참조하십시오.
