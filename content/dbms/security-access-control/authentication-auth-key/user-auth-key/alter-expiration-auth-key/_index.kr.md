---
type: docs
title: 'AUTH KEY 만료 변경'
weight: 40
---

## 개요

등록된 AUTH KEY의 유효 기간(`valid_before`)을 변경합니다. 만료일이 지난 AUTH KEY는 인증에 사용할 수 없으며, 오류가 반환됩니다.

## 구문

```sql
-- AUTH KEY 유효 기간 변경
ALTER USER app_user ALTER AUTH KEY ID <key_id> VALID_BEFORE='YYYY-MM-DD';
```

## 예제

```sql
-- key_id 3번 키의 만료일을 2048-06-30으로 변경
ALTER USER app_user ALTER AUTH KEY ID 3 VALID_BEFORE='2048-06-30';

-- key_id 2번 키의 만료일을 연장
ALTER USER app_user ALTER AUTH KEY ID 2 VALID_BEFORE='2049-12-31';
```

## 주의 사항

- `VALID_BEFORE` 형식은 `YYYY-MM-DD`만 허용합니다. 시각이 포함된 `YYYY-MM-DD HH24:MI:SS` 형식은 허용되지 않습니다.
- 이미 만료된 키의 만료일을 미래 날짜로 연장하면 해당 키는 즉시 다시 사용 가능해집니다. 단, 키가 비활성화 상태(`ACTIVATED=0`)이면 만료일 연장만으로는 인증에 사용할 수 없습니다.
- 만료일이 없는(무제한) 키로 변경하는 것은 현재 이 구문으로 지원되지 않습니다. 무제한으로 변경하려면 해당 키를 삭제하고 재등록하세요.

## key_id 확인 방법

```sql
SELECT key_id, user_name, key_algo, activated, valid_before, comment
  FROM V$USER_AUTH_KEYS
 WHERE user_name = 'APP_USER'
 ORDER BY key_id;
```

## 만료 KEY 처리 절차

만료가 임박한 키는 다음 절차로 교체합니다.

```sql
-- 1. 현재 키 상태 확인
SELECT key_id, activated, valid_before, comment
  FROM V$USER_AUTH_KEYS
 WHERE user_name = 'APP_USER';

-- 2. 신규 키 추가
ALTER USER app_user ADD AUTH KEY (
    key='<신규_공개키>',
    valid_before='2049-12-31',
    comment='renewal key'
);

-- 3. 클라이언트 전환 후 기존 키 만료일 단축 또는 삭제
ALTER USER app_user ALTER AUTH KEY ID 1 VALID_BEFORE='2025-07-31';
-- 또는
ALTER USER app_user DROP AUTH KEY ID 1;
```
