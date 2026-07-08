---
type: docs
title: 'SYS AS USER 인증 제약'
weight: 30
---

## 개요

SYS는 Machbase의 관리자 계정입니다. SYS 계정의 AUTH KEY 인증 사용과 관련하여 다음 사항을 이해하고 운영해야 합니다.

## SYS 계정 인증 특성

SYS 계정은 서버 관리 목적으로 사용되며, 인증 방식 사용에 다음과 같은 사항을 이해해야 합니다.

- `AUTH_MODE=CHALLENGE`는 서버 전역 설정이 아니라 클라이언트 연결 옵션입니다.
- SYS 계정으로 CHALLENGE 인증을 사용하려면 SYS 계정에도 AUTH KEY를 등록해야 합니다.
- SYS 계정에 AUTH KEY가 없으면 PASSWORD 방식 연결을 사용합니다.

## SYS 계정 AUTH KEY 등록

SYS 계정도 일반 사용자와 동일한 방법으로 AUTH KEY를 등록할 수 있습니다.

```bash
# SYS용 ECDSA P-256 키 생성
openssl ecparam -name prime256v1 -genkey -noout -out sys_ecdsa.key
openssl ec -in sys_ecdsa.key -pubout -out sys_ecdsa.pub
chmod 600 sys_ecdsa.key

# 공개키 변환
KEY_ESCAPED=$(awk '{printf "%s\\n", $0}' sys_ecdsa.pub)
```

```sql
-- SYS 계정에 AUTH KEY 추가 (SYS 계정으로 실행)
ALTER USER SYS ADD AUTH KEY (
    key='<변환된_공개키>',
    valid_before='2047-12-31',
    comment='sys admin key'
);
```

## 운영 환경 권장 사항

SYS 계정을 일상적인 애플리케이션 접속에 직접 사용하는 것은 권장하지 않습니다.

**권장 운영 방식:**

1. **전용 애플리케이션 계정 사용**: 각 애플리케이션별로 전용 계정을 생성하고 필요한 최소 권한만 부여합니다.
2. **SYS 계정 직접 사용 최소화**: SYS 계정은 계정 관리, 권한 부여, 유지보수 등 관리 작업에만 사용합니다.
3. **SYS 비밀번호 보호**: SYS 비밀번호는 안전하게 관리하고 정기적으로 변경합니다.

```sql
-- 애플리케이션 전용 계정 생성 예
CREATE USER app_user IDENTIFIED BY 'App#StrongPwd1' PASSWORD POLICY HIGH;
GRANT SELECT, INSERT ON sys.sensor_log TO app_user;

-- app_user에 AUTH KEY 등록
ALTER USER app_user ADD AUTH KEY (
    key='<공개키>',
    valid_before='2047-12-31',
    comment='app_user production key'
);
```

## SYS 계정 CHALLENGE 인증 사용

SYS 계정으로 CHALLENGE 인증을 사용해야 한다면 먼저 SYS 계정에 AUTH KEY를 등록하고,
클라이언트 연결 옵션에 `AUTH_MODE=CHALLENGE`, `AUTH_KEY_FILE`,
`AUTH_SIG_SCHEME`을 지정합니다.
