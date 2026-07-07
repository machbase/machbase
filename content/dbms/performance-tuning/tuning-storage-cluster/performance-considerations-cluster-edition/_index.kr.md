---
type: docs
title: 'Cluster Edition 성능 고려사항'
weight: 20
---

Machbase Cluster Edition은 여러 노드에 데이터를 분산 저장하여 단일 노드의 처리 한계를 넘어설 수 있습니다. 그러나 클러스터 구성은 단순히 노드를 추가한다고 해서 자동으로 최적 성능을 내지는 않습니다. 노드 역할, 데이터 분산 방식, 네트워크 구성을 이해하고 각각을 조율해야 합니다.

## 클러스터 노드 구조

Machbase Cluster Edition은 세 가지 역할의 노드로 구성됩니다.

```
클라이언트
    │
    ▼
[Broker 노드]   ← 라우팅 담당, 클라이언트 접속 수신
    │
    ▼
[Active 노드]   ← 실제 데이터 저장 및 Append 처리 (여러 개)
    │
    ▼
[Lookup 노드]   ← 태그 메타데이터 및 인덱스 조회
```

### Broker 노드

- 클라이언트 요청을 받아 적절한 Active 노드로 라우팅합니다.
- 데이터를 직접 저장하지 않으므로 CPU 부하가 낮습니다.
- 대신 많은 클라이언트 연결을 동시에 수용해야 하므로 메모리를 충분히 확보해야 합니다.
- Broker 노드가 병목이 되는 경우는 드물지만, 연결 수가 매우 많은 환경에서는 `MAX_SESSION_COUNT`와 `CLUSTER_LINK_MAX_LISTEN`을 조정하십시오.

### Active 노드

- Append 처리와 실제 데이터 파일 저장을 담당합니다.
- Append 처리량은 Active 노드 수에 비례해 증가합니다 (이론상 N개 Active = N배 처리량).
- **SSD와 충분한 RAM**이 Active 노드 성능의 핵심입니다.
- 각 Active 노드는 독립적으로 체크포인트와 flush를 수행합니다.

### Lookup 노드

- 태그 메타데이터와 인덱스를 유지하여 쿼리 시 Active 노드 위치를 안내합니다.
- Lookup 노드 장애 시 조회가 전면 불가능해지므로 고가용성 구성(이중화)을 권장합니다.

## 데이터 분산과 병렬 처리

Active 노드가 N개일 때 Append 처리량은 이론상 단일 노드 대비 N배입니다. 실제로는 네트워크 오버헤드와 Broker 라우팅 비용이 있으므로 완전한 선형 확장은 어렵지만, 3~4개 Active 노드 구성에서 2.5~3.5배 이상의 처리량 개선을 기대할 수 있습니다.

데이터는 태그명의 해시 값에 따라 Active 노드에 분산됩니다. 분산이 고르지 않으면 일부 Active 노드에 부하가 집중됩니다.

**불균등 분포 확인 방법**

```sql
-- 각 Active 노드별 저장된 데이터 건수 비교
SELECT warehouse_id, count(*) 
FROM v$table_stat 
GROUP BY warehouse_id;
```

특정 노드에 데이터가 집중된다면 태그 이름 설계 또는 파티션 수(`TAG_PARTITION_COUNT`) 조정을 검토하십시오.

### INSERT_RECORD_COUNT_PER_NODE

입력 수행 시 Warehouse 그룹 전환을 유도하는 데이터 입력 개수입니다.

| | 값 |
|-|----|
| 최솟값 | 1 |
| 최댓값 | 2^32 - 1 |
| 기본값 | 1000 |

이 값을 높이면 한 번에 같은 Active 노드에 더 많은 데이터를 전송하여 네트워크 왕복 횟수를 줄입니다. 대규모 배치 입력 환경에서는 5,000~10,000으로 상향 조정을 고려하십시오.

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

클러스터 환경에서는 네트워크가 핵심 병목입니다. 클라이언트 → Broker → Active 노드 경로에서 패킷이 이동하므로, 클러스터 내부 통신에는 **10GbE 이상** 네트워크를 권장합니다.

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

Active 노드의 디스크 사용률이 `UPPER_BOUND_RATIO`를 초과하면 해당 노드에 새 데이터 입력을 중단하고, `LOWER_BOUND_RATIO` 이하로 회복되면 재개합니다.

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
