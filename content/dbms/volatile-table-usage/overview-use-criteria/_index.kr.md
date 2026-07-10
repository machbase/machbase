---
title: '10.1 개요와 사용 기준'
weight: 10
toc: true
---

VOLATILE 테이블은 데이터를 메모리에 저장하는 임시 테이블이다. 서버가 재시작되면 데이터가 소멸하므로, 재생성 가능한 최신 상태, 임시 집계, 세션 간 공유 캐시 용도로 사용한다.

<a id="overview-volatile-characteristics"></a>

## VOLATILE 테이블의 특성

VOLATILE 테이블은 `CREATE VOLATILE TABLE` 문으로 생성한다.

```sql
CREATE VOLATILE TABLE sensor_latest (
    sensor_id  VARCHAR(64) PRIMARY KEY,
    value      DOUBLE,
    updated_at DATETIME
);
```

VOLATILE 테이블의 주요 특성은 다음과 같다.

| 항목 | 내용 |
|------|------|
| 주요 용도 | 최신 상태 캐시, 임시 집계, 중간 결과 |
| 저장 위치 | 메모리 |
| 재시작 후 데이터 | 소멸 |
| 공유 범위 | 서버 수준 공유 |
| 키 | PRIMARY KEY 선택 |
| 주요 기능 | UPDATE, DELETE, `ON DUPLICATE KEY UPDATE`, Red-Black 트리 인덱스 |
| 백업 | 지원하지 않음 |

<a id="overview-volatile-use-criteria"></a>

## 사용 기준

다음 조건에 해당하면 VOLATILE 테이블을 사용한다.

- 서버 재시작 후 데이터가 없어져도 된다.
- 원본 데이터에서 언제든 다시 계산하거나 재구성할 수 있다.
- 최신 상태, 최근 집계, 임시 작업 결과를 빠르게 조회해야 한다.
- 여러 세션에서 같은 임시 상태를 공유해야 한다.
- 디스크 영속성보다 메모리 기반 응답 시간이 중요하다.

최신 센서 상태를 유지하는 예시는 다음과 같다.

```sql
INSERT INTO sensor_latest VALUES ('TEMP-01', 23.5, NOW)
ON DUPLICATE KEY UPDATE SET value = 23.5, updated_at = NOW;

SELECT *
FROM sensor_latest
WHERE sensor_id = 'TEMP-01';
```

<a id="overview-volatile-not-use"></a>

## 다른 테이블을 검토할 경우

다음 요구사항에는 다른 테이블 타입을 사용한다.

| 요구사항 | 권장 테이블 |
|----------|-------------|
| 재시작 후에도 반드시 보존해야 하는 원본 데이터 | TAG 또는 LOG |
| 기준 코드나 장비 마스터처럼 영속 참조 데이터 | LOOKUP |
| 트랜잭션과 관계형 갱신이 필요한 업무 데이터 | RDB |
| 장기 분석 대상 시계열 데이터 | TAG |

VOLATILE 테이블에만 저장된 데이터는 서버 종료 시 복구할 수 없다. 중요한 데이터는 TAG, LOG, LOOKUP, RDB 중 적합한 영속 테이블에 저장하고, VOLATILE 테이블은 캐시나 중간 결과로 사용한다.

<a id="overview-volatile-design-flow"></a>

## 설계 순서

VOLATILE 테이블 설계 시 다음 순서로 결정한다.

1. 데이터가 재생성 가능한지 확인한다.
2. PRIMARY KEY가 필요한지 결정한다.
3. 예상 행 수와 메모리 사용량을 산정한다.
4. 재시작 후 테이블 생성과 초기 적재 절차를 준비한다.
5. 중요 데이터는 주기적으로 영속 테이블에 플러시한다.

스키마와 PRIMARY KEY 설계는 [테이블 구조와 스키마](/dbms/volatile-table-usage/table-structure-schema/)에서, 재시작 대응은 [재시작과 데이터 소실](/dbms/volatile-table-usage/restart-data-loss/)에서 다룬다.
