---
type: docs
title: '17.1.1.18 ROLLUP_REBUILD syntax'
weight: 180
toc: true
---

`ROLLUP_REBUILD`는 TAG 테이블의 원본 데이터가 수정된 경우, 지정한 시간 범위의 ROLLUP 집계를 재계산하는 명령입니다.

> Standard Edition 전용입니다. Cluster Edition에서는 지원되지 않습니다.

## 문법

```sql
EXEC ROLLUP_REBUILD(table_name, tag_name, start_time, end_time)
```

## 매개변수

| 매개변수 | 타입 | 설명 |
|----------|------|------|
| `table_name` | identifier | 대상 TAG 테이블 이름 |
| `tag_name` | 문자열 | 재계산할 tag 이름 |
| `start_time` | DATETIME 표현식 | 재계산 시작 시각 (inclusive) |
| `end_time` | DATETIME 표현식 | 재계산 종료 시각 (inclusive) |

## 예시

```sql
-- 특정 시간 범위의 ROLLUP 재계산
EXEC ROLLUP_REBUILD(
    sensor_tag,
    'TEMP-01',
    TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'),
    TO_DATE('2024-01-02 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
);
```

```sql
-- 상대 시간을 이용한 재계산 (최근 1시간)
EXEC ROLLUP_REBUILD(
    sensor_tag,
    'TEMP-01',
    now - 1h,
    now
);
```

## 주의사항

- Cluster Edition에서 실행하면 오류가 반환됩니다: `ROLLUP_REBUILD is not supported in Cluster Edition`
- 재계산 대상 시간 범위가 넓을수록 실행 시간이 길어집니다. 필요한 최소 범위만 지정합니다.
- 재계산 중에도 정상적인 ROLLUP 집계 작업은 계속 진행됩니다.
- 원본 데이터 수정(TAG data UPDATE, 이상값 삭제 및 재입력 등) 후 실행해야 의미 있는 결과를 얻을 수 있습니다.

## 활용 시나리오

1. 센서 이상값 수정 후 해당 시간대 ROLLUP 재계산
2. 데이터 누락 구간 보정 후 집계 갱신
3. 원본 데이터 일괄 수정 작업 완료 후 검증

```sql
-- 이상 데이터 정정
UPDATE sensor_tag
   SET value = 25.0
 WHERE name = 'TEMP-01'
   AND time BETWEEN TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
                AND TO_DATE('2024-01-01 01:00:00', 'YYYY-MM-DD HH24:MI:SS');

-- ROLLUP 재계산
EXEC ROLLUP_REBUILD(
    sensor_tag,
    'TEMP-01',
    TO_DATE('2024-01-01 00:00:00', 'YYYY-MM-DD HH24:MI:SS'),
    TO_DATE('2024-01-01 01:00:00', 'YYYY-MM-DD HH24:MI:SS')
);
```

## 관련 문서

- [ROLLUP syntax](../rollup-syntax/) — ROLLUP 생성 및 조회 문법
- [Cluster Edition 제한사항](/dbms/operations-configuration-recovery/cluster/#limitations-cluster) — 에디션별 기능 차이
