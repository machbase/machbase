---
type: docs
title: '18.6.11 제한사항 사전'
weight: 120
toc: true
---

Machbase의 주요 제한 사항을 테이블 유형별, Edition별, 일반 시스템 제한으로 정리합니다. 특정 기능을 사용하기 전에 해당 제한 사항을 먼저 확인하십시오.

## TAG 테이블 제한

| 항목 | 제한 내용 |
|------|----------|
| UPDATE 에디션 | Standard Edition만 지원; Cluster Edition은 미지원 |
| UPDATE 조건 | 태그 선택 조건(`name =`, `name IN`, `name LIKE`)과 하나 이상의 BASETIME 조건 필수 |
| UPDATE 대상 | 실제 데이터 컬럼 가능. 메타데이터는 `UPDATE ... METADATA` 사용 |
| UPDATE 불가 컬럼 | `name` (TAGNAME), `time` (BASETIME) |
| UPDATE SET 우변 | 기존 행 컬럼 참조 불가; 상수·bind·column-free 식 사용 |
| DELETE 방식 | 범위 삭제 지원; 개별 행 삭제는 DELETE 정책 설정 필요 |
| Transaction | 미지원 (Append-only 구조, 즉시 커밋) |
| Append 대상 | TAG/LOG 고속 경로와 TRANSACTION client batch/stream 경로 지원 |
| ROLLUP 재구축 | `ROLLUP_REBUILD`: Standard Edition만 지원 |

상세 내용은 [TAG data UPDATE 지원표](../tag-data-update/)를 참고하십시오.

## LOG 테이블 제한

| 항목 | 제한 내용 |
|------|----------|
| UPDATE | 미지원 |
| Transaction | 미지원 (Append-only 구조) |
| 삭제 방식 | DELETE 정책(RETENTION) 기반; `DELETE FROM` 지원 |
| 텍스트 검색 | KEYWORD INDEX 생성 후 사용 가능 |

## LOOKUP 테이블 제한

| 항목 | 제한 내용 |
|------|----------|
| UPDATE/DELETE | PK 기반 권장; 비-PK 조건은 예상치 못한 범위 적용 가능 |
| JSON 타입 컬럼 | 지원; primary key로는 사용할 수 없음 |
| JSON path query | 지원; JSON path별 전용 인덱스는 미지원 |
| JSON PK | 미지원 |
| Append API | 지원, 중복 키 처리 정책(`LOOKUP_APPEND_UPDATE_ON_DUPKEY`)에 따라 중복 키 처리 방식이 달라짐 |

상세 내용은 [LOOKUP SQL/JSON 지원표](../lookup-sql-json/)를 참고하십시오.

## VOLATILE 테이블 제한

| 항목 | 제한 내용 |
|------|----------|
| 지속성 | 서버 재시작 시 데이터 손실 (메모리 기반) |
| 백업 | 미지원 |
| Cluster Edition | 미지원 |
| Append API | 미지원 (일반 INSERT SQL 사용) |

## Cluster Edition 제한

| 기능 | 제한 내용 |
|------|----------|
| TRANSACTION 테이블 | 미지원 |
| VOLATILE 테이블 | 미지원 |
| MOUNT / UMOUNT | 미지원 |
| Custom ROLLUP | 미지원 |
| ROLLUP_REBUILD | 미지원 |
| machadmin -r 복구 | 미지원 |

## SDK 제한

ROWID와 generated ROWID는 Standard Edition에서만 지원합니다. generated ROWID는 단일
`INSERT ... VALUES`에만 제공되며 batch, Append, loader, `INSERT ... SELECT`, UPSERT에서는
반환하지 않습니다. SDK별 반환 API는
[ROWID와 INSERT 결과 ID](/dbms/application-integration/rowid-generated-id/)를 참고하십시오.

| SDK | 제한 내용 |
|-----|---------|
| Python | Transaction API 미지원. prepared cursor는 cursor당 server statement 하나만 유지 |
| Go (database/sql) | 기본 isolation level의 `Begin`/`BeginTx`, `Commit`, `Rollback` 지원 |
| Go (native) | 전용 Transaction 편의 API 없음. 같은 연결에서 트랜잭션 SQL 직접 실행 가능 |
| .NET | Transaction API, AUTH KEY와 서버 Prepared Statement 미지원. 이름 컬렉션은 client-side 렌더링 |
| Node.js | Transaction 편의 API와 AUTH KEY 미지원. 같은 연결에서 SQL 직접 실행 가능 |

## 일반 시스템 제한

| 항목 | 제한값 | 비고 |
|------|--------|------|
| 테이블당 최대 컬럼 수 | 2048 | |
| VARCHAR 최대 길이 | 32767 바이트 | |
| 테이블 이름 최대 길이 | 40자 | |
| 컬럼 이름 최대 길이 | 40자 | |
| 동시 접속 세션 수 | 설정값 `MAX_SESSION_COUNT` | 현재 값은 `V$PROPERTY`에서 확인 |
