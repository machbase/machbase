---
type: docs
title: 'SYS AS USER 인증 제약'
weight: 30
---

## 개요

SYS는 Machbase의 관리자 계정입니다. SYS 계정의 AUTH KEY 인증 사용과 관련하여 다음 사항을 이해하고 운영해야 합니다.

## SYS 계정 인증 특성

SYS 계정은 서버 관리 목적으로 사용되며, 인증 방식 사용에 다음과 같은 제약이 있습니다.

- `AUTH_MODE=CHALLENGE`로 서버 전체를 설정해도, SYS 계정에 AUTH KEY가 등록되어 있지 않으면 SYS는 비밀번호 인증으로 접속해야 합니다.
- CHALLENGE 전용 모드에서 SYS AUTH KEY 미등록 시 SYS 접속이 불가능해질 수 있으므로, CHALLENGE 모드 전환 전 SYS에도 AUTH KEY를 등록하거나, 서버 직접 접속 수단을 별도로 확보해야 합니다.

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

## CHALLENGE 모드 전환 시 SYS 접속 보장

서버를 `AUTH_MODE=CHALLENGE`로 전환하기 전에 SYS 계정 접속 수단을 보장해야 합니다.

**옵션 1**: SYS 계정에 AUTH KEY 등록 후 CHALLENGE 모드 전환

**옵션 2**: 서버 로컬 접속 방법 확보 (유닉스 도메인 소켓 등)

어떤 계정도 접속할 수 없는 상태가 되면 `machbase.conf`를 직접 수정하고 서버를 재시작하여 `AUTH_MODE=PASSWORD`로 복구해야 합니다.
