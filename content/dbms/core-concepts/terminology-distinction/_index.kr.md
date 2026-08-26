---
type: docs
title: '2.5 용어 구분'
weight: 50
toc: true
aliases:
  - /dbms/reference/ai-agent-reference/terminology-disambiguation/
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
<a id="load-data-infile-vs-machloader"></a>
<a id="ingestion-sdk-append-vs-sql-collector"></a>

## 입력 경로 비교

입력 API, loader와 Collector의 선택 기준은 [데이터 입력과 반출](../../development-tools-integration/data-input-load-export/#machloader-vs-csvimport-csvexport-tagmetaimport)로 이동했습니다. 이 페이지에는 제품 동작을 이해하는 데 필요한 운영 개념 비교만 유지합니다.
