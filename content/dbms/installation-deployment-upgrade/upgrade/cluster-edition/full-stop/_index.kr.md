---
type: docs
title: '전체 중지 업그레이드'
weight: 20
toc: true
---

전체 중지 업그레이드는 클러스터를 완전히 종료한 후 모든 노드를 일괄 업그레이드하는 방식입니다.
Coordinator, Deployer, Lookup까지 포함해 전체 바이너리를 교체해야 하거나 DB 파일 형식 변경이
수반되는 경우에 사용합니다.

## 업그레이드 절차

### 1. 클라이언트 연결 종료

모든 INSERT·APPEND·SELECT 작업이 완료되었는지 확인합니다.

### 2. cluster.yaml의 패키지 변경

`cluster.package.name`과 `cluster.package.origin_path`를 새 패키지로 변경합니다. 업그레이드 전에는 노드
추가, 삭제, 포트 변경 같은 토폴로지 변경이 없어야 합니다. 토폴로지 변경이 있으면 먼저 `apply`로
반영한 뒤 업그레이드를 수행합니다.

`machclusterctl upgrade --full-stop`은 Coordinator와 Deployer를 포함한 모든 노드 홈에 같은
archive를 교체 반영합니다. 따라서 `origin_path`에는 `machcoordinatoradmin`과
`machdeployeradmin`이 포함된 전체 Cluster 패키지를 지정합니다.

### 3. 실행 계획 확인

```bash
machclusterctl upgrade -f cluster.yaml --full-stop --dry-run --verbose
```

### 4. 전체 중지 업그레이드 실행

```bash
machclusterctl upgrade -f cluster.yaml --full-stop --yes --verbose
```

`machclusterctl`은 전체 클러스터 중단을 전제로 패키지를 staging 경로에 해제한 뒤 노드 홈에 교체
반영합니다.

## 수동 배포 참고

수동 배포 환경에서 직접 교체해야 하는 경우 Warehouse → Broker → Deployer → Coordinator 순으로
종료합니다.

```bash
machcoordinatoradmin --shutdown-node=192.168.1.13:5501
machcoordinatoradmin --shutdown-node=192.168.1.14:5501
machcoordinatoradmin --shutdown-node=192.168.1.11:5401
machdeployeradmin --shutdown
machcoordinatoradmin --shutdown
```

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

Coordinator → Deployer → Broker → Warehouse 순으로 시작합니다.

```bash
machcoordinatoradmin --startup
machdeployeradmin --startup
machcoordinatoradmin --startup-node=192.168.1.11:5401
machcoordinatoradmin --startup-node=192.168.1.13:5501
machcoordinatoradmin --startup-node=192.168.1.14:5501
```

### 5. 상태 확인

```bash
machclusterctl status
```

모든 노드가 `normal` 상태이면 업그레이드가 완료된 것입니다.

## 주의사항

- Major 버전 업그레이드는 DB 파일 형식이 변경될 수 있습니다. 반드시 릴리스 노트를 확인하고, 업그레이드 전 백업을 수행하십시오.
- `dbs/` 디렉터리를 절대 삭제하거나 초기화하지 마십시오.

---

**다음 읽을 내용**
- [설치 검증 체크리스트](/kr/dbms/installation-deployment-upgrade/validation-checklist/)
