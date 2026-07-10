---
type: docs
title: '14.4 인증키 관리'
weight: 40
toc: true
---
## AUTH KEY란

AUTH KEY는 공개키 기반 챌린지-응답(challenge-response) 인증 방식입니다. 클라이언트가 개인키로 서버의 챌린지(nonce)에 서명하면, 서버가 등록된 공개키로 서명을 검증합니다. 비밀번호가 네트워크를 경유하지 않으므로 도청이나 재전송 공격에 강합니다.

## 비밀번호 인증과 AUTH KEY 인증 비교

| 항목 | 비밀번호 인증 | AUTH KEY 인증 |
|------|-------------|--------------|
| 인증 방식 | 비밀번호 전송 | 챌린지-응답 서명 |
| 네트워크 전송 | 비밀번호(해시) 전송 | 서명값만 전송 |
| 재전송 공격 | 취약 | 강건 (nonce 일회성) |
| 키 관리 | 비밀번호 주기 변경 필요 | 개인키 파일 보호 |
| 만료 관리 | 비밀번호 만료 | AUTH KEY `valid_before` 설정 |
| 복수 키 | 불가 | 가능 (롤오버 지원) |

## 인증 흐름 요약

1. 클라이언트가 접속 요청 (`AUTH_MODE=CHALLENGE`)
2. 서버가 32바이트 nonce(챌린지) 생성 후 전송
3. 클라이언트가 개인키(`AUTH_KEY_FILE`)로 nonce에 서명
4. 서버가 등록된 공개키로 서명 검증
5. 검증 성공 시 세션 개시

## 주요 설정 항목

| 설정 항목 | 역할 | 위치 |
|-----------|------|------|
| `AUTH_MODE` | 인증 방식 선택 (`PASSWORD` / `CHALLENGE`) | 연결 옵션 |
| `AUTH_KEY_FILE` | 클라이언트 개인키 파일 경로 | 연결 옵션 |
| `AUTH_SIG_SCHEME` | 서명 스킴 (`ECDSA`, `RSA_PKCS1_V15`, `RSA_PSS`) | 연결 옵션 |

`AUTH_MODE`는 서버 `machbase.conf` 속성이 아니라 클라이언트 연결 옵션입니다.
인증 방식은 연결별로 선택하며, 서버 전체를 PASSWORD/CHALLENGE 모드로 전환하지 않습니다.

## 이 섹션의 구성

- [AUTH KEY challenge 인증](/dbms/security-access-control/authentication-auth-key/#authentication-auth-key-challenge) — 챌린지-응답 인증 흐름 상세 설명
- [SYS AS USER 인증 제약](/dbms/security-access-control/authentication-auth-key/#authentication-sys-user) — SYS 계정의 AUTH KEY 사용 제약
- [AUTH_MODE=CHALLENGE](/dbms/security-access-control/authentication-auth-key/#auth-mode-challenge) — CHALLENGE 전용 모드 설정
- [AUTH_KEY_FILE](/dbms/security-access-control/authentication-auth-key/#auth-key-file) — 개인키 파일 경로 설정
- [AUTH_SIG_SCHEME](/dbms/security-access-control/authentication-auth-key/#auth-sig-scheme) — 서명 알고리즘 설정
- [RSA / ECDSA / RSA_PSS 지원 범위](/dbms/security-access-control/authentication-auth-key/#support-scope-rsa-ecdsa-rsa-pss) — 알고리즘별 특성과 SDK 지원 현황
- [사용자 AUTH KEY 관리](/dbms/security-access-control/authentication-auth-key/#user-auth-key) — AUTH KEY 등록·수정·삭제 SQL


<a id="user-auth-key"></a>

## 사용자 AUTH KEY 관리

### 개요

사용자 계정에 공개키를 등록하고, 키의 상태와 유효 기간을 관리하는 SQL 구문을 다룹니다. 한 사용자가 여러 AUTH KEY를 보유할 수 있으므로, 롤오버(교체) 기간에 이전 키와 신규 키를 동시에 활성화하여 무중단 교체가 가능합니다.

### 이 섹션의 구성

- [CREATE USER ... WITH AUTH KEY](/dbms/security-access-control/authentication-auth-key/#create-user-auth-key) — 사용자 생성 시 공개키 함께 등록
- [ALTER USER ... ADD AUTH KEY](/dbms/security-access-control/authentication-auth-key/#alter-user-add-auth-key) — 기존 사용자에 공개키 추가
- [AUTH KEY 활성화/비활성화](/dbms/security-access-control/authentication-auth-key/#enable-disable-auth-key) — 키 단위로 인증 허용 제어
- [AUTH KEY 만료 변경](/dbms/security-access-control/authentication-auth-key/#alter-expiration-auth-key) — 키 유효 기간(`valid_before`) 수정
- [AUTH KEY 삭제](/dbms/security-access-control/authentication-auth-key/#delete-auth-key) — 등록된 공개키 영구 삭제

### AUTH KEY 메타 조회

등록된 AUTH KEY는 `V$USER_AUTH_KEYS`에서 조회할 수 있습니다.

주요 컬럼:

| 컬럼 | 설명 |
|------|------|
| `KEY_ID` | AUTH KEY 식별자 |
| `USER_NAME` | AUTH KEY 소유 사용자 |
| `KEY_ALGO` | 키 알고리즘 (`RSA`, `ECDSA`) |
| `KEY_PARAM` | 키 파라미터 (RSA: 비트 수 예) `2048`, EC: 곡선 이름 예) `P-256`) |
| `ACTIVATED` | 활성화 여부 (`1`: 활성, `0`: 비활성) |
| `VALID_AFTER` | 유효 시작 시각 |
| `VALID_BEFORE` | 유효 만료 시각 |
| `COMMENT` | 사용자 메모 |
| `PUBKEY` | PEM 형식 공개키 본문 |

```sql
-- 특정 사용자의 AUTH KEY 목록 조회
SELECT key_id, user_name, key_algo, key_param, activated, valid_before, comment
  FROM V$USER_AUTH_KEYS
 WHERE user_name = 'APP_USER'
 ORDER BY key_id;

-- 공개키 본문까지 조회
SELECT key_id, user_name, pubkey
  FROM V$USER_AUTH_KEYS
 WHERE user_name = 'APP_USER'
 ORDER BY key_id;
```

### 키 롤오버 절차

운영 중 키를 교체할 때는 무중단 롤오버 절차를 사용합니다.

1. 신규 키 쌍 생성
2. 기존 사용자에 신규 공개키 추가 (`ALTER USER ... ADD AUTH KEY`)
3. 클라이언트가 신규 개인키로 접속 전환 확인
4. 이전 키 비활성화 (`ALTER USER ... DEACTIVATE AUTH KEY ID <id>`)
5. 이전 키 삭제 (`ALTER USER ... DROP AUTH KEY ID <id>`)

<a id="create-user-auth-key"></a>
<a id="user-auth-key-create-user-auth-key"></a>

### CREATE USER ... WITH AUTH KEY

사용자를 생성하면서 공개키를 함께 등록합니다. 첫 번째 AUTH KEY는 즉시 활성 상태(`ACTIVATED=1`)로 설정됩니다.

#### 키 쌍 생성

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

#### 공개키 변환

SQL 문자열에 넣기 위해 공개키 PEM 파일의 줄바꿈을 `\n`으로 이스케이프합니다.

```bash
awk '{printf "%s\\n", $0}' app_user_ecdsa.pub
```

출력 예:

```
-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEshxcrSmtosaqWjhRkOoAw4v3QWqL\ns3OFN2jbJrustEc12uAn/IdtTG94KK69bY7DWl80pzQ48dNL+ENXe8PT3g==\n-----END PUBLIC KEY-----\n
```

#### 등록 SQL 파일 자동 생성

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

#### 구문

```sql
CREATE USER app_user IDENTIFIED BY 'App#1234'
WITH AUTH KEY (
    key='-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEshxcrSmtosaqWjhRkOoAw4v3QWqL\ns3OFN2jbJrustEc12uAn/IdtTG94KK69bY7DWl80pzQ48dNL+ENXe8PT3g==\n-----END PUBLIC KEY-----\n',
    valid_before='2047-12-31',
    comment='initial ecdsa p256 key'
);
```

#### AUTH KEY 절 파라미터

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

#### 등록 확인

```sql
SELECT key_id, user_name, key_algo, key_param, activated, valid_before, comment
  FROM V$USER_AUTH_KEYS
 WHERE user_name = 'APP_USER'
 ORDER BY key_id;
```

<a id="alter-user-add-auth-key"></a>
<a id="user-auth-key-alter-user-add-auth-key"></a>

### ALTER USER ... ADD AUTH KEY

기존 사용자에게 공개키를 추가합니다. 추가된 AUTH KEY는 즉시 활성 상태(`ACTIVATED=1`)로 등록됩니다. 비밀번호 인증만 사용하던 사용자에게 AUTH KEY를 추가하면, 이후 클라이언트의 `AUTH_MODE` 설정에 따라 비밀번호 또는 AUTH KEY 중 하나로 인증할 수 있습니다.

#### 구문

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

#### AUTH KEY 절 파라미터

| 파라미터 | 필수 여부 | 설명 |
|---------|---------|------|
| `key` | 필수 | PEM 형식 공개키 문자열 (줄바꿈을 `\n`으로 이스케이프) |
| `valid_before` | 필수 | 키 만료일 (`YYYY-MM-DD` 형식) |
| `comment` | 필수 | 키 식별 메모 |

`key`, `valid_before`, `comment`는 현재 AUTH KEY 구문에서 모두 필수입니다.
`valid_before`는 생략하거나 NULL/무제한으로 둘 수 없습니다.

#### 공개키 변환 및 SQL 파일 생성

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

#### 키 롤오버에서의 활용

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

#### 등록 확인

```sql
SELECT key_id, user_name, key_algo, key_param, activated, valid_before, comment
  FROM V$USER_AUTH_KEYS
 WHERE user_name = 'APP_USER'
 ORDER BY key_id;
```

<a id="enable-disable-auth-key"></a>
<a id="user-auth-key-enable-disable-auth-key"></a>

### AUTH KEY 활성화/비활성화

등록된 AUTH KEY를 삭제하지 않고 임시로 비활성화하거나 다시 활성화할 수 있습니다. 비활성화된 키는 챌린지 인증에 사용할 수 없습니다.

#### 구문

```sql
-- AUTH KEY 비활성화
ALTER USER app_user DEACTIVATE AUTH KEY ID <key_id>;

-- AUTH KEY 활성화
ALTER USER app_user ACTIVATE AUTH KEY ID <key_id>;
```

#### 예제

```sql
-- key_id 3번 키 비활성화
ALTER USER app_user DEACTIVATE AUTH KEY ID 3;

-- key_id 3번 키 다시 활성화
ALTER USER app_user ACTIVATE AUTH KEY ID 3;
```

#### 활용 사례

**키 롤오버 중 이전 키 차단**

신규 키로 클라이언트 전환이 완료된 후 이전 키를 비활성화합니다. 이전 키를 바로 삭제하지 않고 비활성화 상태로 잠시 보관하면, 문제 발생 시 빠르게 복구할 수 있습니다.

```sql
-- 이전 키(key_id=1) 비활성화
ALTER USER app_user DEACTIVATE AUTH KEY ID 1;

-- 충분한 검증 기간 후 삭제
ALTER USER app_user DROP AUTH KEY ID 1;
```

**보안 이슈 발생 시 즉각 차단**

특정 클라이언트 호스트에서 이상 접속이 감지된 경우, 해당 호스트의 키를 즉시 비활성화하여 접속을 차단합니다.

```sql
ALTER USER app_user DEACTIVATE AUTH KEY ID 2;
```

**유지보수 기간 중 임시 차단**

클라이언트 점검이나 유지보수 중 해당 계정의 AUTH KEY 인증을 임시로 차단합니다.

```sql
-- 유지보수 시작 시 비활성화
ALTER USER app_user DEACTIVATE AUTH KEY ID 1;

-- 유지보수 완료 후 재활성화
ALTER USER app_user ACTIVATE AUTH KEY ID 1;
```

#### 활성화 상태 확인

```sql
SELECT key_id, user_name, key_algo, activated, valid_before, comment
  FROM V$USER_AUTH_KEYS
 WHERE user_name = 'APP_USER'
 ORDER BY key_id;
```

`ACTIVATED` 컬럼 값:
- `1`: 활성 상태 — 챌린지 인증에 사용 가능
- `0`: 비활성 상태 — 챌린지 인증에 사용 불가

#### 주의 사항

- 한 사용자의 모든 AUTH KEY가 비활성화되면 해당 사용자는 AUTH KEY 인증을 사용할 수 없습니다. `AUTH_MODE=PASSWORD`로 접속하거나, SYS 계정에서 키를 재활성화해야 합니다.
- 비활성화와 달리 삭제(`DROP AUTH KEY`)는 복구할 수 없습니다. 일시적 차단에는 비활성화를 사용하십시오.

<a id="alter-expiration-auth-key"></a>
<a id="user-auth-key-alter-expiration-auth-key"></a>

### AUTH KEY 만료 변경

등록된 AUTH KEY의 유효 기간(`valid_before`)을 변경합니다. 만료일이 지난 키는 인증에 사용할 수 없으며 오류가 반환됩니다.

#### 구문

```sql
-- AUTH KEY 유효 기간 변경
ALTER USER app_user ALTER AUTH KEY ID <key_id> VALID_BEFORE='YYYY-MM-DD';
```

#### 예제

```sql
-- key_id 3번 키의 만료일을 2048-06-30으로 변경
ALTER USER app_user ALTER AUTH KEY ID 3 VALID_BEFORE='2048-06-30';

-- key_id 2번 키의 만료일을 연장
ALTER USER app_user ALTER AUTH KEY ID 2 VALID_BEFORE='2049-12-31';
```

#### 주의 사항

- `VALID_BEFORE` 형식은 `YYYY-MM-DD`만 허용합니다. 시각이 포함된 `YYYY-MM-DD HH24:MI:SS` 형식은 허용되지 않습니다.
- 이미 만료된 키의 만료일을 미래 날짜로 연장하면 해당 키는 즉시 다시 사용 가능해집니다. 단, 키가 비활성화 상태(`ACTIVATED=0`)이면 만료일 연장만으로는 인증에 사용할 수 없습니다.
- 만료일이 없는(무제한) 키로 변경하는 것은 지원되지 않습니다. 키를 삭제하고 재등록해도
  `valid_before`는 필수입니다.

#### key_id 확인 방법

```sql
SELECT key_id, user_name, key_algo, activated, valid_before, comment
  FROM V$USER_AUTH_KEYS
 WHERE user_name = 'APP_USER'
 ORDER BY key_id;
```

#### 만료 KEY 처리 절차

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

<a id="delete-auth-key"></a>
<a id="user-auth-key-delete-auth-key"></a>

### AUTH KEY 삭제

`ALTER USER ... DROP AUTH KEY` 구문으로 등록된 AUTH KEY를 영구 삭제합니다. 삭제 즉시 해당 키로는 인증할 수 없으며, 복구도 불가합니다.

#### 구문

```sql
ALTER USER app_user DROP AUTH KEY ID <key_id>;
```

#### 예제

```sql
-- key_id 3번 키 삭제
ALTER USER app_user DROP AUTH KEY ID 3;

-- 삭제 전 대상 키 확인
SELECT key_id, user_name, key_algo, activated, valid_before, comment
  FROM V$USER_AUTH_KEYS
 WHERE user_name = 'APP_USER'
 ORDER BY key_id;
```

#### key_id 확인

삭제할 KEY의 `key_id`는 `V$USER_AUTH_KEYS`에서 조회합니다.

```sql
SELECT key_id, key_algo, key_param, activated, valid_before, comment
  FROM V$USER_AUTH_KEYS
 WHERE user_name = 'APP_USER'
 ORDER BY key_id;
```

#### AUTH KEY 삭제 후 인증 방식

AUTH KEY를 삭제하면 해당 사용자의 남은 AUTH KEY 현황에 따라 인증 가능 여부가 결정됩니다.

| 삭제 후 상황 | 가능한 인증 방식 |
|------------|----------------|
| 다른 활성 AUTH KEY가 남아 있음 | AUTH KEY 인증 계속 가능 |
| 모든 AUTH KEY가 삭제됨 | 비밀번호 인증만 가능 |
| 모든 AUTH KEY가 삭제되고 비밀번호 없음 | 접속 불가 |

#### 사용자 삭제 시 연동

`DROP USER` 실행 시 해당 사용자의 모든 AUTH KEY 메타가 함께 정리됩니다. 별도로 AUTH KEY를 먼저 삭제할 필요가 없습니다.

```sql
-- 사용자 삭제 시 AUTH KEY 메타도 자동 정리
DROP USER app_user;
```

#### 삭제 전 권장 절차

영구 삭제 전에 먼저 비활성화하고 일정 기간 후 삭제하는 절차를 권장합니다.

```sql
-- 1단계: 비활성화 (접속 차단, 복구 가능)
ALTER USER app_user DEACTIVATE AUTH KEY ID 3;

-- 2단계: 충분한 검증 기간 후 영구 삭제
ALTER USER app_user DROP AUTH KEY ID 3;

-- 3단계: 삭제 확인
SELECT key_id, user_name, key_algo, activated, valid_before, comment
  FROM V$USER_AUTH_KEYS
 WHERE user_name = 'APP_USER'
 ORDER BY key_id;
```

<a id="authentication-auth-key-challenge"></a>

## AUTH KEY challenge 인증

공개키 암호화를 기반으로 한 챌린지-응답 인증 방식입니다. 비밀번호를 네트워크로 전송하지 않고, 서버가 보낸 일회성 nonce에 클라이언트가 개인키로 서명하여 신원을 증명합니다.

### 인증 흐름

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

### 보안 특성

- **비밀번호 미전송**: 인증 과정에서 비밀번호가 네트워크를 경유하지 않습니다.
- **일회성 챌린지**: nonce는 매 접속마다 새로 생성되므로 재전송 공격이 불가능합니다.
- **개인키 보호**: 개인키는 클라이언트 호스트에만 존재하며 네트워크로 전송되지 않습니다.
- **서버 측 공개키**: 서버에는 공개키만 저장하므로 서버가 침해되어도 개인키는 노출되지 않습니다.

### 사전 준비 순서

#### 1단계: 키 쌍 생성

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

#### 2단계: 공개키를 SQL에 넣을 형식으로 변환

공개키 PEM 파일의 줄바꿈을 `\n`으로 이스케이프하여 한 줄 문자열로 변환합니다.

```bash
awk '{printf "%s\\n", $0}' app_user_ecdsa.pub
```

#### 3단계: 사용자 생성 또는 기존 사용자에 AUTH KEY 추가

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

#### 4단계: 클라이언트 접속 설정

클라이언트 접속 시 다음 옵션을 지정합니다.

| 옵션 | 값 | 설명 |
|------|----|------|
| `AUTH_MODE` | `CHALLENGE` | 챌린지 인증 방식 선택 |
| `AUTH_KEY_FILE` | `/path/to/app_user_ecdsa.key` | 개인키 파일 경로 |
| `AUTH_SIG_SCHEME` | `ECDSA` (ECDSA 키 시 생략 가능) | 서명 스킴 |

### 인증 실패 조건

다음 경우 AUTH KEY 인증이 실패합니다.

- 등록된 공개키가 없거나 모두 비활성화 상태인 경우
- 공개키 타입과 `AUTH_SIG_SCHEME` 설정이 일치하지 않는 경우
- `valid_before` 만료된 키만 존재하는 경우
- 개인키 파일이 없거나 읽을 수 없는 경우

AUTH KEY 인증 실패 시 비밀번호 인증으로 자동 전환되지 않습니다. 필요하면 `AUTH_MODE=PASSWORD`로 명시하여 별도 접속해야 합니다.

<a id="authentication-sys-user"></a>

## SYS AS USER 인증 제약

SYS는 관리자 계정입니다. AUTH KEY 인증과 관련하여 다음 사항에 유의하십시오.

### SYS 계정 인증 특성

- `AUTH_MODE=CHALLENGE`는 서버 전역 설정이 아니라 클라이언트 연결 옵션입니다.
- SYS 계정으로 CHALLENGE 인증을 사용하려면 SYS 계정에도 AUTH KEY를 등록해야 합니다.
- SYS 계정에 AUTH KEY가 없으면 PASSWORD 방식 연결을 사용합니다.

### SYS 계정 AUTH KEY 등록

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

### 운영 환경 권장 사항

SYS 계정을 일상적인 애플리케이션 접속에 직접 사용하지 마십시오. 각 애플리케이션별로 전용 계정을 생성해 최소 권한만 부여하고, SYS는 관리 작업 전용으로 유지합니다. SYS 비밀번호는 정기적으로 변경하십시오.

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

### SYS 계정 CHALLENGE 인증 사용

SYS 계정으로 CHALLENGE 인증을 사용해야 한다면 먼저 SYS 계정에 AUTH KEY를 등록하고,
클라이언트 연결 옵션에 `AUTH_MODE=CHALLENGE`, `AUTH_KEY_FILE`,
`AUTH_SIG_SCHEME`을 지정합니다.

<a id="auth-mode-challenge"></a>

## AUTH_MODE=CHALLENGE

`AUTH_MODE`는 클라이언트 접속 시 인증 방식을 지정하는 연결 옵션입니다. 서버 `machbase.conf`의 전역 속성이 아닙니다.

| 값 | 설명 |
|----|------|
| `PASSWORD` | 비밀번호 인증 (기본값) |
| `CHALLENGE` | 해당 연결에서 AUTH KEY 챌린지-응답 인증 사용 |

### CHALLENGE 모드 설정

개별 연결에서 인증 방식을 지정합니다.

JDBC 연결 문자열 예:

```
jdbc:machbase://localhost:5656/machbasedb?AUTH_MODE=CHALLENGE&AUTH_KEY_FILE=/home/app/.ssh/app_user.key
```

### CHALLENGE 모드 주의 사항

CHALLENGE 연결을 사용하기 전 다음 사항을 확인하십시오.

**전환 전 체크리스트**

- [ ] 모든 접속 계정(SYS 포함 여부 확인)에 AUTH KEY가 등록되어 있는가
- [ ] 등록된 AUTH KEY가 활성화 상태(`ACTIVATED=1`)인가
- [ ] AUTH KEY의 만료일(`valid_before`)이 유효한가
- [ ] 클라이언트 측 개인키 파일이 올바른 경로에 존재하는가
- [ ] 개인키 파일 권한이 소유자만 읽기 가능(`chmod 600`)인가

AUTH KEY가 등록되지 않은 계정으로 `AUTH_MODE=CHALLENGE` 연결을 시도하면 인증에 실패합니다.

### AUTH KEY 등록 현황 확인

사용자의 AUTH KEY 등록 현황을 확인합니다.

```sql
-- 전체 사용자와 AUTH KEY 현황
SELECT u.name AS user_name,
       k.key_id,
       k.key_algo,
       k.activated,
       k.valid_before
  FROM m$sys_users u
  LEFT JOIN v$user_auth_keys k ON u.name = k.user_name
 ORDER BY u.name, k.key_id;
```

AUTH KEY가 없는 사용자는 `key_id` 컬럼이 NULL로 표시됩니다. 이런 계정으로 CHALLENGE
인증을 사용하려면 먼저 AUTH KEY를 등록해야 합니다.

<a id="auth-key-file"></a>

## AUTH_KEY_FILE

`AUTH_KEY_FILE`은 챌린지 인증 시 클라이언트가 서명에 사용할 개인키 파일 경로를 지정합니다. 개인키는 클라이언트 호스트에만 보관하며 네트워크로 전송되지 않습니다.

### 파일 형식

개인키 파일은 PEM 형식의 암호화되지 않은 개인키입니다.

- ECDSA 키: `-----BEGIN EC PRIVATE KEY-----` 형식
- RSA 키: `-----BEGIN RSA PRIVATE KEY-----` 형식

### 키 파일 생성

#### ECDSA P-256 (권장)

```bash
openssl ecparam -name prime256v1 -genkey -noout -out ~/.machbase/app_user.key
openssl ec -in ~/.machbase/app_user.key -pubout -out ~/.machbase/app_user.pub
chmod 600 ~/.machbase/app_user.key
```

#### ECDSA P-384

```bash
openssl ecparam -name secp384r1 -genkey -noout -out ~/.machbase/app_user_p384.key
openssl ec -in ~/.machbase/app_user_p384.key -pubout -out ~/.machbase/app_user_p384.pub
chmod 600 ~/.machbase/app_user_p384.key
```

#### ECDSA P-521

```bash
openssl ecparam -name secp521r1 -genkey -noout -out ~/.machbase/app_user_p521.key
openssl ec -in ~/.machbase/app_user_p521.key -pubout -out ~/.machbase/app_user_p521.pub
chmod 600 ~/.machbase/app_user_p521.key
```

#### RSA 2048-bit

```bash
openssl genrsa -out ~/.machbase/app_user_rsa.key 2048
openssl rsa -in ~/.machbase/app_user_rsa.key -pubout -out ~/.machbase/app_user_rsa.pub
chmod 600 ~/.machbase/app_user_rsa.key
```

RSA 3072-bit, 4096-bit 키를 사용하려면 `openssl genrsa`의 마지막 인자를 각각 `3072`, `4096`으로 지정합니다.

### 파일 권한 설정

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

### 연결 옵션 지정 방법

#### JDBC

```
jdbc:machbase://localhost:5656/machbasedb?AUTH_MODE=CHALLENGE&AUTH_KEY_FILE=/home/app/.machbase/app_user.key
```

#### machsql

```bash
machsql -s 127.0.0.1 -u app_user \
  -c "AUTH_MODE=CHALLENGE" \
  -K /home/app/.machbase/app_user.key
```

C/ODBC 클라이언트도 연결 속성으로 `AUTH_MODE=CHALLENGE`와 `AUTH_KEY_FILE`을 지정합니다.

### 주의 사항

- `AUTH_KEY_FILE` 경로에 지정된 파일이 존재하지 않거나 읽기 권한이 없으면 인증이 실패합니다.
- 개인키 파일은 정기적으로 갱신하고, 유출 시 즉시 서버 측 공개키를 교체합니다. ([AUTH KEY 삭제](/dbms/security-access-control/authentication-auth-key/#user-auth-key-delete-auth-key) 및 [AUTH KEY 추가](/dbms/security-access-control/authentication-auth-key/#user-auth-key-alter-user-add-auth-key) 참고)
- `AUTH_KEY_FILE`을 지정하지 않으면 `AUTH_MODE=CHALLENGE`로 설정해도 서명을 생성할 수 없어 인증이 실패합니다.

<a id="auth-sig-scheme"></a>

## AUTH_SIG_SCHEME

`AUTH_SIG_SCHEME`은 챌린지 인증 시 nonce 서명에 사용할 스킴을 지정합니다. 지원 값은 다음과 같습니다.

| 값 | 설명 |
|----|------|
| `ECDSA` | ECDSA 서명 방식 (ECDSA 키 사용 시 기본값) |
| `RSA_PKCS1_V15` | RSA PKCS#1 v1.5 서명 방식 (RSA 키 사용 시 기본값) |
| `RSA_PSS` | RSA-PSS 서명 방식 |

### 기본값 동작

`AUTH_SIG_SCHEME`을 생략하면 키 알고리즘에 따라 자동으로 기본 스킴이 선택됩니다.

- ECDSA 키 파일 사용 시: `ECDSA`
- RSA 키 파일 사용 시: `RSA_PKCS1_V15`

RSA-PSS를 사용하려면 반드시 `AUTH_SIG_SCHEME=RSA_PSS`를 명시해야 합니다.

### 지원 키 파라미터와 서명 스킴 매핑

| 키 알고리즘 | 지원 키 파라미터 | 지원 서명 스킴 | 해시 |
|------------|----------------|--------------|------|
| ECDSA | P-256, P-384, P-521 | `ECDSA` | SHA-256 |
| RSA | 2048, 3072, 4096 bits | `RSA_PKCS1_V15` | SHA-256 |
| RSA | 2048, 3072, 4096 bits | `RSA_PSS` | SHA-256 |

### 설정 방법

#### JDBC

```
jdbc:machbase://localhost:5656/machbasedb?AUTH_MODE=CHALLENGE&AUTH_KEY_FILE=/home/app/.machbase/app_user.key&AUTH_SIG_SCHEME=RSA_PSS
```

#### machsql

```bash
machsql -s 127.0.0.1 -u app_user \
  -c "AUTH_MODE=CHALLENGE" \
  -K /home/app/.machbase/app_user_rsa.key \
  --auth-sig-scheme=RSA_PSS
```

### 주의 사항

- 등록된 공개키 타입과 클라이언트의 `AUTH_SIG_SCHEME`이 일치하지 않으면 인증이 실패합니다.
  예: ECDSA 공개키를 등록하고 `AUTH_SIG_SCHEME=RSA_PKCS1_V15`로 접속하면 실패합니다.
- RSA 키로 `AUTH_SIG_SCHEME=RSA_PSS`를 사용하는 경우와 `RSA_PKCS1_V15`를 사용하는 경우는 동일한 RSA 공개키를 공유할 수 있습니다. 서명 스킴만 다를 뿐 키 자체는 같습니다.
- 알고리즘 선택 권장 사항은 [RSA / ECDSA / RSA_PSS 지원 범위](/dbms/security-access-control/authentication-auth-key/#support-scope-rsa-ecdsa-rsa-pss) 페이지를 참고하십시오.

<a id="support-scope-rsa-ecdsa-rsa-pss"></a>

## RSA / ECDSA / RSA_PSS 지원 범위

### 알고리즘 특성 비교

| 항목 | ECDSA | RSA_PKCS1_V15 | RSA_PSS |
|------|-------|--------------|---------|
| 키 알고리즘 | ECDSA | RSA | RSA |
| 지원 키 파라미터 | P-256, P-384, P-521 | 2048, 3072, 4096 bit | 2048, 3072, 4096 bit |
| 서명 스킴 문자열 | `ECDSA` | `RSA_PKCS1_V15` | `RSA_PSS` |
| 해시 알고리즘 | SHA-256 | SHA-256 | SHA-256 |
| 키 크기 대비 보안성 | 높음 | 보통 | 보통 |
| 서명 크기 | 작음 | 중간 | 중간 |
| 성능 | 빠름 | 보통 | 보통 |
| 표준 권고 | NIST 권장 | 레거시 호환 | PKCS#1 v1.5 대체 권고 |

#### ECDSA

타원곡선 암호화 기반 서명 방식입니다. RSA보다 짧은 키로 동등한 보안 수준을 제공합니다.

- P-256: 128-bit 보안 수준. 성능과 보안의 균형이 좋아 일반 용도에 적합합니다.
- P-384: 192-bit 보안 수준. 고보안 요구 환경에 적합합니다.
- P-521: 260-bit 보안 수준. 최고 보안 수준이 필요한 경우 사용합니다.

#### RSA_PKCS1_V15

RSA PKCS#1 v1.5 패딩 방식의 서명입니다. 광범위한 레거시 호환성을 제공하지만 이론적 취약점이 알려져 있어 새로운 환경에서는 RSA_PSS 사용을 권장합니다.

#### RSA_PSS

RSA Probabilistic Signature Scheme의 약자입니다. PKCS#1 v1.5보다 향상된 보안 특성을 가지며, RSA 서명 방식 중에서는 현대적인 선택입니다. RSA 키를 사용해야 하는 환경에서 `RSA_PKCS1_V15` 대신 권장합니다.

### 확인된 클라이언트 지원 범위

| 클라이언트 | ECDSA | RSA_PKCS1_V15 | RSA_PSS |
|-----|-------|--------------|---------|
| JDBC | P-256, P-384, P-521 | 2048, 3072, 4096 | 2048, 3072, 4096 |
| C/ODBC | P-256, P-384, P-521 | 2048, 3072, 4096 | 2048, 3072, 4096 |
| machsql/CLI | P-256, P-384, P-521 | 2048, 3072, 4096 | 2048, 3072, 4096 |

Python, Go, .NET, Node.js 클라이언트는 AUTH KEY 인증을 지원하지 않습니다.

### 권장 알고리즘

신규 환경에서는 **ECDSA P-256**을 권장합니다.

- 짧은 키 크기로 높은 보안 수준 제공
- 서명 생성 및 검증 성능이 RSA보다 빠름
- NIST, IETF 등 표준 기관에서 권장하는 알고리즘

RSA 키 인프라를 이미 운영 중인 환경에서는 `RSA_PSS`를 선택합니다.

### openssl을 이용한 키 생성 명령 요약

```bash
# ECDSA P-256
openssl ecparam -name prime256v1 -genkey -noout -out key.pem
openssl ec -in key.pem -pubout -out pub.pem

# ECDSA P-384
openssl ecparam -name secp384r1 -genkey -noout -out key.pem
openssl ec -in key.pem -pubout -out pub.pem

# ECDSA P-521
openssl ecparam -name secp521r1 -genkey -noout -out key.pem
openssl ec -in key.pem -pubout -out pub.pem

# RSA 2048-bit (RSA_PKCS1_V15 또는 RSA_PSS 모두 사용 가능)
openssl genrsa -out key.pem 2048
openssl rsa -in key.pem -pubout -out pub.pem

# RSA 3072-bit
openssl genrsa -out key.pem 3072
openssl rsa -in key.pem -pubout -out pub.pem

# RSA 4096-bit
openssl genrsa -out key.pem 4096
openssl rsa -in key.pem -pubout -out pub.pem

# 생성 후 개인키 권한 설정
chmod 600 key.pem
```
