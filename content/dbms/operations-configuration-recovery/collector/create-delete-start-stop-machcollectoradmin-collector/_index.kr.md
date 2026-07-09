---
type: docs
title: '13.5.2 machcollectoradmin으로 Collector 생성/시작/중지/삭제'
weight: 20
---

`machcollectoradmin`은 Collector 인스턴스를 생성·시작·중지·삭제하는 CLI 도구입니다. Collector 이름은 각 동작 옵션의 값으로 지정합니다.

## Collector 생성

```bash
machcollectoradmin --create-collector=my_collector --template=collector_config.xml
```

| 옵션 | 설명 |
|------|------|
| `--create-collector=<이름>` | Collector 인스턴스 생성 동작 |
| `--template=<파일>` | Collector 설정 템플릿 파일 경로 |

설정 파일은 수집 소스 유형, 연결 정보, 대상 Machbase 테이블, 버퍼 크기 등을 정의합니다. 생성된 Collector 인스턴스는 STOPPED 상태로 등록됩니다.

## Collector 시작

```bash
machcollectoradmin --start-collector=my_collector
```

STOPPED 상태의 Collector를 RUNNING 상태로 전환합니다. 시작 후 설정 파일에 정의된 소스에서 데이터 수집을 시작합니다.

## Collector 중지

```bash
machcollectoradmin --stop-collector=my_collector
```

RUNNING 상태의 Collector를 안전하게 중지합니다. 현재 처리 중인 배치가 완료된 후 종료되므로, 데이터 유실 없이 중지할 수 있습니다.

## Collector 재시작

```bash
machcollectoradmin --stop-collector=my_collector
machcollectoradmin --start-collector=my_collector
```

설정 변경 적용이나 장애 복구 시 재시작이 필요합니다. machcollectoradmin에는 별도의 restart 동작이 없으므로 stop 후 start를 순서대로 실행합니다.

## Collector 삭제

```bash
machcollectoradmin --drop-collector=my_collector
```

Collector 인스턴스 등록 정보를 삭제합니다. 삭제하려면 먼저 Collector가 STOPPED 상태여야 합니다. RUNNING 상태에서 삭제를 시도하면 오류가 발생합니다.

```bash
# 실행 중인 경우 먼저 중지 후 삭제
machcollectoradmin --stop-collector=my_collector
machcollectoradmin --drop-collector=my_collector
```

## 설정 변경

Collector 설정을 변경하려면 삭제 후 새 설정으로 다시 생성하거나, 설정 파일을 수정한 뒤 재시작합니다.

```bash
# 설정 파일 수정 후 재시작
machcollectoradmin --stop-collector=my_collector
machcollectoradmin --start-collector=my_collector
```

설정 파일 경로는 생성 시 등록된 경로를 사용합니다. 경로를 변경하려면 삭제 후 새 설정 파일로 재생성해야 합니다.
