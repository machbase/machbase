---
type: docs
title: '12.7.2 Cluster Edition 성능 고려사항'
weight: 20
---

Machbase Cluster Edition은 여러 노드에 데이터를 분산 저장하여 단일 노드의 처리 한계를 넘어설 수 있습니다. 그러나 클러스터 구성은 단순히 노드를 추가한다고 해서 자동으로 최적 성능을 내지는 않습니다. 노드 역할, 데이터 분산 방식, 네트워크 구성을 이해하고 각각을 조율해야 합니다.

## 클러스터 노드 구조

Machbase Cluster Edition은 Coordinator, Deployer, Broker, Warehouse, Lookup 역할로 구성됩니다. 성능 튜닝에서 입력 경로와 저장 처리를 볼 때는 주로 Broker와 Warehouse를 확인합니다.

```
클라이언트
    │
    ▼
[Broker 노드]   ← 라우팅 담당, 클라이언트 접속 수신
    │
    ▼
[Warehouse 노드] ← 실제 데이터 저장 및 Append 처리 (여러 개)
    │
    ▼
[Lookup 노드]   ← 태그 메타데이터 및 인덱스 조회
```

### Broker 노드

- 클라이언트 요청을 받아 적절한 Warehouse 경로로 라우팅합니다.
- 데이터를 직접 저장하지 않으므로 CPU 부하가 낮습니다.
- 대신 많은 클라이언트 연결을 동시에 수용해야 하므로 메모리를 충분히 확보해야 합니다.
- Broker 노드가 병목이 되는 경우는 드물지만, 연결 수가 매우 많은 환경에서는 `MAX_SESSION_COUNT`와 `CLUSTER_LINK_MAX_LISTEN`을 조정하십시오.

### Warehouse 노드

- Append 처리와 실제 데이터 파일 저장을 담당합니다.
- Append 처리량은 Warehouse 노드 수와 Broker 라우팅, 네트워크, 스토리지 성능에 영향을 받습니다.
- **SSD와 충분한 RAM**이 Warehouse 노드 성능의 핵심입니다.
- 각 Warehouse 노드는 독립적으로 체크포인트와 flush를 수행합니다.

### Lookup 노드

- 태그 메타데이터와 인덱스를 유지하여 쿼리 시 Warehouse 데이터 위치를 안내합니다.
- Lookup 노드 장애 시 조회가 전면 불가능해지므로 고가용성 구성(이중화)을 권장합니다.

## 데이터 분산과 병렬 처리

Warehouse 노드가 여러 개이면 Append 처리를 분산할 수 있습니다. 실제 처리량은 네트워크 오버헤드, Broker 라우팅, Warehouse 그룹 구성, 스토리지 성능에 따라 달라지므로 실측으로 병목을 확인해야 합니다.

Broker는 입력 데이터를 Warehouse 그룹으로 분배합니다. 분산이 고르지 않으면 일부 Warehouse 노드에 부하가 집중될 수 있습니다.

특정 노드에 데이터가 집중된다면 태그 이름/키 분포, Warehouse 그룹 구성, Broker 라우팅 설정, `INSERT_RECORD_COUNT_PER_NODE`에 따른 전송 단위를 함께 점검합니다. `TAG_PARTITION_COUNT`는 TAG 테이블 내부 파티션 수 설정이며, 클러스터 노드 분산을 직접 조정하는 값으로 사용하지 않습니다.

### INSERT_RECORD_COUNT_PER_NODE

입력 수행 시 Warehouse 그룹 전환을 유도하는 데이터 입력 개수입니다.

| | 값 |
|-|----|
| 최솟값 | 1 |
| 최댓값 | 2^32 - 1 |
| 기본값 | 1000 |

이 값을 높이면 Broker가 Warehouse 그룹을 전환하기 전 한 그룹에 더 많은 레코드를 전송합니다. 대규모 배치 입력 환경에서는 5,000~10,000으로 상향 조정을 고려하십시오.

```ini
# machbase.conf (Broker 노드)
INSERT_RECORD_COUNT_PER_NODE = 5000
```

### INSERT_BULK_DATA_MAX_SIZE

Append 또는 INSERT-SELECT 수행 시 입력 데이터 블록의 최대 크기입니다.

| | 값 |
|-|----|
| 최솟값 | 1024 (byte) |
| 최댓값 | 10 * 1024 * 1024 (byte) |
| 기본값 | 1024 * 1024 (1MB) |

네트워크 대역폭이 충분한 환경에서 대량 입력을 처리할 때는 이 값을 높이면 네트워크 효율이 향상됩니다.

```ini
INSERT_BULK_DATA_MAX_SIZE = 4194304   # 4MB
```

## 네트워크 대역폭 튜닝

클러스터 환경에서는 네트워크가 핵심 병목입니다. 클라이언트 → Broker → Warehouse 경로에서 패킷이 이동하므로, 클러스터 내부 통신에는 **10GbE 이상** 네트워크를 권장합니다.

### CLUSTER_LINK_BUFFER_SIZE

노드 간 송수신 버퍼 크기입니다.

| | 값 |
|-|----|
| 최솟값 | 1,024,768 (byte) |
| 최댓값 | 2^32 - 1 (byte) |
| 기본값 | 33,554,432 (32MB) |

초당 Append 건수가 매우 많거나 네트워크 지연이 발생한다면 이 값을 높이는 것을 검토하십시오.

```ini
CLUSTER_LINK_BUFFER_SIZE = 67108864   # 64MB (고처리량 환경)
```

### CLUSTER_REPLICATION_BLOCK_SIZE

노드 추가 시 Replication 진행 중 한 번에 전송하는 데이터 크기입니다.

| | 값 |
|-|----|
| 최솟값 | 65,536 (64KB) |
| 최댓값 | 104,857,600 (100MB) |
| 기본값 | 655,360 (640KB) |

고속 내부 네트워크(10GbE 이상)를 사용하는 경우 이 값을 높이면 노드 추가 시 Replication 완료 시간을 단축할 수 있습니다.

```ini
CLUSTER_REPLICATION_BLOCK_SIZE = 4194304   # 4MB
```

## Cluster Edition에서 지원하지 않는 기능

일부 기능은 Standard Edition에서만 사용 가능하며, Cluster Edition에서는 동작하지 않습니다.

| 기능 | Standard | Cluster | 대안 |
|------|----------|---------|------|
| CUSTOM_ROLLUP | 지원 | 미지원 | 주기적 집계 쿼리로 대체 |
| ROLLUP_REBUILD | 지원 | 미지원 | 필요 시 데이터 재입력 |
| PVO Cache | 지원 | 미지원 | 쿼리 실행 계획 재사용 불가 |

Cluster Edition 환경에서 집계 성능이 중요한 경우에는 ROLLUP 대신 별도의 집계 테이블을 만들어 주기적으로 데이터를 삽입하는 방식을 검토하십시오.

## Coordinator 설정

Coordinator는 클러스터 전체의 노드 상태를 관리하고 장애를 감지합니다.

### COORDINATOR_DISK_FULL_UPPER_BOUND_RATIO / LOWER_BOUND_RATIO

Warehouse 노드의 디스크 사용률이 `UPPER_BOUND_RATIO`를 초과하면 해당 노드에 새 데이터 입력을 중단하고, `LOWER_BOUND_RATIO` 이하로 회복되면 재개합니다.

```ini
COORDINATOR_DISK_FULL_UPPER_BOUND_RATIO = 90   # 90% 이상 시 입력 중단
COORDINATOR_DISK_FULL_LOWER_BOUND_RATIO = 80   # 80% 이하로 회복 시 재개
```

운영 환경에서는 디스크 사용률이 80%를 넘기 전에 파티션 정리 또는 스토리지 확장 계획을 수립하십시오.

## 권장 클러스터 구성 요약

| 노드 역할 | 권장 사양 | 핵심 설정 |
|-----------|-----------|-----------|
| Broker | CPU 8코어 이상, RAM 32GB | `MAX_SESSION_COUNT`, `CLUSTER_LINK_BUFFER_SIZE` |
| Active | CPU 16코어 이상, RAM 64GB, NVMe SSD | `DISK_IO_THREAD_COUNT`, `INSERT_RECORD_COUNT_PER_NODE` |
| Lookup | CPU 8코어 이상, RAM 32GB, SSD | 이중화(2대) 구성 권장 |
