---
type: docs
title: '4.1 테이블 타입 선택'
weight: 10
toc: true
---
잘못된 타입 선택은 성능 저하와 기능 제한으로 이어지므로, 설계 초기에 데이터 성격에 맞는 타입을 결정해야 합니다.

- **[타입 선택 결정 가이드](/dbms/data-modeling-table-design/table-types-selection-type/#selection-decision)**
- **[타입 비교표](/dbms/data-modeling-table-design/table-types-selection-type/#comparison-tag-log-rdb-volatile-lookup)**
- **[TRANSACTION vs LOOKUP 비교](/dbms/data-modeling-table-design/table-types-selection-type/#comparison-rdb-vs-lookup)**


<a id="table-types-type"></a>

테이블 타입의 역할과 저장 개념은 [데이터 모델 개념](../../core-concepts/concepts/#time-series)을
참고하십시오. 같은 데이터라도 이력을 누적할지, 현재 상태를 갱신할지에 따라 적합한 타입이
달라집니다. 변경·조회·영속성 요구사항을 함께 검토합니다.

<a id="selection-decision"></a>

## 타입 선택 결정 가이드

아래 흐름으로 후보를 좁힌 뒤, 필요한 DML과 트랜잭션, 메모리 사용량, Edition 지원 여부를
비교표에서 확인합니다. 예를 들어 기준 정보라도 여러 변경을 하나의 트랜잭션으로 묶어야
한다면 LOOKUP 대신 TRANSACTION을 검토합니다.

### 결정 흐름

```
데이터가 센서/기기 계측값인가?
  ├── YES → 시간축인가?    YES → TAG TABLE (BASETIME)
  │            거리축인가?  YES → TAG TABLE (BASEDISTANCE)
  └── NO  ↓

데이터가 이벤트/로그/패킷인가? (추가 전용)
  ├── YES → LOG TABLE
  └── NO  ↓

데이터가 코드 테이블/기준 정보인가? (반복 조회·갱신)
  ├── YES → LOOKUP TABLE
  └── NO  ↓

데이터가 서버 재시작 시 폐기 가능한 인메모리 상태/캐시인가?
  ├── YES → VOLATILE TABLE
  └── NO  ↓

일반 관계형 업무 데이터 (UPDATE/DELETE/SELECT/INSERT 모두 필요)
  └── TRANSACTION TABLE
```

### 주요 판단 기준

| 질문 | 타입 |
|------|------|
| 시간 또는 거리 기반 계측값인가? | TAG |
| 원본 이벤트를 추가하고 오래된 구간만 정리하는가? | LOG |
| PRIMARY KEY가 필요한 기준 정보이며 반복 조회·갱신하는가? | LOOKUP |
| 서버 재시작 시 데이터가 사라져도 되는가? | VOLATILE |
| 일반 관계형 업무 (INSERT/UPDATE/DELETE/SELECT)? | TRANSACTION |

### 주의사항

- 이벤트마다 고유한 이름을 태그 식별자로 사용하면 태그 수와 메타데이터가 계속 늘어납니다.
  반복 계측 대상이 없는 이벤트는 LOG 테이블을 검토합니다.
- LOG 테이블은 UPDATE와 일반 조건 DELETE가 불가하므로 수정 가능성이 있는 데이터에는 부적합합니다. 보존/정리 목적의 `BEFORE`, `OLDEST`, `EXCEPT` DELETE만 사용합니다.
- TRANSACTION 테이블은 Standard Edition 전용입니다. Cluster Edition 환경에서는 LOOKUP(소규모) 또는 외부 RDBMS를 활용합니다.
- VOLATILE 테이블은 서버 재시작 시 데이터가 소멸됩니다.

<a id="comparison-tag-log-rdb-volatile-lookup"></a>

## 타입 비교표

### 기능 비교

| 항목 | TAG | LOG | TRANSACTION | VOLATILE | LOOKUP |
|------|-----|-----|-----|----------|--------|
| DDL | `CREATE TAG TABLE` | `CREATE LOG TABLE` | `CREATE TABLE` / `CREATE TRANSACTION TABLE` / `CREATE TXN TABLE` | `CREATE VOLATILE TABLE` | `CREATE LOOKUP TABLE` |
| 주 용도 | 센서·계측값 | 이벤트·로그 | 관계형 업무 | 임시 집계 | 코드·기준 |
| INSERT | O | O | O | O | O |
| UPDATE | O (Standard, 태그/BASETIME 조건) | X | O | O | O |
| DELETE | O (BEFORE/조건/전체) | O (BEFORE/OLDEST/EXCEPT/전체) | O | O (PK 일치/전체) | O (일반 조건식/전체 삭제) |
| PRIMARY KEY | 필수 | X | 선택 | 선택 | 필수 |
| BASETIME | 필수 (시간축) | X | X | X | X |
| _arrival_time | X | 자동 추가 | X | X | X |
| 인덱스 | 태그 인덱스 | BITMAP/KEYWORD | BTREE PK + 보조 인덱스 | Red-Black | Red-Black |
| 영속성 | O | O | O | X (메모리) | O |
| Cluster Edition | O | O | X | O | O |

Append API는 테이블뿐 아니라 SDK와 입력 경로에 따라 지원 범위가 달라집니다.
[SDK Append 지원표](../../development-tools-integration/sdk-support-scope/#append-table-type-matrix)에서
사용하는 드라이버와 테이블 조합을 확인합니다.

### 스토리지 특성

| 항목 | TAG | LOG | TRANSACTION | VOLATILE | LOOKUP |
|------|-----|-----|-----|----------|--------|
| 스토리지 | 컬럼형 | 컬럼형 | 행 기반 (관계형) | 메모리 | 영속 저장 + 전체 행 메모리 상주 |
| 시계열 최적화 | O | 일부 | X | X | X |
| 대용량 적합 | O | O | O | X | X |

### TRANSACTION 테이블 제약

TRANSACTION 테이블은 다음 제약이 있습니다.

- **Cluster Edition 미지원**: Standard Edition 전용
- **최소 컬럼 수**: 1개 이상

<a id="comparison-rdb-vs-lookup"></a>

## TRANSACTION vs LOOKUP 비교

TRANSACTION 테이블과 LOOKUP 테이블은 모두 관계형 데이터를 저장하지만, 대상 규모와 기능에 차이가 있습니다.

### 비교표

| 항목 | TRANSACTION 테이블 | LOOKUP 테이블 |
|------|-----------|--------------|
| DDL | `CREATE TRANSACTION TABLE` | `CREATE LOOKUP TABLE` |
| PRIMARY KEY | 선택 | 필수 |
| INSERT | O | O |
| UPDATE (WHERE 포함) | O | O |
| UPDATE (WHERE 없음) | O (전체 행) | X |
| DELETE | O | O |
| 인덱스 | BTREE PK + 보조 인덱스 | Red-Black |
| 데이터 규모 | 디스크 용량과 트랜잭션 부하로 검증 | 참조 데이터 조회·갱신 부하로 검증 |
| JOIN 대상 | O | O |
| Cluster Edition | X | O |

### 선택 가이드

**TRANSACTION 테이블을 선택하는 경우**
- 명시적 트랜잭션과 관계형 DML이 필요한 데이터
- UPDATE·DELETE·INSERT·SELECT가 모두 필요한 일반 관계형 워크로드
- PRIMARY KEY 없이 다양한 컬럼 조합으로 조회하는 경우
- Standard Edition 환경

**LOOKUP 테이블을 선택하는 경우**
- 코드 테이블과 기준 정보
- PRIMARY KEY 조회와 단건 UPDATE/DELETE가 필요한 경우
- Cluster Edition 환경에서도 사용해야 하는 경우
- 실시간 기준 정보 갱신이 필요한 경우

### 예시

```sql
-- LOOKUP: 국가 코드 테이블 (PK 조회와 조건 기반 UPDATE)
CREATE LOOKUP TABLE country_code (
    code   VARCHAR(4)   PRIMARY KEY,
    name   VARCHAR(64)
);
UPDATE country_code SET name = 'Korea' WHERE code = 'KR';

-- TRANSACTION: 주문 이력 (대규모, 일반 UPDATE/DELETE 지원)
CREATE TRANSACTION TABLE order_history (
    order_id  LONG,
    item_id   INTEGER,
    qty       INTEGER,
    amount    DOUBLE
);
UPDATE order_history SET qty = 10 WHERE order_id = 12345;
DELETE FROM order_history WHERE order_id = 12345;
```
