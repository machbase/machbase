---
type: docs
title: '13.7.6 Cluster 그룹 상태 변경'
weight: 60
---

클러스터 운영 중 유지보수, 장애 대응, 데이터 보호를 위해 노드 그룹 또는 개별 노드의 상태를 수동으로 변경할 수 있습니다.

## 클러스터 활성화/비활성화

클러스터 전체를 서비스 상태(`Service`)로 전환하거나 비활성화(`Deactivate`) 상태로 전환합니다.

```bash
# 클러스터 활성화 (Service 상태로 전환)
machcoordinatoradmin --activate

# 클러스터 비활성화 (Deactivate 상태로 전환)
machcoordinatoradmin --deactivate
```

비활성화 상태에서는 클라이언트의 데이터 쓰기가 차단됩니다. 대규모 유지보수나 클러스터 설정 변경 전에 비활성화 상태로 전환합니다.

## Warehouse 그룹 상태 변경

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

## Warehouse 개별 노드 상태 변경

특정 Warehouse 노드의 상태를 `normal` 또는 `scrapped`로 변경합니다.

```bash
# 노드를 scrapped 상태로 변경 (데이터 손상·복구 필요 표시)
machcoordinatoradmin --set-warehouse-state=scrapped --node=warehouse-a1

# 노드를 정상 상태로 복원
machcoordinatoradmin --set-warehouse-state=normal --node=warehouse-a1
```

`scrapped` 상태는 해당 노드의 데이터를 신뢰할 수 없는 경우 또는 강제 복구가 필요한 경우에 사용합니다.

## Broker 활성화/비활성화

특정 Broker 노드를 비활성화하여 새 클라이언트 연결을 차단합니다. 롤링 업그레이드나 Broker 교체 시 사용합니다.

```bash
# Broker 비활성화 (새 연결 차단)
machcoordinatoradmin --deactivate-broker=192.168.0.32:5301

# Broker 활성화 (연결 허용)
machcoordinatoradmin --activate-broker=192.168.0.32:5301
```

비활성화된 Broker는 기존 연결을 유지하지만 새 연결을 받지 않습니다. 기존 연결이 모두 종료된 후 Broker를 안전하게 종료할 수 있습니다.

## 유지보수 절차 예

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
