---
title: '9.9 활용 패턴과 시나리오'
weight: 90
toc: true
---
활용 패턴과 시나리오에 해당하는 세부 문서를 모았습니다.


<a id="use-cases-lookup"></a>

## 활용 사례

LOOKUP 테이블은 다음과 같은 데이터를 저장하는 데 적합합니다.

### 적합한 데이터 유형

| 유형 | 예시 |
|------|------|
| 코드 테이블 | 국가 코드, 언어 코드, 상태 코드 |
| 기준 정보 | 설비 목록, 제품 분류, 부서 정보 |
| 실시간 갱신 참조 | 환율 테이블, 임계값 설정 |
| 태그 메타데이터 대체 | 센서 정보 (소규모) |

### 예시 스키마

#### 국가 코드 테이블

```sql
CREATE LOOKUP TABLE country_code (
    code   VARCHAR(4)   PRIMARY KEY,
    name   VARCHAR(64),
    region VARCHAR(32)
);

INSERT INTO country_code VALUES ('KR', '대한민국', 'Asia');
INSERT INTO country_code VALUES ('US', '미국', 'America');
UPDATE country_code SET name = 'United States' WHERE code = 'US';
```

#### 설비 마스터

```sql
CREATE LOOKUP TABLE equipment_master (
    equip_id   VARCHAR(32) PRIMARY KEY,
    equip_name VARCHAR(128),
    location   VARCHAR(64),
    dept       VARCHAR(64),
    install_dt DATETIME
);
```

#### 임계값 설정 (실시간 변경 가능)

```sql
CREATE LOOKUP TABLE threshold_config (
    sensor_name VARCHAR(64) PRIMARY KEY,
    low_limit   DOUBLE,
    high_limit  DOUBLE,
    alert_level SHORT
);

-- 실시간 임계값 변경
UPDATE threshold_config SET high_limit = 85.0 WHERE sensor_name = 'TEMP-01';
```

### 부적합한 경우

- 건수가 수백만 건을 초과하는 대용량 데이터 → RDB 테이블 권장
- UPDATE 불필요한 추가 전용 이력 → LOG 테이블 권장
- 센서 계측값 → TAG 테이블 권장
