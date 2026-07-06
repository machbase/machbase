---
type: docs
title: 'TAG data UPDATE 정책 (planned: dbms-nfx#3733)'
weight: 10
---

> **계획된 기능**: TAG 테이블의 실제 시계열 데이터(value 컬럼) UPDATE는 dbms-nfx#3733에서 개발 중입니다. 현재 버전(8.6)에서는 아직 사용할 수 없습니다.

## 현재 상황

현재 Machbase 8.6에서는 TAG 테이블의 실제 시계열 값을 수정하는 UPDATE 구문을 지원하지 않습니다. 이는 태그 데이터의 불변성 원칙과 시계열 저장 구조의 최적화를 위한 설계입니다.

```sql
-- 현재 지원하지 않음
UPDATE tag SET value = 25.0
WHERE name = 'TEMP-01' AND time = '2024-01-01 12:00:00 000:000:000';
-- → 오류 발생
```

## 현재 대안

실제 태그 데이터를 수정해야 하는 경우:

1. **메타데이터 수정**: TAG 메타데이터 컬럼은 지금도 UPDATE 가능 → [TAG data UPDATE와 UPDATE ... METADATA 구분](./distinction-tag-data-update-metadata/) 참고
2. **새 데이터 삽입**: 수정 값을 새 타임스탬프로 재삽입 (원본은 유지)
3. **정정 로그**: 별도 LOG/RDB 테이블에 정정 이력 기록

## 향후 지원 예정 기능

dbms-nfx#3733이 완료되면, 특정 조건에 부합하는 TAG 데이터의 값(value)을 직접 UPDATE하는 것이 가능해질 예정입니다. 단, 다음과 같은 제약이 예상됩니다.

- WHERE 조건: name(PK) + 시간 범위 지정 필수
- 일부 인덱스/통계 재계산 필요
- Standard Edition 전용 가능성

> 해당 기능이 릴리즈되면 이 문서는 실제 사용 예시로 업데이트됩니다.
