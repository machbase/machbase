---
type: docs
title: '17.5.3 Collector regex/options 사전'
weight: 30
toc: true
---

Collector의 `.rgx` 파일은 JSON이 아니라 `KEY=VALUE`와 괄호 목록 형식을 사용합니다. 이
페이지는 NFX 회귀 테스트에서 사용하는 공개 mapping 형식을 기준으로 설명합니다.

## 기본 구조

```ini
LOG_TYPE=machbase

COL_LIST=(
  (
    REGEX_NO=1
    NAME=id
    TYPE=integer
    SIZE=4
  ),
  (
    REGEX_NO=2
    NAME=name
    TYPE=varchar
    SIZE=32
  )
)

FIELD_TERM=","
RECORD_TERM="\n"
```

구분자 기반 입력은 `FIELD_TERM`과 `RECORD_TERM`을 사용합니다. 정규식 기반 입력은 대신
`REGEX`와 필요하면 `END_REGEX`를 지정합니다.

```ini
COL_LIST=(
  (
    REGEX_NO=1
    NAME=host_name
    TYPE=varchar
    SIZE=64
    USE_INDEX=1
  ),
  (
    REGEX_NO=2
    NAME=event_time
    TYPE=datetime
    SIZE=8
    DATE_FORMAT="%Y-%m-%d %H:%M:%S"
  ),
  (
    REGEX_NO=3
    NAME=value
    TYPE=double
    SIZE=8
  )
)

REGEX="^\\[([A-Za-z0-9_-]+)\\]\\s+\\[([0-9 :-]+)\\]\\s+(\\S+)"
END_REGEX="\\n"
```

## 컬럼 mapping

| key | 의미 | 확인 사항 |
|---|---|---|
| `REGEX_NO` | 정규식 capture 번호 또는 구분 필드 순서 | 1부터 시작하며 입력 순서와 일치 |
| `NAME` | 생성·입력할 컬럼 이름 | 대상 schema의 공개 컬럼 이름 사용 |
| `TYPE` | Collector 변환 타입 | 대상 Machbase 컬럼 타입과 호환 |
| `SIZE` | 값 buffer 크기 | 고정값이 아니라 타입·원본 최대 길이로 검증 |
| `DATE_FORMAT` | DATETIME 변환 형식 | 원본 timezone과 정밀도를 함께 기록 |
| `USE_INDEX` | 지원되는 입력 경로의 index 지정 | 배포 버전과 table type에서 지원 여부 확인 |

`COL_LIST`의 순서와 대상 테이블 컬럼 순서를 일치시키고, 필요한 system 컬럼을 사용자 컬럼으로
다시 선언하지 마십시오.

## 지원 타입 확인

회귀 샘플에는 `short`, `integer`, `long`, `float`, `double`, `varchar`, `datetime`, `ipv4`
등이 사용됩니다. 모든 Collector·테이블 조합에서 같은 타입 집합을 지원한다고 가정하지 말고
작은 표본으로 변환과 저장 결과를 확인하십시오.

## 검증 절차

1. 원본 한두 줄과 예상 capture 값을 표로 작성합니다.
2. `REGEX_NO`, `NAME`, `TYPE`, `SIZE`를 대상 schema와 대조합니다.
3. 검증 Collector로 한 파일만 처리합니다.
4. Collector 로그에서 regex match와 타입 변환 오류를 확인합니다.
5. 대상 테이블의 행 수, 시간 범위와 대표 값을 조회합니다.

```sql
SELECT COUNT(*) AS row_count,
       MIN(event_time) AS min_event_time,
       MAX(event_time) AS max_event_time
  FROM collector_event;
```

## 오류 처리

- 괄호, 쉼표, 따옴표가 맞지 않으면 `.rgx` parse 단계에서 실패합니다.
- `REGEX_NO`가 capture 수보다 크거나 순서가 잘못되면 기대한 컬럼에 값이 전달되지 않습니다.
- 숫자·DATETIME·IP 변환에 실패한 record는 Collector 로그와 실패 처리 결과를 확인합니다.
- match되지 않은 행의 skip·failure 정책은 Collector와 template 설정에 따라 달라질 수 있으므로
  실제 배포본에서 확인하십시오.

정확한 source와 template key는 [Collector source type](../dictionary-collector-source-type/)과
[Collector template](../dictionary-collector-template/)을 참고하십시오.
