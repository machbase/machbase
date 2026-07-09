---
type: docs
title: '12.5.2 검색 연산자 성능 튜닝'
weight: 20
---

WHERE 절에서 어떤 연산자를 사용하느냐에 따라 인덱스 활용 여부가 결정됩니다. 이 페이지에서는 인덱스를 사용할 수 있는 연산자와 사용할 수 없는 연산자를 구분하고, 인덱스 종류별 선택 기준을 설명합니다.

## 인덱스 사용 가능 연산자

다음 연산자는 BITMAP 또는 LSM 인덱스를 활용해 스캔 범위를 줄입니다.

| 연산자 | 설명 | 예시 |
|--------|------|------|
| `=` | 동등 비교 | `severity = 'ERROR'` |
| `<` | 미만 | `value < 100.0` |
| `<=` | 이하 | `value <= 100.0` |
| `>` | 초과 | `value > 50.0` |
| `>=` | 이상 | `value >= 50.0` |
| `BETWEEN` | 범위 | `value BETWEEN 10.0 AND 90.0` |
| 전방 LIKE | 접두어 일치 | `host LIKE 'server%'` |

```sql
-- 인덱스 활용: BETWEEN (내부적으로 >= AND <= 로 처리)
EXPLAIN SELECT * FROM machine_log
WHERE  response_code BETWEEN 400 AND 499
  AND  _arrival_time >= '2025-06-01' AND _arrival_time < '2025-06-02';

PLAN
------------------------------------------------------------------------------------
 PROJECT
  INDEX SCAN
   *BITMAP RANGE (table id:3, column id:4, index id:5)
   [KEY RANGE]
    * response_code >= 400
    * response_code <= 499
   [FILTER]
    * _arrival_time >= '2025-06-01 00:00:00'
    * _arrival_time < '2025-06-02 00:00:00'
```

## 인덱스 사용 불가 연산자

다음 패턴은 인덱스를 사용하지 못해 FULL SCAN이 발생합니다.

### 중간/후방 LIKE

와일드카드가 앞에 오는 LIKE 패턴은 인덱스를 사용할 수 없습니다.

```sql
-- 인덱스 미사용: '%xxx%' 또는 '%xxx' 패턴
SELECT * FROM machine_log WHERE message LIKE '%timeout%';  -- FULL SCAN

-- 인덱스 사용 가능: 전방 LIKE (접두어 일치)
SELECT * FROM machine_log WHERE host LIKE 'server%';       -- INDEX SCAN
```

### 컬럼에 함수 적용

WHERE 절에서 컬럼을 함수로 감싸면 옵티마이저가 인덱스를 사용하지 못합니다.

```sql
-- 인덱스 미사용: 함수 내부 컬럼
SELECT * FROM system_log WHERE UPPER(severity) = 'ERROR';   -- FULL SCAN
SELECT * FROM system_log WHERE LENGTH(message) > 100;       -- FULL SCAN

-- 권장: 비교 값을 변환
SELECT * FROM system_log WHERE severity = 'ERROR';           -- INDEX SCAN
```

### OR 조건과 인덱스 결합

OR 조건에서 하나라도 인덱스가 없는 컬럼이 포함되면 전체 FULL SCAN으로 전환될 수 있습니다.

```sql
-- 인덱스 있는 컬럼끼리 OR: INDEX(OR) 사용
EXPLAIN SELECT * FROM machine_log WHERE code = 400 OR code = 500;

PLAN
------------------------------------------------------------------------------------
 PROJECT
  INDEX SCAN
   INDEX (OR)
    *BITMAP RANGE (table id:3, column id:4, index id:5)
    *BITMAP RANGE (table id:3, column id:4, index id:5)
   [KEY RANGE]
    * code = 400 or code = 500

-- 인덱스 없는 컬럼이 OR에 포함: FULL SCAN 전환
SELECT * FROM machine_log WHERE code = 400 OR message = 'ok'; -- FULL SCAN
```

OR 조건 대신 UNION ALL로 분리하면 각 쿼리에서 INDEX SCAN을 활용할 수 있습니다.

```sql
-- UNION ALL로 분리 (각각 INDEX SCAN 적용)
SELECT * FROM machine_log WHERE code = 400
UNION ALL
SELECT * FROM machine_log WHERE code = 500;
```

## BITMAP 인덱스 효과 (LOG 테이블)

LOG 테이블에서 기본으로 생성되는 BITMAP 인덱스는 카디널리티(서로 다른 값의 수)가 낮은 컬럼에 특히 효과적입니다.

| 컬럼 특성 | BITMAP 인덱스 효과 |
|-----------|-------------------|
| 카디널리티 낮음 (예: severity, status_code) | 매우 효과적 — 값당 비트 벡터로 빠른 RID 계산 |
| 카디널리티 높음 (예: session_id, message) | 효과 제한적 — 비트 벡터 밀도가 높아 이점 감소 |

```sql
-- 카디널리티 낮은 컬럼 (severity: ERROR/WARN/INFO) → BITMAP 효과적
CREATE INDEX idx_severity ON machine_log (severity);

-- 복합 조건에서 BITMAP 인덱스 AND 연산
EXPLAIN SELECT * FROM machine_log
WHERE  severity = 'ERROR' AND response_code = 500;

PLAN
------------------------------------------------------------------------------------
 PROJECT
  INDEX SCAN
   *BITMAP RANGE (table id:3, column id:2, index id:4)  -- severity 인덱스
   *BITMAP RANGE (table id:3, column id:5, index id:6)  -- response_code 인덱스
   [KEY RANGE]
    * severity = 'ERROR'
    * response_code = 500
```

두 인덱스의 비트 벡터를 AND 연산해 교집합 RID만 읽으므로 단일 인덱스보다 빠릅니다.

## LSM vs BITMAP 인덱스 선택 기준

Machbase는 LOG 테이블에 두 가지 인덱스 유형을 지원합니다.

| 구분 | LSM 인덱스 | BITMAP 인덱스 |
|------|-----------|--------------|
| 구조 | 정렬된 키 목록 | 값별 비트 벡터 |
| 적합 대상 | 숫자형, 날짜형, 고카디널리티 컬럼 | 문자열, 저카디널리티 컬럼 |
| 범위 검색 | 우수 | 보통 |
| 동등 검색 | 우수 | 우수 |
| 복합 AND | 제한적 | 비트 AND 연산으로 매우 빠름 |
| 생성 구문 | `CREATE INDEX ... INDEX_TYPE LSM` | `CREATE BITMAP INDEX ...` 또는 `CREATE INDEX ... INDEX_TYPE BITMAP` |

```sql
-- BITMAP 인덱스 생성 (문자열·저카디널리티 컬럼에 적합)
CREATE BITMAP INDEX idx_severity ON machine_log (severity);

-- LSM 인덱스 생성 (숫자형 범위 검색에 적합)
CREATE INDEX idx_ts ON machine_log (event_time) INDEX_TYPE LSM;
```

**선택 기준 요약:**
- 값의 종류가 수십~수백 개 이하(저카디널리티): BITMAP
- 숫자·날짜 컬럼의 범위 검색: LSM
- 복합 AND 조건으로 여러 컬럼 동시 필터링: BITMAP 조합이 효과적

## IP 타입 BETWEEN 조회 성능

Machbase의 IP 타입 컬럼은 내부적으로 정수로 저장되므로, BETWEEN 조건을 사용하면 인덱스 범위 검색이 효율적으로 동작합니다.

```sql
-- IP 범위 조회: BETWEEN으로 서브넷 필터링
SELECT _arrival_time, src_ip, dst_ip, bytes
FROM   network_log
WHERE  src_ip BETWEEN '192.168.1.0' AND '192.168.1.255'
  AND  _arrival_time >= '2025-06-01' AND _arrival_time < '2025-06-02';
```

IP 컬럼에 인덱스를 생성하면 BETWEEN 조건에 대해 INDEX SCAN이 적용됩니다.

```sql
CREATE INDEX idx_src_ip ON network_log (src_ip);
```

## 특정 인덱스 비활성화

옵티마이저가 선택한 인덱스보다 다른 인덱스가 더 효율적일 때 `NO_INDEX` 힌트로 특정 인덱스를 제외할 수 있습니다.

```sql
-- idx_code 인덱스를 제외하고 idx_severity 인덱스만 사용
SELECT /*+ NO_INDEX(machine_log, idx_code) */ *
FROM   machine_log
WHERE  code = 400 AND severity = 'ERROR';

PLAN
------------------------------------------------------------------------------------
 PROJECT
  INDEX SCAN
   *BITMAP RANGE (table id:3, column id:2, index id:4)  -- severity 인덱스만 사용
   [KEY RANGE]
    * severity = 'ERROR'
   [FILTER]
    * code = 400
```

## 요약: 연산자별 인덱스 활용 가능 여부

| 패턴 | 인덱스 활용 |
|------|-------------|
| `col = value` | O |
| `col < value`, `col <= value` | O |
| `col > value`, `col >= value` | O |
| `col BETWEEN v1 AND v2` | O |
| `col LIKE 'prefix%'` | O (전방 LIKE) |
| `col LIKE '%suffix'` | X |
| `col LIKE '%middle%'` | X |
| `FUNC(col) = value` | X |
| `col1 = v1 OR col2 = v2` (col2 인덱스 없음) | X (FULL SCAN) |
| `col1 = v1 OR col1 = v2` (같은 컬럼) | O (INDEX OR) |
