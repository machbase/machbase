---
type: docs
title: 'Collector 수집 성능 튜닝'
weight: 20
---

Collector는 외부 데이터 소스(센서, 장비, 시스템 로그 등)에서 데이터를 수집하여 Machbase에 적재하는 컴포넌트입니다. 수집 성능 튜닝은 데이터 유실 없이 최대 처리량을 달성하는 것이 목표입니다.

## 수집 성능 영향 요소

| 요소 | 영향 | 튜닝 방향 |
|------|------|-----------|
| 수집 주기 | 짧을수록 실시간성 높음, 오버헤드 증가 | 데이터 특성에 맞게 설정 |
| 배치 크기 | 클수록 처리량 높음, 메모리 사용량 증가 | 1,000~10,000건 권장 |
| 네트워크 레이턴시 | 높을수록 지연 증가 | 로컬 또는 LAN 환경 권장 |
| 병렬 스레드 수 | 많을수록 처리량 증가, CPU 경쟁 발생 | Active 노드 수 × 1~2배 |
| Append 버퍼 크기 | 클수록 flush 횟수 감소 | 메모리와 내구성 균형 |

## 권장 수집 파이프라인 설계

**단일 소스 파이프라인**

```
[Sensor/Device] → [Collector Thread] → [Machbase Active Node]
```

**다중 소스 병렬 파이프라인 (권장)**

```
[Source 1] → [Collector Thread 1] ─┐
[Source 2] → [Collector Thread 2] ─┼→ [Machbase Active 노드들]
[Source 3] → [Collector Thread 3] ─┘
```

## 배치 크기와 flush 주기

| 데이터 특성 | 배치 크기 | flush 주기 | 설명 |
|------------|:---:|:---:|------|
| 고빈도 센서 (100Hz 이상) | 10,000건 | 1초 | 처리량 우선 |
| 일반 IoT (1Hz) | 1,000건 | 1~5초 | 균형 |
| 이벤트 로그 (불규칙) | 500건 | 5~10초 | 지연 허용 |
| 실시간 알람 | 1~10건 | 즉시 flush | 레이턴시 우선 |

## 병렬 스레드 수 설정

Cluster Edition에서는 Active 노드 수에 맞게 병렬 스레드를 설정합니다.

```
권장 스레드 수 = Active 노드 수 × 1~2
예: Active 4노드 → 4~8개 Collector 스레드
```

Standard Edition에서는 CPU 코어 수를 기준으로 합니다.

```
권장 스레드 수 = CPU 코어 수의 1/2 ~ 2/3
예: 8코어 → 4~5개 스레드
```

## 병목 원인 진단

수집 속도가 느릴 때 Append 병목인지 네트워크 병목인지 구분합니다.

```sql
-- 현재 실행 중인 Append 관련 문장 확인
SELECT user_id, query, state, elapsed_time
  FROM v$stmt
 WHERE query LIKE '%APPEND%'
   AND state != 'IDLE';
```

**Append 병목 징후:**
- CPU 사용률이 낮고 I/O wait가 높음 (`iostat -x 1`)
- → 인덱스 줄이기, SSD 사용, flush 주기 늘리기

**네트워크 병목 징후:**
- `ping` 또는 `iperf` 측정값이 예상보다 높음
- Collector 로그에 connection timeout 반복
- → Collector와 Machbase를 같은 서버/네트워크에 배치

## Collector 큐 모니터링

Collector가 처리하지 못한 데이터가 큐에 쌓이는지 모니터링합니다.

```bash
# Collector 로그에서 지연 또는 큐 관련 메시지 확인
grep -i "queue\|delay\|overflow\|slow" /var/log/machbase/collector.log | tail -50
```

큐가 지속적으로 증가한다면:
1. 배치 크기 늘리기
2. 병렬 스레드 추가
3. flush 주기 조정
4. 데이터 소스 측 전송 속도 제한 검토
