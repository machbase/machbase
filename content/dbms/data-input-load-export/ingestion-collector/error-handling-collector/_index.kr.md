---
type: docs
title: 'Collector 오류 처리'
weight: 70
---

Collector 운영 중 발생할 수 있는 오류 유형과 원인을 파악하고, 각 상황에 맞는 복구 절차를 설명합니다.

## 오류 유형 분류

| 유형 | 원인 | 처리 방식 |
|------|------|-----------|
| 소스 연결 실패 | 소스 장치 오프라인, 네트워크 단절 | 재연결 대기 후 자동 재시도 |
| 파싱 오류 | 데이터 형식 불일치, 컬럼 수 불일치 | 오류 레코드 로그 기록 후 건너뜀 |
| 대상 연결 실패 | Machbase Broker 오프라인 | 재연결 대기, 내부 큐에 데이터 버퍼링 |
| 큐 오버플로우 | 수집 속도가 처리(Append) 속도보다 빠름 | 배치 크기 증가, 워커 스레드 추가 |
| 파일 접근 권한 오류 | 파일/디렉터리 권한 부족 | 권한 수정 후 Collector 재시작 |
| ODBC 드라이버 오류 | 드라이버 미설치, DSN 설정 오류 | 드라이버 설치 및 DSN 재설정 |

## 오류 로그 확인

모든 Collector 이벤트와 오류는 트레이스 로그 파일에 기록됩니다.

```bash
# 전체 로그 마지막 100줄 확인
tail -100 $MACHBASE_HOME/trc/machcollector.trc

# 오류, 실패, 건너뜀, 오버플로우 관련 메시지만 필터링
grep -i "error\|fail\|skip\|overflow\|warn" $MACHBASE_HOME/trc/machcollector.trc

# 특정 Collector 인스턴스 관련 메시지 확인
grep "file_sensor" $MACHBASE_HOME/trc/machcollector.trc | grep -i "error\|fail"

# 실시간 로그 모니터링
tail -f $MACHBASE_HOME/trc/machcollector.trc
```

트레이스 로그에서 확인할 주요 메시지:

| 메시지 키워드 | 의미 | 대응 방법 |
|-------------|------|-----------|
| `connect failed` | 소스 또는 대상 연결 실패 | 네트워크 및 서버 상태 확인 |
| `parse error` | 데이터 파싱 실패 | 템플릿 설정과 실제 데이터 형식 비교 |
| `queue full` / `overflow` | 내부 큐 포화 | 배치 크기 또는 워커 스레드 수 증가 |
| `flush delay` | Append 적재 지연 | I/O 환경 및 Machbase 상태 확인 |
| `permission denied` | 파일 접근 권한 없음 | 파일/디렉터리 권한 수정 |
| `skip record` | 오류 레코드 건너뜀 | 오류 원인 확인 후 데이터 보정 필요 여부 판단 |

## 소스 연결 실패

### 파일 소스

파일이 삭제되거나 디렉터리 경로가 변경된 경우 발생합니다.

```bash
# 감시 경로 및 파일 존재 여부 확인
ls -la /data/sensors/incoming/

# Collector 실행 계정의 디렉터리 접근 권한 확인
sudo -u machbase ls /data/sensors/incoming/
```

### TCP/UDP 소켓 소스

바인드 포트가 이미 사용 중이거나 방화벽에 의해 차단된 경우 발생합니다.

```bash
# 포트 사용 여부 확인
netstat -tlnp | grep 9090
ss -tlnp | grep 9090

# 방화벽 규칙 확인 (iptables)
sudo iptables -L INPUT -n | grep 9090
```

### Machbase 대상 연결 실패

Machbase 서버가 오프라인이거나 방화벽에 의해 차단된 경우 발생합니다. Collector는 자동으로 재연결을 시도하면서 내부 큐에 데이터를 계속 버퍼링합니다.

```bash
# Machbase 서버 상태 확인
machbase status

# 연결 테스트
machsql -s 127.0.0.1 -u SYS -p MANAGER -P 5656
```

재연결 설정:

```json
{
  "target": {
    "reconnect_interval": 5,
    "reconnect_max_retry": 0
  }
}
```

## 파싱 오류

데이터 형식이 템플릿 설정과 다를 때 발생합니다. 파싱에 실패한 레코드는 건너뛰고 다음 레코드를 처리하므로 Collector가 중단되지는 않습니다.

### 일반적인 원인

- CSV 파일의 필드 수가 설정된 `columns` 배열 길이와 다름
- 타임스탬프 형식이 `format` 설정과 다름
- 숫자 컬럼에 숫자가 아닌 값이 포함됨 (예: `N/A`, `-`, `null`)

### 확인 방법

```bash
# 파싱 오류 레코드 확인
grep -i "parse error\|skip record" $MACHBASE_HOME/trc/machcollector.trc | tail -20
```

로그에서 오류가 발생한 원시 데이터를 확인하고 템플릿 설정과 비교합니다.

### 오류 레코드 별도 저장 (Dead Letter Queue 패턴)

파싱에 실패한 레코드를 별도 파일에 저장하여 나중에 재처리하거나 수동으로 검토할 수 있습니다.

```json
{
  "source": {
    "error_path": "/data/collector_error/"
  }
}
```

오류 파일을 검토한 후 데이터를 수정하거나 템플릿을 조정하여 재수집합니다.

## 큐 오버플로우

수집 속도가 Machbase Append 처리 속도보다 빠를 때 발생합니다. 다음 단계로 순차적으로 조치합니다.

1. **배치 크기 증가:** `batch_size`를 2~5배 늘려 한 번에 더 많은 데이터를 Append합니다.

   ```json
   {
     "target": {
       "batch_size": 10000,
       "flush_interval": 1
     }
   }
   ```

2. **워커 스레드 추가:** Append 병렬도를 높입니다.

   ```json
   {
     "target": {
       "worker_threads": 4
     }
   }
   ```

3. **flush 주기 조정:** `flush_interval`을 늘려 I/O 횟수를 줄입니다.

4. **소스 전송 속도 제한:** 가능하다면 소스 측에서 전송 속도를 제한합니다.

5. **수평 확장:** Collector 인스턴스를 여러 개 실행하여 소스를 분산합니다.

## 일반적인 복구 절차

오류 발생 시 다음 순서로 점검합니다.

1. **로그에서 오류 원인 파악**

   ```bash
   grep -i "error\|fail\|warn" $MACHBASE_HOME/trc/machcollector.trc | tail -30
   ```

2. **소스 및 대상 연결 상태 확인**

   소스(파일 경로, 소켓 포트, SFTP 서버, ODBC DSN)와 대상(Machbase 서버) 연결이 정상인지 확인합니다.

3. **설정 파일 검토**

   템플릿의 컬럼 매핑, DATETIME 포맷, 구분자 설정이 실제 데이터와 일치하는지 확인합니다.

4. **Collector 재시작**

   설정을 수정한 후 Collector를 재시작합니다.

   ```bash
   machcollectoradmin --stop-collector=localhost.my_collector
   machcollectoradmin --start-collector=localhost.my_collector
   ```

5. **파일 위치 추적 초기화 (파일 소스)**

   파일 오프셋 정보를 초기화하고 처음부터 재수집해야 하는 경우:

   ```bash
   machcollectoradmin --stop-collector=localhost.file_sensor
   rm -f $MACHBASE_HOME/var/collector/file_sensor.pos
   machcollectoradmin --start-collector=localhost.file_sensor
   ```

## 오프라인 버퍼링

Machbase 서버가 오프라인인 동안 수집된 데이터를 로컬 디스크에 임시 저장했다가 서버가 복구되면 자동으로 적재하는 기능입니다.

```json
{
  "target": {
    "offline_buffer": {
      "enabled": true,
      "path": "/data/collector_buffer/",
      "max_size_mb": 1024
    }
  }
}
```

| 파라미터 | 설명 |
|---------|------|
| `enabled` | 오프라인 버퍼링 활성화 여부 |
| `path` | 버퍼 파일을 저장할 로컬 디렉터리 |
| `max_size_mb` | 버퍼 최대 크기 (MB). 초과 시 가장 오래된 데이터 삭제 |

## 참고

- 파일 Collector 위치 추적: [../file-collector](../file-collector)
- 성능 튜닝 (배치 크기, 스레드): [../../../performance-tuning/performance-tuning/ingestion-performance-tuning-collector](../../../performance-tuning/performance-tuning/ingestion-performance-tuning-collector)
- Collector 레퍼런스: [../../../reference/collector](../../../reference/collector)
