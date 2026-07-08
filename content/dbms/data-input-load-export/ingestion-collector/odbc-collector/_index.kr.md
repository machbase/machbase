---
type: docs
title: 'ODBC Collector'
weight: 50
---

ODBC Collector는 ODBC 드라이버를 통해 외부 데이터베이스(Oracle, MySQL, MSSQL, PostgreSQL 등)에 접속하여 지정한 쿼리의 결과를 Machbase 테이블에 적재합니다. 기존 RDB에 축적된 센서/로그 데이터를 Machbase로 마이그레이션하거나 주기적으로 동기화할 때 사용합니다.

## 동작 원리

```
[외부 DB (Oracle/MySQL/MSSQL)]
  SELECT ... WHERE ts > ? ──ODBC 쿼리──→ [Collector]
                                               │
                                    [컬럼 타입 변환 + Append]
                                               │
                                         [Machbase DB]
                                               │
                              [마지막 처리 시간 상태 저장]
```

Collector는 쿼리 실행 후 마지막으로 처리한 기준 값(예: 타임스탬프)을 내부에 저장합니다. 다음 실행 주기에는 저장된 값 이후의 데이터만 쿼리하여 증분 수집을 구현합니다.

## 사전 요건: ODBC 드라이버 설치

ODBC Collector를 사용하려면 Machbase가 설치된 서버에 대상 DB에 맞는 ODBC 드라이버를 설치해야 합니다.

### Linux에서 ODBC 드라이버 설정 예시 (MySQL)

```bash
# unixODBC 설치
sudo apt-get install unixodbc unixodbc-dev    # Ubuntu/Debian
sudo yum install unixODBC unixODBC-devel      # RHEL/CentOS

# MySQL ODBC 드라이버 설치
sudo apt-get install libmyodbc
# 또는 MySQL 공식 드라이버 다운로드 후 설치

# DSN 설정 파일 편집 (/etc/odbc.ini)
[mysql-sensor]
Driver   = MySQL ODBC 8.0 Unicode Driver
Server   = mysql-host
Port     = 3306
Database = sensordb
User     = dbuser
Password = dbpassword
Charset  = utf8

# 연결 테스트
isql -v mysql-sensor
```

## 기본 설정

### 대상 테이블 생성

```sql
CREATE TABLE odbc_sensor_log (
    sensor_id  VARCHAR(64),
    ts         DATETIME,
    value      DOUBLE
);
```

### Collector 설정 파일 (JSON)

`$MACHBASE_HOME/conf/collector/odbc_collector.json`:

```json
{
  "name": "odbc_sensor",
  "source": {
    "type": "ODBC",
    "dsn": "mysql-sensor",
    "query": "SELECT sensor_id, ts, value FROM sensor_data WHERE ts > ? ORDER BY ts",
    "interval": 30,
    "cursor_column": "ts",
    "cursor_format": "YYYY-MM-DD HH24:MI:SS"
  },
  "template": {
    "type": "ODBC",
    "columns": [
      {"name": "sensor_id", "type": "VARCHAR",  "source_column": "sensor_id"},
      {"name": "ts",        "type": "DATETIME", "source_column": "ts",    "format": "YYYY-MM-DD HH24:MI:SS"},
      {"name": "value",     "type": "DOUBLE",   "source_column": "value"}
    ]
  },
  "target": {
    "table": "odbc_sensor_log",
    "server": {
      "host": "127.0.0.1",
      "port": 5656,
      "user": "SYS",
      "password": "MANAGER"
    }
  }
}
```

## 소스 파라미터 상세

| 파라미터 | 필수 | 기본값 | 설명 |
|---------|------|--------|------|
| `type` | 필수 | - | `"ODBC"` |
| `dsn` | 필수 | - | ODBC DSN 이름 (또는 연결 문자열) |
| `user` | 선택 | - | DB 접속 사용자명 (DSN에 포함되지 않은 경우) |
| `password` | 선택 | - | DB 접속 비밀번호 |
| `query` | 필수 | - | 데이터를 조회할 SQL 쿼리 (`?`는 커서 값 바인딩) |
| `interval` | 선택 | `60` | 쿼리 실행 주기 (초) |
| `cursor_column` | 선택 | - | 증분 수집 기준이 되는 컬럼 이름 |
| `cursor_format` | 선택 | - | 커서 컬럼의 시간 포맷 |
| `batch_size` | 선택 | `1000` | 한 번에 가져올 행 수 |

## 증분 수집 설정

전체 데이터를 매번 쿼리하지 않고, 마지막으로 처리한 기준 값 이후의 데이터만 쿼리하여 수집 효율을 높입니다.

```json
{
  "source": {
    "query": "SELECT sensor_id, ts, value FROM sensor_data WHERE ts > ? ORDER BY ts",
    "cursor_column": "ts",
    "cursor_format": "YYYY-MM-DD HH24:MI:SS",
    "initial_cursor": "2024-01-01 00:00:00"
  }
}
```

- `cursor_column`: 쿼리 결과에서 커서 값을 추출할 컬럼 이름. 가장 마지막으로 처리된 행의 이 컬럼 값이 다음 실행 시 `?` 바인딩 파라미터로 전달됩니다.
- `initial_cursor`: 최초 실행 시 사용할 초기 커서 값. 처음부터 전체 데이터를 수집하려면 데이터가 시작되는 시점으로 설정합니다.

## ODBC 연결 문자열 직접 지정

DSN 대신 연결 문자열을 직접 지정할 수도 있습니다.

```json
{
  "source": {
    "type": "ODBC",
    "connection_string": "Driver={Oracle 21 ODBC driver};DBQ=oracle-host:1521/ORCL;UID=dbuser;PWD=dbpassword"
  }
}
```

주요 ODBC 드라이버별 연결 문자열 형식:

| DB | 연결 문자열 예시 |
|----|-----------------|
| Oracle | `Driver={Oracle 21 ODBC driver};DBQ=host:1521/SID;UID=user;PWD=pass` |
| MySQL | `Driver={MySQL ODBC 8.0 Unicode Driver};Server=host;Port=3306;Database=db;UID=user;PWD=pass` |
| MSSQL | `Driver={ODBC Driver 17 for SQL Server};Server=host;Database=db;UID=user;PWD=pass` |
| PostgreSQL | `Driver={PostgreSQL Unicode};Server=host;Port=5432;Database=db;UID=user;PWD=pass` |

## 대용량 수집 시 배치 크기 조정

외부 DB에서 대량의 데이터를 수집할 때는 배치 크기를 조정하여 성능을 최적화합니다.

```json
{
  "source": {
    "batch_size": 10000,
    "query": "SELECT sensor_id, ts, value FROM sensor_data WHERE ts > ? ORDER BY ts FETCH FIRST 10000 ROWS ONLY"
  }
}
```

> **권장 사항:** 외부 DB 서버에 부하가 가지 않도록 `interval`을 적절히 설정하고, 쿼리의 WHERE 조건에 인덱스가 있는 컬럼을 사용합니다.

## Collector 등록 및 시작

```bash
machcollectoradmin --startup
```

```sql
CREATE COLLECTOR localhost.odbc_sensor
FROM "$MACHBASE_HOME/conf/collector/odbc_collector.json";

ALTER COLLECTOR localhost.odbc_sensor START;
```

## ODBC 연결 및 수집 상태 확인

```bash
# ODBC 연결 및 쿼리 관련 로그 확인
grep -i "odbc\|query\|connect\|error" $MACHBASE_HOME/trc/machcollector.trc | tail -50

# 실시간 모니터링
tail -f $MACHBASE_HOME/trc/machcollector.trc
```

## 참고

- 오류 처리: [../error-handling-collector](../error-handling-collector)
- Collector를 사용해야 하는 경우: [../use-cases-collector](../use-cases-collector)
