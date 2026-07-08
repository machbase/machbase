---
type: docs
title: 'AUTH_MODE=CHALLENGE'
weight: 40
---

## 개요

`AUTH_MODE`는 클라이언트 접속 시 사용할 인증 방식을 지정하는 연결 옵션입니다.
서버 `machbase.conf`의 전역 속성이 아닙니다.

| 값 | 설명 |
|----|------|
| `PASSWORD` | 비밀번호 인증 (기본값) |
| `CHALLENGE` | 해당 연결에서 AUTH KEY 챌린지-응답 인증 사용 |

## CHALLENGE 모드 설정

개별 연결에서 인증 방식을 지정합니다.

JDBC 연결 문자열 예:

```
jdbc:machbase://localhost:5656/machbasedb?AUTH_MODE=CHALLENGE&AUTH_KEY_FILE=/home/app/.ssh/app_user.key
```

## CHALLENGE 모드 주의 사항

CHALLENGE 연결을 사용하기 전 다음 사항을 확인하세요.

**전환 전 체크리스트**

- [ ] 모든 접속 계정(SYS 포함 여부 확인)에 AUTH KEY가 등록되어 있는가
- [ ] 등록된 AUTH KEY가 활성화 상태(`ACTIVATED=1`)인가
- [ ] AUTH KEY의 만료일(`valid_before`)이 유효한가
- [ ] 클라이언트 측 개인키 파일이 올바른 경로에 존재하는가
- [ ] 개인키 파일 권한이 소유자만 읽기 가능(`chmod 600`)인가

AUTH KEY가 등록되지 않은 계정으로 `AUTH_MODE=CHALLENGE` 연결을 시도하면 인증에 실패합니다.

## AUTH KEY 등록 현황 확인

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
