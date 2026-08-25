---
title: '6.16 ROLLUP 운영 주의사항'
weight: 150
toc: true
---

<a id="operational-notes-rollup"></a>

## 운영 주의사항

### ROLLUP 주기와 wakeup 주기

ROLLUP 주기(INTERVAL)와 wakeup 주기는 별개입니다.

- **ROLLUP 주기**: 집계되는 시간 버킷 크기 (예: 1분 = 1분짜리 구간을 집계)
- **wakeup 주기**: 백그라운드 스레드가 깨어나 새 데이터 유무를 확인하는 간격

기본값은 둘이 같지만, wakeup 주기를 더 짧게 설정하면 더 자주 데이터를 처리합니다. CPU 부하가 소폭 증가합니다.

```sql
-- 1분 ROLLUP을 10초마다 확인 (반응성 향상)
ALTER ROLLUP _tag_ru_1m SET WAKEUP INTERVAL 10 SEC;
```

규칙: wakeup 주기는 ROLLUP 주기의 약수여야 합니다.

### 대량 데이터 로드 후 처리

machloader나 Append API로 대량 데이터를 적재한 직후에는 ROLLUP 스레드가 아직 집계하지 않은 데이터가 많습니다.

```sql
-- 강제 집계 (완료까지 대기)
ALTER ROLLUP _tag_ru_1s FORCE;
ALTER ROLLUP _tag_ru_1m FORCE;
ALTER ROLLUP _tag_ru_1h FORCE;
```

### ROLLUP 생성 전 입력 데이터

ROLLUP 생성 이전에 입력된 데이터는 자동으로 집계되지 않습니다. ROLLUP 생성 후 `FORCE`를 실행하면 기존 데이터도 처리합니다.

```sql
-- ROLLUP 생성
CREATE ROLLUP _tag_ru_1h ON tag(value) INTERVAL 1 HOUR;

-- 기존 데이터도 집계
ALTER ROLLUP _tag_ru_1h FORCE;
```

### ROLLUP 삭제 순서

계층 ROLLUP은 반드시 역순으로 삭제합니다. 중간 ROLLUP을 먼저 삭제하려 하면 오류가 발생합니다.

```
올바른 순서: _ru_1h → _ru_1m → _ru_1s
```

### ROLLUP 스토리지 모니터링

ROLLUP의 상태와 처리 지연은 `V$ROLLUP`과 `SHOW ROLLUPGAP`으로 확인합니다. 시스템 저장
테이블의 이름이나 타입을 운영 스크립트에서 사용하지 마십시오.

### 업그레이드 후 확인

업그레이드 후에는 서버 기동 로그, `V$ROLLUP` 상태와 대표 집계 결과를 확인합니다. 카탈로그
또는 ROLLUP 오류가 발생해도 데이터베이스를 새로 만들지 말고, 먼저 백업을 보존한 상태에서
[업그레이드 절차](/dbms/installation-deployment-upgrade/upgrade/)와 기술 지원 절차를
따르십시오.

### 일반적인 운영 체크리스트

- [ ] V$ROLLUP에서 ENABLED=1, RUN_STATE 정상 확인
- [ ] LAST_ELAPSED_MSEC로 집계 소요 시간 모니터링
- [ ] `show rollupgap`으로 처리 지연(gap) 확인
- [ ] 주기적으로 ROLLUP 조회 응답 시간 점검
- [ ] 대량 적재 후 FORCE 실행 여부 확인
