---
type: docs
title: '4.2 테이블 타입 선택'
weight: 20
toc: true
---
잘못된 타입 선택은 성능 저하와 기능 제한으로 이어지므로, 설계 초기에 데이터 성격에 맞는 타입을 결정해야 합니다.

- **[테이블 타입 개요](/dbms/data-modeling-table-design/table-types-selection-type/#table-types-type)**
- **[타입 선택 결정 가이드](/dbms/data-modeling-table-design/table-types-selection-type/#selection-decision)**
- **[타입 비교표](/dbms/data-modeling-table-design/table-types-selection-type/#comparison-tag-log-rdb-volatile-lookup)**
- **[RDB vs LOOKUP 비교](/dbms/data-modeling-table-design/table-types-selection-type/#comparison-rdb-vs-lookup)**


<a id="table-types-type"></a>

## 테이블 타입 개요

### TAG 테이블

센서·IoT 기기에서 수집되는 계측값을 저장하는 타입으로, 시간축(BASETIME) 또는 거리축(BASEDISTANCE)을 기준으로 다수의 태그(센서 이름)를 하나의 테이블에서 관리합니다.

```sql
CREATE TAG TABLE sensor_data (
    name   VARCHAR(64) PRIMARY KEY,
    time   DATETIME    BASETIME,
    value  DOUBLE
);
```

- `PRIMARY KEY` 컬럼: 태그(센서) 식별자
- `BASETIME` 컬럼: 시간축 (나노초 정밀도 DATETIME)
- 값 컬럼: DOUBLE, INTEGER 등

### LOG 테이블

시스템 이벤트, 애플리케이션 로그, 네트워크 패킷 등 추가 전용(append-only) 데이터에 적합합니다. `CREATE TABLE` 기본 문법을 사용합니다.

```sql
CREATE TABLE sys_log (
    level    SHORT,
    msg      VARCHAR(512),
    src_ip   IPV4
);
```

- `_arrival_time` 컬럼이 자동 추가됩니다 (나노초 DATETIME).
- UPDATE와 일반 조건 DELETE는 지원하지 않습니다. 보존/정리 목적의 `BEFORE`, `OLDEST`, `EXCEPT` DELETE를 사용합니다.

### RDB 테이블

관계형 구조의 업무 데이터를 저장합니다. Machbase 8.6에서 도입된 타입으로, 일반적인 관계형 테이블처럼 SELECT·INSERT·UPDATE·DELETE를 모두 지원합니다.

```sql
CREATE RDB TABLE product (
    id       INTEGER,
    name     VARCHAR(128),
    category VARCHAR(64),
    price    DOUBLE
);
```

- SELECT, INSERT, UPDATE, DELETE 모두 지원
- UPDATE는 WHERE 조건 유무 모두 지원
- PRIMARY KEY 인덱스 및 보조 인덱스 생성 가능
- Standard Edition 전용

### VOLATILE 테이블

메모리에만 존재하는 임시 테이블입니다. 서버 재시작 시 데이터가 소멸됩니다.

```sql
CREATE VOLATILE TABLE session_cache (
    id     INTEGER PRIMARY KEY,
    val    VARCHAR(256)
);
```

- `PRIMARY KEY` 선택. `ON DUPLICATE KEY UPDATE`나 PK 기반 조회를 사용하려면 지정합니다.
- `ON DUPLICATE KEY UPDATE` 지원
- 세션 간 공유 가능 (서버 수준)

### LOOKUP 테이블

소규모 코드 테이블·기준 정보를 저장하며, 실시간 업데이트가 가능한 참조 데이터에 적합합니다.

```sql
CREATE LOOKUP TABLE code_master (
    code   VARCHAR(16) PRIMARY KEY,
    label  VARCHAR(128)
);
```

- `PRIMARY KEY` 필수
- PRIMARY KEY 기준 UPDATE·DELETE 지원
- 디스크에 영속 저장

<a id="selection-decision"></a>

## 타입 선택 결정 가이드

아래 질문에 순서대로 답하면 적합한 테이블 타입을 결정할 수 있습니다.

### 결정 흐름

```
데이터가 센서/기기 계측값인가?
  ├── YES → 시간축인가?    YES → TAG TABLE (BASETIME)
  │            거리축인가?  YES → TAG TABLE (BASEDISTANCE)
  └── NO  ↓

데이터가 이벤트/로그/패킷인가? (추가 전용)
  ├── YES → LOG TABLE
  └── NO  ↓

데이터가 코드 테이블/기준 정보인가? (소규모, PK 기반 UPDATE)
  ├── YES, 건수 < 수백만 → LOOKUP TABLE
  └── NO  ↓

데이터가 서버 재시작 시 폐기 가능한 인메모리 상태/캐시인가?
  ├── YES → VOLATILE TABLE
  └── NO  ↓

일반 관계형 업무 데이터 (UPDATE/DELETE/SELECT/INSERT 모두 필요)
  └── RDB TABLE
```

### 주요 판단 기준

| 질문 | 타입 |
|------|------|
| 시간 또는 거리 기반 계측값인가? | TAG |
| 추가만 하고 수정·삭제 불필요? | LOG |
| PRIMARY KEY 기준 UPDATE/DELETE 필요? 소규모? | LOOKUP |
| 서버 재시작 시 데이터가 사라져도 되는가? | VOLATILE |
| 일반 관계형 업무 (INSERT/UPDATE/DELETE/SELECT)? | RDB |

### 주의사항

- TAG 테이블에 이벤트 로그를 저장하면 태그 수 폭발로 성능이 저하됩니다.
- LOG 테이블은 UPDATE와 일반 조건 DELETE가 불가하므로 수정 가능성이 있는 데이터에는 부적합합니다. 보존/정리 목적의 `BEFORE`, `OLDEST`, `EXCEPT` DELETE만 사용합니다.
- RDB 테이블은 Standard Edition 전용입니다. Cluster Edition 환경에서는 LOOKUP(소규모) 또는 외부 RDBMS를 활용합니다.
- VOLATILE 테이블은 서버 재시작 시 데이터가 소멸됩니다.

<a id="comparison-tag-log-rdb-volatile-lookup"></a>

## 타입 비교표

### 기능 비교

| 항목 | TAG | LOG | RDB | VOLATILE | LOOKUP |
|------|-----|-----|-----|----------|--------|
| DDL | `CREATE TAG TABLE` | `CREATE TABLE` | `CREATE RDB TABLE` | `CREATE VOLATILE TABLE` | `CREATE LOOKUP TABLE` |
| 주 용도 | 센서·계측값 | 이벤트·로그 | 관계형 업무 | 임시 집계 | 코드·기준 |
| INSERT | O | O | O | O | O |
| APPEND API | O | O | O (SDK) | X | O |
| UPDATE | O (태그/축 조건) | X | O | O | O |
| DELETE | O (BEFORE/조건) | O (BEFORE/OLDEST/EXCEPT) | O | O (PK equality) | O (PK equality) |
| PRIMARY KEY | 필수 | X | 선택 | 선택 | 필수 |
| BASETIME | 필수 (시간축) | X | X | X | X |
| _arrival_time | X | 자동 추가 | X | X | X |
| 인덱스 | 태그 인덱스 | BITMAP/KEYWORD | BTREE PK + 보조 인덱스 | Red-Black | Red-Black |
| 영속성 | O | O | O | X (메모리) | O |
| Cluster Edition | O | O | X | O | O |

### 스토리지 특성

| 항목 | TAG | LOG | RDB | VOLATILE | LOOKUP |
|------|-----|-----|-----|----------|--------|
| 스토리지 | 컬럼형 | 컬럼형 | 행 기반 (관계형) | 메모리 | 행 기반 |
| 시계열 최적화 | O | 일부 | X | X | X |
| 대용량 적합 | O | O | O | X | X |

### RDB 테이블 제약

RDB 테이블(8.6 신규)은 다음 제약이 있습니다.

- **Cluster Edition 미지원**: Standard Edition 전용
- **최소 컬럼 수**: 1개 이상

<a id="comparison-rdb-vs-lookup"></a>

## RDB vs LOOKUP 비교

RDB 테이블과 LOOKUP 테이블은 모두 관계형 데이터를 저장하지만, 대상 규모와 기능에 차이가 있습니다.

### 비교표

| 항목 | RDB 테이블 | LOOKUP 테이블 |
|------|-----------|--------------|
| DDL | `CREATE RDB TABLE` | `CREATE LOOKUP TABLE` |
| PRIMARY KEY | 선택 | 필수 |
| INSERT | O | O |
| UPDATE (WHERE 포함) | O | O |
| UPDATE (WHERE 없음) | O (전체 행) | X |
| DELETE | O | O |
| 인덱스 | BTREE PK + 보조 인덱스 | Red-Black |
| 대용량 | 대규모 가능 | 수백만 건 이하 권장 |
| JOIN 대상 | O | O |
| Cluster Edition | X | O |

### 선택 가이드

**RDB 테이블을 선택하는 경우**
- 대량 데이터 (수천만 건 이상)
- UPDATE·DELETE·INSERT·SELECT가 모두 필요한 일반 관계형 워크로드
- PRIMARY KEY 없이 다양한 컬럼 조합으로 조회하는 경우
- Standard Edition 환경

**LOOKUP 테이블을 선택하는 경우**
- 코드 테이블, 기준 정보 (수백만 건 이하)
- PRIMARY KEY 기준 UPDATE/DELETE 위주
- Cluster Edition 환경에서도 사용해야 하는 경우
- 실시간 기준 정보 갱신이 필요한 경우

### 예시

```sql
-- LOOKUP: 국가 코드 테이블 (소규모, PK 기반 UPDATE)
CREATE LOOKUP TABLE country_code (
    code   VARCHAR(4)   PRIMARY KEY,
    name   VARCHAR(64)
);
UPDATE country_code SET name = 'Korea' WHERE code = 'KR';

-- RDB: 주문 이력 (대규모, 일반 UPDATE/DELETE 지원)
CREATE RDB TABLE order_history (
    order_id  LONG,
    item_id   INTEGER,
    qty       INTEGER,
    amount    DOUBLE
);
UPDATE order_history SET qty = 10 WHERE order_id = 12345;
DELETE FROM order_history WHERE order_id = 12345;
```
