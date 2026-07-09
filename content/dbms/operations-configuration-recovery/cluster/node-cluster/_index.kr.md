---
type: docs
title: '13.7.5 Cluster 노드 추가와 제거'
weight: 50
---

운영 중인 클러스터에 노드를 추가하거나 제거하는 절차입니다. 노드 추가는 `machcoordinatoradmin --add-node` 명령으로, 제거는 `--remove-node` 명령으로 수행합니다.

## Warehouse 노드 추가

새 Warehouse 노드를 클러스터에 추가하는 절차입니다.

### 1. 준비

- 추가할 호스트에 Machbase 패키지가 Deployer를 통해 배포 가능한 상태여야 합니다.
- Coordinator에 해당 패키지가 등록되어 있어야 합니다.

```bash
# 패키지 등록 확인
machcoordinatoradmin --list-package

# 패키지가 없는 경우 추가
machcoordinatoradmin --add-package=machbase --file-name=machbase-cluster-<version>-LINUX-X86-64-release.tgz
```

### 2. 노드 추가

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

### 3. 노드 시작

```bash
machcoordinatoradmin --startup-node=warehouse-b1
```

### 4. 상태 확인

```bash
machcoordinatoradmin --cluster-status
```

새 노드가 `normal` 상태로 표시되면 추가가 완료된 것입니다.

## 기존 노드 연결 (attach-node)

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

## Lookup 노드 추가

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

## 노드 제거

노드를 클러스터에서 완전히 제거합니다.

### 1. 노드 종료

```bash
machcoordinatoradmin --shutdown-node=warehouse-b1
```

### 2. 노드 분리 (선택)

제거 전 데이터 재분산이 필요한 경우, 노드를 클러스터 메타에서 분리하고 수동으로 데이터를 처리합니다.

```bash
machcoordinatoradmin --detach-node=warehouse-b1
```

### 3. 노드 제거

```bash
machcoordinatoradmin --remove-node=warehouse-b1
```

`--remove-node`는 클러스터 메타에서 노드를 삭제하고 해당 노드의 Machbase 홈 디렉터리와 데이터베이스 파일을 삭제합니다. 별도로 지정된 절대 경로의 `DBS_PATH`도 정리됩니다.

## 주의사항

- 그룹 내 마지막 Warehouse 노드는 제거하지 않는 것이 원칙입니다. 해당 그룹의 데이터에 접근할 수 없게 됩니다.
- 노드 추가 시 `--dbs-path`로 지정한 디렉터리는 추가 시점에 존재하지 않아야 합니다. 이미 존재하면 `DBS_PATH already exists` 오류가 발생합니다.
- `/`, `/etc`, `/usr`, `/home`, `/bin` 같은 시스템 경로 자체는 `--dbs-path`로 지정할 수 없습니다.
