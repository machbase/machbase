---
type: docs
title: '14.2 계정 관리'
weight: 20
---

Machbase에서 데이터베이스에 접근하는 모든 주체는 사용자 계정으로 식별됩니다. 계정 관리는 사용자를 생성하고 삭제하는 기본 작업부터, 비밀번호 정책으로 계정 보안 수준을 강화하는 것까지 포함합니다.

## 이 섹션의 구성

| 항목 | 설명 |
|------|------|
| [사용자 생성과 삭제](./create-delete-user/) | CREATE USER, DROP USER, ALTER USER, 사용자 목록 조회 |
| [비밀번호 정책](./policy-password/) | NONE/LOW/HIGH 정책, 비밀번호 만료, 정책 변경 방법 |

## 계정 관리 핵심 사항

- 사용자명은 대문자로 저장됩니다. `CREATE USER app_user ...`로 생성하면 메타 테이블에는 `APP_USER`로 기록됩니다.
- `SYS` 계정은 삭제할 수 없습니다.
- 테이블을 보유한 사용자는 해당 테이블을 먼저 삭제해야 계정을 삭제할 수 있습니다.
- Machbase 8.5부터 비밀번호 정책(NONE/LOW/HIGH)을 계정별로 지정할 수 있습니다.
- AUTH KEY(공개키 기반 인증) 등록은 [AUTH KEY 인증](../authentication-auth-key/) 섹션을 참고하세요.
