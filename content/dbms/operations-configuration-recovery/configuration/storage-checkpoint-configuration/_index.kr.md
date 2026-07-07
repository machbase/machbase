---
type: docs
title: '스토리지와 체크포인트 설정'
weight: 60
---

데이터 저장 경로, 디스크 I/O 방식, 체크포인트 주기를 올바르게 설정하면 데이터 안전성과 쓰기 성능을 균형 있게 유지할 수 있습니다.

## 데이터 저장 경로

### DBS_PATH

Machbase 데이터베이스 파일이 저장되는 기본 경로입니다. `?`는 `$MACHBASE_HOME`을 의미합니다.

| 항목 | 값 |
|------|----|
| 기본값 | `?/dbs` |
| 재시작 필요 | 예 |

```ini
# machbase.conf
DBS_PATH = ?/dbs
```

별도 디스크나 볼륨을 사용하려면 절대 경로로 지정합니다.

```ini
# SSD 별도 마운트 경로 지정 예시
DBS_PATH = /data/machbase/dbs
```

경로를 변경한 뒤에는 기존 데이터를 새 경로로 이동하고 서버를 재시작해야 합니다.

## 체크포인트 설정

체크포인트는 메모리에 있는 변경 데이터를 디스크에 주기적으로 기록하는 작업입니다. 주기가 짧으면 I/O 부하가 증가하고, 너무 길면 재시작 시 복구 시간이 길어집니다.

### DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC

로그(컬럼형) 테이블의 체크포인트 주기입니다.

| 항목 | 값 |
|------|----|
| 기본값 | 120초 |
| 최솟값 | 1초 |
| 재시작 필요 | 예 |

```ini
# machbase.conf
DISK_COLUMNAR_TABLE_CHECKPOINT_INTERVAL_SEC = 120
```

### DISK_COLUMNAR_INDEX_CHECKPOINT_INTERVAL_SEC

인덱스의 체크포인트 주기입니다. 너무 길게 설정하면 인덱스 빌드 오류가 발생할 수 있습니다.

| 항목 | 값 |
|------|----|
| 기본값 | 120초 |
| 최솟값 | 1초 |
| 재시작 필요 | 예 |

### DISK_COLUMNAR_TABLE_COLUMN_PART_IO_INTERVAL_MIN_SEC

컬럼 파티션 파일을 디스크에 기록하는 최소 주기입니다. 파티션이 가득 차면 이 주기와 관계없이 즉시 기록됩니다.

| 항목 | 값 |
|------|----|
| 기본값 | 3초 |
| 최솟값 | 0초 |
| 재시작 필요 | 예 |

```ini
# machbase.conf
DISK_COLUMNAR_TABLE_COLUMN_PART_IO_INTERVAL_MIN_SEC = 3
```

## Direct I/O 설정

Direct I/O를 사용하면 OS 페이지 캐시를 거치지 않고 디스크에 직접 쓰므로 쓰기 지연 예측이 가능해지고 메모리 효율이 높아집니다.

### DISK_TABLESPACE_DIRECT_IO_WRITE

데이터 쓰기 연산에 Direct I/O를 사용할지 여부입니다.

| 항목 | 값 |
|------|----|
| 기본값 | 1 (사용) |
| 재시작 필요 | 예 |

> **주의**: ZFS처럼 Direct I/O를 지원하지 않는 파일 시스템을 사용한다면 0으로 설정합니다.

```ini
# machbase.conf
DISK_TABLESPACE_DIRECT_IO_WRITE = 1
```

### DISK_TABLESPACE_DIRECT_IO_READ

데이터 읽기 연산에 Direct I/O를 사용할지 여부입니다.

| 항목 | 값 |
|------|----|
| 기본값 | 0 (미사용) |
| 재시작 필요 | 예 |

### DISK_TABLESPACE_DIRECT_IO_FSYNC

Direct I/O 사용 시 fsync 수행 여부입니다. Direct I/O 환경에서는 fsync 없이도 일반적으로 데이터 유실이 없으나, 전원 차단이 발생할 수 있는 환경이라면 1로 설정합니다.

| 항목 | 값 |
|------|----|
| 기본값 | 0 (fsync 미사용) |
| 재시작 필요 | 예 |

### DISK_TABLESPACE_SYNCHRONOUS

디스크 테이블스페이스 파일의 동기화 정책입니다.

| 값 | 모드 | 설명 |
|----|------|------|
| 0 | OFF | 동기화하지 않음 |
| 1 | NORMAL | 더블라이트 파일 쓰기와 백업 시 동기화 (기본값) |
| 2 | FULL | NORMAL 포함, 디스크 파일 close 및 end RID 조정 시 동기화 |
| 3 | EXTRA | FULL 포함, 모든 write마다 동기화 |

## 디스크 I/O 스레드

### DISK_IO_THREAD_COUNT

데이터를 디스크에 기록하는 I/O 전담 스레드 수입니다. 스토리지의 병렬 처리 성능에 맞게 조정합니다.

| 항목 | 값 |
|------|----|
| 기본값 | 3 |
| 최솟값 | 1 |
| 재시작 필요 | 예 |

## 설정 최적화 가이드

| 환경 | 권장 설정 |
|------|-----------|
| SSD (NVMe) | `DISK_TABLESPACE_DIRECT_IO_WRITE=1`, `DISK_IO_THREAD_COUNT=4~8` |
| HDD | `DISK_TABLESPACE_DIRECT_IO_WRITE=0`, `DISK_IO_THREAD_COUNT=2~4` |
| 고가용성 요구 | `DISK_TABLESPACE_SYNCHRONOUS=2`, 체크포인트 주기 60~120초 |
| 고처리량 요구 | `DISK_TABLESPACE_SYNCHRONOUS=0 또는 1`, 체크포인트 주기 120~300초 |
| ZFS 파일 시스템 | `DISK_TABLESPACE_DIRECT_IO_WRITE=0` |

## 현재 설정 확인

```sql
SELECT name, value
  FROM v$property
 WHERE name LIKE 'DISK_%'
    OR name = 'DBS_PATH'
 ORDER BY name;
```
