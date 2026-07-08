---
type: docs
title: 'machcollectoradmin 명령/옵션 사전'
weight: 60
---

`machcollectoradmin`은 Machbase Collector 프로세스를 관리하는 도구입니다. Collector는 외부 데이터 소스에서 Machbase로 데이터를 수집하는 역할을 합니다.

## 옵션 목록

```bash
machcollectoradmin -h
```

| 옵션 | 설명 |
|------|------|
| `-u`, `--startup` | Collector 프로세스 시작 |
| `-s`, `--shutdown` | Collector 프로세스 정상 종료 |
| `-k`, `--kill` | Collector 프로세스 강제 중지 |
| `-e`, `--check` | Collector 프로세스 실행 여부 확인 |
| `-i`, `--silent` | 배너 출력 없이 실행 |
| `--home-path=path` | Machbase Collector 홈 경로 지정 |

## 프로세스 관리

### 시작

```bash
machcollectoradmin -u
```

### 정상 종료

```bash
machcollectoradmin -s
```

### 강제 중지

```bash
machcollectoradmin -k
```

### 실행 상태 확인

```bash
machcollectoradmin -e
```

실행 중이면 PID를 출력합니다.

```
Machbase Collector is running with pid(12345)!
```

실행 중이 아니면 오류를 출력합니다.

```
[ERR] Machbase Collector is not running.
```

## 환경 변수

| 환경 변수 | 설명 |
|----------|------|
| `MACHBASE_COLLECTOR_HOME` | Collector 홈 디렉토리 경로 |

## 설정 파일

Collector의 동작은 `$MACHBASE_COLLECTOR_HOME/conf/` 디렉토리의 설정 파일로 제어합니다. 소스 플러그인 설정에 따라 수집 대상과 방식이 결정됩니다.

설정 파일에 대한 자세한 내용은 [Collector 레퍼런스](../../collector/)를 참고하세요.

## 사용 예시

```bash
# Collector 시작
machcollectoradmin -u

# 상태 확인
machcollectoradmin -e

# 정상 종료
machcollectoradmin -s

# 홈 경로를 직접 지정하여 시작
machcollectoradmin -u --home-path=/opt/machbase/collector
```
