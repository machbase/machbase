---
type: docs
title: '16.7 Collector 파일 적재'
weight: 70
toc: true
---

Collector 설정 항목과 파싱 규칙은
[Collector 입력](/dbms/log-table-usage/collector-ingestion/)과
[Collector 템플릿 사전](/dbms/reference/collector/dictionary-collector-template/)에서 관리합니다.
이 시나리오는 이미 검토한 템플릿을 운영에 투입하는 절차만 다룹니다.

## 1. 입력 계약 확인

- FILE 또는 SFTP 중 실제 `COLLECT_TYPE`
- 원본 파일의 인코딩, 구분자, 시간 형식, 열 개수
- 대상 테이블의 열 순서와 데이터 타입
- 처리 완료·실패 파일의 이동 경로와 재처리 정책
- 중복 입력을 식별할 방법

샘플 파일 한 건을 파서 규칙에 통과시킨 뒤 대상 테이블과 동일한 형태인지 확인합니다.

## 2. Collector 등록

운영 서버가 아닌 검증 환경에서 먼저 등록합니다.

```bash
machcollectoradmin --create-collector=sc16_file \
  --template=/path/to/sc16_file.tpl
machcollectoradmin --status-collector=sc16_file
```

등록 전에 `MACHBASE_COLLECTOR_HOME`과 `conf/machcollector.conf`가 실제 배포에 맞게 준비되어
있어야 합니다.

## 3. 시작과 결과 검증

```bash
machadmin -e
machcollectoradmin --start-collector=sc16_file
machcollectoradmin --status-collector=sc16_file
```

처리 건수만 보지 말고 대상 테이블에서 파일의 최소·최대 시각, 행 수, 대표 값을 조회합니다.
실패 파일과 Collector 로그에 오류가 없는지도 확인합니다.

## 4. 중지와 재처리

```bash
machcollectoradmin --stop-collector=sc16_file
```

재처리 전에 Collector 로그에서 마지막으로 완료한 파일과 offset을 확인합니다. 이미 처리한
파일을 원본 위치에 다시 두면 중복 적재될 수 있습니다. 삭제가 필요하면 중지 상태와 대상
이름을 다시 확인한 뒤 `--drop-collector`를 사용합니다.

장애 대응은 [Collector 운영](/dbms/operations-configuration-recovery/collector/)을 따릅니다.
