---
type: docs
title: '7.13 Collector 기반 수집'
weight: 130
toc: true
---

Collector로 파일 또는 SFTP 레코드를 LOG 테이블에 입력할 때의 스키마와 mapping 기준을
설명합니다. Collector 등록·시작·복구는 운영 장을, template·regex key는 레퍼런스를
정본으로 사용합니다.

## 사용 기준

| 요구사항 | 시작점 |
|---|---|
| 로컬 파일의 반복 수집 | FILE source |
| 원격 파일의 반복 수집 | SFTP source |
| 애플리케이션의 실시간 row 전송 | SDK Append |
| 지원되지 않는 socket·ODBC source | 애플리케이션 또는 검증된 외부 도구 |

현재 공개된 source type은 [Collector source type 사전](/dbms/reference/collector/dictionary-collector-source-type/)에서
확인합니다. template에 남은 호환 key만 보고 다른 source를 지원한다고 가정하지 마십시오.

## 대상 LOG 스키마

Collector record의 컬럼 순서와 타입을 대상 테이블에 맞춥니다. `_ARRIVAL_TIME`은 자동
컬럼이므로 template의 사용자 컬럼으로 다시 선언하지 않습니다.

```sql
CREATE LOG TABLE collector_event (
    source_time DATETIME,
    host_name   VARCHAR(64),
    level       VARCHAR(16),
    message     VARCHAR(1024)
);
```

표본 파일에서 다음을 먼저 확인합니다.

- 문자 encoding과 줄바꿈
- delimiter와 enclosure
- DATETIME 원본 timezone과 format
- NULL·빈 문자열 처리
- 대상 컬럼 수, 순서와 최대 길이

## Mapping 검증

1. 한두 줄짜리 표본 파일을 준비합니다.
2. 설치된 버전의 template·regex 사전으로 mapping을 작성합니다.
3. 검증 환경에 Collector를 등록하고 한 파일만 처리합니다.
4. Collector 처리 건수와 LOG 테이블 행 수를 비교합니다.
5. 시간 범위, host, level과 message의 대표 값을 확인합니다.

```sql
SELECT COUNT(*) AS row_count,
       MIN(source_time) AS min_source_time,
       MAX(source_time) AS max_source_time
  FROM collector_event;
```

## 정본 구분

| 내용 | 정본 |
|---|---|
| 입력 방식 선택 | [데이터 입력과 반출](/dbms/development-tools-integration/data-input-load-export/) |
| 등록·시작·중지·복구 | [Collector 운영](/dbms/operations-configuration-recovery/collector/) |
| 처음부터 끝까지 실행 | [Collector 파일 적재](/dbms/scenario-guides/file-ingestion-collector/) |
| template·regex·source option | [Collector 레퍼런스](/dbms/reference/collector/) |

재처리 전에 완료 파일과 offset을 확인합니다. 이미 처리한 파일을 다시 source 위치에 두면
중복 입력될 수 있습니다.
