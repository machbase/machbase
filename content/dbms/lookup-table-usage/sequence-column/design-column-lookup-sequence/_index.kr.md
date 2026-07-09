---
type: docs
title: '9.11.1 컬럼 및 시퀀스 설계'
weight: 30
---

LOOKUP 테이블의 일반 컬럼 설계와 자동 증가 번호(시퀀스) 활용 방법을 설명합니다.

## 지원 컬럼 타입

| 타입 | 설명 |
|------|------|
| `INTEGER` / `LONG` | 정수 |
| `DOUBLE` / `FLOAT` | 부동소수점 |
| `SHORT` | 단정수 |
| `VARCHAR(n)` | 가변 문자열 |
| `DATETIME` | 날짜·시각 |
| `IPV4` / `IPV6` | 네트워크 주소 |
| `JSON` | 지원하지 않음 |

## 기본 스키마 예시

```sql
CREATE LOOKUP TABLE equipment_master (
    equip_id   INTEGER     PRIMARY KEY,
    equip_name VARCHAR(128),
    location   VARCHAR(64),
    dept       VARCHAR(64),
    status     VARCHAR(16),
    created_at DATETIME
);
```

## 시퀀스(자동 증가) 활용

LOOKUP 테이블에서 자동 증가 번호가 필요하면 `LONG PROPERTY(SEQUENCE=1)` 컬럼과
`NEXTVAL()` 함수를 사용합니다. 별도의 `CREATE SEQUENCE` 객체는 사용하지 않습니다.

```sql
CREATE LOOKUP TABLE equipment_master_seq (
    equip_id   LONG PROPERTY(SEQUENCE=1) PRIMARY KEY,
    equip_name VARCHAR(128),
    location   VARCHAR(64),
    dept       VARCHAR(64),
    status     VARCHAR(16),
    created_at DATETIME
);

INSERT INTO equipment_master_seq
VALUES (NEXTVAL(equip_id), 'Motor-A', 'Line-1', 'Mfg', 'ACTIVE', NOW);

INSERT INTO equipment_master_seq
VALUES (NEXTVAL(equip_id), 'Pump-B', 'Line-2', 'Mfg', 'ACTIVE', NOW);
```

## 타임스탬프 관리 컬럼

```sql
CREATE LOOKUP TABLE code_master (
    code       VARCHAR(16) PRIMARY KEY,
    label      VARCHAR(128),
    created_at DATETIME,
    updated_at DATETIME
);

-- 삽입 시 created_at 초기화
INSERT INTO code_master VALUES ('KR', '대한민국', NOW, NOW);

-- UPDATE 시 updated_at 갱신
UPDATE code_master SET label = '한국', updated_at = NOW WHERE code = 'KR';
```
