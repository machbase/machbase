---
type: docs
title: '13.7 Collector 운영'
weight: 80
toc: true
---

Collector는 로컬 파일 또는 SFTP로 전달된 파일을 읽어 Machbase에 적재합니다. Collector
Manager가 Collector 인스턴스의 생명 주기를 관리하며, `machcollectoradmin`으로 상태를
확인하고 제어합니다. 템플릿 항목은 [Collector 템플릿 사전](/dbms/reference/collector/dictionary-collector-template/)을
참고하십시오.

현재 배포본에서 확인한 `COLLECT_TYPE`은 `FILE`과 `SFTP`입니다.

<a id="start-collectormanager"></a>

## Collector Manager 시작과 종료

Machbase 서버가 준비된 뒤 Collector Manager와 필요한 Collector를 차례로 시작합니다.

```bash
machadmin -e
machcollectoradmin --startup
machcollectoradmin --start-collector=my_collector
```

운영 중인 Collector가 있으면 먼저 중지한 뒤 Manager를 종료합니다.

```bash
machcollectoradmin --stop-collector=all
machcollectoradmin --shutdown
```

Manager의 실행 상태는 Collector 목록과 상태 조회로 확인합니다.

```bash
machcollectoradmin --list
machcollectoradmin --status-collector=all
```

실행 환경에 따라 `MACHBASE_COLLECTOR_HOME`을 설정해야 합니다. 실제 설정 파일과 로그
경로는 설치 패키지의 `conf/machcollector.conf`와 운영 환경 변수를 기준으로 확인하십시오.

<a id="create-delete-start-stop-machcollectoradmin-collector"></a>

## Collector 생성과 생명 주기 관리

검토가 끝난 템플릿으로 Collector를 생성한 뒤 시작합니다.

```bash
machcollectoradmin --create-collector=my_collector --template=/path/to/collector.tpl
machcollectoradmin --start-collector=my_collector
machcollectoradmin --status-collector=my_collector
```

설정 변경이나 장애 조치가 필요하면 해당 Collector만 중지합니다. 삭제는 등록 정보를
제거하므로, 대상 이름과 처리되지 않은 원본 파일이 없는지 확인한 뒤 수행합니다.

```bash
machcollectoradmin --stop-collector=my_collector
machcollectoradmin --drop-collector=my_collector
```

주요 동작 옵션과 현재 배포본의 전체 옵션은
[machcollectoradmin 명령/옵션 사전](/dbms/reference/command-line-tools/dictionary-machcollectoradmin/)에서
확인할 수 있습니다.

<a id="status-check-state-collector"></a>

## Collector 상태 확인

다음 세 가지 증거를 함께 확인합니다.

1. `--status-collector`가 보고하는 실행 상태
2. 일정 시간 동안 처리 건수가 증가하는지 여부
3. Collector 로그의 마지막 성공 시각과 오류

```bash
machcollectoradmin --status-collector=all
machcollectoradmin --status-collector=my_collector
```

상태 이름이나 출력 열은 배포 버전에 따라 달라질 수 있으므로 고정된 출력 형식에 의존하는
파서는 사용하지 마십시오. 자동화에서는 명령 종료 코드와 로그를 함께 판단합니다.

지연을 판정할 때도 일률적인 초 단위 기준보다 소스 파일 도착 주기와 서비스의 허용 지연을
기준으로 삼습니다. 상태를 반복 조회할 때는 시스템에 부담을 주지 않는 간격을 사용하십시오.

<a id="recovery-failure-collector"></a>

## Collector 장애 복구

수집이 멈췄다면 다음 순서로 범위를 좁힙니다.

1. `machadmin -e`로 Machbase 서버 상태를 확인합니다.
2. Collector와 Manager 상태를 확인합니다.
3. 로그에서 최초 오류와 마지막 성공 시점을 찾습니다.
4. 로컬 경로·권한 또는 SFTP 연결을 확인합니다.
5. 원인을 제거한 뒤 해당 Collector만 재시작합니다.
6. 처리 건수와 대상 테이블 데이터가 다시 증가하는지 확인합니다.

```bash
machadmin -e
machcollectoradmin --status-collector=my_collector
machcollectoradmin --stop-collector=my_collector
machcollectoradmin --start-collector=my_collector
machcollectoradmin --status-collector=my_collector
```

재시작 전에는 원본 파일과 처리 완료 파일의 위치를 확인하십시오. 어느 파일과 offset부터
재개하는지는 사용 중인 버전의 로그와 템플릿 설정을 기준으로 판단해야 합니다. 이미 처리한
파일을 입력 위치에 다시 두면 중복 적재될 수 있습니다.

개별 Collector 재시작으로 해결되지 않을 때만 점검 시간에 Manager 재시작을 고려합니다.
Manager 종료는 다른 Collector에도 영향을 주므로 영향 범위와 재시작 순서를 먼저 기록하십시오.
