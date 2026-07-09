---
type: docs
title: '14.4.1 사용자 AUTH KEY 관리'
weight: 10
---

## 개요

사용자 AUTH KEY 관리는 Machbase 사용자 계정에 공개키를 등록하고, 키의 상태와 유효 기간을 관리하는 SQL 구문들을 다룹니다.

한 사용자는 여러 AUTH KEY를 보유할 수 있습니다. 이를 활용하면 키 롤오버(교체) 기간 동안 이전 키와 신규 키를 동시에 활성화하여 무중단으로 키를 교체할 수 있습니다.

## 이 섹션의 구성

- [CREATE USER ... WITH AUTH KEY](create-user-auth-key/) — 사용자 생성 시 공개키 함께 등록
- [ALTER USER ... ADD AUTH KEY](alter-user-add-auth-key/) — 기존 사용자에 공개키 추가
- [AUTH KEY 활성화/비활성화](enable-disable-auth-key/) — 키 단위로 인증 허용 제어
- [AUTH KEY 만료 변경](alter-expiration-auth-key/) — 키 유효 기간(`valid_before`) 수정
- [AUTH KEY 삭제](delete-auth-key/) — 등록된 공개키 영구 삭제

## AUTH KEY 메타 조회

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

## 키 롤오버 절차

운영 중 키를 교체할 때는 무중단 롤오버 절차를 사용합니다.

1. 신규 키 쌍 생성
2. 기존 사용자에 신규 공개키 추가 (`ALTER USER ... ADD AUTH KEY`)
3. 클라이언트가 신규 개인키로 접속 전환 확인
4. 이전 키 비활성화 (`ALTER USER ... DEACTIVATE AUTH KEY ID <id>`)
5. 이전 키 삭제 (`ALTER USER ... DROP AUTH KEY ID <id>`)
