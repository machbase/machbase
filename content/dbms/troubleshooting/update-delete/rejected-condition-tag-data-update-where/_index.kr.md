---
type: docs
title: 'TAG data UPDATE WHERE 조건이 거부될 때 (planned: dbms-nfx#3733)'
weight: 10
---

TAG 테이블의 UPDATE 문에서 WHERE 절에 `name` 이외의 컬럼 조건을 사용하면 오류가 발생하거나 예상치 못한 동작이 발생할 수 있습니다.

{{< callout type="warning" >}}
**현재 제약사항 (planned: dbms-nfx#3733)**

TAG 테이블의 UPDATE WHERE 조건은 현재 PRIMARY KEY(`name`) 기반 조건만 지원합니다. 이 기능은 향후 업데이트될 예정이며, 최신 릴리스 노트를 확인하세요.
{{< /callout >}}

## 증상

TAG 테이블에 UPDATE를 실행할 때 다음과 같은 오류가 발생합니다.

```
[ERR-02XXX]: WHERE condition is not supported for TAG table UPDATE
```

또는 WHERE 절에 `time`, `value` 등의 컬럼 조건을 포함한 UPDATE가 거부됩니다.

## 원인

TAG 테이블의 내부 구조는 시계열 데이터를 효율적으로 저장하도록 설계되어 있으며, PRIMARY KEY(`name`) 기반으로 데이터를 식별합니다. 현재 버전에서 UPDATE는 다음 조건만 지원합니다.

- **지원**: `WHERE name = '...'` — PRIMARY KEY 기반 단건 조건
- **미지원**: `WHERE time >= ... AND time <= ...` — 시간 범위 조건
- **미지원**: `WHERE value > ...` — 값 조건
- **미지원**: `WHERE name LIKE '...'` — 패턴 조건

## 진단

현재 실행하려는 UPDATE 문의 WHERE 절을 확인합니다.

```sql
-- 오류: time 컬럼 조건 사용 (현재 미지원)
UPDATE TAG TABLE sensor_tag SET value = 99.9
WHERE name = 'sensor-01' AND time = TO_DATE('2024-01-01 12:00:00');

-- 오류: 범위 조건 사용 (현재 미지원)
UPDATE TAG TABLE sensor_tag SET value = 99.9
WHERE time >= TO_DATE('2024-01-01') AND time < TO_DATE('2024-01-02');
```

## 임시 해결 방법

PRIMARY KEY(`name`) 조건만으로 UPDATE를 분리하여 실행합니다.

**1단계: 업데이트 대상 name 목록 조회**

```sql
-- 조건에 해당하는 name 목록을 먼저 확인
SELECT DISTINCT name FROM sensor_tag
WHERE time >= TO_DATE('2024-01-01') AND time < TO_DATE('2024-01-02');
```

**2단계: name별로 UPDATE 실행**

```sql
-- 조회된 name에 대해 개별적으로 UPDATE
UPDATE TAG TABLE sensor_tag SET value = 99.9 WHERE name = 'sensor-01';
UPDATE TAG TABLE sensor_tag SET value = 99.9 WHERE name = 'sensor-02';
```

애플리케이션에서 여러 건을 처리해야 한다면 1단계 결과를 순회하여 2단계 UPDATE를 반복 실행합니다.

## 향후 지원 예정

time, value 등 다양한 컬럼 조건을 WHERE 절에서 사용하는 TAG UPDATE 기능은 `planned: dbms-nfx#3733`으로 계획 중입니다. 최신 릴리스 노트를 확인하여 지원 여부를 확인하십시오.
