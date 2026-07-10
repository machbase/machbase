---
title: '9.7 운영과 데이터 생명주기'
weight: 70
toc: true
---
LOOKUP 테이블의 백업·복구와 데이터 영속성을 다룬다.

LOOKUP 테이블은 디스크에 영속 저장되는 참조 데이터 테이블이다. 운영 중 값이 바뀔 수 있으므로 변경 절차, 백업, 복구, 조회 반영 시점을 함께 관리한다.

<a id="lifecycle-lookup-data"></a>

## 데이터 생명주기

LOOKUP 데이터는 생성, 입력, 갱신, 참조, 백업, 복구의 흐름으로 관리한다.

```
테이블 생성
  └── 기준 데이터 입력
        └── TAG/LOG/RDB 조회에서 JOIN 또는 참조
              └── 운영 중 UPDATE/DELETE
                    └── 백업 / 복구 / 마운트
```

기준 데이터는 원본 이벤트보다 작지만, 조회 결과 해석에 직접 영향을 준다. 따라서 변경 전후의 값과 적용 시점을 기록하는 운영 절차를 둔다.

<a id="operate-lookup-change"></a>

## 기준 데이터 변경 절차

운영 중 LOOKUP 데이터를 변경할 때는 다음 순서로 진행한다.

1. 변경 대상 행을 조회한다.
2. 영향 범위를 확인한다.
3. UPDATE 또는 DELETE를 실행한다.
4. 필요한 경우 `EXEC TABLE_REFRESH(table_name)`을 실행한다.
5. 대표 조회 쿼리로 반영 여부를 확인한다.

```sql
SELECT *
FROM sensor_master
WHERE sensor_id = 'TEMP-01';

UPDATE sensor_master
SET status = 'INACTIVE',
    updated_at = NOW
WHERE sensor_id = 'TEMP-01';

EXEC TABLE_REFRESH(sensor_master);
```

일괄 변경은 반드시 대상 건수를 먼저 확인한다.

```sql
SELECT COUNT(*)
FROM sensor_master
WHERE site = 'SEOUL'
  AND status = 'READY';
```


<a id="recovery-support-scope-backup-lookup"></a>

## 백업·복구 지원 범위

LOOKUP 테이블은 디스크에 영속 저장되며 데이터베이스 백업에 포함된다.

## 백업 포함 여부

| 테이블 타입 | 데이터베이스 백업 포함 |
|-----------|-------------------|
| TAG | O |
| LOG | O |
| RDB | O |
| **LOOKUP** | **O** |
| VOLATILE | X (메모리 전용) |

## 백업

```sql
-- LOOKUP 테이블 데이터는 전체 백업에 자동 포함
BACKUP DATABASE INTO DISK = '/backup/machbase_20240101';
```

## 복구

```bash
# 데이터베이스 복원 시 LOOKUP 테이블 데이터도 함께 복원
machadmin -r '/backup/machbase_20240101'
```

## 마운트를 통한 조회

```sql
-- 백업을 마운트하여 LOOKUP 테이블 데이터 조회
MOUNT DATABASE '/backup/machbase_20240101' TO old_db;

SELECT * FROM old_db.country_code;

UMOUNT DATABASE old_db;
```

## 주의사항

- LOOKUP 테이블은 서버 재시작 후에도 데이터가 유지된다.
- VOLATILE 테이블과 달리 데이터 손실 위험이 없다.
- 대용량 LOOKUP 테이블은 백업 시간에 영향을 줄 수 있다.
- LOOKUP 테이블과 VOLATILE 테이블은 메모리 한도 설정의 영향을 받을 수 있으므로 대량 참조 데이터는 규모를 관리한다.

<a id="lifecycle-lookup-monitoring"></a>

## 운영 점검 항목

- 기준 데이터 변경 이력을 별도 로그나 운영 절차로 남긴다.
- 대량 UPDATE/DELETE 전에는 대상 건수를 확인한다.
- 자주 JOIN하는 컬럼에는 인덱스를 검토한다.
- Append 중복 키 처리를 사용하는 경우 `LOOKUP_APPEND_UPDATE_ON_DUPKEY` 설정을 확인한다.
- 백업 복구 후 대표 JOIN 쿼리로 참조 결과를 확인한다.
