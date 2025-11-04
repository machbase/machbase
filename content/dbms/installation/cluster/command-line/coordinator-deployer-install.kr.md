---
title: "Coordinator / Deployer 설치, 패키지 추가"
type: docs
weight: 20
---

## Coordinator 설치

### 환경 설정

machbase 계정으로 로그인하여 machbase 권한으로 실행합니다.

설치 디렉토리 및 경로 정보를 설정합니다.

```bash
# .bashrc를 편집합니다.
export MACHBASE_COORDINATOR_HOME=~/coordinator
export MACHBASE_DEPLOYER_HOME=~/deployer
export MACHBASE_HOME=~/coordinator
export PATH=$MACHBASE_HOME/bin:$PATH
export LD_LIBRARY_PATH=$MACHBASE_HOME/lib:$LD_LIBRARY_PATH

# 변경사항을 반영합니다.
source .bashrc
```

### 디렉토리 생성 및 압축 해제

전용 디렉토리를 생성하고 해당 디렉토리에 패키지 아카이브의 압축을 해제합니다.

```bash
# 디렉토리를 생성합니다.
mkdir $MACHBASE_COORDINATOR_HOME

# 압축을 해제합니다.
tar zxvf machbase-ent-x.y.z.official-LINUX-X86-64-release.tgz -C $MACHBASE_COORDINATOR_HOME
```

### 포트 설정 및 서비스 시작

machbase.conf 파일을 수정하여 포트를 설정하고 서비스를 시작합니다.

```bash
# machbase.conf 파일에서 포트를 설정합니다.
cd $MACHBASE_COORDINATOR_HOME/conf
vi machbase.conf
CLUSTER_LINK_HOST       = 192.168.0.83 (추가할 노드 ip)
CLUSTER_LINK_PORT_NO    = 5101
HTTP_ADMIN_PORT         = 5102

# 메타 정보를 생성하고 서비스를 실행합니다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin -c
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin -u
```

### 노드 등록 및 확인

Coordinator 노드를 추가하고 확인합니다.

```bash
# 노드를 등록합니다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-node="192.168.0.83:5101" --node-type=coordinator

# 노드를 확인합니다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --cluster-status
```

| 옵션        | 설명                                                                                    | 예시              |
| ----------- | --------------------------------------------------------------------------------------- | ----------------- |
| --add-node  | 추가할 노드 이름을 "IP:PORT"로 지정합니다.<br>PORT 값은 CLUSTER_LINK_PORT_NO 값입니다. | 192.168.0.83:5101 |
| --node-type | 노드 타입을 지정합니다.<br>coordinator / deployer / broker / warehouse 네 가지가 있습니다. | coordinator       |

## Coordinator 삭제

Coordinator가 설치된 서버에 접속하여 Coordinator 프로세스를 정상 종료하고 Coordinator 디렉토리를 삭제합니다.

```bash
# coordinator를 종료하고 디렉토리를 삭제합니다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin -s
rm -rf $MACHBASE_COORDINATOR_HOME
```

## Secondary Coordinator 설치

Primary Coordinator 외에 추가 Coordinator를 설치하는 경우 다음 사항을 유의합니다:

- Secondary Coordinator를 시작하기 전에 Primary Coordinator에서 Secondary Coordinator를 Add-Node해야 합니다.
- Secondary Coordinator를 시작할 때 --primary 옵션으로 Primary Coordinator를 지정해야 합니다.
- Secondary Coordinator에서 Primary Coordinator를 add-node하면 안 됩니다.

이를 따르지 않으면 Secondary Coordinator가 Primary Coordinator처럼 동작합니다.

### 디렉토리 생성 및 압축 해제

전용 디렉토리를 생성하고 해당 디렉토리에 패키지 아카이브의 압축을 해제합니다.

```bash

# 디렉토리를 생성합니다.
mkdir $MACHBASE_COORDINATOR_HOME

# 압축을 해제합니다.
tar zxvf machbase-ent-x.y.z.official-LINUX-X86-64-release.tgz -C $MACHBASE_COORDINATOR_HOME
```

### 포트 설정

machbase.conf 파일을 수정하여 포트만 설정합니다. **서비스를 시작하면 Primary Coordinator처럼 동작합니다.**

```bash
# machbase.conf 파일에서 포트를 설정합니다.
cd $MACHBASE_COORDINATOR_HOME/conf
vi machbase.conf
CLUSTER_LINK_HOST       = 192.168.0.83 (추가할 ip 주소)
CLUSTER_LINK_PORT_NO    = 5111
HTTP_ADMIN_PORT         = 5112
```

### 노드 등록 및 확인

**Primary Coordinator에서** Secondary Coordinator 노드를 추가하고 확인합니다.

```bash
# 노드를 등록합니다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-node="192.168.0.83:5111" --node-type=coordinator

# 노드를 확인합니다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --cluster-status
```

### 서비스 실행

이제 Secondary Coordinator를 실행합니다. 시작 시 **--primary** 옵션으로 Primary Coordinator를 지정해야 합니다.

```bash
# 메타 정보를 생성하고 서비스를 실행합니다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin -c
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin -u --primary="192.168.0.83:5101"
```

## Secondary Coordinator 삭제

Primary Coordinator에 등록된 Secondary Coordinator를 제거한 후 Secondary Coordinator를 정상 종료해야 합니다.

```bash
# 노드를 삭제합니다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --remove-node="192.168.0.83:5101"

# secondary coordinator를 종료하고 디렉토리를 삭제합니다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin -s
rm -rf $MACHBASE_COORDINATOR_HOME

# 노드를 확인합니다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --cluster-status
```

| 옵션          | 설명                                                                                    | 예시              |
| ------------- | --------------------------------------------------------------------------------------- | ----------------- |
| --remove-node | 삭제할 노드 이름을 "IP:PORT"로 지정합니다.<br>PORT 값은 CLUSTER_LINK_PORT_NO 값입니다. | 192.168.0.84:5201 |

## Deployer 설치

- **안내**
  Deployer는 broker와 warehouse가 설치될 모든 호스트(= 서버)에 사전에 설치되어야 합니다.

### 환경 설정

설치 디렉토리 및 경로 정보를 설정합니다.

```bash
# .bashrc를 편집합니다.
export MACHBASE_DEPLOYER_HOME=~/deployer
export MACHBASE_HOME=~/deployer
export PATH=$MACHBASE_HOME/bin:$PATH
export LD_LIBRARY_PATH=$MACHBASE_HOME/lib:$LD_LIBRARY_PATH

# 변경사항을 반영합니다.
source .bashrc
```

### 디렉토리 생성 및 압축 해제

전용 디렉토리를 생성하고 해당 디렉토리에 패키지 아카이브의 압축을 해제합니다.

```bash
# 디렉토리를 생성합니다.
mkdir $MACHBASE_DEPLOYER_HOME

# 압축을 해제합니다.
tar zxvf machbase-ent-x.y.z.official-LINUX-X86-64-release.tgz -C $MACHBASE_DEPLOYER_HOME
```

### 포트 설정 및 서비스 시작

machbase.conf 파일을 수정하여 포트를 설정하고 서비스를 시작합니다.

```bash
# machbase.conf 파일에서 포트를 설정합니다.
cd $MACHBASE_DEPLOYER_HOME/conf
vi machbase.conf
CLUSTER_LINK_HOST       = 192.168.0.84
CLUSTER_LINK_PORT_NO    = 5201
HTTP_ADMIN_PORT         = 5202

# 메타 정보를 생성하고 서비스를 실행합니다.
$MACHBASE_DEPLOYER_HOME/bin/machdeployeradmin -c
$MACHBASE_DEPLOYER_HOME/bin/machdeployeradmin -u
```

### 노드 등록 및 확인

- **주의**
  이 작업은 coordinator 노드에서 수행해야 합니다.

Deployer 노드를 추가하고 확인합니다.

```bash
# 노드를 등록합니다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-node="192.168.0.84:5201" --node-type=deployer

# 노드를 확인합니다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --cluster-status
```

| 옵션        | 설명                                                                                    | 예시              |
| ----------- | --------------------------------------------------------------------------------------- | ----------------- |
| --add-node  | 추가할 노드 이름을 "IP:PORT"로 지정합니다.<br>PORT 값은 CLUSTER_LINK_PORT_NO 값입니다. | 192.168.0.84:5201 |
| --node-type | 노드 타입을 지정합니다.<br>coordinator / deployer / broker / warehouse 네 가지가 있습니다. | deployer          |

## Deployer 삭제

Coordinator 노드에서 Deployer 노드를 삭제하고 Deployer가 위치한 서버에서 Deployer 프로세스를 정상 종료해야 합니다.

```bash
# 노드를 삭제합니다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --remove-node="192.168.0.84:5201"

# deployer를 종료하고 디렉토리를 삭제합니다.
$MACHBASE_DEPLOYER_HOME/bin/machdeployeradmin -d
rm -rf $MACHBASE_DEPLOYER_HOME

# 노드를 확인합니다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --cluster-status
```

## 패키지 추가

broker와 warehouse로 설치할 패키지를 Coordinator에 추가합니다. 이때 등록되는 패키지는 MWA를 제외한 경량 버전을 등록합니다.

```bash
# 설치 패키지를 등록합니다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-package=machbase \
    --file-name="/home/machbase/machbase-ent-x.y.z.official-LINUX-X86-64-release-lightweight.tgz"
```

| 옵션          | 설명                                                                                                                                     | 예시                                                                            |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| --add-package | 추가할 패키지 이름을 지정합니다.                                                                                                        | machbase                                                                        |
| --file-name   | 패키지 파일의 전체 경로와 파일 이름을 지정합니다.<br>이 패키지는 broker와 warehouse 설치용이므로 MWA 파일을 제외한 경량 패키지를 지정합니다. | /home/machbase/machbase-ent-5.0.0.official-LINUX-X86-64-release-lightweight.tgz |

## 패키지 삭제

Coordinator에 등록된 패키지를 삭제합니다.

```bash
# 등록된 패키지를 삭제합니다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --remove-package=machbase
```
