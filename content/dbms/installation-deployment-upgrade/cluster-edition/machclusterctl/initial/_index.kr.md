---
type: docs
title: '최초 설치'
weight: 30
---

`cluster.yaml` 작성과 유효성 검사가 완료되면 클러스터를 설치하고 시작합니다.

## 1. 클러스터 설치

패키지를 각 노드에 배포하고 초기화합니다.

```bash
machclusterctl install -f cluster.yaml
```

이 명령은 다음을 자동으로 처리합니다.

1. 패키지를 각 노드에 복사하고 압축 해제
2. 각 노드의 `machbase.conf` 생성 및 포트 설정
3. Coordinator 데이터베이스 초기화
4. 노드 등록 (Coordinator에 각 노드 추가)

## 2. 클러스터 시작

```bash
machclusterctl start -f cluster.yaml
```

시작 순서: Coordinator → Deployer → Broker → Warehouse 순으로 자동 진행됩니다.

## 3. 상태 확인

```bash
machclusterctl status -f cluster.yaml
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
machclusterctl stop -f cluster.yaml
```

---

**다음 읽을 내용**
- [라이선스 설치](/dbms/installation-deployment-upgrade/pre-install-preparation/license/)
- [상태 확인](/dbms/installation-deployment-upgrade/cluster-edition/machclusterctl/status-check-state/)
