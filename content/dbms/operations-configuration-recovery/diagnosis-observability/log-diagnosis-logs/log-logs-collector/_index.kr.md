---
type: docs
title: 'Collector 로그'
weight: 50
---

Machbase Collector는 외부 데이터 소스로부터 데이터를 실시간으로 수집하여 Machbase에 적재하는 프로세스입니다. Collector의 동작 상태와 오류는 전용 로그 파일에 기록됩니다.

## 로그 파일 위치

Collector 로그는 기본적으로 `$MACHBASE_HOME/trc/` 디렉터리에 저장됩니다.

```
$MACHBASE_HOME/trc/
```

Collector 설정 파일에서 로그 파일 경로와 이름을 별도로 지정할 수 있습니다. 설정 파일에서 `LOG_DIR` 또는 `LOG_FILE` 항목을 확인하십시오.

## 로그 파일 유형

| 파일 | 내용 |
|------|------|
| `collector.log` (또는 설정에 따른 이름) | 수집 시작/종료, 성공/실패 건수, 연결 상태 |

## 주요 로그 항목

### 수집 시작/종료

```
[2024-01-15 09:00:05.001] [INFO] Collector started. source=mqtt://broker:1883, target=SENSOR_LOG
[2024-01-15 18:00:00.001] [INFO] Collector stopped. reason=SIGTERM
```

### 수집 통계

```
[2024-01-15 09:10:00.001] [INFO] Stats: received=12500, inserted=12498, error=2, queue_size=0
[2024-01-15 09:20:00.001] [INFO] Stats: received=25000, inserted=24995, error=5, queue_size=0
```

| 항목 | 설명 |
|------|------|
| received | 소스로부터 수신한 레코드 수 |
| inserted | Machbase에 성공적으로 적재한 레코드 수 |
| error | 적재에 실패한 레코드 수 |
| queue_size | 내부 버퍼에 대기 중인 레코드 수 |

### 연결 오류 패턴

소스 연결에 실패하거나 Machbase 서버에 연결할 수 없을 때 기록됩니다.

```
[2024-01-15 10:30:00.001] [ERROR] Connection failed. source=mqtt://broker:1883, reason=Connection refused
[2024-01-15 10:30:05.001] [WARN]  Reconnecting... attempt=1, next_retry=10s
[2024-01-15 10:30:15.001] [INFO]  Reconnected. source=mqtt://broker:1883
```

**조치**: 소스 서버의 상태와 네트워크 경로를 점검합니다. Collector는 일반적으로 재연결을 자동으로 시도합니다.

### 큐 오버플로 패턴

소스에서 데이터가 유입되는 속도가 Machbase에 적재하는 속도보다 빠를 때 발생합니다.

```
[2024-01-15 11:00:00.001] [WARN] Queue overflow detected. queue_size=100000, dropped=523
[2024-01-15 11:00:00.001] [WARN] Slow insert detected. avg_insert_time=250ms
```

**조치**:
- Machbase 서버의 리소스 상태(CPU, 디스크 I/O) 확인
- Collector 배치 크기(`BATCH_SIZE`) 조정
- 필요 시 Collector 인스턴스 수 증가

### Machbase 적재 오류

```
[2024-01-15 11:30:00.001] [ERROR] Insert failed. table=SENSOR_LOG, error=Column type mismatch: column=value
[2024-01-15 11:30:00.001] [ERROR] Insert failed. table=SENSOR_LOG, error=Disk full
```

**조치**:
- 타입 불일치: 소스 데이터 형식과 테이블 스키마를 비교
- 디스크 풀: 디스크 사용량 확인 및 공간 확보 ([디스크 사용량 확인](../../monitoring-capacity/capacity-disk/) 참조)

## 수집 상태 확인

Collector가 실행 중인 경우 V$STREAMS 가상 테이블에서도 상태를 조회할 수 있습니다.

```sql
-- STREAM 기반 Collector 상태 확인
SELECT name, state, last_ex_time, error_msg
  FROM v$streams
 ORDER BY name;
```

## 로그 실시간 모니터링

```bash
# Collector 로그 실시간 확인
tail -f $MACHBASE_HOME/trc/collector.log

# 오류 이벤트만 필터링
grep '\[ERROR\]\|\[WARN\]' $MACHBASE_HOME/trc/collector.log

# 시간대별 수집 통계 확인
grep 'Stats:' $MACHBASE_HOME/trc/collector.log | tail -20
```

## 수집 통계 점검 체크리스트

정기적으로 Collector 로그를 확인할 때 아래 항목을 점검합니다.

- `error` 건수가 `received` 대비 1% 이상인 경우 → 소스 데이터 품질 점검
- `queue_size`가 지속적으로 증가하는 경우 → 처리 지연 확인
- 재연결 로그가 반복되는 경우 → 소스 서버 또는 네트워크 점검
- 로그에 장시간 통계 메시지가 없는 경우 → Collector 프로세스 생존 여부 확인
