---
type: docs
title: 'Collector 오류 처리'
weight: 70
---

Collector 운영 중 발생할 수 있는 오류 유형과 점검 절차를 정리합니다. 현재 확인된
Collector 설정은 `.tpl` 파일과 `.rgx` 컬럼 매핑 파일을 사용합니다.

## 오류 유형 분류

| 유형 | 원인 | 처리 방식 |
|------|------|-----------|
| 파일 접근 실패 | `LOG_SOURCE`, `FILE_BACKUP_PATH` 경로 오류 또는 권한 부족 | 경로와 실행 계정 권한 확인 |
| SFTP 연결 실패 | `SFTP_HOST`, `SFTP_PORT`, `SFTP_USER`, `SFTP_PASS` 오류 | 접속 정보와 네트워크 확인 |
| 파싱 오류 | `PARSE_TYPE`, `.rgx` 컬럼 매핑, 실제 데이터 형식 불일치 | `.tpl`/`.rgx`와 원본 파일 비교 |
| 대상 연결 실패 | `DB_ADDR`, `DB_PORT`, `DB_USER`, `DB_PASS` 오류 또는 Machbase 중지 | DB 접속 확인 |
| 적재 오류 | 대상 테이블명, 컬럼 타입, 컬럼 순서 불일치 | `DB_TABLE_NAME`과 `.rgx` 컬럼 정의 확인 |

## 오류 로그 확인

Collector 이벤트와 오류는 트레이스 로그에서 확인합니다.

```bash
# 전체 로그 마지막 100줄 확인
tail -100 $MACHBASE_HOME/trc/machcollector.trc

# 오류, 실패, 건너뜀 관련 메시지만 필터링
grep -i "error\|fail\|skip\|warn" $MACHBASE_HOME/trc/machcollector.trc

# 실시간 로그 모니터링
tail -f $MACHBASE_HOME/trc/machcollector.trc
```

## 파일 소스 점검

```bash
# LOG_SOURCE 파일 존재 여부 확인
ls -l /data/sensors/sensor.csv

# Collector 실행 계정의 읽기 권한 확인
sudo -u machbase test -r /data/sensors/sensor.csv && echo readable

# 처리 완료 파일 보관 경로 쓰기 권한 확인
sudo -u machbase test -w /data/sensors/done && echo writable
```

확인할 `.tpl` 키:

```text
COLLECT_TYPE=FILE
LOG_SOURCE=/data/sensors/sensor.csv
FILE_BACKUP_PATH=/data/sensors/done
```

## SFTP 소스 점검

```bash
# SFTP 서버 연결 확인
sftp -P 22 collector@sftp.example.com
```

확인할 `.tpl` 키:

```text
COLLECT_TYPE=SFTP
SFTP_HOST=sftp.example.com
SFTP_PORT=22
SFTP_USER=collector
SFTP_PASS=secret
SFTP_TIMEOUT=30
LOG_SOURCE=/data/sensor/sensor.csv
```

## Machbase 대상 연결 점검

```bash
# Machbase 서버 상태 확인
machbase status

# Collector 설정과 같은 접속 정보로 연결 테스트
machsql -s 127.0.0.1 -P 5656 -u SYS -p MANAGER
```

확인할 `.tpl` 키:

```text
DB_TABLE_NAME=sensor_log
DB_ADDR=127.0.0.1
DB_PORT=5656
DB_USER=SYS
DB_PASS=MANAGER
```

## 파싱 오류 점검

파싱 오류가 발생하면 `PARSE_TYPE`, `REGEX_PATH`, `.rgx` 컬럼 정의를 원본 데이터와
비교합니다.

```text
PARSE_TYPE=CSV
REGEX_PATH=/opt/machbase/collector/sensor.rgx
```

`.rgx` 예시:

```text
COL_LIST=NAME,TIME,VALUE
FIELD_TERM=,
RECORD_TERM=\n
REGEX_NO=1

NAME=NAME
TYPE=VARCHAR
SIZE=64

NAME=TIME
TYPE=DATETIME
SIZE=8

NAME=VALUE
TYPE=DOUBLE
SIZE=8
```

원본 CSV 예시:

```csv
TEMP-01,2024-01-01 10:00:00,25.3
TEMP-02,2024-01-01 10:00:01,25.7
```

## 일반적인 복구 절차

1. 로그에서 오류 원인을 확인합니다.

   ```bash
   grep -i "error\|fail\|warn" $MACHBASE_HOME/trc/machcollector.trc | tail -30
   ```

2. `.tpl` 파일의 `COLLECT_TYPE`, `LOG_SOURCE`, `REGEX_PATH`, DB 접속 정보를 확인합니다.
3. `.rgx` 파일의 `COL_LIST`, 각 컬럼의 `NAME`, `TYPE`, `SIZE`가 대상 테이블과 맞는지 확인합니다.
4. 설정을 수정한 후 Collector를 재시작합니다.

   ```bash
   machcollectoradmin --stop-collector=localhost.my_collector
   machcollectoradmin --start-collector=localhost.my_collector
   ```

## 참고

- 파일 Collector: [../file-collector](../file-collector)
- SFTP Collector: [../sftp-collector](../sftp-collector)
- 템플릿과 정규식: [../template-regex-collector](../template-regex-collector)
