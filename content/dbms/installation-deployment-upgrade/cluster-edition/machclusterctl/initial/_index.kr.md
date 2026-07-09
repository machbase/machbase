---
type: docs
title: '최초 설치'
weight: 30
---

`cluster.yaml` 작성과 유효성 검사가 완료되면 설치 계획을 먼저 확인한 뒤 클러스터를 설치합니다.

## 1. 클러스터 설치

패키지를 각 노드에 배포하고 초기화하기 전에 실행 계획과 사전 점검 결과를 확인합니다.

```bash
machclusterctl install -f cluster.yaml --dry-run --verbose
```

문제가 없으면 실제 설치를 실행합니다.

```bash
machclusterctl install -f cluster.yaml --yes --verbose
```

이 명령은 다음을 자동으로 처리합니다.

1. 패키지를 각 노드에 복사하고 압축 해제
2. 각 노드의 `machbase.conf` 생성 및 포트 설정
3. Coordinator 데이터베이스 초기화
4. 노드 등록 (Coordinator에 각 노드 추가)

## 2. 클러스터 시작

`install`은 Coordinator, Deployer, Lookup, Broker, Warehouse를 준비하고 기동합니다. 설치 후 전체
클러스터를 다시 시작해야 할 때만 다음 명령을 사용합니다.

```bash
machclusterctl start
```

## 3. 상태 확인

```bash
export MACHBASE_COORDINATOR_HOME=/home/machbase/coordinator
machclusterctl status
```

한 서버에서 여러 Coordinator 홈을 번갈아 확인할 때는 직접 지정할 수 있습니다.

```bash
machclusterctl status --coordinator /home/machbase/coordinator
```

모든 노드의 상태가 `normal`이어야 합니다.

```
+-------------+-----------------+-----------+----------+
|  Node Type  |    Node Name    |   Group   |  State   |
+-------------+-----------------+-----------+----------+
| coordinator | 192.168.1.10:5101 | Coordinator | normal |
| deployer    | 192.168.1.10:5201 | Deployer  | normal  |
| broker      | 192.168.1.11:5301 | Broker    | leader  |
| broker      | 192.168.1.12:5301 | Broker    | normal  |
| warehouse   | 192.168.1.13:5401 | group1    | normal  |
| warehouse   | 192.168.1.14:5401 | group1    | normal  |
+-------------+-----------------+-----------+----------+
```

## 4. 클라이언트 접속 테스트

Broker 노드의 IP와 포트로 접속합니다.

```bash
machsql -s 192.168.1.11 -u SYS -p MANAGER
# Mach>
```

## 클러스터 종료

```bash
machclusterctl stop
```

---

**다음 읽을 내용**
- [라이선스 설치](/dbms/installation-deployment-upgrade/pre-install-preparation/license/)
- [상태 확인](/dbms/installation-deployment-upgrade/cluster-edition/machclusterctl/status-check-state/)
