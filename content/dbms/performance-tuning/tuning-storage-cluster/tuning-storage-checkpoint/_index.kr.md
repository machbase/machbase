---
type: docs
title: '스토리지와 체크포인트 튜닝'
weight: 10
---

스토리지 튜닝의 핵심은 메모리 버퍼와 디스크 사이의 데이터 이동을 얼마나 효율적으로 제어하느냐에 있습니다. 체크포인트 주기, flush 간격, Direct I/O 설정이 맞물려 Append 처리량과 복구 시간에 동시에 영향을 줍니다.

## 체크포인트(Checkpoint) 이해

체크포인트는 메모리 버퍼에 쌓인 변경 내용을 디스크에 안전하게 동기화하는 작업입니다. Machbase는 테이블 데이터와 인덱스에 대해 각각 독립적인 체크포인트 주기를 설정할 수 있습니다.

```
Append → 메모리 버퍼 → (flush 주기마다) → 파티션 파일
                     → (체크포인트 주기마다) → 체크포인트 메타 기록
```

체크포인트가 기록된 시점까지는 장애가 발생해도 빠르게 복구할 수 있습니다. 체크포인트 간격이 길면 복구 시간이 늘어나고, 너무 짧으면 빈번한 I/O로 처리량이 낮아집니다.

### DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC

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

### DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC

인덱스에 대한 체크포인트 주기를 설정합니다. 너무 길게 설정하면 인덱스 빌드 중 오류가 발생할 수 있습니다.

| | 값 |
|-|----|
| 최솟값 | 1 (초) |
| 최댓값 | 2^32 - 1 (초) |
| 기본값 | 120 (초) |

```ini
DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC = 120
```

## 파티션 Flush 설정

### DISK_COLUMNAR_TABLE_COLUMN_PART_IO_INTERVAL_MIN_SEC

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

### DISK_COLUMNAR_TABLE_COLUMN_PART_FLUSH_MODE

컬럼 파티션이 가득 찼을 때만 flush할지 여부를 설정합니다.

| | 값 |
|-|----|
| 최솟값 | 0 |
| 최댓값 | 1 |
| 기본값 | 0 |

- `0`: 주기(`DISK_COLUMNAR_TABLE_COLUMN_PART_IO_INTERVAL_MIN_SEC`)에 따라 flush
- `1`: 파티션이 가득 찼을 때만 flush (처리량 우선 모드)

Append 처리량을 최대화하고 데이터 유실 허용 범위가 넓다면 `1`로 설정할 수 있습니다.

## Direct I/O 설정

Direct I/O는 OS 페이지 캐시를 우회하여 디스크에 직접 쓰는 방식입니다. Machbase처럼 자체 버퍼 관리 구조를 갖춘 DB에서는 OS 페이지 캐시와의 이중 버퍼링을 피할 수 있어 메모리 효율이 높아집니다.

### DISK_TABLESPACE_DIRECT_IO_WRITE

데이터 쓰기 연산에 Direct I/O를 사용할지 설정합니다.

| | 값 |
|-|----|
| 최솟값 | 0 |
| 최댓값 | 1 |
| 기본값 | 1 |

기본값이 `1`(활성화)이므로 대부분의 환경에서는 변경할 필요가 없습니다. ZFS처럼 Direct I/O를 지원하지 않는 파일 시스템을 사용하는 경우에는 `0`으로 설정해야 합니다.

### DISK_TABLESPACE_DIRECT_IO_READ

데이터 읽기 연산에 Direct I/O를 사용할지 설정합니다.

| | 값 |
|-|----|
| 최솟값 | 0 |
| 최댓값 | 1 |
| 기본값 | 0 |

읽기는 OS 페이지 캐시의 재사용 이점이 있으므로 기본값 `0`을 유지하는 경우가 많습니다. 단, 매우 큰 범위 스캔이 OS 페이지 캐시를 과도하게 차지하는 환경에서는 `1`로 설정을 검토할 수 있습니다.

### DISK_TABLESPACE_DIRECT_IO_FSYNC

Direct I/O 사용 시 fsync 수행 여부를 설정합니다.

| | 값 |
|-|----|
| 최솟값 | 0 |
| 최댓값 | 1 |
| 기본값 | 0 |

Direct I/O를 사용할 경우 데이터 파일에 대한 fsync는 불필요합니다. `0`(비활성)으로 두면 I/O 성능이 향상됩니다. 전원 장애 복구가 매우 중요한 환경이라면 `1`로 설정하십시오.

### DISK_TABLESPACE_SYNCHRONOUS

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

### DISK_IO_THREAD_COUNT

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

## DBS_PATH 배치

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

## 데이터 보존 정책 점검

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

## 권장 설정 요약

| 프로퍼티 | 기본값 | 권장 조정 방향 |
|----------|--------|----------------|
| `DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC` | 120 | 복구 시간 중요 시 낮추고, I/O 부하 높으면 높임 |
| `DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC` | 120 | 기본값 유지 권장 |
| `DISK_COLUMNAR_TABLE_COLUMN_PART_IO_INTERVAL_MIN_SEC` | 3 | Append 처리량 우선 시 높이고, 내구성 우선 시 낮춤 |
| `DISK_TABLESPACE_DIRECT_IO_WRITE` | 1 | 기본값 유지 (ZFS 제외) |
| `DISK_TABLESPACE_SYNCHRONOUS` | 1 | 고처리량 환경은 1, 안전성 최우선은 2 |
| `DISK_IO_THREAD_COUNT` | 3 | NVMe SSD 환경에서 4~8로 상향 검토 |
