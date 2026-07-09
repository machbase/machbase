---
type: docs
title: '제약 조건과 기본값'
weight: 40
---

Machbase 테이블에서 사용할 수 있는 컬럼 제약 조건과 기본값 설정을 정리합니다.

## PRIMARY KEY

VOLATILE, LOOKUP, RDB 테이블의 컬럼에 지정할 수 있습니다. PRIMARY KEY로 지정된 컬럼은 값의 중복을 허용하지 않습니다. LOOKUP/VOLATILE은 Red-Black Tree 인덱스를 사용하고, RDB는 BTREE 인덱스로 표시됩니다.

- **LOOKUP**: PRIMARY KEY 필수 (PK 없이 생성 불가)
- **VOLATILE**: PRIMARY KEY 선택적. 단, `INSERT ... ON DUPLICATE KEY UPDATE` 구문 사용 시 필수
- **RDB**: PRIMARY KEY 선택적

```sql
-- LOOKUP: PK 필수
CREATE LOOKUP TABLE alarm_threshold (
    sensor_id VARCHAR(40) PRIMARY KEY,
    high_limit DOUBLE,
    low_limit  DOUBLE
);

-- VOLATILE: PK 지정 시 UPSERT 가능
CREATE VOLATILE TABLE device_status (
    device_id VARCHAR(40) PRIMARY KEY,
    status    VARCHAR(20),
    value     DOUBLE,
    updated_at DATETIME
);

-- RDB: PK 선택 (지정 시 중복 불가)
CREATE RDB TABLE orders (
    order_id INTEGER PRIMARY KEY,
    product  VARCHAR(100),
    qty      INTEGER
);
```

## NOT NULL

LOG 테이블 컬럼에 사용할 수 있습니다. 해당 컬럼에 NULL 삽입을 금지합니다.

```sql
CREATE TABLE sensor_log (
    sensor_id VARCHAR(40) NOT NULL,
    ts        DATETIME,
    value     DOUBLE
);
```

TAG, VOLATILE, LOOKUP 테이블은 NOT NULL 제약을 별도로 선언하지 않아도 PK 컬럼은 자동으로 NOT NULL이 적용됩니다.

## DEFAULT

일반 `CREATE TABLE` 경로에서는 제한적으로 `DATETIME DEFAULT SYSDATE`를 사용할 수 있습니다.
RDB 테이블은 컬럼 생성 및 `ALTER TABLE ... ADD COLUMN`에서 DEFAULT를 사용할 수 있습니다.
그 외 기본값이 필요하면 INSERT 문이나 애플리케이션 입력 단계에서 값을 명시합니다.

```sql
CREATE RDB TABLE orders_default_example (
    order_id INTEGER,
    status   VARCHAR(20),
    discount DOUBLE,
    created_at DATETIME DEFAULT SYSDATE
);

INSERT INTO orders_default_example
    (order_id, status, discount)
VALUES
    (1, 'PENDING', 0.0);

ALTER TABLE orders_default_example ADD COLUMN (score INTEGER DEFAULT 7);
```

## 시스템 자동 생성 컬럼

LOG 테이블에는 `_ARRIVAL_TIME`과 `_RID` 시스템 컬럼이 자동으로 추가됩니다. TAG, VOLATILE,
LOOKUP 테이블에는 `_RID`이 내부 행 식별자로 추가됩니다. RDB 테이블에는 `_ARRIVAL_TIME`이
자동 추가되지 않습니다.

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| `_ARRIVAL_TIME` | DATETIME | LOG 레코드 삽입 시점의 시스템 시각. Retention과 보존형 DELETE 기준이 됩니다 |
| `_RID` | LONG | 비-RDB 테이블의 내부 행 식별자. 시스템이 자동 부여하며 사용자 변경 불가 |

```sql
-- _RID로 특정 레코드 검색
SELECT * FROM sensor_log WHERE _RID = 1234;

-- _ARRIVAL_TIME으로 최근 1시간 데이터 조회
SELECT * FROM sensor_log WHERE _ARRIVAL_TIME > NOW - 3600000000000;
```

## 테이블 타입별 제약 조건 지원 범위

| 제약 조건 | TAG | LOG | RDB | VOLATILE | LOOKUP |
|-----------|-----|-----|-----|---------|--------|
| PRIMARY KEY | O (name 컬럼) | X | O (선택) | O (선택) | O (필수) |
| NOT NULL | X | O | O | X | X |
| DEFAULT | X | 제한적 | O | 제한적 | 제한적 |
| UNIQUE | X | X | O (UNIQUE INDEX) | X | X |
| FOREIGN KEY | X | X | X | X | X |

> FOREIGN KEY 제약은 지원하지 않습니다. 참조 무결성은 애플리케이션 레이어에서 관리해야 합니다.
