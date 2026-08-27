---
title: '5.8 제약, 오류, 문제 해결'
weight: 80
toc: true
aliases:
  - /dbms/troubleshooting/update-delete/
---


<a id="rejected-condition-tag-data-update-where"></a>

## TAG data UPDATE WHERE 조건 오류

WHERE 절에 태그 선택 조건과 BASETIME 조건이 모두 있어야 합니다.
조건이 모호하거나 허용되지 않는 형태이면 UPDATE가 거부됩니다.

{{< callout type="warning" >}}
**필수 조건**

`WHERE name ...` 형태의 태그 선택 조건과 `time ...` 형태의 BASETIME 조건을 함께 지정합니다.
조건 없는 전체 UPDATE, 태그 조건만 있는 UPDATE, 시간 조건만 있는 UPDATE는 허용되지 않습니다.
{{< /callout >}}

### 증상

다음과 같은 UPDATE가 오류로 거부됩니다.

```sql
-- 시간 조건 없음
UPDATE sensor_tag SET value = 99.9
WHERE name = 'sensor-01';

-- 태그 선택 조건 없음
UPDATE sensor_tag SET value = 99.9
WHERE time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');

-- OR 조건 사용
UPDATE sensor_tag SET value = 99.9
WHERE name = 'sensor-01'
   OR name = 'sensor-02';
```

### 원인

대상 태그와 시간 범위를 명확하게 제한할 수 없는 조건은 거부됩니다.

| 조건 형태 | 지원 여부 |
|-----------|:--------:|
| `name = 'sensor-01' AND time >= ...` | O |
| `name IN ('sensor-01', 'sensor-02') AND time BETWEEN ...` | O |
| `name LIKE 'sensor-%' AND time < ...` | O |
| `value > 10`만 사용 | X |
| `name = 'sensor-01'`만 사용 | X |
| `time >= ...`만 사용 | X |
| `OR`, 서브쿼리, 집계 조건 | X |

### 해결 방법

태그 선택 조건과 시간 조건을 함께 명시합니다.

```sql
UPDATE sensor_tag
   SET value = 99.9
 WHERE name = 'sensor-01'
   AND time = TO_DATE('2026-07-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS');

UPDATE sensor_tag
   SET status = 1
 WHERE name IN ('sensor-01', 'sensor-02')
   AND time >= TO_DATE('2026-07-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
   AND time <  TO_DATE('2026-07-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

### NAME 또는 TIME bind가 `ERR-2190`으로 거부될 때

Machbase 8.7.0부터 Standard Edition에서는 다음과 같이 NAME과 BASETIME 조건 값에 bind
parameter를 사용할 수 있습니다.

```sql
UPDATE sensor_tag
   SET value = ?
 WHERE name = ?
   AND time = ?;
```

태그 선택 조건과 BASETIME 조건이 모두 있는데도 이 문장이 `ERR-2190: Invalid UPDATE/DELETE
condition`으로 거부되면 서버 버전을 확인합니다. 구버전 서버는 TAG data UPDATE의 NAME/TIME
bind를 지원하지 않습니다. 서버를 8.7.0 이상으로 업그레이드하고, named marker를 사용하면
해당 이름 기반 API를 지원하는 8.7.0 SDK를 함께 사용합니다.

같은 prepared statement를 재사용할 때는 SET, NAME, TIME 값을 모두 다시 바인딩합니다.
자세한 marker 규칙은
[TAG data UPDATE bind](/dbms/reference/sql/syntax-dictionary-sql/dml-syntax/tag-data-update-syntax/#tag-data-update-predicate-bind)를
참고하십시오.

대량 UPDATE 전에는 같은 WHERE 조건으로 `SELECT COUNT(*)`를 실행해 수정 대상 row 수를
확인합니다.

<a id="column-error-tag-data-update-set"></a>

## TAG data UPDATE SET 대상 컬럼 오류

SET 절은 실제 데이터 컬럼만 대상으로 합니다. PRIMARY KEY, BASETIME,
메타데이터 컬럼을 SET 대상으로 지정하면 오류가 발생합니다.

{{< callout type="warning" >}}
**SET 대상**

`value`와 사용자 데이터 컬럼은 UPDATE할 수 있습니다. `name`, `time`, METADATA 블록의 컬럼은
TAG data UPDATE의 SET 대상이 아닙니다.
{{< /callout >}}

### 증상

```sql
-- 오류: PRIMARY KEY 컬럼(name) 업데이트 시도
UPDATE sensor_tag
   SET name = 'new-sensor'
 WHERE name = 'old-sensor'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');

-- 오류: BASETIME 컬럼(time) 업데이트 시도
UPDATE sensor_tag
   SET time = NOW
 WHERE name = 'sensor-01'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');

-- 오류: 메타데이터 컬럼을 data UPDATE에서 수정
UPDATE sensor_tag
   SET location = 'zone-2'
 WHERE name = 'sensor-01'
   AND time >= TO_DATE('2026-07-01', 'YYYY-MM-DD');
```

### 컬럼 유형별 UPDATE 가능 여부

| 컬럼 유형 | 설명 | data UPDATE |
|-----------|------|:-----------:|
| PRIMARY KEY (`name`) | TAG를 식별하는 고유 키 | X |
| BASETIME (`time`) | 시계열 데이터의 타임스탬프 | X |
| 데이터 컬럼 (`value`, 보조 컬럼) | 실제 row 값 | O |
| `SUMMARIZED` 데이터 컬럼 | 통계 대상 데이터 컬럼 | O |
| 메타데이터 컬럼 | METADATA 블록의 태그 속성 | X |

### 해결 방법

데이터 값은 일반 UPDATE로 수정합니다.

```sql
UPDATE sensor_tag
   SET value = 99.9,
       status = 1
 WHERE name = 'sensor-01'
   AND time = TO_DATE('2026-07-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS');
```

메타데이터는 별도 구문을 사용합니다.

```sql
UPDATE sensor_tag METADATA
   SET location = 'zone-2'
 WHERE name = 'sensor-01';
```

태그 이름이나 시간 축을 변경해야 하는 경우에는 새 `name`/`time` 값으로 데이터를 삽입한 뒤
운영 정책에 따라 기존 데이터를 삭제합니다.

<a id="limitations-tag"></a>

## 제약 및 주의사항

### 지원하지 않는 기능

| 기능 | 상태 |
|------|------|
| 실제 시계열 데이터 UPDATE | 지원 (태그/축 조건 필요) |
| 메타데이터 UPDATE | 지원 (`UPDATE ... METADATA`) |
| DELETE | 지원 (`BEFORE` 또는 태그/축 조건) |
| 다중 PRIMARY KEY | 미지원 (단일 컬럼만) |
| BASETIME과 BASEDISTANCE 동시 사용 | 미지원 |
| ALTER TABLE (컬럼 삭제/변경) | 미지원 |

### 태그 수 제한

- 단일 TAG 테이블에 생성 가능한 태그 수는 시스템 설정에 따라 제한됩니다.
- 태그 수가 늘면 태그 인덱스와 메타데이터의 메모리 사용량도 증가하므로 운영 규모의 데이터로
  조회와 입력 성능을 측정합니다.
- 태그 이름이 레코드마다 고유한 값이 되도록 설계하면 안 됩니다 (안티패턴 — [센서별 테이블 생성](/dbms/data-modeling-table-design/table-types-patterns-type-anti/#per-sensor-create) 참고).

### 시간 역삽입 제한

- BASETIME 컬럼에는 임의의 과거 시각을 삽입할 수 있습니다.
- 늦게 도착한 데이터가 많은 워크로드는 실제 입력률과 조회 성능을 별도로 측정합니다.

### Cluster Edition 지원

TAG 테이블은 Cluster Edition에서 지원됩니다.

단, TAG data UPDATE는 Standard Edition 전용이며 Cluster Edition에서는 지원되지 않습니다.

### 요약

```
TAG 테이블 = 센서 이름 (PK) + 시간/거리 축 + 계측값
- INSERT/APPEND: O
- UPDATE: 실제 데이터 O (태그/축 조건), METADATA O
- DELETE: O (BEFORE 또는 태그/축 조건)
- METADATA: O (별도 속성 저장, UPDATE 가능)
```

---

**다음 읽을 내용**
- [TRANSACTION 테이블 설계](/dbms/rdb-table-usage/)
