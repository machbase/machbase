---
type: docs
title: '11.11.1 Fluentd 입력 파이프라인'
weight: 10
toc: true
aliases:
  - /dbms/log-table-usage/fluentd-pipeline/
---

검증된 Machbase output plugin을 사용해 Fluentd record를 TAG 또는 LOG 테이블로 전달합니다.
plugin 설치 방법과 option은 배포된 Ruby·Fluentd·plugin 버전의 문서를 정본으로 사용합니다.

<a id="pipeline-fluentd"></a>
<a id="log-logs-pipeline-connection-fluentd"></a>

## 문서 소유 범위

| 내용 | 정본 |
|---|---|
| Fluentd에서 Machbase로 전달하는 흐름과 검증 | 이 페이지 |
| LOG schema, 검색과 lifecycle | [LOG 테이블 활용](/dbms/log-table-usage/) |
| SDK·Append 지원 비교 | [SDK 기능 지원 범위](../../sdk-support-scope/) |
| plugin option과 호환 버전 | 설치한 plugin의 해당 버전 문서 |

확인되지 않은 source, filter, output 조합을 지원 기능으로 가정하지 않습니다.

## 배포 순서

1. 원본 record, 대상 테이블, 컬럼 순서, timestamp 의미와 encoding을 고정합니다.
2. plugin이 현재 Ruby와 Fluentd 버전을 지원하는지 확인합니다.
3. Fluentd host에서 Machbase native port와 최소 권한 계정의 연결을 검증합니다.
4. buffer, flush, retry, overflow와 실패 record 보존 정책을 정합니다.
5. 작은 표본을 전송하고 행 수, 시간 범위와 대표 값을 확인합니다.
6. Fluentd를 재시작해 중복 전송과 유실 처리 결과를 확인합니다.

## LOG 테이블 예제

`_ARRIVAL_TIME`은 서버가 자동으로 제공하므로 사용자 컬럼으로 선언하지 않습니다.

```sql
CREATE LOG TABLE fluentd_event (
    source_time DATETIME,
    host_name   VARCHAR(64),
    level       VARCHAR(16),
    message     VARCHAR(1024)
);
```

record field를 정확한 컬럼 순서에 맞추거나 plugin이 문서화한 named mapping을 사용합니다.
비밀번호와 개인키를 source control의 Fluentd 설정에 기록하지 않습니다.

## 전달 보장

- 성공 acknowledgement 뒤에만 source checkpoint를 전진시킵니다.
- retry 횟수와 backoff에는 상한을 둡니다.
- 영구적인 schema·type 오류는 자동 재시도하지 않고 별도 경로로 격리합니다.
- 재시작 후 같은 record가 다시 전달될 수 있으므로 중복 정책을 정의합니다.
- buffer 파일의 소유자, 권한, 용량과 보존 기간을 운영 정책으로 관리합니다.

## 결과 검증

```sql
SELECT COUNT(*) AS row_count,
       MIN(source_time) AS min_source_time,
       MAX(source_time) AS max_source_time
  FROM fluentd_event;
```

Fluentd output 건수, retry·격리 record와 테이블 행 수를 함께 비교합니다. 시간값, NULL,
문자열 encoding과 숫자 타입도 표본 row로 왕복 검증한 뒤 운영에 반영하십시오.
