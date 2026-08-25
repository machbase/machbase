---
type: docs
title: '18.5 Collector 레퍼런스'
weight: 50
toc: true
---

Machbase Collector는 로컬 또는 SFTP 파일을 읽어 Machbase 테이블에 적재합니다. 설정은
JSON이 아니라 `KEY=VALUE` 형식의 `.tpl` 템플릿과 컬럼 매핑용 `.rgx` 파일로 구성합니다.

현재 배포 소스에서 확인되는 `COLLECT_TYPE`은 `FILE`과 `SFTP`입니다. TCP, UDP,
SERIAL, HTTP, MQTT는 지원 소스 타입으로 문서화하지 않습니다.

## 설정 구성

```text
[FILE 또는 SFTP 파일] -> [.tpl 수집 설정] -> [.rgx 파싱·컬럼 매핑] -> [Machbase]
```

| 파일 | 역할 |
|------|------|
| `.tpl` | 소스 타입, 입력 경로, 파싱 방식, DB 접속과 대상 테이블을 지정합니다. |
| `.rgx` | CSV·REGEX·JSON 입력의 레코드 파싱과 컬럼 매핑을 정의합니다. |

## 하위 레퍼런스

| 섹션 | 설명 |
|------|------|
| [Collector template 사전](./dictionary-collector-template/) | `.tpl`과 `.rgx`의 설정 키 |
| [Collector source type 사전](./dictionary-collector-source-type/) | `FILE`, `SFTP` 소스 타입 |
| [Collector regex/options 사전](./dictionary-collector-regex-options/) | 정규식 옵션과 패턴 예시 |

설치부터 파일 수집까지의 절차는
[Collector 기반 수집](/dbms/log-table-usage/collector-ingestion/)을 참고하십시오. Manager 운영과
장애 대응은 [Collector 운영](/dbms/operations-configuration-recovery/collector/)을
참고하십시오.
