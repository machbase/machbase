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

수동 배포 환경에서 직접 교체해야 하는 경우 먼저 Coordinator에 새 패키지를 등록합니다.

```bash
machcoordinatoradmin --add-package=machbase-v8.6.0 \
  --file-name=/home/machbase/packages/machbase-cluster-8.6.0.official-LINUX-X86-64-release.tgz
```

그 다음 Warehouse → Broker → Lookup → Deployer → Coordinator 순으로 종료합니다.

```bash
machcoordinatoradmin --shutdown-node=192.168.1.13:5501
machcoordinatoradmin --shutdown-node=192.168.1.14:5501
machcoordinatoradmin --shutdown-node=192.168.1.11:5401
machcoordinatoradmin --shutdown-node=192.168.1.10:5301
machdeployeradmin --shutdown
machcoordinatoradmin --shutdown
```

각 노드 홈을 새 패키지로 교체할 때는 기존 `conf/machbase.conf`, `dbs/`, `meta/`, `package/`
디렉터리를 보존합니다. 기존 홈 위에 단순히 압축을 해제하지 말고, staging 경로에 새 패키지를
해제한 뒤 보존 대상 경로를 제외하고 교체합니다.

Coordinator → Deployer → Lookup → Broker → Warehouse 순으로 시작합니다.

```bash
machcoordinatoradmin --startup
machdeployeradmin --startup
machcoordinatoradmin --startup-node=192.168.1.10:5301
machcoordinatoradmin --startup-node=192.168.1.11:5401
machcoordinatoradmin --startup-node=192.168.1.13:5501
machcoordinatoradmin --startup-node=192.168.1.14:5501
```

재시작 후 Broker와 Warehouse의 패키지 메타데이터를 새 패키지 이름으로 동기화합니다.

```bash
machcoordinatoradmin --upgrade-node=192.168.1.11:5401 --package-name=machbase-v8.6.0
machcoordinatoradmin --upgrade-node=192.168.1.13:5501 --package-name=machbase-v8.6.0
machcoordinatoradmin --upgrade-node=192.168.1.14:5501 --package-name=machbase-v8.6.0
```

### 5. 상태 확인

```bash
machclusterctl status
```

모든 노드가 각 역할에 맞는 정상 상태이면 업그레이드가 완료된 것입니다.

## 주의사항

- Major 버전 업그레이드는 DB 파일 형식이 변경될 수 있습니다. 반드시 릴리스 노트를 확인하고, 업그레이드 전 백업을 수행하십시오.
- `conf/machbase.conf`, `dbs/`, `meta/`, `package/` 경로를 절대 삭제하거나 초기화하지 마십시오.

---

**다음 읽을 내용**
- [설치 검증 체크리스트](/kr/dbms/installation-deployment-upgrade/validation-checklist/)
