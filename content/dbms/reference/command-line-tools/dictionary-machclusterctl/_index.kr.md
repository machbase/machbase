---
type: docs
title: 'machclusterctl 명령/옵션 사전'
weight: 70
---

`machclusterctl`은 Machbase Cluster Edition의 클러스터 전체를 단일 명령으로 관리하는 도구입니다. YAML 설정 파일을 기반으로 클러스터 초기화, 시작, 종료, 상태 확인 등을 수행합니다.

## 주요 명령

| 명령 | 설명 |
|------|------|
| `init` | 클러스터 초기화 (설정 파일 기반 환경 생성) |
| `start` | 클러스터 전체 노드 시작 |
| `stop` | 클러스터 전체 노드 정상 종료 |
| `destroy` | 클러스터 제거 (데이터 포함) |
| `status` | 클러스터 전체 노드 상태 확인 |
| `connect` | Broker에 machsql로 접속 |
| `export` | 현재 클러스터 설정을 파일로 내보내기 |

## 사용법

```bash
machclusterctl <command> [options]
```

## 명령 상세

### init

YAML 설정 파일을 읽어 클러스터 환경을 초기화합니다. Coordinator, Deployer, Broker, Warehouse 각 노드의 디렉토리와 설정 파일을 생성합니다.

```bash
machclusterctl init -f cluster.yaml
```

### start

클러스터 전체를 순서에 맞게 시작합니다. Coordinator → Deployer → Broker → Warehouse 순으로 기동됩니다.

```bash
machclusterctl start
machclusterctl start -f cluster.yaml
```

### stop

클러스터 전체를 정상 종료합니다.

```bash
machclusterctl stop
```

### destroy

클러스터를 완전히 제거합니다. 데이터베이스 파일도 삭제되므로 주의해서 사용합니다.

```bash
machclusterctl destroy
```

### status

클러스터 각 노드의 현재 상태를 출력합니다.

```bash
machclusterctl status
```

### connect

Broker 노드에 `machsql`로 접속합니다.

```bash
machclusterctl connect
```

### export

현재 클러스터 구성을 YAML 파일로 내보냅니다.

```bash
machclusterctl export -o cluster_backup.yaml
```

## YAML 설정 파일 구조

`machclusterctl init`에 사용하는 YAML 설정 파일의 기본 구조입니다.

```yaml
cluster:
  coordinator:
    host: 192.168.0.32
    port: 5101
    http_port: 5102
    home: /home/machbase/coordinator1

  deployer:
    - host: 192.168.0.32
      port: 5201
      home: /home/machbase/deployer1

  broker:
    - host: 192.168.0.32
      port: 5301
      http_port: 5302
      home: /home/machbase/broker1
      service_port: 5757

  warehouse:
    - group: Group1
      host: 192.168.0.32
      port: 5401
      http_port: 5402
      home: /home/machbase/warehouse_a1
      service_port: 5400
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `-f`, `--file` | 클러스터 설정 YAML 파일 경로 |
| `-o`, `--output` | 출력 파일 경로 (`export` 명령에서 사용) |
| `-h`, `--help` | 도움말 출력 |

## 사용 예시

```bash
# 클러스터 초기 구성
machclusterctl init -f my_cluster.yaml

# 클러스터 시작
machclusterctl start

# 상태 확인
machclusterctl status

# Broker에 접속하여 SQL 실행
machclusterctl connect

# 클러스터 종료
machclusterctl stop

# 설정 내보내기
machclusterctl export -o cluster_config_backup.yaml
```
