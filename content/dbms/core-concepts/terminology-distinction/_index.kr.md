---
type: docs
title: '2.5 용어 구분'
weight: 50
toc: true
---
이 페이지는 이름이나 목적이 비슷해 혼동하기 쉬운 기능의 선택 기준만 비교합니다. 실행 예제와
옵션은 연결된 상세 문서를 참고하십시오.

- **[Retention vs DELETE·TRUNCATE](#retention-vs-delete-truncate)** -- 자동 보존 정책과 일회성 삭제
- **[Backup vs Restore vs Mount](#backup-vs-restore-mount)** -- 복사, 복구, 읽기 전용 조회
- **[파일 입출력 도구](#machloader-vs-csvimport-csvexport-tagmetaimport)** -- 범용 적재와 간편 래퍼, TAG 메타데이터 도구
- **[LOAD DATA INFILE vs machloader](#load-data-infile-vs-machloader)** -- 서버 파일과 클라이언트 파일
- **[SDK Append vs SQL INSERT vs Collector](#ingestion-sdk-append-vs-sql-collector)** -- 지속 입력 경로

<a id="retention-vs-delete-truncate"></a>

## Retention vs DELETE·TRUNCATE

| 항목 | Retention Policy | DELETE | TRUNCATE |
| --- | --- | --- | --- |
| 실행 성격 | 설정 후 주기적으로 동작 | 실행할 때 한 번 동작 | 실행할 때 한 번 동작 |
| 범위 | 보관 기간을 넘긴 데이터 | 테이블 유형이 허용하는 조건 범위 | 지원 테이블의 전체 데이터 |
| 주된 목적 | 지속적인 저장 공간 관리 | 특정 데이터 정정·제거 | 테이블 초기화 |

테이블 유형마다 `DELETE`와 `TRUNCATE` 지원 범위가 다릅니다. 운영 SQL을 작성하기 전에
[데이터 보존 정책](/dbms/operations-configuration-recovery/policy-data-retention/)과 각 테이블의
DML 문서를 확인하십시오.

<a id="backup-vs-restore-mount"></a>

## Backup vs Restore vs Mount

| 항목 | Backup | Restore | Mount |
| --- | --- | --- | --- |
| 목적 | 복구용 복사본 생성 | 백업으로 인스턴스 복구 | 백업을 읽기 전용으로 조회 |
| 일반적인 서버 상태 | 실행 중 | 중지 | 실행 중 |
| 운영 데이터 변경 | 없음 | 있음 | 없음 |

지원 범위와 절차는 Edition 및 백업 종류에 따라 달라질 수 있습니다. 실제 명령은
[백업·복원·마운트](/dbms/operations-configuration-recovery/backup-restore-mount/)를 기준으로
작성하십시오.

<a id="machloader-vs-csvimport-csvexport-tagmetaimport"></a>

## machloader vs csvimport·csvexport vs tagmetaimport

| 도구 | 역할 | 선택 기준 |
| --- | --- | --- |
| `machloader` | 테이블 데이터 적재·반출 | 형식, 컬럼 매핑과 오류 파일을 세밀하게 제어 |
| `csvimport` / `csvexport` | CSV 입출력 래퍼 | 단순한 CSV 작업을 짧은 명령으로 수행 |
| `tagmetaimport` | TAG 메타데이터 적재 | 태그 이름과 메타데이터를 일괄 등록·변경 |

`tagmetaimport`는 TAG의 시계열 측정값을 적재하는 도구가 아닙니다. 지원 테이블, 파일 형식과
옵션은 [데이터 입력·적재·반출](/dbms/development-tools-integration/data-input-load-export/) 및
[명령행 도구 사전](/dbms/reference/command-line-tools/)을 참고하십시오.

<a id="load-data-infile-vs-machloader"></a>

## LOAD DATA INFILE vs machloader

| 항목 | `LOAD DATA INFILE` | `machloader` |
| --- | --- | --- |
| 파일을 읽는 주체 | Machbase 서버 | 명령을 실행한 클라이언트 |
| 파일 위치 | 서버가 접근할 수 있는 경로 | 클라이언트가 접근할 수 있는 경로 |
| 실행 인터페이스 | SQL | 명령행 |
| 적합한 경우 | 서버에 배치된 파일을 SQL 작업으로 적재 | 클라이언트 파일을 전송하고 오류 행을 분리 |

파일 위치와 권한을 먼저 확인한 뒤 선택하십시오. 전체 구문과 재현 가능한 예제는
[데이터 입력·적재·반출](/dbms/development-tools-integration/data-input-load-export/)에 있습니다.

<a id="ingestion-sdk-append-vs-sql-collector"></a>

## SDK Append vs SQL INSERT vs Collector

| 경로 | 특성 | 적합한 경우 |
| --- | --- | --- |
| SDK Append | 여러 행을 Append API로 전송 | 지속적인 고처리량 시계열 입력 |
| SQL `INSERT` | SQL 파싱과 실행을 거쳐 행 입력 | 저빈도 입력, 기능 확인, 기존 SQL 연동 |
| Collector | `.tpl`과 `.rgx` 설정으로 파일 수집 | 로컬 또는 SFTP 파일을 코드 없이 수집 |

현재 Collector의 공개 소스 유형은 `FILE`과 `SFTP`입니다. 템플릿에 남아 있는 호환 키만 보고
TCP, UDP, 소켓 또는 ODBC 수집을 지원한다고 가정하지 마십시오. 설정 형식과 지원 범위는
[Collector 레퍼런스](/dbms/reference/collector/)를 기준으로 확인하십시오.

애플리케이션 입력 경로의 API와 성능 특성은
[데이터 입력 방식 선택](/dbms/development-tools-integration/data-input-load-export/)을 참고하십시오.
