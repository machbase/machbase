---
title: '9.7 운영과 데이터 생명주기'
weight: 70
toc: true
---
LOOKUP 테이블의 백업·복구와 데이터 영속성을 다룹니다.

LOOKUP 테이블은 디스크에 영속 저장되는 참조 데이터 테이블입니다. 운영 중 값이 바뀔 수 있으므로 변경 절차, 백업, 복구, 조회 반영 시점을 함께 관리합니다.

영속 저장과 조회 시 데이터 위치는 구분해야 합니다. 서버가 기동되면 영속 저장본의 모든
LOOKUP 행을 메모리 테이블에 복원하고 `PRIMARY KEY`와 보조 인덱스를 구성합니다. 서비스 중
SQL 조회는 이 메모리 구조를 사용합니다.

<a id="lifecycle-lookup-data"></a>

## 데이터 생명주기

LOOKUP 데이터는 생성, 입력, 갱신, 참조, 백업, 복구의 흐름으로 관리합니다.

```
테이블 생성
  └── 기준 데이터 입력
        └── TAG/LOG/RDB 조회에서 JOIN 또는 참조
              └── 운영 중 UPDATE/DELETE
                    └── 백업 / 복구 / 마운트
```

기준 데이터는 원본 이벤트보다 작지만, 조회 결과 해석에 직접 영향을 줍니다. 따라서 변경 전후의 값과 적용 시점을 기록하는 운영 절차를 둡니다.

<a id="operate-lookup-change"></a>

## 기준 데이터 변경 절차

운영 중 LOOKUP 데이터를 변경할 때는 다음 순서로 진행합니다.

1. 변경 대상 행을 조회합니다.
2. 영향 범위를 확인합니다.
3. UPDATE 또는 DELETE를 실행합니다.
4. 필요한 경우 `EXEC TABLE_REFRESH(table_name)`을 실행합니다.
5. 대표 조회 쿼리로 반영 여부를 확인합니다.

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

일괄 변경은 반드시 대상 건수를 먼저 확인합니다.

```sql
SELECT COUNT(*)
FROM sensor_master
WHERE site = 'SEOUL'
  AND status = 'READY';
```


<a id="recovery-support-scope-backup-lookup"></a>

## 백업·복구 지원 범위

LOOKUP 테이블은 디스크에 영속 저장되며 데이터베이스 백업에 포함됩니다.

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

- LOOKUP 테이블은 서버 재시작 후에도 데이터가 유지됩니다.
- 서버 기동 시 모든 LOOKUP 행과 인덱스를 메모리에 구성하므로 데이터 규모에 따라 기동 시간과
  메모리 사용량이 증가합니다.
- VOLATILE 테이블과 달리 데이터 손실 위험이 없습니다.
- 대용량 LOOKUP 테이블은 백업 시간에 영향을 줄 수 있습니다.
- LOOKUP 테이블과 VOLATILE 테이블은 메모리 한도 설정의 영향을 받습니다. LOOKUP에는 서버
  메모리에 상주시킬 수 있는 규모의 참조 데이터를 저장합니다.

<a id="lifecycle-lookup-monitoring"></a>

## 운영 점검 항목

- 기준 데이터 변경 이력을 별도 로그나 운영 절차로 남깁니다.
- 대량 UPDATE/DELETE 전에는 대상 건수를 확인합니다.
- 자주 JOIN하는 컬럼에는 인덱스를 검토합니다.
- 서버 기동 시간과 LOOKUP 행·인덱스의 메모리 사용량을 실제 데이터 규모로 점검합니다.
- Append 중복 키 처리를 사용하는 경우 `LOOKUP_APPEND_UPDATE_ON_DUPKEY` 설정을 확인합니다.
- 백업 복구 후 대표 JOIN 쿼리로 참조 결과를 확인합니다.
