---
type: docs
title: 'Coordinator / Deployer 설치'
weight: 10
toc: true
---

패키지 배포가 완료되면 Coordinator를 먼저 설치·시작한 후 Deployer를 등록합니다.

## Coordinator 설치

### 1. machbase.conf 설정

`$MACHBASE_COORDINATOR_HOME/conf/machbase.conf`를 편집합니다.

```bash
vi $MACHBASE_COORDINATOR_HOME/conf/machbase.conf
```

주요 설정:

```
CLUSTER_LINK_HOST    = 192.168.1.10   # 이 노드의 IP
CLUSTER_LINK_PORT_NO = 5101
HTTP_ADMIN_PORT      = 5102
```

### 2. 메타 데이터베이스 생성 및 서비스 시작

```bash
machcoordinatoradmin -c
machcoordinatoradmin -u
```

### 3. 자기 자신을 Coordinator 노드로 등록

```bash
machcoordinatoradmin --add-node="192.168.1.10:5101" --node-type=coordinator
```

### 4. 등록 확인

```bash
machcoordinatoradmin --cluster-status
```

## Secondary Coordinator 설치 (선택)

고가용성을 위해 Secondary Coordinator를 추가합니다.

Secondary 노드에서 패키지를 배포하고 `machbase.conf`를 설정한 후, **Primary Coordinator에서** 먼저 노드를 등록합니다.

```bash
# Primary Coordinator에서 먼저 등록
machcoordinatoradmin --add-node="192.168.1.20:5101" --node-type=coordinator

# 그 다음 Secondary 노드에서 시작 (--primary 옵션으로 Primary 지정)
machcoordinatoradmin -u --primary=192.168.1.10:5101
```

Secondary를 시작하기 전에 반드시 Primary에서 노드 등록을 완료해야 합니다.

## Deployer 설치

### 1. machbase.conf 설정

```
CLUSTER_LINK_HOST    = 192.168.1.10   # Deployer 노드 IP
CLUSTER_LINK_PORT_NO = 5201
HTTP_ADMIN_PORT      = 5202
```

### 2. 시작

```bash
machdeployeradmin -c
machdeployeradmin -u
```

### 3. Coordinator에 Deployer 노드 등록

```bash
machcoordinatoradmin --add-node="192.168.1.10:5201" --node-type=deployer
```

---

**다음 읽을 내용**
- [Lookup / Broker / Warehouse 설치](/dbms/installation-deployment-upgrade/cluster-edition/manual-machcoordinatoradmin/lookup-broker-warehouse/)
