---
type: docs
title: '온라인 업그레이드'
weight: 10
---

온라인 업그레이드는 서비스를 중단하지 않고 노드를 순차적으로 업그레이드하는 방식입니다. Warehouse 노드를 그룹 단위로 롤링 업그레이드하여 데이터 가용성을 유지합니다.

## 업그레이드 절차

### 1. Coordinator 업그레이드

Coordinator가 다운되어도 Broker·Warehouse의 INSERT·APPEND·SELECT는 영향을 받지 않습니다.

```bash
# Coordinator 종료
machcoordinatoradmin --shutdown

# 새 패키지 압축 해제 (덮어쓰기)
tar zxf machbase-cluster-8.6.0.official-LINUX-X86-64-release.tgz -C $MACHBASE_COORDINATOR_HOME

# Coordinator 시작
machcoordinatoradmin --startup
```

### 2. Deployer 업그레이드

Coordinator와 동일한 방식으로 진행합니다.

```bash
machdeployeradmin --shutdown
tar zxf machbase-cluster-8.6.0.official-LINUX-X86-64-release.tgz -C $MACHBASE_DEPLOYER_HOME
machdeployeradmin --startup
```

### 3. 새 패키지를 Coordinator에 등록

Broker·Warehouse 업그레이드에 사용할 경량 패키지를 Coordinator에 등록합니다.

```bash
machcoordinatoradmin --add-package=v8.6.0 \
  --file-name=./machbase-cluster-8.6.0.official-LINUX-X86-64-release-lightweight.tgz
```

동일한 파일 이름의 패키지가 이미 등록되어 있으면 오류가 발생하므로 패키지 이름을 고유하게 지정합니다.

### 4. Warehouse 노드 롤링 업그레이드

각 그룹 내 노드를 한 번에 하나씩 업그레이드합니다. 같은 그룹의 다른 노드가 살아있어 서비스가 유지됩니다.

```bash
# 노드 종료 후 업그레이드
machcoordinatoradmin --shutdown-node=192.168.1.13:5401
machcoordinatoradmin --upgrade-node=192.168.1.13:5401 --package-name=v8.6.0
machcoordinatoradmin --startup-node=192.168.1.13:5401

# 상태 확인 후 다음 노드 진행
machcoordinatoradmin --cluster-status

# 같은 그룹의 나머지 노드 업그레이드
machcoordinatoradmin --shutdown-node=192.168.1.14:5401
machcoordinatoradmin --upgrade-node=192.168.1.14:5401 --package-name=v8.6.0
machcoordinatoradmin --startup-node=192.168.1.14:5401
```

### 5. Broker 노드 업그레이드

```bash
machcoordinatoradmin --shutdown-node=192.168.1.11:5301
machcoordinatoradmin --upgrade-node=192.168.1.11:5301 --package-name=v8.6.0
machcoordinatoradmin --startup-node=192.168.1.11:5301
```

Broker가 하나만 남아있을 때 업그레이드하면 해당 시간 동안 클라이언트 접속이 끊길 수 있습니다. Broker가 2개 이상이면 순차적으로 업그레이드합니다.

### 6. 전체 상태 확인

```bash
machcoordinatoradmin --cluster-status
```

모든 노드가 `normal` 상태이고 버전이 일치하면 업그레이드 완료입니다.

---

**다음 읽을 내용**
- [설치 검증 체크리스트](/dbms/installation-deployment-upgrade/validation-checklist/)
