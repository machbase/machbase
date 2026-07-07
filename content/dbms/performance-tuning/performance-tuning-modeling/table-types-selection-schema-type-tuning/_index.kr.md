---
type: docs
title: '스키마와 테이블 타입 선택 튜닝'
weight: 10
---

테이블 타입과 컬럼 구조는 성능의 출발점입니다. 운영 중에 테이블 타입을 변경하려면 데이터 마이그레이션이 필요하므로, 설계 단계에서 올바른 선택을 하는 것이 중요합니다.

## TAG vs LOG: 데이터 특성에 따른 선택

가장 먼저 결정해야 할 것은 TAG 테이블과 LOG 테이블 중 어느 것이 데이터 특성에 맞는가입니다.

### 선택 기준

| 질문 | TAG 선택 | LOG 선택 |
|------|----------|----------|
| 데이터 발생 주체가 고정된 센서/장비인가? | 예 | 아니오 |
| 동일 센서에서 주기적으로 반복 측정하는가? | 예 | 아니오 |
| "센서 A의 최근 값은?" 형태의 조회가 잦은가? | 예 | 아니오 |
| 발생 주체가 사전에 정의되지 않는 이벤트인가? | 아니오 | 예 |
| 이벤트 내용이 다양하고 컬럼 수가 많은가? | 아니오 | 예 |
| 시간 범위 내 전체 이벤트 스캔이 주 패턴인가? | 아니오 | 예 |

**센서 데이터 → TAG 테이블**

공장 온도 센서, 압력 게이지, 전력 미터 등 고정된 장비에서 주기적으로 측정값을 수집하는 경우입니다. 태그 이름(`name` 컬럼)과 시간을 조합한 파티션 인덱스가 자동으로 생성되므로, 특정 센서의 시간 범위 조회가 매우 빠릅니다.

```sql
-- TAG 테이블 생성 예시 (센서 계측값)
CREATE TAG TABLE factory_sensor (
    name        VARCHAR(64) PRIMARY KEY,
    time        DATETIME BASETIME,
    value       DOUBLE SUMMARIZED,
    quality     SHORT
);
```

**이벤트·로그 데이터 → LOG 테이블**

시스템 알람, 사용자 액션, 보안 이벤트 등 발생 주체가 가변적이고 이벤트 내용이 다양한 경우입니다. `_ARRIVAL_TIME` 기반 시간 범위 스캔에 최적화되어 있으며, 컬럼별 LSM 인덱스를 추가하여 특정 조건 검색을 가속할 수 있습니다.

```sql
-- LOG 테이블 생성 예시 (설비 알람 로그)
CREATE TABLE alarm_log (
    alarm_id    VARCHAR(32),
    device_id   VARCHAR(32),
    alarm_code  INTEGER,
    severity    SHORT,
    message     VARCHAR(256)
);
```

### 잘못된 타입 선택이 초래하는 문제

**센서 데이터를 LOG에 저장한 경우**

수천 개 센서가 있을 때 특정 센서의 최근 값을 조회하면 전체 테이블 스캔이 발생합니다. `sensor_id` 컬럼에 LSM 인덱스를 생성해도 센서 수가 많아질수록 인덱스 크기와 유지 비용이 커집니다. TAG 테이블로 전환하면 동일 쿼리를 수십 배 빠르게 처리할 수 있습니다.

**이벤트 로그를 TAG에 저장한 경우**

TAG 테이블의 `name` 컬럼은 고정된 센서 식별자를 전제로 파티션을 나눕니다. 이벤트 로그처럼 발생 주체가 매번 달라지면 파티션이 무수히 분산되어 메모리와 디스크 사용량이 급증합니다. 또한 TAG 테이블은 특정 태그 없이 전체 시간 범위 스캔 시 오히려 LOG 테이블보다 느립니다.

## 컬럼 수 최소화

LOG 테이블은 컬럼 수가 입력 성능에 직접 영향을 미칩니다. 컬럼형 저장 구조이므로 데이터를 입력할 때 각 컬럼별로 별도 파일에 분산 기록합니다. 컬럼 수가 많을수록 입력 시 파일 I/O가 비례하여 증가합니다.

**컬럼 수와 입력 성능 관계 (참고 수치)**

| 컬럼 수 | 상대적 입력 성능 | 비고 |
|---------|----------------|------|
| 10개 이하 | 기준 (1.0x) | 권장 범위 |
| 20~30개 | 약 0.7x | 허용 범위 |
| 50개 이상 | 약 0.4x 이하 | 재설계 고려 |

**권장 사항**

- 실제 조회에 사용하지 않는 컬럼은 정의하지 않습니다.
- 여러 성격의 데이터를 하나의 테이블에 넣으려고 컬럼을 과다하게 추가하는 것을 피합니다.
- 필요하면 테이블을 분리하고 `_ARRIVAL_TIME`을 기준으로 조인하는 방식을 검토합니다.

```sql
-- 나쁜 예: 불필요한 컬럼이 많은 경우
CREATE TABLE sensor_log (
    sensor_id   VARCHAR(64),
    value1      DOUBLE,
    value2      DOUBLE,
    value3      DOUBLE,
    -- ... value20 까지
    reserved1   VARCHAR(256),  -- 미사용
    reserved2   VARCHAR(256),  -- 미사용
    reserved3   INTEGER        -- 미사용
);

-- 좋은 예: 실제 사용하는 컬럼만 정의
CREATE TABLE sensor_log (
    sensor_id   VARCHAR(64),
    value       DOUBLE,
    unit        VARCHAR(16)
);
```

## VARCHAR 컬럼 크기 설정

VARCHAR 컬럼의 최대 크기를 실제 데이터보다 훨씬 크게 설정하면 저장 공간과 메모리 버퍼를 불필요하게 낭비합니다. Machbase의 LOG 테이블 VARCHAR는 실제 저장된 데이터 길이만큼만 저장하지만, 내부 버퍼와 인덱스 구조는 선언된 최대 크기를 기준으로 공간을 예약하는 경우가 있습니다.

**권장 사항**

- 실제 데이터의 최대 길이보다 20~30% 여유를 두되, 과도하게 크게 설정하지 않습니다.
- 센서 이름처럼 길이가 예측 가능한 컬럼은 실제 길이에 맞게 설정합니다.
- 이벤트 메시지처럼 길이가 가변적인 컬럼은 실제 95번째 백분위수 길이를 기준으로 설정합니다.

```sql
-- 나쁜 예: 실제 데이터가 최대 32자인데 크기 과다 설정
CREATE TABLE event_log (
    event_id    VARCHAR(1024),  -- 실제 최대 32자인데 1024 설정
    message     VARCHAR(65535)  -- 실제 최대 512자인데 65535 설정
);

-- 좋은 예: 실제 데이터 길이에 맞게 설정
CREATE TABLE event_log (
    event_id    VARCHAR(40),    -- UUID + 여유분
    message     VARCHAR(512)    -- 실제 최대 길이 기준
);
```

## METADATA 컬럼 활용 (TAG 테이블)

TAG 테이블의 METADATA 컬럼은 태그 이름에 연결된 정적 속성을 저장합니다. 자주 필터링하는 센서 속성을 METADATA로 정의하면, 조회 시 데이터 파티션을 스캔하기 전에 메타데이터만으로 대상 태그를 빠르게 걸러낼 수 있습니다.

**METADATA 컬럼 활용 예시**

```sql
-- TAG 테이블에 METADATA 컬럼 추가
CREATE TAG TABLE factory_sensor (
    name        VARCHAR(64)  PRIMARY KEY,
    time        DATETIME     BASETIME,
    value       DOUBLE       SUMMARIZED,
    -- METADATA 컬럼: 센서 속성 (한 번 등록, 자주 필터링)
    plant_id    VARCHAR(32)  METADATA,
    line_id     VARCHAR(32)  METADATA,
    sensor_type VARCHAR(16)  METADATA
);

-- 메타데이터 기반 필터링 (빠름: 데이터 파티션 스캔 전에 태그 필터링)
SELECT name, LAST(time, value)
FROM factory_sensor
WHERE plant_id = 'PLANT_A' AND sensor_type = 'TEMPERATURE'
GROUP BY name;
```

**METADATA 컬럼 선택 기준**

| METADATA로 적합한 속성 | METADATA로 부적합한 속성 |
|----------------------|------------------------|
| 설비 위치, 라인 번호 | 실시간으로 변하는 값 |
| 센서 종류, 단위 | 이벤트성 상태 값 |
| 담당 부서, 구역 ID | 측정 품질 플래그 |

METADATA 컬럼은 태그 등록 시 함께 기입하며, 이후 UPDATE로 변경할 수 있습니다. 단, 데이터 파티션에 저장되는 컬럼이 아니므로 시간에 따라 이력을 유지하지 않습니다.

## MINMAX_CACHE_SIZE 설정

LOG 테이블의 각 컬럼에는 MINMAX 캐시를 설정할 수 있습니다. MINMAX 캐시는 각 데이터 파티션(파트)의 최솟값과 최댓값을 메모리에 유지하여, 범위 조건으로 불필요한 파티션을 빠르게 건너뛸 수 있게 합니다.

**`_ARRIVAL_TIME` 컬럼의 기본 MINMAX 캐시**

`_ARRIVAL_TIME` 컬럼은 기본값으로 100 MB의 MINMAX 캐시가 할당됩니다. 이 값은 `machbase.conf`의 `DISK_COLUMNAR_TABLE_COLUMN_MINMAX_CACHE_SIZE` 프로퍼티로 설정합니다.

```
# machbase.conf
DISK_COLUMNAR_TABLE_COLUMN_MINMAX_CACHE_SIZE = 200*1024*1024  # 200MB
```

시간 범위 조회가 매우 잦고 테이블 크기가 큰 경우, 이 값을 200~500 MB로 늘리면 시간 범위 스캔 성능이 향상됩니다.

**특정 컬럼에 MINMAX 캐시 지정**

테이블 생성 시 자주 범위 조건으로 사용하는 컬럼에 MINMAX 캐시를 지정할 수 있습니다.

```sql
-- value 컬럼에 32MB MINMAX 캐시 지정
CREATE TABLE sensor_log (
    sensor_id   VARCHAR(64),
    value       DOUBLE,
    quality     SHORT
) PROPERTY (
    'MINMAX_CACHE_SIZE' = '33554432'  -- 32MB
);
```

**MINMAX 캐시 크기 결정 기준**

| 조건 | 권장 캐시 크기 |
|------|---------------|
| 테이블 크기 소규모 (수 GB 이하) | 기본값(100 MB) 유지 |
| 테이블 크기 중규모, 시간 범위 조회 잦음 | 200~300 MB |
| 테이블 크기 대규모, 시간 범위 조회 매우 잦음 | 500 MB 이상 |

메모리 여유가 충분하지 않다면 캐시를 무작정 늘리는 것보다 RS Cache(결과 캐시)와 함께 균형 있게 설정하는 것이 좋습니다. RS Cache 설정은 **[캐시·메모리 튜닝](../../cache-tuning-memory/)** 을 참고하십시오.

## 요약: 모델링 성능 체크리스트

설계 시 아래 항목을 순서대로 확인합니다.

- [ ] 센서/계측 데이터는 TAG 테이블, 이벤트/로그 데이터는 LOG 테이블로 정의했는가?
- [ ] LOG 테이블의 컬럼 수가 30개 이하인가?
- [ ] VARCHAR 컬럼 크기가 실제 데이터 길이와 적절히 일치하는가?
- [ ] TAG 테이블에서 자주 필터링하는 센서 속성을 METADATA 컬럼으로 정의했는가?
- [ ] 시간 범위 조회가 잦은 대규모 LOG 테이블에 충분한 MINMAX 캐시를 설정했는가?
