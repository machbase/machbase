---
type: docs
title: '14.4.1.1 CREATE USER ... WITH AUTH KEY'
weight: 10
---

## 개요

`CREATE USER ... WITH AUTH KEY` 구문은 사용자를 생성하면서 동시에 공개키를 등록합니다. 사용자 생성 시 등록한 첫 번째 AUTH KEY는 즉시 활성 상태(`ACTIVATED=1`)로 설정됩니다.

## 키 쌍 생성

먼저 openssl로 키 쌍을 생성합니다.

**ECDSA P-256 (권장)**

```bash
openssl ecparam -name prime256v1 -genkey -noout -out app_user_ecdsa.key
openssl ec -in app_user_ecdsa.key -pubout -out app_user_ecdsa.pub
chmod 600 app_user_ecdsa.key
```

**RSA 2048-bit**

```bash
openssl genrsa -out app_user_rsa.key 2048
openssl rsa -in app_user_rsa.key -pubout -out app_user_rsa.pub
chmod 600 app_user_rsa.key
```

## 공개키 변환

SQL 문자열에 넣기 위해 공개키 PEM 파일의 줄바꿈을 `\n`으로 이스케이프합니다.

```bash
awk '{printf "%s\\n", $0}' app_user_ecdsa.pub
```

출력 예:

```
-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEshxcrSmtosaqWjhRkOoAw4v3QWqL\ns3OFN2jbJrustEc12uAn/IdtTG94KK69bY7DWl80pzQ48dNL+ENXe8PT3g==\n-----END PUBLIC KEY-----\n
```

## 등록 SQL 파일 자동 생성

```bash
KEY_ESCAPED=$(awk '{printf "%s\\n", $0}' app_user_ecdsa.pub)

cat > create_app_user.sql <<EOF
CREATE USER app_user IDENTIFIED BY 'App#1234'
WITH AUTH KEY (
    key='${KEY_ESCAPED}',
    valid_before='2047-12-31',
    comment='initial ecdsa p256 key'
);
EOF
```

## 구문

```sql
CREATE USER app_user IDENTIFIED BY 'App#1234'
WITH AUTH KEY (
    key='-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEshxcrSmtosaqWjhRkOoAw4v3QWqL\ns3OFN2jbJrustEc12uAn/IdtTG94KK69bY7DWl80pzQ48dNL+ENXe8PT3g==\n-----END PUBLIC KEY-----\n',
    valid_before='2047-12-31',
    comment='initial ecdsa p256 key'
);
```

## AUTH KEY 절 파라미터

| 파라미터 | 필수 여부 | 설명 |
|---------|---------|------|
| `key` | 필수 | PEM 형식 공개키 문자열 (줄바꿈을 `\n`으로 이스케이프) |
| `valid_before` | 필수 | 키 만료일 (`YYYY-MM-DD` 형식) |
| `comment` | 필수 | 키 식별 메모 |

주의 사항:

- `valid_before`는 `YYYY-MM-DD` 형식만 허용합니다. 시각이 포함된 `YYYY-MM-DD HH24:MI:SS` 형식은 허용되지 않습니다.
- `valid_before`는 생략하거나 NULL/무제한으로 둘 수 없습니다.
- `comment`는 현재 AUTH KEY 구문에서 필수입니다.
- 사용자는 비밀번호와 AUTH KEY를 동시에 보유할 수 있습니다. 실제 인증은 클라이언트의 `AUTH_MODE` 선택에 따라 비밀번호 또는 챌린지 방식 중 하나만 수행되며, 실패 시 다른 방식으로 자동 전환되지 않습니다.

## 등록 확인

```sql
SELECT key_id, user_name, key_algo, key_param, activated, valid_before, comment
  FROM V$USER_AUTH_KEYS
 WHERE user_name = 'APP_USER'
 ORDER BY key_id;
```
