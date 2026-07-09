---
type: docs
title: '2.1.2 쓰기 중심 워크로드와 append-only 모델'
weight: 20
---

Machbase DBMS가 초당 수백만 건의 시계열 입력을 처리할 수 있는 근거는 LOG/TAG 테이블의 append 중심 모델에 있습니다. 데이터를 먼저 빠르게 추가하고, 과거 행을 임의로 갱신하는 경로를 제한해 행 단위 잠금과 트랜잭션 롤백 오버헤드를 줄이는 구조입니다.

## append-only 모델이란

append 중심 모델에서는 새로운 이벤트나 측정값을 기존 행의 변경이 아니라 새 행의 추가로 표현합니다. LOG 테이블은 이 원칙을 가장 엄격하게 따르고, TAG 테이블은 태그와 시간 범위를 명확히 지정한 data UPDATE만 제한적으로 허용합니다. 이 단순한 원칙이 아래와 같은 성능상 이점을 만들어 냅니다.

**행 단위 잠금이 없다**

전통적인 RDBMS에서 `UPDATE`는 해당 행에 잠금을 걸고, 다른 세션이 같은 행에 접근하면 대기가 발생합니다. LOG/TAG 입력 경로는 과거 행을 일반적인 CRUD 방식으로 갱신하지 않도록 설계되어, 수천 개의 쓰기 스레드가 낮은 경합으로 동시에 동작할 수 있습니다.

**순차 쓰기에 최적화된다**

새 데이터는 항상 파티션의 끝에 추가됩니다. 이 순차적 특성 덕분에 디스크 쓰기가 랜덤 I/O 없이 연속으로 이루어지고, 컬럼 지향 압축도 더 높은 비율로 적용됩니다.

**롤백 로그가 줄어든다**

일반적인 트랜잭션 업데이트 경로를 타지 않으므로 undo 로그가 최소화됩니다. 실패 시 정리해야 할 상태가 단순합니다.

## 테이블 유형별 쓰기 제약

append-only 원칙은 테이블 유형마다 다르게 적용됩니다.

| 테이블 유형 | INSERT | UPDATE | DELETE |
| --- | --- | --- | --- |
| LOG | 가능 | 불가 | `BEFORE`, `OLDEST`, `EXCEPT` 등 시간/보존 조건 기반 |
| TAG | 가능 | 가능 (Standard Edition, 태그 선택자와 시간축 조건 필요) | `BEFORE` 또는 태그/축 조건 기반 |
| LOOKUP | 가능 | Primary key 조건 기반 | Primary key 조건 기반 |
| VOLATILE | 가능 | Primary key 조건 기반 | Primary key 조건 기반 |
| RDB | 가능 | 일반 WHERE 조건 기반 | 일반 WHERE 조건 기반 |

LOG와 TAG 테이블이 append-only의 핵심입니다. LOOKUP과 VOLATILE은 기준 정보와 세션성 데이터를 위해
UPDATE/DELETE를 지원하지만, 현재 UPDATE/DELETE 조건은 Primary key equality 형태로 제한됩니다.
고속 대량 입력보다는 소규모 참조 데이터 관리에 사용합니다. RDB 테이블은 관계형 업무 데이터를
Machbase 안에서 다루기 위한 행 지향 테이블이며, append-only 설계 대상이 아닙니다.

## 쓰기 경로: INSERT vs APPEND

Machbase에서 대량 데이터를 입력하는 방법은 두 가지입니다.

**SQL `INSERT`**

표준 SQL 문장으로 한 번에 한 행씩 입력합니다. 네트워크 왕복과 파싱 오버헤드가 있어 소량 입력이나 테스트에 적합합니다.

```sql
INSERT INTO sensor_log VALUES (TO_DATE('2026-07-03 09:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'pump01', 23.5);
```

**SDK APPEND**

Machbase 전용 APPEND 프로토콜로 여러 행을 배치로 전송합니다. 네트워크 왕복을 최소화하고 서버 측 파싱 비용을 줄여, 같은 양의 데이터를 `INSERT`보다 수십 배 빠르게 입력할 수 있습니다. 실시간 수집기나 데이터 파이프라인에서는 APPEND를 기본으로 사용합니다.

고속 입력이 필요한 환경에서는 `INSERT` 대신 APPEND 프로토콜을 먼저 검토하십시오. 자세한 내용은 [데이터 입력 방식 선택](/dbms/data-input-load-export/)을 참고합니다.

## append-only가 가져오는 설계 제약

append-only 모델은 성능상 이점이 크지만, 설계 시 염두에 두어야 할 제약이 있습니다.

**잘못 입력된 데이터를 수정할 때 대상 범위를 제한해야 한다**

LOG 테이블에 잘못된 값을 넣으면 해당 행을 수정하는 것이 아니라, 보정 이벤트를 추가하거나
시간 범위로 삭제한 뒤 재입력해야 합니다. TAG 테이블의 실제 시계열 값은 `UPDATE`로 정정할
수 있지만, 태그 선택자(`=`, `IN`, `LIKE`)와 최소 한쪽 이상의 시간축 조건이 필요하며 태그명,
시간축 컬럼, hidden/system 컬럼, metadata 컬럼은 data UPDATE로 변경할 수 없습니다.
이력 보존이 필요하면 보정 컬럼이나 보정 이력 테이블을 함께 사용합니다([TAG 데이터 보정 설계](/dbms/tag-table-usage/tag-data-update-correction/design-correction-tag/) 참고).

**스키마 변경이 제한된다**

데이터가 적재된 LOG/TAG 테이블의 컬럼 타입을 변경하거나 컬럼을 삭제하는 DDL은 지원되지 않습니다. 스키마 설계는 운영 전에 신중하게 결정해야 합니다.

**데이터 볼륨 관리가 필요하다**

데이터를 수정 없이 계속 추가하면 저장 공간이 증가합니다. 보관 정책(Retention Policy)으로 오래된 데이터를 자동 삭제하거나, Rollup으로 집계된 형태로 전환하는 설계가 필요합니다.

## 다음 읽을 내용

- [시간 모델과 `_arrival_time`](../time-model-arrival-time/) — 테이블 유형별 시간 표현 방식
- [데이터 입력 방식 선택](/dbms/data-input-load-export/) — INSERT vs APPEND vs Collector 비교
- [Retention Policy의 역할](/dbms/core-concepts/features-concepts/role-retention-policy/) — 데이터 보관 정책 개념
