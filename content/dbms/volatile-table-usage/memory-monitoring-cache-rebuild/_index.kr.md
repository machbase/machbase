---
title: '10.15 메모리 모니터링과 캐시 재구성'
weight: 150
toc: true
---

VOLATILE 테이블의 행 수와 메모리 한도를 확인하고 캐시를 재구성하는 절차를 설명합니다.

<a id="monitor-volatile-row-count"></a>

## 행 수 확인

테이블별 `COUNT(*)`와 업무 키의 표본 조회로 예상 범위를 벗어난 증가를 확인합니다. 시간
조건으로 다수 행을 임의 삭제하기보다, 영속 원본에서 다시 만들 수 있는 캐시는 전체
재구성을 고려합니다.

<a id="monitor-volatile-memory-view"></a>

## 메모리 상태 확인

다음 조회는 서버의 VOLATILE 저장소와 전체·세션 메모리 상태를 확인합니다.

```sql
SELECT * FROM V$STORAGE_DC_VOLATILE_TABLE;
SELECT * FROM V$SYSMEM;
SELECT * FROM V$SESMEM;
```

가상 테이블의 컬럼은 버전에 따라 달라질 수 있으므로 특정 내부 컬럼명에 의존하지 않습니다.

<a id="monitor-volatile-limit"></a>

## 메모리 한도 확인

```sql
SELECT NAME, VALUE
FROM V$PROPERTY
WHERE NAME = 'VOLATILE_TABLESPACE_MEMORY_MAX_SIZE';
```

한도를 변경하기 전에는 LOOKUP 사용량, 동시 쿼리 메모리, 운영체제 여유 메모리를 함께
검토합니다.

<a id="rebuild-volatile-cache"></a>

## 캐시 재구성

1. 기존 캐시의 행 수와 표본 값을 기록합니다.
2. 캐시를 사용하는 쓰기·조회 흐름의 전환 방식을 정합니다.
3. 테이블을 삭제하고 동일한 스키마로 생성합니다.
4. 영속 원본에서 정의된 범위만 다시 적재합니다.
5. 행 수, 최신 시각, 표본 키를 확인한 뒤 사용을 재개합니다.

원본 스키마에 따라 초기 적재 SQL이 달라지므로 존재하지 않는 고정 테이블을 가정한 예제는
제공하지 않습니다.

<a id="rebuild-volatile-startup"></a>

## 서버 시작 시 재구성

접속 호스트, 포트, 데이터베이스, 계정은 배포 환경에서 주입합니다. 비밀번호를 스크립트에
하드코딩하지 말고 설치 환경의 자격 증명 관리 방식을 사용합니다.

<a id="monitor-volatile-checklist"></a>

## 운영 체크리스트

- 행 수와 메모리 한도를 함께 관찰합니다.
- 캐시 재구성 SQL을 영속 원본의 현재 스키마에 맞춰 검증합니다.
- 재시작 후 자동 생성·초기 적재가 실제로 실행되는지 확인합니다.
- 실패 시 빈 캐시로 전환하거나 이전 서비스 상태를 유지하는 절차를 준비합니다.
