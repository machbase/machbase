---
type: docs
title: '17.5 Collector 레퍼런스'
weight: 50
toc: true
---

Machbase Collector는 다양한 소스(파일, 네트워크, 시리얼 포트 등)에서 데이터를 수집하여 Machbase 테이블에 입력하는 에이전트입니다. 이 섹션은 Collector 설정 파라미터의 빠른 참조 레퍼런스입니다.

## 설정 파일 구조

Collector 설정은 JSON 형식 파일로 관리합니다. 기본 구조는 다음과 같습니다.

```json
{
  "name": "collector-name",
  "source": {
    "type": "<소스 타입>",
    ...
  },
  "template": {
    "type": "<템플릿 타입>",
    ...
  },
  "target": {
    "table": "<테이블 이름>",
    ...
  }
}
```

## 하위 섹션

| 섹션 | 설명 |
|------|------|
| [Collector template 사전](./dictionary-collector-template/) | 데이터 파싱 템플릿 설정 (CSV, JSON, 정규식) |
| [Collector source type 사전](./dictionary-collector-source-type/) | 지원 소스 타입과 필수 설정 파라미터 |
| [Collector regex/options 사전](./dictionary-collector-regex-options/) | 정규식 패턴 옵션과 자주 쓰는 패턴 예시 |

## 빠른 참조: 주요 설정 파라미터

| 파라미터 | 위치 | 설명 |
|---------|------|------|
| `name` | 최상위 | Collector 인스턴스 이름 |
| `source.type` | source | 수집 소스 타입 (FILE, TCP, UDP 등) |
| `template.type` | template | 파싱 방식 (CSV, JSON, REGEX 등) |
| `target.table` | target | 데이터를 입력할 Machbase 테이블 이름 |
| `target.server` | target | Machbase 서버 접속 정보 |

Collector 기능의 개념과 운영 가이드는 [데이터 수집](/dbms/operations-configuration-recovery/collector/) 섹션을 참고하십시오.
