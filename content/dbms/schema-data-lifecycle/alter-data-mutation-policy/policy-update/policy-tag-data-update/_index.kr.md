---
type: docs
title: 'TAG 실제 데이터 UPDATE 미지원 정책'
weight: 10
---

TAG 테이블의 실제 시계열 데이터(value 컬럼)는 현재 빌드에서 UPDATE할 수 없습니다.

## 현재 상황

TAG 테이블의 실제 시계열 값을 수정하는 UPDATE 구문은 오류가 발생합니다. 이는 태그
데이터의 append-oriented 저장 구조와 통계/롤업 최적화를 유지하기 위한 현재 정책입니다.

```sql
-- 현재 지원하지 않음
UPDATE tag SET value = 25.0
WHERE name = 'TEMP-01' AND time = '2024-01-01 12:00:00 000:000:000';
-- [ERR-02278: UPDATE statement is not allowed for TAG.]
```

## 현재 대안

실제 태그 데이터를 수정해야 하는 경우:

1. **메타데이터 수정**: TAG 메타데이터 컬럼은 지금도 UPDATE 가능 → [TAG data UPDATE와 UPDATE ... METADATA 구분](./distinction-tag-data-update-metadata/) 참고
2. **새 데이터 삽입**: 수정 값을 새 타임스탬프로 재삽입 (원본은 유지)
3. **정정 로그**: 별도 LOG/RDB 테이블에 정정 이력 기록

## 지원하지 않는 예제와 혼동하지 않기

`UPDATE tag SET ...` 형식의 실제 데이터 UPDATE 예제는 현재 실행 예제가 아닙니다. TAG에서
현재 UPDATE 가능한 대상은 `UPDATE ... METADATA` 구문의 메타데이터 컬럼입니다.
