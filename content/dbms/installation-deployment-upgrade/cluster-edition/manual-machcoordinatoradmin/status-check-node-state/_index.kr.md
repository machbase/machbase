---
type: docs
title: '노드 상태 확인'
weight: 40
toc: true
---

클러스터 구성 완료 후 모든 노드의 상태를 확인합니다.

## 전체 클러스터 상태 조회

```bash
machcoordinatoradmin --cluster-status
```

정상 클러스터 출력 예시:

```
+-------------+-------------------+-------------------+-------------------+--------------+
|  Node Type  |     Node Name     |    Group Name     |    Group State    |     State    |
+-------------+-------------------+-------------------+-------------------+--------------+
| coordinator | 192.168.1.10:5101 | Coordinator       | normal            | primary      |
| broker      | 192.168.1.11:5401 | Broker            | normal            | normal       |
| warehouse   | 192.168.1.13:5501 | group1            | normal            | normal       |
| warehouse   | 192.168.1.14:5501 | group1            | normal            | normal       |
+-------------+-------------------+-------------------+-------------------+--------------+
```

Deployer 상태까지 함께 보려면 `--cluster-status --verbose`를 사용합니다. Desired/Actual
state, RP state, 디스크 사용률, ping 값은 `--cluster-status-full`에서 확인합니다.

## 개별 노드 관리 명령

| 명령 | 설명 |
|------|------|
| `machcoordinatoradmin --startup-node=IP:PORT` | 특정 노드 시작 |
| `machcoordinatoradmin --shutdown-node=IP:PORT` | 특정 노드 종료 |
| `machcoordinatoradmin --cluster-status` | 전체 상태 조회 |
| `machcoordinatoradmin --configuration` | Coordinator 설정 조회 |

## 상태값 설명

| 값 | 의미 |
|----|------|
| `normal` | 정상 동작 |
| `primary` | Coordinator Primary |
| `sync-active` | 복제 송신 역할 |
| `sync-standby` | 복제 수신 역할 |
| `inactive` | 비활성 상태 |
| `scrapped` | 장애 감지, 복구 필요 |
| `ddl-incompl` | DDL 처리 미완료 상태 |
| `ddl-recov` | DDL 복구 진행 상태 |
| `**unknown**` | 통신 불가, 노드 다운 의심 |

`leader`처럼 Broker 역할을 나타내는 값은 상태 출력의 Desired/Actual state나 그룹 상태 영역에
표시될 수 있습니다.

## 클라이언트 접속 테스트

Broker 포트로 접속하여 쿼리를 실행합니다.

```bash
machsql -s 192.168.1.11 -u SYS -p MANAGER
Mach> SELECT * FROM V$NODE_STATUS;
```

`V$NODE_STATUS` 뷰에서 등록된 노드 목록과 상태를 확인할 수 있습니다.

---

**다음 읽을 내용**
- [설치 검증 체크리스트](/kr/dbms/installation-deployment-upgrade/validation-checklist/)
