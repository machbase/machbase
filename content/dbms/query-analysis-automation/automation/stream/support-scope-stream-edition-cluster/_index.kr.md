---
type: docs
title: 'STREAM 지원 범위'
weight: 70
---

## Edition별 지원

| 기능 | Standard Edition | Cluster Edition |
|------|:---:|:---:|
| STREAM_CREATE | O | X |
| STREAM_DROP | O | X |
| STREAM_START | O | X |
| STREAM_STOP | O | X |
| STREAM_EXECUTE | O | X |
| V$STREAMS 조회 | O | X |

> STREAM은 **Standard Edition 전용** 기능입니다. Cluster Edition에서 STREAM 프로시저를 실행하면 오류가 반환됩니다.

## 소스 테이블 제약

| 소스 테이블 타입 | STREAM 사용 가능 |
|----------------|:---:|
| LOG | O |
| TAG | X |
| RDB | X |
| VOLATILE | X |
| LOOKUP | X |

STREAM의 소스(`FROM` 대상)는 반드시 LOG 테이블이어야 합니다.

## 지원 쿼리 패턴

| 패턴 | 지원 여부 |
|------|:---:|
| `INSERT INTO ... SELECT ... FROM log_table` | O |
| `INSERT INTO ... SELECT ... FROM log_table WHERE condition` | O |
| `INSERT INTO ... SELECT ... FROM log_table GROUP BY ... BY n SECOND` | O |
| `INSERT INTO ... SELECT ... FROM log_table GROUP BY ... BY USER` | O |
| 서브쿼리 / JOIN | 제한적 |
| 집계 함수 (주기 없음) | X |

## 동시 실행 STREAM 수

서버당 동시에 실행 가능한 STREAM 수는 시스템 설정에 따라 달라집니다. 운영 중 STREAM이 많아지면 각 STREAM의 `LAST_ELAPSED_MSEC`를 모니터링해 부하를 확인하세요.

## STREAM과 ROLLUP 비교

| 항목 | STREAM | ROLLUP |
|------|--------|--------|
| 대상 테이블 | LOG | TAG |
| 집계 방식 | INSERT...SELECT (사용자 정의) | 고정 집계 (MIN/MAX/SUM/COUNT) |
| 실행 트리거 | 데이터 입력 감지 | wakeup 스케줄 |
| Edition | Standard만 | Standard + Cluster |
| 재구성(Rebuild) | 미지원 | 지원 |
