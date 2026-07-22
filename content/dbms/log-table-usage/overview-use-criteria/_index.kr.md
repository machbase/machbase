---
title: '7.1 개요와 사용 기준'
weight: 10
toc: true
---

LOG 테이블은 이벤트, 로그, 패킷, 센서 원시 이벤트처럼 계속 추가되는 데이터를 저장하는 기본 테이블 타입입니다. 입력 시각을 나타내는 `_arrival_time` 컬럼이 자동으로 관리되며, 대량 append와 시간 범위 조회에 맞춰 사용합니다.

<a id="overview-log-characteristics"></a>

## LOG 테이블의 특성

LOG 테이블은 `CREATE LOG TABLE` 문으로 생성합니다. 사용자가 정의한 컬럼 외에 `_arrival_time` 컬럼이 자동으로 추가되어 데이터가 Machbase에 도착한 시각을 기록합니다.

```sql
CREATE LOG TABLE event_log (
    event_time DATETIME,
    device_id  VARCHAR(64),
    level      SHORT,
    message    TEXT
);
```

LOG 테이블의 주요 특성은 다음과 같습니다.

| 항목 | 내용 |
|------|------|
| 주요 용도 | 이벤트 로그, 보안 로그, 네트워크 패킷, 원시 수집 데이터 |
| 기본 시간 | `_arrival_time` 자동 컬럼 |
| 입력 패턴 | append 중심 대량 입력 |
| 조회 패턴 | 시간 범위, 조건 필터, 전문 검색, 네트워크 타입 조건 |
| 변경 제약 | 일반 UPDATE와 임의 조건 DELETE는 사용하지 않음 |
| 보존 관리 | 기간 조건 삭제와 백업 정책으로 관리 |

<a id="overview-log-use-criteria"></a>

## 사용 기준

다음 조건에 해당하면 LOG 테이블을 사용합니다.

- 데이터가 계속 추가되고, 입력 후 수정하지 않습니다.
- 입력 순서와 도착 시각이 중요합니다.
- 최근 구간 또는 특정 기간의 이벤트를 빠르게 조회해야 합니다.
- `TEXT`, `IPV4`, `IPV6` 같은 로그 분석용 타입을 활용합니다.
- 파일, collector, Append API, `LOAD DATA` 등으로 대량 수집합니다.

LOG 테이블은 원본 이벤트를 보존하고, 분석 쿼리나 집계는 별도 테이블 또는 쿼리에서 처리하는 구조에 적합합니다.

```sql
SELECT event_time, device_id, level, message
FROM event_log
WHERE _arrival_time >= NOW - 3600000000000
  AND level >= 3;
```

<a id="overview-log-not-use"></a>

## 다른 테이블을 검토할 경우

다음 요구사항에는 다른 테이블 타입을 검토합니다.

| 요구사항 | 권장 테이블 |
|----------|-------------|
| 센서 이름과 시간축 기준의 계측 데이터 저장 | TAG |
| 코드, 장비 마스터, 임계값 같은 참조 데이터 관리 | LOOKUP |
| 행 단위 UPDATE/DELETE와 트랜잭션이 필요한 업무 데이터 | TRANSACTION |
| 재시작 시 사라져도 되는 최신 상태 캐시 | VOLATILE |

LOG 테이블은 append 중심 구조이므로 잘못 입력된 특정 행을 일반 UPDATE로 수정하는 모델에는 맞지 않습니다. 수정 가능한 기준 정보는 LOOKUP 또는 TRANSACTION 테이블에 분리하고, LOG 테이블에는 변경 이력을 append하는 방식으로 설계합니다.

<a id="overview-log-design-flow"></a>

## 설계 순서

LOG 테이블 설계 시 다음 항목을 먼저 결정합니다.

1. 이벤트 발생 시각 컬럼을 별도로 둘지 결정합니다.
2. 조회 조건에 자주 쓰는 컬럼의 타입을 정합니다.
3. 전문 검색이 필요한 문자열은 `TEXT` 컬럼으로 분리합니다.
4. IP 주소와 포트는 네트워크 타입과 숫자 타입으로 저장합니다.
5. 보존 기간, 삭제 주기, 백업 정책을 정합니다.

스키마 설계는 [테이블 구조와 스키마](/dbms/log-table-usage/table-structure-schema/)를 참고하고, 입력 방식은 [데이터 입력과 변경](/dbms/log-table-usage/data-input-mutation/)에서 다룹니다.
