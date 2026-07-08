---
type: docs
title: 'LOOKUP SQL/JSON 지원표'
weight: 50
---

이 페이지는 LOOKUP 테이블의 SQL 기능과 JSON 관련 제약을 정리합니다.

## 현재 지원 현황

| 기능 | 현재 지원 | 계획 중 | 비고 |
|------|:---------:|:-------:|------|
| **기본 CRUD** | | | |
| INSERT | O | — | |
| SELECT | O | — | |
| UPDATE (PK 조건) | O | — | PK 컬럼 WHERE 조건 권장 |
| DELETE (PK 조건) | O | — | PK 컬럼 WHERE 조건 권장 |
| UPDATE (비-PK 조건) | X | O | planned: dbms-nfx#3696 |
| DELETE (비-PK 조건) | X | O | planned: dbms-nfx#3696 |
| **JSON 기능** | | | |
| JSON 타입 컬럼 | X | — | JSON 컬럼 생성 불가 |
| JSON path query (`$.key`) | X | — | JSON 타입 컬럼 미지원 |
| JSON PK | X | — | JSON 타입 컬럼 미지원 |
| JSON 컬럼 인덱스 | X | — | JSON 타입 컬럼 미지원 |
| **기타** | | | |
| Transaction | △ | — | 개별 DML 지원, 복합 트랜잭션 제한 |
| Prepared Statement | O | — | |
| Append API | X | — | 일반 INSERT 사용 |

## 현재 사용 가능한 방식

### JSON 문자열 저장

JSON 타입 컬럼은 사용할 수 없습니다. JSON 문서를 LOOKUP 테이블에 보관해야 하면 `VARCHAR` 컬럼에 문자열로 저장하고 애플리케이션에서 파싱합니다.

```sql
CREATE TABLE meta_table (
    id      INTEGER,
    name    VARCHAR(100),
    config  VARCHAR(4096),  -- JSON 문자열 저장
    PRIMARY KEY (id)
) ENGINE=LOOKUP;

INSERT INTO meta_table VALUES (1, 'device_a', '{"type":"sensor","unit":"celsius"}');
```

JSON 값을 조건으로 검색하려면 현재는 애플리케이션 레이어에서 처리해야 합니다.

### UPDATE/DELETE (PK 조건, 현재 지원)

```sql
-- PK 기반 UPDATE (권장)
UPDATE meta_table SET config = '{"type":"actuator"}' WHERE id = 1;

-- PK 기반 DELETE (권장)
DELETE FROM meta_table WHERE id = 1;
```

## 계획 중인 기능 (planned: dbms-nfx#3696)

다음 기능은 현재 미지원이며, 향후 업데이트에서 제공될 예정입니다.

- **비-PK UPDATE/DELETE**: PK 외 컬럼 조건으로 UPDATE/DELETE 수행

이 기능이 필요한 경우 구현 일정은 Machbase 릴리스 노트를 확인하세요.

## 현재 제약 우회 방법

| 필요 기능 | 현재 우회 방법 |
|----------|--------------|
| JSON path 검색 | `VARCHAR` 문자열을 애플리케이션에서 JSON 파싱 후 조건 적용 |
| 비-PK UPDATE | PK를 먼저 조회한 후 PK 조건으로 UPDATE |
| JSON 인덱스 | JSON 내 자주 검색하는 필드를 별도 컬럼으로 추출 |
