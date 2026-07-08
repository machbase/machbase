---
type: docs
title: 'Cluster Edition 제한 오류'
weight: 20
---

Machbase Cluster Edition은 Standard Edition의 일부 기능을 지원하지 않습니다. 미지원 기능을 사용하려 하면 오류가 발생합니다. 이 페이지는 주요 제한 기능별 오류 메시지와 대안을 안내합니다.

Cluster Edition의 전반적인 제한사항에 대한 상세 내용은 [Cluster 운영 제한사항](../../../operations-configuration-recovery/cluster/limitations-cluster/)을 참고하십시오.

## 에디션 확인

현재 접속된 서버가 Cluster Edition인지 확인합니다.

```sql
SELECT * FROM v$version;
```

`EDITION` 항목이 `CLUSTER`이면 이 페이지의 제한사항이 적용됩니다.

## 주요 제한 기능과 오류

| 기능 | 오류 메시지 예시 | 대안 |
|------|----------------|------|
| RDB 테이블 생성/사용 | `RDB table is not supported in Cluster Edition` | LOOKUP 테이블 사용 |
| Custom ROLLUP | `Custom rollup is not supported in Cluster Edition` | 기본 자동 ROLLUP 사용 |
| ROLLUP_REBUILD | `ROLLUP_REBUILD is not supported in Cluster Edition` | 해당 기능 없음 (지원 문의) |
| MOUNT DATABASE | `MOUNT is not supported in Cluster Edition` | Standard Edition에서 마운트 후 데이터 추출 |
| UNMOUNT DATABASE | `UNMOUNT is not supported in Cluster Edition` | 해당 기능 없음 |
| STREAM | `STREAM is not supported in Cluster Edition` | CQL 또는 외부 파이프라인 검토 |

## 기능별 상세 안내

### RDB 테이블

Cluster Edition에서는 RDB 테이블을 생성하거나 조회할 수 없습니다.

```sql
-- 오류 발생: Cluster Edition에서 RDB 테이블 생성
CREATE RDB TABLE config_table (key VARCHAR(64), value VARCHAR(256));
-- ERR: RDB table is not supported in Cluster Edition
```

**대안**: 관계형 데이터 저장이 필요하다면 LOOKUP 테이블을 사용합니다.

```sql
-- 대안: LOOKUP 테이블 사용
CREATE TABLE config_table (
    config_key   VARCHAR(64) PRIMARY KEY,
    config_value VARCHAR(256)
);
```

### ROLLUP_REBUILD

ROLLUP 재계산 명령은 Cluster Edition에서 실행되지 않습니다.

```sql
-- 오류 발생: Cluster Edition에서 ROLLUP_REBUILD
EXEC ROLLUP_REBUILD(sensor_tag, rollup_1min, TO_DATE('2024-01-01'), TO_DATE('2024-01-02'));
-- ERR: ROLLUP_REBUILD is not supported in Cluster Edition
```

**대안**: Cluster Edition에서는 ROLLUP 재계산 기능이 없습니다. ROLLUP 데이터 불일치가 발생하면 기술 지원에 문의하십시오.

### MOUNT/UNMOUNT DATABASE

Cluster Edition에서는 백업 데이터베이스 마운트가 지원되지 않습니다.

```sql
-- 오류 발생: Cluster Edition에서 MOUNT
MOUNT DATABASE '/backup/machbase_20240101' TO backup_db;
-- ERR: MOUNT is not supported in Cluster Edition
```

**대안**: Standard Edition 환경에서 마운트하여 필요한 데이터를 추출한 후 Cluster Edition으로 적재합니다.

### STREAM

STREAM 기능은 Cluster Edition에서 제한됩니다.

```sql
-- 오류 발생: Cluster Edition에서 STREAM 생성
EXEC STREAM_CREATE(my_stream, 'INSERT INTO dest SELECT * FROM source;');
-- ERR: STREAM is not supported in Cluster Edition
```

**대안**: CQL(Continuous Query Language) 또는 외부 데이터 파이프라인(Kafka, Flink 등)을 이용한 데이터 흐름 구성을 검토합니다.

## Standard Edition 전환 검토

위 기능들이 운영에 필수적이라면 Standard Edition으로의 전환 또는 혼합 운영 구조를 검토합니다. 에디션 선택 기준에 대한 내용은 Machbase 기술 지원에 문의하십시오.
