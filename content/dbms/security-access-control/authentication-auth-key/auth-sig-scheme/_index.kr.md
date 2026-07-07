---
type: docs
title: 'AUTH_SIG_SCHEME'
weight: 60
---

## 개요

`AUTH_SIG_SCHEME`은 AUTH KEY 챌린지 인증 시 클라이언트가 nonce에 서명할 때 사용하는 서명 스킴을 지정합니다. 소스 코드(`pmuAuth.h`)에 정의된 지원 값은 다음과 같습니다.

| 값 | 설명 |
|----|------|
| `ECDSA` | ECDSA 서명 방식 (ECDSA 키 사용 시 기본값) |
| `RSA_PKCS1_V15` | RSA PKCS#1 v1.5 서명 방식 (RSA 키 사용 시 기본값) |
| `RSA_PSS` | RSA-PSS 서명 방식 |

## 기본값 동작

`AUTH_SIG_SCHEME`을 생략하면 키 알고리즘에 따라 자동으로 기본 스킴이 선택됩니다.

- ECDSA 키 파일 사용 시: `ECDSA`
- RSA 키 파일 사용 시: `RSA_PKCS1_V15`

RSA-PSS를 사용하려면 반드시 `AUTH_SIG_SCHEME=RSA_PSS`를 명시해야 합니다.

## 지원 키 파라미터와 서명 스킴 매핑

| 키 알고리즘 | 지원 키 파라미터 | 지원 서명 스킴 | 해시 |
|------------|----------------|--------------|------|
| ECDSA | P-256, P-384, P-521 | `ECDSA` | SHA-256 |
| RSA | 2048, 3072, 4096 bits | `RSA_PKCS1_V15` | SHA-256 |
| RSA | 2048, 3072, 4096 bits | `RSA_PSS` | SHA-256 |

## 설정 방법

### JDBC

```
jdbc:machbase://localhost:5656/machbasedb?AUTH_MODE=CHALLENGE&AUTH_KEY_FILE=/home/app/.machbase/app_user.key&AUTH_SIG_SCHEME=RSA_PSS
```

### Python

```python
conn = mach.connect(
    host='localhost',
    port=5656,
    user='app_user',
    password='',
    auth_mode='CHALLENGE',
    auth_key_file='/home/app/.machbase/app_user_rsa.key',
    auth_sig_scheme='RSA_PSS'
)
```

## 주의 사항

- 등록된 공개키 타입과 클라이언트의 `AUTH_SIG_SCHEME`이 일치하지 않으면 인증이 실패합니다.  
  예: ECDSA 공개키를 등록하고 `AUTH_SIG_SCHEME=RSA_PKCS1_V15`로 접속하면 실패합니다.
- RSA 키로 `AUTH_SIG_SCHEME=RSA_PSS`를 사용하는 경우와 `RSA_PKCS1_V15`를 사용하는 경우는 동일한 RSA 공개키를 공유할 수 있습니다. 서명 스킴만 다를 뿐 키 자체는 같습니다.
- 알고리즘 선택 권장 사항은 [RSA / ECDSA / RSA_PSS 지원 범위](../support-scope-rsa-ecdsa-rsa-pss/) 페이지를 참고하세요.
