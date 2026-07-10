---
title: '9.3 생성, 변경, 삭제'
weight: 30
toc: true
---
LOOKUP 테이블의 생성, 변경, 삭제 방법을 다룬다.


<a id="original-85-creating-lookup-tables"></a>

## Lookup 테이블 생성 및 관리

참조 테이블을 생성하는 방법은 다음과 같다. LOOKUP 테이블은 반드시 `PRIMARY KEY`를 지정해야 한다.

<a id="create-lookup-table"></a>

## LOOKUP 테이블 생성

```sql
CREATE LOOKUP TABLE lktable (id INTEGER PRIMARY KEY, name VARCHAR(20));
```

운영에서 사용하는 기준 정보는 의미 있는 컬럼명을 사용해 정의한다.

```sql
CREATE LOOKUP TABLE equipment_master (
    equip_id   LONG PRIMARY KEY,
    equip_name VARCHAR(128),
    location   VARCHAR(64),
    status     VARCHAR(16),
    updated_at DATETIME
);
```

`PRIMARY KEY`는 행을 고유하게 식별하고 UPDATE, DELETE, JOIN의 기준이 된다. 여러 컬럼 조합이 비즈니스 키라면 조합 문자열을 별도 키 컬럼으로 만들거나 SEQUENCE 기반 대리키를 사용한다.

```sql
CREATE LOOKUP TABLE product_region_price (
    price_key  VARCHAR(64) PRIMARY KEY,
    product_id VARCHAR(32),
    region     VARCHAR(16),
    price      DOUBLE
);
```

<a id="create-lookup-sequence"></a>

## SEQUENCE 컬럼 사용

자동 증가 번호가 필요하면 `LONG PROPERTY(SEQUENCE=1)` 컬럼을 사용한다. 입력 시에는 `NEXTVAL()` 함수로 다음 값을 가져온다.

```sql
CREATE LOOKUP TABLE alarm_history (
    seq         LONG PROPERTY(SEQUENCE=1) PRIMARY KEY,
    sensor_id   VARCHAR(64),
    alarm_type  VARCHAR(32),
    occurred_at DATETIME,
    message     VARCHAR(256)
);

INSERT INTO alarm_history
VALUES (NEXTVAL(seq), 'TEMP-01', 'HIGH', NOW, '온도 초과');
```

SEQUENCE 컬럼의 세부 정책은 [SEQUENCE 컬럼](/dbms/lookup-table-usage/sequence-column/)에서 다룬다.

<a id="alter-lookup-index"></a>

## 인덱스 추가

자주 조회하거나 JOIN 조건에 사용하는 컬럼에는 인덱스를 추가한다.

```sql
CREATE INDEX idx_equipment_location ON equipment_master(location);
CREATE INDEX idx_equipment_status   ON equipment_master(status);
```

PRIMARY KEY 컬럼에는 기본 인덱스가 생성되므로, 같은 컬럼에 별도 인덱스를 중복 생성하지 않는다. 인덱스가 많으면 입력과 갱신 비용이 증가하므로 조회 조건이 명확한 컬럼에만 추가한다.

<a id="delete-lookup-data"></a>

## 데이터 삭제와 테이블 삭제

행을 삭제하려면 `DELETE` 문을 사용한다. 단건 삭제는 PK 조건을 사용하는 것이 가장 명확하다.

```sql
DELETE FROM equipment_master
WHERE equip_id = 1001;
```

일괄 삭제는 일반 조건식을 사용할 수 있다. 운영 데이터에서는 먼저 같은 조건으로 대상 건수를 확인한다.

```sql
SELECT COUNT(*)
FROM equipment_master
WHERE status = 'RETIRED';

DELETE FROM equipment_master
WHERE status = 'RETIRED';
```

테이블 자체를 삭제하려면 `DROP TABLE`을 사용한다.

```sql
DROP TABLE lktable;
```

`DROP TABLE`은 테이블 정의와 데이터를 모두 삭제한다. 필요한 경우 삭제 전에 백업 또는 내보내기 절차를 수행한다.

<a id="create-lookup-limitations"></a>

## 주의사항

- LOOKUP 테이블은 `PRIMARY KEY`가 필수이다.
- `PRIMARY KEY` 컬럼은 하나만 지정한다.
- `PRIMARY KEY` 값을 변경해야 하면 기존 행을 삭제한 뒤 새 키로 삽입한다.
- 기준 데이터가 커지고 조회·갱신 패턴이 복잡해지면 RDB 테이블을 검토한다.
