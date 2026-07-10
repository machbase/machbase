---
type: docs
title: '3.4 업그레이드'
weight: 40
toc: true
---
운영 중인 Machbase를 새 버전으로 업그레이드하는 절차입니다. 에디션과 업그레이드 방식에 따라 절차가 다릅니다.

## 업그레이드 전 확인사항

- 현재 버전과 대상 버전의 호환성을 확인합니다. Minor 버전이 다르면 DB 파일 형식이 변경될 수 있습니다.
- 업그레이드 전 백업을 수행합니다. [백업 방법](/dbms/operations-configuration-recovery/backup-restore-mount/#backup) 참고.
- 진행 중인 INSERT·APPEND 클라이언트를 확인합니다.

## 업그레이드 경로

| 에디션 | 방식 | 링크 |
|--------|------|------|
| Standard Edition | 서버 종료 후 패키지 교체 | [Standard Edition 업그레이드](/kr/dbms/installation-deployment-upgrade/upgrade/standard-edition/) |
| Cluster Edition | Broker/Warehouse 순차 업그레이드 | [온라인 업그레이드](/kr/dbms/installation-deployment-upgrade/upgrade/cluster-edition/online/) |
| Cluster Edition | 전체 중지 | [전체 중지 업그레이드](/kr/dbms/installation-deployment-upgrade/upgrade/cluster-edition/full-stop/) |

Cluster Edition의 경우 데이터 가용성 요구사항에 따라 온라인 또는 전체 중지 방식을 선택합니다.

---

<a id="standard-edition"></a>

## Standard Edition 업그레이드

서버를 종료하고 패키지를 교체한 후 재시작합니다.

### 업그레이드 전 준비

1. **백업 수행**: 데이터 디렉터리(`$MACHBASE_HOME/dbs/`)를 백업합니다.

2. **클라이언트 연결 종료**: 진행 중인 Append 또는 INSERT 작업을 모두 완료합니다.

3. **현재 버전 확인**:
   ```bash
   machbased -v
   ```

### 업그레이드 절차

#### 1. 서버 종료

```bash
machadmin -s
# Machbase server shut down successfully.
```

#### 2. 기존 패키지 백업 (선택)

실행 파일과 라이브러리를 백업합니다.

```bash
cp -a $MACHBASE_HOME/bin $MACHBASE_HOME/bin.bak
cp -a $MACHBASE_HOME/lib $MACHBASE_HOME/lib.bak
```

**데이터 디렉터리(`dbs/`)는 삭제하지 마십시오.** 기존 데이터가 보존됩니다.

#### 3. 새 패키지 압축 해제

```bash
tar zxf machbase-SDK-8.6.0.official-LINUX-X86-64-release.tgz -C $MACHBASE_HOME
```

압축 해제 시 `bin/`, `lib/`, `include/` 등이 덮어씌워지고 `dbs/`는 변경되지 않습니다.

#### 4. 서버 시작

```bash
machadmin -u
# Machbase server started successfully.
```

#### 5. 버전 확인

```bash
machbased -v

# machsql에서 확인
machsql -u SYS -p MANAGER
Mach> SELECT EDITION, BINARY_DB_MAJOR_VERSION, BINARY_DB_MINOR_VERSION FROM V$VERSION;
```

### 주의사항

- `dbs/` 디렉터리를 절대 삭제하거나 초기화(`machadmin -d`)하지 마십시오.
- Minor 버전 간 업그레이드는 DB 파일 마이그레이션이 필요할 수 있습니다. 릴리스 노트를 반드시 확인하십시오.
- Windows 환경에서는 새 패키지 또는 설치 실행 파일을 적용하기 전에 Machbase 서비스를 중지합니다.

---

<a id="cluster-edition"></a>

## Cluster Edition 업그레이드

서비스 중단 여부에 따라 두 가지 방식을 선택합니다.

| 방식 | 서비스 중단 | 적합한 상황 |
|------|-----------|------------|
| [온라인 업그레이드](/kr/dbms/installation-deployment-upgrade/upgrade/cluster-edition/online/) | Broker/Warehouse 순차 재기동 | Broker와 Warehouse만 교체하는 운영 환경 |
| [전체 중지 업그레이드](/kr/dbms/installation-deployment-upgrade/upgrade/cluster-edition/full-stop/) | 있음 | 유지보수 창이 허용되는 경우, Major 버전 변경 |

### 업그레이드 전 공통 주의사항

- 업그레이드 중에는 DDL 또는 DELETE를 실행하지 마십시오.
- 업그레이드 중 노드 추가·시작·종료·삭제 작업을 병행하지 마십시오.
- 온라인 업그레이드는 Broker와 Warehouse를 대상으로 합니다. Coordinator, Deployer, Lookup까지 교체하려면 전체 중지 업그레이드를 사용합니다.
- 업그레이드 전 백업을 권장합니다.

---

<a id="cluster-edition-online"></a>

### 온라인 업그레이드

실행 중인 클러스터에서 Broker와 Warehouse를 순차적으로 업그레이드합니다. Coordinator, Deployer, Lookup까지 포함한 전체 바이너리 교체가 필요하면 [전체 중지 업그레이드](/kr/dbms/installation-deployment-upgrade/upgrade/cluster-edition/full-stop/)를 사용합니다.

#### 업그레이드 절차

##### 1. cluster.yaml의 패키지 변경

`cluster.package.name`과 `cluster.package.origin_path`를 새 패키지로 변경합니다. 패키지 내용이 바뀌면 패키지 이름과 archive 파일 이름도 함께 고유하게 바꿉니다.

```yaml
cluster:
  package:
    name: machbase-v8.6.0
    origin_path: /home/machbase/packages/machbase-cluster-8.6.0.official-LINUX-X86-64-release.tgz
```

`registered_path`는 `machclusterctl export`가 기록하는 Coordinator package repository 경로입니다. 업그레이드 입력 archive를 지정할 때는 `origin_path`를 사용합니다.

##### 2. 실행 계획 확인

```bash
machclusterctl upgrade -f cluster.yaml --online --dry-run --verbose
```

##### 3. 온라인 업그레이드 실행

```bash
machclusterctl upgrade -f cluster.yaml --online --yes --verbose
```

`--online`을 생략해도 online 모드로 처리되지만, 운영 절차를 명확히 하기 위해 옵션을 명시하는 것을 권장합니다.

##### 4. 전체 상태 확인

```bash
machclusterctl status
```

#### 수동 업그레이드 참고

`machcoordinatoradmin --upgrade-node`를 직접 사용하는 경우에는 대상 노드와 패키지 이름을 함께 지정합니다.

```bash
machcoordinatoradmin --upgrade-node=192.168.1.11:5401 --package-name=machbase-v8.6.0
```

온라인 대상은 Broker와 Warehouse로 제한합니다. Broker가 하나만 남아 있을 때 해당 Broker를 업그레이드하면 그 시간 동안 클라이언트 접속이 끊길 수 있습니다.

모든 대상 노드가 각 역할에 맞는 정상 상태이고 새 패키지로 동작하면 업그레이드 완료입니다.

---

<a id="cluster-edition-full-stop"></a>

### 전체 중지 업그레이드

클러스터를 완전히 종료한 후 모든 노드를 일괄 업그레이드합니다. Coordinator, Deployer, Lookup까지 포함해 전체 바이너리를 교체해야 하거나 DB 파일 형식 변경이 수반되는 경우에 사용합니다.

#### 업그레이드 절차

##### 1. 클라이언트 연결 종료

모든 INSERT·APPEND·SELECT 작업이 완료되었는지 확인합니다.

##### 2. cluster.yaml의 패키지 변경

`cluster.package.name`과 `cluster.package.origin_path`를 새 패키지로 변경합니다. 업그레이드 전에는 노드 추가, 삭제, 포트 변경 같은 토폴로지 변경이 없어야 합니다. 토폴로지 변경이 있으면 먼저 `apply`로 반영한 뒤 업그레이드를 수행합니다.

`machclusterctl upgrade --full-stop`은 Coordinator와 Deployer를 포함한 모든 노드 홈에 같은 archive를 교체 반영합니다. 따라서 `origin_path`에는 `machcoordinatoradmin`과 `machdeployeradmin`이 포함된 전체 Cluster 패키지를 지정합니다.

##### 3. 실행 계획 확인

```bash
machclusterctl upgrade -f cluster.yaml --full-stop --dry-run --verbose
```

##### 4. 전체 중지 업그레이드 실행

```bash
machclusterctl upgrade -f cluster.yaml --full-stop --yes --verbose
```

`machclusterctl`은 전체 클러스터 중단을 전제로 패키지를 staging 경로에 해제한 뒤 노드 홈에 교체 반영합니다.

#### 수동 배포 참고

수동 배포 환경에서 직접 교체해야 하는 경우, Coordinator에 새 패키지를 등록합니다.

```bash
machcoordinatoradmin --add-package=machbase-v8.6.0 \
  --file-name=/home/machbase/packages/machbase-cluster-8.6.0.official-LINUX-X86-64-release.tgz
```

Warehouse → Broker → Lookup → Deployer → Coordinator 순으로 종료합니다.

```bash
machcoordinatoradmin --shutdown-node=192.168.1.13:5501
machcoordinatoradmin --shutdown-node=192.168.1.14:5501
machcoordinatoradmin --shutdown-node=192.168.1.11:5401
machcoordinatoradmin --shutdown-node=192.168.1.10:5301
machdeployeradmin --shutdown
machcoordinatoradmin --shutdown
```

각 노드 홈을 새 패키지로 교체할 때는 기존 `conf/machbase.conf`, `dbs/`, `meta/`, `package/` 디렉터리를 보존합니다. 기존 홈 위에 단순히 압축을 해제하지 말고, staging 경로에 새 패키지를 해제한 뒤 보존 대상 경로를 제외하고 교체합니다.

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

##### 5. 상태 확인

```bash
machclusterctl status
```

모든 노드가 각 역할에 맞는 정상 상태이면 업그레이드 완료입니다.

#### 주의사항

- Major 버전 업그레이드는 DB 파일 형식이 변경될 수 있습니다. 릴리스 노트를 반드시 확인하고, 업그레이드 전 백업을 수행하십시오.
- `conf/machbase.conf`, `dbs/`, `meta/`, `package/` 경로를 절대 삭제하거나 초기화하지 마십시오.
