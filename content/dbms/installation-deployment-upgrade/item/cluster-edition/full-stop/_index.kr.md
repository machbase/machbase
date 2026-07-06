---
type: docs
title: '전체 중지 업그레이드'
weight: 20
---

전체 중지 업그레이드는 클러스터를 완전히 종료한 후 모든 노드를 일괄 업그레이드하는 방식입니다. Major 버전 간 업그레이드나 DB 파일 형식 변경이 수반되는 경우에 사용합니다.

## 업그레이드 절차

### 1. 클라이언트 연결 종료

모든 INSERT·APPEND·SELECT 작업이 완료되었는지 확인합니다.

### 2. 클러스터 전체 종료

```bash
# machclusterctl을 사용하는 경우
machclusterctl stop -f cluster.yaml

# 수동 배포의 경우
machcoordinatoradmin --shutdown-node=192.168.1.13:5401
machcoordinatoradmin --shutdown-node=192.168.1.14:5401
machcoordinatoradmin --shutdown-node=192.168.1.11:5301
machdeployeradmin --shutdown
machcoordinatoradmin --shutdown
```

Warehouse → Broker → Deployer → Coordinator 순으로 종료합니다.

### 3. 각 노드 패키지 업그레이드

모든 노드에서 새 패키지를 압축 해제합니다. **`dbs/` 디렉터리는 건드리지 않습니다.**

```bash
# Coordinator 노드에서
tar zxf machbase-cluster-8.6.0.official-LINUX-X86-64-release.tgz -C $MACHBASE_COORDINATOR_HOME

# Deployer 노드에서
tar zxf machbase-cluster-8.6.0.official-LINUX-X86-64-release.tgz -C $MACHBASE_DEPLOYER_HOME

# Broker / Warehouse 노드에서 (경량 패키지)
tar zxf machbase-cluster-8.6.0.official-LINUX-X86-64-release-lightweight.tgz -C ~/broker
tar zxf machbase-cluster-8.6.0.official-LINUX-X86-64-release-lightweight.tgz -C ~/warehouse
```

### 4. 클러스터 시작

```bash
# machclusterctl을 사용하는 경우
machclusterctl start -f cluster.yaml

# 수동 배포의 경우
machcoordinatoradmin --startup
machdeployeradmin --startup
machcoordinatoradmin --startup-node=192.168.1.11:5301
machcoordinatoradmin --startup-node=192.168.1.13:5401
machcoordinatoradmin --startup-node=192.168.1.14:5401
```

Coordinator → Deployer → Broker → Warehouse 순으로 시작합니다.

### 5. 상태 확인

```bash
machcoordinatoradmin --cluster-status
```

모든 노드가 `normal` 상태이면 업그레이드가 완료된 것입니다.

## 주의사항

- Major 버전 업그레이드는 DB 파일 형식이 변경될 수 있습니다. 반드시 릴리스 노트를 확인하고, 업그레이드 전 백업을 수행하십시오.
- `dbs/` 디렉터리를 절대 삭제하거나 초기화하지 마십시오.

---

**다음 읽을 내용**
- [설치 검증 체크리스트](/dbms/installation-deployment-upgrade/validation-checklist/)
