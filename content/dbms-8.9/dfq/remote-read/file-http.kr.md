---
type: docs
title: '12.12.1 파일 URI와 HTTP(S)'
weight: 10
toc: true
---

같은 CSV를 먼저 서버 파일로 확인한 뒤 HTTP로 조회합니다. HTTPS에서는 서버 인증서의
신뢰 체인과 호스트명을 검사합니다. 실습 인증서를 신뢰하려면 생성된 PEM을 SYS의
호출별 옵션으로 지정하거나 서버 기본 CA 설정을 사용합니다.

## 로컬 경로와 file URI

| 입력 | 해석 |
|---|---|
| `/data/a%20b.csv` | 파일명에 문자 `%20`이 포함됩니다. |
| `file:///data/a%20b.csv` | URI에서 공백을 나타내며 `a b.csv`를 엽니다. |
| `file://localhost/data/events.csv` | 서버의 로컬 파일을 엽니다. |
| `file:///C:/data/events.csv` | Windows 서버에서 C 드라이브의 파일을 엽니다. |

일반 상대경로는 서버 작업 디렉터리를 기준으로 해석합니다. 로컬 file URI에는 authority를
생략하거나 `localhost`를 사용합니다. 변환된 파일에는 디렉터리 권한과 OS 권한이 적용됩니다.
URI의 path는 한 번 해석하며, 원격 객체 키의 역슬래시는 `%5C`로 인코딩합니다.
SQL 문자열 안의 작은따옴표는 두 번 씁니다.

**기존 서버 경로로 CSV 읽기**

```sql
SELECT id, v
FROM READ(
    'source=/tmp/dfq-read-lab/files/measurements.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG'
)
ORDER BY id;
```

**파일 URI로 같은 CSV 읽기**

```sql
SELECT id, v
FROM READ(
    'source=file:///tmp/dfq-read-lab/files/measurements.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG'
)
ORDER BY id;
```

**URI에서 공백을 %20으로 나타내기**

```sql
SELECT id, v
FROM READ(
    'source=file:///tmp/dfq-read-lab/files/a%20b.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG'
)
ORDER BY id;
```

**경로에서 %20을 그대로 사용하기**

```sql
SELECT id, v
FROM READ(
    'source=/tmp/dfq-read-lab/files/a%20b.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG'
)
ORDER BY id;
```

## HTTP CSV와 HTTPS Parquet

`format`과 `type.*`를 지정하면 실습의 두 컬럼을 같은 SQL 타입으로 비교할 수 있습니다.
HTTPS 예제의 `source.tls.ca_file`은 SYS만 지정합니다. 일반 사용자는 관리자가 설정한
서버 CA와 원격 읽기 권한을 사용합니다.

**HTTP에서 CSV 읽기**

```sql
SELECT id, v
FROM READ(
    'source=http://127.0.0.1:18080/measurements.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG'
)
ORDER BY id;
```

**HTTPS에서 Parquet 읽기**

```sql
SELECT id, v
FROM READ(
    'source=https://127.0.0.1:18443/measurements.parquet',
    'format=parquet',
    'source.tls.ca_file=/tmp/dfq-read-lab/ca.pem'
)
ORDER BY id;
```

## 조회 범위와 원본 확인

`LIMIT 1`은 결과를 한 행으로 제한합니다. 원격 전송은 파일 전체를 받습니다.
고정 원본을 확인하려면 `source.consistency=strong`과 제공받은 SHA-256 revision을
사용합니다. revision은 `sha256:` 뒤에 대문자 16진수 64자리로 지정합니다.
해시가 다른 파일은 `SOURCE_CHANGED`로 확인할 수 있습니다.

**HTTP Parquet에서 한 행 반환하기**

```sql
SELECT id, v
FROM READ(
    'source=http://127.0.0.1:18080/measurements.parquet',
    'format=parquet'
)
LIMIT 1;
```

**HTTP 원본을 SHA-256으로 확인하기**

```sql
SELECT id, v
FROM READ(
    'source=http://127.0.0.1:18080/measurements.parquet',
    'format=parquet',
    'source.consistency=strong',
    'source.expected_revision=sha256:451626398ABD8635EB32FDAC6CA854748A80EDDDFCCDBD33DE31F9AFA4D5BB34'
)
ORDER BY id;
```

`http.sql`에는 집계, JSONL, RAW 저장 바이트, 빈 CSV·TSV 헤더, 허용된 주소로의
redirect 예제도 있습니다. RAW의 TOTAL_BYTES는 원본 Parquet 바이트 길이입니다. URL에 query가
있으면 원격 요청에 사용하고, fragment는 요청에 보내지 않습니다.
전체 조회는 `/tmp/dfq-read-lab/sql/http.sql`을 실행합니다. 실패하면
[오류와 해결](../../troubleshooting/#remote-read-errors)을 확인합니다.

## 공개 데이터로 서버의 인터넷 연결 확인

서버가 인터넷에 연결되어 있고 공개 인증서를 신뢰하도록 CA를 설정했다면 SYS 세션에서 Vega의 Barley JSON과 NOAA GHCN의
공개 S3 데이터를 읽을 수 있습니다. NOAA 파일은 gzip으로 압축한 헤더 없는 CSV입니다.
아래 쿼리는 공개 주소를 사용하므로 AWS 계정은 필요하지 않습니다.

```sql
-- 공개 Vega 데이터의 JSON 행 수
SELECT COUNT(*) AS N
FROM READ('source=https://raw.githubusercontent.com/vega/vega-datasets/main/data/barley.json',
          'format=json');

-- NOAA GHCN 공개 S3 객체에서 헤더 없는 gzip CSV 읽기
SELECT COUNT(*) AS N
FROM READ('source=s3://noaa-ghcn-pds/csv.gz/1763.csv.gz',
          'source.s3.auth=anonymous', 'source.s3.region=us-east-1',
          'source.s3.endpoint=https://s3.us-east-1.amazonaws.com',
          'source.s3.addressing_style=virtual',
          'format=csv', 'compression=gzip', 'header=false', 'auto_detect=false');
```

Barley JSON의 조회 결과는 120행, NOAA 파일은 730행입니다. 공개 파일이 갱신되거나
서버의 외부 연결이 제한된 경우에는 로컬 실습으로 결과를 재현합니다.
[공개 데이터 SQL](/assets/dbms-8.9/dfq/remote-read/sql/public.sql) ·
[Vega Barley 원본](https://github.com/vega/vega-datasets/blob/main/data/barley.json) ·
[NOAA GHCN 공개 데이터](https://registry.opendata.aws/noaa-ghcn/)
