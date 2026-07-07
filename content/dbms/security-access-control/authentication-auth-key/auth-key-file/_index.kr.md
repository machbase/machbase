---
type: docs
title: 'AUTH_KEY_FILE'
weight: 50
---

## 개요

`AUTH_KEY_FILE`은 AUTH KEY 챌린지 인증 시 클라이언트가 서명에 사용할 개인키 파일의 경로를 지정하는 설정입니다. 개인키는 클라이언트 호스트에만 보관하며 네트워크로 전송되지 않습니다.

## 파일 형식

개인키 파일은 PEM 형식의 암호화되지 않은 개인키입니다.

- ECDSA 키: `-----BEGIN EC PRIVATE KEY-----` 형식
- RSA 키: `-----BEGIN RSA PRIVATE KEY-----` 형식

## 키 파일 생성

### ECDSA P-256 (권장)

```bash
openssl ecparam -name prime256v1 -genkey -noout -out ~/.machbase/app_user.key
openssl ec -in ~/.machbase/app_user.key -pubout -out ~/.machbase/app_user.pub
chmod 600 ~/.machbase/app_user.key
```

### ECDSA P-384

```bash
openssl ecparam -name secp384r1 -genkey -noout -out ~/.machbase/app_user_p384.key
openssl ec -in ~/.machbase/app_user_p384.key -pubout -out ~/.machbase/app_user_p384.pub
chmod 600 ~/.machbase/app_user_p384.key
```

### ECDSA P-521

```bash
openssl ecparam -name secp521r1 -genkey -noout -out ~/.machbase/app_user_p521.key
openssl ec -in ~/.machbase/app_user_p521.key -pubout -out ~/.machbase/app_user_p521.pub
chmod 600 ~/.machbase/app_user_p521.key
```

### RSA 2048-bit

```bash
openssl genrsa -out ~/.machbase/app_user_rsa.key 2048
openssl rsa -in ~/.machbase/app_user_rsa.key -pubout -out ~/.machbase/app_user_rsa.pub
chmod 600 ~/.machbase/app_user_rsa.key
```

RSA 3072-bit, 4096-bit 키를 사용하려면 `openssl genrsa`의 마지막 인자를 각각 `3072`, `4096`으로 지정합니다.

## 파일 권한 설정

개인키 파일은 반드시 소유자만 읽을 수 있도록 권한을 설정해야 합니다. 권한이 느슨하면 인증이 거부될 수 있습니다.

```bash
chmod 600 ~/.machbase/app_user.key
```

권장 디렉토리 구조:

```
~/.machbase/
├── app_user.key      # 개인키 (소유자 읽기 전용, chmod 600)
└── app_user.pub      # 공개키 (서버 등록용)
```

## 연결 옵션 지정 방법

### JDBC

```
jdbc:machbase://localhost:5656/machbasedb?AUTH_MODE=CHALLENGE&AUTH_KEY_FILE=/home/app/.machbase/app_user.key
```

### Python

```python
conn = mach.connect(
    host='localhost',
    port=5656,
    user='app_user',
    password='',
    auth_mode='CHALLENGE',
    auth_key_file='/home/app/.machbase/app_user.key'
)
```

### Go

```go
dsn := "app_user:@localhost:5656/machbasedb?AUTH_MODE=CHALLENGE&AUTH_KEY_FILE=/home/app/.machbase/app_user.key"
```

## 주의 사항

- `AUTH_KEY_FILE` 경로에 지정된 파일이 존재하지 않거나 읽기 권한이 없으면 인증이 실패합니다.
- 개인키 파일은 정기적으로 갱신하고, 유출 시 즉시 서버 측 공개키를 교체합니다. ([AUTH KEY 삭제](../user-auth-key/delete-auth-key/) 및 [AUTH KEY 추가](../user-auth-key/alter-user-add-auth-key/) 참고)
- `AUTH_KEY_FILE`을 지정하지 않으면 `AUTH_MODE=CHALLENGE`로 설정해도 서명을 생성할 수 없어 인증이 실패합니다.
