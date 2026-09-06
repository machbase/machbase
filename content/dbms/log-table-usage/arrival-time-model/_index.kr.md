---
title: '7.10 _arrival_time 시간 모델'
weight: 100
toc: true
---

LOG 테이블의 `_arrival_time` 컬럼 동작 방식과 조회 방법을 다룹니다.


<a id="time-model-arrival-time"></a>

## _arrival_time 시간 모델

LOG 테이블을 생성하면 `DATETIME` 타입의 `_arrival_time` 컬럼이 자동으로 추가됩니다.
입력 시 값을 생략하면 서버가 수신 시각을 기록합니다. 지원되는 입력 구문으로 시각을 명시할
수도 있으므로, 이 컬럼이 항상 실제 네트워크 수신 시각과 같다고 가정하지 않습니다.

### 특성

- **자동 생성**: DDL에 명시하지 않아도 추가됩니다.
- **저장 단위**: DATETIME 타입으로 나노초(ns) 단위 시각을 표현합니다. 실제 시계의 측정 정밀도와는 구분합니다.
- **기본값**: 입력 경로에서 시각을 생략하면 서버 시각을 사용합니다.
- **입력 후 변경 불가**: LOG 테이블은 UPDATE를 지원하지 않으므로 저장한 값을 수정할 수 없습니다.
- **시간 범위 기준**: `DURATION`과 LOG의 기간 보존 삭제는 `_arrival_time`을 기준으로 합니다.
- **결과 정렬**: 출력 순서가 필요하면 `ORDER BY _arrival_time`을 명시합니다.

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

- **이벤트 발생 시각과 도착 시각의 차이**: 네트워크 지연이 있으면 두 값이 달라질 수 있습니다. 이벤트 발생 시각을 별도 컬럼으로 저장할 것을 권장합니다.
- **명시 시각 입력**: 데이터 이관이나 재현 테스트에서 `_arrival_time`을 지정할 수 있습니다.
  이 경우 입력 시각의 순서를 맞추고 사용 중인 입력 도구의 제약을 확인합니다. 과거 이벤트를
  일반적으로 수집할 때는 실제 발생 시각을 별도 컬럼에 저장합니다.

명시 입력 예제는 [LOG 조회와 분석](../query-analysis/), SQL 입력 규칙은
[DML 구문 사전](/dbms/reference/sql/syntax-dictionary-sql/dml-syntax/)을 참고하십시오.

```sql
-- 이벤트 발생 시각을 별도 컬럼으로 관리하는 패턴
CREATE LOG TABLE app_log (
    event_time DATETIME,   -- 실제 이벤트 발생 시각
    level      VARCHAR(8),
    msg        VARCHAR(1024)
    -- _arrival_time은 자동 추가됨
);
```
