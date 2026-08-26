---
type: docs
title: '2.3 주요 기능과 용어 구분'
weight: 30
toc: true
aliases:
  - /dbms/core-concepts/terminology-distinction/
  - /dbms/reference/ai-agent-reference/terminology-disambiguation/
---
Machbase DBMS의 장기 데이터 운영에 필요한 ROLLUP, Retention Policy, Backup·Restore·Mount의
역할과 선택 기준을 설명합니다. 생성 구문과 운영 절차는 각 기능의 상세 문서에서 다룹니다.

- **[ROLLUP 통계의 역할](#role-statistics-rollup)** -- 반복 집계의 조회 비용을 줄이는 방법
- **[Retention Policy의 역할](#role-retention-policy)** -- 기간에 따라 데이터를 자동 정리하는 방법
- **[Backup·Restore·Mount의 관계](#concepts-backup-restore-mount)** -- 보호, 복구, 조회 목적의 구분

<a id="role-statistics-rollup"></a>

## ROLLUP 통계의 역할

TAG 테이블의 장기간 데이터를 매번 원시 행에서 집계하면 조회 범위가 커질수록 처리 비용도
증가합니다. ROLLUP은 지정한 숫자형 `SUMMARIZED` 컬럼의 구간 통계를 미리 계산해 반복 조회에
사용하는 기능입니다.

기본 ROLLUP은 초(SEC), 분(MIN), 시간(HOUR) 계층을 구성합니다. 테이블을 만들 때
`WITH ROLLUP`을 지정하거나, 필요한 주기와 조건에 맞춘 사용자 정의 ROLLUP을 만들 수 있습니다.
생성되는 객체의 이름이나 저장 구조에 의존하지 말고 공개된 ROLLUP SQL로 관리하십시오.

### 선택 기준

| 조회 패턴 | 선택 |
| --- | --- |
| 장기간의 분·시간 단위 통계를 반복 조회 | 기본 ROLLUP 검토 |
| 사용자 정의 주기나 조건이 필요 | 사용자 정의 ROLLUP 검토 |
| 첫 값·마지막 값이 필요 | 확장 ROLLUP 검토 |
| 원시 값 조회가 대부분이거나 집계 빈도가 낮음 | ROLLUP 없이 시작하고 실행 시간을 측정 |

ROLLUP은 원시 데이터를 대신하는 보관 정책이 아닙니다. 원시 데이터의 보관 기간은 Retention
Policy로 별도 설계하고, TAG 데이터를 수정했다면 해당 범위의 ROLLUP 재구성 여부도 확인합니다.

자세한 생성 구문, 조회 함수, 재구성 절차는 [TAG·ROLLUP 활용](/dbms/tag-rollup-usage/)을
참고하십시오.

<a id="role-retention-policy"></a>
<a id="retention-vs-delete-truncate"></a>

## Retention Policy의 역할

Retention Policy는 LOG 또는 TAG 테이블에서 보관 기간을 넘긴 데이터를 정해진 주기로
정리합니다. 데이터가 계속 유입되는 테이블의 저장 공간을 운영자가 반복적인 삭제 작업 없이
관리할 때 사용합니다.

| 요구사항 | 선택 |
| --- | --- |
| 일정 기간이 지난 데이터를 계속 자동 정리 | Retention Policy |
| 잘못 입력한 특정 범위를 즉시 제거 | 테이블 유형이 지원하는 `DELETE` |
| 지원 테이블의 전체 데이터를 비움 | `TRUNCATE TABLE` |

Retention은 적용 즉시 모든 오래된 데이터가 사라진다는 의미가 아닙니다. 정책의 실행 주기,
대상 테이블 지원 범위와 실제 삭제 상태를 함께 확인해야 합니다. LOOKUP, VOLATILE,
TRANSACTION 테이블의 수명 관리는 해당 테이블이 지원하는 명시적 DML로 처리합니다.

정책 생성·적용·해제 구문과 운영 점검은
[데이터 보존 정책](/dbms/operations-configuration-recovery/policy-data-retention/)을
참고하십시오.

<a id="concepts-backup-restore-mount"></a>
<a id="backup-vs-restore-mount"></a>

## Backup·Restore·Mount의 관계

세 기능은 모두 백업 데이터와 관련되지만 결과가 다릅니다.

| 기능 | 목적 | 운영 서버 | 결과 |
| --- | --- | --- | --- |
| Backup | 복구에 사용할 복사본 생성 | 실행 중 수행 가능 | 별도 경로에 백업 생성 |
| Restore | 백업으로 인스턴스 복구 | 오프라인 절차 필요 | 운영 데이터베이스를 복구 |
| Mount | 백업 내용을 읽기 전용으로 확인 | 실행 중 수행 가능 | 백업을 별도 이름으로 조회 |

Backup은 복구 가능성을 보장하지 않습니다. 정기적으로 Mount 조회 또는 격리 환경의 Restore로
백업을 검증하고, 백업 경로의 권한과 보존 주기를 함께 관리하십시오. Mount는 백업을 운영
데이터로 되돌리지 않으며, 마운트한 데이터에는 쓸 수 없습니다.

명령, 권한, Edition별 지원 범위와 복구 순서는
[백업·복원·마운트](/dbms/operations-configuration-recovery/backup-restore-mount/)를
참고하십시오. 여러 logical database를 운용한다면
[다중 데이터베이스 운영](/dbms/operations-configuration-recovery/multi-database/)도 함께
확인하십시오.

<a id="machloader-vs-csvimport-csvexport-tagmetaimport"></a>
<a id="load-data-infile-vs-machloader"></a>
<a id="ingestion-sdk-append-vs-sql-collector"></a>

## 입력 경로 비교

SDK, loader와 Collector의 선택 기준은
[데이터 입력과 반출](/dbms/development-tools-integration/data-input-load-export/#machloader-vs-csvimport-csvexport-tagmetaimport)로
이동했습니다.
