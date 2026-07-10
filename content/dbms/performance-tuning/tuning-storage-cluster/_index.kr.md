---
type: docs
title: '12.7 스토리지와 Cluster 튜닝'
weight: 70
---
입력과 대용량 범위 조회에서는 디스크 I/O가 병목이 될 수 있습니다. 스토리지 지연과 처리량을
측정하고 Cluster Edition의 노드별 I/O 부하를 확인하는 방법을 다룹니다.

## I/O가 핵심 병목인 이유

Machbase는 컬럼형 스토리지 구조를 사용합니다. Append된 데이터는 메모리 버퍼에 먼저 쌓인 뒤 주기적으로 디스크 파티션 파일로 flush됩니다. 이 flush 경로에서 디스크 I/O 처리 능력이 부족하면 다음 현상이 나타납니다.

- 메모리 버퍼가 가득 차 Append 속도가 느려집니다 (`DISK_COLUMNAR_TABLESPACE_MEMORY_SLOWDOWN_*` 임계치 도달).
- 체크포인트가 밀리고 장애 발생 시 복구 시간이 길어집니다.
- 동시에 SELECT를 실행하면 I/O 경합으로 쿼리 응답 시간이 급격히 증가합니다.

## SSD vs HDD 선택 기준

| 구분 | SSD | HDD |
|------|-----|-----|
| Append 처리량 | 높음 (순차 쓰기 최적화) | 낮음 (회전 지연 발생) |
| 랜덤 읽기 | 빠름 | 매우 느림 |
| 비용 | 높음 | 낮음 |
| 권장 용도 | `DBS_PATH` 데이터 파일 | 콜드 데이터 아카이브 |

**SSD를 우선 검토하는 경우**

- 초당 10만 건 이상 Append가 발생하는 환경
- 여러 테이블을 동시에 쓰고 읽는 혼합 워크로드
- Cluster Edition에서 Warehouse 역할을 담당하는 호스트

이 빌드에서 사용자 설정으로 분리 가능한 별도 WAL/redo 경로는 확인되지 않습니다. 데이터베이스 파일이 저장되는 `DBS_PATH`를 빠른 스토리지에 배치하는 것을 우선 검토합니다.

## 이 섹션의 구성

| 항목 | 설명 |
|------|------|
| [스토리지와 체크포인트 튜닝](/dbms/performance-tuning/tuning-storage-cluster/#tuning-storage-checkpoint) | 체크포인트 주기, flush 설정, Direct I/O, 파티션 정리 |
| [Cluster Edition 성능 고려사항](/dbms/performance-tuning/tuning-storage-cluster/#performance-considerations-cluster-edition) | 노드 구조, 분산 처리, 네트워크 튜닝 |


<a id="tuning-storage-checkpoint"></a>

## 스토리지와 체크포인트 튜닝

스토리지 튜닝의 핵심은 메모리 버퍼와 디스크 사이의 데이터 이동을 얼마나 효율적으로 제어하느냐에 있습니다. 체크포인트 주기, flush 간격, Direct I/O 설정이 맞물려 Append 처리량과 복구 시간에 동시에 영향을 줍니다.

### 체크포인트(Checkpoint) 이해

체크포인트는 메모리 버퍼에 쌓인 변경 내용을 디스크에 안전하게 동기화하는 작업입니다. Machbase는 테이블 데이터와 인덱스에 대해 각각 독립적인 체크포인트 주기를 설정할 수 있습니다.

```
Append → 메모리 버퍼 → (flush 주기마다) → 파티션 파일
                     → (체크포인트 주기마다) → 체크포인트 메타 기록
```

체크포인트가 기록된 시점까지는 장애가 발생해도 빠르게 복구할 수 있습니다. 체크포인트 간격이 길면 복구 시간이 늘어나고, 너무 짧으면 빈번한 I/O로 처리량이 낮아집니다.

#### DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC

테이블 데이터의 체크포인트 주기를 설정합니다.

| | 값 |
|-|----|
| 최솟값 | 1 (초) |
| 최댓값 | 2^32 - 1 (초) |
| 기본값 | 120 (초) |

이 값이 너무 크면 서버 재시작 시 복구 시간이 매우 길어지고, 너무 작으면 I/O가 자주 발생하여 전체 성능이 저하됩니다.

**권장값 가이드**

| 환경 | 권장 주기 |
|------|-----------|
| 고속 SSD, Append 집중 환경 | 60~120초 (기본값 유지) |
| HDD 환경 또는 I/O 부하 높은 경우 | 180~300초 |
| 장애 복구 시간을 최소화해야 하는 경우 | 30~60초 |

```ini
# machbase.conf
DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC = 120
```

#### DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC

인덱스에 대한 체크포인트 주기를 설정합니다. 너무 길게 설정하면 인덱스 빌드 중 오류가 발생할 수 있습니다.

| | 값 |
|-|----|
| 최솟값 | 1 (초) |
| 최댓값 | 2^32 - 1 (초) |
| 기본값 | 120 (초) |

```ini
DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC = 120
```

### 파티션 Flush 설정

#### DISK_COLUMNAR_TABLE_COLUMN_PART_IO_INTERVAL_MIN_SEC

파티션 파일을 디스크에 반영하는 최소 주기입니다. 파티션이 설정된 개수보다 더 많은 데이터를 입력받으면 이 주기와 관계없이 디스크에 반영됩니다.

| | 값 |
|-|----|
| 최솟값 | 0 (초) |
| 최댓값 | 2^32 - 1 (초) |
| 기본값 | 3 (초) |

- 값을 낮추면 디스크 반영이 잦아져 내구성은 높아지지만 I/O 부하가 증가합니다.
- 값을 높이면 처리량이 증가하지만 서버 비정상 종료 시 최대 그 시간만큼의 데이터가 유실될 수 있습니다.
- Append가 매우 빠른 환경에서는 기본값 3초가 적당합니다. Append 속도가 낮고 내구성이 중요하면 1초로 줄이는 것을 검토하십시오.

```ini
DISK_COLUMNAR_TABLE_COLUMN_PART_IO_INTERVAL_MIN_SEC = 3
```

#### DISK_COLUMNAR_TABLE_COLUMN_PART_FLUSH_MODE

컬럼 파티션이 가득 찼을 때만 flush할지 여부를 설정합니다.

| | 값 |
|-|----|
| 최솟값 | 0 |
| 최댓값 | 1 |
| 기본값 | 0 |

- `0`: 주기(`DISK_COLUMNAR_TABLE_COLUMN_PART_IO_INTERVAL_MIN_SEC`)에 따라 flush
- `1`: 파티션이 가득 찼을 때만 flush (처리량 우선 모드)

Append 처리량을 최대화하고 데이터 유실 허용 범위가 넓다면 `1`로 설정할 수 있습니다.

### Direct I/O 설정

Direct I/O는 OS 페이지 캐시를 우회하여 디스크에 직접 쓰는 방식입니다. Machbase처럼 자체 버퍼 관리 구조를 갖춘 DB에서는 OS 페이지 캐시와의 이중 버퍼링을 피할 수 있어 메모리 효율이 높아집니다.

#### DISK_TABLESPACE_DIRECT_IO_WRITE

데이터 쓰기 연산에 Direct I/O를 사용할지 설정합니다.

| | 값 |
|-|----|
| 최솟값 | 0 |
| 최댓값 | 1 |
| 기본값 | 1 |

기본값이 `1`(활성화)이므로 대부분의 환경에서는 변경할 필요가 없습니다. ZFS처럼 Direct I/O를 지원하지 않는 파일 시스템을 사용하는 경우에는 `0`으로 설정해야 합니다.

#### DISK_TABLESPACE_DIRECT_IO_READ

데이터 읽기 연산에 Direct I/O를 사용할지 설정합니다.

| | 값 |
|-|----|
| 최솟값 | 0 |
| 최댓값 | 1 |
| 기본값 | 0 |

읽기는 OS 페이지 캐시의 재사용 이점이 있으므로 기본값 `0`을 유지하는 경우가 많습니다. 단, 매우 큰 범위 스캔이 OS 페이지 캐시를 과도하게 차지하는 환경에서는 `1`로 설정을 검토할 수 있습니다.

#### DISK_TABLESPACE_DIRECT_IO_FSYNC

Direct I/O 사용 시 fsync 수행 여부를 설정합니다.

| | 값 |
|-|----|
| 최솟값 | 0 |
| 최댓값 | 1 |
| 기본값 | 0 |

Direct I/O를 사용할 경우 데이터 파일에 대한 fsync는 불필요합니다. `0`(비활성)으로 두면 I/O 성능이 향상됩니다. 전원 장애 복구가 매우 중요한 환경이라면 `1`로 설정하십시오.

#### DISK_TABLESPACE_SYNCHRONOUS

디스크 테이블스페이스 파일의 동기화 정책을 설정합니다.

| 값 | 모드 | 설명 |
|--|--|--|
| 0 | OFF | 동기화하지 않음 |
| 1 | NORMAL | 더블라이트 파일 쓰기와 백업 시 동기화 |
| 2 | FULL | NORMAL을 포함하며 디스크 파일 close 및 end RID 조정 시 동기화 |
| 3 | EXTRA | FULL을 포함하며 모든 write마다 동기화 |

| | 값 |
|-|----|
| 기본값 | 1 (NORMAL) |

고속 Append가 필요한 환경에서는 기본값 `1`을 유지합니다. 데이터 안전성이 최우선인 금융·의료 환경에서는 `2` 또는 `3`을 검토하되, 처리량 저하를 감안해야 합니다.

#### DISK_IO_THREAD_COUNT

데이터를 디스크에 기록하는 I/O 스레드 수입니다.

| | 값 |
|-|----|
| 최솟값 | 1 |
| 최댓값 | 2^32 - 1 |
| 기본값 | 3 |

NVMe SSD처럼 병렬 I/O 성능이 우수한 스토리지를 사용하는 경우 스레드 수를 늘리면 처리량이 향상될 수 있습니다. 물리 코어 수의 절반을 넘지 않도록 설정하십시오.

```ini
DISK_IO_THREAD_COUNT = 4   # NVMe SSD 사용 시
```

### DBS_PATH 배치

Machbase 데이터 파일은 `DBS_PATH` 아래에 저장됩니다. 쓰기 처리량이 높은 환경에서는 `DBS_PATH`를 지연 시간이 낮고 쓰기 성능이 높은 SSD/NVMe 장치에 배치합니다. 이 빌드에서 사용자 설정으로 분리 가능한 별도 WAL/redo 경로는 확인되지 않습니다.

**모범 사례: 빠른 스토리지 배치 예시**

```
/nvme0/machbase/dbs/       ← DBS_PATH (NVMe SSD)
```

`machbase.conf`에서 경로 변경:

```ini
DBS_PATH = /nvme0/machbase/dbs
```

DBS 경로는 서버 초기 설치 시 결정하는 것이 안전합니다. 운영 중 변경해야 한다면 반드시 정상 종료 후 파일 이동과 설정 변경 절차를 검증해야 합니다.

### 데이터 보존 정책 점검

LOG/TAG 테이블에 데이터를 장기간 적재하면 데이터 파일이 계속 늘어납니다. 보존 기간을 정하고 오래된 데이터를 삭제해야 디스크 공간과 체크포인트 부하를 제어할 수 있습니다.

```sql
-- TAG 테이블의 기본 파티션 설정 확인
SELECT name, value
FROM v$property
WHERE name IN ('TAG_PARTITION_COUNT', 'TAG_DATA_PART_SIZE');

-- TAG 테이블별 파티션 설정 확인
SELECT id, name, value
FROM m$sys_table_property
WHERE name = 'TAG_PARTITION_COUNT';

-- 특정 TAG 테이블의 내부 데이터 테이블 수 확인
SELECT COUNT(*) AS tag_data_table_count
FROM m$sys_tables
WHERE name LIKE '_SENSOR_TAG_DATA_%';

-- 특정 시점 이전 데이터 삭제
DELETE FROM sensor_log BEFORE TO_DATE('2024-01-01', 'YYYY-MM-DD');
DELETE FROM sensor_tag BEFORE TO_DATE('2024-01-01', 'YYYY-MM-DD');
```

이 빌드에서는 `ALTER TABLE ... DROP PARTITION BEFORE ...` 문법을 사용할 수 없습니다. 보존 정책을 자동화할 때는 `DELETE FROM ... BEFORE ...`와 백업 정책을 기준으로 설계합니다.

### 권장 설정 요약

| 프로퍼티 | 기본값 | 권장 조정 방향 |
|----------|--------|----------------|
| `DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC` | 120 | 복구 시간 중요 시 낮추고, I/O 부하 높으면 높임 |
| `DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC` | 120 | 기본값 유지 권장 |
| `DISK_COLUMNAR_TABLE_COLUMN_PART_IO_INTERVAL_MIN_SEC` | 3 | Append 처리량 우선 시 높이고, 내구성 우선 시 낮춤 |
| `DISK_TABLESPACE_DIRECT_IO_WRITE` | 1 | 기본값 유지 (ZFS 제외) |
| `DISK_TABLESPACE_SYNCHRONOUS` | 1 | 고처리량 환경은 1, 안전성 최우선은 2 |
| `DISK_IO_THREAD_COUNT` | 3 | NVMe SSD 환경에서 4~8로 상향 검토 |

<a id="performance-considerations-cluster-edition"></a>

## Cluster Edition 성능 고려사항

Machbase Cluster Edition은 여러 노드에 데이터를 분산 저장하여 단일 노드의 처리 한계를 넘어설 수 있습니다. 그러나 클러스터 구성은 단순히 노드를 추가한다고 해서 자동으로 최적 성능을 내지는 않습니다. 노드 역할, 데이터 분산 방식, 네트워크 구성을 이해하고 각각을 조율해야 합니다.

### 클러스터 노드 구조

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

#### Broker 노드

- 클라이언트 요청을 받아 적절한 Warehouse 경로로 라우팅합니다.
- 데이터를 직접 저장하지 않으므로 CPU 부하가 낮습니다.
- 대신 많은 클라이언트 연결을 동시에 수용해야 하므로 메모리를 충분히 확보해야 합니다.
- Broker 노드가 병목이 되는 경우는 드물지만, 연결 수가 매우 많은 환경에서는 `MAX_SESSION_COUNT`와 `CLUSTER_LINK_MAX_LISTEN`을 조정하십시오.

#### Warehouse 노드

- Append 처리와 실제 데이터 파일 저장을 담당합니다.
- Append 처리량은 Warehouse 노드 수와 Broker 라우팅, 네트워크, 스토리지 성능에 영향을 받습니다.
- **SSD와 충분한 RAM**이 Warehouse 노드 성능의 핵심입니다.
- 각 Warehouse 노드는 독립적으로 체크포인트와 flush를 수행합니다.

#### Lookup 노드

- 태그 메타데이터와 인덱스를 유지하여 쿼리 시 Warehouse 데이터 위치를 안내합니다.
- Lookup 노드 장애 시 조회가 전면 불가능해지므로 고가용성 구성(이중화)을 권장합니다.

### 데이터 분산과 병렬 처리

Warehouse 노드가 여러 개이면 Append 처리를 분산할 수 있습니다. 실제 처리량은 네트워크 오버헤드, Broker 라우팅, Warehouse 그룹 구성, 스토리지 성능에 따라 달라지므로 실측으로 병목을 확인해야 합니다.

Broker는 입력 데이터를 Warehouse 그룹으로 분배합니다. 분산이 고르지 않으면 일부 Warehouse 노드에 부하가 집중될 수 있습니다.

특정 노드에 데이터가 집중된다면 태그 이름/키 분포, Warehouse 그룹 구성, Broker 라우팅 설정, `INSERT_RECORD_COUNT_PER_NODE`에 따른 전송 단위를 함께 점검합니다. `TAG_PARTITION_COUNT`는 TAG 테이블 내부 파티션 수 설정이며, 클러스터 노드 분산을 직접 조정하는 값으로 사용하지 않습니다.

#### INSERT_RECORD_COUNT_PER_NODE

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

#### INSERT_BULK_DATA_MAX_SIZE

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

### 네트워크 대역폭 튜닝

클러스터 환경에서는 네트워크가 핵심 병목입니다. 클라이언트 → Broker → Warehouse 경로에서 패킷이 이동하므로, 클러스터 내부 통신에는 **10GbE 이상** 네트워크를 권장합니다.

#### CLUSTER_LINK_BUFFER_SIZE

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

#### CLUSTER_REPLICATION_BLOCK_SIZE

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

### Cluster Edition에서 지원하지 않는 기능

일부 기능은 Standard Edition에서만 사용 가능하며, Cluster Edition에서는 동작하지 않습니다.

| 기능 | Standard | Cluster | 대안 |
|------|----------|---------|------|
| CUSTOM_ROLLUP | 지원 | 미지원 | 주기적 집계 쿼리로 대체 |
| ROLLUP_REBUILD | 지원 | 미지원 | 필요 시 데이터 재입력 |
| PVO Cache | 지원 | 미지원 | 쿼리 실행 계획 재사용 불가 |

Cluster Edition 환경에서 집계 성능이 중요한 경우에는 ROLLUP 대신 별도의 집계 테이블을 만들어 주기적으로 데이터를 삽입하는 방식을 검토하십시오.

### Coordinator 설정

Coordinator는 클러스터 전체의 노드 상태를 관리하고 장애를 감지합니다.

#### COORDINATOR_DISK_FULL_UPPER_BOUND_RATIO / LOWER_BOUND_RATIO

Warehouse 노드의 디스크 사용률이 `UPPER_BOUND_RATIO`를 초과하면 해당 노드에 새 데이터 입력을 중단하고, `LOWER_BOUND_RATIO` 이하로 회복되면 재개합니다.

```ini
COORDINATOR_DISK_FULL_UPPER_BOUND_RATIO = 90   # 90% 이상 시 입력 중단
COORDINATOR_DISK_FULL_LOWER_BOUND_RATIO = 80   # 80% 이하로 회복 시 재개
```

운영 환경에서는 디스크 사용률이 80%를 넘기 전에 파티션 정리 또는 스토리지 확장 계획을 수립하십시오.

### 권장 클러스터 구성 요약

| 노드 역할 | 권장 사양 | 핵심 설정 |
|-----------|-----------|-----------|
| Broker | CPU 8코어 이상, RAM 32GB | `MAX_SESSION_COUNT`, `CLUSTER_LINK_BUFFER_SIZE` |
| Active | CPU 16코어 이상, RAM 64GB, NVMe SSD | `DISK_IO_THREAD_COUNT`, `INSERT_RECORD_COUNT_PER_NODE` |
| Lookup | CPU 8코어 이상, RAM 32GB, SSD | 이중화(2대) 구성 권장 |
