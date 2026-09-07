---
title: '8. TRANSACTION 테이블 활용'
weight: 80
toc: true
---

원본 로그를 쌓는 일과 주문 상태·재고·장비 정보를 바꾸는 일은 성격이 다릅니다.
상태를 변경하는 업무에서는 “몇 행이 바뀌었는가?”, “중간에 실패하면 어디까지 되돌리는가?”,
“다른 연결이 동시에 수정하면 어떻게 되는가?”까지 확인해야 합니다.

TRANSACTION 테이블은 이런 관계형 조회와 변경을 위한 Standard Edition 전용 테이블입니다.
이 장에서는 작은 표본으로 결과를 확인하면서 스키마, 갱신, 트랜잭션, 동시 접근과 복구를
연결해 봅니다. 내부에 SQLite 저장소를 사용하지만 공개 문법과 지원 범위는 Machbase SQL을
기준으로 해야 합니다. SQLite나 다른 RDBMS의 기능을 모두 그대로 사용할 수 있는 것은 아닙니다.

<a id="필요한-작업부터-찾아보세요"></a>

## 이 장의 구성

| 절 | 확인할 내용 |
|---|---|
| [8.1 개요와 사용 기준](./overview-use-criteria/) | LOG·TAG·LOOKUP과의 역할 구분 |
| [8.2 테이블 구조와 스키마](./table-structure-schema/) | 식별자·업무 키·타입·제약 설계 |
| [8.3 생성, 변경, 삭제](./create-alter-drop/) | DDL 실행과 기존 데이터 확인 |
| [8.4 데이터 입력과 변경](./data-input-mutation/) | 조건부 갱신·삭제·복사·Append |
| [8.5 조회와 분석](./query-analysis/) | 필터·정렬·집계·JSON 조회 |
| [8.6 인덱스와 성능](./index-performance/) | PK·UNIQUE·복합·JSON path 인덱스 |
| [8.7 운영과 데이터 생명주기](./operations-lifecycle/) | 배치 정리와 운영 확인 기준 |
| [8.8 제약, 오류, 문제 해결](./constraints-errors-troubleshooting/) | 증상별 확인과 재시도 판단 |
| [8.9 트랜잭션](./transaction/) | 문장 실패·ROLLBACK·커밋 보장 범위 |
| [8.10 잠금, 충돌, busy timeout](./locking-conflict-timeout/) | 두 연결의 충돌과 스냅샷 재시도 |
| [8.11 JOIN과 관계형 조회 설계](./join-relational-query/) | 조인으로 늘거나 빠지는 행 확인 |
| [8.12 백업, 복원, 마운트](./backup-restore-mount/) | 백업 시점의 데이터를 실제로 검증 |
| [8.13 INSERT ON DUPLICATE KEY UPDATE](./insert-on-duplicate-key-update/) | 삽입·갱신 분기와 중복 처리 |

자동 번호의 공통 문법은
[AUTO_INCREMENT](/dbms/reference/sql/syntax-dictionary-sql/auto-increment-syntax/)에 있습니다.

<a id="실습-환경과-실행-단위를-먼저-맞춥니다"></a>

## 실습 환경과 실행 단위

SQL 실습은 DBMS 8.7 Standard Edition의 검증 환경을 기준으로 합니다.
각 절에서 `ch8_` 접두사의 객체를 준비하고 정리하므로 다른 절의 실행 결과에 의존하지
않습니다. 테이블·인덱스 생성 권한이 필요하며, 백업 실습에는 별도의 권한과 서버 경로가
필요합니다.

BEGIN부터 COMMIT·ROLLBACK까지는 같은 연결에서 실행하세요.
두 세션 실습은 지정한 A·B 순서를 지켜야 합니다. 의도적으로 실패하는 SQL은 정상 흐름과
분리해 두었습니다. 실습을 다시 실행하기 전에는 정리 SQL까지 끝냈는지 확인하세요.

주의: 테이블 이름에 TRANSACTION이 들어간다고 모든 작업과 모든 장애가 한 번에
되돌려지는 것은 아닙니다. DDL, 다른 타입의 쓰기, 여러 테이블의 장애 시 커밋 경계는
[8.9 트랜잭션](./transaction/)에서 먼저 확인하세요.
