---
title : "Coordinator / Deployer 설치, Package 추가"
type: docs
weight: 20
---

## Coordinator 설치

### 환경 설정

machbase 계정으로 로그인한 후에,  machbase 권한으로 다음과 같이 파일을 수정하여 설치 디렉터리와 경로 정보에 대한 환경을 설정한다.

```bash
## .bashrc 편집한다.                                  
export MACHBASE_COORDINATOR_HOME=~/coordinator
export MACHBASE_DEPLOYER_HOME=~/deployer
export MACHBASE_HOME=~/coordinator
export PATH=$MACHBASE_HOME/bin:$PATH
export LD_LIBRARY_PATH=$MACHBASE_HOME/lib:$LD_LIBRARY_PATH
 
## 변경된 내용을 반영한다.
source .bashrc
```

### 디렉터리 생성 및 압축 해제

전용 디렉터리를 생성하고 패키지 압축 파일을 해당 디렉터리에 압축 해제한다.

```bash
## 디렉터리 생성한다.                                     
mkdir $MACHBASE_COORDINATOR_HOME
  
## 압축 해제한다.
tar zxvf machbase-ent-x.y.z.official-LINUX-X86-64-release.tgz -C $MACHBASE_COORDINATOR_HOME
```

### 포트 설정 및 서비스 구동

machbase.conf 파일을 수정하여 포트를 설정하고 서비스를 구동한다.

```bash
## machbase.conf 파일에서 포트번호를 설정한다.
cd $MACHBASE_COORDINATOR_HOME/conf
cp machbase.conf.sample machbase.conf
vi machbase.conf                                      
CLUSTER_LINK_HOST       = 192.168.0.83 (추가할 노드 ip)
CLUSTER_LINK_PORT_NO    = 5101
HTTP_ADMIN_PORT         = 5102
  
## 메타 정보를 생성하고 서비스 구동한다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin -c
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin -u
```

### 노드 등록 및 확인

Coordinator 노드를 추가하고 확인한다.

```bash
## 노드 등록.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-node="192.168.0.83:5101" --node-type=coordinator                                      
  
## 노드 확인.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --cluster-status
```

|옵션 항목| 설명 | 예시|
|--|--|--|
|--add-node| 추가할 노드명으로 “IP:PORT” 형식으로 지정한다.<br> PORT값은 CLUSTER_LINK_PORT_NO 값이다.| 192.168.0.83:5101|
|--node-type| 노드 종류를 지정한다.<br> coordinator / deployer / broker / warehouse 4종류가 있다.| coordinator|


## Coordinator 삭제

Coordinator가 설치된 서버로 접속하여 Coordinator 프로세스를 정상 종료시킨 후 해당 Coordinator 디렉토리를 삭제한다.

```bash
## coordinator를 종료하고 디렉토리를 삭제한다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin -s
rm -rf $MACHBASE_COORDINATOR_HOME
```

## Secondary Coordinator 설치

Primary Coordinator 외에 추가 Coordinator 를 설치하는 경우, 다음을 주의한다.

* Secondary Coordinator 의 Startup 이전에, Primary Coordinator 에 가서 Secondary Coordinator 를 Add-Node 해야 한다.
* Secondary Coordinator 의 Startup 을 할 때, --primary 옵션으로 Primary Coordinator 를 지정해야 한다.
* Secondary Coordinator 에 Primary Coordinator 를 Add-Node 해서는 안 된다.

**이 경우를 지키지 않는다면, Secondary Coordinator 역시 Primary Coordinator 처럼 행동한다.**

### 디렉터리 생성 및 압축 해제

전용 디렉터리를 생성하고 패키지 압축 파일을 해당 디렉터리에 해제한다.

```bash
## 디렉터리 생성한다.                                     
mkdir $MACHBASE_COORDINATOR_HOME
  
## 압축 해제한다.
tar zxvf machbase-ent-x.y.z.official-LINUX-X86-64-release.tgz -C $MACHBASE_COORDINATOR_HOME
```

### 포트 설정

machbase.conf 파일을 수정하여 포트 설정만 한다. 서비스 구동하면 Primary Coordinator 처럼 작동한다.

```bash
## machbase.conf 파일에서 포트 설정한다.
cd $MACHBASE_COORDINATOR_HOME/conf
vi machbase.conf                                      
CLUSTER_LINK_HOST       = 192.168.0.83 (추가할 노드 ip)
CLUSTER_LINK_PORT_NO    = 5111
HTTP_ADMIN_PORT         = 5112
```

### 노드 등록 및 확인

Primary Coordinator 에서, Secondary Coordinator 노드를 추가하고 확인한다.

```bash
## 노드 등록.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-node="192.168.0.83:5111" --node-type=coordinator                                      
  
## 노드 확인.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --cluster-status
```

### 서비스 구동

이제 Secondary Coordinator를 구동한다. Startup을 할 때, --primary 옵션으로 Primary Coordinator를 지정해야 한다.

```bash
## 메타 정보를 생성하고 서비스를 구동한다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin -c
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin -u --primary="192.168.0.83:5101"
```


## Secondary Coordinator 삭제

Primary Coordinator에 등록된 Secondary Coordinator를 삭제한 후 Secondary Coordinator의 프로세스를 정상 종료시켜야 한다.

```bash
## 노드 삭제.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --remove-node="192.168.0.83:5101"
  
## secondary coordinator를 종료하고 디렉토리를 삭제한다.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin -s
rm -rf $MACHBASE_COORDINATOR_HOME
  
## 노드 확인.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --cluster-status
```

| 옵션 항목| 설명| 예시|
|--|--|--|
| --remove-node | 삭제할 노드명으로, “IP:PORT” 형식으로 지정한다.<br> PORT 값은 CLUSTER_LINK_PORT_NO 값이다.| 192.168.0.84:5201|


## Deployer 설치

Deployer는 broker와 warehouse가 설치되는 모든 Host, 즉 서버에 미리 설치해야 한다.

### 환경 설정

다음과 같이, 설치 디렉터리와 경로에 대한 환경을 설정한다.

```bash
## .bashrc 편집한다.                                     
export MACHBASE_DEPLOYER_HOME=~/deployer
export MACHBASE_HOME=~/deployer
export PATH=$MACHBASE_HOME/bin:$PATH
export LD_LIBRARY_PATH=$MACHBASE_HOME/lib:$LD_LIBRARY_PATH
  
## 변경된 내용을 반영한다.
source .bashrc
```

### 디렉터리 생성 및 압축 해제

전용 디렉터리를 생성하고 패키지 압축 파일을 해당 디렉터리에 압축 해제한다.

```bash
## 디렉터리를 생성한다.                                     
mkdir $MACHBASE_DEPLOYER_HOME
 
## 압축을 해제한다.
tar zxvf machbase-ent-x.y.z.official-LINUX-X86-64-release.tgz -C $MACHBASE_DEPLOYER_HOME
```

### 포트 설정 및 서비스 구동

machbase.conf 파일을 수정하여 포트를 설정하고 서비스를 구동한다.

```bash
## machbase.conf 파일에서 포트를 설정한다.
cd $MACHBASE_DEPLOYER_HOME/conf
vi machbase.conf
CLUSTER_LINK_HOST       = 192.168.0.84
CLUSTER_LINK_PORT_NO    = 5201
HTTP_ADMIN_PORT         = 5202
  
## 메타 정보를 생성하고 서비스를 구동한다.
$MACHBASE_DEPLOYER_HOME/bin/machdeployeradmin -c
$MACHBASE_DEPLOYER_HOME/bin/machdeployeradmin -u
```

### 노드 등록 및 확인

**이 작업은 coordinator 노드에서 수행해야 한다.**

Deployer 노드를 추가하고 확인한다.

```bash
## 노드 등록.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-node="192.168.0.84:5201" --node-type=deployer                                         
 
## 노드 확인.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --cluster-status
```

|옵션 항목| 설명 | 예시|
|--|--|--|
|--add-node| 추가할 노드명으로, “IP:PORT” 형식으로 지정한다.<br> PORT 값은 CLUSTER_LINK_PORT_NO 값이다.| 192.168.0.84:5201|
| --node-type | 노드 종류를 지정한다.<br> coordinator / deployer / broker / warehouse 4종류가 있다.| deployer|


## Deployer 삭제

Coordinator 노드에서 Deployer 노드를 삭제하고, Deployer가 있는 서버에서 Deployer 프로세스를 정상 종료시켜야 한다.

```bash
## 노드 삭제.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --remove-node="192.168.0.84:5201"
 
## deployer를 종료하고 디렉토리를 삭제한다.
$MACHBASE_DEPLOYER_HOME/bin/machdeployeradmin -d
rm -rf $MACHBASE_DEPLOYER_HOME
  
## 노드 확인.
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --cluster-status
```


## 패키지 추가

Coordinator에 broker와 warehouse로 설치될 패키지를 추가 등록한다. 이때 등록되는 패키지로 MWA가 제외된 lightweight 버전을 사용한다.

```
## 설치 패키지를 추가 등록한다.                             
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --add-package=machbase \
    --file-name="/home/machbase/machbase-ent-x.y.z.official-LINUX-X86-64-release-lightweight.tgz"
```

|옵션 항목| 설명 | 예시|
|--|--|--|
|--add-package| 추가할 패키지명을 지정한다.| machbase|
| --file-name| 패키지 파일의 전체 경로와 파일명을 지정한다.<br> Broker와 warehouse 설치만을 위한 패키지이므로, MWA 파일이 제외된 lightweight 패키지를 지정한다.| /home/machbase/machbase-ent-5.0.0.official-LINUX-X86-64-release-lightweight.tgz|


## 패키지 삭제

Coordinator에 등록한 패키지를 삭제한다.

```bash
## 등록한 패키지를 삭제한다.                             
$MACHBASE_COORDINATOR_HOME/bin/machcoordinatoradmin --remove-package=machbase
```
