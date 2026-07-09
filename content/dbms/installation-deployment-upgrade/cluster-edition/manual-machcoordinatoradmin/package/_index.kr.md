---
type: docs
title: 'Package 등록'
weight: 20
---

Cluster Edition 수동 배포의 첫 번째 단계입니다. 각 노드에 Machbase 패키지를 배포하고,
Broker와 Warehouse 설치에 사용할 경량 패키지를 Coordinator에 등록합니다.

## 패키지 종류

Cluster Edition에는 두 가지 패키지가 있습니다.

| 패키지 | 대상 노드 | 특징 |
|--------|-----------|------|
| 전체 패키지 | Coordinator, Deployer | 모든 실행 파일 포함 |
| 경량 패키지 (lightweight) | Broker, Warehouse | 데이터 처리에 필요한 파일만 포함, 크기 작음 |

파일명 예시:
- 전체: `machbase-cluster-8.6.0.official-LINUX-X86-64-release.tgz`
- 경량: `machbase-cluster-8.6.0.official-LINUX-X86-64-release-lightweight.tgz`

## 각 노드에 패키지 배포

패키지 파일을 각 노드에 복사하고 압축 해제합니다.

### Coordinator 노드

```bash
# Coordinator 노드에서 실행
mkdir -p ~/coordinator
scp machbase@배포서버:/path/to/machbase-cluster-8.6.0.official-LINUX-X86-64-release.tgz ~/
tar zxf machbase-cluster-8.6.0.official-LINUX-X86-64-release.tgz -C ~/coordinator
```

### Deployer 노드

```bash
mkdir -p ~/deployer
scp machbase@배포서버:/path/to/machbase-cluster-8.6.0.official-LINUX-X86-64-release.tgz ~/
tar zxf machbase-cluster-8.6.0.official-LINUX-X86-64-release.tgz -C ~/deployer
```

### Broker / Warehouse 노드

경량 패키지를 사용합니다.

```bash
# Broker 노드에서
mkdir -p ~/broker
scp machbase@배포서버:/path/to/machbase-cluster-8.6.0.official-LINUX-X86-64-release-lightweight.tgz ~/
tar zxf machbase-cluster-8.6.0.official-LINUX-X86-64-release-lightweight.tgz -C ~/broker

# Warehouse 노드에서
mkdir -p ~/warehouse
scp machbase@배포서버:/path/to/machbase-cluster-8.6.0.official-LINUX-X86-64-release-lightweight.tgz ~/
tar zxf machbase-cluster-8.6.0.official-LINUX-X86-64-release-lightweight.tgz -C ~/warehouse
```

## Coordinator에 패키지 등록

Broker와 Warehouse를 Coordinator에서 기동하려면 경량 패키지를 Coordinator에 등록해야 합니다.
Coordinator 노드에서 다음 명령을 실행합니다.

```bash
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-package=machbase \
  --file-name="/home/machbase/machbase-cluster-8.6.0.official-LINUX-X86-64-release-lightweight.tgz"
```

등록된 패키지는 이후 Broker와 Warehouse를 `--add-node`로 등록할 때 `--package-name=machbase`로 참조합니다.

## 환경 변수 설정

각 노드의 `~/.bashrc`에 해당 역할에 맞는 HOME 경로를 설정합니다.

```bash
# Coordinator 노드
export MACHBASE_COORDINATOR_HOME=~/coordinator
export MACHBASE_HOME=$MACHBASE_COORDINATOR_HOME
export PATH=$MACHBASE_HOME/bin:$PATH
export LD_LIBRARY_PATH=$MACHBASE_HOME/lib:$LD_LIBRARY_PATH
source ~/.bashrc

# Deployer 노드
export MACHBASE_DEPLOYER_HOME=~/deployer
export MACHBASE_HOME=$MACHBASE_DEPLOYER_HOME
...
```

---

**다음 읽을 내용**
- [Coordinator / Deployer 설치](/dbms/installation-deployment-upgrade/cluster-edition/manual-machcoordinatoradmin/coordinator-deployer/)
