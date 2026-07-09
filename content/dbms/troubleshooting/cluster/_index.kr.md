---
type: docs
title: '16.8 Cluster 문제'
weight: 80
---
Machbase Cluster Edition 운영 중 노드 상태 이상이나 Cluster Edition 전용 제한 오류가 발생할 때 원인을 진단하고 해결하는 방법을 설명합니다.

클러스터 구성과 일반적인 운영 절차에 대한 상세 내용은 [Cluster 운영](../../../operations-configuration-recovery/cluster/)을 참고하십시오.

## 이 섹션의 구성

| 페이지 | 내용 |
|--------|------|
| [Cluster 노드 상태가 비정상일 때](/dbms/troubleshooting/cluster/#node-state-status-abnormal-cluster) | 노드 상태 확인, 재기동, Warehouse 복구 방법 |
| [Cluster Edition 제한 오류](/dbms/troubleshooting/cluster/#error-cluster-edition) | 미지원 기능 오류 및 대안 안내 |


<a id="node-state-status-abnormal-cluster"></a>

## Cluster 노드 상태가 비정상일 때

Cluster Edition에서 특정 노드가 비정상 상태로 전환되면 데이터 입력, 쿼리, 또는 클러스터 전체 기능에 영향을 미칠 수 있습니다. 노드 상태를 확인하고 복구하는 방법을 설명합니다.

### 노드 상태 확인

클러스터 전체 상태를 확인합니다.

```bash
# 클러스터 상태 전체 확인
machclusterctl status
```

또는 Coordinator를 통해 상세 상태를 조회합니다.

```bash
machcoordinatoradmin --cluster-status-full
```

SQL로도 노드 상태를 조회할 수 있습니다.

```sql
SELECT host, nodetype, state, coord_host, coord_http_admin_port
  FROM v$node_status;
```

### 비정상 상태 유형과 조치

| 상태 | 의미 | 조치 |
|------|------|------|
| `STOPPED` | 프로세스가 종료된 상태 | 해당 노드에서 `machadmin -u` 실행 |
| `DISCONNECTED` | 네트워크 단절 | 네트워크 상태 확인 후 재연결 대기 |
| `ERROR` | 내부 오류 발생 | 해당 노드 트레이스 로그 확인 |
| `scrapped` | 데이터 손상 또는 복구 불가 상태 | Snapshot 복구 또는 강제 복구 |

### Warehouse 노드 재기동

Warehouse 노드가 `STOPPED` 상태인 경우 해당 노드에서 직접 재기동합니다.

```bash
# 1. 장애 노드 확인
machcoordinatoradmin --cluster-status-full

# 2. Coordinator에서 노드 시작 (Coordinator가 접근 가능한 경우)
machcoordinatoradmin --startup-node=warehouse-a1

# 3. 또는 해당 호스트에 직접 접속하여 시작
export MACHBASE_HOME=/home/machbase/warehouse_a1
machadmin -u

# 4. 상태 복귀 확인
machcoordinatoradmin --cluster-status-full
```

### Broker 노드 확인

Broker 노드에 이상이 있으면 클라이언트 연결 전체가 영향을 받습니다.

```bash
# Broker 상태 확인
machcoordinatoradmin --cluster-status-full | grep -i broker
```

Broker가 응답하지 않으면 해당 Broker 호스트에서 프로세스를 확인하고 재기동합니다.

### Coordinator 상태 확인

Coordinator가 비정상이면 클러스터 메타 변경 및 장애 조치가 불가합니다.

```bash
# Coordinator 상태 확인
machcoordinatoradmin --cluster-status-full
```

Primary Coordinator에 장애가 발생했고 Secondary Coordinator가 구성되어 있다면, Secondary가 자동으로 Primary로 승격됩니다. Secondary가 없다면 Primary를 수동으로 재기동해야 합니다.

### 노드 트레이스 로그 확인

오류 원인을 상세히 파악하려면 해당 노드의 트레이스 로그를 확인합니다.

```bash
# 해당 노드 로그 확인
grep -i "error\|fatal\|assert" $MACHBASE_HOME/trc/machbase.trc | tail -50
```

### 상세 복구 절차

Warehouse 노드의 데이터 손상(`scrapped` 상태) 복구, Snapshot 활용, 강제 복구 방법에 대한 상세 내용은 다음을 참고하십시오.

- [Warehouse 상태 복구](../../../operations-configuration-recovery/cluster/recovery-state-status-warehouse/)
- [Cluster 노드 상태와 전환](../../../operations-configuration-recovery/cluster/state-alter-status-cluster/)

<a id="error-cluster-edition"></a>

## Cluster Edition 제한 오류

Machbase Cluster Edition은 Standard Edition의 일부 기능을 지원하지 않습니다. 미지원 기능을 사용하려 하면 오류가 발생합니다. 이 페이지는 주요 제한 기능별 오류 메시지와 대안을 안내합니다.

Cluster Edition의 전반적인 제한사항에 대한 상세 내용은 [Cluster 운영 제한사항](../../../operations-configuration-recovery/cluster/limitations-cluster/)을 참고하십시오.

### 에디션 확인

현재 접속된 서버가 Cluster Edition인지 확인합니다.

```sql
SELECT * FROM v$version;
```

`EDITION` 항목이 `CLUSTER`이면 이 페이지의 제한사항이 적용됩니다.

### 주요 제한 기능과 오류

| 기능 | 오류 메시지 예시 | 대안 |
|------|----------------|------|
| RDB 테이블 생성/사용 | `RDB table is not supported in Cluster Edition` | LOOKUP 테이블 사용 |
| Custom ROLLUP | `Custom rollup is not supported in Cluster Edition` | 기본 자동 ROLLUP 사용 |
| ROLLUP_REBUILD | `ROLLUP_REBUILD is not supported in Cluster Edition` | 해당 기능 없음 (지원 문의) |
| MOUNT DATABASE | `MOUNT is not supported in Cluster Edition` | Standard Edition에서 마운트 후 데이터 추출 |
| UNMOUNT DATABASE | `UNMOUNT is not supported in Cluster Edition` | 해당 기능 없음 |
| STREAM | `STREAM is not supported in Cluster Edition` | CQL 또는 외부 파이프라인 검토 |

### 기능별 상세 안내

#### RDB 테이블

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

#### ROLLUP_REBUILD

ROLLUP 재계산 명령은 Cluster Edition에서 실행되지 않습니다.

```sql
-- 오류 발생: Cluster Edition에서 ROLLUP_REBUILD
EXEC ROLLUP_REBUILD(sensor_tag, rollup_1min, TO_DATE('2024-01-01'), TO_DATE('2024-01-02'));
-- ERR: ROLLUP_REBUILD is not supported in Cluster Edition
```

**대안**: Cluster Edition에서는 ROLLUP 재계산 기능이 없습니다. ROLLUP 데이터 불일치가 발생하면 기술 지원에 문의하십시오.

#### MOUNT/UNMOUNT DATABASE

Cluster Edition에서는 백업 데이터베이스 마운트가 지원되지 않습니다.

```sql
-- 오류 발생: Cluster Edition에서 MOUNT
MOUNT DATABASE '/backup/machbase_20240101' TO backup_db;
-- ERR: MOUNT is not supported in Cluster Edition
```

**대안**: Standard Edition 환경에서 마운트하여 필요한 데이터를 추출한 후 Cluster Edition으로 적재합니다.

#### STREAM

STREAM 기능은 Cluster Edition에서 제한됩니다.

```sql
-- 오류 발생: Cluster Edition에서 STREAM 생성
EXEC STREAM_CREATE(my_stream, 'INSERT INTO dest SELECT * FROM source;');
-- ERR: STREAM is not supported in Cluster Edition
```

**대안**: CQL(Continuous Query Language) 또는 외부 데이터 파이프라인(Kafka, Flink 등)을 이용한 데이터 흐름 구성을 검토합니다.

### Standard Edition 전환 검토

위 기능들이 운영에 필수적이라면 Standard Edition으로의 전환 또는 혼합 운영 구조를 검토합니다. 에디션 선택 기준에 대한 내용은 Machbase 기술 지원에 문의하십시오.
