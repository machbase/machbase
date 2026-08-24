---
type: docs
title: '2.1 데이터 모델 개념'
weight: 10
toc: true
---
Machbase DBMS가 시계열 데이터를 다루는 방식은 일반적인 관계형 데이터베이스와 근본적으로 다릅니다. 시계열 데이터의 특성을 먼저 이해해야 테이블 구조, 입력 방식, 조회 전략을 적절히 선택할 수 있습니다.

이 섹션은 세 가지 핵심 개념을 다룹니다.

- **시계열 데이터 이해하기**: 시계열 데이터와 일반 데이터의 차이, 그에 맞춘 설계 원칙
- **쓰기 중심 워크로드와 append-only 모델**: 고속 입력을 달성하는 구조적 이유와 그에 따르는 제약
- **시간 모델과 `_arrival_time`**: 테이블 유형별 시간 표현 방식과 `_arrival_time`의 역할


<a id="time-series"></a>

## 시계열 데이터 이해하기

시계열 데이터(time-series data)란 시간 순서로 기록된 데이터 포인트의 연속입니다. 각 레코드는 반드시 타임스탬프를 가지며, 그 타임스탬프가 데이터를 다른 레코드와 구별하는 핵심 축이 됩니다. 공장 설비의 온도 측정값, 거래소의 체결 틱, 서버의 CPU 사용률이 모두 여기에 해당합니다.

### 시계열 데이터의 특성

시계열 데이터는 일반적인 업무 데이터와 여러 측면에서 성격이 다릅니다.

**쓰기가 압도적으로 많다**

설비 센서는 초당 수십 번씩 측정값을 보내고, 거래소는 밀리초마다 틱을 생성합니다. "한 건을 정확히 찾아 수정하는" 패턴이 아니라, INSERT가 거의 전부를 차지합니다.

**과거 데이터는 변하지 않는다**

어제 오전 9시에 기록된 센서 값은 오늘 수정될 이유가 없습니다. 한 번 기록되면 그대로 유지되는 성질이 append-only 설계를 가능하게 하고, 행 단위 잠금 없이 고속 입력을 구현하는 근거가 됩니다.

**조회는 시간 범위 중심이다**

"지난 1시간의 평균 온도", "장 마감 직전 10분의 틱 분포", "이번 달 알람 발생 추이"처럼 시간 범위를 기준으로 조회합니다. 특정 레코드를 키로 조회하는 패턴은 드뭅니다.

**최신 데이터가 가장 자주 읽힌다**

모니터링 대시보드는 최근 24시간을 보여주고, 분석가는 지난 주 데이터를 주로 다룹니다. 몇 년 전 데이터는 규정 준수나 장기 트렌드 분석 목적으로만 드물게 접근합니다. 이 패턴이 Retention Policy와 Rollup 설계의 근거입니다.

**집계로 의미가 만들어진다**

원시 측정값 하나가 아니라 일정 시간 구간의 평균·최대·최소·합계가 실제 분석의 재료입니다.
장기간의 원시 데이터를 매번 집계하는 대신 ROLLUP이 미리 계산된 통계를 유지합니다.

### 시계열 데이터의 두 가지 형태

**계측값(measurement)**

센서가 일정한 간격으로 생성하는 정형화된 값입니다. "온도 센서 A가 특정 시각에 23.5°C를 기록했다"처럼 측정 대상(태그), 시각, 값이 고정된 구조를 가집니다. TAG 테이블이 이 형태를 담당합니다.

**이벤트(event)**

주문 체결, 알람 발생, 서비스 장애처럼 사건이 발생할 때마다 생성되는 기록입니다. 발생 빈도가 불규칙하고 컬럼 구성이 다양합니다. LOG 테이블이 이 형태를 담당합니다.

두 형태는 실제 시스템에서 함께 존재합니다. 산업 IoT에서는 설비의 온도·진동이 계측값이고 알람·정비 이력이 이벤트이며, 금융 시스템에서는 호가·체결 틱이 계측값에 가깝고 수신 상태·지연 경보가 이벤트입니다.

### 전통적인 RDBMS와의 차이

| 관점 | 전통적 RDBMS | Machbase (시계열) |
| --- | --- | --- |
| 주요 연산 | UPDATE 중심 | INSERT 중심 |
| 시간의 역할 | 일반 컬럼 | 데이터의 주축 |
| 인덱스 구조 | B-Tree (랜덤 액세스 최적화) | 시간 파티션/시계열 인덱스 기반 |
| 저장 방식 | 행 지향 | 컬럼 지향 |
| 압축 | 행 단위 데이터 특성에 따라 결정 | 컬럼별 반복 패턴을 활용 |
| 보관 정책 | 수동 관리 | Retention Policy / Rollup |

전통적인 RDBMS에서 시계열 워크로드를 처리하면 행 단위 잠금과 트랜잭션 오버헤드가 누적되어 입력 성능이 급격히 저하됩니다. Machbase는 "한 번 쓰고 시간 범위로 읽는" 특성에 맞추어 잠금 없는 append-only 구조를 채택했습니다.

### 다음 읽을 내용

- [쓰기 중심 워크로드와 append-only 모델](/dbms/core-concepts/concepts/#write-oriented-append-only) — 고속 입력 구조의 원리와 제약
- [시간 모델과 `_arrival_time`](#time-model-arrival-time) — 테이블 유형별 시간 표현 방식

<a id="write-oriented-append-only"></a>

## 쓰기 중심 워크로드와 append-only 모델

Machbase DBMS의 LOG/TAG 테이블은 시계열 입력을 위해 append 중심 모델을 사용합니다. 새 행을
연속해서 추가하고 과거 행의 임의 갱신 경로를 제한하여 동시 입력의 경합을 줄입니다.

### append-only 모델이란

append 중심 모델에서는 새로운 이벤트나 측정값을 기존 행의 변경이 아니라 새 행의 추가로 표현합니다. LOG 테이블은 이 원칙을 가장 엄격하게 따르고, TAG 테이블은 태그와 시간 범위를 명확히 지정한 data UPDATE만 제한적으로 허용합니다.

**행 단위 잠금이 없다**

전통적인 RDBMS의 `UPDATE`는 잠금 경합이 발생할 수 있습니다. LOG/TAG 입력 경로는 과거 행을
일반적인 CRUD 방식으로 갱신하지 않으므로 동시 입력 간 경합을 줄일 수 있습니다.

**순차 쓰기에 최적화된다**

새 데이터는 append 경로로 추가됩니다. 이 방식은 순차 입력과 컬럼 지향 압축에 적합합니다.

**롤백 로그가 줄어든다**

LOG/TAG 입력은 일반적인 행 갱신 트랜잭션과 다른 경로를 사용합니다. 완료된 Append 요청은
TRANSACTION 테이블 트랜잭션의 `ROLLBACK` 대상으로 취급하지 않습니다.

### 테이블 유형별 쓰기 제약

append-only 원칙은 테이블 유형마다 다르게 적용됩니다.

| 테이블 유형 | INSERT | UPDATE | DELETE |
| --- | --- | --- | --- |
| LOG | 가능 | 불가 | `BEFORE`, `OLDEST`, `EXCEPT` 등 시간/보존 조건 기반 |
| TAG | 가능 | 가능 (Standard Edition, 태그 선택자와 시간축 조건 필요) | `BEFORE` 또는 태그/축 조건 기반 |
| LOOKUP | 가능 | Primary key 또는 일반 조건식 | Primary key 또는 일반 조건식, 조건 없는 전체 삭제 |
| VOLATILE | 가능 | Primary key 조건 기반 | Primary key 조건 기반 |
| TRANSACTION | 가능 | 일반 WHERE 조건 기반 | 일반 WHERE 조건 기반 |

LOG와 TAG 테이블이 append 중심 모델의 핵심입니다. LOOKUP은 Primary key fast path와 일반
조건식으로 기준 정보를 변경하고, VOLATILE은 Primary key 조건으로 상태 데이터를 변경합니다.
LOOKUP의 조건 없는 DELETE는 모든 행을 삭제합니다.
TRANSACTION 테이블은 관계형 업무 데이터를 Machbase 안에서 다루는 테이블이며 append-only 설계 대상이
아닙니다.

### 쓰기 경로: INSERT vs APPEND

대량 데이터를 입력하는 방법은 두 가지입니다.

**SQL `INSERT`**

표준 SQL 문장으로 한 번에 한 행씩 입력합니다. 네트워크 왕복과 파싱 오버헤드가 있어 소량 입력이나 테스트에 적합합니다.

```sql
INSERT INTO sensor_log VALUES (TO_DATE('2026-07-03 09:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'pump01', 23.5);
```

**SDK APPEND**

Machbase Append API로 여러 행을 배치 전송합니다. 반복 `INSERT`보다 네트워크 왕복과
SQL 파싱 횟수를 줄일 수 있어 지속적인 시계열 수집에 적합합니다.

고속 입력이 필요한 환경에서는 `INSERT` 대신 Append API를 먼저 검토하십시오. 자세한 내용은 [데이터 입력 방식 선택](/dbms/application-integration/data-input-load-export/)을 참고합니다.

### append-only가 가져오는 설계 제약

append-only 모델은 성능상 이점이 크지만 설계 시 염두에 두어야 할 제약이 있습니다.

**잘못 입력된 데이터를 수정할 때 대상 범위를 제한해야 한다**

LOG 테이블에 잘못된 값을 넣으면 해당 행을 수정하는 것이 아니라, 보정 이벤트를 추가하거나
시간 범위로 삭제한 뒤 재입력해야 합니다. TAG 테이블의 실제 시계열 값은 `UPDATE`로 정정할
수 있지만, 태그 선택자(`=`, `IN`, `LIKE`)와 최소 한쪽 이상의 시간축 조건이 필요하며 태그명,
시간축 컬럼, hidden/system 컬럼, metadata 컬럼은 data UPDATE로 변경할 수 없습니다.
이력 보존이 필요하면 보정 컬럼이나 보정 이력 테이블을 함께 사용합니다([TAG 데이터 보정 설계](/dbms/tag-table-usage/tag-data-update-correction/#design-correction-tag) 참고).

**스키마 변경이 제한된다**

데이터가 적재된 LOG/TAG 테이블의 컬럼 타입을 변경하거나 컬럼을 삭제하는 DDL은 지원되지 않습니다. 스키마 설계는 운영 전에 신중하게 결정해야 합니다.

**데이터 볼륨 관리가 필요하다**

데이터를 수정 없이 계속 추가하면 저장 공간이 증가합니다. Retention Policy로 오래된 데이터를 자동 삭제하거나, Rollup으로 집계된 형태로 전환하는 설계가 필요합니다.

### 다음 읽을 내용

- [시간 모델과 `_arrival_time`](#time-model-arrival-time) — 테이블 유형별 시간 표현 방식
- [데이터 입력 방식 선택](/dbms/application-integration/data-input-load-export/) — INSERT vs APPEND vs Collector 비교
- [Retention Policy의 역할](/dbms/core-concepts/features-concepts/#role-retention-policy) — 데이터 보관 정책 개념

<a id="time-model-arrival-time"></a>

## 시간 모델과 _arrival_time

Machbase DBMS에서 시간은 테이블 유형에 따라 다르게 표현됩니다. LOG 테이블은 시스템이 데이터를 수신한 시각을 자동 기록하고, TAG 테이블은 사용자가 명시적으로 정의한 시간 컬럼을 시간 축으로 사용합니다. LOOKUP, VOLATILE, TRANSACTION 테이블에는 필수 시간축이 없으며, 필요하면 일반 DATETIME 컬럼을 정의합니다.

### LOG 테이블의 `_arrival_time`

LOG 테이블을 생성하면 `_arrival_time`이라는 DATETIME 컬럼이 자동으로 추가됩니다. 사용자가 정의하지 않아도 항상 존재하며, 해당 행이 서버에 입력된 시각을 나노초 정밀도로 기록합니다.

```sql
-- 사용자는 두 컬럼만 정의했지만
CREATE LOG TABLE device_events (
    device_id VARCHAR(20),
    status    VARCHAR(20)
);

-- _arrival_time은 자동으로 추가되어 세 컬럼이 존재합니다
-- SHOW CREATE TABLE device_events;
-- => device_id VARCHAR(20), status VARCHAR(20), _arrival_time DATETIME
```

`_arrival_time`은 데이터가 서버에 도달한 시각이므로, 센서 측정 시각과 네트워크 지연이나 수집기 버퍼링 시간만큼 차이가 날 수 있습니다. 이벤트의 실제 발생 시각이 중요하다면 별도 DATETIME 컬럼을 정의해 직접 값을 입력해야 합니다.

#### `_arrival_time` 기반 조회

시간 범위 조회에서 `_arrival_time`을 WHERE 조건에 명시하거나, `DURATION` 구문을 사용합니다.

```sql
-- 직접 조건 지정
SELECT device_id, status
FROM device_events
WHERE _arrival_time >= TO_DATE('2026-07-03 09:00:00', 'YYYY-MM-DD HH24:MI:SS')
  AND _arrival_time <  TO_DATE('2026-07-03 10:00:00', 'YYYY-MM-DD HH24:MI:SS');

-- DURATION 구문 (최근 1시간)
SELECT device_id, status
FROM device_events
DURATION 1 HOUR;
```

`DURATION` 구문은 내부적으로 `_arrival_time`을 기준으로 동작합니다.

### TAG 테이블의 BASETIME 컬럼

TAG 테이블에는 `_arrival_time`이 없습니다. 대신 테이블 생성 시 `BASETIME` 속성을 붙인 DATETIME 컬럼이 시간 축이 됩니다.

```sql
CREATE TAG TABLE sensor_values (
    name  VARCHAR(128) PRIMARY KEY,
    time  DATETIME BASETIME,        -- 사용자 정의 시간 축
    value DOUBLE SUMMARIZED
);
```

`time` 컬럼에 입력하는 값은 센서가 측정한 실제 시각입니다. 서버 수신 시각이 아니라 발생 시각을 직접 제어하므로, 늦게 도착한 데이터도 올바른 시간 위치에 기록됩니다.

```sql
-- 측정 시각을 직접 지정
INSERT INTO sensor_values
VALUES ('temp_sensor_01', TO_DATE('2026-07-03 08:55:00', 'YYYY-MM-DD HH24:MI:SS'), 23.1);
```

### 두 시간 모델의 비교

| 항목 | LOG: `_arrival_time` | TAG: BASETIME 컬럼 |
| --- | --- | --- |
| 설정 방법 | 자동 추가 (사용자 정의 불필요) | `BASETIME` 속성으로 명시 |
| 의미 | 서버 수신 시각 | 사용자가 지정한 이벤트/측정 시각 |
| 정밀도 | 나노초 | 나노초 |
| 늦게 도착한 데이터 | 수신 시각으로 기록됨 | 원래 측정 시각으로 기록 가능 |
| 조회 기준 | `_arrival_time` 또는 `DURATION` | BASETIME 컬럼 이름으로 조회 |

LOOKUP, VOLATILE, TRANSACTION 테이블의 DATETIME 컬럼은 일반 컬럼입니다. 자동 `_arrival_time`이나
`BASETIME` 의미가 붙지 않으므로, 시간 범위 조회나 보관 정책을 시계열 테이블과 같은 방식으로
기대하면 안 됩니다.

### 어느 모델을 선택해야 하는가

**`_arrival_time`(LOG 테이블)이 적합한 경우**

- 서버 수신 순서가 곧 이벤트 순서인 경우
- 데이터 수신 지연이 매우 짧고 무시할 수 있는 경우
- 스키마에 별도 시간 컬럼 없이도 시간 기반 조회가 필요한 경우

**BASETIME(TAG 테이블)이 적합한 경우**

- 센서 측정 시각이 정확해야 하는 계측값 데이터
- 네트워크 지연이나 수집기 버퍼링으로 실제 발생 시각과 수신 시각이 다를 수 있는 경우
- 태그 이름과 시간 축으로 계측값을 조회해야 하는 경우

### 다음 읽을 내용

- [시계열 데이터 이해하기](/dbms/core-concepts/concepts/#time-series) — 시계열 데이터의 본질
- [LOG 테이블 설계](/dbms/log-table-usage/) — `_arrival_time`을 활용한 이벤트 테이블 설계
- [TAG 테이블 설계](/dbms/tag-table-usage/) — BASETIME을 활용한 계측값 테이블 설계
