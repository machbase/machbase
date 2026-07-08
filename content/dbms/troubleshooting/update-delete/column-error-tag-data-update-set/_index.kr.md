---
type: docs
title: 'TAG data UPDATE SET 대상 컬럼 오류'
weight: 20
---

TAG 테이블에 `UPDATE` 문을 실행하면 SET 대상 컬럼과 관계없이 오류가 발생합니다.

{{< callout type="warning" >}}
**현재 제약사항**

현재 Machbase 8.6 빌드에서 TAG 테이블은 `UPDATE` 문을 지원하지 않습니다.
`value` 컬럼이나 사용자 컬럼도 `UPDATE` 대상으로 사용할 수 없습니다.
{{< /callout >}}

## 증상

TAG 테이블에 UPDATE를 실행할 때 다음과 같은 오류가 발생합니다.

```
[ERR-02278: UPDATE statement is not allowed for SENSOR_TAG.]
```

## 원인

TAG 테이블은 각 컬럼에 특별한 역할이 부여되어 있지만, 현재 버전에서는 컬럼 역할과
무관하게 `UPDATE`가 허용되지 않습니다.

| 컬럼 유형 | 설명 | UPDATE 가능 여부 |
|-----------|------|:---:|
| PRIMARY KEY (`name`) | TAG를 식별하는 고유 키 | 불가 |
| BASETIME (`time`) | 시계열 데이터의 타임스탬프 | 불가 |
| SUMMARIZED (`value`) | 측정값 데이터 | 불가 |
| 기타 사용자 컬럼 | 추가 데이터 컬럼 | 불가 |

PRIMARY KEY 컬럼(`name`)과 BASETIME 컬럼(`time`)뿐 아니라 `value` 컬럼도 `UPDATE`
대상이 될 수 없습니다.

## 오류 발생 패턴

```sql
-- 오류: PRIMARY KEY 컬럼(name) 업데이트 시도
UPDATE sensor_tag SET name = 'new-sensor' WHERE name = 'old-sensor';

-- 오류: BASETIME 컬럼(time) 업데이트 시도
UPDATE sensor_tag SET time = NOW WHERE name = 'sensor-01';

-- 오류: SUMMARIZED 컬럼(value) 업데이트 시도
UPDATE sensor_tag SET value = 99.9 WHERE name = 'sensor-01';
```

## TAG 테이블 컬럼 유형 확인

어느 컬럼이 PRIMARY KEY 또는 BASETIME인지 확인하려면 다음 쿼리를 사용합니다.

```sql
-- 테이블 컬럼 정의 확인
DESC sensor_tag;
```

출력에서 `PRIMARY KEY`, `BASETIME`, `SUMMARIZED` 속성을 확인합니다.

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

## 값 컬럼을 정정해야 하는 경우

측정값을 정정해야 하는 경우에도 직접 `UPDATE`는 사용할 수 없습니다. 정정 데이터를 새로
적재하고, 기존 tag 데이터 제거가 필요한지 운영 정책에 따라 결정합니다.
