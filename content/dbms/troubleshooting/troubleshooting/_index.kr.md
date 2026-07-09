---
type: docs
title: '16.1 문제 해결 접근법'
weight: 10
---

Machbase에서 문제가 발생했을 때 무작정 설정을 바꾸거나 서버를 재시작하기 전에 체계적인 절차를 따르면 원인을 빠르게 파악하고 재발을 방지할 수 있습니다. 아래의 5단계 접근법을 순서대로 따르십시오.

## 5단계 문제 해결 절차

**1단계: 증상 파악**
오류 메시지, 발생 시각, 영향 범위(특정 사용자/전체 서비스)를 기록합니다. 재현 가능한 문제인지 확인합니다.

**2단계: 서버 상태 확인**
서버 프로세스가 정상 실행 중인지, 연결이 가능한지 먼저 확인합니다.

```bash
machadmin -e
```

**3단계: 로그 파일 분석**
`$MACHBASE_HOME/trc/machbase.trc`에서 증상 발생 시각 전후의 오류 메시지를 확인합니다.

```bash
tail -100 $MACHBASE_HOME/trc/machbase.trc | grep -i "error\|warn"
```

**4단계: 진단 SQL 실행**
V$ 가상 테이블과 진단 명령으로 현재 서버 상태를 수집합니다.

```sql
SELECT id, login_time, user_name, user_ip, closed FROM v$session;
SELECT sess_id, id, state, record_size, query FROM v$stmt;
```

**5단계: 해당 섹션의 해결 방법 적용**
증상에 해당하는 섹션을 찾아 원인별 해결 방법을 적용합니다. 해결 후 동일 증상이 재발하지 않는지 모니터링합니다.

## 이 섹션의 구성

| 페이지 | 내용 |
|--------|------|
| [증상 확인](./symptom/) | 증상별 빠른 진단 표, 첫 번째로 실행할 명령 |
| [진단 명령어 모음](./diagnosis-commands/) | 바로 복사해서 쓸 수 있는 진단 SQL과 명령 모음 |
| [로그 확인](./log-logs/) | 주요 로그 파일 목록, 로그 레벨 설정, 오류 분석 방법 |
| [오류 코드로 원인 찾기](./cause-lookup-error-codes/) | 자주 발생하는 오류 코드 표와 해결 방법 |
