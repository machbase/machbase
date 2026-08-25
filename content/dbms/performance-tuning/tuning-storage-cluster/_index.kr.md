---
type: docs
title: '12.7 스토리지와 Cluster 튜닝'
weight: 70
toc: true
---

스토리지와 Cluster 튜닝은 workload 측정, 장애 복구 목표, node별 자원 사용량을 근거로
진행합니다. 고정 hardware 사양이나 임의의 property 값을 모든 환경에 적용하지 않습니다.

<a id="tuning-storage-checkpoint"></a>

## 스토리지와 checkpoint

다음 항목을 같은 시각 범위에서 비교합니다.

- 입력 rows/s와 ack 지연
- query 응답 시간과 읽기량
- device별 IOPS, throughput, queue, latency
- checkpoint 시작·종료와 소요 시간
- memory·swap 변화
- 장애 후 허용 가능한 recovery 시간

```bash
iostat -x 1 5
df -h
```

checkpoint 간격과 I/O 관련 property는 현재값을
[설정 레퍼런스](/dbms/reference/configuration/dictionary-configuration/)에서 확인합니다.
한 번에 하나만 변경하고, restart 필요 여부와 rollback 값을 기록합니다.

## 경로와 용량

- data, backup, export 경로의 소유권과 여유 공간을 확인합니다.
- 같은 physical device에 경로를 나눴다는 이유만으로 I/O가 분산된다고 가정하지 않습니다.
- 운영 중 data file을 수동 이동하지 않습니다.
- 보존 정책과 backup 공간 증가를 함께 계산합니다.
- filesystem·mount option 변경은 지원 범위와 recovery 절차를 검증합니다.

오래된 데이터는 내부 partition table 이름을 직접 찾아 삭제하지 않습니다. table type별
`DELETE ... BEFORE`, retention, backup 정책 등 공개 SQL과 운영 기능을 사용합니다.

<a id="performance-considerations-cluster-edition"></a>

## Cluster 측정

client, Broker, Warehouse, Coordinator의 지표를 분리해 봅니다.

| 구간 | 확인 |
|------|------|
| client → Broker | connection, round trip, batch 크기 |
| Broker | session, routing, CPU·network |
| Warehouse | node별 입력·query·disk 편차 |
| node 간 통신 | bandwidth, packet loss, latency |
| Coordinator | node 상태와 disk-full 정책 |

특정 node에 부하가 몰리면 tag·key 분포, routing, warehouse group, node별 storage와
network를 함께 확인합니다. `TAG_PARTITION_COUNT`를 cluster node 분산 제어값으로
사용하지 않습니다.

## Property 변경 원칙

- 이름, 허용 범위, 기본값은 설치된 버전의 설정 레퍼런스에서 확인합니다.
- 임의의 추천 숫자보다 현재 baseline과 목표를 기록합니다.
- buffer를 키울 때 throughput뿐 아니라 memory와 tail latency를 측정합니다.
- replication 관련 값을 바꾸기 전에 정상·장애 복구 시간을 모두 비교합니다.
- disk-full 상·하한에는 hysteresis를 두고 실제 증설·정리 절차와 연결합니다.
- edition별 미지원 기능은 [지원 범위](/dbms/reference/support-scope-constraints/)에서
  확인합니다.

## 변경 체크리스트

1. node와 구간별 병목 근거가 있는가
2. 설정 현재값과 출처를 기록했는가
3. staging에서 정상·장애 시나리오를 측정했는가
4. node별 배포 순서와 restart 필요 여부를 확인했는가
5. 결과가 나쁘면 되돌릴 값과 절차가 있는가
6. 변경 후 backup·recovery 검증까지 수행했는가
