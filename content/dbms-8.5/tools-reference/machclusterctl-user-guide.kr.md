---
title: 'machclusterctl 사용자 가이드'
type: docs
weight: 70
---

`machclusterctl`은 Machbase Cluster Edition을 YAML 파일로 설치하고 운영하기 위한 명령행 도구입니다. 운영자는 `cluster.yaml`에 원하는 클러스터 구성을 선언하고, `validate`, `install`, `apply`, `upgrade`, `start`, `stop` 같은 명령으로 클러스터를 관리합니다.

YAML 작성 방법은 [machclusterctl YAML 작성 가이드](../machclusterctl-yaml-guide/)를 함께 참고하십시오.

## 1. 기본 개념

`machclusterctl`은 다음 방식으로 동작합니다.

1. `cluster.yaml`을 읽어 클러스터의 목표 상태를 만듭니다.
2. 현재 클러스터 상태와 목표 상태를 비교합니다.
3. 필요한 설치, 추가, 삭제, 업그레이드, 시작/종료 작업만 수행합니다.

일반적인 운영 흐름은 다음과 같습니다.

```bash
machclusterctl validate -f cluster.yaml
machclusterctl install -f cluster.yaml --dry-run
machclusterctl install -f cluster.yaml --yes
machclusterctl status
```

설치 후 YAML을 수정해 노드를 추가하거나 제거할 때는 `install`이 아니라 `apply`를 사용합니다.

```bash
machclusterctl apply -f cluster.yaml --dry-run
machclusterctl apply -f cluster.yaml --yes
```

## 2. 실행 위치와 환경

`machclusterctl`은 primary coordinator를 설치할 서버나, 설치 후에는 primary coordinator 서버에서 실행하는 것을 권장합니다.

권장 환경 변수:

```bash
export MACHBASE_COORDINATOR_HOME=/home/machbase/coordinator
export MACHBASE_HOME=$MACHBASE_COORDINATOR_HOME
export PATH=$MACHBASE_COORDINATOR_HOME/bin:$PATH
export LD_LIBRARY_PATH=$MACHBASE_COORDINATOR_HOME/lib:$LD_LIBRARY_PATH
```

`status`, `start`, `stop`, `connect`, `export`처럼 YAML 없이 실행하는 명령은 `MACHBASE_COORDINATOR_HOME`을 기준으로 primary coordinator를 찾습니다. 설치 후의 current topology는 로컬 상태 파일이 아니라 coordinator metadata에서 조회합니다.

이후 YAML 없이 실행하는 명령은 보통 옵션 없이 사용합니다.

```bash
machclusterctl status
machclusterctl connect broker-1
machclusterctl export -o cluster-export.yaml
```

환경 변수를 바꾸기 어렵거나 한 서버에서 여러 coordinator home을 번갈아 확인할 때만 `--coordinator`로 primary coordinator home을 직접 지정합니다.

```bash
machclusterctl status --coordinator /home/machbase/coordinator
machclusterctl export --coordinator /home/machbase/coordinator -o cluster-export.yaml
```

## 3. 설치 전 준비

설치 전에 다음 항목을 준비합니다.

| 항목 | 설명 |
|------|------|
| package archive | primary coordinator 서버 로컬에 있는 Machbase Cluster Edition package 파일 |
| SSH key | primary coordinator 서버에서 각 대상 서버로 접속할 때 사용하는 private key |
| cluster.yaml | 설치할 coordinator, deployer, lookup, broker, warehouse 구성 |
| 디렉터리 권한 | 각 노드의 `home_path` 상위 경로를 생성하고 쓸 수 있는 권한 |
| 포트 | 각 서버에서 YAML에 지정한 포트가 사용 중이 아니어야 함 |

SSH는 key file 기반의 비대화형 접속을 사용합니다. YAML에는 password 필드를 작성하지 않습니다.

사전 확인 예:

```bash
ssh -i /home/machbase/.ssh/id_rsa machbase@192.168.0.11 'echo ok'
scp -i /home/machbase/.ssh/id_rsa /etc/hosts machbase@192.168.0.11:/home/machbase/hosts.test
```

## 4. 명령 요약

| 명령 | 용도 |
|------|------|
| `validate` | YAML 문법, 필수값, 포트 충돌, topology 검사 |
| `install` | 비어 있는 환경에 새 클러스터 설치 |
| `apply` | 실행 중인 클러스터에 YAML 변경 사항 반영 |
| `upgrade` | package 변경에 따른 노드 업그레이드 |
| `status` | 현재 클러스터 상태 조회 |
| `connect` | broker 또는 warehouse alias로 `machsql` 접속 |
| `start` | 전체, 타입별 또는 특정 노드 시작 |
| `stop` | 전체, 타입별 또는 특정 노드 종료 |
| `export` | 실행 중인 클러스터 topology를 YAML로 출력 |
| `destroy` | 클러스터 설치 흔적 제거 |

자주 쓰는 공통 옵션:

| 옵션 | 설명 |
|------|------|
| `-f`, `--file` | 사용할 YAML 파일입니다. 기본값은 `./cluster.yaml`입니다. |
| `--dry-run` | 실제로 변경하지 않고 검사 결과와 실행 계획만 출력합니다. |
| `-y`, `--yes` | 확인 질문 없이 실행합니다. |
| `-v`, `--verbose` | 호환성을 위해 허용됩니다. 실행 명령은 기본적으로 진행 로그를 출력합니다. |
| `-s`, `--silent` | 진행 로그를 억제합니다. `-v`/`--verbose`보다 우선합니다. |
| `--coordinator` | YAML 없이 실행하는 `status`, `start`, `stop`, `connect`, `export`에서 사용할 primary coordinator home입니다. |

## 5. YAML 검증

설치나 변경 전에는 항상 YAML을 먼저 검증합니다.

```bash
machclusterctl validate -f cluster.yaml
```

정상인 경우:

```text
Validation passed.
```

주요 검증 항목:

- 필수 필드 누락
- node alias 중복
- 같은 host 안의 포트 충돌
- primary coordinator 개수
- lookup master/monitor 구성
- `home_path`, `dbs_path` 경로 형식
- `deployer` 참조

## 6. 최초 설치

`install`은 아직 클러스터가 설치되지 않은 비어 있는 환경에서만 사용합니다. 기존 설치 흔적이 있거나 클러스터가 이미 실행 중이면 실패합니다.

먼저 설치할 수 있는지 확인합니다.

```bash
machclusterctl install -f cluster.yaml --dry-run --verbose
```

문제가 없으면 실제 설치를 실행합니다.

```bash
machclusterctl install -f cluster.yaml --yes --verbose
```

설치가 끝나면 상태를 확인합니다.

```bash
machclusterctl status
```

`install`은 YAML을 기준으로 coordinator, deployer, package, lookup, broker, warehouse를 순서대로 준비하고 기동합니다. 설치 후 `status`, `start`, `stop`, `connect`, `export`는 실행 중인 coordinator에서 current metadata를 조회합니다.

## 7. 운영 변경 반영

설치 후 YAML을 수정해 노드를 추가, 제거, 변경할 때는 `apply`를 사용합니다.

권장 절차:

```bash
machclusterctl validate -f cluster.yaml
machclusterctl apply -f cluster.yaml --dry-run --verbose
machclusterctl apply -f cluster.yaml --yes --verbose
machclusterctl status
```

`apply`는 실행 중인 클러스터에서만 동작합니다. 클러스터가 shutdown 상태이면 먼저 시작합니다.

```bash
machclusterctl start
machclusterctl apply -f cluster.yaml --dry-run
machclusterctl apply -f cluster.yaml --yes
```

`apply`로 처리할 수 있는 대표 작업:

- lookup, broker, warehouse 추가
- lookup, broker, warehouse 삭제
- lookup, broker, warehouse 설정 변경에 따른 재등록
- secondary coordinator 추가
- deployer 추가
- YAML의 package 변경에 따른 broker/warehouse 업그레이드

primary coordinator의 교체나 제거는 지원하지 않습니다.

## 8. 시작, 종료, 상태 조회

전체 상태 조회:

```bash
machclusterctl status
```

전체 시작과 종료:

```bash
machclusterctl start
machclusterctl stop
```

타입별 시작과 종료:

```bash
machclusterctl start --type=warehouse
machclusterctl stop --type=warehouse

machclusterctl start --type=broker
machclusterctl stop --type=broker
```

특정 노드 시작과 종료:

```bash
machclusterctl start --node=warehouse-group1-1
machclusterctl stop --node=warehouse-group1-1
```

`--node`에는 `host:port`가 아니라 YAML의 `alias`를 입력합니다.

warehouse를 중지할 때는 필요한 warehouse group 상태 전환도 함께 수행합니다. 단일 warehouse를 중지한 후에는 group 상태를 다시 `normal`로 복원합니다. 전체 warehouse 중지처럼 group 전체가 내려가는 경우에는 종료 흐름에 맞춰 상태 전환을 요청합니다.

## 9. SQL 접속

broker 또는 warehouse에 `machsql`로 접속하려면 `connect`를 사용합니다.

```bash
machclusterctl connect broker-1
machclusterctl connect warehouse-group1-1
```

`connect`는 alias가 가리키는 host와 `service_port`를 찾아 다음 형식으로 `machsql`을 실행합니다.

```bash
machsql -s <host_ip> -P <service_port>
```

예를 들어 `broker-1`의 host가 `192.168.0.11`이고 `service_port`가 `5656`이면 다음 명령을 실행하는 것과 같습니다.

```bash
machsql -s 192.168.0.11 -P 5656
```

기본적으로 실행 중인 coordinator metadata에서 alias와 service port를 조회합니다. 특정 YAML 파일을 기준으로 접속 대상을 찾으려면 `-f`를 지정합니다.

```bash
machclusterctl connect -f cluster.yaml broker-1
```

주의:

- alias는 broker 또는 warehouse 노드여야 합니다.
- `--node`와 마찬가지로 `host:port`가 아니라 YAML의 `alias`를 사용합니다.
- 일반적으로는 `MACHBASE_COORDINATOR_HOME`으로 primary coordinator home을 지정합니다.
- 환경 변수를 쓰기 어려운 예외 상황에서는 `--coordinator`로 primary coordinator home을 직접 지정할 수 있습니다.

## 10. 패키지 업그레이드

업그레이드는 YAML의 `cluster.package`에 지정한 입력 package를 새 archive로 바꾼 뒤 실행합니다. 운영자가 직접 작성하는 YAML은 보통 `path`를 사용합니다.

```yaml
cluster:
  package:
    name: machbase-v2
    path: /machbase/packages/machbase-v2.tgz
```

`machclusterctl export`가 만든 YAML은 package 경로를 다음과 같이 나눠 기록할 수 있습니다.

```yaml
cluster:
  package:
    name: machbase-v2
    origin_path: /machbase/packages/machbase-v2.tgz
    registered_path: /machbase/coordinator/package/machbase-v2.tgz
```

각 필드의 의미는 다음과 같습니다.

- `path`: 운영자가 작성하는 간단한 입력 archive 경로입니다.
- `origin_path`: `path`와 같은 목적의 입력 archive 경로입니다. `origin_path`와 `path`가 함께 있으면 `origin_path`가 우선합니다.
- `registered_path`: coordinator가 `--add-package` 후 내부 package 저장소에 보관하고 있는 경로입니다. 실행 입력이 아니라 current metadata에서 관찰한 값입니다.

package 변경 여부는 실행 중인 broker/warehouse의 current package name과 YAML의 `cluster.package.name`을 비교해 판단합니다. 같은 `package.name`을 유지한 채 archive 내용이나 `path`/`origin_path`만 바꾸면 기존 broker/warehouse는 업그레이드 대상으로 감지되지 않습니다. 새 archive를 적용할 때는 새 package 이름과 고유한 archive file name을 함께 지정합니다.

### 10-1. package 경로 운영 규칙

`cluster.package.path` 또는 `cluster.package.origin_path`에는 primary coordinator 서버 로컬에 있는 **원본 package archive 경로**를 작성합니다. `install`, 신규 노드 `apply`, `upgrade`는 필요할 때 `machcoordinatoradmin --add-package=<name> --file-name=<archive>`를 자동으로 실행합니다.

package archive는 명령을 실행하는 서버에서 읽을 수 있어야 합니다. `--full-stop` 사전 검사는 archive 안에 `machcoordinatoradmin`, `machdeployeradmin`, `conf/`, `lib/` 항목이 있는지 확인합니다.

운영 YAML에서는 다음과 같이 coordinator가 관리하는 package 저장소 경로를 새 package 등록 source로 사용하지 않는 것을 원칙으로 합니다.

```yaml
# Recommended: source archive path kept by the operator
cluster:
  package:
    name: machbase-v2
    path: /machbase/packages/machbase-v2.tgz

# Not recommended: path stored internally after coordinator registration
cluster:
  package:
    name: machbase-v2
    path: /machbase/coordinator/package/machbase-v2.tgz
```

이유는 다음과 같습니다.

- coordinator package 저장소의 파일은 `--add-package`의 결과물입니다. 같은 파일을 다시 source로 지정하면 “이미 등록된 package”인지 “새 package로 등록하려는 파일명 충돌”인지에 따라 동작이 달라집니다.
- 같은 `package.name`과 같은 file name이 이미 등록되어 있으면 `machclusterctl`은 멱등 처리를 위해 no-op처럼 넘어갈 수 있습니다.
- 다른 `package.name`으로 같은 file name을 재사용하면 coordinator가 file name 중복으로 거절할 수 있습니다. 따라서 새 package는 `machbase-v2.tgz`, `machbase-v3.tgz`처럼 file name도 고유하게 관리합니다.
- `destroy`는 coordinator home과 package 저장소를 제거할 수 있습니다. 재설치에 사용할 archive는 coordinator home 밖의 별도 위치에 보관합니다.

정상 운영 기준:

- `install`, `apply`를 통한 신규 노드 추가, `upgrade`에 사용하는 `path` 또는 `origin_path`에는 coordinator home 밖에 보존할 수 있는 원본 archive 경로를 작성합니다.
- package 내용이 바뀌면 `package.name`과 archive file name을 함께 바꿉니다.
- export YAML을 재설치나 업그레이드 입력으로 재사용할 때는 `origin_path`를 원본 archive 경로로 수정하거나, `registered_path` 대신 `path`를 새로 작성한 뒤 실행합니다.

### 10-2. online 업그레이드

`--online`은 broker와 warehouse에 package를 적용합니다. coordinator, deployer, lookup은 online 모드의 대상이 아닙니다.

```bash
machclusterctl upgrade -f cluster.yaml --online --dry-run
machclusterctl upgrade -f cluster.yaml --online --yes --verbose
```

`upgrade`에서 모드를 생략하면 online 모드로 처리됩니다. 운영 절차를 명확히 하기 위해 명령에 `--online`을 명시하는 것을 권장합니다. `--online`과 `--full-stop`은 함께 사용할 수 없습니다. `apply`가 package 변경을 감지해 자동으로 수행하는 업그레이드도 broker/warehouse online 업그레이드와 범위가 같습니다.

online 업그레이드의 주요 흐름:

1. cluster가 running 상태인지 확인합니다.
2. YAML과 current topology 사이에 노드 추가/삭제/설정 변경이 없는지 확인합니다.
3. 새 package archive를 coordinator package 저장소에 등록합니다.
4. broker는 `--upgrade-node` 후 startup을 수행합니다.
5. warehouse는 group을 `readonly`로 전환하고 대상 노드를 `inactive`로 만든 뒤 `--upgrade-node`, startup/activate, group의 `normal` 복원을 수행합니다.
6. 대상 broker/warehouse가 running 상태인지 확인합니다.

online 모드는 전체 cluster를 중지하지 않지만, HA를 고려한 rolling upgrade를 보장하는 모드는 아닙니다. coordinator/deployer/lookup binary 변경, 프로토콜 호환성 위험이 있는 변경, 전체 노드를 같은 package로 맞춰야 하는 변경은 `--full-stop`으로 처리합니다.

### 10-3. full-stop 업그레이드

coordinator, deployer, lookup까지 포함해 전체 노드의 binary를 교체하려면 `--full-stop`을 사용합니다. 이 모드는 전체 클러스터 중단을 전제로 합니다.

```bash
machclusterctl upgrade -f cluster.yaml --full-stop --dry-run
machclusterctl upgrade -f cluster.yaml --full-stop --yes --verbose
```

full-stop 업그레이드의 주요 흐름:

1. cluster가 running 상태인지 확인합니다.
2. YAML과 current topology 사이에 노드 추가/삭제/설정 변경이 없는지 확인합니다.
3. 로컬 `tar`를 실행할 수 있는지, 원격 노드가 있으면 `ssh`/`scp`도 실행할 수 있는지 확인합니다.
4. package archive가 존재하고 필수 항목을 포함하는지 확인합니다.
5. 모든 대상 노드의 `home_path`가 존재하고 쓰기 가능한지 확인합니다.
6. 새 package를 coordinator package 저장소에 등록합니다.
7. 전체 cluster를 중지합니다.
8. 각 노드의 `home_path` 옆 staging 경로에 archive를 해제한 뒤 노드 홈에 반영합니다.
9. primary coordinator를 먼저 시작하고 나머지 cluster를 시작합니다.
10. broker/warehouse package metadata를 동기화하고, 전체 대상 노드가 running 상태인지 확인합니다.

노드 홈을 교체할 때 `dbs`, `meta`, `package` 디렉터리는 보존합니다. 기존 `conf/machbase.conf`도 백업한 뒤 복원합니다. 교체 중 오류가 발생하면 해당 노드의 기존 홈 항목을 가능한 범위에서 되돌립니다.

업그레이드 전에는 topology 변경이 없어야 합니다. 노드 추가/삭제/변경이 있으면 먼저 `apply`로 반영한 뒤 package 업그레이드를 수행합니다.

업그레이드 후 확인:

```bash
machclusterctl status
machclusterctl apply -f cluster.yaml --dry-run
```

## 11. 현재 topology 내보내기

실행 중인 클러스터 상태를 YAML로 저장하려면 `export`를 사용합니다.

```bash
machclusterctl export -o current.yaml
```

표준 출력으로 확인하려면:

```bash
machclusterctl export
```

`export` 결과는 flat YAML입니다. 즉, `cluster.hosts`, `cluster.defaults`, 환경 변수 표현을 만들지 않고 각 노드의 최종 값을 직접 기록합니다. package는 coordinator package metadata를 기준으로 `origin_path`와 `registered_path`를 출력합니다.

`origin_path`는 coordinator가 알고 있는 원본 archive 경로입니다. metadata에 원본 경로가 없으면 export가 유효한 YAML을 만들 수 있도록 `registered_path` 값을 `origin_path`에도 채웁니다. `registered_path`는 coordinator에 등록되어 보관 중인 package 경로(`<coordinator_home>/package/<File-Name>`)입니다.

이 파일은 현재 운영 상태를 보관하거나 변경 전후의 diff를 비교할 때 유용합니다. 단, export의 `registered_path`는 운영자가 처음 설치할 때 사용한 원본 archive 경로를 복원하는 기능이 아닙니다.
`export`는 package 목록 조회에 실패하거나 current package name에 대응하는 등록 package 경로를 absolute path로 찾지 못하면 실패합니다. 이 경우 package name을 경로 대신 사용해 YAML을 생성하지 않습니다.

export YAML 사용 기준:

- 실행 중인 클러스터와 비교하거나, 같은 running cluster에 대해 no-op `apply --dry-run`을 수행하는 용도로는 그대로 사용할 수 있습니다.
- 재설치용으로 사용할 때는 `destroy` 전에 `origin_path`가 가리키는 package 파일을 coordinator home 밖의 별도 위치에 보존하거나, YAML의 `origin_path` 또는 `path`를 실제 원본 archive 경로로 수정합니다.
- 새 package로 업그레이드할 때는 export YAML의 `registered_path`를 실행 입력처럼 사용하지 말고, `package.name`과 `origin_path` 또는 `path`를 새 원본 archive에 맞춰 함께 변경합니다.
- SSH key/user 같은 bootstrap 정보가 필요하면 YAML에 다시 추가합니다.

## 12. destroy

클러스터를 제거하고 미설치 상태로 되돌리려면 `destroy`를 사용합니다.

```bash
machclusterctl destroy -f cluster.yaml
```

확인 질문 없이 실행하려면:

```bash
machclusterctl destroy -f cluster.yaml --yes --verbose
```

주의:

- running cluster와 stopped cluster의 설치 흔적을 모두 정리합니다.
- broker/warehouse 데이터가 삭제될 수 있습니다.
- 운영 환경에서는 실행 권한을 제한합니다.

## 13. 자주 보는 오류

| 오류/상황 | 조치 |
|-----------|------|
| `cluster is already installed` | 기존 설치 흔적이 있습니다. 새로 설치하려면 `destroy`를 실행하거나 수동으로 정리한 후 `install`을 다시 실행합니다. |
| `cluster is not installed` | 먼저 `install`을 실행해야 합니다. |
| `cluster is installed but not running` | `machclusterctl start`를 실행한 후 `apply` 또는 `upgrade`를 다시 실행합니다. |
| `port conflict` | 같은 host 안에서 중복된 `cluster_link_port`, `http_admin_port`, `service_port` 또는 파생 포트를 수정합니다. |
| `undefined host alias` | YAML의 `host`가 `cluster.hosts`에 정의되어 있는지 확인합니다. |
| `key_file missing` | SSH key 경로를 확인하거나 `cluster.ssh.key_file`을 지정합니다. |
| `ssh.password ... is not supported` | YAML에서 password 항목을 제거하고 key file 기반 SSH를 사용합니다. |
| `missing cluster.package.origin_path` | `cluster.package.path` 또는 `cluster.package.origin_path`에 입력 archive 경로를 지정합니다. |
| `package.path changed but package.name stayed` | 새 package archive에는 새 `package.name`을 지정합니다. `origin_path`만 바꾼 경우에도 같은 원칙이 적용됩니다. |
| `package already exists` 또는 `File-Name already exists` | 같은 archive file name이 coordinator에 이미 등록되어 있습니다. 새 package라면 `package.name`과 archive file name을 모두 새 값으로 바꾸고, `path` 또는 `origin_path`에는 coordinator package 저장소가 아닌 원본 archive 경로를 지정합니다. |
| `connect target ... must be broker or warehouse alias` | `connect` 대상 alias가 broker 또는 warehouse인지 확인합니다. |

문제가 발생하면 먼저 `--dry-run --verbose`로 실행 계획과 사전 검사 결과를 확인합니다.

```bash
machclusterctl install -f cluster.yaml --dry-run --verbose
machclusterctl apply -f cluster.yaml --dry-run --verbose
machclusterctl upgrade -f cluster.yaml --online --dry-run --verbose
```

## 14. 참고 파일

- YAML 작성 가이드: [machclusterctl YAML 작성 가이드](../machclusterctl-yaml-guide/)
- 환경 변수 기반 샘플: [machclusterctl-sample-defaults.yaml](/dbms-8.5/tools-reference/machclusterctl-sample-defaults.yaml)
- 샘플 환경 변수: [machclusterctl-sample-defaults.env.sh](/dbms-8.5/tools-reference/machclusterctl-sample-defaults.env.sh)
- 정적 샘플: [machclusterctl-sample-defaults-noenv.yaml](/dbms-8.5/tools-reference/machclusterctl-sample-defaults-noenv.yaml)
