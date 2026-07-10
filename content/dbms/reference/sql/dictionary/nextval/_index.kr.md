---
type: docs
title: '17.1.3.6 NEXTVAL 함수'
weight: 60
toc: true
---

`NEXTVAL`은 Lookup 테이블의 Sequence 컬럼에 대해 다음 자동 증가값을 반환합니다. `INSERT` 문에서만 사용할 수 있습니다.

## 문법

```sql
NEXTVAL(sequence_column)
```

- `sequence_column`은 `PROPERTY(SEQUENCE=...)` 속성으로 생성된 컬럼이어야 합니다.
- `INSERT` 문 이외의 컨텍스트(SELECT, WHERE 등)에서는 사용할 수 없습니다.

---

## Sequence 컬럼 생성

Sequence 컬럼은 Lookup 테이블에서만 지원합니다. `PROPERTY(SEQUENCE=1)` 속성을 지정하면 해당 컬럼이 자동 증가 Sequence 컬럼이 됩니다.

```sql
-- Sequence 컬럼을 포함한 Lookup 테이블 생성
CREATE TABLE seq_lookup (
    id   INTEGER PROPERTY(SEQUENCE=1),
    name VARCHAR(64)
) TABLE_TYPE=LOOKUP;
```

---

## NEXTVAL 사용

```sql
-- NEXTVAL로 자동 증가 ID 삽입
INSERT INTO seq_lookup (id, name) VALUES (NEXTVAL(id), 'sensor-a');
INSERT INTO seq_lookup (id, name) VALUES (NEXTVAL(id), 'sensor-b');
INSERT INTO seq_lookup (id, name) VALUES (NEXTVAL(id), 'sensor-c');

-- 결과 확인
SELECT * FROM seq_lookup;
id    name
----------
1     sensor-a
2     sensor-b
3     sensor-c
```

---

## 주의사항

- `NEXTVAL`은 `INSERT` 문에서만 사용할 수 있습니다.
- Sequence 컬럼은 **Lookup 테이블**에서만 지원됩니다. TAG, LOG, VOLATILE, RDB 테이블에서는 사용할 수 없습니다.
- Sequence 번호는 트랜잭션 롤백이나 오류 발생 시에도 재사용되지 않을 수 있습니다 (gap이 발생할 수 있음).
- 자세한 DDL 설명은 [DDL - Sequence Column](../../syntax-dictionary-sql/) 문서를 참고하십시오.
