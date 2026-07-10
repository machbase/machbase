---
title: '7.10 _arrival_time 시간 모델'
weight: 100
toc: true
---

LOG 테이블의 `_arrival_time` 컬럼 동작 방식과 조회 방법을 다룬다.


<a id="time-model-arrival-time"></a>

## _arrival_time 시간 모델

LOG 테이블을 생성하면 `_arrival_time` 컬럼이 자동으로 추가된다. 레코드가 서버에 도착한 시각을 나노초 정밀도로 기록하는 컬럼이다.

### 특성

- **자동 생성**: DDL에 명시하지 않아도 추가된다.
- **나노초 정밀도**: DATETIME 타입, 나노초(ns) 단위
- **서버 수신 시각**: 클라이언트가 INSERT/APPEND한 시점에 서버가 기록한다.
- **추가 전용**: 값을 변경할 수 없다.
- **정렬 기준**: 내부적으로 `_arrival_time` 기준으로 데이터가 정렬된다.

### 조회 예시

```sql
-- 최근 1시간 이내 로그 조회
SELECT _arrival_time, level, msg
FROM sys_log
WHERE _arrival_time >= NOW - 3600000000000
ORDER BY _arrival_time DESC;

-- 특정 시간 범위 조회 (문자열 사용)
SELECT *
FROM web_access_log
WHERE _arrival_time BETWEEN '2024-01-01 00:00:00' AND '2024-01-02 00:00:00';
```

### 주의사항

- **이벤트 발생 시각과 도착 시각의 차이**: 네트워크 지연이 있으면 두 값이 달라질 수 있다. 이벤트 발생 시각을 별도 컬럼으로 저장할 것을 권장한다.
- **역순 입력 불가**: `_arrival_time`은 서버 수신 순서이므로 과거 시각으로 역삽입이 불가능하다.

```sql
-- 이벤트 발생 시각을 별도 컬럼으로 관리하는 패턴
CREATE TABLE app_log (
    event_time DATETIME,   -- 실제 이벤트 발생 시각
    level      VARCHAR(8),
    msg        VARCHAR(1024)
    -- _arrival_time은 자동 추가됨
);
```
