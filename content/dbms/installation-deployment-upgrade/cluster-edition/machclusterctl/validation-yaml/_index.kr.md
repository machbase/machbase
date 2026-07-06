---
type: docs
title: 'YAML 검증'
weight: 20
---

`cluster.yaml`을 실제 설치에 사용하기 전에 유효성 검사를 수행합니다. SSH 접속, 포트 충돌, 디렉터리 권한 등을 사전에 점검하여 설치 중 오류를 예방합니다.

## 검증 명령

```bash
machclusterctl validate -f cluster.yaml
```

## 검증 항목

| 항목 | 설명 |
|------|------|
| YAML 문법 | 파일 파싱 오류 여부 |
| SSH 접속 | 각 노드에 비밀번호 없이 접속 가능한지 |
| 포트 사용 여부 | 지정한 포트가 이미 사용 중인지 |
| 홈 디렉터리 | 경로가 존재하거나 생성 가능한지, 쓰기 권한이 있는지 |
| 패키지 파일 | 지정한 패키지 파일이 존재하는지 |

## 출력 예시

```
[OK] YAML syntax check
[OK] SSH: machbase@192.168.1.10
[OK] SSH: machbase@192.168.1.11
[WARN] Port 5656 already in use on 192.168.1.11 — check if Machbase is already running
[OK] Package: /home/machbase/packages/machbase-cluster-8.6.0.official-LINUX-X86-64-release.tgz
Validation completed: 1 warning(s), 0 error(s)
```

경고(WARN)는 계속 진행할 수 있지만, 오류(ERROR)가 있으면 수정 후 재검증해야 합니다.

## 일반적인 오류와 해결

| 오류 | 원인 | 해결 |
|------|------|------|
| `Permission denied (publickey)` | SSH 키 미등록 | `ssh-copy-id`로 키 등록 |
| `Port already in use` | 포트 충돌 | 실행 중인 프로세스 종료 또는 포트 변경 |
| `No such file or directory` | 패키지 파일 경로 오류 | 경로 수정 |
| `mkdir: Permission denied` | 홈 디렉터리 권한 없음 | 해당 노드에서 디렉터리 미리 생성 |

---

**다음 읽을 내용**
- [최초 설치](/dbms/installation-deployment-upgrade/cluster-edition/machclusterctl/initial/)
