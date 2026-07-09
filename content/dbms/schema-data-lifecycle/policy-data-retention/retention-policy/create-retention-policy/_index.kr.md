---
type: docs
title: 'Retention Policy 생성'
weight: 10
---

`CREATE RETENTION` 구문으로 보존 기간과 삭제 주기를 정의한 정책을 생성합니다.

## 구문

```sql
CREATE RETENTION policy_name
    DURATION duration_value {MONTH|DAY|HOUR|MIN|SEC}
    INTERVAL interval_value {DAY|HOUR|MIN|SEC}
```

- **policy_name**: 정책 이름
- **DURATION**: 데이터 보존 기간. 이 기간을 초과한 데이터는 삭제 대상
- **INTERVAL**: 삭제 작업 실행 주기

## 예시

```sql
-- 1일 보존, 1시간마다 삭제 실행
CREATE RETENTION policy_1d_1h DURATION 1 DAY INTERVAL 1 HOUR;

-- 30일 보존, 1일마다 삭제 실행
CREATE RETENTION policy_30d DURATION 30 DAY INTERVAL 1 DAY;

-- 1개월 보존, 3일마다 삭제 실행
CREATE RETENTION policy_1m_3d DURATION 1 MONTH INTERVAL 3 DAY;

-- 1시간 보존, 10분마다 삭제 실행 (테스트용)
CREATE RETENTION policy_1h_10m DURATION 1 HOUR INTERVAL 10 MIN;

-- 30초 보존, 3초마다 삭제 (개발·디버깅용)
CREATE RETENTION policy_30s_3s DURATION 30 SEC INTERVAL 3 SEC;
```

## 정책 목록 확인

```sql
SELECT * FROM M$RETENTION;
```

```
USER_ID     POLICY_NAME       DURATION    INTERVAL
--------------------------------------------------
1           POLICY_1D_1H      86400       3600
1           POLICY_30D        2592000     86400
1           POLICY_1M_3D      2592000     259200
```

DURATION과 INTERVAL 값은 초(second) 단위로 저장됩니다.

## 설계 가이드

- **DURATION**: 비즈니스 요구사항과 규제 보관 의무(예: 3개월, 1년)를 기준으로 결정
- **INTERVAL**: 데이터 삭제 빈도. 너무 짧으면 시스템 부하 증가, 너무 길면 불필요한 데이터가 오래 남음. 일반적으로 DURATION의 1/10 ~ 1/30 수준 권장
- 동일한 정책을 여러 테이블에 공유 적용 가능
