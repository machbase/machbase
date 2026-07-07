---
type: docs
title: 'AUTH_MODE=CHALLENGE'
weight: 40
---

## 개요

`AUTH_MODE`는 클라이언트 접속 시 사용할 인증 방식을 지정하는 설정입니다. 기본값은 `PASSWORD`(비밀번호 인증)이며, `CHALLENGE`로 설정하면 AUTH KEY 기반 챌린지-응답 인증만 허용됩니다.

| 값 | 설명 |
|----|------|
| `PASSWORD` | 비밀번호 인증 (기본값) |
| `CHALLENGE` | AUTH KEY 챌린지-응답 인증 전용, 비밀번호 인증 비활성화 |

## CHALLENGE 모드 설정

### 서버 전체 적용: machbase.conf

`machbase.conf`에서 전체 서버의 기본 인증 방식을 변경합니다.

```
AUTH_MODE = CHALLENGE
```

서버를 재시작해야 변경 사항이 적용됩니다.

### 연결별 적용: 연결 옵션

서버 설정과 무관하게 개별 연결에서 인증 방식을 지정할 수 있습니다.

JDBC 연결 문자열 예:

```
jdbc:machbase://localhost:5656/machbasedb?AUTH_MODE=CHALLENGE&AUTH_KEY_FILE=/home/app/.ssh/app_user.key
```

Python 연결 옵션 예:

```python
import machbase_neo_connector as mach

conn = mach.connect(
    host='localhost',
    port=5656,
    user='app_user',
    password='',
    auth_mode='CHALLENGE',
    auth_key_file='/home/app/.ssh/app_user.key'
)
```

## CHALLENGE 모드 주의 사항

CHALLENGE 모드로 전환하면 비밀번호 인증이 완전히 비활성화됩니다. 전환 전 다음 사항을 반드시 확인하세요.

**전환 전 체크리스트**

- [ ] 모든 접속 계정(SYS 포함 여부 확인)에 AUTH KEY가 등록되어 있는가
- [ ] 등록된 AUTH KEY가 활성화 상태(`ACTIVATED=1`)인가
- [ ] AUTH KEY의 만료일(`valid_before`)이 유효한가
- [ ] 클라이언트 측 개인키 파일이 올바른 경로에 존재하는가
- [ ] 개인키 파일 권한이 소유자만 읽기 가능(`chmod 600`)인가

AUTH KEY가 등록되지 않은 계정이 남아 있는 상태에서 `AUTH_MODE=CHALLENGE`로 전환하면 해당 계정은 접속할 수 없습니다.

## AUTH KEY 등록 현황 확인

전환 전 모든 사용자의 AUTH KEY 등록 현황을 확인합니다.

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

AUTH KEY가 없는 사용자는 `key_id` 컬럼이 NULL로 표시됩니다. 이런 계정은 CHALLENGE 모드 전환 전 AUTH KEY를 등록해야 합니다.

## 모드 복구

CHALLENGE 모드에서 AUTH KEY 관련 문제가 발생하면 서버 콘솔(직접 접속) 또는 `machbase.conf`를 수정하여 `AUTH_MODE = PASSWORD`로 복구합니다.
