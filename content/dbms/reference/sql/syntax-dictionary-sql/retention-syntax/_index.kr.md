---
type: docs
title: '17.1.1.14 RETENTION syntax'
weight: 140
toc: true
---

RETENTION 정책은 테이블에서 오래된 데이터를 자동으로 삭제하는 기능입니다. 지정한 보존 기간이 지난 데이터를 주기적으로 삭제해 스토리지를 관리합니다.

## RETENTION 정책 생성

```sql
CREATE RETENTION policy_name DURATION duration { MONTH | DAY } INTERVAL interval { DAY | HOUR }
```

| 매개변수 | 설명 |
|----------|------|
| `policy_name` | 정책 이름 |
| `DURATION duration MONTH\|DAY` | 데이터 보존 기간 |
| `INTERVAL interval DAY\|HOUR` | 삭제 실행 주기 |

```sql
-- 1일 보존, 1시간마다 삭제 실행
CREATE RETENTION policy_1d_1h DURATION 1 DAY INTERVAL 1 HOUR;

-- 30일 보존, 1일마다 삭제 실행
CREATE RETENTION policy_30d_1d DURATION 30 DAY INTERVAL 1 DAY;

-- 3개월 보존, 1일마다 삭제 실행
CREATE RETENTION policy_3m_1d DURATION 3 MONTH INTERVAL 1 DAY;
```

## RETENTION 정책 삭제

```sql
DROP RETENTION policy_name
```

```sql
DROP RETENTION policy_1d_1h;
```

## 테이블에 RETENTION 정책 적용

```sql
ALTER TABLE table_name ADD RETENTION policy_name;
```

```sql
ALTER TABLE sensor_tag ADD RETENTION policy_1d_1h;
```

## 테이블에서 RETENTION 정책 해제

```sql
ALTER TABLE table_name DROP RETENTION;
```

```sql
ALTER TABLE sensor_tag DROP RETENTION;
```

## RETENTION 정책 목록 조회

시스템 테이블에서 등록된 RETENTION 정책과 적용 현황을 조회합니다.

```sql
-- 모든 RETENTION 정책 조회
SELECT * FROM M$RETENTION;

-- 특정 테이블에 적용된 정책 확인
SELECT TABLE_NAME, POLICY_NAME
  FROM M$RETENTION_TABLE
 WHERE TABLE_NAME = 'SENSOR_TAG';
```

## 전체 예시

```sql
-- 1. RETENTION 정책 생성 (1일 보존, 1시간마다 삭제)
CREATE RETENTION ret_1d DURATION 1 DAY INTERVAL 1 HOUR;

-- 2. TAG 테이블 생성
CREATE TAG TABLE sensor_tag (
    name  VARCHAR(40) PRIMARY KEY,
    time  DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

-- 3. 테이블에 RETENTION 정책 적용
ALTER TABLE sensor_tag ADD RETENTION ret_1d;

-- 4. 정책 적용 확인
SELECT * FROM M$RETENTION;

-- 5. 정책 해제
ALTER TABLE sensor_tag DROP RETENTION;

-- 6. 정책 삭제
DROP RETENTION ret_1d;
```

## 주의사항

- RETENTION 정책은 LOG 테이블과 TAG 테이블에 적용할 수 있습니다.
- 한 테이블에는 하나의 RETENTION 정책만 적용할 수 있습니다.
- RETENTION 삭제는 데이터를 영구 삭제하므로 신중하게 설정합니다.
- `INTERVAL`은 삭제 작업 실행 주기이며, 실제 삭제 시각은 약간 지연될 수 있습니다.

## 관련 문서

- [Retention Policy 역할](/dbms/core-concepts/features-concepts/#role-retention-policy) — 자동 데이터 삭제 정책 개념
