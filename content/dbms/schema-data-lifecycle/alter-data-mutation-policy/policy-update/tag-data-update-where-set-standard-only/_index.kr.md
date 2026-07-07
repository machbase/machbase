---
type: docs
title: 'TAG data UPDATE 구문 미지원 범위'
weight: 30
---

현재 빌드에서는 TAG 테이블의 실제 시계열 데이터에 대해 `UPDATE tag SET ...` 구문을
지원하지 않습니다. 따라서 WHERE/SET 절 제약을 만족하더라도 실행할 수 없습니다.

## 실행할 수 없는 구문

다음 구문은 TAG 실제 데이터 UPDATE 예시로 보일 수 있지만 현재는 오류가 발생합니다.

```sql
UPDATE tag SET value = 25.0
WHERE name = 'TEMP-01'
  AND time = '2024-01-15 10:00:00 000:000:000';
-- [ERR-02278: UPDATE statement is not allowed for TAG.]

UPDATE tag SET value = value * 0.98
WHERE name = 'TEMP-01'
  AND time BETWEEN '2024-01-15 10:00:00 000:000:000'
               AND '2024-01-15 11:00:00 000:000:000';
-- [ERR-02278: UPDATE statement is not allowed for TAG.]
```

## 현재 지원되는 UPDATE

TAG 테이블에서 UPDATE가 가능한 대상은 메타데이터 컬럼입니다.

```sql
UPDATE tag METADATA SET location = 'zone-2'
WHERE name = 'TEMP-01';
```

## 현재 권장 대안

- 잘못 입력된 데이터: 새 타임스탬프로 정정값 재삽입 후 원본은 보존
- 보정이 필요한 경우: RDB 테이블에 보정 이력을 별도 관리하고 JOIN으로 처리
