---
type: docs
title: 'Collector를 사용해야 하는 경우'
weight: 10
---

데이터를 Machbase에 입력하는 방법은 여러 가지가 있습니다. Collector를 사용할지, 아니면 애플리케이션에서 직접 API를 호출할지는 데이터 소스의 성격과 운영 환경에 따라 달라집니다. 이 섹션에서는 Collector 도입이 적합한 상황과 그렇지 않은 상황을 구체적으로 설명합니다.

## Collector vs 직접 API 선택 기준

| 상황 | 권장 방법 |
|------|-----------|
| 애플리케이션이 직접 Machbase에 쓸 수 있음 | Append API (JDBC/Python/Go 등) |
| 외부 장치나 파일에서 자동 수집이 필요함 | Collector |
| 로컬 파일 또는 SFTP 파일을 자동 수집해야 함 | Collector |
| 수신 데이터의 형식 변환이나 파싱이 필요함 | Collector (템플릿 활용) |
| 네트워크 중단 시 데이터 손실 없이 버퍼링이 필요함 | Collector |
| 원격 서버의 파일을 주기적으로 가져와야 함 | Collector (SFTP 소스) |
| 단일 애플리케이션에서 실시간으로 대량 적재 | Append API (직접 연결이 더 효율적) |

## Collector가 적합한 구체적 사용 사례

### 1. 로그 파일 모니터링

애플리케이션이나 시스템이 생성하는 로그 파일을 실시간으로 감시하고 분석 가능한 형태로 적재합니다. 파일 회전(rotation)이 발생해도 새 파일을 자동으로 감지합니다.

```
[App Log File] ──파일 감시──→ [Collector (파일 소스)] ──→ [Machbase]
```

### 2. 원격 서버 파일 수집

원격 장비나 서버에서 주기적으로 생성되는 CSV 파일을 SFTP로 수집합니다. 파일 다운로드, 파싱, 적재, 처리 완료 후 파일 관리까지 자동화됩니다.

```
[원격 서버 /data/*.csv] ──SFTP──→ [Collector (SFTP 소스)] ──→ [Machbase]
```

### 3. 기존 시스템의 DB 데이터 마이그레이션

Oracle, MySQL, MSSQL 등의 기존 RDB에 축적된 센서/로그 데이터를 Machbase로 이전할 때는 외부 DB에서 CSV로 반출한 뒤 `machloader` 또는 `LOAD DATA INFILE`로 적재합니다. 애플리케이션 레벨에서 주기적으로 조회한 뒤 SDK나 SQL INSERT로 입력하는 방식도 사용할 수 있습니다.

## Collector가 적합하지 않은 경우

다음 상황에서는 Collector를 사용하지 않는 것이 더 효율적입니다.

- **애플리케이션이 Machbase에 직접 연결 가능한 경우:** JDBC, Python, Go 등의 드라이버를 사용해 Append API를 직접 호출하면 중간 컴포넌트 없이 더 낮은 지연시간으로 적재할 수 있습니다.
- **단발성 대량 데이터 로드:** CSV 파일을 한 번에 대량으로 적재하는 경우에는 `machloader`나 `LOAD DATA` 구문이 더 적합합니다.
- **실시간 스트리밍(Kafka, MQTT):** Machbase Neo의 내장 스트리밍 파이프라인이나 Flink/Kafka Connect 커넥터를 사용하는 것이 더 효율적입니다.

## Collector 선택 시 확인 사항

Collector 도입을 결정하기 전에 다음 항목을 확인합니다.

1. **데이터 소스 프로토콜:** 소스가 FILE 또는 SFTP 파일로 제공되는가?
2. **데이터 형식:** 원시 데이터가 CSV, JSON, 고정 너비, 로그 텍스트 등 어떤 형식인가?
3. **수집 주기:** 실시간 연속 수집인가, 아니면 주기적인 배치 수집인가?
4. **네트워크 안정성:** 소스와 Machbase 사이의 연결이 불안정할 수 있는가?
5. **처리 후 파일 관리:** 수집 완료 파일을 이동하거나 삭제하는 정책이 필요한가?

## 참고

- 파일 수집 설정: [../file-collector](../file-collector)
- SFTP 수집 설정: [../sftp-collector](../sftp-collector)
