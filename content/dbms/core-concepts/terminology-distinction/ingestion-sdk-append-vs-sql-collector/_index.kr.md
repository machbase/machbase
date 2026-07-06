---
type: docs
title: 'SDK append vs SQL APPEND vs Collector 수집'
weight: 60
---

실시간으로 데이터를 Machbase에 수집하는 경로는 크게 세 가지입니다. 성능 요구사항, 데이터 소스 유형, 개발 비용에 따라 적합한 방법이 달라집니다.

## 비교 표

| 항목 | SDK APPEND | SQL INSERT | Collector |
| --- | --- | --- | --- |
| 수집 방식 | 언어별 SDK로 APPEND 프로토콜 직접 사용 | 표준 SQL INSERT 문장 | Machbase 내장 수집기, 별도 설정 파일 |
| 성능 | 최고 (배치 전송, 최소 오버헤드) | 낮음 (행 단위, SQL 파싱 오버헤드) | 높음 (내부 최적화) |
| 지원 언어/환경 | Go, Python, .NET, C 등 | ODBC, JDBC, machsql 등 모든 SQL 클라이언트 | 파일, 소켓, ODBC, SFTP 등 소스 기반 |
| 개발 필요성 | 높음 (SDK API 구현 필요) | 낮음 (SQL 지식만으로 구현 가능) | 낮음 (설정 파일 작성) |
| 배치 처리 | 가능 (여러 행을 한 번에 전송) | 가능하나 비효율적 | 가능 (내부 버퍼링) |
| 소스 다양성 | 코드에서 직접 생성하는 데이터 | 코드에서 직접 생성하는 데이터 | 파일, 소켓, DB, SFTP 등 외부 소스 |
| 주요 사용 사례 | 고성능 수집기, 실시간 파이프라인 직접 구현 | 간단한 애플리케이션, 테스트, 저빈도 입력 | 외부 시스템 데이터 자동 수집 |

## SDK APPEND

SDK APPEND는 Go, Python, .NET 등 언어별 Machbase SDK를 사용해 APPEND 프로토콜로 데이터를 전송하는 방식입니다. SQL 파싱 단계를 거치지 않고 서버의 저장 계층에 직접 데이터를 전달하므로, 같은 양의 데이터를 SQL INSERT보다 수십 배 빠르게 처리할 수 있습니다.

```go
// Go SDK APPEND 예시 (개념)
appender, _ := conn.Appender(ctx, "sensor_values")
defer appender.Close()

appender.Append("temp_sensor_01", time.Now(), 23.5)
appender.Append("temp_sensor_02", time.Now(), 21.0)
// Flush 시 배치로 전송
```

초당 수십만 건 이상을 처리해야 하는 고성능 수집 파이프라인에서 SDK APPEND를 기본으로 사용합니다. 단, SDK를 사용하는 코드를 직접 작성해야 합니다.

## SQL INSERT

표준 SQL `INSERT` 문장으로 데이터를 입력합니다. ODBC, JDBC, machsql 등 모든 SQL 클라이언트에서 사용할 수 있어 범용성이 가장 높습니다.

```sql
INSERT INTO sensor_values (name, time, value)
VALUES ('temp_sensor_01', NOW(), 23.5);
```

데이터 입력 빈도가 낮거나(초당 수천 건 이하), 별도 SDK 통합 없이 기존 애플리케이션에서 데이터를 입력해야 할 때 적합합니다. 테스트나 운영 도중 소량의 데이터를 수동으로 넣을 때도 SQL INSERT를 사용합니다.

## Collector

Collector는 Machbase에 내장된 수집기입니다. 설정 파일을 작성하면 파일, 소켓, ODBC 소스, SFTP 등 외부 시스템에서 데이터를 자동으로 읽어 Machbase 테이블에 적재합니다. 코드를 직접 작성하지 않고도 다양한 소스의 데이터를 수집할 수 있습니다.

```ini
# Collector 설정 파일 예시 (개념)
[SOURCE]
type = file
path = /var/log/sensor/*.log

[DESTINATION]
table = device_log
```

Collector는 외부 파일 시스템에서 로그를 주기적으로 읽거나, 소켓으로 데이터를 수신하는 등 사전 정의된 소스 유형을 처리할 때 유용합니다. 커스텀 변환 로직이 필요하지 않고 소스 형식이 Collector가 지원하는 유형이라면, 개발 비용 없이 데이터 수집을 구성할 수 있습니다.

## 선택 기준

| 상황 | 권장 방법 |
| --- | --- |
| 초당 수십만 건 이상의 고성능 수집 | SDK APPEND |
| 기존 애플리케이션에서 소량 입력 | SQL INSERT |
| SDK 통합 없이 범용 SQL 클라이언트 사용 | SQL INSERT |
| 파일, 소켓 등 외부 소스에서 자동 수집 | Collector |
| 설정 파일만으로 수집 파이프라인 구성 | Collector |

## 다음 읽을 내용

- [LOAD DATA INFILE vs fastload](../load-data-infile-vs-fastload/) — 파일 기반 일괄 적재 방법 비교
- [machloader vs csvimport / csvexport vs tagmetaimport](../machloader-vs-csvimport-csvexport-tagmetaimport/) — 파일 기반 입출력 도구 비교
- [쓰기 중심 워크로드와 append-only 모델](/dbms/core-concepts/concepts/write-oriented-append-only/) — APPEND 모델의 설계 원칙
