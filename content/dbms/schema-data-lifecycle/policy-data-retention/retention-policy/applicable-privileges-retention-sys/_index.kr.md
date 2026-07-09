---
type: docs
title: 'Retention 적용 가능 테이블과 SYS 권한 제약'
weight: 50
---

## 적용 가능 테이블

Retention Policy는 **TAG, KV, LOG 테이블**에 적용할 수 있습니다. 소스 코드(`qpvRetention.c`) 기준으로, TAG_TABLE, KEYVALUE_TABLE, LOG_TABLE 이외의 테이블 타입에 Retention Policy를 적용하면 오류가 발생합니다.

| 테이블 타입 | Retention Policy 적용 |
|------------|---------------------|
| TAG | O |
| KV | O |
| LOG | O |
| RDB | X |
| VOLATILE | X |
| LOOKUP | X |

```sql
-- 오류: RDB 테이블에 적용 시
ALTER TABLE orders ADD RETENTION policy_30d;
-- → ERR_QP_RETENTION_INVALID_TABLE_TYPE (또는 유사한 오류)
```

## 권한 제약

Retention Policy의 생성과 삭제는 **SYS 계정** 또는 SYS 권한을 가진 사용자만 수행할 수 있습니다.
정책 적용과 해제는 테이블 소유자가 자신의 테이블에 대해 수행할 수 있습니다.

```sql
-- SYS 계정으로 접속
machsql -u SYS -p MANAGER

-- Retention Policy 생성
CREATE RETENTION policy_30d DURATION 30 DAY INTERVAL 1 DAY;

-- 테이블에 적용
ALTER TABLE sensor_tag ADD RETENTION policy_30d;
```

일반 사용자(SYS 권한 없음)는 Retention Policy를 생성하거나 삭제할 수 없습니다. 다만 SYS가
생성한 정책을 자신의 테이블에 적용하거나 해제할 수 있습니다. 다른 사용자의 테이블에 정책을
적용하거나 해제하려고 하면 권한 오류가 발생합니다.

## 정책 정보 확인 뷰

| 뷰 이름 | 설명 |
|--------|------|
| `M$RETENTION` | 생성된 Retention Policy 목록 (이름, DURATION, INTERVAL) |
| `V$RETENTION_JOB` | 정책이 적용된 테이블 목록과 실행 상태 |

```sql
-- 정책 목록
SELECT * FROM M$RETENTION;

-- 적용 상태
SELECT USER_NAME, TABLE_NAME, POLICY_NAME, STATE, LAST_DELETED_TIME
FROM V$RETENTION_JOB;
```
