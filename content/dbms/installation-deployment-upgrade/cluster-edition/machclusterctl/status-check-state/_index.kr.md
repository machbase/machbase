---
type: docs
title: '상태 확인'
weight: 50
toc: true
---

클러스터 전체 노드의 상태를 한 번에 조회합니다.

## 상태 조회

```bash
machclusterctl status
```

`MACHBASE_COORDINATOR_HOME`을 사용하지 않는 환경에서는 Primary Coordinator 홈을 직접 지정합니다.

```bash
machclusterctl status --coordinator /home/machbase/coordinator
```

또는 Coordinator 관리 도구로 직접 조회합니다.

```bash
machcoordinatoradmin --cluster-status
```

## 출력 해석

```
+-------------+--------------------------------+--------------------------------+--------------------------------+-------------------------------+-------------+-----------------+----------+
|  Node Type  |           Node Name            |           Group Name           |           Group State          |    Desired & Actual State     |  RP State   | Disk(%) (00/00) | Ping(μs) |
+-------------+--------------------------------+--------------------------------+--------------------------------+-------------------------------+-------------+-----------------+----------+
| coordinator | coord-1(192.168.1.10:5101)     | Coordinator                    | normal                         | primary       | primary       | ----------- | --------------- |      214 |
| deployer    | deployer-1(192.168.1.10:5201)  | Deployer                       | normal                         | running       | running       | ----------- | --------------- |      100 |
| broker      | broker-1(192.168.1.11:5401)    | Broker                         | normal                         | leader        | leader        | ----------- | --------------- |      100 |
| warehouse   | wh-g1-1(192.168.1.13:5501)     | group1                         | normal                         | normal        | normal        | running     | 26.9            |      100 |
+-------------+--------------------------------+--------------------------------+--------------------------------+-------------------------------+-------------+-----------------+----------+
```

| 상태 | 의미 |
|------|------|
| `normal` | 정상 동작 중 |
| `primary` | Coordinator Primary 역할 |
| `leader` | Broker Leader 역할 |
| `scrapped` | 장애 감지됨, 복구 필요 |
| `unknown` | 통신 불가, 노드 다운 의심 |
| `sync-standby` | 복제 수신 중 (동기화 진행 중) |

## Desired vs Actual State

- **Desired State**: Coordinator가 기대하는 상태
- **Actual State**: 노드의 실제 상태

두 값이 다르면 노드가 전환 중이거나 이상 상태입니다. 오랫동안 차이가 유지되면 로그를 확인하십시오.

## 서버 로그 확인

각 노드의 로그는 해당 노드의 홈 디렉터리 아래 `trc/`에 있습니다.

```bash
tail -f $MACHBASE_HOME/trc/machbase.trc
```

---

**다음 읽을 내용**
- [구성 변경 적용](/dbms/installation-deployment-upgrade/cluster-edition/machclusterctl/configuration-change-alter/)
