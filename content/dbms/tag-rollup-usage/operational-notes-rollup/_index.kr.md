---
title: '6.16 ROLLUP 운영 주의사항'
weight: 150
toc: true
---
ROLLUP 운영 주의사항에 해당하는 세부 문서를 모았습니다.


<a id="operational-notes-rollup"></a>

## 운영 주의사항

### ROLLUP 주기와 wakeup 주기

ROLLUP 주기(INTERVAL)와 wakeup 주기는 다릅니다.

- **ROLLUP 주기**: 집계되는 시간 버킷 크기 (예: 1분 = 1분짜리 구간을 집계)
- **wakeup 주기**: 백그라운드 스레드가 깨어나 새 데이터 유무를 확인하는 간격

기본값은 둘이 같지만, wakeup 주기를 더 짧게 설정하면 더 자주 데이터를 처리합니다. 이 경우 CPU 부하가 소폭 증가합니다.

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

ROLLUP 테이블은 내부적으로 KEYVALUE 테이블로 관리됩니다. `SHOW TABLES`로 확인 가능합니다.

```sql
-- ROLLUP 관련 내부 테이블 확인
SHOW TABLES;
-- _TAG_ROLLUP_SEC, _TAG_ROLLUP_MIN, _TAG_ROLLUP_HOUR 등이 KEYVALUE 타입으로 표시
```

### 메타 버전 업그레이드

Machbase 버전 업그레이드 후 ROLLUP 메타 버전이 변경될 수 있습니다. 서버 최초 기동 시 카탈로그가 자동 갱신됩니다. 갱신 실패 시 서버를 중지하고 새 DB를 생성한 뒤 ROLLUP을 재생성하세요.

### 일반적인 운영 체크리스트

- [ ] V$ROLLUP에서 ENABLED=1, RUN_STATE 정상 확인
- [ ] LAST_ELAPSED_MSEC로 집계 소요 시간 모니터링
- [ ] `show rollupgap`으로 처리 지연(gap) 확인
- [ ] 주기적으로 ROLLUP 조회 응답 시간 점검
- [ ] 대량 적재 후 FORCE 실행 여부 확인
