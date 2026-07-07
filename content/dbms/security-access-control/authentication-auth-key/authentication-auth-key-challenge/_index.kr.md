---
type: docs
title: 'AUTH KEY challenge 인증'
weight: 20
---

## 개요

AUTH KEY challenge 인증은 공개키 암호화를 기반으로 한 챌린지-응답 방식의 인증 메커니즘입니다. 비밀번호를 네트워크로 전송하지 않고, 서버가 보낸 일회성 챌린지(nonce)에 클라이언트가 개인키로 서명하여 신원을 증명합니다.

## 인증 흐름

```
클라이언트                                      서버
   |                                             |
   |---- 접속 요청 (AUTH_MODE=CHALLENGE) ------->|
   |                                             | nonce(32바이트) 생성
   |<--- nonce 전송 ----------------------------|
   |                                             |
   | 개인키(AUTH_KEY_FILE)로 nonce 서명          |
   |                                             |
   |---- 서명값 + 사용자명 전송 --------------->|
   |                                             | 등록된 공개키로 서명 검증
   |<--- 인증 성공 / 실패 응답 ----------------|
   |                                             |
```

1. 클라이언트가 `AUTH_MODE=CHALLENGE` 옵션으로 접속을 요청합니다.
2. 서버가 32바이트 nonce를 생성하여 클라이언트에 전송합니다.
3. 클라이언트가 `AUTH_KEY_FILE`에 지정된 개인키 파일로 nonce에 서명합니다.
4. 서버가 해당 사용자에 등록된 공개키(`V$USER_AUTH_KEYS`)로 서명을 검증합니다.
5. 검증에 성공하면 세션이 개시됩니다. 실패하면 연결이 거부됩니다.

## 보안 특성

- **비밀번호 미전송**: 인증 과정에서 비밀번호가 네트워크를 경유하지 않습니다.
- **일회성 챌린지**: nonce는 매 접속마다 새로 생성되므로 재전송 공격이 불가능합니다.
- **개인키 보호**: 개인키는 클라이언트 호스트에만 존재하며 네트워크로 전송되지 않습니다.
- **서버 측 공개키**: 서버에는 공개키만 저장하므로 서버가 침해되어도 개인키는 노출되지 않습니다.

## 사전 준비 순서

### 1단계: 키 쌍 생성

ECDSA P-256 키를 생성하는 예입니다. (권장 알고리즘)

```bash
openssl ecparam -name prime256v1 -genkey -noout -out app_user_ecdsa.key
openssl ec -in app_user_ecdsa.key -pubout -out app_user_ecdsa.pub
chmod 600 app_user_ecdsa.key
```

RSA 2048-bit 키를 생성하는 예입니다.

```bash
openssl genrsa -out app_user_rsa.key 2048
openssl rsa -in app_user_rsa.key -pubout -out app_user_rsa.pub
chmod 600 app_user_rsa.key
```

### 2단계: 공개키를 SQL에 넣을 형식으로 변환

공개키 PEM 파일의 줄바꿈을 `\n`으로 이스케이프하여 한 줄 문자열로 변환합니다.

```bash
awk '{printf "%s\\n", $0}' app_user_ecdsa.pub
```

### 3단계: 사용자 생성 또는 기존 사용자에 AUTH KEY 추가

사용자 생성 시 공개키를 함께 등록합니다.

```sql
CREATE USER app_user IDENTIFIED BY 'App#1234'
WITH AUTH KEY (
    key='-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEshxcrSmtosaqWjhRkOoAw4v3QWqL\ns3OFN2jbJrustEc12uAn/IdtTG94KK69bY7DWl80pzQ48dNL+ENXe8PT3g==\n-----END PUBLIC KEY-----\n',
    valid_before='2047-12-31',
    comment='initial ecdsa key'
);
```

기존 사용자에게 AUTH KEY를 추가합니다.

```sql
ALTER USER app_user ADD AUTH KEY (
    key='-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEshxcrSmtosaqWjhRkOoAw4v3QWqL\ns3OFN2jbJrustEc12uAn/IdtTG94KK69bY7DWl80pzQ48dNL+ENXe8PT3g==\n-----END PUBLIC KEY-----\n',
    valid_before='2047-12-31',
    comment='initial ecdsa key'
);
```

### 4단계: 클라이언트 접속 설정

클라이언트 접속 시 다음 옵션을 지정합니다.

| 옵션 | 값 | 설명 |
|------|----|------|
| `AUTH_MODE` | `CHALLENGE` | 챌린지 인증 방식 선택 |
| `AUTH_KEY_FILE` | `/path/to/app_user_ecdsa.key` | 개인키 파일 경로 |
| `AUTH_SIG_SCHEME` | `ECDSA` (ECDSA 키 시 생략 가능) | 서명 스킴 |

## 인증 실패 조건

다음 경우 AUTH KEY 인증이 실패합니다.

- 등록된 공개키가 없거나 모두 비활성화 상태인 경우
- 공개키 타입과 `AUTH_SIG_SCHEME` 설정이 일치하지 않는 경우
- `valid_before` 만료된 키만 존재하는 경우
- 개인키 파일이 없거나 읽을 수 없는 경우

AUTH KEY 인증 실패 시 비밀번호 인증으로 자동 전환되지 않습니다. 필요하면 `AUTH_MODE=PASSWORD`로 명시하여 별도 접속해야 합니다.
