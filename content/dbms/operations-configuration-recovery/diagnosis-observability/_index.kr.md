---
type: docs
title: '13.6 관측과 진단'
weight: 60
toc: true
---

운영 진단은 재현 시각과 증상을 기록한 뒤 server 상태, session·statement, storage·memory,
관련 log를 같은 시간축에서 확인합니다. `M$` metadata table은 schema를, `V$` virtual
table은 현재 상태를 제공합니다.

<a id="log-diagnosis-logs"></a>

## 진단과 로그

1. 문제 시작·종료 시각과 client 정보를 기록합니다.
2. `machadmin -e`로 server 응답을 확인합니다.
3. `V$SESSION`과 `V$STMT`에서 관련 작업을 찾습니다.
4. storage·memory·ROLLUP 등 증상에 맞는 virtual table을 확인합니다.
5. 같은 시각의 server·client·loader·Collector log를 비교합니다.
6. 변경 전 현재 property와 baseline을 저장합니다.

<a id="configuration-trace-log"></a>
<a id="log-diagnosis-logs-configuration-trace-log"></a>

## Trace log 설정

trace level과 파일 크기·보존 설정은 장애 분석에 필요한 범위만 조정합니다. 상세 property는
[설정 레퍼런스](/dbms/reference/configuration/dictionary-configuration/)에서 현재 release의
이름, 허용값, restart 필요 여부를 확인합니다. 민감 SQL과 데이터가 기록될 수 있으므로 log
접근 권한과 보존 기간을 설정합니다.

<a id="log-server-logs"></a>
<a id="log-diagnosis-logs-log-server-logs"></a>

## Server log

기본 trace 디렉터리는 `$MACHBASE_HOME/trc`입니다. 파일명이 고정돼 있다고 가정하지 말고
현재 디렉터리와 설정값을 확인합니다.

```bash
ls -lh "$MACHBASE_HOME/trc"
tail -n 200 "$MACHBASE_HOME/trc/machbase.trc"
```

오류 문자열만 세는 대신 최초 오류, 직전 경고, server 시작·종료, checkpoint·storage 사건을
시간 순서로 봅니다. log 파일을 manual 명령으로 일괄 삭제하지 않습니다.

<a id="log-logs-machsql"></a>
<a id="log-diagnosis-logs-log-logs-machsql"></a>

## machsql log

`machsql.history`에는 자격 증명이나 민감 SQL이 남을 수 있습니다. 운영 계정의 history
permission을 제한하고, 장애 공유 전에 내용을 검토합니다. 재현 SQL은 대상 database와
실행 시각, 결과·오류를 함께 보존합니다.

<a id="log-logs-machloader"></a>
<a id="log-diagnosis-logs-log-logs-machloader"></a>

## machloader log

대량 적재에서는 process exit code, summary, log, bad file을 함께 확인합니다.

- schema와 입력 column 수·순서
- delimiter, enclosure, encoding
- NULL과 DATETIME format
- 최초 실패 row와 반복되는 오류 code
- 최종 성공·실패 건수

bad file을 그대로 전체 재실행하지 말고 원인을 수정한 표본으로 검증한 뒤 실패 row만
재처리합니다.

<a id="log-logs-collector"></a>
<a id="log-diagnosis-logs-log-logs-collector"></a>

## Collector log

Collector 상태와 현재 FILE·SFTP source 접근, parser template, target table, 마지막 처리
위치를 확인합니다. 확인되지 않은 MQTT·socket source나 고정 log message를 진단 기준으로
사용하지 않습니다. 명령은 [Collector 운영](../collector/)을 참고합니다.

<a id="item"></a>

## Metadata table

`M$SYS_TABLES`, `M$SYS_COLUMNS`, `M$SYS_INDEXES` 등으로 현재 database의 schema를
확인합니다. 이름만으로 join하지 말고 database ID, owner ID, object ID를 포함합니다.
reserved object 이름과 내부 table 구조에 application이 의존하지 않도록 합니다.

<a id="item-2"></a>

## Virtual table

먼저 현재 release에서 실제 column을 확인합니다.

```sql
SELECT * FROM V$SESSION LIMIT 1;
SELECT * FROM V$STMT LIMIT 1;
SELECT * FROM V$PROPERTY LIMIT 1;
SELECT * FROM V$STORAGE_USAGE LIMIT 1;
SELECT * FROM V$SYSMEM LIMIT 1;
SELECT * FROM V$ROLLUP LIMIT 1;
SELECT * FROM V$LICENSE_INFO LIMIT 1;
```

전체 목록과 column 의미는
[system catalog](/dbms/reference/log-logs-system-catalog/virtual-table-full/)을 정본으로
사용합니다.

<a id="monitoring-capacity"></a>

## 모니터링과 용량 관리

고정 임계값보다 정상 baseline, 증가율, 업무 peak, recovery 여유를 기준으로 경보를
설정합니다. filesystem 사용량과 database storage 사용량을 함께 보고 backup·export가
사용하는 별도 공간도 포함합니다.

<a id="status-check-state-server"></a>
<a id="monitoring-capacity-status-check-state-server"></a>

## Server 상태

```bash
"$MACHBASE_HOME/bin/machadmin" -e
```

process 존재만으로 정상이라고 판단하지 않습니다. native connection과 가벼운 SQL,
최근 server log까지 확인합니다.

<a id="execution-session"></a>
<a id="monitoring-capacity-execution-session"></a>

## Session과 실행 SQL

```sql
SELECT id, user_name, user_ip, login_time, client_type
FROM V$SESSION
ORDER BY login_time DESC;

SELECT sess_id, id AS stmt_id, state, record_size, query
FROM V$STMT
ORDER BY sess_id, id;
```

장시간 실행이 곧 오류는 아닙니다. 업무 종류, 처리 row, client timeout, I/O·CPU 상태를
함께 확인한 뒤 cancel·kill 여부를 결정합니다.

<a id="capacity-disk"></a>
<a id="monitoring-capacity-capacity-disk"></a>

## Disk 용량

```bash
df -h "$MACHBASE_HOME"
du -sh "$MACHBASE_HOME/dbs"
```

별도 `DBS_PATH`를 사용하면 실제 경로를 확인합니다. 내부 partition file을 직접 수정하거나
삭제하지 않습니다.

<a id="memory-capacity"></a>
<a id="monitoring-capacity-memory-capacity"></a>

## Memory

OS available memory·swap과 `V$SYSMEM`, cache·query 동시성을 함께 비교합니다. manager별
내부 이름을 자동화의 고정 기준으로 사용하지 않습니다.

<a id="validation-backup"></a>
<a id="monitoring-capacity-validation-backup"></a>

## Backup 검증

backup 명령 성공만 확인하지 않습니다. 경로·크기·완료 상태를 기록하고 격리 환경에서
mount 또는 restore 후 주요 table, row 수, 시간 범위, 표본 query를 검증합니다.

<a id="failure"></a>
<a id="monitoring-capacity-failure"></a>

## 장애 자료 수집

- release와 edition
- 문제 시각·timezone
- 재현 명령과 database·사용자
- server·client·loader·Collector log
- 관련 virtual table 결과
- OS CPU·I/O·memory·disk
- 최근 schema·property·배포 변경
- 이미 시도한 조치와 결과

자격 증명, AUTH KEY, 개인정보와 원문 민감 데이터는 지원 자료에서 제거합니다.
