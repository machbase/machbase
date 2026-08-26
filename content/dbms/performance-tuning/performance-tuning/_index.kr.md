---
type: docs
title: '12.4 입력 성능 튜닝'
weight: 40
toc: true
aliases:
  - /dbms/performance-tuning/data-input-performance/
---

입력 성능은 경로, row 크기, batch, 동시성, index, storage의 영향을 함께 받습니다. 대표
데이터로 end-to-end 처리량과 ack 지연을 측정해 조정합니다.

## 입력 경로 선택

입력 경로와 SDK·table type별 지원 범위는
[데이터 입력과 반출](/dbms/development-tools-integration/data-input-load-export/)에서 선택하고,
이 페이지에서는 선택한 경로의 처리량과 지연만 조정합니다.

<a id="performance-tuning-bulk"></a>

## 측정 순서

1. 실제와 비슷한 schema, row 크기, index를 준비합니다.
2. connection 1개와 작은 batch로 baseline을 측정합니다.
3. batch 크기를 한 단계씩 늘려 rows/s와 flush·ack 지연을 기록합니다.
4. client CPU·memory와 server CPU·I/O·memory를 함께 관찰합니다.
5. connection 수를 늘리며 총처리량과 tail latency를 비교합니다.
6. 실패·재연결·중복 처리 시나리오를 실행합니다.

일률적인 권장 batch 크기나 thread 수를 사용하지 않습니다. 너무 큰 batch는 memory와
오류 재처리 범위를 늘리고, 너무 작은 batch는 network round trip 비중을 키웁니다.

## Append 운영

Append lifecycle·오류·중복 처리 계약은
[공통 연동 개념](/dbms/development-tools-integration/concepts-common/#append-api-batch)과
[SDK Append matrix](/dbms/development-tools-integration/sdk-support-scope/#append-table-type-matrix)를
따릅니다. 이 페이지에서는 batch 크기, connection 수, rows/s와 tail latency만 측정합니다.

## 파일 적재

파일 형식 검증, bad file, exit code와 최종 row 확인은
[데이터 입력과 반출](/dbms/development-tools-integration/data-input-load-export/)을 정본으로
사용합니다. 여기서는 같은 검증이 끝난 workload의 성능만 비교합니다.

## 병목 분류

| 관찰 | 다음 확인 |
|------|-----------|
| client CPU 포화 | serialization, 변환, logging |
| network wait 증가 | batch, round trip, packet loss |
| server CPU 포화 | index 수, SQL parse, 동시성 |
| storage latency 증가 | checkpoint, device queue, 보존 작업 |
| memory 증가 | batch buffer, connection 수, cache |
| 일부 node만 느림 | key 분포, routing, node별 자원 |

## 변경 전후

처리량만 높이고 데이터 유실·지연을 숨기지 않습니다. 성공 row 수, 실패 row 수, end-to-end
지연, server 반영 시각을 함께 검증하고, 변경이 query 성능과 recovery 시간에 미치는 영향도
확인합니다.
