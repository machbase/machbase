---
title: '9.11 SEQUENCE 컬럼'
weight: 110
toc: true
---
LOOKUP 테이블의 SEQUENCE 컬럼 설정과 활용을 다룹니다.


<a id="design-column-lookup-sequence"></a>


## LOOKUP SEQUENCE 컬럼 정의

레코드의 고유 순서를 자동으로 부여하기 위해 SEQUENCE 컬럼을 사용합니다.

## SEQUENCE 컬럼이 필요한 이유

이벤트 로그나 알람 이력을 관리할 때 DATETIME 컬럼만으로는 동일 시각에 발생한 여러 레코드를 구분할 수 없습니다. SEQUENCE 컬럼은 자동 증가하는 고유 번호를 부여해 이 문제를 해결합니다.

## SEQUENCE 컬럼 선언

SEQUENCE는 `LONG` 또는 `INT64` 타입 컬럼에 지정할 수 있습니다. PROPERTY 절의 `SEQUENCE`
파라미터로 시작값을 설정합니다.

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

- SEQUENCE 컬럼은 `LONG`, `INT64` 타입을 지원합니다.
- 시작값은 양수(`SEQUENCE=1` 이상)만 허용됩니다.
- NEXTVAL()을 쓰지 않고 중복 값을 삽입하는 것도 허용되므로, 고유성 보장이 필요하면 PRIMARY KEY를 함께 지정합니다.
