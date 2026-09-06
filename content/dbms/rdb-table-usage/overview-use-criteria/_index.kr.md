---
title: '8.1 개요와 사용 기준'
weight: 10
toc: true
aliases:
  - /dbms/rdb-table-usage/patterns-scenarios/
---

TRANSACTION 테이블은 Machbase에서 관계형 데이터 모델을 사용하기 위한 테이블 타입입니다. INSERT, SELECT, UPDATE, DELETE를 모두 사용하고, PRIMARY KEY와 보조 인덱스를 기반으로 업무 데이터, 마스터 데이터, 집계 결과를 관리합니다.

<a id="overview-rdb-characteristics"></a>

## TRANSACTION 테이블의 특성

TRANSACTION 테이블은 다음 세 문법으로 생성할 수 있습니다.

- `CREATE TABLE`: 테이블 유형을 생략하는 기본 문법
- `CREATE TRANSACTION TABLE`: 전체 테이블 유형 이름을 명시하는 문법
- `CREATE TXN TABLE`: 축약형을 사용하는 문법

세 문법은 동일한 TRANSACTION 테이블을 생성합니다. LOG 테이블은 `CREATE LOG TABLE`로
명시해야 하며, 이전 공개 명칭인 `RDB`와 축약형 `TRX`는 지원하지 않습니다.

```sql
CREATE TRANSACTION TABLE order_history (
    order_id  LONG PRIMARY KEY,
    item_id   INTEGER,
    qty       INTEGER,
    amount    DOUBLE,
    status    VARCHAR(16)
);
```

TRANSACTION 테이블의 주요 특성은 다음과 같습니다.

| 항목 | 내용 |
|------|------|
| 주요 용도 | 관계형 업무 데이터, 마스터 데이터, 집계 결과, 상태 관리 |
| 주요 DML | INSERT, SELECT, UPDATE, DELETE |
| 키와 인덱스 | PRIMARY KEY, UNIQUE INDEX, 일반 인덱스 |
| 트랜잭션 | TRANSACTION DML에 `BEGIN`, `COMMIT`, `ROLLBACK` 지원 |
| 부가 기능 | AUTO_INCREMENT, JSON 경로 인덱스, 백업·마운트 |
| 에디션 | Standard Edition에서만 사용 |

<a id="overview-rdb-use-criteria"></a>
<a id="use-cases-rdb"></a>

## 사용 기준

다음 조건에 해당하면 TRANSACTION 테이블을 사용합니다.

- 행 단위 UPDATE와 DELETE가 필요합니다.
- PRIMARY KEY 또는 인덱스 기반으로 특정 행을 자주 조회합니다.
- TRANSACTION DML을 트랜잭션으로 하나의 작업 단위로 묶어야 합니다.
- TAG, LOG 테이블의 원본 데이터를 집계한 결과를 업무 테이블로 관리합니다.
- JSON 컬럼과 JSON path 인덱스를 관계형 조회와 함께 사용해야 합니다.
- 백업·마운트 대상에 포함되는 관계형 데이터를 관리합니다.

| 적합한 데이터 유형 | 설명 |
|--------------------|------|
| 주문·거래 이력 | 상태 변경, 조회와 삭제 |
| 설비 이력 | 점검 결과 수정과 이력 조회 |
| 재고 관리 | 수량 갱신과 업무 key 조회 |
| 관계형 참조 이력 | 명시적 transaction과 일반 관계형 DML |
| 이벤트 상태 관리 | 상태 column UPDATE가 필요한 업무 |

```sql
CREATE TRANSACTION TABLE inventory (
    item_id LONG PRIMARY KEY,
    qty     INTEGER
);

INSERT INTO inventory VALUES (42, 10);

BEGIN;
UPDATE inventory SET qty = qty - 1 WHERE item_id = 42;
INSERT INTO order_history VALUES (1001, 42, 1, 19900, 'ORDERED');
COMMIT;

DROP TABLE inventory;
DROP TABLE order_history;
```

<a id="overview-rdb-not-use"></a>

## 다른 테이블을 검토할 경우

다음 요구사항에는 다른 테이블 타입을 검토합니다.

| 요구사항 | 권장 테이블 |
|----------|-------------|
| 센서 이름과 시간축 기준의 대량 계측 데이터 | TAG |
| append 중심 원본 로그와 이벤트 | LOG |
| 작은 기준 코드와 참조 데이터 | LOOKUP |
| 재시작 후 사라져도 되는 인메모리 상태 캐시 | VOLATILE |

TRANSACTION 테이블은 관계형 갱신과 조회에 적합하지만, 초고속 append 중심 원본 수집에는 LOG 또는 TAG 테이블이 더 적합합니다. 원본은 LOG/TAG에 저장하고, 업무 상태나 집계 결과만 TRANSACTION 테이블로 관리하는 구성을 우선 검토합니다.

Cluster Edition에서는 타입을 생략한 `CREATE TABLE`, `CREATE TRANSACTION TABLE`, `CREATE TXN TABLE`을
모두 지원하지 않습니다. Cluster Edition에서 LOG 테이블을 만들 때는 `CREATE LOG TABLE`을
사용합니다.

<a id="overview-rdb-design-flow"></a>

## 설계 순서

TRANSACTION 테이블 설계 시 다음 순서로 결정합니다.

1. 행을 식별할 PRIMARY KEY를 정합니다.
2. 자동 번호가 필요하면 `AUTO_INCREMENT` 사용 여부를 결정합니다.
3. 중복을 허용하지 않을 업무 키에는 UNIQUE INDEX를 생성합니다.
4. 조회, UPDATE, DELETE 조건에 맞춰 일반 인덱스를 설계합니다.
5. 트랜잭션 경계를 정하고 장시간 열린 트랜잭션을 피합니다.
6. 백업, 복원, 읽기 전용 마운트 절차를 운영 정책에 포함합니다.

스키마 설계는 [테이블 구조와 스키마](/dbms/rdb-table-usage/table-structure-schema/)에서, 트랜잭션은 [트랜잭션](/dbms/rdb-table-usage/transaction/)에서 다룹니다.
