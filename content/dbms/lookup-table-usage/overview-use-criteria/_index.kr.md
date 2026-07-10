---
title: '9.1 개요와 사용 기준'
weight: 10
toc: true
---

LOOKUP 테이블은 기준 코드, 장비 마스터, 임계값, 설정값처럼 비교적 작고 자주 참조되는 데이터를 저장하는 테이블이다. 데이터는 영속 저장되며, `PRIMARY KEY`를 기준으로 빠르게 조회하고 갱신한다.

<a id="overview-lookup-characteristics"></a>

## LOOKUP 테이블의 특성

LOOKUP 테이블은 `CREATE LOOKUP TABLE` 문으로 생성하며, `PRIMARY KEY`가 필수이다.

```sql
CREATE LOOKUP TABLE sensor_master (
    sensor_id VARCHAR(64) PRIMARY KEY,
    site      VARCHAR(32),
    unit      VARCHAR(16),
    status    VARCHAR(16)
);
```

LOOKUP 테이블의 주요 특성은 다음과 같다.

| 항목 | 내용 |
|------|------|
| 주요 용도 | 코드 테이블, 장비 마스터, 임계값, 참조 데이터 |
| 필수 조건 | `PRIMARY KEY` 필요 |
| 저장 방식 | 영속 저장 |
| 조회 패턴 | PK 조회, 일반 조건 조회, 다른 테이블과 JOIN |
| 변경 패턴 | INSERT, UPDATE, DELETE |
| 부가 기능 | SEQUENCE 컬럼, Append 중복 키 정책 |

<a id="overview-lookup-use-criteria"></a>

## 사용 기준

다음 조건에 해당하면 LOOKUP 테이블을 사용한다.

- 데이터 건수가 상대적으로 작고 전체 데이터가 자주 참조된다.
- 코드, 이름, 위치, 단위, 상태 같은 기준 정보를 관리한다.
- TAG 또는 LOG 테이블의 원본 데이터에 설명 정보를 JOIN해야 한다.
- 임계값이나 설정값처럼 운영 중 변경될 수 있는 참조값을 저장한다.
- `PRIMARY KEY`로 행을 명확하게 식별할 수 있다.

예를 들어 센서 마스터와 TAG 데이터를 결합하면 위치와 단위를 함께 조회할 수 있다.

```sql
SELECT d.name, m.site, m.unit, d.time, d.value
FROM sensor_data d
JOIN sensor_master m ON d.name = m.sensor_id
WHERE m.status = 'ACTIVE'
  AND d.time >= NOW - 3600000000000;
```

<a id="overview-lookup-not-use"></a>

## 다른 테이블을 검토할 경우

다음 요구사항에는 다른 테이블 타입을 검토한다.

| 요구사항 | 권장 테이블 |
|----------|-------------|
| 대량 시계열 계측 데이터 저장 | TAG |
| append 중심 원본 이벤트 저장 | LOG |
| 트랜잭션과 관계형 업무 처리가 필요한 데이터 | RDB |
| 서버 메모리에서만 유지할 최신 상태 캐시 | VOLATILE |

LOOKUP 테이블은 참조 데이터에 적합하지만, 대량 원본 로그나 센서 계측값을 계속 쌓는 용도에는 맞지 않는다. 원본 데이터는 LOG 또는 TAG 테이블에 저장하고, LOOKUP 테이블에는 해당 데이터를 해석하는 기준 정보를 저장한다.

<a id="overview-lookup-design-flow"></a>

## 설계 순서

LOOKUP 테이블을 설계할 때는 다음 순서로 결정한다.

1. 행을 식별할 `PRIMARY KEY`를 정한다.
2. 자연키를 사용할지, SEQUENCE 기반 대리키를 사용할지 결정한다.
3. 자주 조회하거나 JOIN하는 컬럼에 인덱스를 추가한다.
4. 운영 중 갱신되는 컬럼과 불변 컬럼을 구분한다.
5. 대량 변경 전에는 대상 범위를 확인하는 쿼리를 준비한다.

스키마와 키 설계는 [테이블 구조와 스키마](/dbms/lookup-table-usage/table-structure-schema/)와 [PRIMARY KEY 정책](/dbms/lookup-table-usage/primary-key-policy/)에서 다룬다.
