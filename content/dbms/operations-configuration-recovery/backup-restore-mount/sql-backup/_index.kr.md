---
type: docs
title: 'SQL BACKUP 범위'
weight: 60
---

SQL `BACKUP` 문의 지원 범위를 에디션, 저장 방식, 테이블 타입에 따라 정리합니다.

## 에디션별 지원 범위

| 기능 | Standard Edition | Cluster Edition |
|------|:----------------:|:---------------:|
| `BACKUP DATABASE` | O | O |
| `BACKUP TABLE` | O | O |
| `MOUNT DATABASE` | O | 제한적 (거부될 수 있음) |
| `UNMOUNT DATABASE` | O | 제한적 (거부될 수 있음) |
| RDB 테이블 백업 | O | X |

> Cluster Edition에서 `MOUNT` 및 `UNMOUNT` 문은 거부될 수 있습니다. 클러스터 환경에서는 각 노드의 데이터를 개별적으로 관리하므로 마운트 방식의 조회가 제한됩니다.

## 저장 방식 비교: DISK vs IBFILE

| 항목 | DISK | IBFILE |
|------|:----:|:------:|
| 저장 형태 | 디렉터리 | 단일 `.ibf` 파일 |
| 마운트 지원 | O | X |
| 증분 백업 지원 | O | X |
| 이식성 | 낮음 | 높음 |
| 용도 | 운영 백업, 복구 | 단기 이전, 소규모 보관 |

## 테이블 타입별 BACKUP 지원

| 테이블 타입 | BACKUP DATABASE | BACKUP TABLE | 비고 |
|------------|:---------------:|:------------:|------|
| LOG 테이블 | O | O | |
| TAG 테이블 | O | O | 기간 복원(machadmin -r) 제한 |
| LOOKUP 테이블 | O | O | |
| VOLATILE 테이블 | X | X | 메모리 기반, 백업 불가 |
| RDB 테이블 | △ | △ | Standard Edition 전용 |

## BACKUP DATABASE 문법 전체 구조

```sql
BACKUP [ DATABASE | TABLE table_name ]
  [ AFTER 'previous_backup_path' ]
  [ FROM start_time TO end_time ]
  INTO { DISK = 'directory_path' | IBFILE = 'file_path' };
```

## 백업 권한

일반 사용자가 `BACKUP DATABASE`를 실행하려면 SYS 사용자가 권한을 부여해야 합니다.

```sql
-- 백업 권한 부여
GRANT BACKUP ON machbasedb TO user_name;

-- 권한 회수
REVOKE BACKUP ON machbasedb FROM user_name;
```

권한 관리에 대한 자세한 내용은 [사용자 관리](../../../../../reference/sql-reference/user-manage/) 섹션을 참고하세요.

## 백업 진행 상태 확인

백업이 실행 중인 동안 별도 세션에서 시스템 뷰를 통해 진행 상태를 확인할 수 있습니다.

```sql
-- 현재 실행 중인 세션 확인
SELECT * FROM v$session WHERE query LIKE '%BACKUP%';
```
