---
type: docs
title: '데이터 조회하기'
weight: 30
---

Machbase의 일반적인 쿼리 패턴과 최적화 기법을 마스터합니다. 시계열 데이터 분석을 위한 효율적인 쿼리 작성 방법을 학습합니다.

## 쿼리 기본

### 간단한 SELECT

```sql
-- 모든 최근 데이터 가져오기
SELECT * FROM sensors DURATION 1 HOUR;

-- 특정 컬럼만 선택
SELECT sensor_id, value, _arrival_time
FROM sensors DURATION 1 HOUR;

-- 조건 사용
SELECT * FROM sensors
WHERE sensor_id = 'sensor01'
DURATION 1 HOUR;
```

### 시간 기반 쿼리

```sql
-- 최근 10분
SELECT * FROM logs DURATION 10 MINUTE;

-- 최근 1시간
SELECT * FROM logs DURATION 1 HOUR;

-- 최근 1일
SELECT * FROM logs DURATION 1 DAY;

-- 2시간 전부터 30분간
SELECT * FROM logs DURATION 30 MINUTE BEFORE 2 HOUR;

-- 특정 시간 범위
SELECT * FROM logs
WHERE _arrival_time BETWEEN '2025-10-10 00:00:00' AND '2025-10-10 23:59:59';
```

## 일반 패턴

### 패턴 1: 최근 데이터 모니터링

```sql
-- 최근 5분간의 에러
SELECT * FROM app_logs
WHERE level = 'ERROR'
DURATION 5 MINUTE;

-- 최신 센서 읽기값
SELECT sensor_id, value, _arrival_time
FROM sensors
DURATION 10 MINUTE
ORDER BY _arrival_time DESC;
```

### 패턴 2: 집계

```sql
-- 시간대별 카운트
SELECT
    TO_CHAR(_arrival_time, 'YYYY-MM-DD HH24:00:00') as hour,
    COUNT(*) as count
FROM logs
DURATION 24 HOUR
GROUP BY TO_CHAR(_arrival_time, 'YYYY-MM-DD HH24:00:00');

-- 센서별 평균
SELECT
    sensor_id,
    AVG(value) as avg_value,
    MIN(value) as min_value,
    MAX(value) as max_value
FROM sensors
DURATION 1 DAY
GROUP BY sensor_id;
```

### 패턴 3: 텍스트 검색

```sql
-- 키워드 검색
SELECT * FROM logs
WHERE message SEARCH 'timeout'
DURATION 1 HOUR;

-- 여러 키워드 (OR)
SELECT * FROM logs
WHERE message SEARCH 'error'
   OR message SEARCH 'failed'
DURATION 1 HOUR;

-- 대소문자 구분 없는 검색
SELECT * FROM logs
WHERE LOWER(message) LIKE '%error%'
DURATION 1 HOUR;
```

### 패턴 4: JOIN 연산

```sql
-- 디바이스 정보로 센서 데이터 보강
SELECT
    s.sensor_id,
    s.value,
    s._arrival_time,
    d.device_name,
    d.location
FROM sensors s
JOIN devices d ON s.sensor_id = d.device_id
DURATION 1 HOUR;

-- 다중 조인
SELECT
    s.*,
    d.device_name,
    f.facility_name,
    f.city
FROM sensors s
JOIN devices d ON s.sensor_id = d.device_id
JOIN facilities f ON d.facility = f.facility_code
DURATION 1 HOUR;
```

### 패턴 5: 롤업 쿼리 (Tag 테이블)

```sql
-- 시간별 롤업 조회
SELECT
    sensor_id,
    time,
    min_temperature,
    max_temperature,
    avg_temperature,
    count
FROM sensors
WHERE rollup = hour
DURATION 7 DAY;

-- 분 단위 롤업
SELECT * FROM sensors
WHERE rollup = min
DURATION 24 HOUR;

-- 초 단위 롤업
SELECT * FROM sensors
WHERE rollup = sec
DURATION 1 HOUR;
```

## 쿼리 최적화

### 1. 항상 시간 필터 사용

**나쁨** (모든 데이터 스캔):
```sql
SELECT * FROM sensors WHERE sensor_id = 'sensor01';
```

**좋음** (관련 파티션만 스캔):
```sql
SELECT * FROM sensors
WHERE sensor_id = 'sensor01'
DURATION 1 HOUR;
```

### 2. 대규모 결과에 LIMIT 사용

```sql
-- 결과 제한
SELECT * FROM logs DURATION 1 DAY LIMIT 1000;

-- 상위 N개 결과
SELECT * FROM sensors
ORDER BY value DESC
LIMIT 10;
```

### 3. 원시 데이터가 아닌 롤업 조회

**느림** (수백만 행 처리):
```sql
SELECT sensor_id, AVG(value)
FROM sensors
DURATION 30 DAY
GROUP BY sensor_id;
```

**빠름** (사전 집계된 데이터 조회):
```sql
SELECT sensor_id, AVG(avg_value)
FROM sensors
WHERE rollup = hour
DURATION 30 DAY
GROUP BY sensor_id;
```

### 4. 인덱스 사용

```sql
-- 자주 조회하는 컬럼에 인덱스 생성
CREATE INDEX idx_level ON logs(level);

-- 이제 이 쿼리는 빠름
SELECT * FROM logs
WHERE level = 'ERROR'
DURATION 1 HOUR;
```

### 5. SELECT * 피하기

```sql
-- 나쁨 (모든 컬럼 읽기)
SELECT * FROM sensors;

-- 좋음 (필요한 컬럼만 읽기)
SELECT sensor_id, value FROM sensors DURATION 1 HOUR;
```

## 고급 쿼리

### 서브쿼리

```sql
-- 평균 이상의 센서 찾기
SELECT sensor_id, value
FROM sensors
WHERE value > (
    SELECT AVG(value) FROM sensors DURATION 1 HOUR
)
DURATION 1 HOUR;
```

### 공통 테이블 표현식 (CTE)

```sql
-- 시간대별 평균 계산
WITH hourly_avg AS (
    SELECT
        sensor_id,
        TO_CHAR(_arrival_time, 'HH24') as hour,
        AVG(value) as avg_value
    FROM sensors
    DURATION 24 HOUR
    GROUP BY sensor_id, TO_CHAR(_arrival_time, 'HH24')
)
SELECT * FROM hourly_avg WHERE avg_value > 25.0;
```

### 윈도우 함수

```sql
-- 이동 평균
SELECT
    sensor_id,
    value,
    AVG(value) OVER (
        PARTITION BY sensor_id
        ORDER BY _arrival_time
        ROWS BETWEEN 9 PRECEDING AND CURRENT ROW
    ) as moving_avg
FROM sensors
DURATION 1 HOUR;
```

## 시간 함수

### 날짜/시간 형식 지정

```sql
-- 타임스탬프 형식 지정
SELECT
    TO_CHAR(_arrival_time, 'YYYY-MM-DD HH24:MI:SS') as formatted_time,
    sensor_id,
    value
FROM sensors DURATION 1 HOUR;

-- 부분 추출
SELECT
    TO_CHAR(_arrival_time, 'YYYY') as year,
    TO_CHAR(_arrival_time, 'MM') as month,
    TO_CHAR(_arrival_time, 'DD') as day,
    TO_CHAR(_arrival_time, 'HH24') as hour
FROM logs DURATION 1 DAY;
```

### 시간 계산

```sql
-- 현재 시간
SELECT SYSDATE;
SELECT NOW;

-- 시간 연산
SELECT SYSDATE - INTERVAL '1' HOUR;
SELECT NOW + INTERVAL '30' MINUTE;

-- 날짜 변환
SELECT TO_DATE('2025-10-10', 'YYYY-MM-DD');
SELECT TO_TIMESTAMP('2025-10-10 14:30:00', 'YYYY-MM-DD HH24:MI:SS');
```

## 분석 쿼리

### 통계 분석

```sql
-- 종합 통계
SELECT
    sensor_id,
    COUNT(*) as count,
    AVG(value) as mean,
    STDDEV(value) as stddev,
    MIN(value) as min,
    MAX(value) as max,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY value) as median
FROM sensors
DURATION 1 DAY
GROUP BY sensor_id;
```

### 추세 분석

```sql
-- 시간대별 추세
SELECT
    TO_CHAR(_arrival_time, 'YYYY-MM-DD HH24:00:00') as hour,
    AVG(value) as avg_value,
    LAG(AVG(value)) OVER (ORDER BY TO_CHAR(_arrival_time, 'YYYY-MM-DD HH24:00:00')) as prev_hour,
    AVG(value) - LAG(AVG(value)) OVER (ORDER BY TO_CHAR(_arrival_time, 'YYYY-MM-DD HH24:00:00')) as change
FROM sensors
DURATION 24 HOUR
GROUP BY TO_CHAR(_arrival_time, 'YYYY-MM-DD HH24:00:00')
ORDER BY hour;
```

### 이상 감지

```sql
-- 표준편차 2배를 벗어나는 값 찾기
WITH stats AS (
    SELECT
        AVG(value) as mean,
        STDDEV(value) as stddev
    FROM sensors DURATION 1 DAY
)
SELECT s.*, st.mean, st.stddev
FROM sensors s, stats st
WHERE s.value < st.mean - 2 * st.stddev
   OR s.value > st.mean + 2 * st.stddev
DURATION 1 DAY;
```

## 쿼리 성능 모니터링

### 활성 쿼리 확인

```sql
-- 실행 중인 쿼리 보기
SHOW STATEMENTS;
```

### 쿼리 실행 계획

```sql
-- 쿼리 계획 설명
EXPLAIN SELECT * FROM sensors DURATION 1 HOUR;
```

### 성능 팁

1. **시간 필터 사용** - 항상 DURATION 또는 시간 WHERE 절 포함
2. **롤업 조회** - Tag 테이블의 사전 집계 데이터 사용
3. **인덱스 생성** - Log/Lookup 테이블의 자주 조회하는 컬럼에 인덱스 생성
4. **결과 제한** - LIMIT를 사용하여 결과셋 크기 제한
5. **특정 컬럼 선택** - SELECT * 피하기
6. **배치 작업** - 대용량 데이터셋을 청크 단위로 처리

## 일반 쿼리 패턴

### 대시보드 쿼리

```sql
-- 실시간 상태 보드
SELECT
    device_id,
    status,
    last_value,
    last_updated
FROM device_status
ORDER BY last_updated DESC
LIMIT 20;

-- 에러 요약
SELECT
    level,
    COUNT(*) as count,
    MAX(_arrival_time) as last_occurrence
FROM logs
DURATION 1 HOUR
GROUP BY level;
```

### 리포팅 쿼리

```sql
-- 일일 요약 보고서
SELECT
    TO_CHAR(_arrival_time, 'YYYY-MM-DD') as date,
    COUNT(*) as total_records,
    COUNT(DISTINCT sensor_id) as unique_sensors,
    AVG(value) as avg_value
FROM sensors
DURATION 30 DAY
GROUP BY TO_CHAR(_arrival_time, 'YYYY-MM-DD')
ORDER BY date;
```

### 알림 쿼리

```sql
-- 최근 5분간의 중요 에러
SELECT * FROM logs
WHERE level = 'ERROR'
  AND message SEARCH 'critical'
DURATION 5 MINUTE;

-- 임계값 초과 센서
SELECT sensor_id, value, _arrival_time
FROM sensors
WHERE value > 30.0
DURATION 10 MINUTE;
```

## 모범 사례

1. **항상 시간으로 필터링** - DURATION 또는 시간 기반 WHERE 절 사용
2. **먼저 작은 시간 범위로 테스트** - 대용량 데이터셋에서 실행하기 전에 확인
3. **LIMIT 사용** - 실수로 수백만 행을 반환하는 것을 방지
4. **분석에 롤업 조회** - 원시 데이터 집계보다 훨씬 빠름
5. **인덱스 생성** - Log/Lookup 테이블의 자주 조회하는 컬럼에 대해
6. **성능 모니터링** - SHOW STATEMENTS로 느린 쿼리 추적
7. **적절한 테이블 타입 사용** - 센서는 Tag, 이벤트는 Log 등

## 문제 해결

**쿼리가 너무 느림**:
- 시간 필터 추가 (DURATION)
- LIMIT 절 사용
- 원시 데이터 대신 롤업 조회
- 필터 컬럼에 인덱스 생성

**메모리 부족**:
- 시간 범위 축소
- LIMIT 사용
- 더 적은 컬럼 선택
- 서버 메모리 증가 (MAX_QPX_MEM)

**연결 타임아웃**:
- 쿼리 타임아웃 증가
- 더 작은 쿼리로 분할
- 쿼리 최적화 (인덱스 추가, 롤업 사용)

## 다음 단계

- **사용자 관리**: [사용자 관리](../user-management/) - 쿼리 권한 제어
- **백업**: [백업 및 복구](../backup-recovery/) - 데이터 보호
- **핵심 개념**: [인덱싱](../../core-concepts/indexing/) - 성능에 대한 심층 분석

---

이러한 쿼리 패턴을 마스터하고 Machbase 분석의 완전한 능력을 발휘하세요!
