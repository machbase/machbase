---
type: docs
title: '14.10 Cluster 운영'
weight: 110
toc: true
---

Cluster 작업은 topology, node 역할, replication·data 상태를 확인한 뒤 검증된 runbook으로
수행합니다. 이 페이지는 안전한 확인 순서만 제공하며, start·stop·remove·destroy 명령을
복사 실행하는 절차로 제공하지 않습니다.

## 구성 요소

| 역할 | 확인 |
|------|------|
| Coordinator | topology와 node state |
| Deployer | package와 node 배포 |
| Broker | client connection과 query routing |
| Warehouse | data 저장·query 처리 |
| Lookup | 참조 데이터 service |

node 수와 배치는 가용성·처리량·장애 영역 요구사항을 근거로 설계합니다. 고정 node 수나
hardware 사양을 모든 환경에 적용하지 않습니다.

<a id="status-check-state-cluster"></a>

## 상태 확인

변경 전후에 Coordinator 관점의 전체 topology와 각 node의 process·resource를 확인합니다.
상태 문자열과 명령 option은 설치된 도구의 help를 기준으로 합니다.

```bash
machcoordinatoradmin --help
machclusterctl --help
```

- expected node가 모두 등록돼 있는가
- node role, host, port, group이 배포 기록과 같은가
- service·replication·scrap 상태가 정상인가
- node별 CPU·memory·disk·network 편차가 있는가
- Broker를 통한 실제 connection·query가 성공하는가

<a id="machclusterctl-connect-export"></a>

## Connect와 설정 export

`machclusterctl connect`로 접속할 때 대상 Broker와 native port를 명시하고 실제
`CURRENT_DATABASE()`와 표본 query를 확인합니다. 설정 export에는 host·port·경로와 운영
정보가 포함될 수 있으므로 접근 권한을 제한하고, import 전에 diff를 검토합니다.

<a id="node-start-cluster"></a>

## Node 시작·종료

node 제어 전 다음을 확인합니다.

1. 대상 node 이름·alias·host·role
2. client connection과 진행 중 query·Appender
3. Warehouse group의 redundancy와 data state
4. node 중지 시 남은 capacity
5. start·stop 순서와 rollback
6. 유지보수 뒤 정상 판정 기준

강제 종료는 정상 종료가 반복해서 실패하고 data·recovery 영향을 판단한 경우에만
사용합니다. 단순 timeout에 바로 kill을 실행하지 않습니다.

<a id="machclusterctl-start-stop-destroy"></a>

## Cluster 전체 제어와 destroy

전체 start·stop은 Coordinator, Deployer, Broker, Warehouse, Lookup 의존 순서를 현재
release runbook에서 확인합니다. `destroy`는 topology와 node data를 제거할 수 있는
파괴적 작업입니다.

- 이름이 비슷한 다른 cluster가 아닌지 확인
- 최신 backup과 restore 검증
- service owner 승인과 client 차단
- 외부 `DBS_PATH` 포함 삭제 범위 확인
- rollback 불가능 영역 명시
- 실행 후 host별 잔여 process·path 확인

일반 상태 복구에 `destroy`를 사용하지 않습니다.

<a id="node-cluster"></a>

## Node 추가·제거

추가 전 package·version·port·path·filesystem·network를 확인합니다. 제거 전에는 data
redundancy와 migration 완료, node를 참조하는 alias·group·monitoring을 확인합니다. node
remove가 home과 data path를 삭제할 수 있으므로 정확한 범위는 해당 명령 help와 staging
검증으로 확인합니다.

<a id="state-alter-status-cluster"></a>

## 상태 변경

Broker 비활성화, Warehouse group read-only, node scrap 같은 상태 변경은 목적이 다릅니다.
문제 node를 숨기기 위해 상태를 임의 변경하지 않습니다.

| 목적 | 먼저 확인 |
|------|-----------|
| 새 connection 차단 | Broker drain과 기존 connection |
| write 중단 | Warehouse group과 진행 중 Append |
| node 격리 | replication·data 손상 근거 |
| service 복귀 | health, data 동기화, 표본 query |

<a id="recovery-state-status-warehouse"></a>

## Warehouse 복구

1. 장애 시각과 최초 오류를 보존합니다.
2. process, disk, network, replication 상태를 확인합니다.
3. 남은 node의 redundancy와 service 영향을 판단합니다.
4. 단순 restart, reattach, rebuild 중 지원되는 경로를 선택합니다.
5. recovery 진행률과 오류를 관찰합니다.
6. 완료 후 node별 row·시간 범위와 query 결과를 비교합니다.

data 손상 여부를 확인하지 않고 node를 normal로 강제 전환하지 않습니다.

<a id="limitations-cluster"></a>

## 제약과 점검표

edition별 SQL, ROLLUP, backup, ALTER SYSTEM 지원 범위는
[지원 범위](/dbms/reference/support-scope-constraints/)를 확인합니다.

- 모든 node와 client SDK release가 호환되는가
- maintenance 중 허용되는 read·write 범위가 정의됐는가
- backup·restore와 node 복구 훈련이 완료됐는가
- host·port·path를 두 사람이 교차 확인했는가
- monitoring과 alert가 새 topology를 반영하는가
- 변경 후 Broker connection, query, Append, metadata를 검증했는가
