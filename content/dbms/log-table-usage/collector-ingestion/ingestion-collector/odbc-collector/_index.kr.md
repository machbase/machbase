---
type: docs
title: 'ODBC Collector'
weight: 50
---

현재 확인된 Collector `COLLECT_TYPE`은 `FILE`과 `SFTP`입니다. ODBC 수집 설정은 현재
브랜치의 Collector 타입 파서에서 확인되지 않았으므로 이 장에서는 설정 예제를 제공하지
않습니다.

외부 RDBMS 데이터를 Machbase로 이전하거나 주기적으로 적재해야 하는 경우에는 다음 경로를
검토합니다.

## 대안

| 요구 사항 | 권장 경로 |
|-----------|-----------|
| 일회성 대량 이전 | 외부 DB에서 CSV 반출 후 `machloader` 또는 `LOAD DATA INFILE` |
| 애플리케이션 레벨 동기화 | JDBC/ODBC 클라이언트에서 조회 후 Machbase SDK 또는 SQL INSERT |
| 원격 서버에 생성된 CSV 수집 | [SFTP Collector](../sftp-collector/) |
