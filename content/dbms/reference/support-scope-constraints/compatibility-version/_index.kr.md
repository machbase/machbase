---
type: docs
title: '18.6.10 버전 및 호환성'
weight: 110
toc: true
---

Machbase 8.7.0 버전의 하위 호환성, 업그레이드 주의사항, 지원 OS/플랫폼 정리입니다.

## 8.7.0 버전 하위 호환성

### 클라이언트 드라이버 호환

| 서버 버전 | 8.5 클라이언트 드라이버 | 8.7.0 클라이언트 드라이버 |
|-----------|:---------------------:|:---------------------:|
| 8.7.0 서버 | 제한적 호환 | 완전 호환 |
| 8.5 서버 | 완전 호환 | 하위 호환 |

- 8.7.0 서버에 8.5 클라이언트 드라이버를 사용하면 일부 신규 기능이 동작하지 않을 수 있습니다.
- 구버전 서버 또는 드라이버 조합에서는 Nullable 메타데이터가 기존 값이나 판정 불가
  값으로 반환될 수 있습니다. 이 값에 의존하는 애플리케이션은 서버와 SDK를 모두
  8.7.0으로 업그레이드하십시오.
- CAST의 모든 대상 타입과 길이·정밀도 옵션을 사용하는 SQL은 8.7.0 서버에서 지원됩니다.
  Cluster Edition에서는 모든 cluster node를 CAST를 지원하는 동일 버전으로 구성해야 합니다.
  자세한 문법과 변환 규칙은 [CAST 함수](../sql/dictionary/functions-full/#cast)를 참고하십시오.
- 8.7.0의 Standard Edition에서는 SELECT/JOIN 계획 개선으로 테이블 스캔 순서와 정렬하지
  않은 결과의 반환 순서가 구버전과 달라질 수 있습니다. 결과 순서가 필요하면 `ORDER BY`를
  사용하고, 업그레이드 후에는 [SELECT/JOIN 옵티마이저](/dbms/performance-tuning/performance-query-tuning/#select-join-optimizer)의
  절차에 따라 결과와 실행 계획을 함께 확인하십시오.
- 8.7.0 JDBC 드라이버는 다중 호스트 URL에서 연결 단계의 I/O 오류가 발생하면 다음
  호스트로 연결을 시도합니다. 구버전 드라이버가 첫 호스트의 일부 socket 오류에서 연결을
  종료하는 환경에서는 8.7.0 JDBC 드라이버로 교체하고
  [다중 호스트 연결](/dbms/development-tools-integration/jdbc/#jdbc-multi-host)의 URL과
  timeout 설정을 확인하십시오.
- 서버와 SDK의 버전 조합에 따른 기능 차이는 [서버와 SDK 호환성](../compatibility-xma-protocol/)을 참고하십시오.

<a id="removed-features-870"></a>

### 8.7.0에서 제거된 기능

Machbase 8.7.0은 다음 기능과 인터페이스를 제공하지 않습니다. 제거된 설정, SQL, C API에는
호환 계층이 없으므로 업그레이드 전에 설정 파일, 운영 SQL, 애플리케이션을 변경해야 합니다.

| 8.5 기능 또는 인터페이스 | 8.7.0 상태 | 사용자 영향 | 전환 방법 |
|--------------------------|------------|-------------|-----------|
| DB HTTP/REST (`/machbase`, `/machiot`, 포트 5657) | 제거 | 기존 HTTP 조회와 Append 요청을 사용할 수 없음 | SQLCLI, ODBC, JDBC, Python, Go, Node.js 또는 .NET SDK 사용 |
| WebAdmin/MWA, 정적 ClusterAdmin UI | 제거 | 웹 UI와 관련 시작 스크립트를 사용할 수 없음 | 서버·클러스터 명령행 도구 사용 |
| STREAM SQL과 카탈로그 | 제거 | 등록된 STREAM을 실행하거나 상태를 조회할 수 없음 | Collector, Fluentd 또는 애플리케이션 작업으로 처리 |
| Result Cache | 제거 | 결과 캐시 설정, 상태 조회, flush 명령을 사용할 수 없음 | 인덱스·ROLLUP·쿼리 최적화 또는 애플리케이션 캐시 사용 |
| `machcli.h`와 `MachCLI*()` | 제거 | 기존 C/C++ 소스와 바이너리를 그대로 사용할 수 없음 | Machbase SQLCLI 또는 ODBC로 이전 |

다음 항목은 이름이 비슷하지만 계속 지원합니다.

| 유지 기능 | 설명 |
|-----------|------|
| Machbase SQLCLI | `<machbase_sqlcli.h>`의 `SQL*` API. ODBC와는 별도의 API 집합입니다. |
| ODBC, JDBC 및 언어별 SDK | Python, Go, Node.js, .NET을 포함한 지원 드라이버를 계속 사용할 수 있습니다. |
| MachEngine API | 기존 `Mach*` API를 계속 사용할 수 있습니다. |
| PVO Cache | 실행 계획 객체를 재사용하는 캐시이며 제거된 Result Cache와 다른 기능입니다. |
| Coordinator/Collector 관리 REST | 데이터 SQL REST가 아닌 관리용 API입니다. Coordinator의 `/admin/` 경로를 계속 사용할 수 있습니다. |

#### 업그레이드 전에 설정 파일 정리

다음 프로퍼티가 8.7.0의 `machbase.conf`에 남아 있으면 알 수 없는 프로퍼티로 처리되어 서버가
시작되지 않습니다. 바이너리를 교체하기 전에 모두 삭제합니다.

```text
HTTP_AUTH
HTTP_ENABLE
HTTP_MAX_MEM
HTTP_PORT_NO
RS_CACHE_APPROXIMATE_RESULT_ENABLE
RS_CACHE_ENABLE
RS_CACHE_MAX_MEMORY_PER_QUERY
RS_CACHE_MAX_MEMORY_SIZE
RS_CACHE_MAX_RECORD_PER_QUERY
RS_CACHE_TIME_BOUND_MSEC
STREAM_THREAD_COUNT
STREAM_WAIT_MS
```

기존 STREAM 정의가 필요하면 8.5 서버를 중지하기 전에 `V$STREAMS`와 관련 SQL을 별도로
기록합니다. 8.7.0에서는 `SYS_STREAM_STMTS`, `V$STREAMS`, `V$HTTP_STATUS`,
`V$RS_CACHE_LIST`, `V$RS_CACHE_STAT`이 등록되지 않습니다.

업그레이드 후 다음 쿼리의 결과가 각각 `0`인지 확인합니다.

```sql
SELECT COUNT(*) AS removed_property_count
FROM V$PROPERTY
WHERE NAME IN (
    'HTTP_AUTH', 'HTTP_ENABLE', 'HTTP_MAX_MEM', 'HTTP_PORT_NO',
    'RS_CACHE_APPROXIMATE_RESULT_ENABLE', 'RS_CACHE_ENABLE',
    'RS_CACHE_MAX_MEMORY_PER_QUERY', 'RS_CACHE_MAX_MEMORY_SIZE',
    'RS_CACHE_MAX_RECORD_PER_QUERY', 'RS_CACHE_TIME_BOUND_MSEC',
    'STREAM_THREAD_COUNT', 'STREAM_WAIT_MS'
);

SELECT COUNT(*) AS removed_table_count
FROM V$TABLES
WHERE NAME IN (
    'SYS_STREAM_STMTS', 'V$HTTP_STATUS', 'V$RS_CACHE_LIST',
    'V$RS_CACHE_STAT', 'V$STREAMS'
);
```

### DDL 동시성 호환

Machbase 8.7.0은 Edition에 따라 DDL 동시 실행 정책이 다릅니다.

| Edition | 8.7.0 동작 | `DDL_LOCK_TIMEOUT` |
|---------|------------|--------------------|
| Standard | 서로 다른 독립 객체의 DDL을 동시에 수행할 수 있음 | 제공함. 기본값 `0`(NOWAIT) |
| Cluster | 기존 카탈로그 범위 DDL 정책 유지 | 제공하지 않음 |

Standard Edition에서 같은 객체나 직접 관련된 객체의 DDL이 충돌하면 기본 설정에서는
`ERR-02031: Resource busy (<object>)`가 즉시 반환됩니다. 이전 버전의 대기 동작을 전제로 작성한
배포 스크립트는 업그레이드 후 다음 중 하나를 명시적으로 적용합니다.

- 배포 세션에서 `ALTER SESSION SET DDL_LOCK_TIMEOUT = seconds`로 제한된 대기 시간을 설정합니다.
- `ERR-02031`에만 제한된 재시도와 대기 간격을 적용합니다.
- 재시도 전에 객체 상태를 다시 확인하고 `already exists`, 권한, 문법 오류는 재시도하지 않습니다.

자세한 충돌 관계와 설정 방법은
[DDL 동시성과 잠금](/dbms/reference/sql/syntax-dictionary-sql/ddl-syntax/#ddl-concurrency)을
참고하십시오.

### 백업 파일 호환성

| 백업 파일 버전 | 8.7.0에서 복원 | 비고 |
|--------------|:-----------:|------|
| 8.5 백업 | O | `MOUNT` 또는 `machadmin -r` 사용 |
| 8.7.0 백업 | O | |
| 8.4 이하 백업 | △ | 버전에 따라 다름, 테스트 필요 |

## 업그레이드 시 주의사항

### 8.5 → 8.7.0 업그레이드

1. **업그레이드 전 백업 필수**: `BACKUP DATABASE`로 전체 백업을 수행하십시오.
2. **드라이버 업데이트**: 서버 업그레이드 후 클라이언트 드라이버(JDBC, ODBC, Python 등)도 8.7.0 버전으로 업데이트하십시오.
3. **설정 파일 검토**: 제거된 HTTP, STREAM, RS Cache 프로퍼티를 `machbase.conf`에서 삭제하십시오.
4. **SDK 호환성**: 이전 버전 SDK는 8.7.0 서버와 제한적으로 호환됩니다. 가급적 서버와 SDK를 함께 업그레이드하십시오.

### 업그레이드 절차

```bash
# 1. 현재 버전 백업
machsql -e "BACKUP DATABASE INTO DISK = '/data/backup/pre_upgrade_backup'"

# 2. 서버 중지
machadmin -s

# 3. 8.7.0 바이너리 설치 (패키지 또는 tarball)

# 4. 서버 시작
machadmin -u

# 5. 버전 확인
machsql -e "SELECT * FROM v$version"
```

## 지원 OS 및 플랫폼

| 플랫폼 | 아키텍처 | 지원 여부 | 최소 요구 버전 |
|--------|---------|:--------:|-------------|
| Linux (RHEL / CentOS) | x86_64 | O | 7.x 이상 |
| Linux (Ubuntu) | x86_64 | O | 18.04 LTS 이상 |
| Linux (Debian) | x86_64 | O | 10 이상 |
| Linux | ARM64 (aarch64) | O | |
| Windows | x86_64 | X | 미지원 |
| macOS | x86_64 / ARM64 | X | 미지원 (개발 환경 용도 제외) |

## 지원 종료 (EOL) 정책

- 각 메이저 버전은 출시 후 최소 2년간 보안 패치를 제공합니다.
- 8.4 이하 버전은 지원이 종료되었습니다.
- 지원 버전 현황은 Machbase 공식 사이트를 확인하십시오.

## 버전 확인 방법

```sql
-- 서버 버전 확인
SELECT * FROM v$version;

-- 서버 정보 확인
SELECT * FROM v$property WHERE name LIKE '%VERSION%';
```
