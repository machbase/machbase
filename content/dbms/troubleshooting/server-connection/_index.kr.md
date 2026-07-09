---
type: docs
title: '16.2 서버와 연결 문제'
weight: 20
---

서버 프로세스 시작 실패, 네트워크 접속 불가, 인증 오류 등 서버와의 연결에 관련된 문제를 다룹니다.

## 이 섹션의 구성

| 페이지 | 증상 |
|--------|------|
| [서버가 시작되지 않을 때](./start-server/) | `machadmin -u` 실행 후 서버가 뜨지 않음, 포트 충돌, 라이선스 오류, 디스크 공간 부족 |
| [연결할 수 없을 때](./connection/) | 서버는 실행 중이나 클라이언트에서 Connection refused, 원격 접속 불가, 최대 연결 수 초과 |
| [인증이 실패할 때](./failure-authentication/) | 비밀번호 오류, AUTH KEY 인증 실패, 계정 잠금 |

## 빠른 확인

```bash
# 서버 프로세스 상태
machadmin -e

# 서버가 사용하는 포트 확인 (기본: 5656)
netstat -tlnp | grep 5656
```

```sql
-- 현재 접속된 세션 수
SELECT COUNT(*) FROM v$session;
```
