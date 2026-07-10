---
title: '6.14 ROLLUP 삭제와 부분 재구성'
weight: 130
toc: true
---

<a id="differences-rollup-delete-partial-rebuild"></a>

## ROLLUP 삭제·부분 재구성 차이

이상 데이터 보정이나 원본 데이터 재적재 후에는 기존 ROLLUP 집계도 갱신해야 합니다. DROP 후 재생성과 부분 Rebuild 중 상황에 맞는 방법을 선택합니다.

### DROP ROLLUP vs Rebuild

| 항목 | DROP + 재생성 | Rollup Rebuild |
|------|--------------|----------------|
| 대상 범위 | 전체 ROLLUP 삭제 | 특정 시간 범위만 재집계 |
| 다운타임 | 재생성 + 재집계 시간 필요 | 없음 (운영 중 부분 갱신) |
| 적용 대상 | 기본 ROLLUP (ON/FROM) | 기본 ROLLUP (ON/FROM) |
| Custom Rollup | 가능 (전체 재생성) | 불가 (수동 처리 필요) |
| 사용 시점 | 구조 변경, 전체 재적재 | 일부 구간 데이터 수정 |

### DROP 후 재생성 (전체 재구성)

```sql
-- 1. 의존 순서 역순으로 삭제
DROP ROLLUP _tag_ru_1h;
DROP ROLLUP _tag_ru_1m;
DROP ROLLUP _tag_ru_1s;

-- 2. 재생성
CREATE ROLLUP _tag_ru_1s ON tag(value) INTERVAL 1 SEC;
CREATE ROLLUP _tag_ru_1m FROM _tag_ru_1s INTERVAL 1 MIN;
CREATE ROLLUP _tag_ru_1h FROM _tag_ru_1m INTERVAL 1 HOUR;

-- 3. 강제 집계 (과거 데이터 전체 재처리)
ALTER ROLLUP _tag_ru_1s FORCE;
ALTER ROLLUP _tag_ru_1m FORCE;
ALTER ROLLUP _tag_ru_1h FORCE;
```

### Rollup Rebuild (부분 재구성)

원본 TAG 데이터를 수정하거나 삭제·재적재한 경우, 해당 시간 범위의 ROLLUP만 다시 계산합니다.

```sql
-- 특정 기간의 롤업 재계산
EXEC ROLLUP_REBUILD(tag, 'TEMP-01',
                    TO_DATE('2024-01-01 00:00:00'),
                    TO_DATE('2024-01-02 00:00:00'));
```

> Rollup Rebuild는 Built-in ROLLUP(ON/FROM 방식)에서만 지원됩니다. Custom Rollup은 대상 테이블을 직접 관리해야 합니다.

### Custom Rollup 데이터 수정

Custom Rollup의 집계 결과를 수정해야 하는 경우:

```sql
-- 1. 해당 기간의 집계 결과 삭제
DELETE FROM stock_rollup_1m
WHERE time BETWEEN '2024-01-15 09:00:00' AND '2024-01-15 18:00:00'
  AND _arrival_time BEFORE TO_DATE('2024-01-16');

-- 2. Custom Rollup 강제 실행으로 재적재
ALTER ROLLUP rollup_stock_1m FORCE;
```

### 선택 가이드

- **특정 기간만 데이터 오류**: Rollup Rebuild 사용
- **ROLLUP 설정 변경 (주기, 컬럼 등)**: DROP + 재생성
- **전체 데이터 재적재**: DROP + 재생성 + FORCE
- **Custom Rollup 부분 수정**: 대상 테이블 직접 삭제 후 FORCE
