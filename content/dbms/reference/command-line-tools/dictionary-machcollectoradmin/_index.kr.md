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
| `-d`, `--destroy` | Collector 메타데이터 삭제 |
| `--status-collector=collector_name` | 지정 collector 상태 확인. `all`, `run`, `stop`, `error` 지정 가능 |
| `--status[=collector_name]` | `--status-collector` alias |
| `--status-send-fail=collector_name` | 전송 실패 목록 확인. `all` 지정 가능 |
| `--list` | collector 목록 출력 |
| `--create-collector=collector_name` | collector 생성. `--template` 필요 |
| `--drop-collector=collector_name` | collector 삭제 |
| `--start-collector=collector_name` | collector 시작. `all` 지정 가능 |
| `--stop-collector=collector_name` | collector 중지. `all` 지정 가능 |
| `--kill-collector=collector_name` | collector 강제 종료. `all` 지정 가능 |
| `-m`, `--template=template_path` | collector 생성 시 템플릿 파일 경로 지정 |
| `-t`, `--trace=0~7` | collector 시작 시 trace 옵션 지정 |
| `-i`, `--silent` | 배너 출력 없이 실행 |

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
machcollectoradmin --status
machcollectoradmin --list
```

`--status`는 `--status-collector`의 alias이며, collector 이름 또는 `all`, `run`, `stop`, `error` 필터를 지정해 collector 상태를 출력합니다.

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
machcollectoradmin --status

# 템플릿으로 collector 생성 후 시작
machcollectoradmin --create-collector sensor_file --template /opt/machbase/collector/sensor.tpl
machcollectoradmin --start-collector sensor_file

# 정상 종료
machcollectoradmin -s
```
