---
type: docs
title: 'Package 준비와 등록'
weight: 10
toc: true
---

Cluster Edition 수동 배포의 패키지 준비와 등록 절차입니다. 먼저 Coordinator와 Deployer에는 전체
패키지를 설치하고 환경 변수를 설정합니다. Broker와 Warehouse 배포에 사용할 경량 패키지는
Coordinator가 기동된 후 Coordinator에 등록합니다.

## 패키지 종류

Cluster Edition에는 두 가지 패키지가 있습니다.

| 패키지 | 대상 노드 | 특징 |
|--------|-----------|------|
| 전체 패키지 | Coordinator, Deployer | 모든 실행 파일 포함 |
| 경량 패키지 (lightweight) | Broker, Warehouse | 데이터 처리에 필요한 파일만 포함, 크기 작음 |

파일명 예시:
- 전체: `machbase-cluster-8.6.0.official-LINUX-X86-64-release.tgz`
- 경량: `machbase-cluster-8.6.0.official-LINUX-X86-64-release-lightweight.tgz`

## Coordinator와 Deployer에 패키지 배포

전체 패키지 파일을 Coordinator와 Deployer 노드에 복사하고 압축 해제합니다.

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

Broker와 Warehouse 노드에는 이 단계에서 경량 패키지를 직접 압축 해제하지 않습니다. 경량 패키지를
Coordinator에 등록하면, 이후 `--add-node`로 지정한 Deployer가 대상 노드의 `--home-path`에
패키지를 배포합니다.

## Coordinator에 패키지 등록

Broker와 Warehouse를 Coordinator에서 기동하려면 경량 패키지를 Coordinator에 등록해야 합니다.
Coordinator와 Deployer를 설치하고 Coordinator가 실행 중인 상태에서 다음 명령을 실행합니다.

```bash
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-package=machbase \
  --file-name="/home/machbase/machbase-cluster-8.6.0.official-LINUX-X86-64-release-lightweight.tgz"
```

등록된 패키지는 이후 Broker와 Warehouse를 `--add-node`로 등록할 때 `--package-name=machbase`로 참조합니다.

## 환경 변수 설정

Coordinator와 Deployer 운영 계정의 `~/.bashrc`에 해당 역할에 맞는 HOME 경로를 설정합니다.

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
- [Coordinator / Deployer 설치](/kr/dbms/installation-deployment-upgrade/cluster-edition/manual-machcoordinatoradmin/coordinator-deployer/)
