---
type: docs
title: '14.11 Cluster 운영'
weight: 110
toc: true
---
Cluster Edition은 대규모 시계열 데이터를 여러 노드에 분산 저장·처리하는 아키텍처입니다. 클러스터 구성 요소의 역할, 운영 도구, 장애 복구 절차를 다룹니다.

## 클러스터 노드 구성

| 노드 유형 | 역할 | 비고 |
|-----------|------|------|
| **Coordinator** | 클러스터 전체 메타데이터·토폴로지 관리, 노드 상태 감시 | 클러스터당 1~2개 (Primary/Secondary) |
| **Deployer** | 패키지 배포, 노드 설치·업그레이드 자동화 | 호스트당 1개 |
| **Broker** | 클라이언트 연결 수신, 쿼리 라우팅 | 1개 이상 (HA 시 복수) |
| **Warehouse** | 실제 데이터 저장·처리 노드 | 그룹 단위로 복수 배치 |
| **Lookup** | 참조 데이터(룩업 테이블) 저장 | 선택적 구성 |

## 주요 운영 도구

| 도구 | 설명 |
|------|------|
| `machclusterctl` | 클러스터 전체를 대상으로 한 통합 시작·종료·상태 확인 CLI |
| `machcoordinatoradmin` | Coordinator 및 개별 노드 세부 관리 CLI |
| `machadmin` | 개별 Warehouse/Broker 노드의 프로세스 관리 |

## 이 섹션의 구성

| 주제 | 내용 |
|------|------|
| [Cluster 상태 확인](/dbms/operations-configuration-recovery/cluster/#status-check-state-cluster) | 전체 클러스터 상태 및 노드별 상태 조회 |
| [machclusterctl connect/export](/dbms/operations-configuration-recovery/cluster/#machclusterctl-connect-export) | 클러스터 접속 및 설정 내보내기 |
| [Cluster 노드 시작과 종료](/dbms/operations-configuration-recovery/cluster/#node-start-cluster) | 개별 노드 기동·종료 절차 |
| [machclusterctl start/stop/destroy](/dbms/operations-configuration-recovery/cluster/#machclusterctl-start-stop-destroy) | 클러스터 전체 시작·종료·삭제 |
| [Cluster 노드 추가와 제거](/dbms/operations-configuration-recovery/cluster/#node-cluster) | 운영 중 노드 확장·축소 |
| [Cluster 그룹 상태 변경](/dbms/operations-configuration-recovery/cluster/#state-alter-status-cluster) | 유지보수 모드 전환, 그룹 상태 변경 |
| [Warehouse 상태 복구](/dbms/operations-configuration-recovery/cluster/#recovery-state-status-warehouse) | Warehouse 노드 장애 복구 절차 |
| [Cluster 운영 제한사항](/dbms/operations-configuration-recovery/cluster/#limitations-cluster) | 단일 에디션 대비 제한 기능 목록 |

## Cluster Edition 전용 제약사항

Cluster Edition에서는 다음 기능이 지원되지 않습니다.

- **TRANSACTION 테이블** 미지원
- **Custom ROLLUP** 미지원
- **ROLLUP_REBUILD** 미지원
- `MOUNT`/`UMOUNT`, Stream/CQL 등 일부 Standard Edition 기능 제한
- 일부 `ALTER TABLE` 기능 제한

자세한 내용은 [Cluster 운영 제한사항](/dbms/operations-configuration-recovery/cluster/#limitations-cluster)을 참조하십시오.


<a id="status-check-state-cluster"></a>

## Cluster 상태 확인

클러스터 상태를 정기적으로 확인하여 모든 노드가 정상 동작 중인지 점검합니다.

### machcoordinatoradmin으로 상태 확인

#### 기본 상태 출력

```bash
machcoordinatoradmin --cluster-status
```

출력 예:

```
+-------------+-------------------+-------------------+-------------------+--------------+
|  Node Type  |     Node Name     |    Group Name     |    Group State    |     State    |
+-------------+-------------------+-------------------+-------------------+--------------+
| coordinator | 192.168.0.32:5101 | Coordinator       | normal            | primary      |
| deployer    | 192.168.0.32:5201 | Deployer          | normal            | normal       |
| broker      | 192.168.0.32:5301 | Broker            | normal            | leader       |
| warehouse   | 192.168.0.32:5401 | Group1            | normal            | normal       |
+-------------+-------------------+-------------------+-------------------+--------------+
```

#### 상세 상태 출력 (Desired vs Actual State)

```bash
machcoordinatoradmin --cluster-status-full
```

`Desired State`와 `Actual State`를 함께 표시합니다. 두 값이 다른 노드는 상태 전환 중이거나 문제가 있는 노드입니다.

#### Deployer 상태 포함 출력

```bash
machcoordinatoradmin --cluster-status --verbose
```

#### 클러스터 전체 정보 출력

```bash
machcoordinatoradmin --cluster-node
```

출력 예:

```
Token Pid      : 29245
Token Time     : 1553153902646178
Cluster Status : Service
Broker         : 192.168.0.32:5301
Warehouse      : 192.168.0.32:5401
```

`Cluster Status`가 `Service`이면 클러스터가 정상 서비스 중입니다.

### SQL로 노드 상태 확인

machsql 또는 애플리케이션에서 SQL로 노드 상태를 조회할 수 있습니다.

#### 노드 상태 조회

```sql
-- 전체 클러스터 노드 상태
SELECT * FROM v$cluster_node_status;

-- Warehouse 노드 상태
SELECT * FROM v$warehouse_node_status;
```

### 노드 상태 값

| 상태 | 의미 |
|------|------|
| `normal` | 정상 동작 중 |
| `primary` | Coordinator Primary 상태 |
| `leader` | Broker Leader 상태 |
| `readonly` | 읽기 전용 상태 (그룹 상태) |
| `sync-standby` | 동기화 대기 상태 |
| `sync-active` | 동기화 진행 상태 |
| `scrapped` | 데이터 손상 또는 복구 필요 상태 |
| `inactive` | 비활성 상태 |
| `**unknown**` | 상태 미확인 또는 연결 불가 |
| `ddl-recovering` | DDL 복구 중 |

### 클러스터 상태 값 (Cluster Status)

| 상태 | 의미 |
|------|------|
| `Service` | 정상 서비스 중 |
| `Deactivate` | 비활성화 상태 |

### 호스트 리소스 모니터링

클러스터 노드가 위치한 호스트의 CPU·메모리·디스크·네트워크 사용량을 확인할 수 있습니다.

```bash
# 리소스 수집 활성화
machcoordinatoradmin --host-resource-enable

# 전체 호스트 리소스 확인
machcoordinatoradmin --get-host-resource

# 특정 메트릭만 확인
machcoordinatoradmin --get-host-resource --metric=cpu
machcoordinatoradmin --get-host-resource --metric=disk

# 특정 호스트만 확인
machcoordinatoradmin --get-host-resource --host=192.168.0.32

# 리소스 수집 비활성화
machcoordinatoradmin --host-resource-disable
```

### 정기 상태 확인 스크립트 예

```bash
#!/bin/bash
# 클러스터 상태 확인 후 비정상 노드 감지

OUTPUT=$(machcoordinatoradmin --cluster-status 2>&1)
echo "$OUTPUT"

# unknown 또는 scrapped 상태 노드 감지
if echo "$OUTPUT" | grep -qE '\\*\\*unknown\\*\\*|scrapped'; then
  echo "[경고] 비정상 노드가 감지되었습니다. 즉시 확인하십시오."
fi
```

<a id="machclusterctl-connect-export"></a>

## machclusterctl connect/export

`machclusterctl`은 클러스터 전체 기동·종료 외에 클러스터 접속과 설정 내보내기 기능을 제공합니다.

### 클러스터 접속

```bash
machclusterctl connect broker-1
```

지정한 Broker 또는 Warehouse alias를 통해 machsql 클라이언트로 클러스터에 접속합니다. alias는 클러스터 YAML 또는 Coordinator 메타에 등록된 이름을 사용합니다.

접속 후 일반 machsql과 동일하게 SQL을 실행할 수 있습니다.

```sql
Mach> SELECT COUNT(*) FROM my_table;
Mach> SELECT * FROM v$cluster_node_status;
Mach> EXIT
```

특정 Broker로 직접 접속하려면 해당 Broker alias를 지정하거나 machsql을 직접 사용합니다.

```bash
# 특정 Broker alias로 접속
machclusterctl connect broker-2

# 호스트와 서비스 포트를 직접 지정해 접속
machsql -s <broker_host> -P <service_port>
```

### 클러스터 설정 내보내기

```bash
machclusterctl export -o cluster_config.yaml
```

현재 클러스터 구성 정보를 YAML 파일로 내보냅니다. 내보낸 파일에는 다음 정보가 포함됩니다.

- 각 노드의 호스트·포트 정보
- 노드 유형 (coordinator, deployer, broker, warehouse, lookup)
- 그룹 구성
- 패키지·홈 경로 정보

#### 활용 예

- **문서화**: 현재 클러스터 구성을 기록으로 남길 때
- **재구성 참조**: 클러스터를 재구성하거나 유사한 환경을 구성할 때 참조 파일로 활용
- **백업**: 클러스터 메타 정보 변경 전 현재 상태를 저장

출력 파일 예:

```yaml
version: "1"
cluster:
  coordinators:
    - alias: coordinator-1
      host: 192.168.0.32
      cluster_link_port: 5101
      http_admin_port: 5102
      home_path: /home/machbase/coordinator-1
  deployers:
    - alias: deployer-1
      host: 192.168.0.32
      cluster_link_port: 5201
      http_admin_port: 5202
      home_path: /home/machbase/deployer-1
  brokers:
    - alias: broker-1
      host: 192.168.0.32
      deployer: deployer-1
      cluster_link_port: 5301
      http_port_no: 5302
      service_port: 5757
      home_path: /home/machbase/broker-1
  warehouse_groups:
    - name: Group1
      nodes:
        - alias: warehouse-group1-1
          host: 192.168.0.32
          deployer: deployer-1
          cluster_link_port: 5401
          service_port: 5656
          home_path: /home/machbase/warehouse-group1-1
          dbs_path: /home/machbase/warehouse-group1-1/dbs
```

> YAML 기반 구성 변경은 `machclusterctl apply -f <파일>` 흐름을 사용합니다. 개별 노드의 세부 운영이 필요한 경우에만 `machcoordinatoradmin`을 사용합니다.

<a id="node-start-cluster"></a>

## Cluster 노드 시작과 종료

클러스터 전체를 재시작하지 않고 특정 노드만 시작하거나 종료해야 하는 경우 `machcoordinatoradmin`을 사용합니다. 개별 노드 제어는 유지보수, 장애 복구, 롤링 업그레이드 시 활용합니다.

### Coordinator를 통한 노드 제어

Coordinator가 실행 중인 상태에서 `machcoordinatoradmin`으로 개별 노드를 원격 제어합니다.

#### 노드 시작

```bash
# 특정 노드 시작 (노드 이름 또는 alias 사용 가능)
machcoordinatoradmin --startup-node=192.168.0.32:5401

# alias 사용
machcoordinatoradmin --startup-node=warehouse-a1
```

#### 노드 종료

```bash
# 특정 노드 정상 종료
machcoordinatoradmin --shutdown-node=192.168.0.32:5401

# 특정 노드 강제 종료 (응답 없을 때)
machcoordinatoradmin --kill-node=192.168.0.32:5401
```

#### Lookup 노드 시작·종료

```bash
# Lookup 노드 전체 시작
machcoordinatoradmin --startup-lookup

# Lookup 노드 전체 종료
machcoordinatoradmin --shutdown-lookup
```

### 노드 직접 제어 (machadmin)

Coordinator와 통신할 수 없는 상황이거나 해당 호스트에 직접 접속한 경우, 각 노드에서 `machadmin`으로 직접 제어합니다.

#### Warehouse 노드

```bash
# Warehouse 노드가 설치된 호스트에서 직접 실행
export MACHBASE_HOME=/home/machbase/warehouse_a1
machadmin -u    # 시작
machadmin -s    # 종료
machadmin -e    # 실행 여부 확인
```

#### Broker 노드

```bash
export MACHBASE_HOME=/home/machbase/broker1
machadmin -u    # 시작
machadmin -s    # 종료
```

#### Coordinator 노드

```bash
export MACHBASE_HOME=/home/machbase/coordinator1
machcoordinatoradmin -u    # 시작 (-u, --startup)
machcoordinatoradmin -s    # 종료 (-s, --shutdown)
machcoordinatoradmin -e    # 실행 여부 확인
```

### 노드 제어 시 권장 순서

#### 특정 노드만 재시작

```bash
# 1. 노드 종료
machcoordinatoradmin --shutdown-node=warehouse-a1

# 2. 클러스터 상태 확인 (inactive 또는 **unknown** 상태 확인)
machcoordinatoradmin --cluster-status

# 3. 노드 시작
machcoordinatoradmin --startup-node=warehouse-a1

# 4. 클러스터 상태 확인 (normal 상태로 복귀 확인)
machcoordinatoradmin --cluster-status
```

#### Broker 교체

```bash
# 1. 기존 Broker 비활성화 (클라이언트 연결 차단)
machcoordinatoradmin --deactivate-broker=192.168.0.32:5301

# 2. 기존 Broker 종료
machcoordinatoradmin --shutdown-node=192.168.0.32:5301

# 3. 유지보수 작업 수행

# 4. Broker 시작
machcoordinatoradmin --startup-node=192.168.0.32:5301

# 5. Broker 활성화
machcoordinatoradmin --activate-broker=192.168.0.32:5301
```

### 주의사항

- **Coordinator 종료 시**: Coordinator가 종료되면 클러스터 메타 변경이 불가합니다. Coordinator 종료 전에 클러스터 상태가 안정적인지 확인합니다.
- **단일 Broker 환경**: Broker가 하나만 있는 경우 Broker를 종료하면 클라이언트가 접속할 수 없습니다. HA 구성을 권장합니다.
- **Warehouse 종료 시**: 해당 그룹의 다른 Warehouse 노드가 정상 동작 중인지 확인한 후 종료합니다.

<a id="machclusterctl-start-stop-destroy"></a>

## machclusterctl start/stop/destroy

`machclusterctl`은 Machbase Cluster Edition 전용 통합 CLI입니다. 클러스터 전체를 대상으로 시작·종료·삭제를 한 번에 처리합니다.

### 클러스터 전체 시작

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

### 클러스터 전체 종료

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

### 클러스터 완전 삭제

```bash
machclusterctl destroy
```

> **주의:** 이 명령은 클러스터 메타데이터와 데이터베이스 파일을 **영구적으로 삭제**합니다. 실행 전 반드시 데이터 백업 여부를 확인하십시오.

클러스터에 등록된 모든 노드의 프로세스를 종료하고 데이터베이스 파일, 설정 파일, 메타 정보를 삭제합니다. 클러스터를 완전히 초기화하고 새로 구성할 때 사용합니다.

### 시작/종료 시 주의사항

- **개별 노드가 이미 실행 중인 경우**: `machclusterctl start`는 이미 실행 중인 노드를 건너뜁니다.
- **네트워크 단절 상태에서 시작**: 특정 노드에 도달할 수 없는 경우 해당 노드 시작이 실패하고 전체 시작이 중단될 수 있습니다.
- **대규모 클러스터**: 노드 수가 많을수록 `start`/`stop` 완료까지 시간이 걸립니다. 완료 메시지가 출력될 때까지 기다립니다.

### 개별 노드 제어

클러스터 전체가 아닌 특정 노드만 시작·종료하려면 `machclusterctl`의 `--node` 옵션에 노드 alias를 지정합니다. `machcoordinatoradmin`은 저수준 수동 운영이 필요한 경우에만 사용합니다.

```bash
# 특정 노드 시작
machclusterctl start --node=warehouse-group1-1

# 특정 노드 종료
machclusterctl stop --node=warehouse-group1-1
```

자세한 내용은 [Cluster 노드 시작과 종료](/dbms/operations-configuration-recovery/cluster/#node-start-cluster)를 참조하십시오.

<a id="node-cluster"></a>

## Cluster 노드 추가와 제거

운영 중인 클러스터에 노드를 추가하거나 제거하는 절차입니다. 노드 추가는 `machcoordinatoradmin --add-node` 명령으로, 제거는 `--remove-node` 명령으로 수행합니다.

### Warehouse 노드 추가

새 Warehouse 노드를 클러스터에 추가하는 절차입니다.

#### 1. 준비

- 추가할 호스트에 Machbase 패키지가 Deployer를 통해 배포 가능한 상태여야 합니다.
- Coordinator에 해당 패키지가 등록되어 있어야 합니다.

```bash
# 패키지 등록 확인
machcoordinatoradmin --list-package

# 패키지가 없는 경우 추가
machcoordinatoradmin --add-package=machbase --file-name=machbase-cluster-<version>-LINUX-X86-64-release.tgz
```

#### 2. 노드 추가

```bash
machcoordinatoradmin \
  --add-node=192.168.0.33:5401 \
  --node-type=warehouse \
  --deployer=192.168.0.33:5201 \
  --package-name=machbase \
  --home-path=/home/machbase/warehouse_b1 \
  --port-no=5400 \
  --http-port-no=5402 \
  --group=Group2 \
  --alias=warehouse-b1 \
  --dbs-path=/data/machbase/warehouse_b1_dbs
```

| 옵션 | 설명 |
|------|------|
| `--add-node` | 추가할 노드의 클러스터 링크 주소 (`호스트:포트`) |
| `--node-type` | `warehouse`, `broker`, `lookup` 중 선택 |
| `--deployer` | 해당 호스트의 Deployer 주소 |
| `--package-name` | Coordinator에 등록된 패키지 이름 |
| `--home-path` | Deployer 기준 설치 경로 |
| `--port-no` | Machbase 서비스 포트 |
| `--group` | 배치할 그룹 이름 |
| `--alias` | 노드 별칭 (선택) |
| `--dbs-path` | 데이터베이스 파일 저장 경로 (선택, 기본값: `?/dbs`) |

#### 3. 노드 시작

```bash
machcoordinatoradmin --startup-node=warehouse-b1
```

#### 4. 상태 확인

```bash
machcoordinatoradmin --cluster-status
```

새 노드가 `normal` 상태로 표시되면 추가가 완료된 것입니다.

### 기존 노드 연결 (attach-node)

이미 설치된 노드를 클러스터 메타에 연결할 때는 `--attach-node`를 사용합니다. `--add-node`와 달리 패키지 배포 없이 메타 등록만 수행합니다.

```bash
machcoordinatoradmin \
  --attach-node=192.168.0.33:5401 \
  --node-type=warehouse \
  --home-path=/home/machbase/warehouse_b1 \
  --port-no=5400 \
  --http-port-no=5402 \
  --group=Group2 \
  --alias=warehouse-b1
```

> `--attach-node`에서는 `--dbs-path`를 사용할 수 없습니다.

### Lookup 노드 추가

```bash
machcoordinatoradmin \
  --add-node=192.168.0.33:5601 \
  --node-type=lookup \
  --lookup-type=master \
  --deployer=192.168.0.33:5201 \
  --package-name=machbase \
  --home-path=/home/machbase/lookup1 \
  --alias=lookup-master-1
```

Lookup 노드 추가 후 마스터를 지정합니다.

```bash
machcoordinatoradmin --set-lookup-master=lookup-master-1
```

### 노드 제거

노드를 클러스터에서 완전히 제거합니다.

#### 1. 노드 종료

```bash
machcoordinatoradmin --shutdown-node=warehouse-b1
```

#### 2. 노드 분리 (선택)

제거 전 데이터 재분산이 필요한 경우, 노드를 클러스터 메타에서 분리하고 수동으로 데이터를 처리합니다.

```bash
machcoordinatoradmin --detach-node=warehouse-b1
```

#### 3. 노드 제거

```bash
machcoordinatoradmin --remove-node=warehouse-b1
```

`--remove-node`는 클러스터 메타에서 노드를 삭제하고 해당 노드의 Machbase 홈 디렉터리와 데이터베이스 파일을 삭제합니다. 별도로 지정된 절대 경로의 `DBS_PATH`도 정리됩니다.

### 주의사항

- 그룹 내 마지막 Warehouse 노드는 제거하지 않는 것이 원칙입니다. 해당 그룹의 데이터에 접근할 수 없게 됩니다.
- 노드 추가 시 `--dbs-path`로 지정한 디렉터리는 추가 시점에 존재하지 않아야 합니다. 이미 존재하면 `DBS_PATH already exists` 오류가 발생합니다.
- `/`, `/etc`, `/usr`, `/home`, `/bin` 같은 시스템 경로 자체는 `--dbs-path`로 지정할 수 없습니다.

<a id="state-alter-status-cluster"></a>

## Cluster 그룹 상태 변경

클러스터 운영 중 유지보수, 장애 대응, 데이터 보호를 위해 노드 그룹 또는 개별 노드의 상태를 수동으로 변경할 수 있습니다.

### 클러스터 활성화/비활성화

클러스터 전체를 서비스 상태(`Service`)로 전환하거나 비활성화(`Deactivate`) 상태로 전환합니다.

```bash
# 클러스터 활성화 (Service 상태로 전환)
machcoordinatoradmin --activate

# 클러스터 비활성화 (Deactivate 상태로 전환)
machcoordinatoradmin --deactivate
```

비활성화 상태에서는 클라이언트의 데이터 쓰기가 차단됩니다. 대규모 유지보수나 클러스터 설정 변경 전에 비활성화 상태로 전환합니다.

### Warehouse 그룹 상태 변경

Warehouse 그룹 전체를 `normal` 또는 `readonly` 상태로 변경합니다.

```bash
# 그룹을 읽기 전용으로 전환
machcoordinatoradmin --set-group-state=readonly --group=Group1

# 그룹을 정상 상태로 복원
machcoordinatoradmin --set-group-state=normal --group=Group1
```

상태 변경 후 `--cluster-status`로 확인합니다.

```
+-------------+-------------------+-------------------+-------------------+--------------+
|  Node Type  |     Node Name     |    Group Name     |    Group State    |     State    |
+-------------+-------------------+-------------------+-------------------+--------------+
| warehouse   | 192.168.0.32:5401 | Group1            | readonly          | normal       |
+-------------+-------------------+-------------------+-------------------+--------------+
```

**readonly 상태 활용 사례:**
- 그룹 내 노드 유지보수 전 쓰기 차단
- 데이터 일관성 검증 중 변경 방지
- 특정 그룹의 데이터를 보존해야 하는 상황

### Warehouse 개별 노드 상태 변경

특정 Warehouse 노드의 상태를 `normal` 또는 `scrapped`로 변경합니다.

```bash
# 노드를 scrapped 상태로 변경 (데이터 손상·복구 필요 표시)
machcoordinatoradmin --set-warehouse-state=scrapped --node=warehouse-a1

# 노드를 정상 상태로 복원
machcoordinatoradmin --set-warehouse-state=normal --node=warehouse-a1
```

`scrapped` 상태는 해당 노드의 데이터를 신뢰할 수 없는 경우 또는 강제 복구가 필요한 경우에 사용합니다.

### Broker 활성화/비활성화

특정 Broker 노드를 비활성화하여 새 클라이언트 연결을 차단합니다. 롤링 업그레이드나 Broker 교체 시 사용합니다.

```bash
# Broker 비활성화 (새 연결 차단)
machcoordinatoradmin --deactivate-broker=192.168.0.32:5301

# Broker 활성화 (연결 허용)
machcoordinatoradmin --activate-broker=192.168.0.32:5301
```

비활성화된 Broker는 기존 연결을 유지하지만 새 연결을 받지 않습니다. 기존 연결이 모두 종료된 후 Broker를 안전하게 종료할 수 있습니다.

### 유지보수 절차 예

그룹 전체 유지보수가 필요한 경우의 표준 절차입니다.

```bash
# 1. 그룹 읽기 전용 전환 (쓰기 차단)
machcoordinatoradmin --set-group-state=readonly --group=Group1

# 2. 상태 확인
machcoordinatoradmin --cluster-status

# 3. 유지보수 작업 수행 (노드 재시작, 패키지 업그레이드 등)

# 4. 유지보수 완료 후 정상 상태로 복원
machcoordinatoradmin --set-group-state=normal --group=Group1

# 5. 상태 확인
machcoordinatoradmin --cluster-status
```

<a id="recovery-state-status-warehouse"></a>

## Warehouse 상태 복구

Warehouse 노드에 장애가 발생하면 해당 노드의 상태가 `scrapped`, `inactive`, `**unknown**` 등으로 전환될 수 있습니다. 장애 유형에 따라 자동 복구 또는 수동 복구를 수행합니다.

### 장애 유형과 복구 방법

| 장애 유형 | 증상 | 복구 방법 |
|-----------|------|-----------|
| 일시적 네트워크 단절 | `**unknown**` 또는 `inactive` | 네트워크 복구 후 자동 재연결 |
| 프로세스 비정상 종료 | `**unknown**` 또는 `inactive` | 노드 재시작 |
| 데이터 손상 | scrapped | Snapshot 복구 또는 강제 복구 |
| 디스크 장애 | scrapped | 디스크 교체 후 데이터 복구 |

### 자동 복구

네트워크 단절이나 일시적 프로세스 오류의 경우, Coordinator가 자동으로 노드 재연결을 시도합니다. `CLUSTER_LINK_CONNECT_RETRY_TIMEOUT` 설정 내에 연결이 복구되면 자동으로 `normal` 상태로 전환됩니다.

```bash
# 복구 진행 확인
machcoordinatoradmin --cluster-status
```

`sync-standby`, `sync-active`, `ddl-recovering` 등의 전환 상태가 `normal` 상태로 돌아올 때까지 대기합니다.

### 수동 복구: 노드 재시작

프로세스가 종료된 경우 해당 노드를 재시작합니다.

```bash
# 1. 장애 노드 상태 확인
machcoordinatoradmin --cluster-status

# 2. 노드 시작 (Coordinator가 접근 가능한 경우)
machcoordinatoradmin --startup-node=warehouse-a1

# 3. 또는 해당 호스트에 직접 접속하여 시작
export MACHBASE_HOME=/home/machbase/warehouse_a1
machadmin -u

# 4. 상태 복귀 확인
machcoordinatoradmin --cluster-status
```

### Snapshot 복구

데이터 손상으로 노드가 `scrapped` 상태인 경우 Snapshot 기능으로 복구합니다.

#### Snapshot 실행 (사전 준비)

정기적으로 Snapshot을 실행해 복구 포인트를 만들어 두어야 합니다.

```bash
# Snapshot 주기 설정 (초 단위)
machcoordinatoradmin --snapshot-interval=3600

# 즉시 Snapshot 실행
machcoordinatoradmin --exec-snapshot --group=Group1
```

#### Snapshot으로 복구

```bash
# scrapped 노드를 Snapshot 기반으로 복구
machcoordinatoradmin --snapshot-recover=warehouse-a1
```

#### Snapshot 정리

오래된 Snapshot을 정리하여 디스크 공간을 확보합니다.

```bash
machcoordinatoradmin --snapshot-clean
```

### Sync 복구

다른 노드와 데이터를 동기화하여 복구합니다.

```bash
# 지정 노드에 Sync 실행 (다른 노드로부터 데이터 동기화)
machcoordinatoradmin --exec-sync=warehouse-a1
```

### 강제 복구

Snapshot이 없거나 Sync가 불가능한 경우, `scrapped` 상태의 노드를 강제로 복구합니다. 단, 강제 복구 후 해당 노드의 데이터 일관성은 보장되지 않습니다.

```bash
# scrapped 노드 강제 복구
machcoordinatoradmin --force-restore-warehouse=warehouse-a1
```

강제 복구 후 반드시 데이터 일관성을 검증합니다.

### 복구 후 확인

```bash
# 전체 클러스터 상태 확인
machcoordinatoradmin --cluster-status

# 특정 노드 상세 정보
machcoordinatoradmin --list-node=warehouse-a1
```

복구된 노드의 `Actual State`가 `normal`로 표시되고 `Desired State`와 일치하면 복구가 완료된 것입니다.

### 복구 불가 시 조치

복구가 불가능한 경우 해당 노드를 클러스터에서 제거하고 새 노드로 교체합니다.

```bash
# 1. 노드 제거
machcoordinatoradmin --remove-node=warehouse-a1

# 2. 새 노드 추가
machcoordinatoradmin \
  --add-node=192.168.0.32:5401 \
  --node-type=warehouse \
  --deployer=192.168.0.32:5201 \
  --package-name=machbase \
  --home-path=/home/machbase/warehouse_a1 \
  --port-no=5400 \
  --group=Group1 \
  --alias=warehouse-a1

# 3. 노드 시작
machcoordinatoradmin --startup-node=warehouse-a1
```

노드 교체 이후 데이터 재분산이 필요한지 확인하고, 필요하다면 `--exec-sync`로 동기화합니다.

<a id="limitations-cluster"></a>

## Cluster 운영 제한사항

Machbase Cluster Edition은 단일 노드(Standard/Edge Edition) 대비 일부 기능이 지원되지 않거나 동작 방식이 다릅니다. 클러스터 환경으로 마이그레이션하기 전에 반드시 확인합니다.

### 테이블 유형 제한

| 테이블 유형 | Standard Edition | Cluster Edition |
|-------------|:---:|:---:|
| Log 테이블 | 지원 | 지원 |
| Tag 테이블 | 지원 | 지원 |
| Volatile 테이블 | 지원 | 지원 |
| Lookup 테이블 | 지원 | 지원 (Lookup 노드 필요) |
| **TRANSACTION 테이블** | 지원 | **미지원** |

TRANSACTION 테이블을 사용하는 애플리케이션은 Cluster Edition으로 이전할 때 대체 방안을 마련해야 합니다.

### ROLLUP 관련 제한

| 기능 | Standard Edition | Cluster Edition |
|------|:---:|:---:|
| 자동 ROLLUP | 지원 | 지원 |
| **Custom ROLLUP** | 지원 | **미지원** |
| **ROLLUP_REBUILD** | 지원 | **미지원** |

Cluster Edition에서는 시스템이 자동으로 관리하는 ROLLUP만 사용할 수 있습니다. 사용자 정의 ROLLUP 함수나 ROLLUP 재구성 명령은 실행 시 오류가 발생합니다.

### DDL 및 ALTER TABLE 제한

Cluster Edition에서는 일부 `ALTER TABLE` 명령이 제한됩니다.

- **파티션 추가/삭제** 일부 제한
- **인덱스 변경** 중 데이터 쓰기 일시 차단 가능
- **컬럼 추가/삭제** 클러스터 전체 동기화 필요

ALTER TABLE 실행 전 반드시 테스트 환경에서 검증합니다.

### 백업, 마운트, Stream 제한

Cluster Edition에서는 일부 Standard Edition SQL 기능이 제한되거나 거부될 수 있습니다.

| 기능 | Cluster Edition 참고 |
|------|----------------------|
| `BACKUP DATABASE`, `BACKUP TABLE` | 클러스터 구성과 운영 절차에 따라 제한될 수 있음 |
| `MOUNT DATABASE`, `UMOUNT DATABASE` | 거부될 수 있음 |
| Stream/CQL 문 | Standard Edition 중심 기능으로, Cluster Edition에서 거부될 수 있음 |

### 고가용성 제한

#### 단일 Broker 구성

Broker가 하나만 있는 경우 해당 Broker에 장애가 발생하면 모든 클라이언트 연결이 차단됩니다. 운영 환경에서는 Broker를 2개 이상 구성하는 HA 구성을 강력히 권장합니다.

#### 단일 Coordinator 구성

Primary Coordinator에 장애가 발생하면 클러스터 메타 변경이 불가합니다. Secondary Coordinator를 함께 구성하면 자동 페일오버가 가능합니다.

### 쿼리 실행 제한

| 기능 | 비고 |
|------|------|
| 크로스-그룹 조인 | 그룹 간 대용량 조인 시 성능 저하 가능 |
| 서브쿼리 분산 처리 | 일부 복잡한 서브쿼리는 단일 노드에서 처리 |
| 전체 정렬(ORDER BY) | 대용량 데이터 정렬 시 Broker 메모리 소비 증가 |

### 운영 도구 제한

일부 `machadmin` 옵션은 Cluster Edition에서 직접 사용하지 않습니다. 개별 노드에서 `machadmin`을 직접 실행하는 대신 `machcoordinatoradmin`을 통해 클러스터 전체를 관리합니다.

### 버전 혼재 제한

클러스터 내 모든 노드는 동일한 Machbase 버전을 사용해야 합니다. 버전이 다른 노드가 혼재하면 클러스터가 정상적으로 동작하지 않을 수 있습니다. 업그레이드 시 롤링 업그레이드 절차를 따릅니다.

### 제한사항 요약

| 항목 | 제한 내용 |
|------|-----------|
| TRANSACTION 테이블 | 미지원 |
| Custom ROLLUP | 미지원 |
| ROLLUP_REBUILD | 미지원 |
| MOUNT/UMOUNT | 제한 또는 거부 가능 |
| Stream/CQL | 제한 또는 거부 가능 |
| 일부 ALTER TABLE | 제한 또는 동작 차이 |
| 단일 Broker | HA 미구성 시 단일 장애점(SPOF) |
| 단일 Coordinator | Secondary 미구성 시 단일 장애점(SPOF) |
| 버전 혼재 | 미지원 (동일 버전 필수) |
