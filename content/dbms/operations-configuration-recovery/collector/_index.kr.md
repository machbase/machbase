---
type: docs
title: 'Collector 운영'
weight: 50
---

Collector는 외부 데이터 소스에서 Machbase로 데이터를 수집하는 컴포넌트입니다. 파일, 메시지 큐, 네트워크 스트림 등 다양한 소스에서 데이터를 읽어 Machbase 테이블에 실시간으로 적재합니다.

## Collector 아키텍처

```
[외부 데이터 소스]  →  [Collector 인스턴스]  →  [collectormanager]  →  [Machbase]
   파일/소켓/MQ           수집·변환·버퍼링            프로세스 관리         저장
```

- **collectormanager**: 여러 Collector 인스턴스를 관리하는 데몬 프로세스입니다. Machbase 서버와 독립된 별도 프로세스로 동작합니다.
- **Collector 인스턴스**: 각 데이터 소스별로 생성·관리됩니다. 하나의 collectormanager 아래 여러 인스턴스를 동시에 실행할 수 있습니다.
- **machcollectoradmin**: Collector 인스턴스를 생성·시작·중지·삭제하는 CLI 도구입니다.

## 이 섹션의 구성

| 주제 | 내용 |
|------|------|
| [collectormanager 시작과 종료](./start-collectormanager/) | collectormanager 데몬 기동·정지 절차 |
| [Collector 생성/시작/중지/삭제](./create-delete-start-stop-machcollectoradmin-collector/) | machcollectoradmin으로 인스턴스 관리 |
| [Collector 상태 확인](./status-check-state-collector/) | 목록 조회, 상태 확인, 로그 분석 |
| [Collector 장애 복구](./recovery-failure-collector/) | 수집 중단 원인 파악과 복구 절차 |

## 운영 시작 순서

Collector를 운영하려면 반드시 다음 순서를 따릅니다.

1. Machbase 서버 기동 (`machadmin -u`)
2. collectormanager 기동 (`collectormanager start`)
3. 개별 Collector 인스턴스 시작 (`machcollectoradmin -a start -n <이름>`)

종료 시에는 역순으로 진행합니다.
