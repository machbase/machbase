---
type: docs
title: 'TAG data UPDATE와 UPDATE ... METADATA 구분'
weight: 20
---

TAG 테이블에는 **실제 시계열 데이터**(time, value 등)와 **메타데이터**(METADATA 블록의
컬럼)가 있습니다. 두 영역 모두 수정할 수 있지만 구문과 제약이 다릅니다.

## TAG 테이블 구조 복습

```sql
CREATE TAG TABLE tag (
    name     VARCHAR(20) PRIMARY KEY,
    time     DATETIME BASETIME,
    value    DOUBLE SUMMARIZED,
    status   INTEGER
) METADATA (
    location VARCHAR(40),
    dept     VARCHAR(20)
);
```

## 실제 시계열 데이터 UPDATE

데이터 컬럼은 일반 `UPDATE` 문으로 수정합니다. WHERE 절에는 태그 선택 조건과 BASETIME
조건이 모두 필요합니다.

```sql
UPDATE tag
   SET value = 25.0,
       status = 1
 WHERE name = 'TEMP-01'
   AND time = TO_DATE('2024-01-15 10:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

`name`, `time`, 메타데이터 컬럼은 이 구문의 SET 대상이 아닙니다.

## 메타데이터 UPDATE

TAG 메타데이터는 태그 속성 영역이며 `UPDATE ... METADATA` 구문으로 수정합니다.

```sql
UPDATE tag METADATA SET location = 'zone-2'
WHERE name = 'TEMP-01';

UPDATE tag METADATA SET dept = 'R&D', location = 'building-B'
WHERE name = 'TEMP-01';
```

메타데이터 변경은 해당 tag name의 속성을 바꾸는 작업이며, 개별 시계열 row의 `value`나
보조 데이터 컬럼 값을 변경하지 않습니다.

## 구분 정리

| 대상 | UPDATE 구문 | 지원 여부 |
|------|------------|:--------:|
| 데이터 컬럼 (`value`, `status` 등) | `UPDATE tag SET ... WHERE name ... AND time ...` | O |
| 메타데이터 컬럼 (`location`, `dept` 등) | `UPDATE tag METADATA SET ...` | O |
| 태그 이름(PK) | 변경 불가 | X |
| 시간 축(BASETIME) | 변경 불가 | X |

## 주의 사항

- 데이터 UPDATE는 대상 row 범위를 좁히기 위해 태그 조건과 시간 조건을 모두 요구합니다.
- 메타데이터 UPDATE는 태그 속성 변경이며, 시계열 값 정정 용도로 사용하지 않습니다.
- 롤업이 있는 테이블의 데이터 값을 정정한 뒤에는 필요한 롤업을 재구성합니다.
