---
type: docs
title: 'TAG data UPDATE SET 대상 컬럼 오류 (planned: dbms-nfx#3733)'
weight: 20
---

TAG 테이블의 UPDATE SET 절에 업데이트할 수 없는 컬럼을 지정하면 오류가 발생합니다. 현재 TAG 테이블에서 UPDATE 가능한 컬럼은 제한되어 있습니다.

{{< callout type="warning" >}}
**현재 제약사항 (planned: dbms-nfx#3733)**

TAG 테이블의 UPDATE는 현재 `value` 컬럼(SUMMARIZED 컬럼)에 대해서만 지원합니다. 이 제약은 향후 확장될 예정입니다.
{{< /callout >}}

## 증상

TAG 테이블에 UPDATE를 실행할 때 다음과 같은 오류가 발생합니다.

```
[ERR-02XXX]: Column 'name' cannot be updated in TAG table
[ERR-02XXX]: BASETIME column cannot be updated
```

## 원인

TAG 테이블은 각 컬럼에 특별한 역할이 부여되어 있습니다.

| 컬럼 유형 | 설명 | UPDATE 가능 여부 |
|-----------|------|:---:|
| PRIMARY KEY (`name`) | TAG를 식별하는 고유 키 | 불가 |
| BASETIME (`time`) | 시계열 데이터의 타임스탬프 | 불가 |
| SUMMARIZED (`value`) | 측정값 데이터 | **가능** |
| 기타 사용자 컬럼 | TAG 메타데이터 등 | 확인 필요 |

PRIMARY KEY 컬럼(`name`)과 BASETIME 컬럼(`time`)은 데이터의 식별자와 시간 축 역할을 하므로 UPDATE 대상이 될 수 없습니다.

## 오류 발생 패턴

```sql
-- 오류: PRIMARY KEY 컬럼(name) 업데이트 시도
UPDATE sensor_tag SET name = 'new-sensor' WHERE name = 'old-sensor';

-- 오류: BASETIME 컬럼(time) 업데이트 시도
UPDATE sensor_tag SET time = NOW WHERE name = 'sensor-01';
```

## 올바른 UPDATE 방법

SUMMARIZED 컬럼(`value`)을 대상으로 하며, WHERE 절에는 PRIMARY KEY 조건을 사용합니다.

```sql
-- 정상: value(SUMMARIZED) 컬럼 업데이트
UPDATE TAG TABLE sensor_tag SET value = 99.9 WHERE name = 'sensor-01';
```

## TAG 테이블 컬럼 유형 확인

어느 컬럼이 PRIMARY KEY 또는 BASETIME인지 확인하려면 다음 쿼리를 사용합니다.

```sql
-- 테이블 컬럼 정의 확인
DESC sensor_tag;
```

출력에서 `FLAG` 열의 값으로 컬럼 역할을 구분할 수 있습니다.
- `1` 또는 `PK`: PRIMARY KEY 컬럼
- `BASETIME`: 시간 축 컬럼

## name 컬럼을 변경해야 하는 경우

TAG의 이름을 변경해야 할 경우 직접 UPDATE는 불가능합니다. 다음 절차를 사용합니다.

1. 기존 데이터를 조회하여 새 name으로 INSERT
2. 기존 name의 데이터를 DELETE (DELETE FROM sensor_tag WHERE name = 'old-sensor')

```sql
-- 1. 새 name으로 기존 데이터 복사
INSERT INTO sensor_tag SELECT 'new-sensor', time, value FROM sensor_tag
WHERE name = 'old-sensor';

-- 2. 기존 데이터 삭제
DELETE FROM sensor_tag WHERE name = 'old-sensor';
```

## 향후 지원 예정

더 넓은 범위의 컬럼에 대한 UPDATE 지원은 `planned: dbms-nfx#3733`으로 계획 중입니다. 최신 릴리스 노트를 확인하십시오.
