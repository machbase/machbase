---
type: docs
title: 'Collector 장애 복구'
weight: 40
---

Collector가 ERROR 상태이거나 수집이 중단된 경우 다음 절차에 따라 복구합니다.

## 수집 중단의 주요 원인

| 원인 | 증상 | 확인 방법 |
|------|------|-----------|
| 네트워크 단절 | ERROR 상태, 연결 오류 로그 | 네트워크 연결 및 방화벽 확인 |
| Machbase 서버 재시작 | ERROR 상태, DB 연결 실패 로그 | `machadmin -e` |
| 데이터 소스 중단 | RUNNING이나 수집 행 수 미증가 | 소스 서버·파일 경로 확인 |
| 설정 파일 오류 | STARTING에서 ERROR로 전환 | 설정 XML 문법·경로 확인 |
| 디스크 공간 부족 | ERROR 상태, 디스크 쓰기 실패 로그 | `df -h` |
| 권한 오류 | ERROR 상태, 권한 오류 로그 | 파일·디렉터리 권한 확인 |

## 기본 복구 절차

```bash
# 1. 현재 상태 확인
machcollectoradmin --list
machcollectoradmin --status=my_collector

# 2. 오류 로그 확인
tail -100 $MACHBASE_COLLECTOR_HOME/trc/machcollector.trc

# 3. 원인 제거 (네트워크 복구, 소스 서버 재시작 등)

# 4. Machbase 서버 실행 여부 확인
machadmin -e

# 5. Collector 재시작
machcollectoradmin --stop-collector=my_collector
machcollectoradmin --start-collector=my_collector

# 6. 상태 확인
machcollectoradmin --status=my_collector
```

## Machbase 재시작 후 복구

Machbase 서버가 재시작되면 Collector가 연결을 잃고 ERROR 상태가 될 수 있습니다. 이 경우 Machbase 서버가 완전히 기동된 후 Collector를 재시작합니다.

```bash
# Machbase 서버 기동 확인
machadmin -e

# 모든 Collector 재시작
machcollectoradmin --list | awk 'NR>2 {print $1}' | \
  xargs -I{} sh -c 'machcollectoradmin --stop-collector={} ; machcollectoradmin --start-collector={}'
```

## 데이터 유실 방지

Collector는 내부 버퍼를 이용해 Machbase 연결이 일시적으로 끊어지더라도 수집된 데이터를 보존합니다.

- **내부 메모리 버퍼**: 단기 연결 단절 시 데이터를 메모리에 보관하다가 재연결 후 전송합니다.
- **파일 버퍼**: 설정 파일에서 파일 기반 버퍼를 활성화하면 Collector 프로세스가 종료된 경우에도 재시작 후 미전송 데이터를 복구할 수 있습니다.

파일 버퍼 설정 예 (collector_config.xml):

```xml
<buffer>
  <type>file</type>
  <path>/data/collector_buffer/my_collector</path>
  <max-size-mb>1024</max-size-mb>
</buffer>
```

## 설정 오류로 인한 복구

설정 파일 오류인 경우 Collector를 삭제하고 수정된 설정으로 재생성합니다.

```bash
# 1. Collector 중지 및 삭제
machcollectoradmin --stop-collector=my_collector
machcollectoradmin --drop-collector=my_collector

# 2. 설정 파일 수정
vi /path/to/collector_config.xml

# 3. 새 설정으로 재생성 및 시작
machcollectoradmin --create-collector=my_collector --template=/path/to/collector_config.xml
machcollectoradmin --start-collector=my_collector
```

## Collector Manager 재시작

개별 Collector 재시작으로 해결되지 않는 경우, Collector Manager 자체를 재시작합니다.

```bash
machcollectoradmin --shutdown
machcollectoradmin --startup

# 각 Collector 수동 시작
machcollectoradmin --start-collector=my_collector
```

> Collector Manager를 재시작하면 모든 Collector 인스턴스가 중지됩니다. 재시작 후 필요한 Collector를 수동으로 시작해야 합니다.
