---
type: docs
title: '14.4 ALTER SYSTEM 운영'
weight: 40
toc: true
---

`ALTER SYSTEM`은 instance 전체에 영향을 줄 수 있는 관리자 명령입니다. 실행 전 대상
instance, 권한, 진행 중 작업, rollback 또는 해제 명령을 확인합니다. 전체 구문은
[system·session ALTER 구문](/dbms/reference/sql/syntax-dictionary-sql/system-session-alter-syntax/)을
정본으로 사용합니다.

## 공통 절차

1. 현재 server와 database, release를 확인합니다.
2. 관련 session·statement·backup·checkpoint 상태를 기록합니다.
3. 명령의 blocking·I/O·memory 영향을 확인합니다.
4. maintenance 창과 실패 시 조치를 정합니다.
5. 실행 직후 결과와 관련 virtual table·log를 확인합니다.

<a id="checkpoint"></a>

## CHECKPOINT

```text
ALTER SYSTEM CHECKPOINT;
```

checkpoint는 storage I/O를 증가시킬 수 있습니다. backup·shutdown 전 필요성을 검토하고
동시 대량 입력과 query 영향을 관찰합니다. 단순히 “느리다”는 이유로 반복 실행하지 않습니다.

<a id="check-disk-usage"></a>

## CHECK DISK_USAGE

```text
ALTER SYSTEM CHECK DISK_USAGE;
```

filesystem 상태와 database storage metadata의 점검이 필요한 경우 사용합니다. 실행 전
free space와 mount 상태를 확인하고 결과 log를 검토합니다. 내부 file을 직접 수정해 수치를
맞추지 않습니다.

<a id="install-license"></a>

## INSTALL LICENSE

```text
ALTER SYSTEM INSTALL LICENSE;
ALTER SYSTEM INSTALL LICENSE = '/absolute/path/license.dat';
```

license file의 출처, 대상 instance, edition, 만료일을 확인합니다. file 내용은 문서·log에
복사하지 않고 permission을 제한합니다. 설치 뒤 `V$LICENSE_INFO`와 새 connection으로
적용을 확인합니다.

<a id="kill-cancel-session"></a>

## KILL과 CANCEL SESSION

```text
ALTER SYSTEM CANCEL SESSION session_id;
ALTER SYSTEM KILL SESSION session_id;
```

먼저 `V$SESSION`과 `V$STMT`에서 user, client IP, SQL, 상태를 확인합니다. `CANCEL`은 실행
중 statement 중단을 우선 시도할 때, `KILL`은 connection 자체를 종료해야 할 때
검토합니다. transaction·Appender·application retry가 만드는 중복과 rollback 영향을
확인합니다.

<a id="freeze-unfreeze"></a>

## FREEZE와 UNFREEZE

```text
ALTER SYSTEM FREEZE;
ALTER SYSTEM UNFREEZE;
```

freeze는 공개 backup 기능으로 대체할 수 없는 filesystem snapshot 절차에서만 검토합니다.
실행 전 허용되는 read·write 범위와 최대 freeze 시간을 정하고, 어떤 오류 경로에서도
`UNFREEZE`를 실행할 담당자와 확인 절차를 준비합니다. session을 freeze 상태로 방치하지
않습니다.

<a id="flush-ager"></a>

## FLUSH AGER

```text
ALTER SYSTEM FLUSH AGER;
```

삭제된 공간의 정리 지연을 조사할 때 사용 여부를 검토합니다. retention·DELETE 상태와
storage 여유를 먼저 확인하고, 정상 background 작업을 반복 강제하지 않습니다.

<a id="flush-pvo-cache"></a>

## FLUSH PVO_CACHE

```text
ALTER SYSTEM FLUSH PVO_CACHE;
```

cached plan을 비우면 이후 query가 다시 parse·optimize됩니다. schema·plan 문제를
분리 진단할 때만 실행하고, 동시 query의 latency spike를 관찰합니다. cache flush를
지속적인 성능 문제의 해결책으로 사용하지 않습니다.

<a id="flush-sys-stat"></a>

## FLUSH SYS_STAT

```text
ALTER SYSTEM FLUSH SYS_STAT;
```

누적 통계를 초기화하기 전에 필요한 baseline을 저장합니다. 초기화 시각을 monitoring에
기록해 rate 계산과 장애 분석이 왜곡되지 않게 합니다.

<a id="flush-page-cache"></a>

## FLUSH PAGE_CACHE

```text
ALTER SYSTEM FLUSH PAGE_CACHE;
```

page cache flush는 후속 query의 I/O와 latency를 크게 바꿀 수 있습니다. cold-cache
비교나 제한된 진단에서만 사용하고 운영 peak에는 실행하지 않습니다.

## 권한과 감사

최소 관리자 계정으로 실행하고 명령, 대상, 시각, 실행자, 사유, 결과를 감사 기록에
남깁니다. 예제의 session ID, path, property 값을 그대로 운영 명령으로 사용하지 않습니다.
