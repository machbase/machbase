---
type: docs
title: '제한사항 사전'
weight: 120
---

Machbase의 주요 제한 사항을 테이블 유형별, Edition별, 일반 시스템 제한으로 정리합니다. 특정 기능을 사용하기 전에 해당 제한 사항을 먼저 확인하세요.

## TAG 테이블 제한

| 항목 | 제한 내용 |
|------|----------|
| UPDATE 조건 | `WHERE name = '...'` (TAGNAME PK 컬럼) 조건 필수 |
| UPDATE 대상 | SUMMARIZED 속성 컬럼만 가능 |
| UPDATE 불가 컬럼 | `name` (TAGNAME), `time` (BASETIME) |
| DELETE 방식 | 범위 삭제 지원; 개별 행 삭제는 DELETE 정책 설정 필요 |
| Transaction | 미지원 (Append-only 구조, 즉시 커밋) |
| Append 대상 | TAG, LOG 테이블만 가능 |
| ROLLUP 재구축 | `ROLLUP_REBUILD`: Standard Edition만 지원 |

상세 내용은 [TAG data UPDATE 지원표](../tag-data-update/)를 참고하세요.

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

상세 내용은 [LOOKUP SQL/JSON 지원표](../lookup-sql-json/)를 참고하세요.

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
| RDB 테이블 | 미지원 |
| VOLATILE 테이블 | 미지원 |
| MOUNT / UNMOUNT | 미지원 |
| STREAM | 미지원 |
| Custom ROLLUP | 미지원 |
| ROLLUP_REBUILD | 미지원 |
| machadmin -r 복구 | 미지원 |

## SDK 제한

| SDK | 제한 내용 |
|-----|---------|
| Python | Prepared Statement 미지원 (클라이언트 렌더링) |
| Go (database/sql) | Transaction 미지원 |
| Go (native) | Transaction 미지원, AUTH KEY 미지원 |
| Node.js | Transaction 미지원, AUTH KEY 미지원 |
| REST API | Transaction 미지원, Prepared Statement 미지원, AUTH KEY 미지원 |

## 일반 시스템 제한

| 항목 | 제한값 | 비고 |
|------|--------|------|
| 테이블당 최대 컬럼 수 | 2048 | |
| VARCHAR 최대 길이 | 32767 바이트 | |
| 테이블 이름 최대 길이 | 40자 | |
| 컬럼 이름 최대 길이 | 40자 | |
| 동시 접속 세션 수 | 설정값 `MAX_SESSION_COUNT` | 기본값 512 |

## 계획 중인 기능 (Planned)

아래 항목은 현재 미지원이나 향후 업데이트 예정입니다.

| 항목 | 이슈 |
|------|------|
| TAG UPDATE WHERE time BETWEEN | dbms-nfx#3733 |
