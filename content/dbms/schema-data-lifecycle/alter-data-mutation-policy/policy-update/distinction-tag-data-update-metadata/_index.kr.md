---
type: docs
title: 'TAG data UPDATE와 UPDATE ... METADATA 구분'
weight: 20
---

TAG 테이블에는 두 종류의 데이터가 존재합니다. **실제 시계열 데이터**(time, value 등)와 **메타데이터**(METADATA 블록의 컬럼)입니다. 이 둘의 UPDATE 가능 여부가 다르기 때문에 구분이 필요합니다.

## TAG 테이블 구조 복습

```sql
CREATE TAG TABLE tag (
    name     VARCHAR(20) PRIMARY KEY,   -- 태그 식별자
    time     DATETIME BASETIME,         -- 시계열 축 (데이터 영역)
    value    DOUBLE SUMMARIZED          -- 센서 측정값 (데이터 영역)
) METADATA (
    location VARCHAR(40),              -- 메타데이터 영역
    dept     VARCHAR(20)               -- 메타데이터 영역
);
```

## 메타데이터 UPDATE (현재 지원)

TAG 메타데이터는 태그 이름(name) 기준으로 수정할 수 있습니다. 메타데이터는 내부적으로 별도의 테이블에 저장되어 일반 UPDATE와 유사하게 동작합니다.

```sql
-- 센서 위치 변경
UPDATE tag METADATA SET location = 'zone-2'
WHERE name = 'TEMP-01';

-- 부서 변경
UPDATE tag METADATA SET dept = 'R&D', location = 'building-B'
WHERE name = 'TEMP-01';
```

## 실제 시계열 데이터 UPDATE (미지원)

TAG 테이블에 직접 삽입된 시계열 값(value)은 현재 버전에서 UPDATE할 수 없습니다.

```sql
-- 지원하지 않음 (8.6 기준)
UPDATE tag SET value = 25.0
WHERE name = 'TEMP-01' AND time = '2024-01-15 10:00:00 000:000:000';
```

이 기능은 dbms-nfx#3733에서 계획 중입니다.

## 구분 정리

| 대상 | UPDATE 구문 | 지원 여부 |
|------|-----------|---------|
| 메타데이터 컬럼 (location, dept 등) | `UPDATE tag METADATA SET ...` | O (현재 지원) |
| 시계열 값 (value, 사용자 추가 컬럼) | `UPDATE tag SET value = ...` | X (미지원, 계획 중) |
| 태그 이름(PK) | 변경 불가 | X |

## 주의 사항

- 메타데이터 UPDATE는 해당 name의 **모든 시계열 데이터**에 영향을 줍니다. (name 단위 속성이므로)
- 메타데이터 변경 후에는 메타데이터 캐시가 갱신되어야 조회에 반영됩니다.
