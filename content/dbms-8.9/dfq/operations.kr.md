---
type: docs
title: '12.10 권한과 운영'
weight: 100
toc: true
---

로컬 파일 조회에는 DB와 서버 OS 권한이 필요합니다. 원격 조회는 실제 접속 주소와
인증 출처의 권한을 사용합니다. VIEW의 READ 권한은 실행 사용자 기준으로 검사합니다.

## 디렉터리 권한

SYS가 기존 절대 디렉터리에 권한을 부여합니다. analyst는 이미 존재하는 사용자 예입니다.

```sql
GRANT READ ON DIRECTORY '/srv/dfq' TO analyst;
REVOKE READ ON DIRECTORY '/srv/dfq' FROM analyst;
```

해당 디렉터리와 하위 디렉터리의 일반 파일을 허용하며 명시 READ·인용 FROM·raw·inspect에
같은 경계를 적용합니다. OS 읽기 권한도 필요합니다. 여러 파일·glob는 각 파일을 검사합니다.
REVOKE는 다음 실행·새 open부터 적용하고 이미 열린 cursor는 기존 수명대로 끝납니다.

승인 경로에는 심볼릭 링크나 중간 부모 이동을 사용하지 않습니다. Windows는 drive가 있는
로컬 절대 경로를 사용하며 UNC·장치 경로·junction/reparse point 등 안전하게 승인할 수 없는
경로를 허용하지 않습니다. 상대 경로는 클라이언트가 아니라 서버의 작업 디렉터리 기준입니다.
파일 존재를 알아내기 위한 권한 없는 조회도 허용하지 않습니다.

## 파일 변경과 일관성

best_effort는 실행 중 파일 내용 전체를 불변 snapshot으로 보장하지 않습니다.
고정 내용이 필요하면 지원되는 source.consistency=strong을 사용합니다. 큰 source·다중
source는 복사·검사·임시 공간 비용이 있으므로 필요한 범위와 reader의 한도를 확인합니다.

원본 revision·mapping token과 구조 schema ID는 서로 다릅니다. 재조회에서
SOURCE_CHANGED·MAPPING_CHANGED가 나면 오래된 token을 다른 설정에 재사용하지 않고
다시 탐색합니다. SQL 입력에는 파일 snapshot 옵션을 붙이지 않습니다.

## 병렬·메모리·임시 디스크

CSV/TSV·JSON/JSONL의 parallel=auto/true/false와 threads 상한은 reader에 따라 적용됩니다.
CPU_COUNT와 실효 작업자 수를 확인하며 auto가 항상 빠르다고 가정하지 않습니다.
Parquet·NumPy·MCAP·HDF5·LeRobot의 동기 실행을 같은 병렬 계약으로 해석하지 않습니다.

MAX_QPX_MEM, SQL 결과의 타입 한도, reader별 레코드·해제·spool·metadata 예산을 함께 적용합니다.
메모리가 부족하면 지원 연산은 임시 디스크로 전환할 수 있지만 모든 decoder의 내부 heap에
동일한 hard cap을 보장하지는 않습니다. 오류·디스크 부족 시 잘린 결과를 성공으로 취급하지 않습니다.

## 취소와 측정

QUERY_TIMEOUT, SQLCancel 또는 관리 연결의 세션 취소를 사용하고 열린 cursor를 정리합니다.
취소된 요청의 일부 행을 완전한 결과로 사용하지 않습니다.
EXPLAIN FULL은 실제 쿼리를 실행하므로 부하가 생깁니다. prepare·추론·실행·전체 fetch와
디코딩·후처리 시간을 분리합니다. 단순 집계와 전체 원문 전송의 시간을 비교하지 않습니다.

LIMIT 성공은 파일 전체 검사의 성공이 아닙니다. 압축 chunk의 손상은 해당 chunk를 읽을 때
발견될 수 있습니다. LeRobot 미디어의 목록 조회는 실제 영상의 존재·내용·시간 정합성을
모두 확인한 것이 아닙니다.

## CSV/TSV 병렬 처리와 실행 통계

threads는 1~32의 동시 제출 작업 상한이고 기본은 min(4,CPU_COUNT)입니다.
CPU_COUNT 기본 1이면 auto도 순차이며 threads=1도 순차입니다. auto는 입력 크기·실측
압축률을 사용해 디코딩 입력이 8 MiB 이상으로 추정되거나 관측되면 병렬 처리를 시작합니다.
true는 작은 입력에서도 병렬 경로를 요청하지만 실제 작업자 사용을 보장하지 않습니다.

```sql
EXPLAIN FULL SELECT id,label FROM READ('/srv/dfq/sensor.csv',
 'parallel=auto','threads=4','type.label=TEXT') ORDER BY label LIMIT 3;
```

CSV_PARALLEL의 requested·effective·used·worker_rows·auto_decision을 확인합니다.
작은 샘플은 순차가 정상입니다. workers는 실행 중 사용한 고유 작업자 수여서 threads와
같지 않을 수 있습니다. decoded_bytes는 UTF-8 디코딩 후의 논리 바이트이며 물리 디스크 I/O가 아닙니다.

TEXT_TOPN은 K=LIMIT+OFFSET, seen·stored·peak_rows·peak_bytes·transitions를 표시합니다.
후보 메모리가 부족하면 임시 디스크 정렬로 전환하며, 작은 LIMIT이 모든 입력의 읽기와
표현식 검사를 없애지 않습니다. GROUP_CONCAT 결과의 32 KiB 한도는 유지합니다.

## EXPLAIN FULL의 READ 실행 계수

- `READ_SCAN`은 reader가 순회에서 반환한 행을 셉니다. `row=` 선택 이전에 순회한 행도
  포함하며 선택 행의 위치를 다시 읽어 값을 구성할 때는 행 수가 늘지 않습니다.
- `READ_INPUT.source_bytes`는 DATA 실행 중 source 인터페이스가 반환한 바이트입니다.
  `decoded_bytes`는 CSV·JSON의 변환 입력, NPY·NPZ의 NPY 디코더 입력,
  MCAP의 디코딩된 메시지 입력을 셉니다. HDF5·Parquet은 디코더가 전달한 수치 값과
  문자열·바이너리의 논리 바이트를 셉니다. LeRobot은 단계 Parquet 파일의 계수를 합산합니다.
- `READ_ARRAY`는 SQL 결과에 전달한 native ARRAY payload를 기록합니다.

## 원격 ENDPOINT 읽기 권한 {#endpoint-read-permissions}

로컬 경로와 `file://`에는 디렉터리 권한을 적용합니다. 원격 요청에서는 SYS가 현재
데이터베이스의 기존 사용자에게 **실제 접속 주소와 자격증명 출처**의 조합을 허용합니다.
VIEW로 읽을 때도 실행 사용자의 권한을 확인합니다. VIEW 자체의 SELECT 권한도 필요합니다.

| 인증 절 | 실제 요청에 사용하는 인증 |
|---|---|
| 생략 | 공개 HTTP(S), 익명 S3·FTP(S), 사전 서명 HTTPS URL, TFTP |
| `PROFILE 'production'` | 해당 AWS 공유 파일 프로필의 키 |
| `USING ENVIRONMENT` | 서버의 AWS 자격증명 환경변수 |
| `USING NETRC` | 서버 .netrc의 FTP·FTPS 계정 |

실습 서비스가 생성한 `/tmp/dfq-read-lab/sql/grant.sql`은 디렉터리,
공개 HTTP, 같은 S3 주소의 두 인증 출처, FTPS 계정과 VIEW의 SELECT 권한을 각각
설정합니다. 다음은 문서의 실습 포트를 기준으로 한 원격 권한 부분입니다.

```sql
GRANT READ ON ENDPOINT 'http://127.0.0.1:18080' TO DFQ_REMOTE_LAB;
GRANT READ ON ENDPOINT 'https://localhost:19000' PROFILE 'dfq-lab' TO DFQ_REMOTE_LAB;
GRANT READ ON ENDPOINT 'https://localhost:19000' USING ENVIRONMENT TO DFQ_REMOTE_LAB;
GRANT READ ON ENDPOINT 'ftps://127.0.0.1:18990' USING NETRC TO DFQ_REMOTE_LAB;
```

- 스킴·호스트·유효 포트를 정규화해 비교합니다. `https://files.example`과
  `https://files.example:443`은 같은 권한 대상입니다. 주소에 경로와 호스트 패턴을
  넣어 권한을 나누지 않습니다.
- `s3://`는 변환 후 실제 HTTP(S) 주소를 사용합니다. virtual 방식은 버킷이 포함된
  호스트, path 방식은 endpoint 호스트가 권한 대상입니다. SQL에서 주소를 덮어쓰면
  변경한 주소에 맞는 권한을 부여합니다.
- `AWS_PROFILE`에서 접속 설정을 읽더라도 키를 환경변수에서 가져오면 `USING ENVIRONMENT`
  권한이 필요합니다. 실제 인증 출처에 맞춰 승인합니다.
- 원격 요청 전과 redirect 목적지마다 권한을 검사합니다. 자격증명 또는 사전 서명을
  사용하는 요청은 다른 접속 주소로 redirect할 수 없습니다. HTTPS에서 HTTP로의
  전환도 거부합니다.
- `REVOKE`는 다음 실행에 적용되며 이미 준비한 SQL을 다시 실행할 때도 확인합니다.

```sql
REVOKE READ ON ENDPOINT 'http://127.0.0.1:18080' FROM DFQ_REMOTE_LAB;
```

`analyst.sql`로 권한 적용 후 결과를 확인합니다. 위 권한을 회수한 뒤 같은 VIEW를
조회하면 `ACCESS_DENIED`가 발생합니다. 문법은 [ENDPOINT READ 권한](/kr/dbms-8.9/reference/sql/syntax/user-auth-syntax/#read-on-endpoint)을 참고합니다.

## TLS와 계정 파일 {#remote-read-auth}

| 서버 설정 | 역할 |
|---|---|
| `READ_REMOTE_CA_FILE` | TLS에서 서버 인증서 검증에 사용할 PEM CA 번들 경로 |
| `READ_REMOTE_NETRC_FILE` | FTP·FTPS의 호스트별 계정 정보를 찾을 서버 측 파일 경로 |

CA 번들을 생략하면 Linux는 `/etc/ssl/certs/ca-certificates.crt`, macOS는
`/etc/ssl/cert.pem`, Windows는 `MACHBASE_HOME/conf/read-remote-ca.pem`을
사용합니다. HTTPS, HTTPS S3, 명시적 FTP TLS, FTPS는 신뢰 체인과 호스트명을 검사합니다.

관리자는 .netrc 파일에 대상 호스트의 `machine` 항목을 등록합니다.

```text
machine archive.example
    login read-service
    password <FTP_PASSWORD>
```

파일 권한은 서버 실행 계정이 읽을 수 있도록 제한합니다. 파일을 지정하지 않았거나
호스트 일치 항목이 없으면 익명 FTP(S)를 사용합니다. 파일 읽기가 실패하거나 해당
항목의 계정이 불완전하면 오류가 발생합니다. `default`로 다른 호스트의 계정을
대체하지 않습니다. URL의 `user:password@`나 READ 옵션에 직접 계정을 넣지 않습니다.

SYS는 READ 호출에 `source.tls.ca_file`과 `source.ftp.netrc_file`을 지정해 해당
호출에서 사용할 서버 파일을 선택할 수 있습니다. 생략하면 서버 설정을 적용합니다.
일반 사용자는 호출별 서버 파일 경로를 지정할 수 없으며 VIEW를 통해서도 해당 제한을
적용합니다. [FTP TLS 옵션](../remote-read/ftp-tftp/)을 참고합니다.

## 원격 다운로드와 임시 공간 {#remote-read-spool}

서버는 원격 원본 바이트를 `DBS_PATH` 아래의 비공개 임시 파일에 순차 저장합니다.
기본 위치는 `MACHBASE_HOME/dbs`입니다. 전체 다운로드가 완료되면 포맷 reader가
그 파일에서 CSV 자동 감지, Parquet footer 읽기, RAW 반환과 재스캔을 수행합니다.
HTTP(S)와 S3는 전체 GET을 사용합니다. `LIMIT 1`이라도 첫 결과 전에 전체 원본을
전송합니다. 연결에서 사용하는 전송 버퍼와 임시 디스크 용량은 별도로 계획합니다.
Linux에서는 열린 임시 파일의 디렉터리 항목을 제거하므로 파일명 목록에 보이지 않습니다.

`READ_REMOTE_MAX_SPOOL_BYTES`의 기본값은 **1 TB(1,000,000,000,000바이트)**입니다.
같은 SQL 문의 원격 파일, 중첩 SQL 소스와 다른 READ 임시 저장을 합산합니다.
임시 파일을 만들거나 쓸 수 없으면 `IO_ERROR`, 한도를 넘으면 `LIMIT_EXCEEDED`입니다.
쿼리가 끝나거나 오류·취소·연결 종료가 발생하면 파일과 예약 공간을 반환합니다.

| 실행 방식 | 다운로드 수명 |
|---|---|
| `machsql -f`의 일반 SELECT처럼 한 요청 안에서 준비·실행 | 동일 READ의 준비 단계 파일을 실행에 넘깁니다. |
| PREPARE와 EXECUTE를 분리 | 준비에서 스키마를 확인한 뒤 파일을 닫습니다. 실행마다 현재 권한·자격증명으로 원본을 받습니다. |

`source.consistency=strong` 또는 `source.expected_revision=sha256:...`를 지정하면
받은 원본 바이트의 SHA-256을 계산합니다. 해시가 다르면 `SOURCE_CHANGED`입니다.
기본 best_effort 임시 파일에는 공개 SHA-256 revision을 발급하지 않습니다.
실행 시 키를 다시 읽으므로 다음 실행에 새 자격증명이 적용될 수 있습니다.
환경변수를 바꾸려면 서버 프로세스에 변경 값이 전달되도록 설정합니다.

전송 중인 SQL을 중지하려면 별도 SYS 세션에서 `V$SESSION.ID`를 확인하고
`ALTER SYSTEM CANCEL SESSION <SID>`를 실행합니다. SQLCLI의 취소나 연결 종료로도
진행 중인 전송과 임시 공간이 정리됩니다. 중단된 파일은 reader에 전달하지 않습니다.
[원격 READ 오류 해결](../troubleshooting/#remote-read-errors)을 참고합니다.
