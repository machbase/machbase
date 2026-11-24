---
type: docs
title: '12.12.2 FTP·FTPS·TFTP'
weight: 20
toc: true
---

파일 서버가 제공하는 전송 방식을 확인하고 `READ` 주소를 선택합니다. 서버에 설치한
CA와 계정 파일을 사용하는 절차는 [TLS와 계정 파일](../../operations/#remote-read-auth)을
참고합니다.

| 방식 | 주소와 옵션 | 계정·권한 |
|---|---|---|
| 익명 FTP | `ftp://host/path.csv` | 인증 절을 생략한 endpoint 권한 |
| 계정 FTP | `ftp://host/path.csv` | 호스트에 맞는 .netrc 계정과 `USING NETRC` 권한 |
| 명시적 TLS | `ftp://host/path.csv`, `source.ftp.tls=required` | FTP endpoint, 신뢰 CA, 사용한 인증 출처의 권한 |
| Implicit FTPS | `ftps://host/path.csv` | FTPS endpoint, 신뢰 CA, 사용한 인증 출처의 권한 |
| TFTP | `tftp://host/path.csv` | 인증 절을 생략한 endpoint 권한 |

`source.ftp.tls`는 `none` 또는 `required`입니다. FTP 기본은 `none`입니다.
`required`는 제어 연결의 TLS 전환과 데이터 연결 보호를 요구합니다. 전환에 실패하면
오류가 발생합니다. FTPS는 연결 시작부터 TLS를 사용하므로 별도 전환 옵션이 필요하지
않습니다. `ftps://`에 `none`을 지정하거나 TFTP에 FTP 옵션을 지정하면 오류입니다.

## 실행 예제

전용 실습 서버의 설정 파일에서 CA와 .netrc를 준비합니다. 다음 SYS 예제의 호출별 옵션은
실습에서 만든 서버 파일을 선택합니다. 익명 FTP 예제는 계정이 지정되지 않은 `localhost`
주소를 사용합니다. 평문 FTP의 계정과 데이터는 전송 중 암호화되지 않습니다.

**익명 FTP로 CSV 읽기**

```sql
SELECT id, v
FROM READ(
    'source=ftp://localhost:18210/measurements.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG'
)
ORDER BY id;
```

**FTP에서 .netrc 계정으로 읽기**

```sql
SELECT id, v
FROM READ(
    'source=ftp://127.0.0.1:18210/measurements.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG',
    'source.ftp.netrc_file=/tmp/dfq-read-lab/ftp.netrc'
)
ORDER BY id;
```

**명시적 FTP TLS로 CSV 읽기**

```sql
SELECT id, v
FROM READ(
    'source=ftp://127.0.0.1:18211/measurements.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG',
    'source.ftp.tls=required',
    'source.tls.ca_file=/tmp/dfq-read-lab/ca.pem',
    'source.ftp.netrc_file=/tmp/dfq-read-lab/ftp.netrc'
)
ORDER BY id;
```

**연결 시작부터 TLS를 사용하는 FTPS**

```sql
SELECT id, v
FROM READ(
    'source=ftps://127.0.0.1:18990/measurements.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG',
    'source.tls.ca_file=/tmp/dfq-read-lab/ca.pem',
    'source.ftp.netrc_file=/tmp/dfq-read-lab/ftp.netrc'
)
ORDER BY id;
```

**TFTP에서 작은 CSV 읽기**

```sql
SELECT id, v
FROM READ(
    'source=tftp://127.0.0.1:18069/measurements.csv',
    'format=csv',
    'header=true',
    'type.id=LONG',
    'type.v=LONG'
)
ORDER BY id;
```

각 조회는 동일한 `ID`, `V` 100행을 반환합니다. FTP의 파일 형식 처리 방법은
[포맷별 문서](../../formats/)에서 확인합니다.
전체 조회는 `/tmp/dfq-read-lab/sql/ftp.sql`을 실행합니다.
