---
type: docs
title: '인증이 실패할 때'
weight: 30
---

서버에 접속은 시도되나 인증 단계에서 오류가 발생하는 경우를 다룹니다. Machbase는 비밀번호 인증과 AUTH KEY(공개키) 인증 두 가지를 지원합니다.

## 오류 메시지별 원인

| 메시지 | 원인 |
|--------|------|
| `Wrong password` | 비밀번호 불일치 |
| `Authentication failed` | 사용자명 또는 비밀번호 오류 |
| `Account locked` | 연속 인증 실패로 계정 잠금 |
| `Auth key not found` | 서버에 등록된 AUTH KEY 없음 |
| `Invalid auth key` | 키 파일 내용이 올바르지 않음 |
| `Password expired` | 비밀번호 유효기간 만료 (HIGH 보안 정책) |

## 비밀번호 인증 실패

### 기본 계정 정보 확인

| 항목 | 기본값 |
|------|--------|
| 사용자명 | `SYS` |
| 비밀번호 | `MANAGER` |

Machbase의 사용자명은 대문자로 저장됩니다. `sys`로 입력해도 `SYS`로 처리됩니다.
비밀번호는 대소문자를 구분하지 않습니다. `manager`와 `MANAGER`는 동일합니다.

### 비밀번호 재설정

SYS 계정으로 접속 가능한 다른 경로(예: 로컬 접속)가 있다면 비밀번호를 재설정합니다.

```sql
-- 사용자 비밀번호 변경
ALTER USER user_name IDENTIFIED BY 'new_password';
```

SYS 계정 자체를 잃었다면 Machbase 지원팀에 문의합니다.

### 보안 정책 확인

HIGH 보안 정책 적용 시 비밀번호 만료 또는 잠금이 발생할 수 있습니다.

```sql
-- 현재 보안 정책 확인
SELECT name, value FROM v$property WHERE name LIKE '%PASSWORD%';
```

계정 잠금 상태는 SYS 계정으로 해제합니다.

```sql
-- 계정 잠금 해제
ALTER USER locked_user ACCOUNT UNLOCK;
```

## AUTH KEY 인증 실패

Machbase는 공개키/개인키 쌍을 이용한 AUTH KEY 인증을 지원합니다.

### AUTH_MODE 설정 확인

```sql
-- AUTH_MODE 설정 확인
SELECT name, value FROM v$property WHERE name = 'AUTH_MODE';
```

AUTH KEY 인증을 사용하려면 값이 `CHALLENGE`여야 합니다.

### 개인키 파일 경로와 권한 확인

```bash
# 개인키 파일 존재 여부와 권한 확인
ls -la ~/.machbase/auth_key

# 개인키 파일 권한은 반드시 600이어야 합니다
chmod 600 ~/.machbase/auth_key
```

개인키 파일의 권한이 너무 넓으면(예: 644) Machbase가 보안 위험으로 판단하여 인증을 거부합니다.

### 서버에 등록된 공개키 확인

```sql
-- 특정 사용자의 등록된 AUTH KEY 목록
SELECT * FROM m$sys_auth_key WHERE user_name = 'SYS';

-- 모든 사용자의 AUTH KEY 확인
SELECT user_name, key_name, created_time FROM m$sys_auth_key;
```

등록된 키가 없거나 사용 중인 개인키와 쌍이 맞지 않으면 새 키 쌍을 생성하여 등록합니다.

```bash
# 새 키 쌍 생성
machsql -s localhost -u SYS -p MANAGER
```

```sql
-- 공개키 등록 (machsql에서)
CREATE AUTH KEY key_name FOR SYS FROM '/path/to/public_key.pub';
```

## 관련 섹션

- [연결할 수 없을 때](../connection/) — 인증 이전에 접속 자체가 안 될 때
- [오류 코드로 원인 찾기](../../troubleshooting/cause-lookup-error-codes/) — ERR-021xx 권한 오류 코드 목록
