---
type: docs
title: '기본 개념'
weight: 40
---

몇 가지 핵심 개념을 이해하면 Machbase를 효과적으로 사용하는 데 도움이 됩니다. 이 가이드는 알아야 할 필수 사항을 다룹니다.

## Machbase의 차별점은 무엇인가요?

Machbase는 **시계열 데이터**에 최적화되어 있습니다 - 타임스탬프와 함께 지속적으로 유입되는 데이터:

- IoT 센서 판독값
- 애플리케이션 로그
- 제조 장비 데이터
- 네트워크 트래픽
- 금융 틱 데이터

전통적인 데이터베이스와 달리 Machbase는 다음을 위해 특별히 구축되었습니다:
- **쓰기 중심** 워크로드 (초당 수백만 건의 삽입)
- **시간 기반** 쿼리 (최근 데이터, 시간 범위)
- **추가 전용** 데이터 (거의 업데이트되거나 삭제되지 않음)

## 4가지 테이블 타입

Machbase는 4가지 다른 테이블 타입을 제공합니다. **올바른 것을 선택하는 것이 중요합니다!**

### 빠른 결정 가이드

**어떤 테이블을 사용해야 하나요?**

```
센서 데이터(ID, 타임스탬프, 값)가 있나요?
    예 → TAG TABLE 사용

로그 데이터 또는 혼합 데이터 타입인가요?
    예 → LOG TABLE 사용

키로 특정 레코드를 UPDATE 또는 DELETE해야 하나요?
    예 → VOLATILE TABLE (인메모리) 사용

거의 변경되지 않는 참조/마스터 데이터인가요?
    예 → LOOKUP TABLE 사용
```

### 1. 태그 테이블 - 센서 데이터용

**사용 시기**: 센서/디바이스 시계열 데이터 저장

**최적 용도**:
- IoT 센서 판독값 (온도, 압력, 진동)
- 스마트 미터 데이터
- 환경 모니터링
- 장비 원격 측정

**구조**:
```
(sensor_name, timestamp, value, [선택적 컬럼])
```

**주요 기능**:
- 초당 수백만 건의 레코드
- 자동 통계 생성 (rollup)
- 센서 ID + 시간 범위별 초고속 쿼리
- 중복 제거 지원

**예시**:
```sql
CREATE TAGDATA TABLE sensors (
    sensor_name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    temperature DOUBLE SUMMARIZED,
    humidity DOUBLE SUMMARIZED
);
```

### 2. 로그 테이블 - 일반 시계열 데이터용

**사용 시기**: 로그 파일, 이벤트 또는 타임스탬프가 있는 모든 데이터 저장

**최적 용도**:
- 애플리케이션 로그
- 이벤트 스트림
- 액세스 로그
- 트랜잭션 로그
- 여러 컬럼이 있는 PLC 데이터

**구조**: 원하는 모든 스키마!

**주요 기능**:
- 초당 수백만 건의 레코드
- 자동 `_arrival_time` 컬럼 (나노초 정밀도)
- 최신 데이터가 먼저 반환됨
- SEARCH 키워드로 전문 검색
- 유연한 스키마

**예시**:
```sql
CREATE TABLE app_logs (
    level VARCHAR(10),
    user_id INTEGER,
    message VARCHAR(1000),
    ip_addr IPV4
);
```

### 3. 휘발성 테이블 - 인메모리 데이터용

**사용 시기**: 메모리에서 빠른 INSERT/UPDATE/DELETE가 필요할 때

**최적 용도**:
- 실시간 대시보드
- 세션 데이터
- 임시 계산
- 키-값 캐싱
- 실시간 모니터링 디스플레이

**구조**: 모든 스키마, PRIMARY KEY 지원

**주요 기능**:
- 초당 수만 건의 작업
- 기본 키로 UPDATE 및 DELETE 지원
- 모든 데이터가 메모리에 있음 (매우 빠름)
- **종료 시 데이터 손실!**

**예시**:
```sql
CREATE VOLATILE TABLE live_status (
    device_id INTEGER PRIMARY KEY,
    status VARCHAR(20),
    last_updated DATETIME
);
```

### 4. 룩업 테이블 - 참조 데이터용

**사용 시기**: 거의 변경되지 않는 참조/마스터 데이터 저장

**최적 용도**:
- 디바이스 레지스트리
- 구성 테이블
- 카테고리/차원 테이블
- 마스터 데이터

**구조**: 모든 스키마

**주요 기능**:
- 빠른 SELECT 성능
- 영구 저장
- 느린 INSERT/UPDATE (디스크 기반)
- 표준 데이터베이스 작업

**예시**:
```sql
CREATE LOOKUP TABLE devices (
    device_id INTEGER,
    name VARCHAR(50),
    location VARCHAR(100),
    type VARCHAR(20)
);
```

## 비교 표

| 기능 | 태그 테이블 | 로그 테이블 | 휘발성 테이블 | 룩업 테이블 |
|---------|-----------|-----------|----------------|--------------|
| **용도** | 센서 데이터 | 로그/이벤트 데이터 | 인메모리 캐시 | 마스터 데이터 |
| **삽입 속도** | 백만/초 | 백만/초 | 만/초 | 백/초 |
| **UPDATE 지원** | 아니오* | 아니오 | 예 | 예 |
| **DELETE 지원** | 시간 기반 | 시간 기반 | 키 기반 | 키 기반 |
| **저장소** | 디스크 | 디스크 | 메모리 | 디스크 |
| **스키마** | 고정 패턴 | 유연 | 유연 | 유연 |
| **최적 쿼리** | ID + 시간 | 시간 기반 | 키 기반 | 모두 |
| **데이터 영속성** | 예 | 예 | **아니오** | 예 |

*태그 테이블 메타데이터 컬럼은 업데이트 가능

## 자동 타임스탬프: _arrival_time

모든 로그 테이블 레코드는 자동으로 타임스탬프를 받습니다:

```sql
-- 이렇게 삽입하면
INSERT INTO app_logs VALUES ('ERROR', 'Connection failed');

-- Machbase는 이렇게 저장합니다
-- _arrival_time: 2025-10-10 14:23:45 123:456:789
-- level: ERROR
-- message: Connection failed
```

다음으로 액세스:
```sql
SELECT _arrival_time, * FROM app_logs;
```

타임스탬프는 **나노초 정밀도**를 가집니다 - 고주파 데이터에 완벽합니다!

## 데이터 순서: 최신 우선

전통적인 데이터베이스와 달리 Machbase는 **최신 데이터를 먼저** 반환합니다:

```sql
SELECT * FROM app_logs;
-- 가장 최근 로그가 맨 위에 반환됨
-- ORDER BY _arrival_time DESC 필요 없음
```

이는 최근 데이터가 가장 가치 있는 시계열 분석에 최적화되어 있습니다.

## 시간 기반 쿼리: DURATION

`DURATION` 키워드는 시간 쿼리를 간단하게 만듭니다:

```sql
-- 최근 10분
SELECT * FROM app_logs DURATION 10 MINUTE;

-- 대신에:
-- SELECT * FROM app_logs
-- WHERE _arrival_time >= NOW() - INTERVAL '10' MINUTE;
```

더 많은 예시:
```sql
-- 최근 1시간
DURATION 1 HOUR

-- 최근 1일
DURATION 1 DAY

-- 2시간 전부터 30분간
DURATION 30 MINUTE BEFORE 2 HOUR
```

## 한 번 쓰기 아키텍처

Machbase는 **추가 전용** 데이터를 위해 설계되었습니다:

- 태그/로그 테이블에서 UPDATE 없음
- 무작위 DELETE 없음
- 시간 기반 삭제만

**이유는?** 이를 통해 다음이 가능합니다:
- 초고속 쓰기 (행 잠금 없음)
- 데이터 무결성 (로그 변조 불가)
- 단순화된 아키텍처

**UPDATE/DELETE가 필요한 경우:**
- 인메모리 데이터는 Volatile 테이블 사용
- 영구 참조 데이터는 Lookup 테이블 사용

## 시간 기반 삭제

오래된 데이터를 효율적으로 정리:

```sql
-- 가장 오래된 1000개 행 삭제
DELETE FROM app_logs OLDEST 1000 ROWS;

-- 최근 10000개 행만 유지
DELETE FROM app_logs EXCEPT 10000 ROWS;

-- 최근 7일만 유지
DELETE FROM app_logs EXCEPT 7 DAYS;

-- 특정 날짜 이전 데이터 삭제
DELETE FROM app_logs
BEFORE TO_DATE('2025-01-01', 'YYYY-MM-DD');
```

## 인덱스

Machbase는 인덱스를 자동으로 최적으로 생성합니다:

- **태그 테이블**: 3단계 파티션 인덱스 (자동)
- **로그 테이블**: LSM 인덱스 (선택 사항, CREATE INDEX로 생성)
- **휘발성 테이블**: Red-black tree 인덱스 (PRIMARY KEY용)
- **룩업 테이블**: LSM 인덱스 (선택 사항)

대부분의 사용자는 인덱스를 수동으로 관리할 필요가 없습니다!

## Rollup 테이블 (태그 테이블만)

태그 테이블은 자동으로 통계를 생성합니다:

```sql
-- SUMMARIZED 컬럼이 있는 태그 테이블 생성
CREATE TAGDATA TABLE sensors (
    sensor_name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    temperature DOUBLE SUMMARIZED
);

-- 시간별 통계를 자동으로 쿼리
SELECT * FROM sensors WHERE rollup = hour;
-- 반환: MIN, MAX, AVG, SUM, COUNT, SUMSQ
```

3가지 자동 롤업 레벨:
- 초당
- 분당
- 시간당

## 압축

Machbase는 데이터를 자동으로 압축합니다:

- **논리적 압축**: 컬럼 기반 압축 (최대 100배)
- **물리적 압축**: 블록 레벨 압축 (특허)

아무것도 구성할 필요가 없습니다 - 그냥 작동합니다!

## 주요 용어

| 용어 | 의미 |
|------|---------|
| **Tag** | 센서 또는 데이터 소스 식별자 |
| **BASETIME** | 태그 테이블의 타임스탬프 컬럼 |
| **SUMMARIZED** | 자동 롤업 통계용 컬럼 표시 |
| **_arrival_time** | 자동 생성된 타임스탬프 (나노초 정밀도) |
| **DURATION** | 시간 범위 쿼리용 키워드 |
| **Rollup** | 자동 생성된 통계 요약 |
| **LSM Index** | Log-Structured Merge 인덱스 (빠른 쓰기용) |

## 모범 사례

### 1. 올바른 테이블 타입 선택

- **많은 ID가 있는 대용량 센서** → 태그 테이블
- **애플리케이션 로그, 이벤트** → 로그 테이블
- **실시간 업데이트 필요** → 휘발성 테이블
- **구성, 참조 데이터** → 룩업 테이블

### 2. 시간 쿼리에 DURATION 사용

```sql
-- 좋음 (최적화됨)
SELECT * FROM logs DURATION 1 HOUR;

-- 덜 최적화됨
SELECT * FROM logs
WHERE _arrival_time >= NOW() - INTERVAL '1' HOUR;
```

### 3. 데이터 보존 구현

자동 정리 설정:

```sql
-- 30일간의 데이터만 유지
DELETE FROM app_logs EXCEPT 30 DAYS;
```

이를 위한 cron 작업 설정을 고려하세요.

### 4. 다중 센서 데이터에 태그 테이블 사용

1000개의 센서가 있다면 1000개의 테이블을 생성하지 마세요!

```sql
-- 좋음: 모든 센서를 위한 하나의 태그 테이블
CREATE TAGDATA TABLE all_sensors (
    sensor_id VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

-- 특정 센서 쿼리
SELECT * FROM all_sensors
WHERE sensor_id = 'sensor123'
AND time BETWEEN ... AND ...;
```

## 일반 패턴

### 패턴 1: IoT 센서 수집

```sql
-- 센서 데이터용 태그 테이블
CREATE TAGDATA TABLE sensors (...);

-- 센서 메타데이터용 룩업 테이블
CREATE LOOKUP TABLE sensor_info (
    sensor_id VARCHAR(20),
    location VARCHAR(100),
    type VARCHAR(50)
);
```

### 패턴 2: 애플리케이션 모니터링

```sql
-- 애플리케이션 로그용 로그 테이블
CREATE TABLE app_logs (...);

-- 액세스 로그용 로그 테이블
CREATE TABLE access_logs (...);

-- 실시간 사용자 세션용 휘발성 테이블
CREATE VOLATILE TABLE active_sessions (...);
```

### 패턴 3: 제조

```sql
-- 장비 센서용 태그 테이블
CREATE TAGDATA TABLE equipment_sensors (...);

-- 생산 이벤트용 로그 테이블
CREATE TABLE production_events (...);

-- 장비 레지스트리용 룩업 테이블
CREATE LOOKUP TABLE equipment_list (...);
```

## 다음은 무엇인가요?

이제 핵심 개념을 이해했습니다:

1. [**튜토리얼**](../../tutorials/) - 실제 시나리오로 연습
2. [**일반 작업**](../../common-tasks/) - 일상 작업 학습
3. [**테이블 타입 심층 분석**](../../table-types/) - 상세한 문서

## 빠른 참조

```sql
-- TAG TABLE (센서 데이터)
CREATE TAGDATA TABLE t (
    name VARCHAR(20) PRIMARY KEY,
    time DATETIME BASETIME,
    value DOUBLE SUMMARIZED
);

-- LOG TABLE (유연한 시계열)
CREATE TABLE t (
    col1 TYPE,
    col2 TYPE
);
-- _arrival_time 자동 추가

-- VOLATILE TABLE (인메모리)
CREATE VOLATILE TABLE t (
    id INTEGER PRIMARY KEY,
    value TYPE
);

-- LOOKUP TABLE (참조 데이터)
CREATE LOOKUP TABLE t (
    id INTEGER,
    name VARCHAR(100)
);
```
