---
type: docs
title: 'Retention Policy'
weight: 10
---

Retention Policy는 TAG 또는 LOG 테이블에 보존 기간을 설정하여 오래된 데이터를 자동으로 삭제하는 기능입니다.

## 전체 흐름

1. **[Retention Policy 생성](./create-retention-policy/)**: 보존 기간·삭제 주기 정의
2. **[테이블에 적용](./retention-policy/)**: `ALTER TABLE ... ADD RETENTION`
3. **[실행 상태 확인](./execution-status-check-state-retention/)**: `V$RETENTION_JOB` 조회
4. **[적용 해제](./detach-retention-policy/)**: `ALTER TABLE ... DROP RETENTION`
5. **[정책 삭제](./delete-retention-policy/)**: `DROP RETENTION`

## 정책 목록 조회

적용 중인 정책과 테이블 정보는 다음 시스템 뷰로 확인합니다.

```sql
-- 생성된 Retention Policy 목록
SELECT * FROM M$RETENTION;

-- 정책이 적용된 테이블 목록
SELECT * FROM V$RETENTION_JOB;
```

## 권한

Retention Policy 생성·삭제·적용은 **SYS 계정 권한**이 필요합니다. 일반 사용자가 정책을 관리하려면 SYS 권한 부여가 필요합니다.

> 상세 권한 요건은 [Retention 적용 가능 테이블과 SYS 권한 제약](./applicable-privileges-retention-sys/)을 참고하세요.
