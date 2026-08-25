---
type: docs
title: '12.8 입력 성능과 연동 경로'
weight: 80
toc: true
---

입력 성능은 먼저 적재 경로를 고른 뒤, 대표 데이터로 배치 크기와 병렬도를 측정해
조정합니다. 상세 튜닝 원칙과 예제는
[대량 입력 성능 튜닝](/dbms/performance-tuning/performance-tuning/#performance-tuning-bulk)을
정본으로 사용하십시오.

## 입력 경로 선택

| 요구사항 | 권장 경로 | 다음 문서 |
|----------|-----------|-----------|
| 지속적인 TAG/LOG 대량 수집 | SDK Append API | [SDK 기능 지원표](/dbms/development-tools-integration/sdk-support-scope/#support-scope-sdk-append) |
| 애플리케이션의 소량·범용 DML | Prepared SQL `INSERT` | [공통 연동 개념](/dbms/development-tools-integration/concepts-common/) |
| 클라이언트 CSV 가져오기·내보내기 | `machloader` | [machloader 레퍼런스](/dbms/reference/command-line-tools/dictionary-machloader/) |
| 서버가 접근할 수 있는 파일 적재 | `LOAD DATA INFILE` | [LOAD DATA INFILE](/dbms/reference/sql/syntax-dictionary-sql/load-data-infile-syntax/) |
| 로컬·SFTP 파일의 반복 수집 | Collector | [Collector 기반 수집](/dbms/log-table-usage/collector-ingestion/) |

<a id="performance-principles"></a>

## 측정 순서

1. 대표 입력 경로 하나를 선택합니다.
2. 동일한 데이터와 서버 상태에서 기준 처리량과 지연을 기록합니다.
3. 배치 크기를 한 단계씩 바꾸고 처리량, flush 지연, 실패 시 재전송 범위를 비교합니다.
4. 단일 연결이 포화된 뒤에만 연결 수나 worker 수를 늘립니다.
5. CPU, 디스크, 네트워크 중 먼저 포화되는 자원을 확인합니다.
6. 변경 전후 결과를 같은 조건으로 다시 측정합니다.

TAG/LOG 입력은 Append를 우선 검토하고, 불필요한 인덱스를 줄이며, 가능하면 오래된
시각부터 순서대로 적재합니다. 특정 배치 크기나 worker 수를 보편적인 최적값으로
간주하지 마십시오.

<a id="path-guide-sdk"></a>

## SDK 경로

언어별 설치, 연결, Append와 오류 처리는 11장 SDK 레퍼런스에서 확인합니다.

- [Machbase SQLCLI와 ODBC](/dbms/development-tools-integration/cli-odbc/)
- [JDBC](/dbms/development-tools-integration/jdbc/)
- [Python](/dbms/development-tools-integration/python/)
- [Node.js / TypeScript](/dbms/development-tools-integration/node-js-typescript/)
- [.NET Connector](/dbms/development-tools-integration/net-connector/)
- [Go](/dbms/development-tools-integration/go/)

Append, batch, flush, 병렬 입력과 네트워크 병목의 상세 설명은
[대량 입력 성능 튜닝](/dbms/performance-tuning/performance-tuning/#performance-tuning-bulk)에서
계속합니다.
