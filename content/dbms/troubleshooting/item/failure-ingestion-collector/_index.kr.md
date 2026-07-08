---
type: docs
title: 'Collector 수집이 실패할 때'
weight: 30
---

Machbase Collector를 통한 데이터 수집이 멈추거나 지연되는 경우 트레이스 로그가 첫 번째 단서입니다. 소스 연결 실패, 큐 오버플로우, Machbase 연결 실패, 데이터 형식 오류 중 어느 쪽인지 로그를 보고 판단합니다.

## 트레이스 로그 확인

Collector 기본 로그는 `$MACHBASE_COLLECTOR_HOME/trc/machcollector.trc`에 기록됩니다.
Collector별 trace 설정을 별도로 사용한 경우에는 해당 collector 이름의 로그를 함께 확인합니다.

```bash
# 최근 100줄 확인
tail -100 $MACHBASE_COLLECTOR_HOME/trc/machcollector.trc

# 오류/경고 메시지만 필터링
grep -i "error\|fail\|queue\|overflow" \
  $MACHBASE_COLLECTOR_HOME/trc/machcollector.trc | tail -50
```

`MACHBASE_COLLECTOR_HOME`을 별도로 지정하지 않았다면 Collector 실행 환경의 trace 경로를
확인하십시오.

## 원인별 진단

### 1. 소스 연결 실패

소스 장치나 서버에 연결할 수 없을 때 발생합니다.

**로그 예시**

```
[ERROR] failed to connect to source: connection refused (192.168.1.100:1234)
[ERROR] source timeout after 30s
```

**진단 및 해결**

```bash
# 소스 서버/장치 네트워크 연결 확인
ping 192.168.1.100

# 포트 연결 가능 여부 확인
telnet 192.168.1.100 1234
```

- 소스 서버가 정상 실행 중인지 확인합니다.
- 방화벽 규칙에서 해당 포트가 허용되어 있는지 확인합니다.
- Collector 설정 파일에서 소스 접속 정보(호스트, 포트, 계정)를 재확인합니다.

### 2. 큐 오버플로우

소스에서 데이터가 들어오는 속도보다 Machbase에 저장하는 속도가 느릴 때 발생합니다. 큐가 가득 차면 데이터 유실이 생길 수 있습니다.

**로그 예시**

```
[WARN] queue overflow: dropping 500 records
[WARN] queue delay: 15000ms behind
[INFO] queue size: 10000/10000 (full)
```

**큐 상태 모니터링**

```bash
grep -i "queue\|delay\|overflow\|slow" \
  $MACHBASE_COLLECTOR_HOME/trc/machcollector.trc | tail -50
```

**해결 방법**

- Collector 설정에서 배치 크기(`batch_size`)를 늘려 한 번에 더 많은 데이터를 저장합니다.
- 병렬 처리 스레드 수(`worker_threads`)를 늘립니다.
- Machbase 서버의 Append 성능을 점검합니다([쿼리가 느릴 때](../../performance/slow/) 참고).

### 3. Machbase 연결 실패

Collector가 Machbase에 연결하지 못하는 경우입니다.

**로그 예시**

```
[ERROR] failed to connect to Machbase: connection refused (localhost:5656)
[ERROR] Machbase broker is not responding
```

**진단 및 해결**

```bash
# Machbase 서버 상태 확인
machadmin -e

# 서버가 중지된 경우 시작
machadmin -u
```

- Machbase가 정상 실행 중이라면 Collector 설정 파일의 접속 정보(호스트, 포트, 사용자, 비밀번호)를 확인합니다.
- 포트 번호가 `machbase.conf`의 `PORT_NO` 설정과 일치하는지 확인합니다.

### 4. 데이터 형식 오류

소스 데이터의 형식이 Machbase 테이블의 스키마와 맞지 않는 경우입니다.

**로그 예시**

```
[ERROR] type mismatch at column 'temperature': expected DOUBLE, got STRING
[ERROR] invalid datetime format: '2024/01/15 09:30:00'
```

**해결 방법**

- Collector 설정 파일에서 컬럼 매핑과 타입 변환 설정을 확인합니다.
- 날짜 형식이 맞지 않는다면 Collector의 날짜 파싱 포맷을 수정합니다.
- 소스 데이터에 NULL 또는 빈 값이 섞여 있다면 NULL 처리 방식을 설정합니다.

## 수집 복구 절차

수집이 완전히 중단된 경우 다음 순서로 복구합니다.

**1단계: 로그 확인 및 원인 파악**

```bash
grep -i "error\|fail" $MACHBASE_COLLECTOR_HOME/trc/machcollector.trc | tail -30
```

**2단계: Collector 재시작**

```bash
# Collector 중지
machcollectoradmin --stop-collector=<collector-name>

# 잠시 대기 후 시작
machcollectoradmin --start-collector=<collector-name>
```

**3단계: 수집 재개 확인**

```bash
# 로그에서 정상 수집 여부 확인
tail -f $MACHBASE_COLLECTOR_HOME/trc/machcollector.trc
```

`[INFO] collected N records` 메시지가 주기적으로 출력되면 정상입니다.

**4단계: 배치 크기 조정 (큐 오버플로우인 경우)**

Collector 설정 파일을 열어 배치 크기를 기존 값의 2배로 늘린 뒤 재시작합니다. 변경 후 큐 딜레이 로그가 줄어드는지 확인합니다.
