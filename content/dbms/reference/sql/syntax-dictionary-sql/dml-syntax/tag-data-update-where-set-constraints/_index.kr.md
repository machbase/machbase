---
type: docs
title: '17.1.1.12.2 TAG data UPDATE WHERE/SET constraints'
weight: 20
toc: true
---

TAG data UPDATE는 대상 범위가 명확해야 합니다. WHERE 절에는 태그 선택 조건과 BASETIME
조건이 모두 필요하고, SET 절은 실제 데이터 컬럼만 대상으로 합니다.

<span class="badge-since">Machbase 8.7.0부터 지원되는 기능</span>

## SET 절 제약

| 컬럼 역할 | SET 가능 여부 | 설명 |
|-----------|:------------:|------|
| 데이터 컬럼 | O | `value`, 보조 수치/문자열 컬럼 등 |
| `SUMMARIZED` 데이터 컬럼 | O | 원본 TAG row 값이 변경됨 |
| BASETIME 컬럼 | X | 시간 축 컬럼은 변경 불가 |
| PRIMARY KEY 컬럼 (`name`) | X | 태그 이름 변경 불가 |
| 메타데이터 컬럼 | X | `UPDATE ... METADATA`로 별도 처리 |
| 숨김/시스템 컬럼 | X | 내부 컬럼은 SET 대상이 아님 |

SET 표현식에는 상수, bind 변수, 기존 행 컬럼을 참조하지 않는 산술식·문자열식·`CASE`,
허용된 형변환 함수와 NULL을 사용할 수 있습니다. 기존 행 컬럼을 참조하는 식, 서브쿼리와
집계식은 SET RHS로 사용할 수 없습니다.

## WHERE 절 제약

```sql
UPDATE table_name
   SET col = expr
 WHERE name = 'tag-name'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');
```

| WHERE 조건 | 지원 여부 |
|-----------|:---------:|
| `name = '...'` | O |
| `name IN ('...', '...')` | O |
| `name LIKE '...'` | O |
| `time = t1` | O |
| `time BETWEEN t1 AND t2` | O |
| `time >= t1 AND time < t2` | O |
| 한쪽 시간 조건 | O |
| 데이터 컬럼 조건 | O |
| 태그 선택 없는 조건 | X |
| 시간 조건 없는 조건 | X |
| `OR` 조건 | X |
| `IN (SELECT ...)` | X |
| 태그/축 컬럼을 함수·연산식으로 감싼 표현식 | X |

## 메타데이터 UPDATE

```sql
UPDATE table_name METADATA
   SET meta_col = value
 WHERE condition;
```

메타데이터 UPDATE는 태그 속성 영역을 수정합니다. 실제 시계열 row의 데이터 컬럼을 수정하는
TAG data UPDATE와 구문과 대상이 다릅니다.

## 컬럼 역할 확인 방법

`DESC` 명령으로 컬럼 속성을 확인합니다.

```sql
DESC sensor_tag;
```

또는 시스템 테이블에서 컬럼 FLAG를 조회합니다.

```sql
SELECT NAME, TYPE, FLAG
  FROM M$SYS_COLUMNS
 WHERE TABLE_ID = (
     SELECT ID FROM M$SYS_TABLES WHERE NAME = 'SENSOR_TAG'
 );
```

| FLAG 값 | 역할 |
|---------|------|
| 1 | Tag Data 컬럼 |
| 2 | Rollup 컬럼 |
| 4 | Tag Meta 컬럼 |
| 8 | Tag Stat 컬럼 |

## 오류 사례

```sql
-- 오류: BASETIME 컬럼을 SET 대상으로 지정
UPDATE sensor_tag
   SET time = TO_DATE('2026-07-01', 'YYYY-MM-DD')
 WHERE name = 'TEMP-01'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');

-- 오류: 시간 조건이 없음
UPDATE sensor_tag
   SET value = 0.0
 WHERE name = 'TEMP-01';

-- 오류: OR 조건 사용
UPDATE sensor_tag
   SET value = 0.0
 WHERE name = 'TEMP-01'
    OR name = 'TEMP-02';
```

## 관련 문서

- [TAG data UPDATE syntax](../tag-data-update-syntax/)
- [ROLLUP_REBUILD syntax](../../rollup-rebuild-syntax/)
