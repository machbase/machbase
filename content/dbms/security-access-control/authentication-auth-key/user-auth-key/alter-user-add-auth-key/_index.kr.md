---
type: docs
title: '14.4.1.2 ALTER USER ... ADD AUTH KEY'
weight: 20
---

## 개요

`ALTER USER ... ADD AUTH KEY` 구문은 기존 사용자에게 공개키를 추가합니다. 추가된 AUTH KEY는 즉시 활성 상태(`ACTIVATED=1`)로 등록됩니다.

비밀번호 인증만 사용하던 기존 사용자에게 AUTH KEY를 추가하면 이후 비밀번호 또는 AUTH KEY 두 가지 방식 모두로 인증할 수 있습니다. 실제 어떤 방식을 사용할지는 클라이언트의 `AUTH_MODE` 설정에 따라 결정됩니다.

## 구문

```sql
ALTER USER app_user ADD AUTH KEY (
    key='-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEshxcrSmtosaqWjhRkOoAw4v3QWqL\ns3OFN2jbJrustEc12uAn/IdtTG94KK69bY7DWl80pzQ48dNL+ENXe8PT3g==\n-----END PUBLIC KEY-----\n',
    valid_before='2047-12-31',
    comment='ecdsa p256 key'
);
```

RSA 공개키 추가 예:

```sql
ALTER USER app_user ADD AUTH KEY (
    key='-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqO+tddiAQzsT8iajPy5Q\nJPamIlyq2zB01wgHSTs3OOrvw0uKoFQDcqKaDzRya73LETXIEev3nwhGCnG4Sjed\nMHj3EH9/rRJphFtv/dzw0OHum/UhVulRIXUYzrTbKPTQ+qyjS8UXTteMncf9OOh4\nAQyS4+iJW+U344fxymR8USRgZ25N9jhf2gkKnn5YSPZHf8ZHQGeA7OXANBwPmH5d\nQwfqghXRa7Nk1hmkIAnQQXCBJW/Lin+xwQfqv8DVwNaiziz77voPwaeD5akq1JYW\nvcPlOnh+NN3tpu5gudke/t/In4NFJ3W94unVcYIfxcdDSoht3AMObGmuDazOjQJFG\nQIDAQAB\n-----END PUBLIC KEY-----\n',
    valid_before='2048-01-31',
    comment='rsa 2048 rollover candidate'
);
```

## AUTH KEY 절 파라미터

| 파라미터 | 필수 여부 | 설명 |
|---------|---------|------|
| `key` | 필수 | PEM 형식 공개키 문자열 (줄바꿈을 `\n`으로 이스케이프) |
| `valid_before` | 필수 | 키 만료일 (`YYYY-MM-DD` 형식) |
| `comment` | 필수 | 키 식별 메모 |

`key`, `valid_before`, `comment`는 현재 AUTH KEY 구문에서 모두 필수입니다.
`valid_before`는 생략하거나 NULL/무제한으로 둘 수 없습니다.

## 공개키 변환 및 SQL 파일 생성

```bash
KEY_ESCAPED=$(awk '{printf "%s\\n", $0}' app_user_ecdsa.pub)

cat > add_app_user_key.sql <<EOF
ALTER USER app_user ADD AUTH KEY (
    key='${KEY_ESCAPED}',
    valid_before='2047-12-31',
    comment='ecdsa p256 production key'
);
EOF
```

## 키 롤오버에서의 활용

한 사용자에게 여러 AUTH KEY를 등록할 수 있으므로, 무중단 키 교체(롤오버)가 가능합니다.

```sql
-- 1. 신규 공개키 추가 (이전 키와 신규 키 모두 활성 상태)
ALTER USER app_user ADD AUTH KEY (
    key='<신규_공개키>',
    valid_before='2049-12-31',
    comment='2025 rotation key'
);

-- 2. 클라이언트가 신규 개인키로 접속 전환 완료 후 이전 키 비활성화
ALTER USER app_user DEACTIVATE AUTH KEY ID 1;

-- 3. 이전 키 삭제
ALTER USER app_user DROP AUTH KEY ID 1;
```

## 등록 확인

```sql
SELECT key_id, user_name, key_algo, key_param, activated, valid_before, comment
  FROM V$USER_AUTH_KEYS
 WHERE user_name = 'APP_USER'
 ORDER BY key_id;
```
