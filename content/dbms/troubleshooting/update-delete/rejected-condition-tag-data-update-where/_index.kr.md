---
type: docs
title: 'TAG data UPDATE가 거부될 때'
weight: 10
---

TAG 테이블에 `UPDATE` 문을 실행하면 오류가 발생합니다.

{{< callout type="warning" >}}
**현재 제약사항**

현재 Machbase 8.6 빌드에서 TAG 테이블은 `UPDATE` 문을 지원하지 않습니다.
TAG 값을 정정해야 할 때는 새 행을 삽입한 뒤, 필요하면 기존 tag 데이터를 `DELETE`로 제거합니다.
{{< /callout >}}

## 증상

TAG 테이블에 UPDATE를 실행할 때 다음과 같은 오류가 발생합니다.

```
[ERR-02278: UPDATE statement is not allowed for SENSOR_TAG.]
```

`UPDATE TAG TABLE ...` 형태의 구문도 지원되지 않습니다.

```
[ERR-02010: Syntax error: near token (TABLE ...).]
```

## 원인

TAG 테이블은 append 중심의 시계열 저장 구조입니다. 현재 버전에서는 `WHERE name = ...`
조건을 사용하더라도 `UPDATE` 문 자체가 허용되지 않습니다.

- **미지원**: `UPDATE sensor_tag SET value = ... WHERE name = ...`
- **미지원**: `UPDATE sensor_tag SET value = ... WHERE name = ... AND time = ...`
- **미지원**: `UPDATE TAG TABLE sensor_tag SET value = ... WHERE name = ...`

## 진단

현재 실행하려는 UPDATE 문의 WHERE 절을 확인합니다.

```sql
-- 오류: TAG 테이블 UPDATE는 지원되지 않음
UPDATE sensor_tag SET value = 99.9
WHERE name = 'sensor-01';

-- 오류: UPDATE TAG TABLE 구문은 지원되지 않음
UPDATE TAG TABLE sensor_tag SET value = 99.9
WHERE name = 'sensor-01';
```

## 임시 해결 방법

기존 값을 직접 수정하지 말고, 정정 데이터를 새로 입력한 뒤 필요하면 기존 tag 데이터를 삭제합니다.

**1단계: 정정 대상 데이터 확인**

```sql
SELECT name, time, value
  FROM sensor_tag
 WHERE name = 'sensor-01'
 ORDER BY time;
```

**2단계: 정정 데이터 재입력**

```sql
INSERT INTO sensor_tag
VALUES ('sensor-01',
        TO_DATE('2024-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS'),
        99.9);
```

**3단계: 기존 tag 데이터를 제거해야 하는 경우**

```sql
DELETE FROM sensor_tag WHERE name = 'sensor-01';
```

`DELETE FROM tag_table WHERE name = ...`는 해당 tag 이름의 데이터를 제거합니다. 일부 시간대만
삭제해야 하는 경우에는 운영 절차상 백업, 재적재, 테이블 교체 방식을 함께 검토합니다.
