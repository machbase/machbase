---
type: docs
title: 'TAG data UPDATE WHERE/SET 제약과 Standard-only 범위'
weight: 30
---

> **계획된 기능**: 이 페이지는 dbms-nfx#3733 구현 완료 후 갱신됩니다. 현재 기술된 내용은 설계 방향을 바탕으로 한 것으로, 실제 릴리즈 시 변경될 수 있습니다.

## 예상 WHERE 절 제약

TAG 데이터 UPDATE가 지원되면, WHERE 절에는 반드시 다음 조건을 포함해야 할 것으로 예상됩니다.

- **name(PK) 조건 필수**: 특정 태그를 식별하지 않으면 UPDATE 대상 범위가 너무 넓어져 성능 문제가 발생합니다.
- **time 범위 조건 권장**: 정확한 타임스탬프 또는 시간 범위를 지정해야 합니다.

```sql
-- 예상 구문 (향후 지원 예정)
UPDATE tag SET value = 25.0
WHERE name = 'TEMP-01'
  AND time = '2024-01-15 10:00:00 000:000:000';

-- 범위 UPDATE (향후 예상)
UPDATE tag SET value = value * 0.98
WHERE name = 'TEMP-01'
  AND time BETWEEN '2024-01-15 10:00:00 000:000:000'
               AND '2024-01-15 11:00:00 000:000:000';
```

## 예상 SET 절 제약

- name(PK) 컬럼과 time(BASETIME) 컬럼은 변경 불가 예상
- value 등 사용자 정의 데이터 컬럼만 수정 가능 예상

## Standard Edition 전용 가능성

TAG 데이터 UPDATE는 클러스터 환경에서의 복제 정합성 문제로 인해 Standard Edition에서만 지원될 가능성이 있습니다. Cluster Edition에서는 다른 접근이 필요할 수 있습니다.

## 현재 권장 대안

- 잘못 입력된 데이터: 새 타임스탬프로 정정값 재삽입 후 원본은 보존
- 보정이 필요한 경우: RDB 테이블에 보정 이력을 별도 관리하고 JOIN으로 처리

> 최신 지원 현황은 Machbase 공식 릴리즈 노트를 확인하세요.
