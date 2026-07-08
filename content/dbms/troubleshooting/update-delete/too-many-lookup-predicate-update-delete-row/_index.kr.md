---
type: docs
title: 'LOOKUP 일반 predicate UPDATE/DELETE가 예상보다 많은 row에 적용될 때 (planned: dbms-nfx#3696)'
weight: 30
---

LOOKUP 테이블에서 PRIMARY KEY가 아닌 일반 컬럼 조건(일반 predicate)으로 UPDATE 또는 DELETE를 실행하면 의도한 것보다 많은 행에 영향을 미칠 수 있습니다.

{{< callout type="warning" >}}
**현재 제약사항 (planned: dbms-nfx#3696)**

LOOKUP 테이블의 UPDATE/DELETE는 PRIMARY KEY 기반 조건으로만 정확한 단건 처리가 보장됩니다. 비-PK 조건을 사용한 UPDATE/DELETE의 정확한 필터링은 향후 지원 예정입니다.
{{< /callout >}}

## 증상

비-PK 컬럼 조건으로 UPDATE/DELETE를 실행했을 때 다음 현상이 발생합니다.

- 조건에 맞지 않는 행까지 함께 수정되거나 삭제됨
- 예상한 것보다 많은 `affected rows` 수 반환
- 데이터 일관성 문제 발생

## 원인

LOOKUP 테이블의 내부 인덱스는 PRIMARY KEY 기반으로 최적화되어 있습니다. 비-PK 컬럼(일반 predicate)을 WHERE 절에 사용하면 인덱스를 통한 정확한 행 식별이 어려워, 내부적으로 더 넓은 범위의 행이 처리 대상에 포함될 수 있습니다.

```sql
-- 문제 발생 가능: 비-PK 컬럼(location)을 조건으로 사용
DELETE FROM equipment WHERE location = 'A동';

-- 문제 발생 가능: 비-PK 컬럼을 조건으로 UPDATE
UPDATE equipment SET status = 'inactive' WHERE department = '생산1팀';
```

## 진단

UPDATE/DELETE 실행 전에 SELECT로 먼저 영향 범위를 확인합니다.

```sql
-- 먼저 영향받을 행 수와 대상 확인
SELECT COUNT(*), eq_id, location FROM equipment WHERE location = 'A동';
```

반환된 건수가 예상과 다르다면 비-PK 조건 필터링 문제일 수 있습니다.

## 임시 해결 방법

항상 PRIMARY KEY 조건을 포함하여 UPDATE/DELETE를 실행합니다.

**1단계: 영향 범위 확인**

```sql
-- 조건에 해당하는 PK 목록을 먼저 조회
SELECT eq_id FROM equipment WHERE location = 'A동';
```

**2단계: PK 기반으로 개별 처리**

```sql
-- PRIMARY KEY(eq_id)를 명시하여 정확하게 처리
DELETE FROM equipment WHERE eq_id = 'EQ-001';
DELETE FROM equipment WHERE eq_id = 'EQ-002';

-- UPDATE도 동일하게 PK 조건을 포함
UPDATE equipment SET status = 'inactive' WHERE eq_id = 'EQ-001';
```

**일괄 처리가 필요한 경우**

애플리케이션 레이어에서 1단계 결과의 PK 목록을 순회하며 2단계 처리를 반복합니다. 이렇게 하면 의도한 행에만 정확히 변경이 적용됩니다.

## 데이터 정합성 확인

UPDATE/DELETE 후에는 반드시 결과를 확인합니다.

```sql
-- 변경 후 결과 확인
SELECT eq_id, location, status FROM equipment WHERE location = 'A동';
```

## 향후 지원 예정

비-PK 컬럼 조건을 사용한 LOOKUP 테이블의 정확한 UPDATE/DELETE 필터링은 `planned: dbms-nfx#3696`으로 계획 중입니다. 최신 릴리스 노트를 확인하십시오.
