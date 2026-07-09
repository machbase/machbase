---
type: docs
title: '13.7.3 Cluster 노드 시작과 종료'
weight: 30
---

클러스터 전체를 재시작하지 않고 특정 노드만 시작하거나 종료해야 하는 경우 `machcoordinatoradmin`을 사용합니다. 개별 노드 제어는 유지보수, 장애 복구, 롤링 업그레이드 시 활용합니다.

## Coordinator를 통한 노드 제어

Coordinator가 실행 중인 상태에서 `machcoordinatoradmin`으로 개별 노드를 원격 제어합니다.

### 노드 시작

```bash
# 특정 노드 시작 (노드 이름 또는 alias 사용 가능)
machcoordinatoradmin --startup-node=192.168.0.32:5401

# alias 사용
machcoordinatoradmin --startup-node=warehouse-a1
```

### 노드 종료

```bash
# 특정 노드 정상 종료
machcoordinatoradmin --shutdown-node=192.168.0.32:5401

# 특정 노드 강제 종료 (응답 없을 때)
machcoordinatoradmin --kill-node=192.168.0.32:5401
```

### Lookup 노드 시작·종료

```bash
# Lookup 노드 전체 시작
machcoordinatoradmin --startup-lookup

# Lookup 노드 전체 종료
machcoordinatoradmin --shutdown-lookup
```

## 노드 직접 제어 (machadmin)

Coordinator와 통신할 수 없는 상황이거나 해당 호스트에 직접 접속한 경우, 각 노드에서 `machadmin`으로 직접 제어합니다.

### Warehouse 노드

```bash
# Warehouse 노드가 설치된 호스트에서 직접 실행
export MACHBASE_HOME=/home/machbase/warehouse_a1
machadmin -u    # 시작
machadmin -s    # 종료
machadmin -e    # 실행 여부 확인
```

### Broker 노드

```bash
export MACHBASE_HOME=/home/machbase/broker1
machadmin -u    # 시작
machadmin -s    # 종료
```

### Coordinator 노드

```bash
export MACHBASE_HOME=/home/machbase/coordinator1
machcoordinatoradmin -u    # 시작 (-u, --startup)
machcoordinatoradmin -s    # 종료 (-s, --shutdown)
machcoordinatoradmin -e    # 실행 여부 확인
```

## 노드 제어 시 권장 순서

### 특정 노드만 재시작

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

### Broker 교체

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

## 주의사항

- **Coordinator 종료 시**: Coordinator가 종료되면 클러스터 메타 변경이 불가합니다. Coordinator 종료 전에 클러스터 상태가 안정적인지 확인합니다.
- **단일 Broker 환경**: Broker가 하나만 있는 경우 Broker를 종료하면 클라이언트가 접속할 수 없습니다. HA 구성을 권장합니다.
- **Warehouse 종료 시**: 해당 그룹의 다른 Warehouse 노드가 정상 동작 중인지 확인한 후 종료합니다.
