---
type: docs
title: '12.4 입력 성능 튜닝'
weight: 40
toc: true
---

입력 성능은 경로, row 크기, batch, 동시성, index, storage의 영향을 함께 받습니다. 대표
데이터로 end-to-end 처리량과 ack 지연을 측정해 조정합니다.

## 입력 경로 선택

| 경로 | 적합한 작업 |
|------|-------------|
| 단건 INSERT | 소량 입력, 즉시 결과 확인 |
| prepared batch | 반복 SQL과 중간 규모 batch |
| Append API | 지속적인 TAG·LOG 대량 입력 |
| TRANSACTION transaction | 원자성이 필요한 관계형 DML |
| machloader·csvimport | 큰 파일의 일괄 적재 |

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

- query connection과 Append connection을 분리합니다.
- 대상 table의 컬럼 순서와 타입을 metadata로 확인합니다.
- flush와 close의 성공·실패 건수를 기록합니다.
- error callback·ack를 소비하지 않아 오류가 누적되지 않도록 합니다.
- 재연결 뒤 이전 batch를 다시 보낼 때 중복 정책을 적용합니다.
- 여러 Appender가 같은 key를 보낼 때 ordering 요구사항을 정의합니다.

SDK별 코드는 [11장 개발 및 애플리케이션 연동](/dbms/development-tools-integration/)을 참고합니다.

## 파일 적재

machloader와 csvimport는 작은 표본 파일로 delimiter, encoding, NULL, DATETIME을 먼저
검증합니다. 운영 실행에서는 log와 bad file을 보존하고 exit code, 입력·실패 건수, 대상
table의 최종 시간 범위를 확인합니다.

명령과 옵션은 [데이터 입력과 반출](/dbms/development-tools-integration/data-input-load-export/)을
참고합니다.

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
