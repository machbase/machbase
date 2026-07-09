---
type: docs
title: '13.7 Collector 운영'
weight: 50
---
Collector는 외부 데이터 소스에서 Machbase로 데이터를 수집하는 컴포넌트입니다. 파일, 메시지 큐, 네트워크 스트림 등 다양한 소스에서 데이터를 읽어 Machbase 테이블에 실시간으로 적재합니다.

## Collector 아키텍처

```
[외부 데이터 소스]  →  [Collector 인스턴스]  →  [Collector Manager]  →  [Machbase]
   파일/소켓/MQ           수집·변환·버퍼링            프로세스 관리         저장
```

- **Collector Manager**: 여러 Collector 인스턴스를 관리하는 데몬 프로세스입니다. Machbase 서버와 독립된 별도 프로세스로 동작합니다.
- **Collector 인스턴스**: 각 데이터 소스별로 생성·관리됩니다. 하나의 Collector Manager 아래 여러 인스턴스를 동시에 실행할 수 있습니다.
- **machcollectoradmin**: Collector Manager와 Collector 인스턴스를 시작·중지하고 Collector를 생성·시작·중지·삭제하는 CLI 도구입니다.

## 이 섹션의 구성

| 주제 | 내용 |
|------|------|
| [Collector Manager 시작과 종료](/dbms/operations-configuration-recovery/collector/#start-collectormanager) | Collector Manager 데몬 기동·정지 절차 |
| [Collector 생성/시작/중지/삭제](/dbms/operations-configuration-recovery/collector/#create-delete-start-stop-machcollectoradmin-collector) | machcollectoradmin으로 인스턴스 관리 |
| [Collector 상태 확인](/dbms/operations-configuration-recovery/collector/#status-check-state-collector) | 목록 조회, 상태 확인, 로그 분석 |
| [Collector 장애 복구](/dbms/operations-configuration-recovery/collector/#recovery-failure-collector) | 수집 중단 원인 파악과 복구 절차 |

## 운영 시작 순서

Collector를 운영하려면 반드시 다음 순서를 따릅니다.

1. Machbase 서버 기동 (`machadmin -u`)
2. Collector Manager 기동 (`machcollectoradmin --startup`)
3. 개별 Collector 인스턴스 시작 (`machcollectoradmin --start-collector=<이름>`)

종료 시에는 역순으로 진행합니다.


<a id="start-collectormanager"></a>

## Collector Manager 시작과 종료

Collector Manager는 Collector 인스턴스를 관리하는 데몬 프로세스입니다. Machbase 서버와 독립된 별도 프로세스이므로 Machbase 서버 기동 후에 별도로 시작해야 합니다.

### 시작

```bash
machcollectoradmin --startup
```

정상적으로 시작되면 아래와 같이 출력됩니다.

```
Machbase Collector Manager started successfully.
```

Collector Manager가 실행되면 설정 파일(`$MACHBASE_COLLECTOR_HOME/conf/machcollector.conf`)에 정의된 설정을 사용합니다. `MACHBASE_COLLECTOR_HOME`을 별도로 지정하지 않은 환경에서는 `$MACHBASE_HOME`과 같은 홈을 사용할 수 있습니다.

### 상태 확인

```bash
machcollectoradmin --status-collector=all
```

Collector Manager에는 별도의 `--check` 옵션이 없습니다. 전체 Collector 상태 조회 명령으로 Collector Manager와 Collector 동작 상태를 함께 확인합니다.

### 종료

```bash
machcollectoradmin --shutdown
```

종료 시 실행 중인 모든 Collector 인스턴스가 먼저 안전하게 중지된 후 Collector Manager 프로세스가 종료됩니다.

### 시작 순서

Collector Manager는 반드시 Machbase 서버가 기동된 상태에서 시작해야 합니다. Machbase 서버가 실행되지 않은 상태에서 Collector 인스턴스를 시작하면 Machbase에 연결하지 못해 수집이 실패합니다.

```
1. machadmin -u               # Machbase 서버 시작
2. machcollectoradmin --startup                 # Collector Manager 시작
3. machcollectoradmin --start-collector=<이름>  # 개별 Collector 시작
```

### 자동 시작 설정

시스템 재부팅 시 자동으로 시작되도록 systemd 서비스로 등록하거나, 운영 환경의 init 스크립트에 Machbase 서버 기동 직후 `machcollectoradmin --startup`을 추가하는 것을 권장합니다.

### 로그

Collector Manager 자체 로그는 `$MACHBASE_COLLECTOR_HOME/trc/machcollectormanager.trc`에 저장됩니다. 관리 도구 로그는 `$MACHBASE_COLLECTOR_HOME/trc/machcollectoradmin.trc`에서 확인합니다.

```bash
tail -100 $MACHBASE_COLLECTOR_HOME/trc/machcollectormanager.trc
tail -100 $MACHBASE_COLLECTOR_HOME/trc/machcollectoradmin.trc
```

<a id="create-delete-start-stop-machcollectoradmin-collector"></a>

## machcollectoradmin으로 Collector 생성/시작/중지/삭제

`machcollectoradmin`은 Collector 인스턴스를 생성·시작·중지·삭제하는 CLI 도구입니다. Collector 이름은 각 동작 옵션의 값으로 지정합니다.

### Collector 생성

```bash
machcollectoradmin --create-collector=my_collector --template=collector_config.xml
```

| 옵션 | 설명 |
|------|------|
| `--create-collector=<이름>` | Collector 인스턴스 생성 동작 |
| `--template=<파일>` | Collector 설정 템플릿 파일 경로 |

설정 파일은 수집 소스 유형, 연결 정보, 대상 Machbase 테이블, 버퍼 크기 등을 정의합니다. 생성된 Collector 인스턴스는 STOPPED 상태로 등록됩니다.

### Collector 시작

```bash
machcollectoradmin --start-collector=my_collector
```

STOPPED 상태의 Collector를 RUNNING 상태로 전환합니다. 시작 후 설정 파일에 정의된 소스에서 데이터 수집을 시작합니다.

### Collector 중지

```bash
machcollectoradmin --stop-collector=my_collector
```

RUNNING 상태의 Collector를 안전하게 중지합니다. 현재 처리 중인 배치가 완료된 후 종료되므로, 데이터 유실 없이 중지할 수 있습니다.

### Collector 재시작

```bash
machcollectoradmin --stop-collector=my_collector
machcollectoradmin --start-collector=my_collector
```

설정 변경 적용이나 장애 복구 시 재시작이 필요합니다. machcollectoradmin에는 별도의 restart 동작이 없으므로 stop 후 start를 순서대로 실행합니다.

### Collector 삭제

```bash
machcollectoradmin --drop-collector=my_collector
```

Collector 인스턴스 등록 정보를 삭제합니다. 삭제하려면 먼저 Collector가 STOPPED 상태여야 합니다. RUNNING 상태에서 삭제를 시도하면 오류가 발생합니다.

```bash
# 실행 중인 경우 먼저 중지 후 삭제
machcollectoradmin --stop-collector=my_collector
machcollectoradmin --drop-collector=my_collector
```

### 설정 변경

Collector 설정을 변경하려면 삭제 후 새 설정으로 다시 생성하거나, 설정 파일을 수정한 뒤 재시작합니다.

```bash
# 설정 파일 수정 후 재시작
machcollectoradmin --stop-collector=my_collector
machcollectoradmin --start-collector=my_collector
```

설정 파일 경로는 생성 시 등록된 경로를 사용합니다. 경로를 변경하려면 삭제 후 새 설정 파일로 재생성해야 합니다.

<a id="status-check-state-collector"></a>

## Collector 상태 확인

Collector 상태를 정기적으로 확인하여 수집이 정상적으로 진행되고 있는지 점검합니다.

### 전체 Collector 목록 조회

```bash
machcollectoradmin --list
```

등록된 모든 Collector 인스턴스와 상태를 출력합니다.

```
Name           Status    Config File
-----------    --------  -----------------------------------
my_collector   RUNNING   /home/mach/conf/collector_a.xml
log_collector  STOPPED   /home/mach/conf/collector_b.xml
err_collector  ERROR     /home/mach/conf/collector_c.xml
```

### 특정 Collector 상태 조회

```bash
machcollectoradmin --status=my_collector
```

특정 Collector의 상세 상태를 출력합니다.

```
Name        : my_collector
Status      : RUNNING
Config File : /home/mach/conf/collector_a.xml
Collected   : 1,234,567 rows
Error Count : 0
Last Active : 2026-07-07 10:32:15
```

### Collector 상태 값

| 상태 | 의미 |
|------|------|
| `RUNNING` | 정상적으로 데이터를 수집 중 |
| `STOPPED` | 중지 상태. 시작 명령 대기 중 |
| `ERROR` | 수집 오류 발생. 로그 확인 필요 |
| `STARTING` | 시작 처리 중 (일시적 상태) |
| `STOPPING` | 종료 처리 중 (일시적 상태) |

### 로그 파일 위치

기본 Collector 로그는 `$MACHBASE_COLLECTOR_HOME/trc/machcollector.trc`에 기록됩니다. Collector별 trace 로그를 활성화한 경우에는 `$MACHBASE_COLLECTOR_HOME/trc/<collector>.trc` 파일도 생성될 수 있습니다.

```bash
# 기본 Collector 로그 확인
tail -f $MACHBASE_COLLECTOR_HOME/trc/machcollector.trc

# Collector별 trace 로그를 활성화한 경우
tail -f $MACHBASE_COLLECTOR_HOME/trc/my_collector.trc
```

### 오류 확인 방법

ERROR 상태인 Collector가 있으면 다음 순서로 원인을 파악합니다.

1. **상태 조회**: `machcollectoradmin --status=<이름>`으로 오류 개수와 마지막 활동 시간 확인
2. **로그 확인**: 기본적으로 `$MACHBASE_COLLECTOR_HOME/trc/machcollector.trc`에서 오류 메시지 확인. Collector별 trace 로그를 활성화했다면 `$MACHBASE_COLLECTOR_HOME/trc/<이름>.trc`도 함께 확인
3. **Machbase 연결 확인**: Machbase 서버가 정상 실행 중인지 `machadmin -e`로 확인
4. **소스 연결 확인**: 데이터 소스(파일 경로, 소켓 포트, MQ 서버 등)가 유효한지 확인

오류 원인을 제거한 후 [장애 복구](/dbms/operations-configuration-recovery/collector/#recovery-failure-collector) 절차에 따라 복구합니다.

### 수집 지연 감지

수집이 지연되고 있는지 확인하려면 일정 시간 간격으로 `status` 명령을 실행하여 수집 행 수가 증가하는지 확인합니다.

```bash
# 10초 간격으로 수집 상태 확인
watch -n 10 "machcollectoradmin --status=my_collector"
```

수집 행 수가 증가하지 않거나 `Last Active` 시간이 오래된 경우 수집 지연 또는 중단 상태입니다.

<a id="recovery-failure-collector"></a>

## Collector 장애 복구

Collector가 ERROR 상태이거나 수집이 중단된 경우 다음 절차에 따라 복구합니다.

### 수집 중단의 주요 원인

| 원인 | 증상 | 확인 방법 |
|------|------|-----------|
| 네트워크 단절 | ERROR 상태, 연결 오류 로그 | 네트워크 연결 및 방화벽 확인 |
| Machbase 서버 재시작 | ERROR 상태, DB 연결 실패 로그 | `machadmin -e` |
| 데이터 소스 중단 | RUNNING이나 수집 행 수 미증가 | 소스 서버·파일 경로 확인 |
| 설정 파일 오류 | STARTING에서 ERROR로 전환 | 설정 XML 문법·경로 확인 |
| 디스크 공간 부족 | ERROR 상태, 디스크 쓰기 실패 로그 | `df -h` |
| 권한 오류 | ERROR 상태, 권한 오류 로그 | 파일·디렉터리 권한 확인 |

### 기본 복구 절차

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

### Machbase 재시작 후 복구

Machbase 서버가 재시작되면 Collector가 연결을 잃고 ERROR 상태가 될 수 있습니다. 이 경우 Machbase 서버가 완전히 기동된 후 Collector를 재시작합니다.

```bash
# Machbase 서버 기동 확인
machadmin -e

# 모든 Collector 재시작
machcollectoradmin --list | awk 'NR>2 {print $1}' | \
  xargs -I{} sh -c 'machcollectoradmin --stop-collector={} ; machcollectoradmin --start-collector={}'
```

### 데이터 유실 방지

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

### 설정 오류로 인한 복구

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

### Collector Manager 재시작

개별 Collector 재시작으로 해결되지 않는 경우, Collector Manager 자체를 재시작합니다.

```bash
machcollectoradmin --shutdown
machcollectoradmin --startup

# 각 Collector 수동 시작
machcollectoradmin --start-collector=my_collector
```

> Collector Manager를 재시작하면 모든 Collector 인스턴스가 중지됩니다. 재시작 후 필요한 Collector를 수동으로 시작해야 합니다.
