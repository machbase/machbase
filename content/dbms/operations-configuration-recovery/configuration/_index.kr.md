---
type: docs
title: '13.3 설정 운영'
weight: 30
toc: true
---

설정 변경은 현재값, 변경 근거, 적용 방식, 검증값, rollback을 기록하고 한 번에 하나씩
진행합니다. property 목록과 기본값을 이 페이지에 복제하지 않고 현재 release의
[설정 레퍼런스](/dbms/reference/configuration/dictionary-configuration/)를 정본으로
사용합니다.

<a id="file-config-configuration"></a>

## 설정 파일

기본 설정 파일은 `$MACHBASE_HOME/conf/machbase.conf`입니다. package·service 구성에 따라
다른 파일을 사용할 수 있으므로 시작 명령과 실제 환경을 확인합니다.

변경 전에는 다음을 기록합니다.

- 파일 경로, 소유자, permission
- 변경할 property의 현재 파일값과 `V$PROPERTY` 값
- 단위와 허용 범위
- runtime 변경 가능 여부와 restart 필요 여부
- 관련 node·instance 범위
- rollback 값과 검증 SQL

비밀번호, AUTH KEY, license 내용을 일반 설정 백업이나 작업 기록에 포함하지 않습니다.

<a id="alter-start-restart-configuration-runtime"></a>

## Runtime 변경과 restart

`ALTER SYSTEM SET`은 지원되는 일부 property만 runtime에 변경합니다. 문서에 예시가 있다는
이유로 임의 property를 실행하지 않습니다.

```sql
SELECT NAME, VALUE
FROM V$PROPERTY
ORDER BY NAME;
```

1. 설정 레퍼런스에서 dynamic 여부를 확인합니다.
2. maintenance 범위와 영향받는 connection·query를 정합니다.
3. 현재값을 저장합니다.
4. staging 또는 제한된 workload에서 한 property만 변경합니다.
5. 응답 시간, 처리량, memory·I/O와 오류를 비교합니다.
6. 유지할 값은 설정 파일에도 반영해 restart 후 되돌아가지 않게 합니다.
7. restart 후 `V$PROPERTY`와 기능 테스트로 적용을 확인합니다.

<a id="parameters-configuration"></a>

## Property 찾기

```sql
SELECT NAME, VALUE
FROM V$PROPERTY
WHERE NAME LIKE 'PVO_CACHE%'
ORDER BY NAME;
```

정확한 이름을 알고 있을 때는 `NAME = '...'`로 조회합니다. 이름이 비슷한 property를
추정해 설정하지 않습니다.

<a id="memory-configuration"></a>

## Memory 설정

process 상한, table space·cache, 입력 buffer, query·session의 일시 memory를 하나의
예산으로 봅니다. OS와 같은 host의 다른 process에 필요한 memory도 남깁니다.

- 정상·peak workload의 resident memory와 available memory
- swap 발생 여부와 증가 시각
- 동시 query·Appender·session 수
- PVO, Min-Max, LOOKUP·VOLATILE 등 cache 사용량
- index 생성, 정렬, 집계 같은 일시 작업

고정 비율이나 예시 byte 값을 그대로 적용하지 않습니다.

<a id="network-session-configuration"></a>

## Network와 session

listener 주소·포트, 최대 session, connect·query timeout은 application connection 수와
장애 격리 요구사항을 기준으로 정합니다. 방화벽과 binding을 별도 검증하고, 최대 session을
늘리기 전에 connection leak과 pool 설정을 확인합니다.

```sql
SELECT ID, USER_NAME, USER_IP, LOGIN_TIME, CLIENT_TYPE
FROM V$SESSION
ORDER BY LOGIN_TIME DESC;
```

<a id="storage-checkpoint-configuration"></a>

## Storage와 checkpoint

`DBS_PATH`, checkpoint, direct I/O, I/O thread 관련 설정은 data 위치와 recovery 시간에
직접 영향을 줍니다. 운영 data file을 수동 이동하거나 다른 경로를 추정하지 않습니다.

- 실제 data·backup 경로와 filesystem을 확인합니다.
- checkpoint 시간과 device latency를 같은 시각에서 비교합니다.
- restart가 필요한 설정은 service 중단·복구 절차를 준비합니다.
- 변경 후 정상 restart와 backup·restore를 검증합니다.

<a id="timezone"></a>

## Timezone

시간 문자열을 입력·표시할 timezone을 server, command-line tool, SDK에서 일관되게
설정합니다. epoch 단위와 `DATETIME` 정밀도를 별도로 확인하고, 같은 값의 입력·조회 왕복
테스트를 수행합니다.

<a id="timezone-server-configuration"></a>
<a id="timezone-timezone-server-configuration"></a>

## Server timezone

server 기본 timezone property의 정확한 이름과 형식은 설정 레퍼런스에서 확인합니다. 변경
후 새 connection에서 `SHOW TIMEZONE`과 표본 `DATETIME` 조회로 적용을 확인합니다. 기존
connection의 session 설정이 즉시 바뀐다고 가정하지 않습니다.

<a id="machsql-z"></a>
<a id="timezone-machsql-z"></a>

## machsql `-z`

```bash
"$MACHBASE_HOME/bin/machsql"   -s 127.0.0.1 -P 5656   -u APP_USER -p "$MACH_SAMPLE_PASSWORD"   -z +0900
```

입력·출력 문자열이 해당 offset으로 해석·표시되는지 표본으로 확인합니다.

<a id="machloader-z"></a>
<a id="timezone-machloader-z"></a>

## machloader `-z`

```bash
"$MACHBASE_HOME/bin/machloader"   -s 127.0.0.1 -P 5656   -u APP_USER -p "$MACH_SAMPLE_PASSWORD"   -z +0900 -i -t SENSOR_LOG -d /data/sensor.csv
```

CSV 원본의 timezone과 date format을 함께 문서화합니다.

<a id="connection-cli-jdbc-net-timezone"></a>
<a id="timezone-connection-cli-jdbc-net-timezone"></a>

## SDK connection timezone

지원 option 이름은 SDK마다 다릅니다. [11장 개발 및 애플리케이션 연동](/dbms/development-tools-integration/)
에서 해당 driver의 connection option을 확인하고, 입력·조회·pool 재사용 뒤에도 같은
timezone이 적용되는지 검증합니다.

## 변경 기록

| 항목 | 기록 |
|------|------|
| 대상 | host, instance, node, database |
| 변경 | property와 이전·새 값 |
| 근거 | baseline과 목표 |
| 적용 | runtime 또는 restart |
| 검증 | SQL, workload, OS 지표 |
| rollback | 값, 실행 순서, 담당자 |

확인되지 않은 추천값이나 과거 release의 기본값을 현재 설정으로 간주하지 않습니다.
