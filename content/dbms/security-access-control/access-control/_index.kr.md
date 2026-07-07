---
type: docs
title: '접속 제어'
weight: 50
---

접속 제어는 어떤 네트워크 경로에서, 어떤 인증 방식으로 Machbase에 연결할 수 있는지를 결정합니다. 계정 인증보다 앞선 레이어에서 동작하므로, 접속 자체를 차단하는 강력한 보안 수단입니다.

## 이 섹션의 구성

| 항목 | 설명 |
|------|------|
| [원격 접속 설정](./remote-access-configuration/) | `GRANT_REMOTE_ACCESS`로 원격 접속 허용 여부 제어 |
| [HTTP 인증 설정](./authentication-configuration-http/) | `HTTP_AUTH`로 REST API Basic Auth 활성화 |
| [BIND_IP_ADDRESS와 네트워크 노출 제어](./network-exposure-bind-ip-address/) | 리스너가 열리는 네트워크 인터페이스 지정 |

## 접속 제어 관련 주요 설정

| 설정 항목 | 기본값 | 설명 |
|-----------|--------|------|
| `GRANT_REMOTE_ACCESS` | `1` | 원격 접속 허용(1) / 차단(0) |
| `BIND_IP_ADDRESS` | `0.0.0.0` | 리스너 바인드 주소 (모든 인터페이스) |
| `HTTP_AUTH` | `0` | REST API Basic Authentication 활성화(1) / 비활성화(0) |

설정은 `machbase.conf`에서 영구적으로 변경하거나, `ALTER SYSTEM SET` 구문으로 재시작 없이 즉시 반영할 수 있습니다.

```sql
-- 원격 접속 차단
ALTER SYSTEM SET GRANT_REMOTE_ACCESS = 0;

-- REST API Basic Auth 활성화
ALTER SYSTEM SET HTTP_AUTH = 1;
```
