---
type: docs
title: 'TAG data UPDATE WHERE/SET 지원 범위'
weight: 30
---

TAG data UPDATE는 지원되지만, WHERE/SET 절에는 안전한 대상 범위를 보장하기 위한 제약이
있습니다.

## 실행 가능한 구문

```sql
UPDATE tag
   SET value = 25.0
 WHERE name = 'TEMP-01'
   AND time = TO_DATE('2024-01-15 10:00:00', 'YYYY-MM-DD HH24:MI:SS');

UPDATE tag
   SET value = value * 0.98
 WHERE name = 'TEMP-01'
   AND time BETWEEN TO_DATE('2024-01-15 10:00:00', 'YYYY-MM-DD HH24:MI:SS')
                AND TO_DATE('2024-01-15 11:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

## 허용되는 WHERE/SET

- 태그 선택: `name =`, `name IN (...)`, `name LIKE ...`
- 시간 조건: `time =`, `BETWEEN`, 양쪽 범위, 한쪽 범위
- 추가 필터: 데이터 컬럼 predicate
- SET 대상: 실제 데이터 컬럼과 `SUMMARIZED` 데이터 컬럼

## 허용되지 않는 범위

- WHERE 없는 UPDATE
- 태그 선택 조건 없는 UPDATE
- 시간 조건 없는 UPDATE
- `OR`, 서브쿼리, 집계식 기반 조건
- `name`, `time`, 메타데이터 컬럼 SET

## 메타데이터 UPDATE

TAG 메타데이터는 별도 구문을 사용합니다.

```sql
UPDATE tag METADATA SET location = 'zone-2'
WHERE name = 'TEMP-01';
```
