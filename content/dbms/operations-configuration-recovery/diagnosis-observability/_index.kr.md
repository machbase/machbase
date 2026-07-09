---
type: docs
title: '13.4 관측과 진단'
weight: 40
---

Machbase 서버의 상태를 파악하고 문제를 진단하기 위해 두 가지 주요 도구를 제공합니다. 첫째는 `M$`로 시작하는 **메타 테이블**로 스키마 정의 정보를 조회합니다. 둘째는 `V$`로 시작하는 **가상 테이블(Virtual Table)**로 서버의 실시간 운영 상태를 조회합니다. 이 두 그룹과 함께 서버가 기록하는 **로그 파일**을 분석하면 대부분의 운영 상황에 대응할 수 있습니다.

## 주요 V$ 가상 테이블

| 카테고리 | 테이블 이름 | 주요 용도 |
|---------|-----------|---------|
| 세션/시스템 | V$SESSION | 현재 접속 세션 목록과 상태 |
| 세션/시스템 | V$STMT | 실행 중인 SQL 문과 상태 |
| 세션/시스템 | V$PROPERTY | 현재 서버 설정값 조회 |
| 세션/시스템 | V$SYSMEM | 시스템 메모리 사용량 |
| 세션/시스템 | V$SYSSTAT | 시스템 통계 정보 |
| Result Cache | V$RS_CACHE_LIST | 결과 캐시 목록 |
| Result Cache | V$RS_CACHE_STAT | 결과 캐시 통계 |
| 스토리지 | V$STORAGE_USAGE | 디스크 사용량 및 한계 비율 |
| 스토리지 | V$STORAGE_TABLES | 테이블별 스토리지 사용량 |
| 태그 Rollup | V$ROLLUP | Rollup 작업 상태 |
| 스트림 | V$STREAMS | Stream 쿼리 실행 상태 |
| 라이선스 | V$LICENSE_INFO | 라이선스 정보와 위반 상태 |

## 로그 파일 위치 요약

| 로그 파일 | 위치 | 용도 |
|---------|------|------|
| 서버 메인 로그 | `$MACHBASE_HOME/trc/machbase.trc` | 서버 동작 전반, 오류 기록 |
| machsql 이력 | `$MACHBASE_HOME/trc/machsql.history` | 대화형 SQL 실행 이력 |
| machloader 오류 | 실행 디렉터리 `machloader.err` | 적재 실패 레코드 |
| machloader 통계 | 실행 디렉터리 `machloader.log` | 처리 건수, 오류 건수 |
| Collector 로그 | `$MACHBASE_COLLECTOR_HOME/trc/` | Collector 수집 상태 |

모든 로그 파일은 기본적으로 `$MACHBASE_HOME/trc/` 디렉터리에 위치합니다. Trace Log 레벨은 `machbase.conf`의 `TRACE_LOG_LEVEL` 파라미터로 조정합니다.

## 이 섹션의 구성

- [진단과 로그](./log-diagnosis-logs/) — 서버 로그 파일의 종류와 분석 방법, Trace Log 설정, 각 도구별 로그
- [메타 테이블 활용](./item/) — M$ 메타 테이블을 이용한 스키마 정보 조회
- [가상 테이블 활용](./item-2/) — V$ 가상 테이블을 이용한 실시간 서버 상태 조회
- [모니터링과 용량 관리](./monitoring-capacity/) — 정기 점검 절차, 디스크·메모리 용량 관리, 장애 징후 확인
