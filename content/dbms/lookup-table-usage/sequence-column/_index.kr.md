---
title: '9.11 SEQUENCE 컬럼'
weight: 110
toc: true
---
LOOKUP 테이블의 SEQUENCE 컬럼 설정과 활용을 다룹니다.


<a id="design-column-lookup-sequence"></a>

## 컬럼 및 시퀀스 설계

일반 컬럼 설계와 자동 증가 번호(시퀀스) 활용 방법입니다.

## 지원 컬럼 타입

| 타입 | 설명 |
|------|------|
| `INTEGER` / `LONG` | 정수 |
| `DOUBLE` / `FLOAT` | 부동소수점 |
| `SHORT` | 단정수 |
| `VARCHAR(n)` | 가변 문자열 |
| `DATETIME` | 날짜·시각 |
| `IPV4` / `IPV6` | 네트워크 주소 |
| `JSON` | 일반 컬럼으로 지원, primary key로는 사용 불가 |

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

자동 증가 번호가 필요하면 `LONG PROPERTY(SEQUENCE=1)` 컬럼과
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

<a id="definition-column-lookup-sequence"></a>

## LOOKUP SEQUENCE 컬럼 정의

레코드의 고유 순서를 자동으로 부여하기 위해 SEQUENCE 컬럼을 사용합니다.

## SEQUENCE 컬럼이 필요한 이유

이벤트 로그나 알람 이력을 관리할 때 DATETIME 컬럼만으로는 동일 시각에 발생한 여러 레코드를 구분할 수 없습니다. SEQUENCE 컬럼은 자동 증가하는 고유 번호를 부여해 이 문제를 해결합니다.

## SEQUENCE 컬럼 선언

SEQUENCE는 `LONG` 타입 컬럼에만 지정할 수 있습니다. PROPERTY 절의 `SEQUENCE` 파라미터로 시작값을 설정합니다.

```sql
CREATE LOOKUP TABLE alarm_history (
    seq       LONG PROPERTY(SEQUENCE=1) PRIMARY KEY,
    sensor_id VARCHAR(40),
    alarm_type VARCHAR(20),
    occurred_at DATETIME,
    message   VARCHAR(200)
);
```

- `SEQUENCE=1`: seq 컬럼이 1부터 자동 증가
- SEQUENCE 컬럼은 PRIMARY KEY로 지정하는 것이 일반적

## SEQUENCE 값 삽입: NEXTVAL()

`NEXTVAL()` 함수를 사용하면 현재 저장된 최댓값 + 1을 자동으로 계산해 삽입합니다.

```sql
-- NEXTVAL()로 자동 증가값 입력
INSERT INTO alarm_history (seq, sensor_id, alarm_type, occurred_at, message)
VALUES (NEXTVAL(seq), 'TEMP-01', 'HIGH', NOW, '온도 초과');

INSERT INTO alarm_history (seq, sensor_id, alarm_type, occurred_at, message)
VALUES (NEXTVAL(seq), 'PRESS-02', 'LOW', NOW, '압력 저하');

-- 조회
SELECT * FROM alarm_history ORDER BY seq;
-- seq=1, seq=2 순으로 정렬됨
```

## 일반 컬럼처럼 직접 값 지정

SEQUENCE 컬럼에 직접 값을 입력하는 것도 허용됩니다. 이 경우 내부 최댓값이 갱신되므로 자동 증가 카운터에 영향을 줍니다.

```sql
-- 직접 값 지정 (nextval을 쓰지 않아도 됨)
INSERT INTO alarm_history (seq, sensor_id, alarm_type, occurred_at, message)
VALUES (100, 'FLOW-03', 'NORMAL', NOW, '정상 복구');

-- 이후 NEXTVAL() 호출 시 101이 됩니다
INSERT INTO alarm_history (seq, sensor_id, alarm_type, occurred_at, message)
VALUES (NEXTVAL(seq), 'TEMP-01', 'NORMAL', NOW, '온도 정상');
-- seq = 101
```

## 활용 패턴

```sql
-- 최신 알람 N건 조회
SELECT * FROM alarm_history ORDER BY seq DESC LIMIT 10;

-- 특정 seq 이후 알람 조회
SELECT * FROM alarm_history WHERE seq > 500 ORDER BY seq;

-- 알람 확인 처리 (PK 기준 UPDATE)
UPDATE alarm_history SET alarm_type = 'ACKNOWLEDGED'
WHERE seq = 101;
```

## 주의 사항

- SEQUENCE 컬럼은 `LONG` 타입만 지원합니다.
- 시작값은 양수(`SEQUENCE=1` 이상)만 허용됩니다.
- NEXTVAL()을 쓰지 않고 중복 값을 삽입하는 것도 허용되므로, 고유성 보장이 필요하면 PRIMARY KEY를 함께 지정합니다.
